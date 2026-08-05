# -*- coding: utf-8 -*-
# Copyright (C) 2018-2026 Connet Information Technology Company, Shanghai.
"""T05 — truecolor (SGR 38;2 / 48;2) — ADR-0004.

Colors are ints: `-1` default, `0–255` the 256-color palette, and
`>= 0x1000000` an RGB value `(r << 16) | (g << 8) | b | 0x1000000`.
A truncated `38;2` / `48;2` (missing components) is ignored; values
over 255 clamp to 255 (documented deviation).
"""

from pyqtermx.screen import Cell, Screen, is_rgb, rgb, rgb_parts

from tests.screen.test_screen import feed_to


def test_rgb_helpers_round_trip() -> None:
    assert rgb(0, 0, 0) == 0x1000000
    assert rgb(255, 0, 0) == 0x1FF0000
    assert rgb(12, 34, 56) == 0x10C2238
    assert is_rgb(rgb(1, 2, 3))
    assert is_rgb(0x1000000)
    assert not is_rgb(-1)  # default
    assert not is_rgb(255)  # palette index
    assert not is_rgb(0xFFFFF)  # below the RGB marker
    assert rgb_parts(rgb(12, 34, 56)) == (12, 34, 56)


def test_sgr_38_2_sets_rgb_foreground() -> None:
    screen = feed_to("\x1b[38;2;255;0;0mX")
    assert screen.line(0)[0].fg == rgb(255, 0, 0)
    assert screen.line(0)[0].bg == -1


def test_sgr_48_2_sets_rgb_background() -> None:
    screen = feed_to("\x1b[48;2;10;20;30mX")
    assert screen.line(0)[0].bg == rgb(10, 20, 30)
    assert screen.line(0)[0].fg == -1


def test_rgb_carries_other_attributes() -> None:
    screen = feed_to("\x1b[1;3;38;2;1;2;3mX")
    cell = screen.line(0)[0]
    assert cell.fg == rgb(1, 2, 3)
    assert cell.bold
    assert cell.italic


def test_sgr_39_49_reset_rgb() -> None:
    screen = feed_to("\x1b[38;2;1;2;3;48;2;4;5;6m\x1b[39;49mX")
    cell = screen.line(0)[0]
    assert cell.fg == -1
    assert cell.bg == -1


def test_colon_form_sgr_38_2() -> None:
    """`38:2:r:g:b` — xterm's sub-parameter syntax — sets RGB fg."""
    screen = feed_to("\x1b[38:2:255:0:0mX")
    assert screen.line(0)[0].fg == rgb(255, 0, 0)


def test_colon_form_sgr_48_2_with_color_space() -> None:
    """`48:2:cs:r:g:b` — the color-space slot (0) is accepted and
    ignored; the remaining three components are the RGB value."""
    screen = feed_to("\x1b[48:2:0:10:20:30mX")
    assert screen.line(0)[0].bg == rgb(10, 20, 30)


def test_colon_form_sgr_38_2_empty_color_space() -> None:
    """`38:2::r:g:b` — the empty `:` slot decodes to -1, which the
    color-space position absorbs; the RGB components follow it."""
    screen = feed_to("\x1b[38:2::1:2:3mX")
    assert screen.line(0)[0].fg == rgb(1, 2, 3)


def test_colon_form_sgr_38_5_palette_index() -> None:
    screen = feed_to("\x1b[38:5:196mX")
    assert screen.line(0)[0].fg == 196


def test_colon_form_truncated_is_ignored() -> None:
    """A truncated colon form leaves the color untouched (no leftover
    re-parse — the components are sub-params, not standalone SGR)."""
    screen = feed_to("\x1b[31m\x1b[38:2:1:2mX")
    cell = screen.line(0)[0]
    assert cell.fg == 1  # the SGR 31 from before, untouched
    assert not cell.bold and not cell.dim


def test_colon_form_negative_components_clamp_to_zero() -> None:
    """`38:2::5:5` has an empty color-space slot and a missing blue:
    as (2, r, g, b) that is r=-1, which clamps to 0 — the rest read as
    written."""
    screen = feed_to("\x1b[38:2::5:5mX")
    assert screen.line(0)[0].fg == rgb(0, 5, 5)


def test_colon_and_semicolon_forms_interleave() -> None:
    screen = feed_to("\x1b[38:2:1:2:3m\x1b[38;2;4;5;6mX")
    assert screen.line(0)[0].fg == rgb(4, 5, 6)  # semicolon wins last


def test_rgb_and_palette_interleave() -> None:
    screen = feed_to("\x1b[31m\x1b[38;2;9;9;9m\x1b[38;5;2mX")
    assert screen.line(0)[0].fg == 2  # palette wins last


def test_truncated_rgb_is_ignored() -> None:
    """A truncated 38;2/48;2 leaves the color untouched; the leftover
    components fall through and re-parse as standalone SGR codes
    (xterm.js-verbatim: `38;2;1;2` sets bold + dim)."""
    screen = feed_to("\x1b[31;44m\x1b[38;2;1;2m\x1b[48;2;1mX")
    cell = screen.line(0)[0]
    assert cell.fg == 1  # untouched by the malformed 38;2
    assert cell.bg == 4  # untouched by the malformed 48;2
    assert cell.bold and cell.dim  # the leftover 1;2 re-parsed as SGR


def test_rgb_values_clamp_at_255() -> None:
    screen = feed_to("\x1b[38;2;300;0;128mX")
    assert screen.line(0)[0].fg == rgb(255, 0, 128)


def test_effective_rendition_passes_rgb_through() -> None:
    """The seam returns RGB ints as-is; DECSCNM swaps them."""
    screen = feed_to("\x1b[38;2;1;2;3;48;2;4;5;6m\x1b[?5hX")
    assert screen.effective_rendition(0, 0) == (rgb(4, 5, 6), rgb(1, 2, 3))
    assert screen.line(0)[0] == Cell("X", fg=rgb(1, 2, 3), bg=rgb(4, 5, 6))
