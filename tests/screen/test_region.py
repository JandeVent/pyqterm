# -*- coding: utf-8 -*-
# Copyright (C) 2018-2026 Connet Information Technology Company, Shanghai.
"""T04 — Scroll region (DECSTBM) with xterm.js semantics.

`CSI n;m r` clamps both bounds, ignores a region whose bottom is not
below its top (nothing changes, cursor does not move), moves the cursor
home on a valid set — (0, 0), or (0, scroll_top) under origin mode — and
does not touch origin mode itself. Resize resets the region to full
screen. Scrolling (LF at the region bottom, wrap at the region bottom)
happens within the region, leaving rows outside it untouched.

Regions are observed behaviorally: LF/wrap at the bottom scroll only the
region rows, so row contents outside the region prove the bounds.
"""

from __future__ import annotations

from pyqtermx.screen import DECOM
from tests.screen.test_screen import feed_to


def test_lf_at_region_bottom_scrolls_only_the_region() -> None:
    screen = feed_to(
        "\x1b[3;5r" + "a\r\nb\r\nc\r\nd\r\ne" + "\r\n", lines=6, columns=4
    )
    rows = screen.render().split("\n")
    assert rows[0].rstrip() == "a"  # outside the region: untouched
    assert rows[1].rstrip() == "b"
    assert rows[2].rstrip() == "d"  # region scrolled up by one
    assert rows[3].rstrip() == "e"
    assert rows[4].rstrip() == ""  # fresh row at the region bottom
    assert rows[5].rstrip() == ""  # untouched


def test_wrap_at_region_bottom_scrolls_region() -> None:
    screen = feed_to(
        "\x1b[3;5r" + "a\r\nb\r\nc\r\nd\r\n" + "eeeeX", lines=6, columns=4
    )
    rows = screen.render().split("\n")
    assert rows[0].rstrip() == "a"
    assert rows[1].rstrip() == "b"
    assert rows[2].rstrip() == "d"
    assert rows[3].rstrip() == "eeee"
    assert rows[4].rstrip() == "X"  # wrapped onto the fresh row


def test_inverted_region_is_ignored() -> None:
    # bottom <= top: nothing changes — LF at the bottom still scrolls
    # the full screen.
    screen = feed_to(
        "\x1b[5;3r" + "a\r\nb\r\nc\r\nd\r\ne\r\nf" + "\r\n", lines=6, columns=4
    )
    rows = screen.render().split("\n")
    assert rows[0].rstrip() == "b"  # full-screen scroll happened
    assert rows[5].rstrip() == ""


def test_declaring_region_moves_cursor_home() -> None:
    screen = feed_to("\n\n\n\x1b[3;5r", lines=6, columns=4)
    assert (screen.cursor.x, screen.cursor.y) == (0, 0)


def test_home_is_region_top_under_origin_mode() -> None:
    screen = feed_to("\n\n\n\x1b[?6h\x1b[3;5r", lines=6, columns=4)
    assert (screen.cursor.x, screen.cursor.y) == (0, 2)


def test_decstbm_does_not_reset_origin_mode() -> None:
    screen = feed_to("\x1b[?6h\x1b[2;4r")
    assert screen.mode(DECOM, private=True) is True


def test_resize_resets_region_to_full_screen() -> None:
    screen = feed_to("\x1b[3;5r" + "a\r\nb\r\nc\r\nd\r\ne", lines=6, columns=4)
    screen.resize(6, 4)
    screen.line_feed()  # y=4 → 5 (region no longer [2,4])
    screen.line_feed()  # at the full-screen bottom → scroll everything
    rows = screen.render().split("\n")
    assert rows[0].rstrip() == "b"


def test_empty_params_reset_region_to_full_screen() -> None:
    screen = feed_to("\x1b[3;5r\x1b[r" + "a\r\nb\r\nc\r\nd\r\ne", lines=6, columns=4)
    screen.line_feed()  # y=4 → 5
    screen.line_feed()  # at the full-screen bottom → scroll everything
    rows = screen.render().split("\n")
    assert rows[0].rstrip() == "b"
