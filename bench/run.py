#!/usr/bin/env python3
"""The performance smoke test: three headless workloads, end-to-end numbers.

Usage:
    python bench/run.py            # run all workloads, print, write baseline.json
    python bench/run.py --compare  # print % change vs the stored baseline.json
    python bench/run.py --json     # machine-readable JSON, no baseline write

A plain run overwrites the baseline only when the env stamp matches the
stored one (same platform/Python/Qt) — the original numbers are never
lost to a cross-machine run (spec story 6).

Workloads (80×24, the reference grid), each measured end to end:

  1. scroll-flood — 10k seq-style lines through feed → Snapshot
                    (MB/s and lines/s; the input path's firehose case)
  2. htop —         incremental color/cursor frames (10 Hz cadence);
                    rasterize ms/frame of the damaged band + the
                    fraction of rows each frame actually repaints
  3. paste-burst —  1 MB bracketed paste; total elapsed ms

The input seam is `Session.process` (feed → flush → emit, the reader
thread's exact per-read step, synchronous — no thread). The paint seam
is the renderer painting a snapshot into an offscreen QImage, the same
QImage seam the GUI test suite uses. Standard library only, no display.

Results are written to results/baseline.json (env-stamped) on a plain
run, so later runs can `--compare`; there is no CI gate — comparison is
manual per optimization round.
"""

from __future__ import annotations

import json
import os
import platform
import sys
import time
from pathlib import Path

# Qt must see the offscreen platform before the QApplication exists.
if __name__ == "__main__":
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from PyQt6.QtCore import PYQT_VERSION_STR, Qt  # noqa: E402
from PyQt6.QtGui import QColor, QImage, QPainter  # noqa: E402
from PyQt6.QtWidgets import QApplication  # noqa: E402

from pyqterm.render import TerminalRenderer  # noqa: E402
from pyqterm.session import Session  # noqa: E402

from frames import htop_frames  # noqa: E402

LINES = 24
COLUMNS = 80
CHUNK = 32 * 1024  # a realistic pty read size

#: The reference colors the workloads paint with (default fg/bg).
DEFAULT_FG = QColor(Qt.GlobalColor.black)
DEFAULT_BG = QColor(Qt.GlobalColor.white)


class NoopPty:
    """The bench never starts the reader thread — `Session.process` is
    driven directly. This stand-in satisfies the pty protocol for
    construction only."""

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


def make_session() -> Session:
    return Session(NoopPty(), lines=LINES, columns=COLUMNS, scrollback_limit=1000)


def _feed(session: Session, data: bytes) -> None:
    """Feed `data` in realistic pty-sized chunks (T6 chunking — the
    result is identical to one big feed; this is how the real thread
    delivers it)."""
    for i in range(0, len(data), CHUNK):
        session.process(data[i : i + CHUNK])


# -- workloads ---------------------------------------------------------------


def scroll_flood(iterations: int = 5) -> dict[str, float]:
    """10k `seq`-style lines (CRLF like a pty delivers), fed through the
    full input path: bytes → parser → screen → Snapshot emission."""
    lines = 10000
    data = b"\r\n".join(b"%d" % i for i in range(1, lines + 1)) + b"\r\n"
    nbytes = len(data)

    def run() -> None:
        session = make_session()
        session.process(b"")  # the initial full emit, as the thread does
        _feed(session, data)

    run()  # warmup
    elapsed = min(_time(run, iterations))
    return {
        "mb_per_s": nbytes / elapsed / 1e6,
        "lines_per_s": lines / elapsed,
    }


def htop_incremental(iterations: int = 3) -> dict[str, float]:
    """1000 app frames at 10 Hz cadence: color bands + a moving cursor
    row, each frame a small CSI payload. Measures the paint path: the
    damaged band rasterized into an offscreen QImage (the widget would
    repaint exactly this region), and the mean fraction of rows that
    frame damaged."""
    renderer = TerminalRenderer()
    image = QImage(
        COLUMNS * renderer.cell_w, LINES * renderer.cell_h, QImage.Format.Format_RGB32
    )
    image.fill(DEFAULT_BG)

    frames = htop_frames()

    def run() -> tuple[float, float]:
        session = make_session()
        session.process(b"")  # initial full emit
        painter = QPainter(image)
        paint_ms = 0.0
        damaged_rows = 0
        try:
            for frame in frames:
                session.process(frame)
                snap = session.snapshots[-1]
                row_indices = None if snap.full else snap.dirty_rows
                if snap.full:
                    damaged_rows += LINES
                else:
                    damaged_rows += len(snap.dirty_rows)
                t0 = time.perf_counter()
                renderer.paint(painter, snap, LINES, row_indices=row_indices)
                paint_ms += (time.perf_counter() - t0) * 1000
        finally:
            painter.end()
        return paint_ms / len(frames), damaged_rows / len(frames) / LINES

    run()  # warmup
    samples = [run() for _ in range(iterations)]
    # Report the best (fastest) iteration — least scheduler noise.
    paint_ms, fraction = min(samples, key=lambda s: s[0])
    return {
        "rasterize_ms_per_frame": paint_ms,
        "damaged_rows_fraction": fraction,
    }


def paste_burst(iterations: int = 3) -> dict[str, float]:
    """1 MB bracketed paste — the burst case where input parse
    throughput is the wall."""
    line = b"lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor "
    data = b"\x1b[200~" + (line + b"\r\n") * 12400 + b"\x1b[201~"

    def run() -> None:
        session = make_session()
        session.process(b"")  # the initial full emit, as the thread does
        _feed(session, data)

    run()  # warmup
    elapsed = min(_time(run, iterations))
    return {"total_ms": elapsed * 1000, "mb_per_s": len(data) / elapsed / 1e6}


# -- harness -----------------------------------------------------------------


def _time(run, iterations: int) -> list[float]:
    """Mean-of-one: `iterations` fresh session runs, seconds each."""
    samples = []
    for _ in range(iterations):
        t0 = time.perf_counter()
        run()
        samples.append(time.perf_counter() - t0)
    return samples


def _env() -> dict[str, str]:
    return {
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "platform": platform.platform(),
        "python": platform.python_version(),
        "pyqt": PYQT_VERSION_STR,
    }


def run_all() -> dict:
    results = {"env": _env(), "workloads": {}}
    print("scroll-flood  ...", end="", flush=True)
    results["workloads"]["scroll_flood"] = scroll_flood()
    print(" htop  ...", end="", flush=True)
    results["workloads"]["htop_incremental"] = htop_incremental()
    print(" paste-burst  ...", end="", flush=True)
    results["workloads"]["paste_burst"] = paste_burst()
    print(" done")
    return results


def _fmt(v: float) -> str:
    return f"{v:,.2f}"


def print_summary(results: dict) -> None:
    flood = results["workloads"]["scroll_flood"]
    htop = results["workloads"]["htop_incremental"]
    paste = results["workloads"]["paste_burst"]
    print("\nscroll-flood    %s MB/s   %s lines/s" % (_fmt(flood["mb_per_s"]), _fmt(flood["lines_per_s"])))
    print("htop-incremental %s ms/frame rasterize  (%.1f%% of rows damaged)" % (
        _fmt(htop["rasterize_ms_per_frame"]), htop["damaged_rows_fraction"] * 100))
    print("paste-burst     %s ms total   %s MB/s" % (_fmt(paste["total_ms"]), _fmt(paste["mb_per_s"])))


def compare_with(stored: dict, current: dict) -> None:
    """Print % change, current vs stored. Negative % on time metrics and
    positive % on throughput metrics are the improvements."""
    for name, wl in current["workloads"].items():
        old = stored["workloads"][name]
        for metric, value in wl.items():
            delta = (value - old[metric]) / old[metric] * 100
            arrow = "↓" if (delta < 0) != ("_ms" in metric or "total" in metric) else "↑"
            print(f"  {name:18s} {metric:22s} {old[metric]:9,.2f} → {value:9,.2f}  ({delta:+7.1f}%) {arrow}")


def _env_diff(a: dict[str, str], b: dict[str, str]) -> list[str]:
    """Env-stamp keys that differ between two runs — numbers from
    different platforms/Pythons/Qt builds are not comparable."""
    return [k for k in ("platform", "python", "pyqt") if a.get(k) != b.get(k)]


def main() -> int:
    results_path = ROOT / "bench" / "results" / "baseline.json"
    args = sys.argv[1:]
    stored = None
    if results_path.exists():
        stored = json.loads(results_path.read_text())
    if "--compare" in args:
        if stored is None:
            print(f"no baseline at {results_path} — run `python bench/run.py` first")
            return 1
        current = run_all()
        print("\n% change vs stored baseline:\n")
        for key in _env_diff(stored.get("env", {}), current["env"]):
            print(f"  ! env differs on {key} ({stored['env'][key]} → "
                  f"{current['env'][key]}) — numbers are not comparable\n")
        compare_with(stored, current)
        return 0
    results = run_all()
    if "--json" in args:
        print(json.dumps(results, indent=2))
        return 0
    print_summary(results)
    if stored is not None:
        for key in _env_diff(stored.get("env", {}), results["env"]):
            print(f"refusing to overwrite {results_path}: env differs on {key} "
                  f"({stored['env'][key]} → {results['env'][key]})")
            print("the original numbers are never lost (spec story 6) — "
                  "delete the baseline first if this change is intentional")
            return 1
    results_path.parent.mkdir(parents=True, exist_ok=True)
    results_path.write_text(json.dumps(results, indent=2))
    print(f"\nbaseline written to {results_path}")
    return 0


if __name__ == "__main__":
    app = QApplication.instance() or QApplication(sys.argv)  # noqa: F841
    sys.exit(main())
