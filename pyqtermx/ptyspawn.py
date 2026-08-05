# -*- coding: utf-8 -*-
# Copyright (C) 2018-2026 Connet Information Technology Company, Shanghai.
"""The pty layer — Qt-free (ADR-0005).

A narrow `Pty` interface: spawn a child with its own session (setsid),
exchange bytes over a real pseudo-terminal, set the window size, and
reap the exit. It knows nothing about the emulator, the screen, or Qt —
the reader thread (the single writer) drives it, and tests drive it
directly against fake child programs.

The master fd is non-blocking: the reader thread select()s first, then
reads; `read()` returns None when the child has exited (EIO).
"""

from __future__ import annotations

import errno
import fcntl
import os
import pty
import signal
import struct
import sys
import termios
import time
from typing import Mapping, Sequence

#: The terminal type the child sees (spec: TUIs behave differently
#: without it).
DEFAULT_TERM = "xterm-256color"

#: Truecolor advertisement: apps (vim ≥ 8.1 with termguicolors, fish,
#: git-delta, bat, …) gate `38;2`/`48;2` output on `COLORTERM=truecolor`
#: — TERM=xterm-256color alone does not tell them we can render RGB.
COLORTERM = "truecolor"

#: TIOCSCTTY — the child acquires the pty as its controlling terminal.
#: Python's termios exposes it on some platforms only; the fallbacks
#: are the raw ioctl numbers (macOS: `_IOR('t', 97, int)`; Linux: 0x540E).
try:
    _TIOCSCTTY = termios.TIOCSCTTY
except AttributeError:
    _TIOCSCTTY = 0x20047461 if sys.platform == "darwin" else 0x540E


class Pty:
    """A pseudo-terminal pair with a spawned child.

    Spawning: fork, the child setsid()s (its own session — job control
    and Ctrl+C work), acquires the pty as its controlling terminal and
    foreground process group (ISIG needs a target), dups the slave onto
    0/1/2, and execs the command with `TERM=xterm-256color` and
    `COLORTERM=truecolor` forced (the parent's values are irrelevant to
    the session).
    """

    def __init__(
        self,
        command: Sequence[str] | None = None,
        *,
        env: Mapping[str, str] | None = None,
        rows: int = 24,
        cols: int = 80,
    ) -> None:
        self.rows = rows
        self.cols = cols
        master_fd, slave_fd = pty.openpty()
        os.set_blocking(master_fd, False)
        self._master_fd = master_fd
        self._closed = False
        self._exit_status: int | None = None

        cmd = list(command) if command is not None else [os.environ["SHELL"]]
        child_env = dict(os.environ)
        if env:
            child_env.update(env)
        # The child always sees a compatible TERM — the parent's value
        # is irrelevant to the session (spec: TUIs behave differently).
        # COLORTERM tells truecolor-gated apps (vim termguicolors, fish,
        # git-delta…) that 38;2/48;2 will render correctly. COLUMNS/LINES
        # too: some programs read them instead of the winsize ioctl.
        child_env["TERM"] = DEFAULT_TERM
        child_env["COLORTERM"] = COLORTERM
        child_env["COLUMNS"] = str(cols)
        child_env["LINES"] = str(rows)

        # macOS only propagates TIOCSWINSZ from the slave before a session
        # exists — set the initial size on the slave, then the child's
        # dup2'd 0/1/2 carry it (Linux propagates either way).
        self._set_winsize(rows, cols, slave_fd)
        pid = os.fork()
        if pid == 0:  # child
            try:
                os.setsid()
                for target in (0, 1, 2):
                    os.dup2(slave_fd, target)
                if slave_fd > 2:
                    os.close(slave_fd)
                os.close(master_fd)
                # The pty as the controlling terminal, the child as its
                # foreground process group: without these the line
                # discipline has no process group to signal, so ISIG
                # chars are never converted — Ctrl+C stays a byte
                # instead of SIGINT (the htop bug).
                fcntl.ioctl(0, _TIOCSCTTY, 0)
                os.tcsetpgrp(0, os.getpid())
                os.execvpe(cmd[0], cmd, child_env)
            except BaseException:
                os._exit(127)
        os.close(slave_fd)
        self.pid = pid

    # -- Read API --------------------------------------------------------

    @property
    def master_fd(self) -> int:
        """The master fd — the reader thread's select() surface."""
        return self._master_fd

    def read(self) -> bytes | None:
        """One non-blocking read of the child's output. Returns None
        when the child has exited (EIO on Linux, a 0-byte EOF read on
        macOS) or the pty is closed; b"" on a spurious EAGAIN (a select
        race)."""
        if self._closed:
            return None
        try:
            data = os.read(self._master_fd, 65536)
        except BlockingIOError:
            return b""
        except OSError as exc:
            if exc.errno in (errno.EIO, errno.EBADF):
                return None
            raise
        if data == b"" and not self.is_running():
            # macOS EOF: the slave is gone, so the child is gone too.
            return None
        return data

    def send_data(self, data: bytes) -> None:
        """Write bytes to the child (its stdin). A non-blocking master
        can take a short write when its buffer fills — loop until
        everything is written, retrying EAGAIN."""
        if self._closed:
            return
        while data:
            try:
                n = os.write(self._master_fd, data)
            except BlockingIOError:
                time.sleep(0.01)  # buffer full — wait and retry
                continue
            except OSError as exc:
                if exc.errno in (errno.EIO, errno.EBADF):
                    return
                raise
            data = data[n:]

    # -- Size ------------------------------------------------------------

    def set_window_size(self, rows: int, cols: int) -> None:
        """TIOCSWINSZ: the size the child sees (and SIGWINCHes on)."""
        self.rows = rows
        self.cols = cols
        if not self._closed:
            self._set_winsize(rows, cols, self._master_fd)

    @staticmethod
    def _set_winsize(rows: int, cols: int, fd: int) -> None:
        fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", rows, cols, 0, 0))

    # -- Lifecycle -------------------------------------------------------

    def is_running(self) -> bool:
        """Whether the child is still alive (WNOHANG check)."""
        if self._exit_status is not None:
            return False
        try:
            pid, status = os.waitpid(self.pid, os.WNOHANG)
        except ChildProcessError:
            return False
        if pid == 0:
            return True
        self._exit_status = os.waitstatus_to_exitcode(status)
        return False

    def wait(self) -> int | None:
        """Reap the child (WNOHANG): its exit status, or None while it
        is still running. Callers poll this — it never blocks."""
        self.is_running()
        return self._exit_status

    def signal(self, sig: int) -> None:
        """Send a signal to the child."""
        try:
            os.kill(self.pid, sig)
        except ProcessLookupError:
            pass

    def close(
        self, terminate_timeout: float = 3.0, kill_timeout: float = 2.0
    ) -> None:
        """Close the master and stop the child (spec US 21).

        Closing the master first delivers EOF/SIGHUP to a well-behaved
        child (the normal terminal way); a child still alive afterwards
        gets SIGTERM, a bounded wait, then SIGKILL as the fallback."""
        if not self._closed:
            self._closed = True
            try:
                os.close(self._master_fd)
            except OSError:
                pass
        if self.is_running():
            self.signal(signal.SIGTERM)
            self._wait_bounded(terminate_timeout)
        if self.is_running():
            self.signal(signal.SIGKILL)
            self._wait_bounded(kill_timeout)
        self.wait()

    def _wait_bounded(self, timeout: float) -> None:
        """Poll `wait()` until the child exits or `timeout` passes."""
        deadline = time.monotonic() + timeout
        while self.is_running() and time.monotonic() < deadline:
            time.sleep(0.01)
