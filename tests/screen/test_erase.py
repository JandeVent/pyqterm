# -*- coding: utf-8 -*-
# Copyright (C) 2018-2026 Connet Information Technology Company, Shanghai.
"""T06 — Erase: ED (CSI n J), EL (CSI n K), ECH (CSI n X).

Erase fill = default foreground, the cursor's current background, no
attributes (glossary "Erase fill"; xterm.js backColorErase). Wrapped
markers: a full-row erase clears them — EL 2 always, EL 0 only from
column 0, ED 0 from column 0 (rows below are reset), ED 1 always on
the current row (plus the next row when the whole row was erased), ED
2 resets every row. EL 1 and ECH never clear the marker (xterm.js
_eraseInBufferLine clearWrap).
"""

from __future__ import annotations

from tests.screen.test_screen import feed_to


def test_el_0_erases_to_end_of_row() -> None:
    screen = feed_to("abcd\x1b[2D\x1b[0K", lines=2, columns=6)
    assert screen.render().split("\n")[0].rstrip() == "ab"


def test_el_1_erases_to_cursor_inclusive() -> None:
    screen = feed_to("abcd\x1b[2D\x1b[1K", lines=2, columns=6)
    assert screen.render().split("\n")[0].strip() == "d"


def test_el_2_erases_whole_row() -> None:
    screen = feed_to("abcd\x1b[2K", lines=2, columns=6)
    assert screen.render().split("\n")[0].strip() == ""


def test_ech_erases_n_cells_from_cursor() -> None:
    screen = feed_to("abcd\x1b[2D\x1b[2X", lines=2, columns=6)
    assert screen.render().split("\n")[0].rstrip() == "ab"


def test_ech_clamps_to_row_end() -> None:
    screen = feed_to("ab\x1b[9X", lines=2, columns=6)
    assert screen.render().split("\n")[0].rstrip() == "ab"


def test_ed_0_erases_from_cursor_down() -> None:
    screen = feed_to("a\nb\nc\nd\x1b[1;2H\x1b[0J", lines=4, columns=4)
    rows = screen.render().split("\n")
    assert rows[0].rstrip() == "a"
    assert rows[1].strip() == ""
    assert rows[2].strip() == ""
    assert rows[3].strip() == ""


def test_ed_1_erases_from_top_to_cursor() -> None:
    screen = feed_to("a\nb\nc\nd\x1b[3;4H\x1b[1J", lines=4, columns=4)
    rows = screen.render().split("\n")
    assert rows[0].strip() == ""
    assert rows[1].strip() == ""
    assert rows[2].strip() == ""
    assert rows[3].strip() == "d"  # "d" sits at column 3 (LF keeps x)


def test_ed_2_erases_everything() -> None:
    screen = feed_to("a\nb\x1b[2J", lines=4, columns=4)
    assert screen.render().strip() == ""


def test_erase_fill_uses_cursor_background() -> None:
    screen = feed_to("\x1b[44mX\x1b[2K", lines=2, columns=6)
    cell = screen.line(0)[2]
    assert cell.fg == -1
    assert cell.bg == 4


def test_el_2_clears_wrapped_marker() -> None:
    screen = feed_to("x" * 6 + "\x1b[2K", lines=2, columns=5)
    assert screen.line(1).wrapped is False


def test_ed_0_from_column_zero_clears_marker() -> None:
    screen = feed_to("x" * 6 + "\r\x1b[0J", lines=2, columns=5)
    # CR puts the cursor at column 0 of the wrapped row; ED 0 from
    # column 0 erases the whole row and clears its marker
    assert screen.line(1).wrapped is False


def test_el_0_from_mid_row_keeps_marker() -> None:
    screen = feed_to("x" * 6 + "\x1b[2C\x1b[0K", lines=2, columns=5)
    assert screen.line(1).wrapped is True


def test_el_1_keeps_wrapped_marker() -> None:
    screen = feed_to("x" * 6 + "\x1b[1K", lines=2, columns=5)
    assert screen.line(1).wrapped is True


def test_ech_keeps_wrapped_marker() -> None:
    screen = feed_to("x" * 6 + "\x1b[1X", lines=2, columns=5)
    assert screen.line(1).wrapped is True
