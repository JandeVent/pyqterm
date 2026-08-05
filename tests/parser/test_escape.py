"""T3 — ESC sequences + charset designation.

The seam: the dispatcher protocol, observed through a recorder (tests/recorder.py).
"""

from __future__ import annotations

from tests.recorder import feed


def test_esc_sequence_dispatches_by_final() -> None:
    assert feed("\x1b7") == [("escape_dispatch", "", "7")]


def test_esc_sequence_with_intermediates() -> None:
    # ESC # 8 (DECALN): '#' is the intermediate byte.
    assert feed("\x1b#8") == [("escape_dispatch", "#", "8")]


def test_intermediate_then_final_across_escapes() -> None:
    assert feed("\x1b!A") == [("escape_dispatch", "!", "A")]


def test_multiple_intermediates() -> None:
    assert feed("\x1b#$x") == [("escape_dispatch", "#$", "x")]


def test_charset_designation_g0() -> None:
    assert feed("\x1b(0") == [("designate_charset", "(", "0")]


def test_charset_designation_g1() -> None:
    assert feed("\x1b)A") == [("designate_charset", ")", "A")]


def test_charset_designation_g2_and_g3() -> None:
    assert feed("\x1b*B") == [("designate_charset", "*", "B")]
    assert feed("\x1b+4") == [("designate_charset", "+", "4")]


def test_charset_then_text() -> None:
    assert feed("\x1b(0abc") == [("designate_charset", "(", "0"), ("chars", "abc")]


def test_c1_execute_range() -> None:
    # IND (0x84), NEL (0x85), HTS (0x88), RI (0x8D) as 8-bit code points.
    for code in (0x84, 0x85, 0x88, 0x8D, 0x8E, 0x8F, 0x91, 0x97):
        assert feed(chr(code)) == [("execute", code)]


def test_esc_then_executable_stays_in_escape() -> None:
    # xterm.js: executables execute inside ESCAPE and the escape continues.
    assert feed("\x1b\n7") == [("execute", 10), ("escape_dispatch", "", "7")]


def test_truncated_escape_waits() -> None:
    assert feed("\x1b") == []
    assert feed("\x1b7") == [("escape_dispatch", "", "7")]


def test_esc_ignored_until_next_final_after_bad_intermediate() -> None:
    # ESC followed by an unrecognized intermediate then a printable is
    # implementation-defined; we return to ground without dispatch.
    assert feed("\x1b\x1b7") == [("escape_dispatch", "", "7")]
