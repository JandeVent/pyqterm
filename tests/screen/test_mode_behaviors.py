"""T03 — The first behavioral consumers of the mode registry.

DECAWM off (?7 l): printing at the last column overwrites in place, a
wide character that does not fit is dropped, and no pending wrap is
set. IRM on (4 h): each printed character shifts the rest of the row
right by its width (erase-fill cells in, trailing cells dropped), a
wide lead landing on the last cell is blanked, and combining marks do
not shift. NLM on (20 h): line feed also returns the cursor to column 0.

All xterm.js-verbatim (print()/insertCells()/lineFeed() in the vendored
source).
"""

from __future__ import annotations

from tests.screen.test_screen import feed_to


def test_decawm_off_overwrites_at_last_column() -> None:
    screen = feed_to("\x1b[?7l" + "abcde", lines=2, columns=4)
    rows = screen.render().split("\n")
    assert rows[0].rstrip() == "abce"  # "e" overwrote "d" in place
    assert rows[1].rstrip() == ""  # no wrap
    assert (screen.cursor.x, screen.cursor.y) == (3, 0)


def test_decawm_off_drops_wide_char_at_last_column() -> None:
    screen = feed_to("\x1b[?7l" + "abc中", lines=2, columns=4)
    rows = screen.render().split("\n")
    assert rows[0].rstrip() == "abc"  # 中 does not fit at column 3: dropped
    assert (screen.cursor.x, screen.cursor.y) == (3, 0)


def test_decawm_default_wraps() -> None:
    screen = feed_to("abcde", lines=2, columns=4)
    rows = screen.render().split("\n")
    assert rows[0].rstrip() == "abcd"
    assert rows[1].rstrip() == "e"


def test_irm_shifts_row_right_on_print() -> None:
    screen = feed_to("\x1b[4h" + "ab\rXY", lines=2, columns=5)
    rows = screen.render().split("\n")
    assert rows[0].rstrip() == "XYab"


def test_irm_drops_trailing_cells() -> None:
    screen = feed_to("\x1b[4h" + "abcde\rZ", lines=2, columns=5)
    rows = screen.render().split("\n")
    assert rows[0].rstrip() == "Zabcd"  # "e" fell off the edge


def test_irm_shifts_wide_char_pair() -> None:
    screen = feed_to("\x1b[4h" + "中\rX", lines=2, columns=6)
    rows = screen.render().split("\n")
    assert rows[0].rstrip() == "X中"


def test_irm_blanks_wide_lead_landing_on_last_cell() -> None:
    screen = feed_to("\x1b[4h" + "abc中\rZ", lines=2, columns=5)
    rows = screen.render().split("\n")
    assert rows[0].rstrip() == "Zabc"  # the shifted-out 中 is blanked


def test_irm_combining_marks_do_not_shift() -> None:
    screen = feed_to("\x1b[4h" + "a\u0301b", lines=2, columns=5)
    rows = screen.render().split("\n")
    assert rows[0].rstrip() == "a\u0301b"  # combining mark attached in place


def test_nlm_lf_returns_to_column_zero() -> None:
    screen = feed_to("\x1b[20h" + "a\nb", lines=2, columns=5)
    rows = screen.render().split("\n")
    assert rows[1].strip() == "b"


def test_nlm_off_lf_keeps_column() -> None:
    screen = feed_to("\x1b[20h\x1b[20l" + "a\nb", lines=2, columns=5)
    rows = screen.render().split("\n")
    assert rows[1].strip() == "b"  # "b" sits at column 1
    assert (screen.cursor.x, screen.cursor.y) == (2, 1)
