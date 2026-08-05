# -*- coding: utf-8 -*-
# Copyright (C) 2018-2026 Connet Information Technology Company, Shanghai.
"""Shared test seam: a recorder handler implementing the dispatcher protocol."""

from __future__ import annotations

from pyqtermx.dispatcher import Dispatcher
from pyqtermx.params import Params
from pyqtermx.parser import Parser


class Recorder(Dispatcher):
    """Records every dispatcher call as an (event, *payload) tuple."""

    def __init__(self) -> None:
        self.events: list[tuple[object, ...]] = []

    def chars(self, text: str) -> None:
        self.events.append(("chars", text))

    def execute(self, code: int) -> None:
        self.events.append(("execute", code))

    def csi_dispatch(
        self, intermediates: str, prefix: str, params: Params, final: str
    ) -> None:
        # Params is asserted by its groups for readability.
        self.events.append(("csi_dispatch", intermediates, prefix, params.groups, final))

    def escape_dispatch(self, intermediates: str, final: str) -> None:
        self.events.append(("escape_dispatch", intermediates, final))

    def designate_charset(self, designator: str, charset: str) -> None:
        self.events.append(("designate_charset", designator, charset))

    def osc_dispatch(self, payload: str) -> None:
        self.events.append(("osc_dispatch", payload))


def feed(text: str) -> list[tuple[object, ...]]:
    """Feed text to a fresh parser and return the full recorded event sequence."""
    recorder = Recorder()
    parser = Parser(recorder)
    parser.feed(text)
    parser.flush()
    return recorder.events


def feed_bytes(data: bytes) -> list[tuple[object, ...]]:
    recorder = Recorder()
    parser = Parser(recorder)
    parser.feed_bytes(data)
    parser.flush()
    return recorder.events
