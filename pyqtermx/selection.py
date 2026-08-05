"""Mouse selection — the pure model behind click/drag selection.

Selection coordinates are *viewport* rows and columns (what the GUI can
see, ADR-0005): the widget holds only snapshot rows, so a selection is
cleared whenever the viewport scrolls — it selects visible text, not
buffer text (the GUI never reads the model).

Qt-free by design: rows are the frozen `Row`/`Cell` objects snapshots
carry, `column_range` feeds the renderer's per-cell paint test, and
`selected_text` produces the copy payload.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from .screen import Row

#: Open-ended column bound for mid-selection rows (the renderer's
#: `col <= end` test): far beyond any real grid width.
INF = 1 << 30


@dataclass(frozen=True)
class Selection:
    """A normalized selection: `row1 <= row2` and, within one row,
    `col1 <= col2`. `rectangular` is the Alt-drag mode — a column slice
    across rows instead of contiguous text."""

    row1: int
    col1: int
    row2: int
    col2: int
    rectangular: bool = False


def point(row: int, col: int) -> Selection:
    """A single-cell selection — the click anchor."""
    return Selection(row, col, row, col)


def word(row: int, col: int, rows: Sequence[Row]) -> Selection:
    """The word (maximal non-space run) containing the cell. A space
    cell is its own single-cell word; the hidden continuation cell of
    a wide char belongs to the word, so CJK text never splits
    mid-glyph."""
    cells = rows[row].cells if 0 <= row < len(rows) else []
    if col >= len(cells):
        return point(row, col)
    cell = cells[col]
    if cell.data.strip() == "" and not cell.hidden:
        return point(row, col)
    left = col
    while left > 0 and (cells[left - 1].data.strip() != "" or cells[left - 1].hidden):
        left -= 1
    right = col
    while right + 1 < len(cells) and (
        cells[right + 1].data.strip() != "" or cells[right + 1].hidden
    ):
        right += 1
    return Selection(row, left, row, right)


def line(row: int, columns: int) -> Selection:
    """The whole row (the copy contract trims trailing blanks)."""
    return Selection(row, 0, row, columns - 1)


def extend(
    anchor_row: int,
    anchor_col: int,
    row: int,
    col: int,
    rectangular: bool = False,
) -> Selection:
    """Drag: grow the selection from the fixed `(anchor_row, anchor_col)`
    cell toward `(row, col)`, normalized so `row1`/`col1` is always the
    start. The anchor is explicit because the normalized `Selection`
    stores no anchor — deriving it from `row1`/`col1` drifts: a drag
    past the anchor pushes it into `row2`/`col2`, and the next extend
    would then anchor at the *last mouse cell*, not the press cell.
    The widget remembers the press cell for the whole drag."""
    if (row, col) < (anchor_row, anchor_col):
        return Selection(row, col, anchor_row, anchor_col, rectangular)
    return Selection(anchor_row, anchor_col, row, col, rectangular)


def column_range(sel: Selection, row: int) -> tuple[int, int] | None:
    """The selected column range on a viewport row, or `None` when the
    row is untouched — the renderer's per-cell test. Mid-selection rows
    are open-ended (`INF`): they span the full width."""
    if row < sel.row1 or row > sel.row2:
        return None
    if sel.rectangular or row == sel.row1 == sel.row2:
        return (min(sel.col1, sel.col2), max(sel.col1, sel.col2))
    if row == sel.row1:
        return (sel.col1, INF)
    if row == sel.row2:
        return (0, sel.col2)
    return (0, INF)


def contains(sel: Selection, row: int, col: int) -> bool:
    """Whether the cell is selected — the hit-test that keeps a click
    inside the current selection from discarding it (xterm behavior)."""
    r = column_range(sel, row)
    return r is not None and r[0] <= col <= r[1]


def selected_text(rows: Sequence[Row], sel: Selection) -> str:
    """The selected text — the copy contract: per row, the selected
    cells' data (hidden continuations of wide chars skipped), trailing
    blanks trimmed, rows joined with newlines. Rows and columns are
    clamped to what the viewport actually holds."""
    view = rows[max(0, sel.row1) : sel.row2 + 1]
    out: list[str] = []
    for i, row in enumerate(view):
        first, last = i == 0, i == len(view) - 1
        if sel.rectangular:
            c1, c2 = min(sel.col1, sel.col2), max(sel.col1, sel.col2)
        elif first and last:
            c1, c2 = min(sel.col1, sel.col2), max(sel.col1, sel.col2)
        elif first:
            c1, c2 = sel.col1, len(row.cells)
        elif last:
            c1, c2 = 0, sel.col2
        else:
            c1, c2 = 0, len(row.cells)
        text = "".join(c.data for c in row.cells[c1 : c2 + 1] if not c.hidden)
        out.append(text.rstrip())
    return "\n".join(out)
