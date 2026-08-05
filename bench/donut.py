#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2018-2026 Connet Information Technology Company, Shanghai.
"""Render a 3D spinning ASCII donut (torus) in the terminal.

A pure-stdlib port of Andy Sloane's classic "donut" animation
(https://www.a1k0n.net/2011/07/20/donut-math/).

Usage:
    python3 donut.py

Quit with Ctrl+C.
"""

from __future__ import annotations

import math
import os
import sys
import time

# Luminance ramp from dark to bright, indexed by the surface normal.
LUMINANCE = ".,-~:;=!*#$@"

# Torus geometry and camera position.
R1 = 1.0  # minor radius (tube radius)
R2 = 2.0  # major radius (torus centre to tube centre)
K2 = 5.0  # distance from camera to torus centre

# Rotation increment per frame.
A_STEP = 0.04  # tilt
B_STEP = 0.02  # spin

# Sampling step for each torus angle (matches the classic look).
THETA_STEP = 0.07  # around the tube
PHI_STEP = 0.02  # around the main circle

FPS = 90.0

# ANSI escape sequences.
_CURSOR_HIDE = "\x1b[?25l"
_CURSOR_SHOW = "\x1b[?25h"
_CLEAR_SCREEN = "\x1b[2J"
_MOVE_HOME = "\x1b[H"


def projection_scale(width: int, height: int) -> float:
    """Perspective scale factor so the donut fits the terminal.

    Terminal cells are roughly twice as tall as they are wide, so the
    limiting dimension is width vs. twice the height. At 80x24 this
    reproduces the classic K1 = 30.
    """
    return min(width, 2 * height) * K2 * 3 / (8 * (R1 + R2))


def render_frame(angle_a: float, angle_b: float, width: int, height: int) -> str:
    """Return one frame of the spinning torus as a plain string.

    The frame is drawn into a character buffer with a per-pixel depth
    buffer so closer surfaces occlude farther ones. Pure function: no
    terminal interaction, same inputs always yield the same output.
    """
    scale = projection_scale(width, height)
    center_x = width // 2
    center_y = height // 2

    pixels = [" "] * (width * height)
    depth = [0.0] * (width * height)

    sin_a, cos_a = math.sin(angle_a), math.cos(angle_a)
    sin_b, cos_b = math.sin(angle_b), math.cos(angle_b)

    theta = 0.0
    while theta < 2 * math.pi:
        sin_theta, cos_theta = math.sin(theta), math.cos(theta)
        radius = R2 + R1 * cos_theta  # point's distance from the torus axis

        phi = 0.0
        while phi < 2 * math.pi:
            sin_phi, cos_phi = math.sin(phi), math.cos(phi)

            # Rotate the torus point by A (tilt) and B (spin).
            x = (
                radius * (cos_b * cos_phi + sin_a * sin_b * sin_phi)
                - R1 * cos_a * sin_b * sin_theta
            )
            y = (
                radius * (sin_b * cos_phi - cos_b * sin_a * sin_phi)
                + R1 * cos_a * cos_b * sin_theta
            )
            z = cos_a * radius * sin_phi + R1 * sin_a * sin_theta

            # Perspective projection: xp/yp from inverse depth (ooz).
            ooz = 1 / (z + K2)
            xp = int(center_x + scale * ooz * x)
            yp = int(center_y - (scale / 2) * ooz * y)

            # Luminance from the surface normal's z-component (dark to bright).
            lum = (
                (sin_theta * sin_a - sin_phi * cos_theta * cos_a) * cos_b
                - sin_phi * cos_theta * sin_a
                - sin_theta * cos_a
                - cos_phi * cos_theta * sin_b
            )

            index = yp * width + xp
            if 0 <= xp < width and 0 <= yp < height and ooz > depth[index]:
                depth[index] = ooz
                pixels[index] = LUMINANCE[max(0, int(lum * 8))]

            phi += PHI_STEP
        theta += THETA_STEP

    lines = []
    for y in range(height):
        start = y * width
        lines.append("".join(pixels[start : start + width]))
    return "\n".join(lines)


def terminal_size(fallback_width: int = 80, fallback_height: int = 24) -> tuple[int, int]:
    """Return the terminal size, falling back to the classic 80x24."""
    try:
        size = os.get_terminal_size()
    except OSError:
        return fallback_width, fallback_height
    return size.columns, size.lines


def animate(width: int | None = None, height: int | None = None) -> None:
    """Spin the torus forever, redrawing each frame in place."""
    if width is None or height is None:
        detected_width, detected_height = terminal_size()
        width = width or detected_width
        height = height or detected_height

    angle_a = 0.0
    angle_b = 0.0
    frame_delay = 1 / FPS

    sys.stdout.write(_CURSOR_HIDE + _CLEAR_SCREEN)
    try:
        while True:
            frame = render_frame(angle_a, angle_b, width, height)
            sys.stdout.write(_MOVE_HOME + frame)
            sys.stdout.flush()
            angle_a += A_STEP
            angle_b += B_STEP
            time.sleep(frame_delay)
    except KeyboardInterrupt:
        pass  # Leave the terminal exactly as we found it.
    finally:
        sys.stdout.write(_CURSOR_SHOW)
        sys.stdout.flush()


def main() -> int:
    animate()
    return 0


if __name__ == "__main__":
    sys.exit(main())
