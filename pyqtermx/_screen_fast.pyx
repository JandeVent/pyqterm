# cython: language_level=3, boundscheck=False, wraparound=False
"""Cython fast path for Screen.print() — the inner character loop.

The hot path processes millions of characters per second. Moving the loop
to C eliminates Python interpreter dispatch overhead while keeping all
Python object operations (dict.get, Cell creation, list assignment) as
cpdef calls back into Python.

Design:
- print_text() takes the Screen object and text string
- Extracts all needed attributes at the start (hoisted out of loop)
- Processes each character in C (loop control, comparisons, width)
- Calls back into Python for dict operations, object creation, attribute writes
"""

from __future__ import annotations

from cpython.unicode cimport PyUnicode_READ_CHAR
from libc.stdint cimport int32_t

from .screen import (
    Cell,
    Screen,
    DECAWM,
    IRM,
    _CHARSETS,
    _CELL_INTERN_CAP,
    _pack_rendition,
)

# ============================================================================
# The fast print function
# ============================================================================

cpdef print_text(screen: Screen, text: str):
    """Fast path for Screen.print(): process text in C loop.

    The Screen object's state is extracted once at the start. The inner
    loop runs at C speed for the common case (ASCII printable in GROUND).
    Rare cases (wrap, combining,IRM) call back into Python methods.
    """
    # --- Hoist Screen attributes (done once, not per character) ---
    cdef object cursor = screen.cursor
    cdef list grid = screen._grid
    cdef int columns = screen.columns
    cdef int lines = screen.lines
    cdef bint decawm = screen.mode(DECAWM, private=True)
    cdef bint irm = screen.mode(IRM)

    # Charset translation
    cdef dict translate = None
    charset = screen._charsets[screen._charset_level]
    if charset != "B":
        translate = _CHARSETS[charset]

    # Cursor rendition (hoisted — can't change mid-batch)
    cdef int fg = cursor.fg
    cdef int bg = cursor.bg
    cdef bint bold = cursor.bold
    cdef bint underline = cursor.underline
    cdef bint reverse = cursor.reverse
    cdef bint blink = cursor.blink
    cdef bint dim = cursor.dim
    cdef bint italic = cursor.italic
    cdef bint hidden = cursor.hidden
    cdef bint strike = cursor.strike
    cdef bint overline = cursor.overline

    cdef object dirty = screen._dirty_rows
    cdef dict intern = screen._cell_intern
    cdef int x = cursor.x
    cdef int y = cursor.y
    cdef int marked_y = -1
    cdef int cells_y = -1
    cdef list cells = []

    # Pre-pack rendition
    cdef long long packed = _pack_rendition(
        fg, bg, bold, underline, reverse, blink,
        dim, italic, hidden, strike, overline,
    )

    # Cache frequently called methods
    cdef object dirty_add = dirty.add
    cdef object intern_get = intern.get
    cdef object grid_getitem = grid.__getitem__

    # Pre-create common keys (avoid tuple creation in hot loop)
    cdef tuple cont_key = ("", packed)

    cdef Py_ssize_t i, length = len(text)
    cdef int cp, width
    cdef str char, translated
    cdef tuple key
    cdef object cell, cont, row_obj
    cdef list row_cells
    cdef bint pending

    for i in range(length):
        # --- Read code point directly from C str buffer ---
        cp = <int>PyUnicode_READ_CHAR(text, i)
        char = <str>text[i]  # single-char string for dict/Cell

        # Charset translation (rare — only when not "B")
        if translate is not None and cp < 0x7F:
            translated = translate.get(cp, char)
            if translated is not char:
                char = translated

        # Mark row dirty (once per row)
        if marked_y != y:
            dirty_add(y)
            marked_y = y

        # Pending wrap resolution
        pending = cursor.pending_wrap
        if pending:
            # Call back into Python for _resolve_wrap + _mark_wrapped
            wrapped = screen._resolve_wrap()
            x = cursor.x
            y = cursor.y
            if wrapped:
                screen._grid[y].wrapped = True
            cells_y = -1

        # Width: ASCII is always 1, others need wcwidth
        if cp < 0x80:
            width = 1
        elif cp < 0xA0:
            # C0/C1 control — skip (not printable)
            continue
        else:
            width = screen._wcwidth(char)
            if width < 0:
                continue  # control character
            if width == 0:
                # Combining mark — call back into Python
                screen._attach_combining(char)
                continue

        # Wide char at right edge: wrap first
        if width == 2 and x >= columns - 1:
            if decawm:
                wrapped = screen._resolve_wrap()
                x = cursor.x
                y = cursor.y
                if wrapped:
                    screen._grid[y].wrapped = True
                cells_y = -1
            else:
                continue

        # Insert mode: call back into Python (rare)
        if irm:
            screen._insert_cells(y, x, width)

        # Cache row cells
        if cells_y != y:
            row_obj = grid_getitem(y)
            cells = row_obj.cells
            cells_y = y

        # --- Cell flyweight lookup (unavoidable Python) ---
        key = (char, packed)
        cell = intern_get(key)
        if cell is None:
            if len(intern) >= _CELL_INTERN_CAP:
                intern.clear()
            cell = Cell(char, fg, bg, bold, underline, reverse, blink,
                        dim, italic, hidden, strike, overline)
            intern[key] = cell

        cells[x] = cell

        # Second dirty mark (after wrap may have changed y)
        if marked_y != y:
            dirty_add(y)
            marked_y = y

        # Wide character continuation cell
        if width == 2:
            cont = intern_get(cont_key)
            if cont is None:
                cont = Cell("", fg, bg, bold, underline, reverse, blink,
                            dim, italic, hidden, strike, overline)
                intern[cont_key] = cont
            cells[x + 1] = cont

        # Advance cursor
        x += width
        if x >= columns:
            x = columns - 1
            if decawm:
                cursor.pending_wrap = True
        cursor.x = x
