# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root — the domain glossary (this repo's ubiquitous language)
- **`docs/adr/`** — read ADRs that touch the area you're about to work in

If any of these files don't exist, proceed silently. Don't flag their absence; don't suggest creating them upfront.

## File structure

Single-context repo:

```
/
├── CONTEXT.md
├── docs/adr/
│   ├── 0001-code-point-parser.md
│   ├── 0002-full-state-skeleton.md
│   └── 0003-reflow-on-resize.md
└── pyqtermx/
```

## Language

Use the project's glossary terms throughout (cell, cursor, pending wrap, wrapped row, scroll region, erase fill, tab stop, graphic rendition, mode, …). See `CONTEXT.md` — it also lists terms to avoid.
