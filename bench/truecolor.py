#!/usr/bin/env python3
"""Live truecolor test card — run it *inside* the terminal.

    python bench/truecolor.py      # fit the rainbow/gradients to the window
    python bench/truecolor.py 120  # force a width

Prints raw escape sequences (stdlib only — no Qt, no pyqterm imports):
the 16 ANSI colors, the 256-color cube and grayscale ramp, and
truecolor primary ramps, a hue rainbow, and background gradients via
SGR 38;2 / 48;2. A short environment report (COLORTERM, TERM) goes to
stderr — stdout carries only the card — and the full-width rows trim
to the window when it is narrower than 120 columns.

Run it inside pyqterm to eyeball 24-bit rendering: smooth ramps and
aligned cube rows mean the truecolor chain works end to end.
"""

from __future__ import annotations

import os
import sys

#: Full-card width: the rainbow and gradient rows span it. The 16-ANSI
#: and cube sections are narrower and fit any reasonable window.
FULL_WIDTH = 120


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


def build_card(columns: int) -> bytes:
    """The test card — the same rows as bench/colors.py's headless card
    (so its pixel checks apply verbatim), adapted to `columns` width for
    the rainbow and gradient rows."""
    card = Card()
    card.put(b"\x1b[1m", "pyqterm — xterm-256 + truecolor rendering")
    card.put(b"\x1b[0m", "   (live card from bench/truecolor.py — run inside the terminal)")
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
    for i in range(columns):
        r, g, b = hue_rgb(i * 360 / columns)
        card.put(b"\x1b[0;38;2;%d;%d;%dm" % (r, g, b), "\u2588")
    card.newline()
    card.label("truecolor — background gradients (SGR 48;2)")
    for a, b in ((0, 0xFFFFFF), (0xFF0000, 0x0000FF)):
        ar, ag, ab = (a >> 16) & 0xFF, (a >> 8) & 0xFF, a & 0xFF
        br, bg_, bb = (b >> 16) & 0xFF, (b >> 8) & 0xFF, b & 0xFF
        for i in range(columns):
            t = i / (columns - 1)
            sgr = b"\x1b[0;48;2;%d;%d;%dm" % (
                lerp(ar, br, t), lerp(ag, bg_, t), lerp(ab, bb, t),
            )
            # One space per column — the 2-space swatch trick would
            # wrap into two rows on narrow windows.
            card.put(sgr, " ")
        card.newline()
    card.blank()

    card.put(b"\x1b[0;2m", "If the ramps are smooth and the cube rows align, "
                           "xterm-256 and truecolor render end to end.")
    card.newline()
    return card.build()


# -- Environment report ----------------------------------------------------


def report(columns: int) -> str:
    """COLORTERM/TERM summary plus warnings that affect the verdict."""
    colorterm = os.environ.get("COLORTERM", "")
    term = os.environ.get("TERM", "(unset)")
    program = os.environ.get("TERM_PROGRAM", "")
    env = f"environment: COLORTERM={colorterm or '(unset)'} TERM={term}"
    if program:
        env += f" TERM_PROGRAM={program}"
    lines = [env]
    if "truecolor" not in colorterm and "24bit" not in colorterm:
        lines.append(
            "warning: COLORTERM is not truecolor — the app may fall back to "
            "256 colors; pyqterm sets COLORTERM=truecolor for its children"
        )
    if columns < FULL_WIDTH:
        lines.append(
            f"note: window is {columns} columns — the rainbow/gradient rows "
            f"are trimmed (the full card needs {FULL_WIDTH})"
        )
    return "\n".join(lines) + "\n"


# -- Main -----------------------------------------------------------------


def _term_columns() -> int:
    """The window width, clamped to the card's range; 120 when the
    width is unknowable (piped output)."""
    try:
        return min(FULL_WIDTH, max(10, os.get_terminal_size().columns))
    except OSError:
        return FULL_WIDTH


def main(argv: list[str]) -> int:
    columns = int(argv[0]) if argv and argv[0].isdigit() else _term_columns()
    # The report goes to stderr: stdout must carry only the card — a
    # terminal renders everything it receives, and LF-only lines (like
    # the report's) shift every following row's column.
    sys.stderr.write(report(columns))
    sys.stderr.flush()
    sys.stdout.buffer.write(build_card(columns))
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
