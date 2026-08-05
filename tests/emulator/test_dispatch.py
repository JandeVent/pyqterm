"""Emulator-level dispatch completeness (spec line 96).

Every entry in the CSI dispatch table must resolve to an existing handler
method, and every final this phase claims must have an entry — so a
half-wired sequence can never silently parse-and-ignore. The escape table
(`_ESC_DISPATCH`) is asserted the same way; the C0 execute set is probed
via the source, since `execute` handles a fixed handful of byte codes.
"""

from pyqtermx.emulator import Emulator
from pyqtermx.screen import Screen

#: The finals this phase claims, keyed by their family (spec line 9:
#: "~30 finals plus escapes").
CSI_FINALS = {
    "h": "SM — set ANSI modes",
    "l": "RM — reset ANSI modes",
    "r": "DECSTBM — set scroll region",
    "m": "SGR — graphic rendition",
    "A": "CUU — cursor up",
    "B": "CUD — cursor down",
    "C": "CUF — cursor forward",
    "D": "CUB — cursor backward",
    "E": "CNL — cursor next line",
    "F": "CPL — cursor preceding line",
    "H": "CUP — cursor position",
    "f": "HVP — horizontal/vertical position",
    "G": "CHA — cursor horizontal absolute",
    "d": "VPA — cursor vertical absolute",
    "J": "ED — erase in display",
    "K": "EL — erase in line",
    "X": "ECH — erase characters",
    "@": "ICH — insert characters",
    "L": "IL — insert lines",
    "M": "DL — delete lines",
    "P": "DCH — delete characters",
    "S": "SU — scroll up",
    "T": "SD — scroll down",
    "g": "TBC — tab clear",
    "I": "CHT — cursor forward tabulation",
    "Z": "CBT — cursor backward tabulation",
    "s": "CSI s — save cursor (DECSC alias)",
    "u": "CSI u — restore cursor (DECRC alias)",
}

#: The finals this phase claims on the escape path (spec line 89).
#: Intermediate-bearing entries — DECALN `ESC # 8` — can't be
#: expressed as bare finals; they are pinned by
#: `test_escape_lookup_is_exact_no_bare_final_fallback` instead.
ESCAPE_FINALS = {
    "D": "IND — index",
    "E": "NEL — next line",
    "M": "RI — reverse index",
    "n": "LS2 — shift to G2",
    "o": "LS3 — shift to G3",
    "~": "LS1R — shift G1",
    "}": "LS2R — shift G2",
    "|": "LS3R — shift G3",
    "H": "HTS — set tab stop",
    "7": "DECSC — save cursor",
    "8": "DECRC — restore cursor",
}

#: C0 codes this phase claims on the execute path (spec line 89).
EXECUTE_CODES = {
    0x0E: "SO — shift to G1",
    0x0F: "SI — shift to G0",
}


def test_every_dispatch_entry_resolves_to_a_handler() -> None:
    for key, name in Emulator._CSI_DISPATCH.items():
        assert callable(getattr(Emulator, name, None)), (
            f"dispatch {key} points at missing handler {name!r}"
        )


def test_every_claimed_csi_final_is_dispatched() -> None:
    for final, label in CSI_FINALS.items():
        assert any(key[2] == final for key in Emulator._CSI_DISPATCH), (
            f"no dispatch entry for {final} ({label})"
        )


def test_every_escape_entry_resolves_to_a_handler() -> None:
    for key, name in Emulator._ESC_DISPATCH.items():
        assert callable(getattr(Emulator, name, None)), (
            f"escape dispatch {key} points at missing handler {name!r}"
        )


def test_every_claimed_escape_final_is_dispatched() -> None:
    for final, label in ESCAPE_FINALS.items():
        assert any(key[1] == final for key in Emulator._ESC_DISPATCH), (
            f"no dispatch entry for ESC {final} ({label})"
        )


def test_escape_lookup_is_exact_no_bare_final_fallback() -> None:
    # Intermediate-bearing escapes dispatch exactly (ESC # 8 DECALN,
    # Phase 3) — they never fall back to the bare final (ESC 8 would
    # restore the cursor state).
    emulator = Emulator(Screen())
    assert emulator._lookup_esc("#", "8") == "_decaln"
    assert emulator._lookup_esc("", "8") == "_decrc"
    assert emulator._lookup_esc("", "D") == "_ind"


def test_every_claimed_execute_code_is_dispatched() -> None:
    import inspect

    source = inspect.getsource(Emulator.execute)
    for code, label in EXECUTE_CODES.items():
        assert f"0x{code:02X}" in source, (
            f"execute has no branch for 0x{code:02X} ({label})"
        )


def test_csi_final_mapping_uses_bare_final_fallback() -> None:
    # an entry with intermediates must not shadow the bare-final entry
    for key in Emulator._CSI_DISPATCH:
        if key[1]:
            assert (key[0], "", key[2]) in Emulator._CSI_DISPATCH, (
                f"{key} has no bare-final fallback"
            )
