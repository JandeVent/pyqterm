# cython: language_level=3, boundscheck=False, wraparound=False
# -*- coding: utf-8 -*-
# Copyright (C) 2018-2026 Connet Information Technology Company, Shanghai.
"""Cython reimplementation of the VT500/xterm stream parser.

The hot path (feed inner loop) runs at C speed: no Python per-character
overhead, flat array lookup, and direct method calls for actions. The
Dispatcher protocol boundary is a cpdef call — unavoidable, but the
common path (PRINT in GROUND) bypasses it entirely.
"""

from __future__ import annotations

import codecs
from enum import Enum, auto

from .dispatcher import Dispatcher
from .params import ParamsBuilder

# ============================================================================
# Enums
# ============================================================================

class ParserState(Enum):
    GROUND = 0
    ESCAPE = 1
    ESCAPE_INTERMEDIATE = 2
    CSI_ENTRY = 3
    CSI_PARAM = 4
    CSI_INTERMEDIATE = 5
    CSI_IGNORE = 6
    OSC_STRING = 7
    CHARSET = 8
    DCS_ENTRY = 9
    DCS_PARAM = 10
    DCS_INTERMEDIATE = 11
    DCS_IGNORE = 12
    SOS_PM_STRING = 13
    APC_ENTRY = 14


class Action(Enum):
    PRINT = 0
    EXECUTE = 1
    CLEAR = 2
    IGNORE = 3
    COLLECT = 4
    PARAM = 5
    CSI_DISPATCH = 6
    ESC_DISPATCH = 7
    CHARSET_DISPATCH = 8
    OSC_START = 9
    OSC_PUT = 10
    OSC_END = 11
    OSC_ABORT = 12


# ============================================================================
# Character classification constants
# ============================================================================

ASCII_PRINTABLE = (0x20, 0x7E)
UNICODE_MAX_CODE_POINT = 0x10FFFF
UNICODE_PRINTABLE = (0xA0, UNICODE_MAX_CODE_POINT)

C0_EXECUTABLE_RANGES = ((0x00, 0x17), (0x19, 0x19), (0x1C, 0x1F))
ESC_CHARACTER = (0x1B, 0x1B)
DEL_CHARACTER = (0x7F, 0x7F)
CAN_CHARACTER = (0x18, 0x18)
SUB_CHARACTER = (0x1A, 0x1A)
BEL_CHARACTER = (0x07, 0x07)

CSI_FINAL_CHARACTERS = (0x40, 0x7E)
INTERMEDIATE_CHARACTERS = (0x20, 0x2F)
CSI_PARAMETER_CHARACTERS = (0x30, 0x3F)
CSI_PARAMETER_DATA_CHARACTERS = (0x30, 0x3B)
CSI_DIGIT_CHARACTERS = (0x30, 0x39)
CSI_SUBPARAMETER_SEPARATOR = 0x3A
CSI_PARAMETER_SEPARATOR = 0x3B
CSI_PRIVATE_PREFIX_CHARACTERS = (0x3C, 0x3F)
CSI_PREFINAL_CHARACTERS = (0x20, 0x3F)
ESC_FINAL_CHARACTERS = (0x30, 0x7E)
CHARSET_DESIGNATORS = (0x28, 0x29, 0x2A, 0x2B)

C1_EXECUTE_RANGES = ((0x80, 0x8F), (0x91, 0x97))
C1_DCS = (0x90, 0x90)
C1_SOS = (0x98, 0x98)
C1_CAN = (0x99, 0x99)
C1_SUB = (0x9A, 0x9A)
C1_CSI = (0x9B, 0x9B)
C1_ST = (0x9C, 0x9C)
C1_OSC = (0x9D, 0x9D)
C1_PM = (0x9E, 0x9E)
C1_APC = (0x9F, 0x9F)


def in_range(code_point: int, char_range: tuple[int, int]) -> bool:
    start, end = char_range
    return start <= code_point <= end


# ============================================================================
# Transition table — built as Python lists, accessed from C inner loop
# ============================================================================

# Action/State int constants for C-level dispatch
ACT_PRINT = Action.PRINT.value
ACT_EXECUTE = Action.EXECUTE.value
ACT_CLEAR = Action.CLEAR.value
ACT_IGNORE = Action.IGNORE.value
ACT_COLLECT = Action.COLLECT.value
ACT_PARAM = Action.PARAM.value
ACT_CSI_DISPATCH = Action.CSI_DISPATCH.value
ACT_ESC_DISPATCH = Action.ESC_DISPATCH.value
ACT_CHARSET_DISPATCH = Action.CHARSET_DISPATCH.value
ACT_OSC_START = Action.OSC_START.value
ACT_OSC_PUT = Action.OSC_PUT.value
ACT_OSC_END = Action.OSC_END.value
ACT_OSC_ABORT = Action.OSC_ABORT.value

ST_GROUND = ParserState.GROUND.value


def _build_lookup():
    """Build the transition lookup table.

    Returns (table, unicode_defaults) where:
    - table[state_int] = list of (action_int, next_state_int) for slots 0x00-0x9F
    - unicode_defaults[state_int] = (action_int, next_state_int) for slots >= 0xA0
    """
    def _rule(s, e, a, ns):
        return (s, e, a.value, ns.value)

    def _exec_rules(st):
        return [_rule(*s, Action.EXECUTE, st) for s in C0_EXECUTABLE_RANGES]

    def _ignore_c0(st):
        return [_rule(*s, Action.IGNORE, st) for s in C0_EXECUTABLE_RANGES]

    _TABLE = {}
    _TABLE[ParserState.GROUND] = [
        _rule(*ASCII_PRINTABLE, Action.PRINT, ParserState.GROUND),
        _rule(*UNICODE_PRINTABLE, Action.PRINT, ParserState.GROUND),
        _rule(*ESC_CHARACTER, Action.CLEAR, ParserState.ESCAPE),
        _rule(*DEL_CHARACTER, Action.IGNORE, ParserState.GROUND),
    ] + _exec_rules(ParserState.GROUND)

    # Charset designators override the generic ESCAPE_INTERMEDIATE range rule,
    # so they must come last in per-state rules (table building: later wins).
    charset_esc = [_rule(c, c, Action.COLLECT, ParserState.CHARSET) for c in CHARSET_DESIGNATORS]
    _TABLE[ParserState.ESCAPE] = [
        _rule(*INTERMEDIATE_CHARACTERS, Action.COLLECT, ParserState.ESCAPE_INTERMEDIATE),
        _rule(0x30, 0x4F, Action.ESC_DISPATCH, ParserState.GROUND),
        _rule(0x51, 0x57, Action.ESC_DISPATCH, ParserState.GROUND),
        _rule(0x59, 0x5A, Action.ESC_DISPATCH, ParserState.GROUND),
        _rule(0x5C, 0x5C, Action.ESC_DISPATCH, ParserState.GROUND),
        _rule(0x60, 0x7E, Action.ESC_DISPATCH, ParserState.GROUND),
        _rule(0x5B, 0x5B, Action.CLEAR, ParserState.CSI_ENTRY),
        _rule(0x5D, 0x5D, Action.OSC_START, ParserState.OSC_STRING),
        _rule(0x50, 0x50, Action.CLEAR, ParserState.DCS_ENTRY),
        _rule(0x58, 0x58, Action.IGNORE, ParserState.SOS_PM_STRING),
        _rule(0x5E, 0x5E, Action.IGNORE, ParserState.SOS_PM_STRING),
        _rule(0x5F, 0x5F, Action.CLEAR, ParserState.APC_ENTRY),
        _rule(*DEL_CHARACTER, Action.IGNORE, ParserState.ESCAPE),
    ] + _exec_rules(ParserState.ESCAPE) + charset_esc

    _TABLE[ParserState.ESCAPE_INTERMEDIATE] = [
        _rule(*INTERMEDIATE_CHARACTERS, Action.COLLECT, ParserState.ESCAPE_INTERMEDIATE),
        _rule(*ESC_FINAL_CHARACTERS, Action.ESC_DISPATCH, ParserState.GROUND),
        _rule(*DEL_CHARACTER, Action.IGNORE, ParserState.ESCAPE_INTERMEDIATE),
    ] + _exec_rules(ParserState.ESCAPE_INTERMEDIATE)

    _TABLE[ParserState.CHARSET] = [
        _rule(*INTERMEDIATE_CHARACTERS, Action.COLLECT, ParserState.CHARSET),
        _rule(*ESC_FINAL_CHARACTERS, Action.CHARSET_DISPATCH, ParserState.GROUND),
        _rule(*DEL_CHARACTER, Action.IGNORE, ParserState.CHARSET),
    ] + _exec_rules(ParserState.CHARSET)

    _TABLE[ParserState.CSI_ENTRY] = [
        _rule(*CSI_FINAL_CHARACTERS, Action.CSI_DISPATCH, ParserState.GROUND),
        _rule(*CSI_PARAMETER_DATA_CHARACTERS, Action.PARAM, ParserState.CSI_PARAM),
        _rule(*CSI_PRIVATE_PREFIX_CHARACTERS, Action.COLLECT, ParserState.CSI_PARAM),
        _rule(*INTERMEDIATE_CHARACTERS, Action.COLLECT, ParserState.CSI_INTERMEDIATE),
        _rule(*DEL_CHARACTER, Action.IGNORE, ParserState.CSI_ENTRY),
    ] + _exec_rules(ParserState.CSI_ENTRY)

    _TABLE[ParserState.CSI_PARAM] = [
        _rule(*CSI_FINAL_CHARACTERS, Action.CSI_DISPATCH, ParserState.GROUND),
        _rule(*CSI_PARAMETER_DATA_CHARACTERS, Action.PARAM, ParserState.CSI_PARAM),
        _rule(*CSI_PRIVATE_PREFIX_CHARACTERS, Action.IGNORE, ParserState.CSI_IGNORE),
        _rule(*INTERMEDIATE_CHARACTERS, Action.COLLECT, ParserState.CSI_INTERMEDIATE),
        _rule(*DEL_CHARACTER, Action.IGNORE, ParserState.CSI_PARAM),
    ] + _exec_rules(ParserState.CSI_PARAM)

    _TABLE[ParserState.CSI_INTERMEDIATE] = [
        _rule(*INTERMEDIATE_CHARACTERS, Action.COLLECT, ParserState.CSI_INTERMEDIATE),
        _rule(*CSI_PARAMETER_CHARACTERS, Action.IGNORE, ParserState.CSI_IGNORE),
        _rule(*CSI_FINAL_CHARACTERS, Action.CSI_DISPATCH, ParserState.GROUND),
    ]

    _TABLE[ParserState.CSI_IGNORE] = [
        _rule(*CSI_PREFINAL_CHARACTERS, Action.IGNORE, ParserState.CSI_IGNORE),
        _rule(*CSI_FINAL_CHARACTERS, Action.IGNORE, ParserState.GROUND),
        _rule(*DEL_CHARACTER, Action.IGNORE, ParserState.CSI_IGNORE),
    ]

    # OSC: BEL terminates (OSC_END), but C0 range includes it. Put BEL last so
    # per-state rule wins over the generic C0 ignore in table building.
    _TABLE[ParserState.OSC_STRING] = [
        _rule(*C1_ST, Action.OSC_END, ParserState.GROUND),
        _rule(*ESC_CHARACTER, Action.OSC_END, ParserState.ESCAPE),
        _rule(*CAN_CHARACTER, Action.OSC_ABORT, ParserState.GROUND),
        _rule(*SUB_CHARACTER, Action.OSC_ABORT, ParserState.GROUND),
        _rule(*ASCII_PRINTABLE, Action.OSC_PUT, ParserState.OSC_STRING),
        _rule(*DEL_CHARACTER, Action.OSC_PUT, ParserState.OSC_STRING),
        _rule(*UNICODE_PRINTABLE, Action.OSC_PUT, ParserState.OSC_STRING),
    ] + _ignore_c0(ParserState.OSC_STRING) + [
        # BEL overrides the C0 ignore range above (BEL is in 0x00-0x17).
        _rule(*BEL_CHARACTER, Action.OSC_END, ParserState.GROUND),
    ]

    _TABLE[ParserState.DCS_ENTRY] = [
        _rule(*INTERMEDIATE_CHARACTERS, Action.COLLECT, ParserState.DCS_INTERMEDIATE),
        _rule(*CSI_PARAMETER_CHARACTERS, Action.IGNORE, ParserState.DCS_PARAM),
        _rule(*CSI_FINAL_CHARACTERS, Action.IGNORE, ParserState.DCS_IGNORE),
        _rule(*DEL_CHARACTER, Action.IGNORE, ParserState.DCS_ENTRY),
    ] + _ignore_c0(ParserState.DCS_ENTRY)

    _TABLE[ParserState.DCS_PARAM] = [
        _rule(*INTERMEDIATE_CHARACTERS, Action.COLLECT, ParserState.DCS_INTERMEDIATE),
        _rule(*CSI_PARAMETER_CHARACTERS, Action.IGNORE, ParserState.DCS_PARAM),
        _rule(*CSI_FINAL_CHARACTERS, Action.IGNORE, ParserState.DCS_IGNORE),
        _rule(*DEL_CHARACTER, Action.IGNORE, ParserState.DCS_PARAM),
    ] + _ignore_c0(ParserState.DCS_PARAM)

    _TABLE[ParserState.DCS_INTERMEDIATE] = [
        _rule(*INTERMEDIATE_CHARACTERS, Action.COLLECT, ParserState.DCS_INTERMEDIATE),
        _rule(*CSI_PARAMETER_CHARACTERS, Action.IGNORE, ParserState.DCS_IGNORE),
        _rule(*CSI_FINAL_CHARACTERS, Action.IGNORE, ParserState.DCS_IGNORE),
        _rule(*DEL_CHARACTER, Action.IGNORE, ParserState.DCS_INTERMEDIATE),
    ] + _ignore_c0(ParserState.DCS_INTERMEDIATE)

    _TABLE[ParserState.DCS_IGNORE] = [
        _rule(*ASCII_PRINTABLE, Action.IGNORE, ParserState.DCS_IGNORE),
        _rule(*UNICODE_PRINTABLE, Action.IGNORE, ParserState.DCS_IGNORE),
        _rule(*DEL_CHARACTER, Action.IGNORE, ParserState.DCS_IGNORE),
    ] + _ignore_c0(ParserState.DCS_IGNORE)

    _TABLE[ParserState.SOS_PM_STRING] = [
        _rule(*ASCII_PRINTABLE, Action.IGNORE, ParserState.SOS_PM_STRING),
        _rule(*UNICODE_PRINTABLE, Action.IGNORE, ParserState.SOS_PM_STRING),
        _rule(*C1_ST, Action.IGNORE, ParserState.GROUND),
        _rule(*DEL_CHARACTER, Action.IGNORE, ParserState.SOS_PM_STRING),
    ] + _ignore_c0(ParserState.SOS_PM_STRING)

    _TABLE[ParserState.APC_ENTRY] = [
        _rule(*ESC_CHARACTER, Action.IGNORE, ParserState.GROUND),
        _rule(*C1_ST, Action.IGNORE, ParserState.GROUND),
        _rule(*CAN_CHARACTER, Action.IGNORE, ParserState.GROUND),
        _rule(*SUB_CHARACTER, Action.IGNORE, ParserState.GROUND),
        _rule(*ASCII_PRINTABLE, Action.IGNORE, ParserState.APC_ENTRY),
        _rule(*UNICODE_PRINTABLE, Action.IGNORE, ParserState.APC_ENTRY),
        _rule(*DEL_CHARACTER, Action.IGNORE, ParserState.APC_ENTRY),
    ] + _ignore_c0(ParserState.APC_ENTRY)

    _GLOBAL = [
        _rule(*CAN_CHARACTER, Action.EXECUTE, ParserState.GROUND),
        _rule(*SUB_CHARACTER, Action.EXECUTE, ParserState.GROUND),
        _rule(*C1_CAN, Action.EXECUTE, ParserState.GROUND),
        _rule(*C1_SUB, Action.EXECUTE, ParserState.GROUND),
        _rule(*ESC_CHARACTER, Action.CLEAR, ParserState.ESCAPE),
        _rule(*C1_ST, Action.IGNORE, ParserState.GROUND),
        _rule(*C1_CSI, Action.CLEAR, ParserState.CSI_ENTRY),
        _rule(*C1_OSC, Action.OSC_START, ParserState.OSC_STRING),
        _rule(*C1_DCS, Action.CLEAR, ParserState.DCS_ENTRY),
        _rule(*C1_SOS, Action.IGNORE, ParserState.SOS_PM_STRING),
        _rule(*C1_PM, Action.IGNORE, ParserState.SOS_PM_STRING),
        _rule(*C1_APC, Action.CLEAR, ParserState.APC_ENTRY),
    ] + [_rule(*s, Action.EXECUTE, ParserState.GROUND) for s in C1_EXECUTE_RANGES]

    # Compile into flat arrays: table[state][slot] = (action, next_state)
    table = []
    unicode_defaults = []
    default_action = ACT_IGNORE
    default_next = ParserState.GROUND.value

    for state in ParserState:
        row = [(default_action, default_next)] * 0xA0
        u_action = default_action
        u_next = default_next

        # Pass 1: globals set the baseline for all states.
        for rule in _GLOBAL:
            lo_r, hi_r, act, ns = rule
            lo = max(lo_r, 0)
            hi = min(hi_r, 0x9F)
            for cp in range(lo, hi + 1):
                row[cp] = (act, ns)
            if hi_r >= 0xA0:
                u_action = act
                u_next = ns

        # Pass 2: per-state rules override globals (per-state wins).
        for rule in _TABLE[state]:
            lo_r, hi_r, act, ns = rule
            lo = max(lo_r, 0)
            hi = min(hi_r, 0x9F)
            for cp in range(lo, hi + 1):
                row[cp] = (act, ns)
            if hi_r >= 0xA0:
                u_action = act
                u_next = ns

        table.append(row)
        unicode_defaults.append((u_action, u_next))

    return table, unicode_defaults


# Build at import time
_LOOKUP, _UNICODE_DEFAULTS = _build_lookup()


# ============================================================================
# The Parser
# ============================================================================

class Parser:
    """Stream parser: feed code points (or UTF-8 bytes), observe dispatcher
    calls. The dispatcher protocol (pyqtermx/dispatcher.py) is the pre-agreed
    test seam (tests/recorder.py)."""

    def __init__(self, dispatcher: Dispatcher) -> None:
        self._dispatcher = dispatcher
        self._state = ParserState.GROUND
        self._print_buffer: list[str] = []
        self._params = ParamsBuilder()
        self._intermediates = ""
        self._prefix = ""
        self._osc_buffer: list[str] = []
        self._decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")

    def feed(self, text: str) -> None:
        """Parse a run of code points, dispatching as it goes.

        Hot path: in GROUND, ASCII and Unicode printables are appended to
        the print buffer directly — no lookup, no dispatch — exactly what
        the table would say (PRINT → stay in GROUND).
        """
        cdef int state = self._state.value
        cdef list buf = self._print_buffer
        cdef list lookup = _LOOKUP
        cdef list unicode_defs = _UNICODE_DEFAULTS
        cdef int cp, action, next_state
        cdef tuple transition

        for ch in text:
            cp = ord(ch)
            # Fast path: GROUND + ASCII printable — no table lookup needed.
            if state == ST_GROUND and cp >= 32 and cp <= 126:
                buf.append(ch)
                continue

            # O(1) lookup
            if cp < 0xA0:
                transition = lookup[state][cp]
            else:
                transition = unicode_defs[state]
            action = transition[0]
            next_state = transition[1]

            # Apply action (calls back into Python)
            self._apply(action, cp)
            state = next_state

        self._state = ParserState(state)

    def feed_bytes(self, data: bytes) -> None:
        """Incrementally UTF-8 decode bytes, then parse them (ADR-0001)."""
        self.feed(self._decoder.decode(data, final=False))

    def flush(self) -> None:
        """Dispatch any pending printable run (the write boundary)."""
        self._flush_print()

    def reset(self) -> None:
        """Return to GROUND and drop all collected state."""
        self._state = ParserState.GROUND
        self._print_buffer.clear()
        self._params.reset()
        self._intermediates = ""
        self._prefix = ""
        self._osc_buffer = []
        self._decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")

    def _apply(self, int action, int cp):
        """Perform the action part of a rule for code point `cp`.

        C switch statement — no Python dict lookup, no if/elif chain.
        """
        if action == ACT_PRINT:
            self._print_buffer.append(chr(cp))
        elif action == ACT_EXECUTE:
            self._flush_print()
            self._dispatcher.execute(cp)
        elif action == ACT_PARAM:
            if 0x30 <= cp <= 0x39:
                self._params.add_digit(cp - 48)
            elif cp == CSI_SUBPARAMETER_SEPARATOR:
                self._params.add_subparam()
            elif cp == CSI_PARAMETER_SEPARATOR:
                self._params.add_param()
        elif action == ACT_COLLECT:
            if 0x3C <= cp <= 0x3F:
                self._prefix = chr(cp)
            else:
                self._intermediates += chr(cp)
        elif action == ACT_CSI_DISPATCH:
            self._dispatcher.csi_dispatch(
                self._intermediates, self._prefix, self._params.build(), chr(cp)
            )
            self._params.reset()
            self._intermediates = ""
            self._prefix = ""
        elif action == ACT_ESC_DISPATCH:
            self._dispatcher.escape_dispatch(self._intermediates, chr(cp))
            self._intermediates = ""
        elif action == ACT_CHARSET_DISPATCH:
            self._dispatcher.designate_charset(self._intermediates, chr(cp))
            self._intermediates = ""
        elif action == ACT_OSC_START:
            self._flush_print()
            self._osc_buffer = []
        elif action == ACT_OSC_PUT:
            self._osc_buffer.append(chr(cp))
        elif action == ACT_OSC_END:
            self._dispatcher.osc_dispatch("".join(self._osc_buffer))
            self._osc_buffer = []
        elif action == ACT_OSC_ABORT:
            self._osc_buffer = []
        elif action == ACT_CLEAR:
            self._flush_print()
            self._params.reset()
            self._intermediates = ""
            self._prefix = ""
        else:  # ACT_IGNORE
            self._flush_print()

    def _flush_print(self) -> None:
        if self._print_buffer:
            self._dispatcher.chars("".join(self._print_buffer))
            self._print_buffer.clear()
