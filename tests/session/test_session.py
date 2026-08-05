"""Phase 4 — Reader thread, command queue & snapshots (ADR-0005).

The seam: `Session` (reader thread as the single writer) driven two
ways — a pipe-based FakePty for deterministic queue/threading tests, and
a real pty with fake child programs for end-to-end coverage. Assertions
read the model only after the expected snapshot arrives (the reader
thread is quiescent between emissions), and check snapshot payloads
(dirty rows, viewport, cursor) as the GUI would receive them.

The session is Qt-free — snapshot delivery here is a plain callback +
an append-only list; the GUI layer (Slice B) bridges it to Qt signals.
"""

from __future__ import annotations

import os
import sys
import time

import pytest

from pyqterm.ptyspawn import Pty
from pyqterm.session import Session, Snapshot

from tests.pty.test_pty import wait_for


class FakePty:
    """A pipe-pair stand-in for `pyqterm.ptyspawn.Pty`: the test writes the
    child's "output" to the pipe; everything the session sends lands in
    `sent`; resizes are recorded. read() returns None once closed."""

    def __init__(self, rows: int = 24, cols: int = 80) -> None:
        self._r, self._w = os.pipe()
        os.set_blocking(self._r, False)
        self.sent = b""
        self.winsizes: list[tuple[int, int]] = []
        self.rows = rows
        self.cols = cols
        self.closed = False

    @property
    def master_fd(self) -> int:
        return self._r

    def read(self) -> bytes | None:
        if self.closed:
            return None
        try:
            data = os.read(self._r, 65536)
        except BlockingIOError:
            return b""
        except OSError:
            return None
        if data == b"":
            return None
        return data

    def send_data(self, data: bytes) -> None:
        self.sent += data

    def set_window_size(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols
        self.winsizes.append((rows, cols))

    def close(self) -> None:
        if not self.closed:
            self.closed = True
            os.close(self._r)
            os.close(self._w)

    def output(self, data: bytes) -> None:
        """Simulate the child writing `data`."""
        os.write(self._w, data)


def row_text(row) -> str:
    """The row's cells as text (trailing blanks stripped)."""
    return "".join(cell.data for cell in row.cells).strip()


def make_session(pty: object, **kwargs) -> Session:
    session = Session(pty, **kwargs)  # type: ignore[arg-type]
    session.start()
    return session


# -- Deterministic queue/threading tests (FakePty) ----------------------


def test_initial_snapshot_is_full() -> None:
    fake = FakePty()
    session = make_session(fake, lines=3, columns=4)
    try:
        assert wait_for(lambda: session.snapshots)
        snap = session.snapshots[0]
        assert snap.full
        assert snap.dirty_rows == ()
        assert snap.cursor == (0, 0)
        assert snap.scrollback_len == 0
        assert len(snap.rows) == 3
    finally:
        session.close()


def test_output_produces_incremental_snapshots() -> None:
    fake = FakePty()
    session = make_session(fake, lines=3, columns=4)
    try:
        fake.output(b"AB\n")
        assert wait_for(lambda: session.snapshots and session.snapshots[-1].dirty_rows)
        snap = session.snapshots[-1]
        assert not snap.full
        assert snap.dirty_rows == (0, 1)  # AB row + cursor's new row
        assert snap.content_changed  # the grid text changed
        assert row_text(snap.rows[0]) == "AB"
        assert snap.cursor == (1, 2)
    finally:
        session.close()


def test_send_data_posts_bytes_to_child() -> None:
    fake = FakePty()
    session = make_session(fake)
    try:
        session.send_data(b"ping\r")
        assert wait_for(lambda: fake.sent == b"ping\r")
    finally:
        session.close()


def test_process_runs_the_read_step_synchronously() -> None:
    """The benchmark seam: `process` performs the reader thread's
    per-read step (feed, flush, emit) in the caller's thread — the same
    observable behavior as a pty read, without the thread."""
    fake = FakePty()
    session = Session(fake, lines=3, columns=4)
    session.process(b"")  # the initial full emit, as _run does on start
    session.process(b"AB\n")
    assert session.snapshots  # emitted synchronously
    snap = session.snapshots[-1]
    assert not snap.full
    assert snap.dirty_rows == (0, 1)
    assert row_text(snap.rows[0]) == "AB"
    assert snap.cursor == (1, 2)


def test_resize_reflows_and_reaches_pty() -> None:
    fake = FakePty()
    session = make_session(fake, lines=10, columns=80)
    try:
        fake.output(b"ABCDEFGH")
        assert wait_for(lambda: session.snapshots and len(session.snapshots) > 1)
        session.resize(10, 4)
        assert wait_for(lambda: session.snapshots[-1].full)  # resize → full repaint
        assert fake.winsizes == [(10, 4)]
        assert session.screen.columns == 4
        lines = session.screen.render().split("\n")
        assert lines[0] == "ABCD"
        assert lines[1] == "EFGH"
    finally:
        session.close()


def test_scroll_commands_move_offset_and_emit_full() -> None:
    fake = FakePty()
    session = make_session(fake, lines=5, columns=4)
    try:
        # CRLF lines — one clean row each (LF-only would wrap mid-line).
        # The last line has no terminator, so no trailing row is consumed.
        fake.output(b"".join(f"L{i}\r\n".encode() for i in range(29)) + b"L29")
        assert wait_for(
            lambda: session.snapshots and session.snapshots[-1].scrollback_len == 25
        )

        session.scroll(5)
        assert wait_for(lambda: session.snapshots[-1].viewport_offset == 5)
        snap = session.snapshots[-1]
        assert snap.full
        assert snap.scrollback_len == 25
        assert row_text(session.screen.viewport_row(0)) == "L20"

        session.scroll_to_bottom()
        assert wait_for(lambda: session.snapshots[-1].viewport_offset == 0)
        assert row_text(session.screen.viewport_row(0)) == "L25"
    finally:
        session.close()


def test_cursor_move_is_snapshotted() -> None:
    fake = FakePty()
    session = make_session(fake, lines=10, columns=80)
    try:
        fake.output(b"AB\r\n")
        assert wait_for(lambda: session.snapshots and session.snapshots[-1].cursor == (1, 0))
        fake.output(b"\x1b[5;5H")  # CUP → cursor (4, 4)
        assert wait_for(lambda: session.snapshots[-1].cursor == (4, 4))
        snap = session.snapshots[-1]
        assert not snap.full
        assert snap.dirty_rows == (1, 4)  # old and new cursor rows repaint
        assert not snap.content_changed  # no text changed — only the cursor moved
    finally:
        session.close()


def test_cursor_visibility_flip_is_snapshotted() -> None:
    """DECTCEM ?25: a visibility flip repaints the cursor row (the block
    is painted over it) without changing text — the selection survives."""
    fake = FakePty()
    session = make_session(fake, lines=10, columns=80)
    try:
        fake.output(b"AB\r\n")
        assert wait_for(lambda: session.snapshots and session.snapshots[-1].cursor == (1, 0))
        fake.output(b"\x1b[?25l")  # hide the cursor
        assert wait_for(lambda: session.snapshots[-1].cursor_visible is False)
        snap = session.snapshots[-1]
        assert not snap.full
        assert snap.dirty_rows == (1,)  # the cursor row repaints (block erased)
        assert not snap.content_changed  # no text changed
        fake.output(b"\x1b[?25h")  # show it again
        assert wait_for(lambda: session.snapshots[-1].cursor_visible is True)
        assert session.snapshots[-1].dirty_rows == (1,)
    finally:
        session.close()


# -- End-to-end tests (real pty + fake child programs) ------------------


def test_child_output_lands_on_screen() -> None:
    pty = Pty([sys.executable, "-c", "print('HELLO', flush=True)"])
    session = make_session(pty)
    try:
        assert wait_for(lambda: "HELLO" in session.screen.render())
    finally:
        session.close()


def test_close_stops_thread_and_closes_pty() -> None:
    pty = Pty([sys.executable, "-c", "import time\ntime.sleep(60)\n"])
    session = make_session(pty)
    try:
        assert wait_for(lambda: session.is_alive)
    finally:
        session.close()
    assert not session.is_alive
    assert pty.read() is None  # master closed by the session


def test_child_exit_stops_reader_and_reaps() -> None:
    pty = Pty([sys.executable, "-c", "print('BYE', flush=True)\n"])
    session = make_session(pty)
    try:
        assert wait_for(lambda: "BYE" in session.screen.render())
        assert wait_for(lambda: not session.is_alive)
        assert pty.wait() == 0  # clean exit, no zombie
    finally:
        session.close()


def test_scrollback_len_reaches_snapshot() -> None:
    script = "".join(
        f"print('L{i}', end='\\r\\n', flush=True)\n" for i in range(29)
    ) + "print('L29', end='', flush=True)\n"
    pty = Pty([sys.executable, "-c", script])
    session = make_session(pty, lines=5, columns=80)
    try:
        assert wait_for(
            lambda: session.snapshots and session.snapshots[-1].scrollback_len == 25
        )
    finally:
        session.close()


# -- The headless milestone: a scripted fake-shell session --------------
# (spec: prompt → command echo → output → scroll-fill → ED3 clear,
# asserting screen + scrollback through render()/viewport_row, extended
# across the pty seam.)

FAKE_SHELL = (
    "import sys\n"
    "while True:\n"
    "    sys.stdout.write('> ')\n"
    "    sys.stdout.flush()\n"
    "    line = sys.stdin.readline()\n"
    "    if not line:\n"
    "        break\n"
    "    if line.strip() == 'clear':\n"
    "        sys.stdout.write('\\x1b[3J')  # ED3 — raw, no trailing newline\n"
    "    else:\n"
    "        sys.stdout.write('OK:' + line.strip() + '\\n')\n"
    "    sys.stdout.flush()\n"
)


def test_fake_shell_session_prompt_echo_output() -> None:
    pty = Pty([sys.executable, "-c", FAKE_SHELL], rows=10, cols=40)
    session = make_session(pty, lines=10, columns=40)
    try:
        # Prompt arrives without input.
        assert wait_for(lambda: session.screen.render().startswith("> "))
        # Typed line: the driver echoes it after the prompt, the shell
        # answers on the next row.
        session.send_data(b"hello\r")
        assert wait_for(lambda: "> hello" in session.screen.render())
        assert wait_for(lambda: "OK:hello" in session.screen.render())
        assert wait_for(lambda: session.screen.render().rstrip().endswith(">"))
    finally:
        session.close()


def test_fake_shell_session_scroll_fill_then_ed3() -> None:
    pty = Pty([sys.executable, "-c", FAKE_SHELL], rows=5, cols=40)
    session = make_session(pty, lines=5, columns=40)
    try:
        # Fill the screen and overflow into scrollback (CRLF lines).
        for i in range(10):
            session.send_data(f"line{i}\r".encode())
        assert wait_for(
            lambda: session.screen.scrollback_len > 0
            and "OK:line9" in session.screen.render()
        )
        history = session.screen.scrollback_len
        assert history > 0

        # ED3: the only runtime erasure of history (ADR-0006). The
        # shell's "clear" command emits the raw ESC[3J (the driver's
        # echo of typed control chars would mangle it as ^[).
        session.send_data(b"clear\r")
        assert wait_for(lambda: session.screen.scrollback_len == 0)
        assert session.screen.viewport_offset == 0
        # The live grid survives the clear.
        assert "> " in session.screen.render()
    finally:
        session.close()


def test_decset_mouse_modes_reach_snapshots() -> None:
    fake = FakePty()
    session = make_session(fake, lines=5, columns=10)
    try:
        assert wait_for(lambda: session.snapshots and session.snapshots[-1].full)
        fake.output(b"\x1b[?1000h\x1b[?1002h\x1b[?1003h\x1b[?1006h")
        assert wait_for(
            lambda: session.snapshots
            and session.snapshots[-1].mouse_1000
            and session.snapshots[-1].mouse_1006
        )
        snap = session.snapshots[-1]
        assert snap.mouse_1000 and snap.mouse_1002
        assert snap.mouse_1003 and snap.mouse_1006
        # DECRST clears the mirror; the other modes stay.
        fake.output(b"\x1b[?1006l")
        assert wait_for(lambda: session.snapshots and not session.snapshots[-1].mouse_1006)
        snap = session.snapshots[-1]
        assert snap.mouse_1000
    finally:
        session.close()


def test_mouse_modes_default_to_off() -> None:
    fake = FakePty()
    session = make_session(fake, lines=3, columns=4)
    try:
        assert wait_for(lambda: session.snapshots)
        snap = session.snapshots[0]
        assert not snap.mouse_1000 and not snap.mouse_1002
        assert not snap.mouse_1003 and not snap.mouse_1006
    finally:
        session.close()
