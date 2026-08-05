# -*- coding: utf-8 -*-
# Copyright (C) 2018-2026 Connet Information Technology Company, Shanghai.
"""T5 — DCS/SOS/PM/APC parse-and-ignore: consumed, never dispatched, no desync.

The seam: the dispatcher protocol, observed through a recorder (tests/recorder.py).
"""

from __future__ import annotations

from tests.recorder import feed


def test_dcs_consumed_without_dispatch() -> None:
    assert feed("\x1bP1;2|payload\x1b\\abc") == [
        ("escape_dispatch", "", "\\"),  # trailing backslash of the two-byte ST
        ("chars", "abc"),
    ]


def test_dcs_with_intermediates() -> None:
    assert feed("\x1bP!|data\x1b\\") == [("escape_dispatch", "", "\\")]


def test_8bit_dcs_terminated_by_8bit_st() -> None:
    assert feed("\x90payload\x9cabc") == [("chars", "abc")]


def test_dcs_containing_escape_does_not_desync() -> None:
    # The ESC inside the payload ends the string; what follows parses fresh.
    assert feed("\x1bP|esc\x1b\\X") == [("escape_dispatch", "", "\\"), ("chars", "X")]


def test_csi_after_dcs_parses_correctly() -> None:
    assert feed("\x1bPxyz\x1b\\\x1b[31m") == [
        ("escape_dispatch", "", "\\"),
        ("csi_dispatch", "", "", ((31,),), "m"),
    ]


def test_sos_ignored() -> None:
    assert feed("\x1bXpayload\x1b\\") == [("escape_dispatch", "", "\\")]


def test_pm_ignored() -> None:
    assert feed("\x1b^payload\x9c") == []


def test_8bit_sos_pm_ignored() -> None:
    assert feed("\x98payload\x9c") == []
    assert feed("\x9epayload\x9c") == []


def test_apc_ignored_until_st() -> None:
    assert feed("\x1b_payload\x9cabc") == [("chars", "abc")]


def test_apc_terminated_by_esc() -> None:
    # Unlike OSC, APC ends directly at ESC (xterm.js APC_END → GROUND).
    assert feed("\x1b_payload\x1b7") == [("chars", "7")]


def test_apc_8bit() -> None:
    assert feed("\x9fpayload\x9c") == []


def test_bel_does_not_terminate_apc() -> None:
    # BEL is not an APC terminator; the string continues until ST/ESC/CAN.
    assert feed("\x1b_payload\x07more\x9cabc") == [("chars", "abc")]


def test_stream_survives_all_string_types() -> None:
    soup = "\x1bP|d\x1b\\\x9d0;t\x07\x1b^p\x9c\x9fapc\x9c\x1b]8;;u\x07"
    assert feed(soup) == [
        ("escape_dispatch", "", "\\"),
        ("osc_dispatch", "0;t"),
        ("osc_dispatch", "8;;u"),
    ]
