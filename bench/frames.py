# -*- coding: utf-8 -*-
# Copyright (C) 2018-2026 Connet Information Technology Company, Shanghai.
"""The benchmark workload generators, shared by the harness and the
desktop GL A/B script.

Pure Python, no Qt imports, no environment side effects — importing
this module must be safe from a desktop session (the harness itself
forces the offscreen platform at import, which would break a real GL
A/B).
"""

from __future__ import annotations

#: The reference grid the workloads are built for (the harness's grid).
LINES = 24
COLUMNS = 80


def htop_frames(frames: int = 1000) -> list[bytes]:
    """1000 app frames at 10 Hz cadence: color bands + a moving cursor
    row, each frame a small CSI payload. Built once, replayed by both
    the headless harness and the desktop A/B — the two must measure
    the same workload."""
    out: list[bytes] = []
    for f in range(frames):
        parts = ["\x1b[%d;1H\x1b[%dm" % (band * 4 + 1, 31 + (band + f) % 6) + " " * COLUMNS
                 for band in range(5)]
        parts.append("\x1b[%d;1H\x1b[1mX" % (f % LINES + 1))
        out.append("".join(parts).encode())
    return out
