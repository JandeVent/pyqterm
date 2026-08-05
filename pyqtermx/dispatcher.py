"""The dispatcher protocol — the seam between parser and terminal state.

The parser owns parsing; a dispatcher owns semantics. The screen (later) and
the test recorder (now) both implement this protocol, so the parser is
testable without any terminal state existing.

The protocol grows per ticket: ground dispatch (T1), CSI (T2), escape and
charset events (T3), OSC (T4).
"""

from __future__ import annotations

from typing import Protocol

from .params import Params


class Dispatcher(Protocol):
    """Receives every parse result as a method call."""

    def chars(self, text: str) -> None:
        """A run of printable characters."""
        ...

    def execute(self, code: int) -> None:
        """A C0 control character, identified by its code point."""
        ...

    def csi_dispatch(
        self, intermediates: str, prefix: str, params: Params, final: str
    ) -> None:
        """A complete control sequence.

        `intermediates` are the intermediate bytes (0x20–0x2F), `prefix` is
        the private marker (`?`, `>`, `=` or `<`) when present, `params` the
        typed parameters, and `final` the final byte.
        """
        ...

    def escape_dispatch(self, intermediates: str, final: str) -> None:
        """A complete escape sequence: intermediate bytes and final byte."""
        ...

    def designate_charset(self, designator: str, charset: str) -> None:
        """A charset designation (ESC ( / ) / * / + …).

        `designator` is the intermediate identifying the slot (G0–G3) and
        `charset` the final byte naming the charset.
        """
        ...

    def osc_dispatch(self, payload: str) -> None:
        """A complete OSC string, payload delivered intact."""
        ...
