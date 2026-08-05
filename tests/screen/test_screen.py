"""T1 — Dumb screen tracer bullet: printable text lands in the grid.

The seam: the dispatcher protocol (parser → emulator) plus the screen's
read API (line(y), render()). Tests drive the full pipeline
`Parser.feed → Emulator → Screen` and observe the screen's state.
"""

from __future__ import annotations

from pyqterm.emulator import Emulator
from pyqterm.parser import Parser
from pyqterm.screen import Cell, Screen


def make_screen(lines: int = 24, columns: int = 80) -> tuple[Parser, Emulator, Screen]:
    """Build the full pipeline with a fresh screen."""
    screen = Screen(lines=lines, columns=columns)
    emulator = Emulator(screen)
    parser = Parser(emulator)
    return parser, emulator, screen


def feed_to(text: str, lines: int = 24, columns: int = 80) -> Screen:
    """Feed text through the full pipeline and return the screen."""
    parser, _emulator, screen = make_screen(lines, columns)
    parser.feed(text)
    parser.flush()
    return screen


def test_printable_text_lands_in_grid_cells() -> None:
    screen = feed_to("hi")
    assert screen.line(0)[0].data == "h"
    assert screen.line(0)[1].data == "i"


def test_render_shows_printed_text() -> None:
    screen = feed_to("hi")
    rendered = screen.render()
    assert rendered.split("\n")[0].startswith("hi")


def test_cursor_moves_past_printed_text() -> None:
    screen = feed_to("hi")
    assert (screen.cursor.x, screen.cursor.y) == (2, 0)


def test_unprinted_cells_are_blank() -> None:
    screen = feed_to("hi")
    blank = screen.line(0)[3]
    assert blank == Cell(data=" ", fg=-1, bg=-1)


def test_printed_cells_carry_default_rendition() -> None:
    screen = feed_to("x")
    cell = screen.line(0)[0]
    assert cell.fg == -1 and cell.bg == -1
    assert not (cell.bold or cell.underline or cell.reverse or cell.blink)


def test_cell_blank_classmethod_creates_default() -> None:
    assert Cell.blank() == Cell()


def test_screen_default_size_is_80x24() -> None:
    screen = Screen()
    assert screen.columns == 80
    assert screen.lines == 24
