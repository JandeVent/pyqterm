# -*- coding: utf-8 -*-
# Copyright (C) 2018-2026 Connet Information Technology Company, Shanghai.
"""Render benchmark unittest — the paint path's regression guard.

Measures the rasterize cost of two workloads through the same seam as
bench/run.py (Session.process → Snapshot → renderer.paint into an
offscreen QImage, paint timed only, best of 3) and asserts each stays
within a tolerance of a stored, env-stamped baseline:

  - htop:           partial-damage frames (the canonical bench workload)
  - donut_fullscreen: full-screen redraws (the render-heavy case)

The baseline lives in bench/results/render_baseline.json, stamped with
platform/python/pyqt exactly like bench/results/baseline.json. First
run (or a missing entry) writes it and skips — the baseline is
established, not asserted. A run on a different env skips (numbers are
not comparable across machines). A run on the same env asserts
`measured < stored * TOLERANCE`, so a regression like the pre-batch
renderer (htop 3.86 ms/frame vs 1.64 now) fails the guard.
"""

from __future__ import annotations

import json
import platform
import sys
import time
from pathlib import Path

import pytest
from PyQt6.QtCore import PYQT_VERSION_STR
from PyQt6.QtGui import QImage, QPainter

from pyqtermx.render import DEFAULT_BG, TerminalRenderer
from pyqtermx.session import Session

# bench/ has no package __init__ — the workloads live there as modules.
BENCH = Path(__file__).resolve().parent.parent.parent / "bench"
sys.path.insert(0, str(BENCH))

from donut import A_STEP, B_STEP, _MOVE_HOME, render_frame  # noqa: E402
from frames import COLUMNS, LINES, htop_frames  # noqa: E402

BASELINE_PATH = BENCH / "results" / "render_baseline.json"

#: A regression must exceed this multiple of the stored baseline to
#: fail. 2x leaves ~50% headroom for machine noise while still catching
#: the pre-batch renderer (htop 3.86 vs 1.64 ms/frame).
TOLERANCE = 2.0

HTOP_FRAMES = 200
DONUT_FRAMES = 120


class NoopPty:
    """The bench never starts the reader thread — `Session.process` is
    driven directly (the benchmark seam, same as bench/run.py)."""

    @property
    def master_fd(self) -> int:
        return -1

    def read(self) -> bytes | None:
        return None

    def send_data(self, data: bytes) -> None:
        pass

    def set_window_size(self, rows: int, cols: int) -> None:
        pass

    def close(self) -> None:
        pass


def _paint_ms_per_frame(payloads: list[bytes]) -> float:
    """Best-of-3 rasterize ms/frame for `payloads` — only paint is
    timed; the input path runs synchronously outside the clock."""
    renderer = TerminalRenderer()
    image = QImage(
        round(COLUMNS * renderer.cell_w), LINES * renderer.cell_h, QImage.Format.Format_RGB32
    )
    image.fill(DEFAULT_BG)

    def run_once() -> float:
        session = Session(NoopPty(), lines=LINES, columns=COLUMNS, scrollback_limit=1000)
        session.process(b"")  # the initial full emit, as the thread does
        painter = QPainter(image)
        paint_s = 0.0
        try:
            for payload in payloads:
                session.process(payload)
                snap = session.snapshots[-1]
                row_indices = None if snap.full else snap.dirty_rows
                t0 = time.perf_counter()
                renderer.paint(painter, snap, LINES, row_indices=row_indices)
                paint_s += time.perf_counter() - t0
        finally:
            painter.end()
        return paint_s * 1000 / len(payloads)

    run_once()  # warmup
    return min(run_once() for _ in range(3))


def _htop_payloads() -> list[bytes]:
    return htop_frames(HTOP_FRAMES)


def _donut_payloads() -> list[bytes]:
    """The donut's per-frame payloads (the ~19 ms/frame projection math
    is generation, not render — it must not be inside the timed region)."""
    payloads: list[bytes] = []
    a = 0.0
    b = 0.0
    for _ in range(DONUT_FRAMES):
        payloads.append((_MOVE_HOME + render_frame(a, b, COLUMNS, LINES)).encode())
        a += A_STEP
        b += B_STEP
    return payloads


def _env() -> dict[str, str]:
    return {
        "platform": platform.platform(),
        "python": platform.python_version(),
        "pyqt": PYQT_VERSION_STR,
    }


def _load_baseline() -> dict | None:
    if BASELINE_PATH.exists():
        return json.loads(BASELINE_PATH.read_text())
    return None


def _write_baseline(workloads: dict[str, float]) -> None:
    BASELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
    BASELINE_PATH.write_text(json.dumps({"env": _env(), "workloads": workloads}, indent=2))


@pytest.mark.parametrize("name", ["htop", "donut_fullscreen"])
def test_paint_within_baseline(name: str) -> None:
    payloads = _htop_payloads() if name == "htop" else _donut_payloads()
    measured = _paint_ms_per_frame(payloads)
    baseline = _load_baseline()
    if baseline is None:
        _write_baseline({name: measured})
        pytest.skip(
            f"no baseline — wrote {BASELINE_PATH.name} "
            f"({name}: {measured:.2f} ms/frame)"
        )
    if _env() != baseline["env"]:
        pytest.skip("env differs from the stored baseline — numbers not comparable")
    stored = baseline["workloads"].get(name)
    if stored is None:
        _write_baseline({**baseline["workloads"], name: measured})
        pytest.skip(f"no {name} entry in baseline — recorded {measured:.2f} ms/frame")
    assert measured < stored * TOLERANCE, (
        f"{name} rasterize {measured:.2f} ms/frame exceeds baseline "
        f"{stored:.2f} × {TOLERANCE}"
    )