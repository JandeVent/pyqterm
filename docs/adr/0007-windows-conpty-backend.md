# Windows support: a ConPTY pty behind the same narrow interface

pyqtermx targets Windows as well as Unix, and Windows has no fork or pty(4) — the platform pseudo-terminal is ConPTY (Windows 10 1809+). We add a second pty backend, `WinPty`, that implements the *same* narrow Qt-free interface as `pyqtermx.ptyspawn.Pty` (ADR-0005), selected by the entry point on `win32`. The emulator, session, and widget never know which backend they are driving.

## The model

- **Backend**: `pyqtermx/winpty.py` wraps **pywinpty** (the Rust winpty-rs rewrite, v3), `PtyProcess.spawn(argv, cwd, env, dimensions)` creating the ConPTY and the child. The wrapper is platform-guarded — the module imports on every OS, the `winpty` package only on Windows — so macOS/Linux builds and the mock tests are unaffected.
- **Selectability**: the session's reader loop `select()`s on `pty.master_fd` (ADR-0005). Python's `select` on Windows only accepts sockets, and a raw ConPTY pipe is not selectable — but pywinpty's `PtyProcess` already pumps the ConPTY output through a **loopback TCP socket pair**, so `master_fd` is `fileno()` of that socket and the reader loop works unchanged. A failed spawn leaves `master_fd = -1`; the loop's `except (OSError, ValueError)` ends it gracefully.
- **The byte contract**: pywinpty delivers `str` (UTF-8 decoded) and takes `str` — `read()` re-encodes to bytes, `send_data` decodes with `errors='replace'` (the xSide-Terminal reference implementation does the same). EOF surfaces as `EOFError` from the pump, mapped to the interface's `None` ("child is gone"); a dead-but-not-yet-flushed child also yields `None`.
- **Lifecycle**: `is_running`/`wait` map to `isalive()`/`exitstatus`; `close()` follows the Unix contract — EOF first (`close(force=False)`), bounded wait, then escalation. Windows has no SIGKILL: `terminate(force=True)` (SIGINT → SIGTERM escalation) is the kill-equivalent, and `signal()` maps SIGTERM to `os.kill` (TerminateProcess).
- **Failure parity**: a Unix exec failure exits the child with 127; a Windows spawn failure (`FileNotFoundError` — missing program) reports the same 127 exit status, so consumers see a dead session, not a live one.

## Considered options

- **Raw ConPTY via ctypes** (`CreatePseudoConsole`, `InitializeProcThreadAttributeList`, ...): no dependency, but a large amount of unsafe, error-prone Windows API plumbing for zero behavioral benefit over pywinpty — rejected.
- **Legacy winpty.dll backend**: pywinpty still offers it, but ConPTY is the modern path (Win10 1809+, proper resize/ANSI), and pywinpty's `Backend.ConPTY` is the default — winpty.dll not considered further.
- **`select` on the ConPTY pipe directly**: impossible — Python's `select` on Windows accepts sockets only. This is exactly the problem pywinpty's socket-pump design already solves; driving it through `master_fd` keeps the session loop platform-agnostic. Rejected alternatives: a polling reader thread inside the pty layer (would duplicate the session's single-writer loop) and a QSocketNotifier-based reader (Qt-coupled, breaks the headless harness).

## Accepted limitations

- **UTF-8 only**: ConPTY output is UTF-8-centric; non-UTF-8 bytes are replaced on the decode/re-encode roundtrip, unlike the byte-transparent Unix pty. Acceptable — xterm.js-class terminals and the reference implementation make the same trade.
- **No POSIX signals**: SIGTERM means TerminateProcess; Ctrl+C/Ctrl+Break are console events owned by ConPTY, not kill(). `signal()` is therefore narrower than on Unix.
- **pywinpty pump latency**: output crosses an extra socket hop (~1 ms); irrelevant at terminal rates.
- **Windows CI only**: the real-ConPTY integration tests are `skipif`-guarded and run only on Windows; the wrapper's contract is pinned everywhere by mock-backed tests.
