# -*- coding: utf-8 -*-
# Copyright (C) 2018-2026 Connet Information Technology Company, Shanghai.
"""The runnable terminal (`python -m pyqtermx`) — thin glue: pty +
session + widget in a window. All behavior lives in the tested layers;
this module only wires them together.

Lifecycle (spec §9): window close → `Session.close` (the reader thread
stops and the master closes, delivering EOF/SIGHUP to the child).
"""

from __future__ import annotations

import os
import sys

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QMainWindow

from pyqtermx.session import Session
from pyqtermx.widget import TerminalWidget

# The pty backend is platform-native: the ConPTY wrapper (ADR-0007) on
# Windows, the fork-based pty (ADR-0005) elsewhere. Both implement the
# same narrow interface.
if sys.platform == "win32":
    from pyqtermx.win_pty import WinPty as Pty
else:
    from pyqtermx.ptyspawn import Pty

DEFAULT_LINES = 24
DEFAULT_COLUMNS = 80

FALLBACK_SHELL = "cmd.exe" if sys.platform == "win32" else "/bin/zsh"


def build_window(
    command: list[str] | None = None,
    rows: int = DEFAULT_LINES,
    cols: int = DEFAULT_COLUMNS,
) -> tuple[QMainWindow, Session]:
    """Construct the session and the window. `command` overrides the
    shell (`argv[1:]`); the session is started by the caller before the
    window is shown (so the initial full snapshot arrives queued,
    ADR-0005)."""
    pty = Pty(command or [os.environ.get("SHELL", FALLBACK_SHELL)], rows=rows, cols=cols)
    session = Session(pty, lines=rows, columns=cols)
    widget = TerminalWidget(session)
    window = QMainWindow()
    window.setWindowTitle("pyqtermx")
    window.setCentralWidget(widget)
    window.resize(widget.sizeHint() + QSize(0, 32))
    return window, session


def run(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv
    app = QApplication(args)
    window, session = build_window(command=args[1:] or None)
    app.aboutToQuit.connect(session.close)
    window.show()
    session.start()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(run())
