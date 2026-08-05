# -*- coding: utf-8 -*-
# Copyright (C) 2018-2026 Connet Information Technology Company, Shanghai.
"""T09 — the runnable app: `python -m pyqtermx` wires pty + session +
widget into a window. Smoke test: the window builds, the session runs
and delivers snapshots to the widget (offscreen)."""

from __future__ import annotations

from pytestqt.qtbot import QtBot
from PyQt6.QtWidgets import QMainWindow

from pyqtermx.__main__ import DEFAULT_COLUMNS, DEFAULT_LINES, build_window


def test_build_window_wires_the_layers(qtbot: QtBot) -> None:
    window, session = build_window()
    qtbot.addWidget(window)
    assert isinstance(window, QMainWindow)
    widget = window.centralWidget()
    assert widget is not None
    assert widget._session is session  # type: ignore[attr-defined]

    session.start()
    try:
        # The reader thread emits the initial full snapshot; the queued
        # signal delivers it to the widget (ADR-0005 bridge).
        qtbot.waitUntil(lambda: len(session.snapshots) >= 1)
        assert widget.sizeHint().width() == DEFAULT_COLUMNS * widget._renderer.cell_w  # type: ignore[attr-defined]
        assert widget.sizeHint().height() == DEFAULT_LINES * widget._renderer.cell_h  # type: ignore[attr-defined]
    finally:
        session.close()
