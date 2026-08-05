"""T11 — Scrolling and row ops: SU/SD scroll the region; IL/DL insert and
delete lines; ICH/DCH insert and delete characters.

Fills follow xterm.js verbatim: lines scrolled in by LF/RI/SU/IL/DL and
rows reset by ED carry the erase fill (default fg, cursor's bg); SD alone
fills its fresh top line with default attributes (DEFAULT_ATTR_DATA).
"""

from tests.screen.test_screen import feed_to


# -- SU: scroll up ------------------------------------------------------

def test_su_scrolls_region_up() -> None:
    screen = feed_to("1\r\n2\r\n3\r\n4\x1b[S", lines=4, columns=4)
    rows = screen.render().split("\n")
    assert rows[0].strip() == "2"
    assert rows[1].strip() == "3"
    assert rows[2].strip() == "4"
    assert rows[3].strip() == ""


def test_su_in_narrowed_region() -> None:
    screen = feed_to("1\r\n2\r\n3\r\n4\r\n5\x1b[2;4r\x1b[2S", lines=5, columns=4)
    rows = screen.render().split("\n")
    assert rows[0].strip() == "1"
    assert rows[1].strip() == "4"
    assert rows[2].strip() == ""
    assert rows[3].strip() == ""
    assert rows[4].strip() == "5"


def test_su_larger_than_region_blanks_it() -> None:
    screen = feed_to("1\r\n2\r\n3\x1b[2;4r\x1b[9S", lines=4, columns=4)
    rows = screen.render().split("\n")
    assert rows[0].strip() == "1"
    assert rows[1].strip() == ""
    assert rows[2].strip() == ""
    assert rows[3].strip() == ""


def test_su_keeps_cursor_position() -> None:
    screen = feed_to("abc\x1b[4;2H\x1b[S", lines=4, columns=4)
    assert (screen.cursor.x, screen.cursor.y) == (1, 3)


def test_su_wrapped_marker_rides_with_row() -> None:
    screen = feed_to("x" * 6 + "\x1b[2;2H\x1b[S", lines=3, columns=5)
    # the wrapped "x" row scrolls up to row 0, keeping its marker
    assert screen.line(0).wrapped is True
    assert screen.line(0)[0].data == "x"


# -- SD: scroll down ----------------------------------------------------

def test_sd_scrolls_region_down() -> None:
    screen = feed_to("1\r\n2\r\n3\r\n4\x1b[T", lines=4, columns=4)
    rows = screen.render().split("\n")
    assert rows[0].strip() == ""
    assert rows[1].strip() == "1"
    assert rows[2].strip() == "2"
    assert rows[3].strip() == "3"


def test_sd_in_narrowed_region() -> None:
    screen = feed_to("1\r\n2\r\n3\r\n4\r\n5\x1b[2;4r\x1b[T", lines=5, columns=4)
    rows = screen.render().split("\n")
    assert rows[0].strip() == "1"
    assert rows[1].strip() == ""
    assert rows[2].strip() == "2"
    assert rows[3].strip() == "3"
    assert rows[4].strip() == "5"


# -- IL: insert lines ---------------------------------------------------

def test_il_inserts_blank_line_at_cursor() -> None:
    screen = feed_to("1\r\n2\r\n3\r\n4\x1b[2;2H\x1b[L", lines=4, columns=4)
    rows = screen.render().split("\n")
    assert rows[0].strip() == "1"
    assert rows[1].strip() == ""
    assert rows[2].strip() == "2"
    assert rows[3].strip() == "3"


def test_il_outside_region_is_noop() -> None:
    screen = feed_to("1\r\n2\r\n3\r\n4\x1b[2;4r\x1b[L", lines=4, columns=4)
    rows = screen.render().split("\n")
    assert rows[0].strip() == "1"
    assert rows[1].strip() == "2"
    assert rows[2].strip() == "3"
    assert rows[3].strip() == "4"


def test_il_below_region_untouched() -> None:
    screen = feed_to("1\r\n2\r\n3\r\n4\r\n5\x1b[2;4r\x1b[2;2H\x1b[L", lines=5, columns=4)
    rows = screen.render().split("\n")
    assert rows[0].strip() == "1"
    assert rows[1].strip() == ""
    assert rows[2].strip() == "2"
    assert rows[3].strip() == "3"
    assert rows[4].strip() == "5"


def test_il_returns_cursor_to_column_zero() -> None:
    screen = feed_to("a\x1b[2;3H\x1b[L", lines=4, columns=4)
    assert (screen.cursor.x, screen.cursor.y) == (0, 1)


def test_il_inserts_unwrapped_line() -> None:
    screen = feed_to("x" * 6 + "\x1b[2;2H\x1b[L", lines=3, columns=5)
    assert screen.line(1).wrapped is False
    # the wrapped "x" row moved down, marker intact
    assert screen.line(2).wrapped is True


def test_il_multiple_lines() -> None:
    screen = feed_to("1\r\n2\r\n3\r\n4\r\n5\x1b[3;3H\x1b[3L", lines=5, columns=4)
    rows = screen.render().split("\n")
    assert rows[0].strip() == "1"
    assert rows[1].strip() == "2"
    assert rows[2].strip() == ""
    assert rows[3].strip() == ""
    assert rows[4].strip() == ""


# -- DL: delete lines ---------------------------------------------------

def test_dl_deletes_line_at_cursor() -> None:
    screen = feed_to("1\r\n2\r\n3\r\n4\x1b[2;2H\x1b[M", lines=4, columns=4)
    rows = screen.render().split("\n")
    assert rows[0].strip() == "1"
    assert rows[1].strip() == "3"
    assert rows[2].strip() == "4"
    assert rows[3].strip() == ""


def test_dl_outside_region_is_noop() -> None:
    screen = feed_to("1\r\n2\r\n3\r\n4\x1b[2;4r\x1b[M", lines=4, columns=4)
    rows = screen.render().split("\n")
    assert rows[0].strip() == "1"
    assert rows[1].strip() == "2"
    assert rows[2].strip() == "3"
    assert rows[3].strip() == "4"


def test_dl_returns_cursor_to_column_zero() -> None:
    screen = feed_to("a\x1b[2;3H\x1b[M", lines=4, columns=4)
    assert (screen.cursor.x, screen.cursor.y) == (0, 1)


def test_dl_multiple_lines() -> None:
    screen = feed_to("1\r\n2\r\n3\r\n4\r\n5\x1b[3;3H\x1b[2M", lines=5, columns=4)
    rows = screen.render().split("\n")
    assert rows[0].strip() == "1"
    assert rows[1].strip() == "2"
    assert rows[2].strip() == "5"
    assert rows[3].strip() == ""
    assert rows[4].strip() == ""


# -- ICH: insert characters ---------------------------------------------

def test_ich_shifts_row_right() -> None:
    screen = feed_to("ab\x1b[1;2H\x1b[@", lines=2, columns=4)
    assert screen.render().split("\n")[0].strip() == "a b"
    # the cursor does not move (xterm.js insertChars)
    assert screen.cursor.x == 1


def test_ich_multiple_cells() -> None:
    screen = feed_to("abcd\x1b[1;2H\x1b[2@", lines=2, columns=4)
    assert screen.render().split("\n")[0].strip() == "a  b"


def test_ich_blanks_wide_lead_split_by_insertion() -> None:
    screen = feed_to("中\x1b[1;2H\x1b[@", lines=2, columns=4)
    row = screen.line(0)
    assert row[0].data == " "  # the split wide lead is blanked
    assert row[1].data == " "
    assert row[2].data == ""  # the orphaned continuation survives


# -- DCH: delete characters ---------------------------------------------

def test_dch_shifts_row_left() -> None:
    screen = feed_to("abcd\x1b[1;3H\x1b[P", lines=2, columns=4)
    assert screen.render().split("\n")[0].strip() == "abd"


def test_dch_multiple_cells() -> None:
    screen = feed_to("abcd\x1b[1;2H\x1b[2P", lines=2, columns=4)
    assert screen.render().split("\n")[0].strip() == "ad"


def test_dch_deleting_a_cell_keeps_wide_char() -> None:
    screen = feed_to("中a\x1b[1;3H\x1b[P", lines=2, columns=4)
    assert screen.render().split("\n")[0].strip() == "中"


def test_dch_deleting_wide_lead_blanks_continuation() -> None:
    screen = feed_to("中x\x1b[1;2H\x1b[P", lines=2, columns=4)
    row = screen.line(0)
    assert row[0].data == " "  # the wide lead is gone
    assert row[1].data == "x"
    assert row[2].data == " "  # no orphaned continuation stub


# -- Fill colors of scrolled-in lines (xterm.js-verbatim) ----------------

def test_su_scrolled_line_uses_erase_fill() -> None:
    screen = feed_to("a\r\nb\x1b[41m\x1b[S", lines=2, columns=4)
    assert screen.line(1)[0].fg == -1
    assert screen.line(1)[0].bg == 1  # the cursor's bg at scroll time


def test_sd_scrolled_line_uses_default_attrs() -> None:
    screen = feed_to("a\x1b[41m\x1b[T", lines=2, columns=4)
    assert screen.line(0)[0].bg == -1  # SD alone: DEFAULT_ATTR_DATA


def test_lf_scrolled_line_uses_erase_fill() -> None:
    screen = feed_to("a\r\nb\x1b[41m\n", lines=2, columns=4)
    assert screen.line(1)[0].bg == 1


def test_reverse_index_scrolled_line_uses_erase_fill() -> None:
    screen = feed_to("a\x1b[41m\x1b[1;1H\x1bM", lines=2, columns=4)
    assert screen.line(0)[0].bg == 1


def test_il_inserted_line_uses_erase_fill() -> None:
    screen = feed_to("ab\x1b[41m\x1b[1;1H\x1b[L", lines=2, columns=4)
    assert screen.line(0)[0].bg == 1


def test_dl_appended_line_uses_erase_fill() -> None:
    screen = feed_to("ab\x1b[41m\x1b[1;1H\x1b[M", lines=2, columns=4)
    assert screen.line(1)[0].bg == 1


def test_ed_reset_rows_use_erase_fill() -> None:
    screen = feed_to("a\r\nb\x1b[41m\x1b[1;1H\x1b[0J", lines=2, columns=4)
    assert screen.line(0)[0].bg == 1
    assert screen.line(1)[0].bg == 1
