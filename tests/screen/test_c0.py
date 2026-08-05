# -*- coding: utf-8 -*-
# Copyright (C) 2018-2026 Connet Information Technology Company, Shanghai.
"""T2 — C0 controls and full-screen scroll.

The seam: the dispatcher protocol (parser → emulator) and the screen's
read API. Each C0 control maps to a screen operation; LF at the bottom
line scrolls the whole screen up via the scroll-region primitive.
"""

from __future__ import annotations

from tests.screen.test_screen import feed_to


def test_cr_returns_to_column_zero() -> None:
    screen = feed_to("ab\rcd")
    assert screen.render().split("\n")[0].startswith("cd")
    assert (screen.cursor.x, screen.cursor.y) == (2, 0)


def test_lf_moves_cursor_down() -> None:
    screen = feed_to("ab\n")
    assert (screen.cursor.x, screen.cursor.y) == (2, 1)


def test_lf_preserves_column() -> None:
    screen = feed_to("  x\ny")
    assert (screen.cursor.x, screen.cursor.y) == (4, 1)


def test_lf_at_bottom_scrolls_whole_screen() -> None:
    screen = feed_to("a\r\nb\r\n", lines=2, columns=4)
    # a on row 0; CR+LF → row 1; b on row 1; CR+LF at bottom → scroll up.
    assert screen.render() == "b   \n    "
    assert (screen.cursor.x, screen.cursor.y) == (0, 1)


def test_lf_at_bottom_discards_top_line() -> None:
    screen = feed_to("1111\r\n2222\r\n3333", lines=2, columns=4)
    assert screen.render() == "2222\n3333"


def test_bs_moves_left_one_column() -> None:
    screen = feed_to("ab\bX")
    assert screen.render().split("\n")[0].startswith("aX")


def test_bs_at_column_zero_is_clamped() -> None:
    screen = feed_to("\bX")
    assert screen.render().split("\n")[0].startswith("X")


def test_tab_advances_to_next_stop() -> None:
    screen = feed_to("a\tb")
    assert screen.render().split("\n")[0].startswith("a       b")  # col 8


def test_tab_at_last_stop_clamps() -> None:
    # 5 columns: TAB from col 1 advances to the next stop (8), clamped to
    # the last column (4) — the stop itself is out of range.
    screen = feed_to("ab\tX", columns=5)
    assert (screen.cursor.x, screen.cursor.y) == (4, 0)


def test_bel_is_swallowed() -> None:
    screen = feed_to("a\ab")
    assert screen.render().split("\n")[0].startswith("ab")
    assert (screen.cursor.x, screen.cursor.y) == (2, 0)


def test_motion_clears_pending_wrap() -> None:
    screen = feed_to("abcd\rX", lines=1, columns=4)
    assert (screen.cursor.x, screen.cursor.y) == (1, 0)
    assert screen.cursor.pending_wrap is False
