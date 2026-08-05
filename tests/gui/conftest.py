# -*- coding: utf-8 -*-
# Copyright (C) 2018-2026 Connet Information Technology Company, Shanghai.
"""Slice B GUI tests run headless: force the offscreen platform before
Qt is initialized (process-wide — the non-GUI tests don't care), and
ensure a QApplication exists for every test (QFontMetrics, clipboard)."""

import os

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


@pytest.fixture(autouse=True)
def _qt_app(qapp):
    """pytest-qt's session QApplication, made unconditional."""
    return qapp
