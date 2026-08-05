"""T6 — Hardening: streaming invariance and the no-crash guarantee.

Two load-bearing properties, exhaustive:

1. Byte-split invariance: every corpus input fed whole and fed in *every*
   possible chunking (byte splits can land mid-UTF-8, mid-CSI, mid-OSC, …)
   produces an identical event sequence.
2. No-crash guarantee: arbitrary bytes never raise, and after garbage the
   parser recovers to ground and parses clean input correctly.
"""

from __future__ import annotations

import random

import pytest

from pyqtermx.parser import Parser
from tests.recorder import Recorder

#: Corpus exercising every state family plus awkward boundaries.
_CORPUS = [
    b"",
    b"hello",
    b"\x1b",
    b"\x1b[",
    b"\x1b[31mred\x1b[0m",
    b"\x1b[1;2;3:4:5m",
    b"\x1b[>1;2q",
    b"\x1b[?25l",
    b"\x1b[9999999999m",  # param overflow
    b"\x1b[:::::::::m",  # subparam overflow
    b"\x1b]0;title\x07",
    b"\x1b]0;title\x1b\\",
    b"\x1b]",
    b"\x1bP1;2|payload\x1b\\",
    b"\x90payload\x9c",
    b"\x1bXpayload\x1b\\",
    b"\x1b^pm\x9c",
    b"\x9e\x9c",
    b"\x1b_payload\x9c",
    b"\x9f\x9c",
    b"\x1b(0\x1b(B",
    b"\x1b#8",
    b"\x1b7\x1b8\x1b=",
    b"\x1b[31;44",
    b"caf\xc3\xa9",  # é
    b"\xf0\x9f\x98\x80",  # 😀
    b"\xf0\x9f",  # truncated 4-byte UTF-8
    b"\x1b[\xc3",  # truncated UTF-8 inside CSI
    b"\x1b]8;;https://x.example/\x07link",
    b"\x1bP|" + bytes(range(0x20, 0x80)) + b"\x1b\\",
    b"\x1b[31m\x1b[2J\x1b[H\x1b(B\x1b]0;t\x07caf\xc3\xa9",
]

_GOOD = b"\x1b[31mHello \xf0\x9f\x91\x8d\x07"  # clean stream with UTF-8 + BEL


def _run(data: bytes, chunk_sizes: list[int]) -> list[tuple[object, ...]]:
    """Feed `data` in the given chunks; return the full event sequence."""
    recorder = Recorder()
    parser = Parser(recorder)
    offset = 0
    for size in chunk_sizes:
        parser.feed_bytes(data[offset : offset + size])
        offset += size
    parser.flush()
    return recorder.events


def _whole(data: bytes) -> list[tuple[object, ...]]:
    return _run(data, [len(data)])


def _all_chunkings(data: bytes) -> list[list[int]]:
    """Every composition of `data` into contiguous non-empty chunks."""
    if len(data) <= 12:
        chunkings: list[list[int]] = []
        for mask in range(2 ** max(len(data) - 1, 0)):
            chunks, start = [], 0
            for i in range(len(data) - 1):
                if mask >> i & 1:
                    chunks.append(i + 1 - start)
                    start = i + 1
            chunks.append(len(data) - start)
            chunkings.append(chunks)
        return chunkings
    # Long inputs: exhaustive chunking is 2^(n-1); sample fixed + random cuts.
    rng = random.Random(hash(data) & 0xFFFF)
    cuts = sorted(rng.sample(range(1, len(data)), min(8, len(data) - 1)))
    sizes: list[int] = []
    start = 0
    for cut in cuts:
        sizes.append(cut - start)
        start = cut
    sizes.append(len(data) - start)
    return [[len(data)]] + [sizes]


def test_whole_and_single_bytes_agree() -> None:
    for data in _CORPUS:
        expected = _whole(data)
        assert _run(data, [1] * len(data)) == expected, data


def test_byte_split_invariance() -> None:
    for data in _CORPUS:
        expected = _whole(data)
        for chunking in _all_chunkings(data):
            assert _run(data, chunking) == expected, (data, chunking)


def test_random_corpus_chunked_vs_whole() -> None:
    rng = random.Random(20260801)
    for _ in range(25):
        data = bytes(rng.randrange(0x100) for _ in range(rng.randrange(1, 300)))
        expected = _whole(data)
        cuts = sorted(rng.sample(range(1, len(data)), min(6, len(data) - 1)))
        sizes, start = [], 0
        for cut in cuts:
            sizes.append(cut - start)
            start = cut
        sizes.append(len(data) - start)
        assert _run(data, sizes) == expected, data.hex()


def test_fuzz_never_raises() -> None:
    rng = random.Random(0xDECAFBAD)
    for _ in range(200):
        size = rng.randrange(0, 2048)
        data = bytes(rng.randrange(0x100) for _ in range(size))
        _run(data, [size])  # must not raise


def test_fuzz_with_escape_payloads_never_raises() -> None:
    rng = random.Random(0xF00DFACE)
    prefixes = [b"\x1b[", b"\x1b", b"\x1b]", b"\x1bP", b"\x1b_", b"\x9b", b"\x9d"]
    for _ in range(200):
        payload = bytes(rng.randrange(0x100) for _ in range(rng.randrange(0, 128)))
        _run(rng.choice(prefixes) + payload, [len(payload) + len(prefixes)])


def test_recovers_to_ground_after_garbage() -> None:
    """Garbage then CAN: everything parsed afterwards must be clean."""
    rng = random.Random(0xBADC0DE)
    for _ in range(50):
        garbage = bytes(rng.randrange(0x100) for _ in range(rng.randrange(0, 512)))
        recorder = Recorder()
        parser = Parser(recorder)
        parser.feed_bytes(garbage)  # may print/execute while in GROUND: unasserted
        parser.feed_bytes(b"\x18")  # CAN: every state terminates to GROUND
        parser.feed_bytes(_GOOD)
        parser.flush()
        # The clean stream after the CAN must parse perfectly, whatever
        # happened before it.
        assert recorder.events[-3:] == [
            ("csi_dispatch", "", "", ((31,),), "m"),
            ("chars", "Hello \U0001F44D"),
            ("execute", 7),  # the trailing BEL of _GOOD
        ], garbage.hex()


def test_partial_utf8_spans_chunks() -> None:
    # A 4-byte character split 2|2 and a 3-byte one split 1|1|1.
    assert _run(b"\xf0\x9f", [2]) == []
    recorder = Recorder()
    parser = Parser(recorder)
    parser.feed_bytes(b"\xf0\x9f")
    parser.feed_bytes(b"\x98\x80")
    parser.flush()
    assert recorder.events == [("chars", "\U0001F600")]


def test_flush_boundary_matches_chunked_feed() -> None:
    recorder = Recorder()
    parser = Parser(recorder)
    parser.feed("ab")
    parser.feed("\x1b[31m")
    parser.flush()
    assert recorder.events == [("chars", "ab"), ("csi_dispatch", "", "", ((31,),), "m")]


def test_mid_sequence_utf8_does_not_desync() -> None:
    # A non-parameter code point inside CSI falls to the default (xterm.js
    # ERROR): it is ignored and the parser returns to GROUND.
    recorder = Recorder()
    parser = Parser(recorder)
    parser.feed_bytes(b"\x1b[")
    parser.feed_bytes(b"\xc3\xa9m")  # é is not a param byte: ignored
    parser.feed_bytes(b"\x1b[31mok")
    parser.flush()
    assert recorder.events == [
        ("chars", "m"),
        ("csi_dispatch", "", "", ((31,),), "m"),
        ("chars", "ok"),
    ]


@pytest.mark.parametrize(
    "data, trailing",
    [
        (b"\x1b[?", [("execute", 24)]),  # CSI_PARAM: CAN executes
        (b"\x1b[>", [("execute", 24)]),
        (b"\x1b]0;", []),  # OSC_STRING: CAN aborts without executing
        (b"\x1bP", [("execute", 24)]),  # DCS_ENTRY: CAN cancels via global
        (b"\x1b_", []),  # APC_ENTRY: CAN ends without executing
        (b"\x1b(", [("execute", 24)]),  # CHARSET: CAN executes
        (b"\x1b#", [("execute", 24)]),
        (b"\x1b ", [("execute", 24)]),  # ESCAPE_INTERMEDIATE
    ],
)
def test_truncated_sequences_then_resume(data: bytes, trailing: list[tuple[object, ...]]) -> None:
    recorder = Recorder()
    parser = Parser(recorder)
    parser.feed_bytes(data)
    parser.feed_bytes(b"\x18")  # cancel
    parser.feed_bytes(b"ok")
    parser.flush()
    assert recorder.events == trailing + [("chars", "ok")]
