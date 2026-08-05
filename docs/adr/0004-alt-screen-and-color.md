# Alternate screen and color: xterm.js semantics, per-screen state

Full-screen apps (vim/htop-style) need an alternate screen, DECALN, reverse video, and truecolor. xterm.js erase-fills on entry, clears on *exit* for all of 47/1047/1049, carries the cursor position both ways, and keeps per-buffer DECSC slots — with a FIXME admitting its own deviation. The fixture corpus cannot arbitrate (the upstream alt-screen expected files are runner-era artifacts). We follow xterm.js verbatim — it is the project doctrine and its unit tests encode the adopted semantics.

## The model

- **Two grids, one screen.** The screen owns a normal grid and an alternate grid plus an active pointer; the emulator dispatches `?47`/`?1047`/`?1048`/`?1049` through the existing generic DEC mode registry.
- **Per-screen state**: grid, cursor *position* (x, y, pending wrap), scroll region, tab stops, DECSC slot (snapshot of position, rendition, charsets, origin/autowrap at save time). **Shared state**: mode registry, cursor *rendition*, charsets + level. The cursor splits internally into position + rendition; the public cursor API is unchanged.
- **Switch semantics**: entry = erase-fill (default fg, cursor's current bg); exit = clear, always (47 included); cursor carried both ways; `?1049` saves to the normal screen's DECSC slot on entry and restores from it on exit; the alt screen's own DECSC slot survives switches and clears; `?1048` is save/restore only; CSI `s`/`u` alias DECSC/DECRC.
- **Resize** reflows both grids independently under ADR-0003 (keep bottom rows, region resets to full screen, tab stops reset, saved positions clamp).
- **DECALN** (`ESC # 8`): fill the active grid with `E` stamped with the cursor's full current rendition (not the erase-fill rule), clear every wrapped marker, home the cursor. Bare `ESC 8` stays DECRC (exact-match dispatch).
- **Reverse video** (`?5`): stored mode only; the inversion is renderer-side via a new query `effective_rendition(x, y) -> (fg, bg)` — per-cell SGR reverse and DECSCNM each swap once and XOR-stack. Stored cells are never mutated; `render()` stays text-only.
- **Truecolor**: cell `fg`/`bg` stay integers — `-1` default, `0–255` palette index, `≥ 0x1000000` = 24-bit RGB `(r<<16)|(g<<8)|b|0x1000000`. `38;2`/`48;2` parse with truncated sequences ignored; components > 255 clamp (documented deviation — xterm.js leaves that an untestable packed-bit edge).
- **Bold-as-bright** is a renderer-side contract only (bold + fg 0–7 → bright, fg only, after the inversion), implemented with the future renderer.

## Accepted limitations

- **Real vim/htop headless is out of scope.** PTY capability negotiation is flaky; the milestone is a deterministic hand-built vim-style fixture plus the ported xterm.js unit tests.
- **The alt screen has no scrollback** (matching the model until the scrollback phase).
- **`effective_rendition` returns colors only** — attribute flags and bold-bright mapping belong to the renderer phase.
