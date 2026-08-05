"""T8 — Charset designation and level shifts.

The screen owns four slots G0–G3 plus the active level (glossary
"Charset designation"); `ESC ( 0` fills G0 with the line-drawing charset,
`ESC ( B` restores ASCII, `ESC ( A` the UK charset. Print translates ASCII
code points (below 0x7F) through the active slot's map; Unicode is never
translated. SI/SO pick G0/G1, `ESC n`/`o` G2/G3, `ESC ~`/`}`/`|` G1R/G2R/G3R.
"""

from tests.screen.test_screen import feed_to


def test_default_is_ascii() -> None:
    screen = feed_to("q")
    assert screen.line(0)[0].data == "q"


def test_esc_paren_zero_designates_line_drawing() -> None:
    screen = feed_to("\x1b(0q")
    assert screen.line(0)[0].data == "\u2500"  # ─


def test_esc_paren_b_restores_ascii() -> None:
    screen = feed_to("\x1b(0q\x1b(Bq")
    assert screen.line(0)[0].data == "\u2500"
    assert screen.line(0)[1].data == "q"


def test_line_drawing_box_corners() -> None:
    screen = feed_to("\x1b(0lmkq")
    assert screen.line(0)[0].data == "\u250c"  # ┌
    assert screen.line(0)[1].data == "\u2514"  # └
    assert screen.line(0)[2].data == "\u2510"  # ┐
    assert screen.line(0)[3].data == "\u2500"  # ─


def test_line_drawing_vertical_and_junctions() -> None:
    screen = feed_to("\x1b(0xtuwv")
    assert screen.line(0)[0].data == "\u2502"  # │
    assert screen.line(0)[1].data == "\u251c"  # ├
    assert screen.line(0)[2].data == "\u2524"  # ┤
    assert screen.line(0)[3].data == "\u252c"  # ┬ (w)
    assert screen.line(0)[4].data == "\u2534"  # ┴ (v)


def test_uk_charset_maps_pound() -> None:
    screen = feed_to("\x1b(A#a")
    assert screen.line(0)[0].data == "\u00a3"  # £
    assert screen.line(0)[1].data == "a"  # the rest is ASCII


def test_unknown_charset_name_ignored() -> None:
    screen = feed_to("\x1b(1q")
    assert screen.line(0)[0].data == "q"


def test_designation_into_other_slots() -> None:
    # G1 designated, then made active via SO
    screen = feed_to("\x1b)0q\x0eq")
    assert screen.line(0)[0].data == "q"  # G0 still ASCII
    assert screen.line(0)[1].data == "\u2500"  # SO switched to G1


def test_si_so_toggle() -> None:
    screen = feed_to("\x1b)0\x0eq\x0fq")
    assert screen.line(0)[0].data == "\u2500"  # SO → G1
    assert screen.line(0)[1].data == "q"  # SI → G0


def test_ls2_ls3_and_right_shifts() -> None:
    screen = feed_to("\x1b*0\x1bnq")  # G2 designated, ESC n → G2
    assert screen.line(0)[0].data == "\u2500"
    screen = feed_to("\x1b+0\x1boq")  # G3 designated, ESC o → G3
    assert screen.line(0)[0].data == "\u2500"
    screen = feed_to("\x1b*0\x1b}q")  # G2 via LS2R
    assert screen.line(0)[0].data == "\u2500"
    screen = feed_to("\x1b+0\x1b|q")  # G3 via LS3R
    assert screen.line(0)[0].data == "\u2500"
    screen = feed_to("\x1b)0\x1b~q")  # G1 via LS1R
    assert screen.line(0)[0].data == "\u2500"


def test_unicode_never_translated() -> None:
    screen = feed_to("\x1b(0中q")
    assert screen.line(0)[0].data == "中"
    assert screen.line(0)[2].data == "\u2500"


def test_high_codepoints_pass_through() -> None:
    screen = feed_to("\x1b(0\u0100")
    assert screen.line(0)[0].data == "\u0100"


def test_line_drawing_is_single_width() -> None:
    screen = feed_to("\x1b(0q", columns=4)
    assert screen.cursor.x == 1  # ─ is one cell, not two
