"""T5 — Width-aware print: wide characters and combining marks.

The seam: the screen's read API. A wide character (CJK, wcwidth 2) fills
its cell plus a blank continuation cell; a combining mark (wcwidth 0)
attaches to the cell behind the cursor instead of occupying a cell.
"""

from __future__ import annotations

from tests.screen.test_screen import feed_to


def test_wide_char_occupies_two_cells() -> None:
    screen = feed_to("你")
    assert screen.line(0)[0].data == "你"
    assert screen.line(0)[1].data == ""  # blank continuation cell
    assert (screen.cursor.x, screen.cursor.y) == (2, 0)


def test_wide_char_shifts_following_text() -> None:
    screen = feed_to("你a")
    assert screen.line(0)[2].data == "a"
    assert (screen.cursor.x, screen.cursor.y) == (3, 0)


def test_combining_mark_attaches_to_previous_cell() -> None:
    screen = feed_to("e\u0301")  # é as e + combining acute
    assert screen.line(0)[0].data == "e\u0301"
    assert screen.line(0)[1].data == " "
    assert (screen.cursor.x, screen.cursor.y) == (1, 0)


def test_combining_mark_at_column_zero_is_dropped() -> None:
    screen = feed_to("\u0301a")
    assert screen.line(0)[0].data == "a"
    assert (screen.cursor.x, screen.cursor.y) == (1, 0)


def test_wide_char_at_last_column_resolves_wrap() -> None:
    # 4 columns: 你 at cols 0–1, then 'a' at col 2, 'b' at col 3 → pending.
    screen = feed_to("你abX", lines=2, columns=4)
    assert screen.line(1)[0].data == "X"
    assert (screen.cursor.x, screen.cursor.y) == (1, 1)


def test_wide_char_does_not_fit_at_edge_wraps_first() -> None:
    # 3 columns: 'a' at 0, 你 needs cols 1–2 — fits exactly.
    screen = feed_to("a你", columns=3)
    assert screen.line(0)[0].data == "a"
    assert screen.line(0)[1].data == "你"
    assert (screen.cursor.x, screen.cursor.y) == (2, 0)
    assert screen.cursor.pending_wrap is True


def test_wide_char_with_only_one_cell_left_wraps() -> None:
    # 4 columns: 'abc' at 0–2, then 你 needs cols 3–4 — only 1 left, so it
    # wraps to the next line first.
    screen = feed_to("abc你X", lines=2, columns=4)
    assert screen.line(1)[0].data == "你"
    assert screen.line(1)[2].data == "X"
    assert (screen.cursor.x, screen.cursor.y) == (3, 1)


def test_combining_mark_after_wide_char() -> None:
    screen = feed_to("你\u0301")
    # Combining attaches to the wide char's *glyph* cell, not the blank
    # continuation.
    assert screen.line(0)[0].data == "你\u0301"
    assert screen.line(0)[1].data == ""
