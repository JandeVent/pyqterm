# Scrollback lives in the screen: history rows above the grid, one-stream reflow

Scrollback is the phase's biggest model change, and its shape decides reflow, the renderer, and the alt screen. We keep the history **inside the screen**: the normal state owns a bounded list of retained rows above the visible grid plus a viewport offset, and resize reflows history + grid as **one stream** (ADR-0003) so a wrapped line spanning the boundary re-joins exactly as it would if the screen were taller. Retention follows xterm: rows enter history only when a **full-screen-region** scroll pushes them off the top, the alt screen has none and never writes to it, the history is bounded (default 1000 rows, constructor-configurable), and only the new ED3 claim erases it.

## The model

- **Layout**: each normal-state `_ScreenState` gains `scrollback: list[Row]` (frozen rows, oldest first) and `scroll_offset: int`. The grid stays the visible region; history rows carry the same wrapped markers as grid rows.
- **Entry**: a scroll that pushes rows off the top of the grid while the scroll region is **full-screen** moves them into `scrollback`; a narrowed-region scroll discards them exactly as before. The cap drops oldest-first.
- **Alt screen**: excluded — no scrollback, no writes to history, entering/leaving never touches it (falls out of the per-screen model; pinned as a rule).
- **Erase**: ED1/ED2 and DECALN leave history untouched; **ED3 (`ESC[3J`)** is a new claim that clears the scrollback and snaps the viewport to 0. RIS (Phase 5) must also clear it.
- **Viewport**: `scroll_offset` counts rows up from the bottom, clamped to `[0, len(scrollback)]`; read side is `viewport_row(k)`. New output auto-scrolls only when the offset is 0; a key press snaps it back to 0 (`scroll_on_input`). The offset is model state, mutated only through the command queue — the renderer never writes it.

## Considered options

- **Separate `Scrollback` object owned by the emulator layer**: keeps the screen single-purpose, but reflow then coordinates two objects, and the wrapped-line-spanning-boundary case — the exact case reflow must get right — gets split across them. Rejected.
- **Renderer-side history**: the renderer snapshots rows that scroll off; reflow-on-resize becomes the renderer's job and headless tests can't see history at all. Rejected — the phase's harness is headless.
- **Unbounded history**: reflow cost and memory grow without bound; every terminal bounds it. Rejected (default 1000, configurable).

## Accepted limitations

- Reflow cost is bounded by the cap (1000 rows); widening re-joins and narrowing re-wraps the whole retained stream, not just the grid.
- `render()` stays text-only over the visible grid; scrollback is observable only through `viewport_row` and the viewport API — the headless tests assert through those seams.
