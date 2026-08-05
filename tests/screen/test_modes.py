# -*- coding: utf-8 -*-
# Copyright (C) 2018-2026 Connet Information Technology Company, Shanghai.
"""T02 — Mode registry (ANSI + DEC-private namespaces) and its setters.

SM/RM (CSI n h/l) and DECSET/DECRST (CSI ? n h/l) each collapse to one
loop over parameters, toggling modes in one of two registries on the
screen. Modes are named after their DEC/ANSI numbers (glossary); the
behavioral consumers (IRM/DECAWM/NLM) land in T03 — this ticket is the
registry and the wiring.

xterm.js truth: DECAWM (autowrap ?7) is ON by default; everything else
starts off. A sequence with no parameters defaults to mode 0, which is
no-op.
"""

from __future__ import annotations

from pyqtermx.screen import DECAWM, DECOM, IRM, NLM
from tests.screen.test_screen import feed_to


def test_modes_default_off_except_autowrap() -> None:
    screen = feed_to("")
    assert screen.mode(IRM) is False
    assert screen.mode(NLM) is False
    assert screen.mode(DECOM, private=True) is False
    assert screen.mode(DECAWM, private=True) is True


def test_sm_sets_ansi_mode() -> None:
    screen = feed_to("\x1b[4h")  # SM: insert mode on
    assert screen.mode(IRM) is True


def test_rm_resets_ansi_mode() -> None:
    screen = feed_to("\x1b[4h\x1b[4l")
    assert screen.mode(IRM) is False


def test_decset_sets_private_mode() -> None:
    screen = feed_to("\x1b[?7l\x1b[?6h")
    assert screen.mode(DECAWM, private=True) is False
    assert screen.mode(DECOM, private=True) is True


def test_decrst_resets_private_mode() -> None:
    screen = feed_to("\x1b[?7h\x1b[?7l")
    assert screen.mode(DECAWM, private=True) is False


def test_multiple_params_one_sequence() -> None:
    screen = feed_to("\x1b[4;20h")
    assert screen.mode(IRM) is True
    assert screen.mode(NLM) is True


def test_dec_multiple_params() -> None:
    screen = feed_to("\x1b[?6;7h")
    assert screen.mode(DECOM, private=True) is True
    assert screen.mode(DECAWM, private=True) is True


def test_namespaces_are_separate() -> None:
    # ?4 is DEC private (smooth scroll): toggling it must not touch ANSI
    # IRM (4) or vice versa.
    screen = feed_to("\x1b[?4h")
    assert screen.mode(IRM) is False
    assert screen.mode(4, private=True) is True
    screen = feed_to("\x1b[?4l")
    assert screen.mode(4, private=True) is False


def test_empty_params_default_to_mode_zero() -> None:
    # SM/RM with no parameters → mode 0: no-op, must not crash or
    # toggle anything real.
    screen = feed_to("\x1b[h\x1b[l")
    assert screen.mode(IRM) is False
    assert screen.mode(DECAWM, private=True) is True
