"""T03 — DECALN (`ESC # 8`) — screen alignment test.

The screen is filled with `E` in the cursor's *full current rendition*
(not the erase fill), the wrapped markers are cleared, and the cursor
is homed before and after. Tab stops, the scroll region, the DECSC
slot, and the modes are untouched. In the alternate screen the active
grid is the one filled (ADR-0004).
"""

from pyqterm.screen import Cell, Screen

from tests.screen.test_screen import feed_to, make_screen


def _row_text(screen: Screen, y: int) -> str:
    return "".join(cell.data for cell in screen.line(y).cells).rstrip(" ")


def test_decaln_fills_grid_with_e_in_cursor_rendition() -> None:
    """Every cell is `E` carrying the cursor's rendition at fill time —
    foreground, background, and the SGR attributes (not the erase
    fill: the background comes from the cursor, not from a default)."""
    screen = feed_to("\x1b[31;1m\x1b[44m\x1b#8")
    assert _row_text(screen, 0) == "E" * 80
    assert _row_text(screen, 23) == "E" * 80
    e = screen.line(0)[0]
    assert e == Cell("E", fg=1, bg=4, bold=True)


def test_decaln_homes_cursor() -> None:
    """The cursor ends at the home position."""
    screen = feed_to("abc\x1b#8")
    assert (screen.cursor.x, screen.cursor.y) == (0, 0)


def test_decaln_clears_wrapped_flags() -> None:
    """Wrapped rows from earlier output are marked unwrapped."""
    parser, _emulator, screen = make_screen(4, 5)
    parser.feed("abcdefghij")
    parser.flush()
    assert screen.line(1).wrapped  # "fghij" continues the wrapped row
    parser.feed("\x1b#8")
    parser.flush()
    for y in range(4):
        assert not screen.line(y).wrapped


def test_decaln_fills_active_screen_only() -> None:
    """Inside the alternate screen, DECALN fills the alt grid; the
    normal grid is preserved."""
    parser, _emulator, screen = make_screen(4, 5)
    parser.feed("abc\r\ndef\x1b[?1047h\x1b#8")
    parser.flush()
    assert _row_text(screen, 0) == "EEEEE"
    parser.feed("\x1b[?1047l")
    parser.flush()
    assert _row_text(screen, 0) == "abc"
    assert _row_text(screen, 1) == "def"


def test_decaln_leaves_tabs_region_and_saved_cursor() -> None:
    """DECALN is a display fill only: tab stops, the scroll region and
    the DECSC slot survive."""
    parser, _emulator, screen = make_screen(6, 10)
    parser.feed("\x1b[2;4r\x1b[1;5H\x1bH\x1b7\x1b#8\x1b8")
    parser.flush()
    assert screen.scroll_top == 1  # "2;4" → rows 1-3, 0-based
    assert screen.scroll_bottom == 3
    assert 4 in screen._tab_stops  # the stop at column 4 set by HTS
    # The DECSC save/restore round-trip left the cursor at its
    # pre-DECALN position — and DECALN did not wipe it.
    assert (screen.cursor.x, screen.cursor.y) == (4, 0)
