"""Snapshot → pixels (Slice B). The renderer paints viewport rows into a
QImage backing store the widget blits in paintEvent; it never touches
the model — it consumes only frozen `Snapshot` rows (ADR-0005).

Cell colors: `-1` is the default, `0–255` a 256-color palette index
(0–15 xterm, 16–231 the 6×6×6 cube, 232–255 grayscale), and `>= 0x1000000`
an RGB value (`pyqtermx.screen.rgb`). SGR support here: bold (palette
colors 0–7 step up to their bright entries), reverse (fg/bg swap),
dim (fg mixed halfway toward bg), underline, strike, overline, hidden
(no glyph), italic (font flag), and DECSCNM ?5 (whole-screen reverse).

Box-drawing (U+2500–257F) and block characters (U+2580–259F) are drawn
as vectors — painter.drawLine / fillRect quadrant math — not through the
font, so adjacent cells join seamlessly. Blink is parsed but not yet
painted (needs a widget timer).
"""

from __future__ import annotations

from collections.abc import Sequence

from PyQt6.QtCore import QRect, QRectF, Qt
from PyQt6.QtGui import QColor, QFont, QFontDatabase, QFontMetrics, QImage, QPainter

from pyqtermx.screen import Cell, Row, is_rgb, rgb_parts
from pyqtermx.selection import Selection, column_range
from pyqtermx.session import Snapshot

#: xterm's 16 ANSI colors (bright variants in the second half).
_PALETTE: tuple[int, ...] = (
    0x000000, 0xCD0000, 0x00CD00, 0xCDCD00, 0x0000EE, 0xCD00CD, 0x00CDCD, 0xE5E5E5,
    0x7F7F7F, 0xFF0000, 0x00FF00, 0xFFFF00, 0x5C5CFF, 0xFF00FF, 0x00FFFF, 0xFFFFFF,
)

#: The 6×6×6 color cube levels (16–231) and the grayscale ramp (232–255).
_CUBE_LEVELS = (0, 95, 135, 175, 215, 255)

DEFAULT_FG = QColor(0xE8, 0xE8, 0xE8)
DEFAULT_BG = QColor(0x10, 0x10, 0x10)

#: Block characters (U+2580–259F) as cell-relative fill rectangles
#: (fx, fy, fw, fh) — fillRect quadrant math, so adjacent cells join
#: without font gaps.
_BLOCK_FILLS: dict[int, tuple[tuple[float, float, float, float], ...]] = {
    0x2588: ((0.0, 0.0, 1.0, 1.0),),  # █ full
    0x258C: ((0.0, 0.0, 0.5, 1.0),),  # ▌ left half
    0x2590: ((0.5, 0.0, 0.5, 1.0),),  # ▐ right half
    0x2580: ((0.0, 0.0, 1.0, 0.5),),  # ▀ top half
    0x2584: ((0.0, 0.5, 1.0, 0.5),),  # ▄ bottom half
    0x259D: ((0.5, 0.0, 0.5, 0.5),),  # ▝ top-right
    0x2598: ((0.0, 0.0, 0.5, 0.5),),  # ▘ top-left
    0x2596: ((0.0, 0.5, 0.5, 0.5),),  # ▖ bottom-left
    0x2597: ((0.5, 0.5, 0.5, 0.5),),  # ▗ bottom-right
    0x259B: ((0.0, 0.0, 1.0, 0.5), (0.0, 0.5, 0.5, 0.5)),  # ▛
    0x259C: ((0.0, 0.0, 1.0, 0.5), (0.5, 0.5, 0.5, 0.5)),  # ▜
    0x2599: ((0.0, 0.0, 0.5, 0.5), (0.0, 0.5, 1.0, 0.5)),  # ▙
    0x259F: ((0.5, 0.0, 0.5, 0.5), (0.0, 0.5, 1.0, 0.5)),  # ▟
    0x259A: ((0.0, 0.0, 0.5, 0.5), (0.5, 0.5, 0.5, 0.5)),  # ▚
    0x259E: ((0.5, 0.0, 0.5, 0.5), (0.0, 0.5, 0.5, 0.5)),  # ▞
}


#: drawText alignment — a module constant: per-cell `|` on the enums
#: was ~0.65 s of the htop profile (enum.__or__ per cell).
_TEXT_FLAGS = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft

#: Box-drawing segment tables as cell-relative half-units — hoisted out
#: of the per-cell call (a `ls` box row hits these on every cell) while
#: reproducing the original absolute geometry exactly: a coordinate `u`
#: maps to `x + u * w // 2` (so 0 → x, 1 → the center, 2 → x + w).
_BOX_SEGS = {
    0x2500: ((0, 1, 2, 1),),  # ─
    0x2502: ((1, 0, 1, 2),),  # │
    0x250C: ((1, 1, 2, 1), (1, 1, 1, 2)),  # ┌
    0x2510: ((0, 1, 1, 1), (1, 1, 1, 2)),  # ┐
    0x2514: ((1, 1, 2, 1), (1, 1, 1, 0)),  # └ — right + up
    0x2518: ((0, 1, 1, 1), (1, 1, 1, 0)),  # ┘ — left + up
    0x251C: ((1, 0, 1, 2), (1, 1, 2, 1)),  # ├
    0x2524: ((1, 0, 1, 2), (0, 1, 1, 1)),  # ┤
    0x252C: ((0, 1, 2, 1), (1, 1, 1, 2)),  # ┬
    0x2534: ((0, 1, 2, 1), (1, 1, 1, 0)),  # ┴ — left + right + up
    0x253C: ((0, 1, 2, 1), (1, 0, 1, 2)),  # ┼
}


#: Cap for the renderer color flyweight: the 256-palette entries fit
#: comfortably, leaving headroom for arbitrary RGB ints — bounded like
#: screen's `_CELL_INTERN_CAP`, so a stream of unique RGB colors (a
#: rainbow dump) cannot grow the cache without bound.
_COLOR_CACHE_CAP = 4096


class TerminalRenderer:
    """Paints `Snapshot.rows` into an image sized `lines × columns`
    cells. One-shot: call `render` with each arriving snapshot."""

    def __init__(self, font: QFont | None = None, *, antialias: bool = True) -> None:
        # Copy the font so a caller-provided QFont is never mutated.
        if font is None:
            # "Menlo" only exists on macOS; on other platforms Qt falls
            # back to whatever font is closest, which may be a
            # proportional UI font. Use the platform's native
            # monospace font, falling back to Menlo/DejaVu Sans Mono.
            system = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
            if system.family():
                font = system
            else:
                font = QFont("Menlo", 12)
        self._font = QFont(font) if font is not None else QFont("Menlo", 12)
        if not antialias:
            # Opt out (experiments/GL comparisons): 1-bit glyph masks.
            # The shipped look is font-smoothed; crisp
            # pixel-aligned edges come from the grid geometry and the
            # off painter antialiasing, not from jagged glyphs; at a
            # Retina DPR a NoAntialias mask still shows sawtooth.
            self._font.setStyleStrategy(QFont.StyleStrategy.NoAntialias)
        metrics = QFontMetrics(self._font)
        self.cell_w = metrics.horizontalAdvance("M")
        self.cell_h = metrics.height()
        #: Derived fonts by (bold, italic) — a per-cell QFont would be
        #: hundreds of allocations per frame.
        self._font_cache: dict[tuple[bool, bool], QFont] = {}
        #: Cell color ints → QColor: a per-cell QColor construction was
        #: ~0.55 s of the htop profile (capped, see `_COLOR_CACHE_CAP`).
        self._color_cache: dict[tuple[int, bool], QColor] = {}

    def _color(self, color: int, default: QColor, *, bright: bool = False) -> QColor:
        """A cell color int → QColor (-1 → `default`), cached by value."""
        if color == -1:
            return default
        cache = self._color_cache
        key = (color, bright)
        qcolor = cache.get(key)
        if qcolor is not None:
            return qcolor
        if is_rgb(color):
            r, g, b = rgb_parts(color)
            qcolor = QColor(r, g, b)
        elif color < 8 and bright:
            color += 8
            qcolor = QColor(_PALETTE[color])
        elif color < 16:
            qcolor = QColor(_PALETTE[color])
        elif color < 232:
            value = color - 16
            qcolor = QColor(
                _CUBE_LEVELS[value // 36],
                _CUBE_LEVELS[(value // 6) % 6],
                _CUBE_LEVELS[value % 6],
            )
        else:
            gray = 8 + 10 * (color - 232)
            qcolor = QColor(gray, gray, gray)
        if len(cache) >= _COLOR_CACHE_CAP:
            cache.clear()
        cache[key] = qcolor
        return qcolor

    @property
    def font(self) -> QFont:
        """The glyph font (bold/italic variants derive from it)."""
        return self._font

    def _font_for(self, bold: bool, italic: bool) -> QFont:
        key = (bold, italic)
        font = self._font_cache.get(key)
        if font is None:
            font = QFont(self._font)
            font.setBold(bold)
            font.setItalic(italic)
            self._font_cache[key] = font
        return font

    def cell_rect(self, viewport_row: int, col: int) -> QRect:
        return QRect(col * self.cell_w, viewport_row * self.cell_h, self.cell_w, self.cell_h)

    def render(
        self,
        image: QImage,
        snapshot: Snapshot,
        rows: Sequence[Row] | None = None,
        row_indices: Sequence[int] | None = None,
        selection: Selection | None = None,
    ) -> None:
        """Paint the snapshot's rows into `image` (the CPU path — also
        the test seam: pixel checks read the image). `full` snapshots
        carry every viewport row at indices 0..lines-1; incremental
        snapshots carry only the dirty rows at their viewport indices.
        `rows` overrides the snapshot's rows with a merged viewport
        (the widget's persistent grid — the selection needs every row,
        not just the dirty ones). `row_indices` limits the repaint to
        specific viewport rows — partial rendering: the widget
        re-rasterizes only what a snapshot changed, not the whole
        frame. `selection` (viewport coordinates) renders the selected
        cells reversed.

        A dpr-scaled backing image (Retina: the widget's store is
        `logical × dpr` pixels) is painted in logical coordinates —
        QPainter applies the image's device-pixel ratio automatically,
        so glyphs rasterize at full device resolution and the widget's
        blit is 1:1 physical pixels, never an upscale."""
        painter = QPainter(image)
        try:
            dpr = image.devicePixelRatio()
            self.paint(
                painter,
                snapshot,
                round(image.height() / (self.cell_h * dpr)),
                rows=rows,
                row_indices=row_indices,
                selection=selection,
            )
        finally:
            painter.end()

    def paint(
        self,
        painter: QPainter,
        snapshot: Snapshot,
        viewport_lines: int,
        rows: Sequence[Row] | None = None,
        row_indices: Sequence[int] | None = None,
        selection: Selection | None = None,
    ) -> None:
        """Paint the snapshot onto an open painter — the widget's
        backing renderer (the CPU path renders into a QImage, then
        blits it). `rows` overrides the snapshot's rows with a merged
        viewport (the widget's persistent grid). Otherwise `full`
        snapshots carry every viewport row; incremental snapshots carry
        only the dirty rows at their viewport indices. `row_indices`
        limits the repaint to specific viewport rows — partial
        rendering: the widget repaints only the damaged region of the
        frame (and the cursor, when visible and its row is among them).
        `selection` (viewport coordinates) renders the selected cells
        reversed — the None fast path is untouched, so an idle
        selectionless frame costs nothing."""
        if rows is None:
            if snapshot.full:
                pairs: list[tuple[int, Row]] = list(enumerate(snapshot.rows))
            else:
                pairs = list(zip(snapshot.dirty_rows, snapshot.rows))
        else:
            pairs = list(enumerate(rows))
        if row_indices is not None:
            wanted = frozenset(row_indices)
            pairs = [(i, r) for i, r in pairs if i in wanted]
        for viewport_row, row in pairs:
            sel = column_range(selection, viewport_row) if selection is not None else None
            self._paint_row(painter, viewport_row, row, snapshot.reverse_video, sel)
        if snapshot.cursor_visible and snapshot.cursor[0] >= 0:
            cursor_row = snapshot.cursor[0] + snapshot.viewport_offset
            if row_indices is None or cursor_row in row_indices:
                self._paint_cursor(painter, snapshot, viewport_lines)

    # -- painting --------------------------------------------------------

    def _paint_row(
        self,
        painter: QPainter,
        viewport_row: int,
        row: Row,
        reverse_video: bool,
        sel_range: tuple[int, int] | None = None,
    ) -> None:
        """Two passes: all backgrounds, then all glyphs — a wide char's
        glyph spans its own cell and the empty continuation cell, so the
        continuation's background must be filled before the glyph (which
        would otherwise be overwritten by it). The painter stays open —
        callers own its lifecycle.

        Hot path: colors and fonts are cached (this method), and
        adjacent cells sharing a rendition are batched into runs — one
        fillRect per background run, one drawText per glyph run — so a
        full row of uniform text is a handful of Qt calls, not one per
        cell (per-cell drawText was ~44% of the htop profile). Box,
        block, and wide characters break runs and draw individually.
        `sel_range` (the selection's column range on this row, from
        `selection.column_range`) renders the row's selected cells
        reversed — the swap mirrors the SGR 7 XOR below, so selection
        combines correctly with it.

        When the Cython `_render_fast` extension is built, the per-cell
        loop runs there (`collect_runs` emits the same runs; the draw
        loop is mirrored in `paint_row`); this pure-Python body is the
        fallback and the reference the parity test compares against."""
        if _paint_row_fast is not None:
            _paint_row_fast(painter, self, viewport_row, row, reverse_video, sel_range)
            return
        color = self._color
        cw = self.cell_w
        ch = self.cell_h
        y0 = viewport_row * ch
        cells = row.cells
        n = len(cells)

        # Pass 1: backgrounds — one fillRect per run of identical bg.
        run_start = 0
        run_bg: QColor | None = None
        for col, cell in enumerate(cells):
            bg = color(cell.bg, DEFAULT_BG)
            if cell.reverse != reverse_video:  # SGR 7 XOR DECSCNM ?5
                bg = color(cell.fg, DEFAULT_FG)
            if sel_range is not None and sel_range[0] <= col <= sel_range[1]:
                # Selected: the background is the cell's foreground (the
                # glyph pass swaps the other way — they must agree).
                bg = (
                    color(cell.fg, DEFAULT_FG, bright=cell.bold)
                    if cell.reverse == reverse_video
                    else color(cell.bg, DEFAULT_BG, bright=cell.bold)
                )
            if bg != run_bg:
                if run_bg is not None:
                    painter.fillRect(run_start * cw, y0, (col - run_start) * cw, ch, run_bg)
                run_bg = bg
                run_start = col
        if run_bg is not None:
            painter.fillRect(run_start * cw, y0, (n - run_start) * cw, ch, run_bg)

        # Pass 2: glyphs — one drawText per run of identical rendition.
        font_for = self._font_for
        run_start = 0
        run_text: list[str] = []
        run_fg: QColor | None = None
        run_font_key: tuple[bool, bool] | None = None
        run_underline = False
        run_strike = False
        run_overline = False

        def flush(end_col: int) -> None:
            nonlocal run_text, run_fg, run_font_key, run_underline, run_strike, run_overline
            if not run_text:
                return
            assert run_fg is not None  # a run's fg/font are always set with it
            assert run_font_key is not None
            rect = QRect(run_start * cw, y0, (end_col - run_start) * cw, ch)
            painter.setFont(font_for(*run_font_key))
            painter.setPen(run_fg)
            painter.drawText(rect, _TEXT_FLAGS, "".join(run_text))
            if run_underline:
                painter.fillRect(rect.left(), rect.bottom() - 1, rect.width(), 1, run_fg)
            if run_strike:
                painter.fillRect(rect.left(), rect.top() + rect.height() // 2, rect.width(), 1, run_fg)
            if run_overline:
                painter.fillRect(rect.left(), rect.top(), rect.width(), 1, run_fg)
            run_text.clear()
            run_fg = None
            run_font_key = None
            run_underline = False
            run_strike = False
            run_overline = False

        for col, cell in enumerate(cells):
            if cell.hidden or cell.data == "":
                flush(col)
                continue  # continuation cells draw no glyph
            bg = color(cell.bg, DEFAULT_BG)
            fg = color(cell.fg, DEFAULT_FG, bright=cell.bold)
            if cell.reverse != reverse_video:
                # SGR 7 XOR DECSCNM: fg/bg swap — bold-is-bright
                # applies after the swap (xterm behavior).
                fg = color(cell.bg, DEFAULT_BG, bright=cell.bold)
                bg = color(cell.fg, DEFAULT_FG)
            if sel_range is not None and sel_range[0] <= col <= sel_range[1]:
                fg, bg = bg, fg  # selection renders reversed
            if cell.dim:
                # SGR 2: fg mixed halfway toward bg (xterm faint).
                fg = QColor(
                    (fg.red() + bg.red()) // 2,
                    (fg.green() + bg.green()) // 2,
                    (fg.blue() + bg.blue()) // 2,
                )
            cp = ord(cell.data[0]) if len(cell.data) == 1 else 0
            wide = col + 1 < n and cells[col + 1].data == ""
            if 0x2500 <= cp <= 0x257F or 0x2580 <= cp <= 0x259F or wide:
                # Box/block/wide chars break the run and draw individually.
                flush(col)
                rect = QRect(col * cw, y0, cw, ch)
                if wide:
                    # A wide char: one glyph across two cells.
                    rect.setWidth(2 * cw)
                if 0x2500 <= cp <= 0x257F:  # box-drawing, vector-drawn
                    self._draw_box_drawing(painter, rect, cp, fg)
                elif 0x2580 <= cp <= 0x259F:  # block characters, fillRects
                    self._draw_block_char(painter, rect, cp, fg, bg)
                else:
                    painter.setFont(font_for(cell.bold, cell.italic))
                    painter.setPen(fg)
                    painter.drawText(rect, _TEXT_FLAGS, cell.data)
                if cell.underline:
                    painter.fillRect(rect.left(), rect.bottom() - 1, rect.width(), 1, fg)
                if cell.strike:
                    painter.fillRect(rect.left(), rect.top() + rect.height() // 2, rect.width(), 1, fg)
                if cell.overline:
                    painter.fillRect(rect.left(), rect.top(), rect.width(), 1, fg)
                continue
            key = (cell.bold, cell.italic)
            if (
                fg == run_fg
                and key == run_font_key
                and cell.underline == run_underline
                and cell.strike == run_strike
                and cell.overline == run_overline
            ):
                run_text.append(cell.data)
            else:
                flush(col)
                run_start = col
                run_fg = fg
                run_font_key = key
                run_underline = cell.underline
                run_strike = cell.strike
                run_overline = cell.overline
                run_text.append(cell.data)
        flush(n)

    def _draw_box_drawing(self, painter: QPainter, rect: QRect, cp: int, color: QColor) -> None:
        """Box-drawing characters as painter.drawLine/drawArc — never the
        font, whose glyphs leave seams between adjacent cells. Unknown
        entries fall back to the font."""
        painter.setPen(color)
        x, y = rect.left(), rect.top()
        w, h = rect.width(), rect.height()
        cx, cy = x + w // 2, y + h // 2
        segs = _BOX_SEGS.get(cp)
        if segs is not None:
            # `u` is a half-unit: 0 → x, 1 → center, 2 → x + w.
            for sx, sy, ex, ey in segs:
                painter.drawLine(
                    x + sx * w // 2, y + sy * h // 2, x + ex * w // 2, y + ey * h // 2
                )
            return
        # Rounded corners ╭╮╯╰: an arc in the cell center + two legs
        # (rare enough that the tables stay inline here).
        r = min(w, h) // 4
        arcs = {
            0x256D: (0, -90, (cx + r, cy, x + w, cy), (cx, cy + r, cx, y + h)),  # ╭
            0x256E: (180, -90, (x, cy, cx - r, cy), (cx, cy + r, cx, y + h)),  # ╮
            0x256F: (90, 90, (x, cy, cx - r, cy), (cx, y, cx, cy - r)),  # ╯
            0x2570: (0, 90, (cx + r, cy, x + w, cy), (cx, y, cx, cy - r)),  # ╰
        }.get(cp)
        if arcs is not None:
            a0, a1, leg1, leg2 = arcs
            painter.drawArc(
                QRectF(cx - r, cy - r, 2 * r, 2 * r), a0 * 16, a1 * 16
            )
            painter.drawLine(*leg1)
            painter.drawLine(*leg2)
            return
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, chr(cp))

    def _draw_block_char(
        self, painter: QPainter, rect: QRect, cp: int, fg: QColor, bg: QColor
    ) -> None:
        """Block characters (U+2580–259F) as quadrant fillRects — the
        font version leaves gaps where adjacent cells should join
        seamlessly."""
        x, y = rect.left(), rect.top()
        w, h = rect.width(), rect.height()
        painter.fillRect(rect, bg)  # the unlit quadrants
        hw, hh = w / 2, h / 2
        fills = _BLOCK_FILLS.get(cp)
        if fills is not None:
            for fx, fy, fw, fh in fills:
                painter.fillRect(QRectF(x + fx * w, y + fy * h, fw * w, fh * h), fg)
            return
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, chr(cp))

    def _paint_cursor(
        self, painter: QPainter, snapshot: Snapshot, viewport_lines: int
    ) -> None:
        """The cursor as a reverse block at its viewport position (grid
        row plus the scroll offset — the viewport shows history rows
        above the grid); off-viewport cursors draw nothing."""
        y, x = snapshot.cursor
        viewport_row = y + snapshot.viewport_offset
        if not (0 <= viewport_row < viewport_lines):
            return
        rect = self.cell_rect(viewport_row, x)
        painter.fillRect(rect, DEFAULT_FG)


# Late import to avoid circular dependency (_render_fast imports render).
try:
    from ._render_fast import paint_row as _paint_row_fast  # type: ignore[import-not-found]
except ImportError:
    _paint_row_fast = None
