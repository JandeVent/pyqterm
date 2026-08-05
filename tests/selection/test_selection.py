"""Mouse selection — the pure model the widget drives (click → word →
line, drag extend, rectangular, and the copy text extraction). Qt-free:
rows are the frozen snapshot `Row`/`Cell` objects, selection coordinates
are viewport rows/columns — the widget clears a selection when the
viewport scrolls, because the GUI only ever holds viewport rows
(ADR-0005) and cannot re-identify text that scrolled away.

The behavior set is the modern-terminal one (xterm/kitty/wezterm/
iTerm2): click-drag selects, double-click selects a word, triple-click
a line, Alt-drag a rectangle, and copy trims trailing blanks per row
and joins rows with newlines.
"""

from __future__ import annotations

from pyqterm.screen import Cell, Row
from pyqterm.selection import (
    INF,
    Selection,
    column_range,
    contains,
    extend,
    line,
    point,
    selected_text,
    word,
)


def make_rows(*texts: str) -> list[Row]:
    return [Row([Cell(c) for c in text]) for text in texts]


# -- point / word / line -------------------------------------------------


def test_point_selection_covers_one_cell() -> None:
    sel = point(2, 3)
    assert sel == Selection(2, 3, 2, 3)
    assert contains(sel, 2, 3)
    assert not contains(sel, 2, 4)
    assert not contains(sel, 1, 3)


def test_word_spans_the_non_space_run() -> None:
    rows = make_rows("aa bb cc")
    assert word(0, 3, rows) == Selection(0, 3, 0, 4)
    assert word(0, 6, rows) == Selection(0, 6, 0, 7)
    assert word(0, 0, rows) == Selection(0, 0, 0, 1)


def test_word_on_a_space_is_single_cell() -> None:
    rows = make_rows("aa bb")
    assert word(0, 2, rows) == Selection(0, 2, 0, 2)


def test_word_includes_wide_char_continuations() -> None:
    # 你 occupies two cells; the continuation is a hidden empty cell —
    # it belongs to the word (CJK text must not split mid-glyph).
    rows = [Row([Cell("你"), Cell(" ", hidden=True), Cell("x")])]
    assert word(0, 0, rows) == Selection(0, 0, 0, 2)
    assert word(0, 1, rows) == Selection(0, 0, 0, 2)  # clicked on the continuation
    assert word(0, 2, rows) == Selection(0, 0, 0, 2)
    rows = [Row([Cell("你"), Cell(" ", hidden=True), Cell("x"), Cell(" "), Cell("y")])]
    assert word(0, 0, rows) == Selection(0, 0, 0, 2)
    assert word(0, 4, rows) == Selection(0, 4, 0, 4)


def test_word_out_of_bounds_is_a_point() -> None:
    assert word(5, 3, make_rows("ab")) == Selection(5, 3, 5, 3)
    assert word(0, 9, make_rows("ab")) == Selection(0, 9, 0, 9)


def test_line_selects_the_whole_row() -> None:
    assert line(1, 10) == Selection(1, 0, 1, 9)


# -- extend --------------------------------------------------------------


def test_extend_keeps_the_anchor_cell() -> None:
    sel = extend(1, 1, 3, 4)
    assert sel == Selection(1, 1, 3, 4)
    assert extend(1, 1, 4, 0) == Selection(1, 1, 4, 0)


def test_extend_normalizes_backwards_drags() -> None:
    assert extend(2, 3, 1, 5) == Selection(1, 5, 2, 3)
    assert extend(2, 3, 2, 1) == Selection(2, 1, 2, 3)


def test_extend_anchor_survives_direction_reversal() -> None:
    # The anchor-drift regression: dragging past the anchor and back
    # must extend from the original press cell, never the last mouse
    # cell. Press at col 10, drag left to 5, drag right to 8 — the
    # selection must be 8–10, not 5–8.
    assert extend(0, 10, 0, 5) == Selection(0, 5, 0, 10)
    assert extend(0, 10, 0, 8) == Selection(0, 8, 0, 10)
    assert extend(0, 10, 0, 3) == Selection(0, 3, 0, 10)


def test_extend_preserves_rectangular_mode() -> None:
    assert extend(0, 0, 2, 3, rectangular=True).rectangular


# -- column_range (the renderer's per-row test) ---------------------------


def test_column_range_single_row() -> None:
    sel = Selection(2, 3, 2, 5)
    assert column_range(sel, 2) == (3, 5)
    assert column_range(sel, 1) is None
    assert column_range(sel, 3) is None


def test_column_range_multi_row_has_open_ends() -> None:
    sel = Selection(1, 3, 3, 5)
    assert column_range(sel, 1) == (3, INF)  # first row: to end
    assert column_range(sel, 2) == (0, INF)  # middle rows: full width
    assert column_range(sel, 3) == (0, 5)  # last row: from start
    assert column_range(sel, 0) is None
    assert column_range(sel, 4) is None


def test_column_range_rectangular_is_same_every_row() -> None:
    sel = Selection(1, 2, 3, 4, rectangular=True)
    assert column_range(sel, 1) == (2, 4)
    assert column_range(sel, 2) == (2, 4)
    assert column_range(sel, 3) == (2, 4)
    assert column_range(sel, 0) is None


# -- selected_text (the copy contract) ------------------------------------


def test_selected_text_trims_trailing_blanks() -> None:
    rows = make_rows("ab   ")
    assert selected_text(rows, Selection(0, 0, 0, 4)) == "ab"


def test_selected_text_joins_rows_with_newlines() -> None:
    rows = make_rows("hello", "world")
    assert selected_text(rows, Selection(0, 0, 1, 4)) == "hello\nworld"


def test_selected_text_middle_rows_are_fully_included() -> None:
    rows = make_rows("abcdef", "ghijkl", "mnopqr")
    sel = Selection(0, 2, 2, 3)
    assert selected_text(rows, sel) == "cdef\nghijkl\nmnop"


def test_selected_text_skips_hidden_continuations() -> None:
    rows = [Row([Cell("你"), Cell(" ", hidden=True), Cell("x")])]
    assert selected_text(rows, Selection(0, 0, 0, 1)) == "你"


def test_selected_text_rectangular_slices_columns() -> None:
    rows = make_rows("ab", "cd")
    assert selected_text(rows, Selection(0, 0, 1, 0, rectangular=True)) == "a\nc"


def test_selected_text_clamps_out_of_bounds_rows() -> None:
    rows = make_rows("ab")
    assert selected_text(rows, Selection(0, 0, 5, 9)) == "ab"
    assert selected_text(rows, Selection(5, 0, 7, 9)) == ""
