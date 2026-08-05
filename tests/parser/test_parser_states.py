"""P0 — parser state machine, ported from xterm.js EscapeSequenceParser.test.ts.

Reference: references/xterm.js/src/common/parser/EscapeSequenceParser.test.ts.
That suite drives the parser one code point at a time from a chosen state and
asserts the resulting state, collected buffers, and dispatcher calls.

pyqterm's table (parser.py Part 4) is a transcription of the same VT500
table, so the reference assertions port 1:1 except where pyqterm
deliberately differs — each divergence is noted inline:

- DCS is parsed but never dispatched at Step 1 (ADR-0002): the final byte
  enters DCS_IGNORE and the payload is discarded — no hook/put/unhook.
- APC has no passthrough: APC_ENTRY ignores everything, and ESC/ST/CAN/SUB
  end it with plain IGNORE (no execute, no escape restart) — so the byte
  after an ESC terminator parses in GROUND, and the '\' of a two-byte ST
  prints as text (xterm.js resumes at ESCAPE and swallows it).
- OSC abort (CAN/SUB) silently discards the payload — pyqterm has no
  success flag to dispatch. OSC_END on an empty buffer dispatches "".
- CSI_INTERMEDIATE and CSI_IGNORE have no C0-execute rules: a C0 control
  falls to the default (IGNORE → GROUND) instead of executing in place.
- ESC \\ dispatches escape_dispatch("", "\\") instead of being swallowed.
- The charset designators ( ) * + route to a dedicated CHARSET state.
"""

from __future__ import annotations

import pytest

from pyqterm.parser import Parser, ParserState
from tests.recorder import Recorder, feed

# xterm.js EXECUTABLES: 0x00–0x17, 0x19, 0x1C–0x1F (CAN/SUB/ESC excluded).
_EXECUTABLES = list(range(0x00, 0x18)) + [0x19] + list(range(0x1C, 0x20))

# C1 controls that execute everywhere (xterm.js global-anywhere set).
_C1_EXECUTE = list(range(0x80, 0x90)) + list(range(0x91, 0x98)) + [0x99, 0x9A]


class Probe(Parser):
    """Parser subclass exposing internals — the pyqterm analogue of
    xterm.js's TestEscapeSequenceParser."""

    def __init__(self) -> None:
        self.recorder = Recorder()
        super().__init__(self.recorder)

    @property
    def state(self) -> ParserState:
        return self._state

    @state.setter
    def state(self, value: ParserState) -> None:
        self._state = value

    @property
    def params_groups(self) -> tuple[tuple[int, ...], ...]:
        return self._params.build().groups

    @property
    def intermediates(self) -> str:
        return self._intermediates

    @property
    def prefix(self) -> str:
        return self._prefix

    @property
    def osc(self) -> str:
        return "".join(self._osc_buffer)

    @property
    def events(self) -> list[tuple[object, ...]]:
        return self.recorder.events


def feed_from(state: ParserState, text: str) -> Probe:
    """Feed `text` to a fresh parser forced into `state` (xterm.js style)."""
    probe = Probe()
    probe.state = state
    probe.feed(text)
    probe.flush()
    return probe


def _dirty(probe: Probe) -> None:
    """Dirty the collection buffers (xterm.js sets params/collect by hand)."""
    probe._params.add_digit(2)
    probe._params.add_param()
    probe._params.add_digit(3)  # groups ((2,), (3,))
    probe._intermediates = "#"
    probe._prefix = "?"


# ---------------------------------------------------------------------------
# Parser init and methods (xterm.js: 'Parser init and methods')
# ---------------------------------------------------------------------------


class TestInitAndReset:
    def test_initial_state(self) -> None:
        probe = Probe()
        assert probe.state is ParserState.GROUND
        assert probe.params_groups == ((0,),)
        assert probe.intermediates == ""
        assert probe.prefix == ""
        assert probe.osc == ""
        assert probe.events == []

    def test_reset_returns_to_initial_state(self) -> None:
        probe = Probe()
        probe.state = ParserState.CSI_PARAM
        probe._osc_buffer = ["#"]
        _dirty(probe)
        probe.reset()
        assert probe.state is ParserState.GROUND
        assert probe.params_groups == ((0,),)
        assert probe.intermediates == ""
        assert probe.prefix == ""
        assert probe.osc == ""
        assert probe.events == []


# ---------------------------------------------------------------------------
# GROUND (xterm.js: 'state GROUND execute action' / 'print action')
# ---------------------------------------------------------------------------


class TestGround:
    def test_c0_executables_execute_and_stay(self) -> None:
        for code in _EXECUTABLES:
            probe = feed_from(ParserState.GROUND, chr(code))
            assert probe.state is ParserState.GROUND
            assert probe.events == [("execute", code)]

    def test_ascii_printables_print(self) -> None:
        for code in range(0x20, 0x7F):  # DEL (0x7F) excluded
            probe = feed_from(ParserState.GROUND, chr(code))
            assert probe.state is ParserState.GROUND
            assert probe.events == [("chars", chr(code))]

    def test_unicode_printables_print(self) -> None:
        probe = feed_from(ParserState.GROUND, "中😀")
        assert probe.events == [("chars", "中😀")]

    def test_del_is_ignored(self) -> None:
        probe = feed_from(ParserState.GROUND, "\x7f")
        assert probe.state is ParserState.GROUND
        assert probe.events == []


# ---------------------------------------------------------------------------
# Global-anywhere rules (xterm.js: 'trans ANYWHERE --> GROUND with actions')
# ---------------------------------------------------------------------------


class TestGlobalAnywhere:
    def test_can_sub_and_c1_executes_return_to_ground(self) -> None:
        # Exceptions: OSC_STRING aborts (no execute), APC_ENTRY ends with
        # plain IGNORE (no execute) — everywhere else CAN/SUB/C1 execute.
        exceptions = {ParserState.OSC_STRING, ParserState.APC_ENTRY}
        for state in ParserState:
            for code in [0x18, 0x1A] + _C1_EXECUTE:
                probe = feed_from(state, chr(code))
                assert probe.state is ParserState.GROUND, (state, hex(code))
                expected = [] if code in (0x18, 0x1A) and state in exceptions else [("execute", code)]
                assert probe.events == expected, (state, hex(code))

    def test_8bit_st_is_swallowed_everywhere(self) -> None:
        for state in ParserState:
            probe = feed_from(state, "\x9c")
            assert probe.state is ParserState.GROUND, state
            if state is not ParserState.OSC_STRING:
                # OSC_STRING ends at ST with an (empty) osc_dispatch — see
                # TestOscStringState.test_empty_osc_dispatches_empty.
                assert probe.events == [], state

    def test_esc_goes_to_escape_and_clears(self) -> None:
        for state in ParserState:
            probe = Probe()
            probe.state = state
            _dirty(probe)
            probe.feed("\x1b")
            probe.flush()
            if state is ParserState.APC_ENTRY:
                # APC ends at ESC with plain IGNORE: no escape is restarted.
                assert probe.state is ParserState.GROUND
            else:
                assert probe.state is ParserState.ESCAPE
            if state not in (ParserState.OSC_STRING, ParserState.APC_ENTRY):
                # The CLEAR action drops collected state (OSC_END does not).
                assert probe.params_groups == ((0,),)
                assert probe.intermediates == ""
                assert probe.prefix == ""

    @pytest.mark.parametrize(
        "code, expected",
        [
            (0x9B, ParserState.CSI_ENTRY),
            (0x90, ParserState.DCS_ENTRY),
            (0x9F, ParserState.APC_ENTRY),
            (0x9D, ParserState.OSC_STRING),
            (0x98, ParserState.SOS_PM_STRING),
            (0x9E, ParserState.SOS_PM_STRING),
        ],
    )
    def test_8bit_introducers_enter_their_state_everywhere(
        self, code: int, expected: ParserState
    ) -> None:
        for state in ParserState:
            probe = Probe()
            probe.state = state
            _dirty(probe)
            probe.feed(chr(code))
            probe.flush()
            assert probe.state is expected, (state, hex(code))
            if code in (0x9B, 0x90, 0x9F):  # CLEAR action drops collected state
                assert probe.params_groups == ((0,),)
                assert probe.intermediates == ""
                assert probe.prefix == ""


# ---------------------------------------------------------------------------
# ESCAPE (xterm.js: 'state ESCAPE *' + 'trans ESCAPE --> ...')
# ---------------------------------------------------------------------------


class TestEscapeState:
    def test_c0_executables_execute_and_stay(self) -> None:
        for code in _EXECUTABLES:
            probe = feed_from(ParserState.ESCAPE, chr(code))
            assert probe.state is ParserState.ESCAPE
            assert probe.events == [("execute", code)]

    def test_del_is_ignored(self) -> None:
        probe = feed_from(ParserState.ESCAPE, "\x7f")
        assert probe.state is ParserState.ESCAPE
        assert probe.events == []

    def test_finals_dispatch_to_ground(self) -> None:
        # 0x30–0x7E minus the routes claimed by other states: the charset
        # designators ( ) * + → CHARSET, P → DCS, X → SOS, [ → CSI,
        # ] → OSC, ^ → PM, _ → APC.
        claimed = {0x28, 0x29, 0x2A, 0x2B, 0x50, 0x58, 0x5B, 0x5D, 0x5E, 0x5F}
        for code in range(0x30, 0x7F):
            if code in claimed:
                continue
            probe = feed_from(ParserState.ESCAPE, chr(code))
            assert probe.state is ParserState.GROUND, hex(code)
            assert probe.events == [("escape_dispatch", "", chr(code))], hex(code)

    def test_esc_backslash_dispatches(self) -> None:
        # Divergence: xterm.js registers a swallowing handler for ESC \;
        # pyqterm dispatches it as an ordinary escape sequence.
        assert feed("\x1b\\") == [("escape_dispatch", "", "\\")]

    def test_intermediates_collect_to_escape_intermediate(self) -> None:
        for code in list(range(0x20, 0x28)) + list(range(0x2C, 0x30)):
            probe = feed_from(ParserState.ESCAPE, chr(code))
            assert probe.state is ParserState.ESCAPE_INTERMEDIATE
            assert probe.intermediates == chr(code)

    def test_charset_designators_route_to_charset(self) -> None:
        for code in (0x28, 0x29, 0x2A, 0x2B):
            probe = feed_from(ParserState.ESCAPE, chr(code))
            assert probe.state is ParserState.CHARSET
            assert probe.intermediates == chr(code)

    def test_7bit_string_introducers_route_to_their_states(self) -> None:
        assert feed_from(ParserState.ESCAPE, "[").state is ParserState.CSI_ENTRY
        assert feed_from(ParserState.ESCAPE, "]").state is ParserState.OSC_STRING
        assert feed_from(ParserState.ESCAPE, "P").state is ParserState.DCS_ENTRY
        assert feed_from(ParserState.ESCAPE, "X").state is ParserState.SOS_PM_STRING
        assert feed_from(ParserState.ESCAPE, "^").state is ParserState.SOS_PM_STRING
        assert feed_from(ParserState.ESCAPE, "_").state is ParserState.APC_ENTRY


# ---------------------------------------------------------------------------
# ESCAPE_INTERMEDIATE (xterm.js: 'state ESCAPE_INTERMEDIATE *')
# ---------------------------------------------------------------------------


class TestEscapeIntermediateState:
    def test_c0_executables_execute_and_stay(self) -> None:
        for code in _EXECUTABLES:
            probe = feed_from(ParserState.ESCAPE_INTERMEDIATE, chr(code))
            assert probe.state is ParserState.ESCAPE_INTERMEDIATE
            assert probe.events == [("execute", code)]

    def test_del_is_ignored(self) -> None:
        probe = feed_from(ParserState.ESCAPE_INTERMEDIATE, "\x7f")
        assert probe.state is ParserState.ESCAPE_INTERMEDIATE
        assert probe.events == []

    def test_intermediates_collect(self) -> None:
        for code in range(0x20, 0x30):
            probe = feed_from(ParserState.ESCAPE_INTERMEDIATE, chr(code))
            assert probe.state is ParserState.ESCAPE_INTERMEDIATE
            assert probe.intermediates == chr(code)

    def test_finals_dispatch_to_ground(self) -> None:
        for code in range(0x30, 0x7F):
            probe = feed_from(ParserState.ESCAPE_INTERMEDIATE, chr(code))
            assert probe.state is ParserState.GROUND
            assert probe.events == [("escape_dispatch", "", chr(code))]

    def test_full_sequence_with_intermediates(self) -> None:
        assert feed("\x1b#8") == [("escape_dispatch", "#", "8")]


# ---------------------------------------------------------------------------
# CHARSET (pyqterm-specific state; xterm.js folds it into ESCAPE_INTERMEDIATE)
# ---------------------------------------------------------------------------


class TestCharsetState:
    def test_finals_designate_to_ground(self) -> None:
        for code in range(0x30, 0x7F):
            probe = feed_from(ParserState.CHARSET, chr(code))
            assert probe.state is ParserState.GROUND
            assert probe.events == [("designate_charset", "", chr(code))]

    def test_intermediates_collect(self) -> None:
        for code in range(0x20, 0x30):
            probe = feed_from(ParserState.CHARSET, chr(code))
            assert probe.state is ParserState.CHARSET
            assert probe.intermediates == chr(code)

    def test_full_designation_sequence(self) -> None:
        assert feed("\x1b(0") == [("designate_charset", "(", "0")]


# ---------------------------------------------------------------------------
# CSI_ENTRY (xterm.js: 'state CSI_ENTRY *')
# ---------------------------------------------------------------------------


class TestCsiEntryState:
    def test_c0_executables_execute_and_stay(self) -> None:
        for code in _EXECUTABLES:
            probe = feed_from(ParserState.CSI_ENTRY, chr(code))
            assert probe.state is ParserState.CSI_ENTRY
            assert probe.events == [("execute", code)]

    def test_del_is_ignored(self) -> None:
        probe = feed_from(ParserState.CSI_ENTRY, "\x7f")
        assert probe.state is ParserState.CSI_ENTRY
        assert probe.events == []

    def test_finals_dispatch_to_ground(self) -> None:
        for code in range(0x40, 0x7F):
            probe = feed_from(ParserState.CSI_ENTRY, chr(code))
            assert probe.state is ParserState.GROUND
            assert probe.events == [("csi_dispatch", "", "", ((0,),), chr(code))]

    def test_digits_collect_as_param(self) -> None:
        for digit in range(10):
            probe = feed_from(ParserState.CSI_ENTRY, chr(0x30 + digit))
            assert probe.state is ParserState.CSI_PARAM
            assert probe.params_groups == ((digit,),)

    def test_semicolon_starts_second_param(self) -> None:
        probe = feed_from(ParserState.CSI_ENTRY, ";")
        assert probe.state is ParserState.CSI_PARAM
        assert probe.params_groups == ((0,), (0,))

    def test_colon_starts_subparam(self) -> None:
        probe = feed_from(ParserState.CSI_ENTRY, ":")
        assert probe.state is ParserState.CSI_PARAM
        assert probe.params_groups == ((0, -1),)

    def test_private_prefix_collects(self) -> None:
        for code in range(0x3C, 0x40):
            probe = feed_from(ParserState.CSI_ENTRY, chr(code))
            assert probe.state is ParserState.CSI_PARAM
            assert probe.prefix == chr(code)

    def test_intermediates_collect_to_csi_intermediate(self) -> None:
        for code in range(0x20, 0x30):
            probe = feed_from(ParserState.CSI_ENTRY, chr(code))
            assert probe.state is ParserState.CSI_INTERMEDIATE
            assert probe.intermediates == chr(code)


# ---------------------------------------------------------------------------
# CSI_PARAM (xterm.js: 'state CSI_PARAM *')
# ---------------------------------------------------------------------------


class TestCsiParamState:
    def test_c0_executables_execute_and_stay(self) -> None:
        for code in _EXECUTABLES:
            probe = feed_from(ParserState.CSI_PARAM, chr(code))
            assert probe.state is ParserState.CSI_PARAM
            assert probe.events == [("execute", code)]

    def test_del_is_ignored(self) -> None:
        probe = feed_from(ParserState.CSI_PARAM, "\x7f")
        assert probe.state is ParserState.CSI_PARAM
        assert probe.events == []

    def test_digits_accumulate(self) -> None:
        probe = feed_from(ParserState.CSI_PARAM, "12")
        assert probe.state is ParserState.CSI_PARAM
        assert probe.params_groups == ((12,),)

    def test_params_separated_by_semicolons(self) -> None:
        probe = feed_from(ParserState.CSI_PARAM, "1;2")
        assert probe.params_groups == ((1,), (2,))

    def test_finals_dispatch_with_params(self) -> None:
        probe = feed_from(ParserState.CSI_PARAM, "10;20H")
        assert probe.state is ParserState.GROUND
        assert probe.events == [("csi_dispatch", "", "", ((10,), (20,)), "H")]

    def test_second_private_prefix_is_malformed(self) -> None:
        probe = feed_from(ParserState.CSI_PARAM, "?")
        assert probe.state is ParserState.CSI_IGNORE

    def test_malformed_sequence_swallowed_to_final(self) -> None:
        probe = feed_from(ParserState.CSI_PARAM, "?>abcX")
        assert probe.state is ParserState.GROUND
        assert probe.events == [("chars", "bcX")]

    def test_intermediates_after_params_collect(self) -> None:
        probe = feed_from(ParserState.CSI_PARAM, "5 q")
        assert probe.state is ParserState.GROUND
        assert probe.events == [("csi_dispatch", " ", "", ((5,),), "q")]


# ---------------------------------------------------------------------------
# CSI_INTERMEDIATE (xterm.js: 'state CSI_INTERMEDIATE *')
# ---------------------------------------------------------------------------


class TestCsiIntermediateState:
    def test_intermediates_collect(self) -> None:
        for code in range(0x20, 0x30):
            probe = feed_from(ParserState.CSI_INTERMEDIATE, chr(code))
            assert probe.state is ParserState.CSI_INTERMEDIATE
            assert probe.intermediates == chr(code)

    def test_finals_dispatch_with_intermediates(self) -> None:
        probe = feed_from(ParserState.CSI_INTERMEDIATE, " q")
        assert probe.state is ParserState.GROUND
        assert probe.events == [("csi_dispatch", " ", "", ((0,),), "q")]

    def test_param_after_intermediate_is_malformed(self) -> None:
        probe = feed_from(ParserState.CSI_INTERMEDIATE, "1")
        assert probe.state is ParserState.CSI_IGNORE

    def test_del_falls_to_default(self) -> None:
        # Divergence: xterm.js ignores DEL and stays in CSI_INTERMEDIATE;
        # pyqterm's table has no DEL rule here → default (IGNORE → GROUND).
        probe = feed_from(ParserState.CSI_INTERMEDIATE, "\x7f")
        assert probe.state is ParserState.GROUND
        assert probe.events == []

    def test_c0_falls_to_default(self) -> None:
        # Divergence: xterm.js executes C0 here and stays; pyqterm's table
        # has no C0 rules in CSI_INTERMEDIATE → default (IGNORE → GROUND).
        for code in _EXECUTABLES:
            probe = feed_from(ParserState.CSI_INTERMEDIATE, chr(code))
            assert probe.state is ParserState.GROUND
            assert probe.events == []


# ---------------------------------------------------------------------------
# CSI_IGNORE (xterm.js: 'state CSI_IGNORE *')
# ---------------------------------------------------------------------------


class TestCsiIgnoreState:
    def test_prefinal_bytes_swallowed(self) -> None:
        for code in range(0x20, 0x40):
            probe = feed_from(ParserState.CSI_IGNORE, chr(code))
            assert probe.state is ParserState.CSI_IGNORE
            assert probe.events == []

    def test_del_swallowed(self) -> None:
        probe = feed_from(ParserState.CSI_IGNORE, "\x7f")
        assert probe.state is ParserState.CSI_IGNORE
        assert probe.events == []

    def test_final_resyncs_to_ground_without_dispatch(self) -> None:
        for code in range(0x40, 0x7F):
            probe = feed_from(ParserState.CSI_IGNORE, chr(code))
            assert probe.state is ParserState.GROUND
            assert probe.events == []

    def test_c0_falls_to_default(self) -> None:
        # Divergence: same as CSI_INTERMEDIATE — no C0-execute rules.
        for code in _EXECUTABLES:
            probe = feed_from(ParserState.CSI_IGNORE, chr(code))
            assert probe.state is ParserState.GROUND
            assert probe.events == []


# ---------------------------------------------------------------------------
# OSC_STRING (xterm.js: 'state OSC_STRING *')
# ---------------------------------------------------------------------------


class TestOscStringState:
    def test_c0_controls_ignored(self) -> None:
        for code in _EXECUTABLES:
            if code == 0x07:  # BEL terminates the string instead (OSC_END)
                continue
            probe = feed_from(ParserState.OSC_STRING, chr(code))
            assert probe.state is ParserState.OSC_STRING
            assert probe.osc == ""
            assert probe.events == []

    def test_printables_put(self) -> None:
        for code in range(0x20, 0x7F):
            probe = feed_from(ParserState.OSC_STRING, chr(code))
            assert probe.state is ParserState.OSC_STRING
            assert probe.osc == chr(code)

    def test_del_is_payload(self) -> None:
        probe = feed_from(ParserState.OSC_STRING, "\x7f")
        assert probe.state is ParserState.OSC_STRING
        assert probe.osc == "\x7f"

    def test_unicode_is_payload(self) -> None:
        probe = feed_from(ParserState.OSC_STRING, "€")
        assert probe.state is ParserState.OSC_STRING
        assert probe.osc == "€"

    def test_bel_ends_and_dispatches(self) -> None:
        probe = feed_from(ParserState.OSC_STRING, "0;title\x07")
        assert probe.state is ParserState.GROUND
        assert probe.events == [("osc_dispatch", "0;title")]

    def test_8bit_st_ends_and_dispatches(self) -> None:
        probe = feed_from(ParserState.OSC_STRING, "0;title\x9c")
        assert probe.state is ParserState.GROUND
        assert probe.events == [("osc_dispatch", "0;title")]

    def test_esc_ends_and_moves_to_escape(self) -> None:
        probe = feed_from(ParserState.OSC_STRING, "0;title\x1b")
        assert probe.state is ParserState.ESCAPE
        assert probe.events == [("osc_dispatch", "0;title")]

    def test_can_aborts_without_dispatch(self) -> None:
        probe = feed_from(ParserState.OSC_STRING, "0;title\x18")
        assert probe.state is ParserState.GROUND
        assert probe.events == []

    def test_sub_aborts_without_dispatch(self) -> None:
        probe = feed_from(ParserState.OSC_STRING, "0;title\x1a")
        assert probe.state is ParserState.GROUND
        assert probe.events == []

    def test_empty_osc_dispatches_empty(self) -> None:
        # Divergence: xterm.js suppresses the call for an empty payload;
        # pyqterm's OSC_END always dispatches, even with nothing collected.
        assert feed("\x9d\x9c") == [("osc_dispatch", "")]


# ---------------------------------------------------------------------------
# DCS_* (xterm.js: 'state DCS_*'; pyqterm never dispatches DCS — Step 1)
# ---------------------------------------------------------------------------


class TestDcsEntryState:
    def test_c0_controls_ignored(self) -> None:
        for code in _EXECUTABLES:
            probe = feed_from(ParserState.DCS_ENTRY, chr(code))
            assert probe.state is ParserState.DCS_ENTRY
            assert probe.events == []

    def test_del_ignored(self) -> None:
        probe = feed_from(ParserState.DCS_ENTRY, "\x7f")
        assert probe.state is ParserState.DCS_ENTRY
        assert probe.events == []

    def test_digits_go_to_param(self) -> None:
        for digit in range(10):
            probe = feed_from(ParserState.DCS_ENTRY, chr(0x30 + digit))
            assert probe.state is ParserState.DCS_PARAM
            assert probe.events == []

    def test_intermediates_collect_to_dcs_intermediate(self) -> None:
        for code in range(0x20, 0x30):
            probe = feed_from(ParserState.DCS_ENTRY, chr(code))
            assert probe.state is ParserState.DCS_INTERMEDIATE
            assert probe.intermediates == chr(code)

    def test_final_enters_ignore(self) -> None:
        # Divergence: xterm.js hooks DCS here; Step 1 pyqterm swallows it.
        for code in range(0x40, 0x7F):
            probe = feed_from(ParserState.DCS_ENTRY, chr(code))
            assert probe.state is ParserState.DCS_IGNORE
            assert probe.events == []


class TestDcsParamState:
    def test_c0_controls_ignored(self) -> None:
        for code in _EXECUTABLES:
            probe = feed_from(ParserState.DCS_PARAM, chr(code))
            assert probe.state is ParserState.DCS_PARAM
            assert probe.events == []

    def test_del_ignored(self) -> None:
        probe = feed_from(ParserState.DCS_PARAM, "\x7f")
        assert probe.state is ParserState.DCS_PARAM
        assert probe.events == []

    def test_params_swallowed_but_state_advances(self) -> None:
        probe = feed_from(ParserState.DCS_PARAM, "1;2")
        assert probe.state is ParserState.DCS_PARAM
        assert probe.events == []

    def test_private_prefix_stays_in_param(self) -> None:
        # Divergence: xterm.js sends a second prefix byte to DCS_IGNORE;
        # pyqterm's DCS_PARAM treats all 0x30–0x3F identically.
        for code in range(0x3C, 0x40):
            probe = feed_from(ParserState.DCS_PARAM, chr(code))
            assert probe.state is ParserState.DCS_PARAM
            assert probe.events == []

    def test_intermediates_collect_to_dcs_intermediate(self) -> None:
        probe = feed_from(ParserState.DCS_PARAM, " q")
        assert probe.state is ParserState.DCS_IGNORE
        assert probe.intermediates == " "
        assert probe.events == []

    def test_final_enters_ignore(self) -> None:
        probe = feed_from(ParserState.DCS_PARAM, "1;2a")
        assert probe.state is ParserState.DCS_IGNORE
        assert probe.events == []


class TestDcsIntermediateState:
    def test_intermediates_collect(self) -> None:
        for code in range(0x20, 0x30):
            probe = feed_from(ParserState.DCS_INTERMEDIATE, chr(code))
            assert probe.state is ParserState.DCS_INTERMEDIATE
            assert probe.intermediates == chr(code)

    def test_param_after_intermediate_is_malformed(self) -> None:
        probe = feed_from(ParserState.DCS_INTERMEDIATE, "1")
        assert probe.state is ParserState.DCS_IGNORE

    def test_final_enters_ignore(self) -> None:
        probe = feed_from(ParserState.DCS_INTERMEDIATE, "+a")
        assert probe.state is ParserState.DCS_IGNORE
        assert probe.intermediates == "+"
        assert probe.events == []

    def test_del_ignored(self) -> None:
        probe = feed_from(ParserState.DCS_INTERMEDIATE, "\x7f")
        assert probe.state is ParserState.DCS_INTERMEDIATE
        assert probe.events == []


class TestDcsIgnoreState:
    def test_payload_consumed_until_st(self) -> None:
        codes = _EXECUTABLES + list(range(0x20, 0x80)) + [0x7F] + [0x20AC]
        for code in codes:
            probe = feed_from(ParserState.DCS_IGNORE, chr(code))
            assert probe.state is ParserState.DCS_IGNORE, hex(code)
            assert probe.events == [], hex(code)

    def test_8bit_st_returns_to_ground(self) -> None:
        probe = feed_from(ParserState.DCS_IGNORE, "payload\x9c")
        assert probe.state is ParserState.GROUND
        assert probe.events == []


# ---------------------------------------------------------------------------
# SOS / PM (xterm.js: 'state SOS_PM_STRING *')
# ---------------------------------------------------------------------------


class TestSosPmStringState:
    def test_everything_ignored_until_st(self) -> None:
        codes = _EXECUTABLES + list(range(0x20, 0x80)) + [0x7F]
        for code in codes:
            probe = feed_from(ParserState.SOS_PM_STRING, chr(code))
            assert probe.state is ParserState.SOS_PM_STRING, hex(code)
            assert probe.events == [], hex(code)

    def test_8bit_st_returns_to_ground(self) -> None:
        probe = feed_from(ParserState.SOS_PM_STRING, "payload\x9c")
        assert probe.state is ParserState.GROUND
        assert probe.events == []


# ---------------------------------------------------------------------------
# APC_ENTRY (xterm.js: 'state APC_ENTRY *'; pyqterm has no passthrough)
# ---------------------------------------------------------------------------


class TestApcEntryState:
    def test_everything_ignored_until_terminator(self) -> None:
        codes = _EXECUTABLES + list(range(0x20, 0x80)) + [0x7F]
        for code in codes:
            probe = feed_from(ParserState.APC_ENTRY, chr(code))
            assert probe.state is ParserState.APC_ENTRY, hex(code)
            assert probe.events == [], hex(code)

    def test_can_sub_end_without_executing(self) -> None:
        # Divergence: xterm.js's global CAN/SUB executes here; pyqterm ends
        # the string with plain IGNORE (no execute, no restart).
        for code in (0x18, 0x1A):
            probe = feed_from(ParserState.APC_ENTRY, chr(code))
            assert probe.state is ParserState.GROUND
            assert probe.events == []

    def test_esc_ends_without_restart(self) -> None:
        probe = feed_from(ParserState.APC_ENTRY, "\x1b")
        assert probe.state is ParserState.GROUND
        assert probe.events == []

    def test_8bit_st_ends(self) -> None:
        probe = feed_from(ParserState.APC_ENTRY, "payload\x9c")
        assert probe.state is ParserState.GROUND
        assert probe.events == []


# ---------------------------------------------------------------------------
# End-to-end examples (xterm.js: 'escape sequence examples')
# ---------------------------------------------------------------------------


class TestEscapeSequenceExamples:
    def test_csi_with_print_and_execute(self) -> None:
        assert feed("\x1b[<31;5mHello World! öäü€\nabc") == [
            ("csi_dispatch", "", "<", ((31,), (5,)), "m"),
            ("chars", "Hello World! öäü€"),
            ("execute", 10),
            ("chars", "abc"),
        ]

    def test_osc(self) -> None:
        assert feed("\x1b]0;abc123€öäü\x07") == [("osc_dispatch", "0;abc123€öäü")]

    def test_single_dcs_ignored(self) -> None:
        assert feed("\x1bP1;2;3+$aäbc;däe\x9c") == []

    def test_print_plus_dcs_c1_plus_print(self) -> None:
        assert feed("abc\x901;2;3+$abc;de\x9c") == [("chars", "abc")]

    def test_print_plus_pm_c1_plus_print(self) -> None:
        assert feed("abc\x98123tzf\x9cdefg") == [("chars", "abc"), ("chars", "defg")]

    def test_print_plus_osc_c1_plus_print(self) -> None:
        assert feed("abc\x9d123;tzf\x9cdefg") == [
            ("chars", "abc"),
            ("osc_dispatch", "123;tzf"),
            ("chars", "defg"),
        ]

    def test_single_apc_ignored(self) -> None:
        assert feed("\x1b_X3+$aäbc;däe\x9c") == []

    def test_print_plus_apc_c1_plus_print(self) -> None:
        assert feed("abc\x9fAbc;de\x9cxyz") == [("chars", "abc"), ("chars", "xyz")]

    def test_print_plus_apc_c0_plus_print(self) -> None:
        # Divergence: pyqterm ends the APC at ESC with plain IGNORE, leaving
        # the '\' of the two-byte ST to print in GROUND (xterm.js resumes at
        # ESCAPE, where the '\' is swallowed).
        assert feed("abc\x1b_Abc;de\x1b\\xyz") == [("chars", "abc"), ("chars", "\\xyz")]

    def test_error_recovery(self) -> None:
        assert feed("\x1b[1€abcdefg\x9b<;c") == [
            ("chars", "abcdefg"),
            ("csi_dispatch", "", "<", ((0,), (0,)), "c"),
        ]

    def test_7bit_st_after_osc(self) -> None:
        # Divergence: the trailing '\' of the two-byte ST dispatches as a
        # no-op escape sequence instead of being swallowed.
        assert feed("abc\x9d123;tzf\x1b\\defg") == [
            ("chars", "abc"),
            ("osc_dispatch", "123;tzf"),
            ("escape_dispatch", "", "\\"),
            ("chars", "defg"),
        ]

    def test_colon_notation_in_csi_params(self) -> None:
        assert feed("\x1b[<31;5::123:;8mHello World! öäü€\nabc") == [
            ("csi_dispatch", "", "<", ((31,), (5, -1, 123, -1), (8,)), "m"),
            ("chars", "Hello World! öäü€"),
            ("execute", 10),
            ("chars", "abc"),
        ]

    def test_can_aborts_osc_without_dispatch(self) -> None:
        assert feed("\x1b]0;abc123€öäü\x18") == []

    def test_sub_aborts_osc_without_dispatch(self) -> None:
        assert feed("\x1b]0;abc123€öäü\x1a") == []


# ---------------------------------------------------------------------------
# Coverage (xterm.js: 'coverage tests')
# ---------------------------------------------------------------------------


class TestCoverage:
    def test_unicode_in_csi_ignore_falls_to_default(self) -> None:
        # Divergence: xterm.js ignores and stays in CSI_IGNORE; pyqterm's
        # default resyncs to GROUND.
        probe = feed_from(ParserState.CSI_IGNORE, "€")
        assert probe.state is ParserState.GROUND
        assert probe.events == []

    def test_unicode_in_dcs_ignore_is_consumed(self) -> None:
        probe = feed_from(ParserState.DCS_IGNORE, "€öäü")
        assert probe.state is ParserState.DCS_IGNORE
        assert probe.events == []

    def test_unicode_in_escape_falls_to_default(self) -> None:
        probe = feed_from(ParserState.ESCAPE, "€")
        assert probe.state is ParserState.GROUND
        assert probe.events == []

    def test_8bit_st_in_ground_is_swallowed(self) -> None:
        probe = feed_from(ParserState.GROUND, "\x9c")
        assert probe.state is ParserState.GROUND
        assert probe.events == []
