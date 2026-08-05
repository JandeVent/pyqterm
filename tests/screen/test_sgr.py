"""T3 — Minimal SGR subset in the emulator.

The seam: the dispatcher protocol. `csi_dispatch` with final `m` sets the
cursor's graphic rendition; printed cells are stamped with it. Scope:
`0` (reset), `30–37` fg, `40–47` bg, `38;5` fg. Everything else is
parse-and-ignore.
"""

from __future__ import annotations

from tests.screen.test_screen import feed_to


def test_sgr_reset_restores_defaults() -> None:
    screen = feed_to("\x1b[31mred\x1b[0mplain")
    line = screen.render().split("\n")[0]
    assert line.startswith("redplain")
    cell = screen.line(0)[3]  # 'p'
    assert cell.fg == -1 and cell.bg == -1


def test_sgr_fg_colors_following_text() -> None:
    screen = feed_to("\x1b[31mred")
    for i, cell in enumerate(screen.line(0)[:3]):
        assert cell.data == "red"[i]
        assert cell.fg == 1


def test_sgr_bg_colors_following_text() -> None:
    screen = feed_to("\x1b[44mX")
    cell = screen.line(0)[0]
    assert cell.bg == 4


def test_sgr_38_5_sets_palette_index() -> None:
    screen = feed_to("\x1b[38;5;196mX")
    cell = screen.line(0)[0]
    assert cell.fg == 196


def test_sgr_missing_params_default_to_reset() -> None:
    screen = feed_to("\x1b[31mred\x1b[mplain")
    cell = screen.line(0)[3]
    assert cell.fg == -1


def test_truncated_38_5_is_ignored() -> None:
    # A 38;5 without the index is malformed — xterm ignores it rather than
    # defaulting to black (params.get returns 0 for a missing parameter).
    screen = feed_to("\x1b[38;5mX")
    assert screen.line(0)[0].fg == -1


def test_sgr_applies_to_run_of_chars() -> None:
    screen = feed_to("\x1b[32mhello")
    cells = screen.line(0)[:5]
    assert all(cell.fg == 2 for cell in cells)


def test_unknown_sgr_params_are_ignored() -> None:
    # Font selection (10) is not in scope; must not break the stream.
    screen = feed_to("\x1b[10mplain\x1b[0m")
    assert screen.render().split("\n")[0].startswith("plain")
    assert screen.line(0)[0].bold is False


def test_multiple_sgr_in_one_sequence() -> None:
    screen = feed_to("\x1b[31;44mX")
    cell = screen.line(0)[0]
    assert cell.fg == 1 and cell.bg == 4


def test_unknown_csi_finals_are_ignored() -> None:
    # Cursor moves (A–D) and erase (J/K) are Step 3; must not break the stream.
    screen = feed_to("\x1b[2Jab")
    assert screen.render().split("\n")[0].startswith("ab")


# -- Full attribute set (T7) --------------------------------------------

ATTR_SEQS = [
    ("\x1b[1m", "bold"),
    ("\x1b[2m", "dim"),
    ("\x1b[3m", "italic"),
    ("\x1b[4m", "underline"),
    ("\x1b[5m", "blink"),
    ("\x1b[6m", "blink"),  # rapid blink collapses to blink
    ("\x1b[7m", "reverse"),
    ("\x1b[8m", "hidden"),
    ("\x1b[9m", "strike"),
    ("\x1b[53m", "overline"),
]


def test_sgr_sets_each_attribute_flag() -> None:
    for seq, flag in ATTR_SEQS:
        screen = feed_to(seq + "X")
        assert getattr(screen.line(0)[0], flag) is True, f"{flag} not set by {seq!r}"


def test_sgr_attribute_composition() -> None:
    screen = feed_to("\x1b[1;3;7mX")
    cell = screen.line(0)[0]
    assert (cell.bold, cell.italic, cell.reverse) == (True, True, True)


def test_sgr_21_double_underline_sets_underline() -> None:
    screen = feed_to("\x1b[21mX")
    assert screen.line(0)[0].underline is True


def test_sgr_22_clears_bold_and_dim() -> None:
    screen = feed_to("\x1b[1;2mX\x1b[22mY")
    assert screen.line(0)[1].bold is False
    assert screen.line(0)[1].dim is False


def test_sgr_resets_clear_their_flags() -> None:
    screen = feed_to("\x1b[3;4;5;7;8;9;53mX\x1b[23;24;25;27;28;29;55mY")
    cell = screen.line(0)[1]
    for flag in ("italic", "underline", "blink", "reverse", "hidden", "strike", "overline"):
        assert getattr(cell, flag) is False, f"{flag} not cleared"


def test_sgr_reset_clears_new_flags_too() -> None:
    screen = feed_to("\x1b[1;2;3;4;5;6;7;8;9;53mX\x1b[0mY")
    cell = screen.line(0)[1]
    for flag in (
        "bold", "dim", "italic", "underline", "blink",
        "reverse", "hidden", "strike", "overline",
    ):
        assert getattr(cell, flag) is False, f"{flag} not reset"
    assert cell.fg == -1 and cell.bg == -1


def test_sgr_39_49_restore_default_colors() -> None:
    screen = feed_to("\x1b[31;44mX\x1b[39;49mY")
    cell = screen.line(0)[1]
    assert cell.fg == -1 and cell.bg == -1


def test_sgr_bright_fg_maps_to_palette_8_15() -> None:
    screen = feed_to("\x1b[90mX\x1b[97mY")
    assert screen.line(0)[0].fg == 8
    assert screen.line(0)[1].fg == 15


def test_sgr_bright_bg_maps_to_palette_8_15() -> None:
    screen = feed_to("\x1b[100mX\x1b[107mY")
    assert screen.line(0)[0].bg == 8
    assert screen.line(0)[1].bg == 15


def test_sgr_48_5_sets_bg_palette_index() -> None:
    screen = feed_to("\x1b[48;5;196mX")
    assert screen.line(0)[0].bg == 196
