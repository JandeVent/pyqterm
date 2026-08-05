"""T2 — CSI sequences + typed Params.

The seam: the dispatcher protocol, observed through a recorder (tests/recorder.py).
Expected values are literal strings and tuples, not recomputed by the code.
"""

from __future__ import annotations

from tests.recorder import feed


def test_sgr_with_one_param() -> None:
    assert feed("\x1b[31m") == [("csi_dispatch", "", "", ((31,),), "m")]


def test_multiple_params() -> None:
    assert feed("\x1b[1;2;3A") == [("csi_dispatch", "", "", ((1,), (2,), (3,)), "A")]


def test_multidigit_param() -> None:
    assert feed("\x1b[123m") == [("csi_dispatch", "", "", ((123,),), "m")]


def test_empty_param_is_zero() -> None:
    # "ESC [ ; 5 m": the first (empty) parameter defaults to 0.
    assert feed("\x1b[;5m") == [("csi_dispatch", "", "", ((0,), (5,)), "m")]


def test_no_params_is_zero_default_mode() -> None:
    # ECMA-48 default is sequence-specific; storage stores 0 (xterm.js ZDM).
    assert feed("\x1b[m") == [("csi_dispatch", "", "", ((0,),), "m")]
    assert feed("\x1b[A") == [("csi_dispatch", "", "", ((0,),), "A")]


def test_subparams() -> None:
    assert feed("\x1b[4:3m") == [("csi_dispatch", "", "", ((4, 3),), "m")]


def test_empty_subparam_is_minus_one() -> None:
    # "5::6" — the middle sub-parameter is empty; xterm.js stores -1.
    assert feed("\x1b[5::6m") == [("csi_dispatch", "", "", ((5, -1, 6),), "m")]


def test_private_prefix_question() -> None:
    assert feed("\x1b[?1h") == [("csi_dispatch", "", "?", ((1,),), "h")]


def test_private_prefix_greater_than() -> None:
    assert feed("\x1b[>0u") == [("csi_dispatch", "", ">", ((0,),), "u")]


def test_private_prefix_equals() -> None:
    assert feed("\x1b[=5c") == [("csi_dispatch", "", "=", ((5,),), "c")]


def test_intermediates() -> None:
    assert feed("\x1b[!p") == [("csi_dispatch", "!", "", ((0,),), "p")]


def test_8bit_csi() -> None:
    assert feed("\x9b31m") == [("csi_dispatch", "", "", ((31,),), "m")]


def test_second_prefix_byte_ignores_sequence() -> None:
    # A prefix byte after params started is malformed: ignore until final,
    # dispatch nothing, keep the stream in sync.
    assert feed("\x1b[1?5hX") == [("chars", "X")]


def test_truncated_csi_waits_for_more_input() -> None:
    recorder_feed = feed("\x1b[31")
    assert recorder_feed == []
    assert feed("\x1b[31m") == [("csi_dispatch", "", "", ((31,),), "m")]


def test_csi_spans_feeds() -> None:
    # Chunking mid-sequence must not change the outcome (T6 invariant).
    from tests.recorder import Recorder
    from pyqterm.parser import Parser

    recorder = Recorder()
    parser = Parser(recorder)
    parser.feed("\x1b[3")
    parser.feed("1m")
    parser.flush()
    assert recorder.events == [("csi_dispatch", "", "", ((31,),), "m")]


def test_can_cancels_csi() -> None:
    assert feed("\x1b[31\x18abc") == [("execute", 0x18), ("chars", "abc")]


def test_digit_overflow_is_capped() -> None:
    assert feed("\x1b[99999999999999999999m") == [
        ("csi_dispatch", "", "", ((0xFFFFFFFF,),), "m")
    ]


def test_params_capped_at_32() -> None:
    assert feed("\x1b[" + ";".join(["1"] * 40) + "m") == [
        ("csi_dispatch", "", "", ((1,),) * 32, "m")
    ]
