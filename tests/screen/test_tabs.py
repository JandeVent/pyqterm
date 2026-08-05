# -*- coding: utf-8 -*-
# Copyright (C) 2018-2026 Connet Information Technology Company, Shanghai.
"""T9 — Tab stops: a set seeded every 8, mutable via HTS/TBC, consulted
by HT, navigated by CHT/CBT, reset to defaults by resize (spec line 80).
"""

from tests.screen.test_screen import feed_to


def test_ht_advances_to_next_default_stop() -> None:
    screen = feed_to("a\tb")
    assert screen.line(0)[0].data == "a"
    assert screen.line(0)[8].data == "b"


def test_ht_from_stop_goes_to_next_stop() -> None:
    screen = feed_to("\t\tX", columns=24)
    assert screen.line(0)[16].data == "X"  # landed at stop 16


def test_ht_at_last_column_clamps() -> None:
    screen = feed_to("x" * 20 + "\t", columns=20)
    assert screen.cursor.x == 19


def test_ht_at_wrap_position_keeps_pending_wrap() -> None:
    screen = feed_to("x" * 5 + "\t", lines=2, columns=5)
    # after the 5th x the cursor sits with a pending wrap; a tab past
    # the last stop lands at the wrap position and keeps it — the next
    # char wraps (real xterm: cur_col = cols, wrap_pending survives)
    assert screen.cursor.pending_wrap is True
    assert screen.cursor.x == 4


def test_ht_to_wrap_position_then_overwrite() -> None:
    screen = feed_to("x" * 4 + "\tY", lines=2, columns=5)
    # no pending wrap: the tab lands at the last column without one,
    # so the next char clamps and overwrites (real xterm)
    assert screen.line(0)[4].data == "Y"
    assert screen.cursor.y == 0


def test_hts_sets_stop_at_cursor() -> None:
    screen = feed_to("x\x1b[1;4H\x1bH\x1b[1;1H\t", columns=24)
    # HTS at column 3; HT from column 0 lands there
    assert screen.cursor.x == 3


def test_tbc_0_clears_stop_at_cursor() -> None:
    screen = feed_to("x\x1b[1;4H\x1bH\x1b[0g\x1b[1;1H\tY", columns=24)
    # stop at 3 cleared; HT falls through to the default stop at 8
    assert screen.line(0)[8].data == "Y"


def test_tbc_3_clears_all_stops() -> None:
    screen = feed_to("\x1b[3g\tY", columns=24)
    # no stops left: HT clamps at the last column
    assert screen.cursor.x == 23


def test_tbc_2_is_unsupported_noop() -> None:
    screen = feed_to("\x1b[2g\tY", columns=24)
    assert screen.line(0)[8].data == "Y"  # default stops intact


def test_cht_moves_forward_n_stops() -> None:
    screen = feed_to("\x1b[2I", columns=24)
    assert screen.cursor.x == 16


def test_cbt_moves_backward_n_stops() -> None:
    screen = feed_to("\x1b[1;17H\x1b[Z", columns=24)
    assert screen.cursor.x == 8


def test_cbt_at_column_zero_stays() -> None:
    screen = feed_to("\x1b[Z", columns=24)
    assert screen.cursor.x == 0


def test_cbt_with_custom_stops() -> None:
    screen = feed_to("\x1b[1;4H\x1bH\x1b[1;12H\x1b[2Z", columns=24)
    # stops at 3 and 11; from 11 back two stops → 3
    assert screen.cursor.x == 3


def test_resize_reseeds_default_stops() -> None:
    screen = feed_to("x\x1b[1;4H\x1bH", columns=24)
    screen.resize(24, 24)
    assert screen.cursor.x == 3  # cursor untouched by resize reseed
    screen.carriage_return()
    screen.tab()
    assert screen.cursor.x == 8  # custom stop at 3 is gone
