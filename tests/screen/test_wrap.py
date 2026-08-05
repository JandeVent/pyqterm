# -*- coding: utf-8 -*-
# Copyright (C) 2018-2026 Connet Information Technology Company, Shanghai.
"""T4 — Deferred wrap (the pending-wrap flag).

The seam: the screen's read API. Printing in the last column sets the
flag; the next printable resolves it to the next line; any cursor motion
cancels it. Wrap at the bottom line scrolls.
"""

from __future__ import annotations

from tests.screen.test_screen import feed_to


def test_print_in_last_column_sets_pending_wrap() -> None:
    screen = feed_to("abcd", lines=2, columns=4)
    assert screen.line(0)[3].data == "d"
    assert (screen.cursor.x, screen.cursor.y) == (3, 0)
    assert screen.cursor.pending_wrap is True


def test_next_printable_resolves_wrap_to_next_line() -> None:
    screen = feed_to("abcdX", lines=2, columns=4)
    assert screen.line(0)[3].data == "d"
    assert screen.line(1)[0].data == "X"
    assert (screen.cursor.x, screen.cursor.y) == (1, 1)
    assert screen.cursor.pending_wrap is False


def test_wrap_at_bottom_line_scrolls() -> None:
    screen = feed_to("abcdX", lines=1, columns=4)
    # d at col 3, wrap → scroll whole screen (the old line is discarded),
    # X lands at the start of the fresh line.
    assert screen.render() == "X   "
    assert screen.line(0)[0].data == "X"
    assert (screen.cursor.x, screen.cursor.y) == (1, 0)


def test_cr_cancels_pending_wrap() -> None:
    screen = feed_to("abcd\rZ", lines=2, columns=4)
    assert screen.line(0)[3].data == "d"
    assert screen.line(0)[0].data == "Z"  # Z overwrote a, not row 1
    assert (screen.cursor.x, screen.cursor.y) == (1, 0)


def test_bs_cancels_pending_wrap() -> None:
    screen = feed_to("abcd\bZ", lines=2, columns=4)
    assert screen.line(0)[2].data == "Z"
    assert (screen.cursor.x, screen.cursor.y) == (3, 0)


def test_tab_keeps_pending_wrap_at_wrap_position() -> None:
    screen = feed_to("abcd\tZ", lines=2, columns=4)
    # After d at col 3, a tab past the last stop lands at the wrap
    # position with the pending wrap intact (real xterm: cur_col = cols,
    # wrap_pending survives); the next char wraps to the next line.
    assert screen.line(1)[0].data == "Z"
    assert (screen.cursor.x, screen.cursor.y) == (1, 1)
    assert screen.cursor.pending_wrap is False


def test_long_line_wraps_across_rows() -> None:
    screen = feed_to("abcdefghij", lines=3, columns=4)
    assert screen.line(0)[0].data == "a"
    assert screen.line(1)[0].data == "e"
    assert screen.line(2)[0].data == "i"
    assert (screen.cursor.x, screen.cursor.y) == (2, 2)
