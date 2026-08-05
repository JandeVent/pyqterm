"""T1 — Ground dispatch: printable text and C0 controls flow to the handler.

The seam: the dispatcher protocol. Tests observe behavior through a recorder
handler (tests/recorder.py), never through parser internals.
"""

from __future__ import annotations

from tests.recorder import Recorder, feed, feed_bytes
from pyqterm.parser import Parser


def test_printable_run_is_one_text_event() -> None:
    assert feed("hello") == [("chars", "hello")]


def test_printable_run_accumulates_across_feeds() -> None:
    recorder = Recorder()
    parser = Parser(recorder)
    parser.feed("he")
    parser.feed("llo")
    parser.flush()
    assert recorder.events == [("chars", "hello")]


def test_control_breaks_printable_run() -> None:
    assert feed("a\nb") == [("chars", "a"), ("execute", 10), ("chars", "b")]


def test_all_c0_controls_execute() -> None:
    # 0x00–0x1F except ESC (0x1B), which starts an escape sequence.
    for code in range(0x00, 0x1B):
        assert feed(chr(code)) == [("execute", code)]
    for code in range(0x1C, 0x20):
        assert feed(chr(code)) == [("execute", code)]


def test_del_is_ignored_in_ground() -> None:
    assert feed("a\x7fb") == [("chars", "a"), ("chars", "b")]


def test_utf8_multibyte_character_is_one_text_event() -> None:
    assert feed("héllo") == [("chars", "héllo")]


def test_feed_bytes_decodes_incrementally() -> None:
    recorder = Recorder()
    parser = Parser(recorder)
    parser.feed_bytes(b"\xc3")  # first byte of é
    parser.feed_bytes(b"\xa9")
    parser.flush()
    assert recorder.events == [("chars", "é")]


def test_lone_continuation_byte_becomes_replacement_char() -> None:
    assert feed_bytes(b"\x9b") == [("chars", "\ufffd")]
