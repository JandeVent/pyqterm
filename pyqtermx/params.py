# -*- coding: utf-8 -*-
# Copyright (C) 2018-2026 Connet Information Technology Company, Shanghai.
"""Typed CSI parameters, shaped like xterm.js's ``Params``.

Parsing only, never interpretation: values are stored as integers (empty
parameters and sub-parameters are recorded as 0 and -1 respectively, per
xterm.js's zero-default-mode convention); which value a handler treats as
"default" is a dispatch-time decision.
"""

from __future__ import annotations

from dataclasses import dataclass

#: Digit accumulation caps out here (xterm.js Constants.MAX_VALUE).
MAX_VALUE = 0xFFFFFFFF
#: Maximum storable parameters and sub-parameters (xterm.js defaults).
MAX_PARAMS = 32
MAX_SUBPARAMS = 32


@dataclass(frozen=True)
class Params:
    """Immutable CSI parameters: one tuple per `;`-separated parameter.

    Each group is ``(main_value, sub1, sub2, ...)`` — sub-parameters follow
    the main value; an empty sub-parameter is stored as -1. Parsing only:
    no defaults are applied here.
    """

    groups: tuple[tuple[int, ...], ...]

    def count(self) -> int:
        return len(self.groups)

    def get(self, index: int) -> int:
        """Main value at `index`, or 0 when absent (zero-default-mode)."""
        if index < len(self.groups):
            return self.groups[index][0]
        return 0

    def subparams(self, index: int) -> tuple[int, ...]:
        """Sub-parameters of the parameter at `index`, or () when none."""
        if index < len(self.groups):
            return self.groups[index][1:]
        return ()


class ParamsBuilder:
    """Mutable accumulation target for the parser; :meth:`build` freezes it."""

    def __init__(self) -> None:
        self._groups: list[list[int]] = [[0]]  # zero-default-mode (xterm.js)
        self._digit_is_sub = False
        self._reject = False
        self._sub_count = 0

    def add_digit(self, digit: int) -> None:
        if self._reject:
            return
        group = self._groups[-1]
        if self._digit_is_sub:
            current = group[-1]
            group[-1] = digit if current == -1 else min(current * 10 + digit, MAX_VALUE)
        else:
            current = group[0]
            group[0] = min(current * 10 + digit, MAX_VALUE)

    def add_param(self) -> None:
        """`;`: start a new parameter group."""
        self._digit_is_sub = False
        if len(self._groups) >= MAX_PARAMS:
            self._reject = True
            return
        self._groups.append([0])

    def add_subparam(self) -> None:
        """`:`: start a new sub-parameter on the current group."""
        self._digit_is_sub = True
        if self._reject or self._sub_count >= MAX_SUBPARAMS:
            self._reject = True
            return
        self._sub_count += 1
        self._groups[-1].append(-1)

    def build(self) -> Params:
        return Params(tuple(tuple(group) for group in self._groups))

    def reset(self) -> None:
        self._groups = [[0]]
        self._digit_is_sub = False
        self._reject = False
        self._sub_count = 0
