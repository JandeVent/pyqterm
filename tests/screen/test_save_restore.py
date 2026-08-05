"""T10 — DECSC/DECRC: a single save slot for the cursor (position +
rendition), the charset slots and active level, and the origin/wraparound
modes. CSI `s`/`u` are aliases. Tab stops and the scroll region are not
saved (spec line 81).
"""

from tests.screen.test_screen import feed_to


def test_decsc_decrc_restores_position() -> None:
    screen = feed_to("abc\x1b7\x1b[2;5H\x1b8def", lines=4, columns=8)
    assert screen.line(0)[3].data == "d"
    assert screen.line(0)[5].data == "f"


def test_csi_s_u_are_aliases() -> None:
    screen = feed_to("abc\x1b[s\x1b[2;5H\x1b[uX", lines=4, columns=8)
    assert screen.line(0)[3].data == "X"


def test_decsc_decrc_restores_rendition() -> None:
    screen = feed_to("\x1b[1;31mX\x1b7\x1b[0m\x1b8Y", lines=2, columns=4)
    cell = screen.line(0)[1]
    assert cell.bold is True and cell.fg == 1


def test_decsc_decrc_restores_charset_level_and_slots() -> None:
    screen = feed_to("\x1b)0\x0e\x1b7\x0f\x1b8q", lines=2, columns=4)
    # G1 = line-drawing, SO made it active; after save + SI, restore
    # brings back the level (and the G1 slot)
    assert screen.line(0)[0].data == "\u2500"


def test_decsc_decrc_restores_origin_mode() -> None:
    screen = feed_to("\x1b[?6h\x1b7\x1b[?6l\x1b8", lines=4, columns=4)
    assert screen.mode(6, private=True) is True


def test_decsc_decrc_restores_wraparound_mode() -> None:
    screen = feed_to("\x1b[?7l\x1b7\x1b[?7h\x1b8", lines=4, columns=4)
    assert screen.mode(7, private=True) is False


def test_restore_without_save_is_noop() -> None:
    screen = feed_to("abc\x1b[2;2H\x1b8X", lines=2, columns=4)
    assert screen.line(1)[1].data == "X"  # cursor stayed at (1, 1)


def test_restore_clears_pending_wrap() -> None:
    screen = feed_to("x" * 4 + "\x1b7X\x1b8", lines=2, columns=4)
    assert screen.cursor.pending_wrap is False
    assert (screen.cursor.x, screen.cursor.y) == (3, 0)


def test_restore_clamps_after_resize() -> None:
    screen = feed_to("\x1b7\x1b[20;30H", lines=24, columns=40)
    screen.resize(10, 20)
    screen.restore_state()
    assert (screen.cursor.x, screen.cursor.y) == (0, 0)


def test_restore_clamps_into_region_under_origin() -> None:
    screen = feed_to("\x1b[?6h\x1b7\x1b[2;5r\x1b[1;1H\x1b8", lines=8, columns=8)
    # saved (0, 0) with DECOM on; restore re-applies the mode and
    # clamps the cursor up into the region top
    assert screen.cursor.y == 1


def test_tab_stops_not_saved() -> None:
    screen = feed_to("", columns=24)
    screen.set_cursor(3, 0)
    screen.set_tab_stop()
    screen.save_state()
    screen.clear_tab_stop(0)  # remove only the custom stop at 3
    screen.restore_state()
    screen.carriage_return()
    screen.tab()
    # had stops been saved, restore would re-add 3 and HT would land there
    assert screen.cursor.x == 8


def test_scroll_region_not_saved() -> None:
    screen = feed_to("", lines=8, columns=8)
    screen.set_scroll_region(2, 5)
    screen.save_state()
    screen.set_scroll_region(0, 7)
    screen.restore_state()
    assert (screen.scroll_top, screen.scroll_bottom) == (0, 7)


def test_single_slot_no_stack() -> None:
    screen = feed_to("\x1b7\x1b[2;2H\x1b7\x1b8X", lines=4, columns=8)
    # the second save overwrites the first: restore goes to (1, 1)
    assert screen.line(1)[1].data == "X"
