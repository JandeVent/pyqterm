# -*- coding: utf-8 -*-
# Copyright (C) 2018-2026 Connet Information Technology Company, Shanghai.
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
font, so adjacent cells join seamlessly. SGR blink is parsed but not yet
painted (needs a widget timer); the *cursor* blink is the widget's job —
`paint` takes a `cursor_visible` override the widget's timer drives.
"""

from __future__ import annotations

from collections.abc import Sequence

from PyQt6.QtCore import QPointF, QRect, QRectF, Qt
from PyQt6.QtGui import QColor, QFont, QFontDatabase, QFontMetrics, QFontMetricsF, QImage, QPainter

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
#: maps to `x + u * w / 2` (so 0 → x, 1 → the center, 2 → x + w).
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
                font.setPixelSize(12)
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
        self._default_fg = DEFAULT_FG
        self._default_bg = DEFAULT_BG
        self._apply_font(None)  # keep the prepared font, derive metrics

    def _apply_font(self, font: QFont | None) -> None:
        """(Re)derive the font, cell metrics, and derived-font cache."""
        self._font = QFont(font) if font is not None else self._font
        # Float cell width: QFontMetrics.horizontalAdvance returns an int
        # (rounded), but drawText/QTextLayout position glyphs at the
        # font's true fractional advance. An int cell_w made the grid
        # drift from the glyphs (±0.5px/cell, accumulating across the
        # row) and every run split (selection, rendition change)
        # re-anchor at an integer boundary, visibly shifting the text.
        # cell_w == the advance the layout uses, so glyphs land exactly
        # in their cells. cell_h stays int — vertical centering is
        # consistent across runs; the drift is purely horizontal.
        self.cell_w = QFontMetricsF(self._font).horizontalAdvance("M")
        self.cell_h = QFontMetrics(self._font).height()
        #: Derived fonts by (bold, italic) — a per-cell QFont would be
        #: hundreds of allocations per frame.
        self._font_cache: dict[tuple[bool, bool], QFont] = {}
        #: Cell color ints → QColor: a per-cell QColor construction was
        #: ~0.55 s of the htop profile (capped, see `_COLOR_CACHE_CAP`).
        self._color_cache: dict[tuple[int, bool], QColor] = {}

    def set_font(self, font: QFont) -> None:
        """Replace the glyph font and re-derive the cell grid metrics.
        The widget must rebuild its backing and re-post the resize
        after calling this (cell_w/cell_h changed)."""
        self._apply_font(font)

    def set_palette(self, fg: QColor, bg: QColor) -> None:
        """Replace the default foreground/background colors (the
        terminal's `-1` cell colors). The widget must re-render after
        calling this — the color cache is cleared so defaults are not
        baked into cached cells."""
        self._default_fg = fg
        self._default_bg = bg
        self._color_cache.clear()

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

    @property
    def default_fg(self) -> QColor:
        """The default foreground (the `-1` cell color)."""
        return self._default_fg

    @property
    def default_bg(self) -> QColor:
        """The default background (the `-1` cell color)."""
        return self._default_bg

    def _font_for(self, bold: bool, italic: bool) -> QFont:
        key = (bold, italic)
        font = self._font_cache.get(key)
        if font is None:
            font = QFont(self._font)
            font.setBold(bold)
            font.setItalic(italic)
            self._font_cache[key] = font
        return font

    def cell_rect(self, viewport_row: int, col: int) -> QRectF:
        return QRectF(col * self.cell_w, viewport_row * self.cell_h, self.cell_w, self.cell_h)

    def render(
        self,
        image: QImage,
        snapshot: Snapshot,
        rows: Sequence[Row] | None = None,
        row_indices: Sequence[int] | None = None,
        selection: Selection | None = None,
        cursor_visible: bool | None = None,
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
        cells reversed. `cursor_visible` overrides the snapshot's
        DECTCEM visibility for the cursor gate (the widget's blink
        phase) — `None` keeps the snapshot's value, and the override
        is ANDed with it, so the app's `?25l`/`?25h` always wins.

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
                cursor_visible=cursor_visible,
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
        cursor_visible: bool | None = None,
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
        selectionless frame costs nothing. `cursor_visible` overrides
        the snapshot's DECTCEM visibility for the cursor gate (the
        widget's blink phase) — `None` keeps the snapshot's value, and
        the override is ANDed with it, so the app's `?25l`/`?25h`
        always wins."""
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
        visible = (
            snapshot.cursor_visible
            if cursor_visible is None
            else snapshot.cursor_visible and cursor_visible
        )
        if visible and snapshot.cursor[0] >= 0:
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
            bg = color(cell.bg, self._default_bg)
            if cell.reverse != reverse_video:  # SGR 7 XOR DECSCNM ?5
                bg = color(cell.fg, self._default_fg)
            if sel_range is not None and sel_range[0] <= col <= sel_range[1]:
                # Selected: the background is the cell's foreground (the
                # glyph pass swaps the other way — they must agree).
                bg = (
                    color(cell.fg, self._default_fg, bright=cell.bold)
                    if cell.reverse == reverse_video
                    else color(cell.bg, self._default_bg, bright=cell.bold)
                )
            if bg != run_bg:
                if run_bg is not None:
                    painter.fillRect(
                        QRectF(run_start * cw, y0, (col - run_start) * cw, ch), run_bg
                    )
                run_bg = bg
                run_start = col
        if run_bg is not None:
            painter.fillRect(QRectF(run_start * cw, y0, (n - run_start) * cw, ch), run_bg)

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
            rect = QRectF(run_start * cw, y0, (end_col - run_start) * cw, ch)
            painter.setFont(font_for(*run_font_key))
            painter.setPen(run_fg)
            painter.drawText(rect, _TEXT_FLAGS, "".join(run_text))
            if run_underline:
                painter.fillRect(QRectF(rect.left(), rect.bottom() - 1, rect.width(), 1), run_fg)
            if run_strike:
                painter.fillRect(QRectF(rect.left(), rect.top() + rect.height() // 2, rect.width(), 1), run_fg)
            if run_overline:
                painter.fillRect(QRectF(rect.left(), rect.top(), rect.width(), 1), run_fg)
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
            bg = color(cell.bg, self._default_bg)
            fg = color(cell.fg, self._default_fg, bright=cell.bold)
            if cell.reverse != reverse_video:
                # SGR 7 XOR DECSCNM: fg/bg swap — bold-is-bright
                # applies after the swap (xterm behavior).
                fg = color(cell.bg, self._default_bg, bright=cell.bold)
                bg = color(cell.fg, self._default_fg)
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
                rect = QRectF(col * cw, y0, cw, ch)
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
                    painter.fillRect(QRectF(rect.left(), rect.bottom() - 1, rect.width(), 1), fg)
                if cell.strike:
                    painter.fillRect(QRectF(rect.left(), rect.top() + rect.height() // 2, rect.width(), 1), fg)
                if cell.overline:
                    painter.fillRect(QRectF(rect.left(), rect.top(), rect.width(), 1), fg)
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

    def _draw_box_drawing(self, painter: QPainter, rect: QRectF, cp: int, color: QColor) -> None:
        """Box-drawing characters as painter.drawLine/drawArc — never the
        font, whose glyphs leave seams between adjacent cells. Unknown
        entries fall back to the font. `rect` is a float cell rect — the
        lines land at fractional cell boundaries, so adjacent cells join
        exactly (QPointF: PyQt6's int drawLine overload rejects floats)."""
        painter.setPen(color)
        x, y = rect.left(), rect.top()
        w, h = rect.width(), rect.height()
        cx, cy = x + w / 2, y + h / 2
        segs = _BOX_SEGS.get(cp)
        if segs is not None:
            # `u` is a half-unit: 0 → x, 1 → center, 2 → x + w.
            for sx, sy, ex, ey in segs:
                painter.drawLine(
                    QPointF(x + sx * w / 2, y + sy * h / 2),
                    QPointF(x + ex * w / 2, y + ey * h / 2),
                )
            return
        # Rounded corners ╭╮╯╰: an arc in the cell center + two legs
        # (rare enough that the tables stay inline here).
        r = min(w, h) / 4
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
            painter.drawLine(QPointF(leg1[0], leg1[1]), QPointF(leg1[2], leg1[3]))
            painter.drawLine(QPointF(leg2[0], leg2[1]), QPointF(leg2[2], leg2[3]))
            return
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, chr(cp))

    def _draw_block_char(
        self, painter: QPainter, rect: QRectF, cp: int, fg: QColor, bg: QColor
    ) -> None:
        """Block characters (U+2580–259F) as quadrant fillRects — the
        font version leaves gaps where adjacent cells should join
        seamlessly."""
        x, y = rect.left(), rect.top()
        w, h = rect.width(), rect.height()
        painter.fillRect(rect, bg)  # the unlit quadrants
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
        painter.fillRect(rect, self._default_fg)


# Late import to avoid circular dependency (_render_fast imports render).
try:
    from ._render_fast import paint_row as _paint_row_fast  # type: ignore[import-not-found]
except ImportError:
    _paint_row_fast = None
