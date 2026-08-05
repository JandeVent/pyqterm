"""Phase 4 — Keyboard modes `?1` (DECCKM) and `?2004` (bracketed paste).

The DEC private mode registry stores any private number generically; the
GUI's input path consults these two through the existing `mode(n,
private=True)` read seam (delivered to the GUI inside snapshots — ADR-0005).
This pins that set/reset through the emulator works and that the read
surface reports the mode.

The seam: `screen.mode()` — the same read the snapshot bundle uses.
"""

from __future__ import annotations

from tests.screen.test_scrollback import feed_scrollback

DECCKM = 1
BRACKETED_PASTE = 2004


def test_decckm_set_and_reset() -> None:
    screen = feed_scrollback("\x1b[?1h", lines=3, columns=4)
    assert screen.mode(DECCKM, private=True) is True
    screen = feed_scrollback("\x1b[?1h\x1b[?1l", lines=3, columns=4)
    assert screen.mode(DECCKM, private=True) is False


def test_bracketed_paste_set_and_reset() -> None:
    screen = feed_scrollback("\x1b[?2004h", lines=3, columns=4)
    assert screen.mode(BRACKETED_PASTE, private=True) is True
    screen = feed_scrollback("\x1b[?2004h\x1b[?2004l", lines=3, columns=4)
    assert screen.mode(BRACKETED_PASTE, private=True) is False


def test_keyboard_modes_default_off() -> None:
    screen = feed_scrollback("", lines=3, columns=4)
    assert screen.mode(DECCKM, private=True) is False
    assert screen.mode(BRACKETED_PASTE, private=True) is False


def test_keyboard_modes_do_not_disturb_screen_behavior() -> None:
    # Setting the keyboard modes must not move the cursor or touch the
    # grid — they are keyboard-side state only (glossary "Mode").
    screen = feed_scrollback("abc\x1b[?1h\x1b[?2004h", lines=3, columns=4)
    assert (screen.cursor.x, screen.cursor.y) == (3, 0)
    assert screen.render().split("\n")[0].strip() == "abc"
