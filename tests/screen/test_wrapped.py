# -*- coding: utf-8 -*-
# Copyright (C) 2018-2026 Connet Information Technology Company, Shanghai.
"""T01 — Rows carry the wrapped marker (xterm.js isWrapped).

The marker rides on the row a wrap lands on, is cleared by an explicit
line feed, survives scroll, and is consulted by reflow on widen (the
ADR-0003 fix: distinct full-width rows no longer merge).

Semantics (locked in the Phase 2 design session, xterm.js verbatim):
- set on the row a wrap lands on (no scroll happened);
- cleared by an explicit line feed landing on the row — not by CR,
  and not by cursor motion;
- reflow-on-widen joins a wrapped row to the row above; an unwrapped
  row starts a new line.
"""

from __future__ import annotations

from tests.screen.test_screen import feed_to


def test_wrap_marks_the_landing_row() -> None:
    screen = feed_to("x" * 6, lines=2, columns=5)
    # 5 columns: "xxxxx" fills row 0, the 6th "x" wraps onto row 1.
    assert screen.line(1).wrapped is True


def test_no_wrap_leaves_rows_unwrapped() -> None:
    screen = feed_to("abc")
    assert screen.line(0).wrapped is False


def test_explicit_lf_clears_the_marker_on_the_landed_row() -> None:
    screen = feed_to("x" * 6 + "\n", lines=3, columns=5)
    # Wrap lands on row 1 (wrapped=True), then LF moves to row 2 and
    # clears the marker there — row 1 keeps its marker.
    assert screen.line(1).wrapped is True
    assert screen.line(2).wrapped is False


def test_cr_does_not_clear_the_marker() -> None:
    screen = feed_to("x" * 6 + "\rZ", lines=2, columns=5)
    # CR is not an explicit line feed: the wrap marker on row 1 stays.
    assert screen.line(1).wrapped is True


def test_wrap_at_bottom_scrolls_and_does_not_mark() -> None:
    screen = feed_to("a" * 4 + "b" * 4 + "c" * 4, lines=2, columns=4)
    # "aaaa" fills row 0; "bbbb" wraps onto row 1 (marked); "cccc" wraps
    # at the bottom, so the screen scrolls and the fresh row 1 is never
    # marked — it is a new line, not a continuation.
    assert screen.line(1).wrapped is False
    assert screen.render().split("\n")[1] == "cccc"


def test_marker_survives_scroll() -> None:
    screen = feed_to("x" * 4 + "y" * 5, lines=2, columns=4)
    # "xxxx" fills row 0; the 5th "y" wraps onto row 1 (marked) and the
    # rest fills it; the 6th "y" wraps at the bottom, scrolling the
    # marked row 1 up to row 0 — the marker rides along.
    assert screen.line(0).wrapped is True
    assert screen.render().split("\n")[0] == "yyyy"


def test_widen_joins_wrapped_rows() -> None:
    screen = feed_to("a" * 4 + "b" * 4, lines=2, columns=4)
    assert screen.line(1).wrapped is True
    screen.resize(1, 8)
    assert screen.render().split("\n")[0] == "aaaabbbb"


def test_widen_does_not_merge_unwrapped_rows() -> None:
    """ADR-0003 fix: `abcd\r\nefgh` at 4 columns stays two rows at 8."""
    screen = feed_to("abcd\r\nefgh", lines=2, columns=4)
    screen.resize(2, 8)
    rows = screen.render().split("\n")
    assert rows[0].rstrip() == "abcd"
    assert rows[1].rstrip() == "efgh"


def test_narrow_preserves_wrapped_flag() -> None:
    screen = feed_to("a" * 4 + "b" * 4, lines=2, columns=4)
    screen.resize(4, 2)
    assert screen.line(1).wrapped is True  # still a continuation
    screen.resize(1, 8)
    assert screen.render().split("\n")[0] == "aaaabbbb"
