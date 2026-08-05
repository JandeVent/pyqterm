"""T04 — `?5` (DECSCNM, reverse video) via the `effective_rendition`
seam — the one new seam of Phase 3.

`effective_rendition(x, y)` returns the (fg, bg) a renderer should
draw for the cell at (x, y): the SGR `reverse` attribute and the
DECSCNM mode XOR — both on cancels out, either alone swaps fg/bg.
`render()` itself stays text-only; the mode lives in the generic DEC
registry (`?5h`/`?5l` were already wired by the registry in Phase 2).
"""

from pyqtermx.screen import Cell, Screen

from tests.screen.test_screen import feed_to, make_screen


def test_effective_rendition_is_cell_colors_without_mode() -> None:
    """With DECSCNM off, the effective rendition is the cell's own."""
    screen = feed_to("\x1b[31;44mHI")
    assert screen.effective_rendition(0, 0) == (1, 4)
    assert screen.effective_rendition(1, 0) == (1, 4)
    assert screen.effective_rendition(10, 10) == (-1, -1)  # blank


def test_decsnm_swaps_fg_bg_at_render_time() -> None:
    """`?5h` swaps the effective colors; the stored cell is unchanged."""
    screen = feed_to("\x1b[31;44m\x1b[?5hHI")
    assert screen.effective_rendition(0, 0) == (4, 1)
    cell = screen.line(0)[0]
    assert cell == Cell("H", fg=1, bg=4)  # stored raw


def test_decsnm_off_restores_rendition() -> None:
    """`?5l` turns reverse video back off."""
    screen = feed_to("\x1b[31;44m\x1b[?5h\x1b[?5lHI")
    assert screen.effective_rendition(0, 0) == (1, 4)


def test_sgr_reverse_stacks_with_decsnm_by_xor() -> None:
    """SGR 7 and DECSCNM both reverse; together they cancel (XOR)."""
    screen = feed_to("\x1b[31;44m\x1b[7mHI")  # SGR reverse alone
    assert screen.effective_rendition(0, 0) == (4, 1)
    screen = feed_to("\x1b[31;44m\x1b[7m\x1b[?5hHI")  # both on
    assert screen.effective_rendition(0, 0) == (1, 4)
    screen = feed_to("\x1b[31;44m\x1b[?5h\x1b[27mHI")  # DECSCNM only
    assert screen.effective_rendition(0, 0) == (4, 1)


def test_effective_rendition_reads_the_active_grid() -> None:
    """In the alternate screen, the alt grid's cells are the ones
    consulted (ADR-0004); the shared mode still applies."""
    parser, _emulator, screen = make_screen(4, 5)
    parser.feed("\x1b[31mabc\x1b[?1047h\x1b[?5h")
    parser.flush()
    # (0,0) holds main's red "a" — but the alt grid is blank, so the
    # effective rendition reads the alt cell: default colors. Reading
    # the main grid would give the swapped (-1, 1).
    assert screen.effective_rendition(0, 0) == (-1, -1)
    assert 5 in screen._dec_modes  # the shared mode is on in the alt


def test_render_stays_text_only() -> None:
    """render() output is identical with DECSCNM on or off."""
    off = feed_to("\x1b[31;44mHI")
    on = feed_to("\x1b[31;44m\x1b[?5hHI")
    assert on.render() == off.render()
