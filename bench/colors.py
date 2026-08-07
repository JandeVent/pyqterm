#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2018-2026 Connet Information Technology Company, Shanghai.
"""Visualize the xterm-256 palette and truecolor rendering end to end.

Builds a color test card as escape sequences and feeds it through the
real pipeline — parser → emulator → screen → renderer — exactly the path
the app uses, then paints it into a PNG:

    python bench/colors.py [out.png]   # headless (offscreen Qt)
    python bench/colors.py --show      # save and open the image

The card covers:
  1. the 16 ANSI colors — fg swatches, bg swatches, bold fg (0–7 step
     up to their bright entries)
  2. the 6×6×6 cube (16–231) and the 24-step grayscale ramp (232–255)
     via SGR 48;5
  3. truecolor — primary ramps, a hue rainbow sweep, and two background
     gradients via SGR 38;2 / 48;2

The script also samples pixels back out of the painted image and
verifies known colors against what the escape sequences requested (the
same offscreen seam the GUI test suite uses), so a run either proves
the chain works or fails loudly.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Qt must see the offscreen platform before the QApplication exists
# (same pattern as bench/run.py — only when run directly).
if __name__ == "__main__":
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from PyQt6.QtGui import QColor, QImage  # noqa: E402
from PyQt6.QtWidgets import QApplication  # noqa: E402

from pyqtermx.render import TerminalRenderer  # noqa: E402
from pyqtermx.screen import rgb, rgb_parts  # noqa: E402
from pyqtermx.session import Session  # noqa: E402

LINES = 32
COLUMNS = 120

#: The 16 ANSI colors — the same tuple the renderer's palette starts
#: with (kept in sync with pyqtermx.render._PALETTE).
_PALETTE = (
    0x000000, 0xCD0000, 0x00CD00, 0xCDCD00, 0x0000EE, 0xCD00CD, 0x00CDCD, 0xE5E5E5,
    0x7F7F7F, 0xFF0000, 0x00FF00, 0xFFFF00, 0x5C5CFF, 0xFF00FF, 0x00FFFF, 0xFFFFFF,
)


class NoopPty:
    """The card is fed synchronously via `Session.process` — the reader
    thread never starts, so the pty is only a construction stand-in."""

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


# -- Color math -----------------------------------------------------------


def hue_rgb(h: float) -> tuple[int, int, int]:
    """HSV hue (degrees, 0–360) → RGB. Saturation/value fixed at 1."""
    h = h % 360
    x = 1 - abs((h / 60) % 2 - 1)
    if h < 60:
        r, g, b = 1.0, x, 0.0
    elif h < 120:
        r, g, b = x, 1.0, 0.0
    elif h < 180:
        r, g, b = 0.0, 1.0, x
    elif h < 240:
        r, g, b = 0.0, x, 1.0
    elif h < 300:
        r, g, b = x, 0.0, 1.0
    else:
        r, g, b = 1.0, 0.0, x
    return round(r * 255), round(g * 255), round(b * 255)


def lerp(a: int, b: int, t: float) -> int:
    return round(a + (b - a) * t)


# -- The card -------------------------------------------------------------


class Card:
    """Escape-sequence card builder: a list of rows, each row a list of
    (sgr, text) segments — every segment names its own rendition, so no
    state leaks across segments or rows."""

    def __init__(self) -> None:
        self.rows: list[list[tuple[bytes, bytes]]] = []
        self._row: list[tuple[bytes, bytes]] = []

    def put(self, sgr: bytes, text: str) -> None:
        self._row.append((sgr, text.encode()))

    def newline(self) -> None:
        self.rows.append(self._row)
        self._row = []

    def label(self, text: str) -> None:
        # Reset first: a bare `\x1b[1m` would leak the previous
        # segment's fg/bg into the label (and everything after it).
        self.put(b"\x1b[0;1m", text)
        self.newline()

    def blank(self) -> None:
        self.newline()

    def build(self) -> bytes:
        """All rows joined with CRLF — LF alone is a pure line feed in
        this emulator (xterm-accurate: the column is preserved), so a
        bare `\n` would continue each row at the previous row's column.
        """
        if self._row:
            self.newline()
        parts: list[bytes] = []
        for row in self.rows:
            for sgr, text in row:
                parts.append(sgr)
                parts.append(text)
            parts.append(b"\r\n")
        return b"".join(parts) + b"\x1b[0m"


def ansi_fg(index: int) -> bytes:
    """SGR for an ANSI fg index (0–15): 30–37 for 0–7, 90–97 for 8–15.
    Reset first — segments are self-contained."""
    return b"\x1b[0;%dm" % (30 + index if index < 8 else 90 + index - 8)


def ansi_bg(index: int) -> bytes:
    """SGR for an ANSI bg index (0–15): 40–47 for 0–7, 100–107 for 8–15.
    Reset first — segments are self-contained."""
    return b"\x1b[0;%dm" % (40 + index if index < 8 else 100 + index - 8)


def build_card() -> bytes:
    card = Card()
    card.put(b"\x1b[1m", "pyqtermx — xterm-256 + truecolor rendering")
    card.put(b"\x1b[0m", "   (generated by bench/colors.py, through the real pipeline)")
    card.newline()

    # 1. The 16 ANSI colors.
    card.label("ANSI colors — foreground (SGR 30–37 / 90–97)")
    for i in range(16):
        card.put(ansi_fg(i), "\u2588\u2588")  # ██
    card.newline()
    card.label("ANSI colors — background (SGR 40–47 / 100–107)")
    for i in range(16):
        card.put(ansi_bg(i), "  ")
    card.newline()
    card.label("ANSI colors — bold foreground (0–7 step up to bright)")
    for i in range(8):
        card.put(b"\x1b[0;1;%dm" % (30 + i), "\u2588\u2588")
    card.newline()
    card.blank()

    # 2. The 256-color cube and grayscale ramp.
    card.label("256-color cube 16–231 — background (SGR 48;5), 36 per row")
    for row in range(6):
        for i in range(36):
            card.put(b"\x1b[0;48;5;%dm" % (16 + row * 36 + i), "  ")
        card.newline()
    card.label("grayscale ramp 232–255 — background (SGR 48;5)")
    for i in range(24):
        card.put(b"\x1b[0;48;5;%dm" % (232 + i), "  ")
    card.newline()
    card.blank()

    # 3. Truecolor.
    card.label("truecolor — primary ramps, foreground (SGR 38;2)")
    for name, idx in (("red", 0), ("green", 1), ("blue", 2)):
        for i in range(48):
            comp = lerp(0, 255, i / 47)
            r, g, b = [comp if k == idx else 0 for k in range(3)]
            card.put(b"\x1b[0;38;2;%d;%d;%dm" % (r, g, b), "\u2588")
        card.newline()
    card.label("truecolor — hue rainbow, foreground (SGR 38;2)")
    for i in range(COLUMNS):
        r, g, b = hue_rgb(i * 360 / COLUMNS)
        card.put(b"\x1b[0;38;2;%d;%d;%dm" % (r, g, b), "\u2588")
    card.newline()
    card.label("truecolor — background gradients (SGR 48;2)")
    for a, b in ((0, 0xFFFFFF), (0xFF0000, 0x0000FF)):
        ar, ag, ab = (a >> 16) & 0xFF, (a >> 8) & 0xFF, a & 0xFF
        br, bg_, bb = (b >> 16) & 0xFF, (b >> 8) & 0xFF, b & 0xFF
        for i in range(COLUMNS):
            t = i / (COLUMNS - 1)
            sgr = b"\x1b[0;48;2;%d;%d;%dm" % (
                lerp(ar, br, t), lerp(ag, bg_, t), lerp(ab, bb, t),
            )
            # One space per column — 120 columns fit exactly on a row
            # (the 2-space swatch trick would wrap into two rows).
            card.put(sgr, " ")
        card.newline()
    card.blank()

    card.put(b"\x1b[0;2m", "If the ramps are smooth and the cube rows align, "
                           "xterm-256 and truecolor render end to end.")
    card.newline()
    return card.build()


# -- Verification ---------------------------------------------------------


def sample(image: QImage, renderer: TerminalRenderer, col: int, row: int) -> QColor:
    """The center pixel of cell (col, row) — for █ cells that is the
    foreground fill; for space cells the background fill."""
    x = round(col * renderer.cell_w + renderer.cell_w / 2)
    y = row * renderer.cell_h + renderer.cell_h // 2
    return QColor(image.pixelColor(x, y))


def verify(image: QImage, renderer: TerminalRenderer) -> int:
    """Sample known cells and compare against the colors the escape
    sequences requested. Returns the number of failed checks."""
    failures = 0
    print("pixel checks:")

    def check(label: str, col: int, row: int, expected: tuple[int, int, int]) -> None:
        nonlocal failures
        got = sample(image, renderer, col, row)
        if (got.red(), got.green(), got.blue()) != expected:
            failures += 1
            print(f"  FAIL {label}: expected {expected}, got "
                  f"({got.red()}, {got.green()}, {got.blue()})")

    # ANSI fg swatches (row 2): index 0 black, index 1 CD0000.
    check("ANSI fg 0", 0, 2, (0, 0, 0))
    check("ANSI fg 1", 2, 2, (0xCD, 0, 0))
    # ANSI bg swatches (row 4).
    check("ANSI bg 0", 0, 4, (0, 0, 0))
    check("ANSI bg 15", 30, 4, (0xFF, 0xFF, 0xFF))
    # Bold fg (row 6): index 0 steps up to bright 8 (7F7F7F).
    check("bold fg 0 -> bright 8", 0, 6, (0x7F, 0x7F, 0x7F))
    # Cube (row 9): 16 → (0,0,0), 17 → (0,0,95).
    check("cube 16", 0, 9, (0, 0, 0))
    check("cube 17", 2, 9, (0, 0, 95))
    # Grayscale (row 16): 232 → (8,8,8).
    check("gray 232", 0, 16, (8, 8, 8))
    # Red ramp (row 19): ends at pure red.
    check("red ramp start", 0, 19, (0, 0, 0))
    check("red ramp end", 47, 19, (255, 0, 0))
    # Rainbow (row 23): 120° green, 240° blue.
    check("rainbow 120deg", 40, 23, (0, 255, 0))
    check("rainbow 240deg", 80, 23, (0, 0, 255))
    # Background gradients (rows 25–26).
    check("bg lerp start", 0, 25, (0, 0, 0))
    check("bg lerp end", 119, 25, (255, 255, 255))
    check("bg red start", 0, 26, (255, 0, 0))
    check("bg red->blue end", 119, 26, (0, 0, 255))
    return failures


# -- Main -----------------------------------------------------------------


def render_card() -> QImage:
    """Feed the card through the real pipeline and paint it."""
    session = Session(NoopPty(), lines=LINES, columns=COLUMNS)
    session.process(build_card())
    snapshot = session.snapshots[-1]
    assert snapshot.full, "the first snapshot must be a full frame"

    renderer = TerminalRenderer()
    image = QImage(
        round(COLUMNS * renderer.cell_w),
        LINES * renderer.cell_h,
        QImage.Format.Format_RGB32,
    )
    renderer.render(image, snapshot)
    return image


def main(argv: list[str]) -> int:
    out = Path(argv[0]) if argv and not argv[0].startswith("-") else None
    show = "--show" in argv

    app = QApplication([])
    image = render_card()
    failures = verify(image, TerminalRenderer())

    target = (out or ROOT / "bench" / "results" / "colors.png")
    target.parent.mkdir(parents=True, exist_ok=True)
    if not image.save(str(target)):
        print(f"error: could not write {target}")
        return 1
    print(f"wrote {target} ({image.width()}x{image.height()} px, "
          f"{LINES}x{COLUMNS} cells)")

    if failures:
        print(f"{failures} pixel check(s) FAILED")
        return 1
    print("all pixel checks passed — the color chain renders correctly")
    if show:
        from PyQt6.QtCore import QUrl
        from PyQt6.QtGui import QDesktopServices

        if not QDesktopServices.openUrl(QUrl.fromLocalFile(str(target))):
            print("note: could not open the image — check it manually")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
