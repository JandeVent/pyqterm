# -*- coding: utf-8 -*-
# Copyright (C) 2018-2026 Connet Information Technology Company, Shanghai.
"""T05 — Cursor motion and addressing (clamp, not scroll).

CUU/CUD clamp at the region top/bottom when the cursor is inside the
region, at the screen edges when outside it (xterm.js: the diffToTop/
diffToBottom math). CUF clamps at the last column, CUB at 0. CNL/CPL
combine the vertical move with a return to column 0. CUP/HVP are
1-based absolute addressing — clamped to the screen, or region-relative
plus clamped to the region under origin mode (DECOM). DECOM set/reset
moves the cursor home: region top on set, screen home on reset. IND
(ESC D) moves down scrolling the region at its bottom; NEL (ESC E)
returns to column 0 first; RI (ESC M) moves up, scrolling the region
down at its top. All motions clear a pending wrap.
"""

from __future__ import annotations

from tests.screen.test_screen import feed_to


def test_cuu_clamps_at_region_top() -> None:
    screen = feed_to("\x1b[3;5r" + "\x1b[4B" + "\x1b[5A", lines=6, columns=4)
    # CUD 4 from (0,0) → y=4; CUU 5 → clamped at region top (2)
    assert (screen.cursor.x, screen.cursor.y) == (0, 2)


def test_cud_clamps_at_region_bottom() -> None:
    screen = feed_to("\x1b[3;5r" + "\x1b[2B" + "\x1b[3B", lines=6, columns=4)
    # CUD 2 → y=2 (region top); CUD 3 → clamped at region bottom (4)
    assert screen.cursor.y == 4


def test_cud_below_region_moves_to_screen_bottom() -> None:
    screen = feed_to("\x1b[3;5r" + "\x1b[6;1H" + "\x1b[2B", lines=6, columns=4)
    # CUP to (0,5) — below the region; CUD 2 moves freely, clamped at rows-1
    assert (screen.cursor.x, screen.cursor.y) == (0, 5)


def test_cuf_cub_clamp_at_screen_edges() -> None:
    screen = feed_to("a\x1b[3C\x1b[5D\x1b[1D", lines=2, columns=4)
    # CUF 3 → x=3; CUB 5 → x=0; CUB 1 → still 0
    assert screen.cursor.x == 0
    assert screen.cursor.y == 0


def test_cuf_clamps_at_last_column() -> None:
    screen = feed_to("\x1b[10C", lines=2, columns=4)
    assert screen.cursor.x == 3


def test_cnl_cpl_move_lines_and_to_column_zero() -> None:
    screen = feed_to("ab\x1b[2E\x1b[F", lines=6, columns=4)
    # ab → (2,0); CNL 2 → (0,2); CPL 1 → (0,1)
    assert (screen.cursor.x, screen.cursor.y) == (0, 1)


def test_cup_single_param_moves_to_column_zero() -> None:
    screen = feed_to("\x1b[5;2H\x1b[3H", lines=6, columns=4)
    # CUP 5;2 → (1,4); CUP 3 (one parameter) → (0,2)
    assert (screen.cursor.x, screen.cursor.y) == (0, 2)


def test_cup_defaults_to_home() -> None:
    screen = feed_to("\x1b[2;2H\x1b[H", lines=6, columns=4)
    assert (screen.cursor.x, screen.cursor.y) == (0, 0)


def test_cup_clamps() -> None:
    screen = feed_to("\x1b[99;99H", lines=6, columns=4)
    assert (screen.cursor.x, screen.cursor.y) == (3, 5)


def test_hvp_is_cup_alias() -> None:
    screen = feed_to("\x1b[3;4f", lines=6, columns=4)
    assert (screen.cursor.x, screen.cursor.y) == (3, 2)


def test_cup_origin_relative_to_region_top() -> None:
    screen = feed_to("\x1b[3;5r\x1b[?6h\x1b[2;2H", lines=6, columns=4)
    # region [2,4]; CUP 2;2 → (1, scroll_top + 1) = (1, 3)
    assert (screen.cursor.x, screen.cursor.y) == (1, 3)


def test_cha_moves_to_column_keeping_row() -> None:
    screen = feed_to("ab\x1b[5Gc", lines=3, columns=6)
    # ab → (2,0); CHA 5 → (4,0); c written there
    rows = screen.render().split("\n")
    assert rows[0].strip() == "ab  c"
    assert (screen.cursor.x, screen.cursor.y) == (5, 0)


def test_cha_defaults_to_column_zero() -> None:
    screen = feed_to("ab\x1b[G", lines=3, columns=6)
    assert (screen.cursor.x, screen.cursor.y) == (0, 0)


def test_cha_clamps_at_last_column() -> None:
    screen = feed_to("ab\x1b[99G", lines=3, columns=6)
    assert (screen.cursor.x, screen.cursor.y) == (5, 0)


def test_vpa_moves_to_row_keeping_column() -> None:
    screen = feed_to("ab\x1b[4dc", lines=6, columns=6)
    # ab → (2,0); VPA 4 → (2,3); c written at (3,3)
    rows = screen.render().split("\n")
    assert rows[3].strip() == "c"
    assert (screen.cursor.x, screen.cursor.y) == (3, 3)


def test_vpa_defaults_to_row_zero() -> None:
    screen = feed_to("ab\x1b[3;1H\x1b[d", lines=6, columns=6)
    assert (screen.cursor.x, screen.cursor.y) == (0, 0)


def test_vpa_clamps_at_last_row() -> None:
    screen = feed_to("\x1b[99d", lines=6, columns=6)
    assert (screen.cursor.x, screen.cursor.y) == (0, 5)


def test_vpa_origin_relative_to_region_top() -> None:
    screen = feed_to("\x1b[3;5r\x1b[?6h\x1b[2d", lines=6, columns=4)
    # region [2,4]; VPA 2 → (0, scroll_top + 1) = (0, 3)
    assert (screen.cursor.x, screen.cursor.y) == (0, 3)


def test_origin_mode_set_homes_to_region_top() -> None:
    screen = feed_to("\x1b[3;5r" + "\x1b[2;2H" + "\x1b[?6h", lines=6, columns=4)
    assert (screen.cursor.x, screen.cursor.y) == (0, 2)


def test_origin_mode_reset_homes_to_screen_top() -> None:
    screen = feed_to("\x1b[3;5r\x1b[?6h\x1b[2;2H\x1b[?6l", lines=6, columns=4)
    assert (screen.cursor.x, screen.cursor.y) == (0, 0)


def test_ind_moves_down_keeping_column() -> None:
    screen = feed_to("ab\x1bDc", lines=2, columns=4)
    assert (screen.cursor.x, screen.cursor.y) == (3, 1)


def test_nel_returns_to_column_zero_and_moves_down() -> None:
    screen = feed_to("ab\x1bEc", lines=2, columns=4)
    assert (screen.cursor.x, screen.cursor.y) == (1, 1)


def test_nel_at_region_bottom_scrolls_region() -> None:
    # NEL is CR + index (xterm.js nextLine): at the region bottom the
    # index scrolls — unlike CNL, whose clamped motion just stops.
    screen = feed_to(
        "\x1b[2;4r" + "a\r\nb\r\nc" + "\x1b[4;1H" + "d\x1bE", lines=5, columns=4
    )
    rows = screen.render().split("\n")
    assert rows[0].strip() == "a"  # above the region: untouched
    assert rows[1].strip() == "c"  # region scrolled up
    assert rows[2].strip() == "d"
    assert rows[3].strip() == ""  # fresh blank at the region bottom
    assert (screen.cursor.x, screen.cursor.y) == (0, 3)


def test_nel_preserves_wrapped_marker() -> None:
    # NEL is CR + index; index does not clear the wrapped marker
    # (xterm.js nextLine → index), unlike LF which clears it.
    screen = feed_to("abcd\x1b[1;1H\x1bE", lines=4, columns=2)
    # "abcd" wraps: row 1 holds "cd" with the wrapped marker; the NEL
    # lands on it via index, which leaves the marker alone.
    assert screen.line(1).wrapped is True


def test_ri_moves_up_keeping_column() -> None:
    screen = feed_to("a\nb\x1bM", lines=2, columns=4)
    # 'b' sits at column 1 (LF keeps the column); RI moves up, keeping it
    assert (screen.cursor.x, screen.cursor.y) == (2, 0)


def test_ri_at_region_top_scrolls_region_down() -> None:
    screen = feed_to(
        "\x1b[3;5r" + "a\r\nb\r\nc\r\nd\r\ne" + "\x1b[2A\x1bM", lines=6, columns=4
    )
    rows = screen.render().split("\n")
    assert rows[0].strip() == "a"  # above the region: untouched
    assert rows[1].strip() == "b"
    assert rows[2].strip() == ""  # fresh blank at the region top
    assert rows[3].strip() == "c"  # region shifted down
    assert rows[4].strip() == "d"


def test_motion_clears_pending_wrap() -> None:
    screen = feed_to("aaaa\x1b[1A", lines=2, columns=4)
    assert screen.cursor.pending_wrap is False
    assert (screen.cursor.x, screen.cursor.y) == (3, 0)
