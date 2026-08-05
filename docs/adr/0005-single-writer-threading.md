# Single-writer threading: reader thread owns the emulator, GUI posts commands

pyqtermx gains a PTY and a GUI in the same phase, and the two ends of the pipeline must share the screen model. We chose a dedicated reader thread that is the **only writer** of terminal state: it reads the pty, applies every command (send_data, resize, scroll, close) from a serialized command queue, and emits change notifications as queued signals carrying **snapshots** (immutable changed rows, the viewport offset, the cursor position). The GUI thread never reads or writes the model directly — it renders from snapshots and posts commands. Rows and cells are frozen objects, so snapshot handoff needs no locks and no copies.

## The model

- **Reader thread owns emulator + screen.** All mutation happens here; there is no shared mutable state anywhere.
- **Command queue**: GUI → reader thread, consumed by the thread: `send_data(bytes)`, `resize(rows, cols)`, `scroll(n)`, `scroll_to_bottom()`, `close()`. Commands serialize with output reads in arrival order.
- **Snapshots**: emitted when anything visible changes — the changed row indices (dirty-row tracking on the emulator, cleared on read), immutable references to the rows, the viewport offset, and the cursor position. Delivered via queued Qt signals (auto-queued across threads); `Row`/`Cell` being frozen makes the handoff race-free by construction.
- **GUI is a pure consumer**: `TerminalView` repaints only the dirty lines from the latest snapshot; the QScrollBar mirrors the offset from snapshots and posts `scroll` commands on user input.
- **The pty layer is Qt-free** — a narrow `Pty` interface (`spawn`, output callback, `send_data`, `set_window_size`, `close`) so the whole pipeline is testable headless in pytest; the GUI instantiates it and drives it through the queue.

## Considered options

- **QSocketNotifier, all in the GUI thread** (QTermWidget-style): no threads at all, but every byte of pty output is processed on the GUI thread (jank under bursts), the pipeline becomes Qt-coupled, and Slice A loses its pure-pytest harness. Rejected.
- **QThread reader with writes/resize on the GUI thread**: the emulator and screen are then touched by two threads — a data race on every write. Rejected.
- **GUI reads the model under a lock**: reintroduces two writers plus locking; breaks the single-writer invariant the snapshot design gives us for free. Rejected.

## Accepted limitations

- Qt signals are the transport to the GUI; the model path itself stays Qt-free (the emulator/screen don't know Qt exists — the reader thread owns the Qt signal emission, in the pty/gui layer).
- A snapshot carries rows, not a copy of the whole grid: a burst of output that changes more rows than the grid height degenerates to a full-grid repaint — acceptable, it is exactly what a terminal must repaint anyway.
