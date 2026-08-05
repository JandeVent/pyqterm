# Reflow on resize, not clip

Resize re-wraps every line at the new width (and scrollback, once it exists) instead of truncating. VT102 clipped; modern terminals (xterm.js) reflow, which is what users expect when resizing split panes. Chosen now because it shapes the buffer representation — rows stay independent lists — and retrofitting reflow into a clipped buffer later would rewrite buffer and history handling.

## Accepted limitations (Step 2)

- ~~**Distinct full-width rows merge on widen.**~~ **Resolved in Phase 2.** Rows now carry a wrapped marker (`Row.wrapped`, xterm.js's `isWrapped`): set on the row a wrap lands on, cleared by an explicit line feed or by full-row erase (not by cursor motion or row/column shifts, matching xterm.js `insertCells`/`deleteCells`). Reflow consults it, so `abcd\r\nefgh` at 4 columns stays two rows when widened to 8. Scrollback (Phase 4) needs the marker anyway for history handling.
- **Reflow drops trailing padding, keeps everything else.** Only each row's trailing blank cells are discarded (they re-pad at the new width); leading and interior blanks, blank separator lines, graphic rendition, and wide characters survive. Unbounded combining-mark runs survive cell-for-cell.
- **The cursor clamps into the kept window** (spec: "clamped in"); it does not follow content through a shrink. Revisit when scrollback lands.
