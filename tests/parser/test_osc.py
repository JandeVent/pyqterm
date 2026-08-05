# -*- coding: utf-8 -*-
# Copyright (C) 2018-2026 Connet Information Technology Company, Shanghai.
"""T4 — OSC strings: payload collection, ST and BEL terminators.

The seam: the dispatcher protocol, observed through a recorder (tests/recorder.py).
"""

from __future__ import annotations

from tests.recorder import feed


def test_osc_terminated_by_bel() -> None:
    assert feed("\x1b]0;title\x07") == [("osc_dispatch", "0;title")]


def test_osc_terminated_by_esc_st() -> None:
    # xterm.js quirk: the ESC dispatches the payload, then the trailing
    # backslash of the two-byte ST dispatches as a no-op escape sequence.
    assert feed("\x1b]0;title\x1b\\") == [
        ("osc_dispatch", "0;title"),
        ("escape_dispatch", "", "\\"),
    ]


def test_osc_terminated_by_8bit_st() -> None:
    assert feed("\x1b]0;title\x9c") == [("osc_dispatch", "0;title")]


def test_8bit_osc() -> None:
    assert feed("\x9d0;title\x07") == [("osc_dispatch", "0;title")]


def test_can_cancels_osc_without_dispatch() -> None:
    # xterm.js: CAN terminates the string; the control is not executed.
    assert feed("\x1b]0;title\x18abc") == [("chars", "abc")]


def test_sub_cancels_osc_without_dispatch() -> None:
    assert feed("\x1b]0;title\x1aabc") == [("chars", "abc")]


def test_del_is_payload_in_osc() -> None:
    assert feed("\x1b]0;ti\x7ftle\x07") == [("osc_dispatch", "0;ti\x7ftle")]


def test_non_ascii_payload() -> None:
    assert feed("\x1b]8;;https://é.example\x07") == [
        ("osc_dispatch", "8;;https://é.example")
    ]


def test_executables_inside_osc_are_ignored() -> None:
    assert feed("\x1b]0;ti\x00tle\x07") == [("osc_dispatch", "0;title")]


def test_osc_restarted_by_new_osc() -> None:
    # A second 8-bit OSC_START aborts the first payload without dispatching
    # it (ESC cannot do this — ESC always terminates the string).
    assert feed("\x9d0;first\x9d0;second\x07") == [("osc_dispatch", "0;second")]


def test_osc_esc_then_other_escape() -> None:
    # ESC ends the payload; the following escape byte dispatches normally.
    assert feed("\x1b]0;title\x1b7") == [
        ("osc_dispatch", "0;title"),
        ("escape_dispatch", "", "7"),
    ]


def test_text_around_osc() -> None:
    assert feed("hello\x1b]0;x\x07world") == [
        ("chars", "hello"),
        ("osc_dispatch", "0;x"),
        ("chars", "world"),
    ]
