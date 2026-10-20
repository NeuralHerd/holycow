#!/usr/bin/env python3
"""Print HolyCow's identity; never probe or configure the host."""

import argparse
import os
from pathlib import Path
import shutil
import sys


ASSETS = Path(__file__).resolve().parent.parent / "assets"
CYAN = (0, 170, 189)
BLUE = (0, 112, 217)
VIOLET = (136, 77, 230)
GOLD = (255, 166, 65)
RESET = "\033[0m"
ANSI16 = (
    (0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0),
    (0, 0, 128), (128, 0, 128), (0, 128, 128), (192, 192, 192),
    (128, 128, 128), (255, 0, 0), (0, 255, 0), (255, 255, 0),
    (0, 0, 255), (255, 0, 255), (0, 255, 255), (255, 255, 255),
)


def color_mode(requested, env, is_tty):
    if requested != "auto":
        return requested
    term = env.get("TERM", "").lower()
    if not is_tty or env.get("NO_COLOR") or term in ("", "dumb"):
        return "never"
    if env.get("COLORTERM", "").lower() in ("truecolor", "24bit") or "direct" in term:
        return "truecolor"
    return "256" if "256color" in term else "16"


def foreground(rgb, mode):
    if mode == "truecolor":
        return "\033[38;2;{};{};{}m".format(*rgb)
    if mode == "256":
        levels = (0, 95, 135, 175, 215, 255)
        r, g, b = [min(range(6), key=lambda i: abs(levels[i] - v)) for v in rgb]
        return "\033[38;5;{}m".format(16 + 36 * r + 6 * g + b)
    if mode == "16":
        index = min(range(16), key=lambda i: sum((a - b) ** 2 for a, b in zip(rgb, ANSI16[i])))
        return "\033[{}m".format(30 + index if index < 8 else 90 + index - 8)
    return ""


def blend(start, end, amount):
    return tuple(round(a + (b - a) * amount) for a, b in zip(start, end))


def paint(line, row, height, columns, mode, halo_rows):
    if mode == "never":
        return line
    output, previous = ["\033[1m"], None
    for column, char in enumerate(line):
        if char != " ":
            if row < halo_rows:
                rgb = GOLD
            else:
                depth = (row - halo_rows) / max(1, height - halo_rows - 1)
                amount = 0.7 * depth + 0.3 * (1 - column / max(1, columns - 1))
                rgb = blend(CYAN, BLUE, amount * 2) if amount < 0.5 else blend(BLUE, VIOLET, amount * 2 - 1)
            escape = foreground(rgb, mode)
            if escape != previous:
                output.append(escape)
                previous = escape
        output.append(char)
    return "".join(output) + RESET


def render(width, mode):
    cow = (ASSETS / "cyber-cow.txt").read_text(encoding="ascii").splitlines()
    halo_rows = 3
    if width < max(map(len, cow)):
        cow = (ASSETS / "cyber-cow-compact.txt").read_text(encoding="ascii").splitlines()
        halo_rows = 2
    if width < max(map(len, cow)):
        for label in ("HOLYCOW / INIT", "HOLYCOW", "HC"):
            if len(label) <= width:
                return label + "\n"
        return "H\n"

    columns = max(map(len, cow))
    artwork = [paint(line, i, len(cow), columns, mode, halo_rows) for i, line in enumerate(cow)]
    message = [
        "HOLYCOW / INIT",
        "by NeuralHerd",
        "",
        "Let's get this repo",
        "ready for the herd.",
    ]
    inner = max(map(len, message)) + 2
    box = ["+" + "-" * inner + "+"]
    box += ["| " + line.ljust(inner - 2) + " |" for line in message]
    box += ["+" + "-" * inner + "+"]
    if mode != "never":
        box[1] = foreground(BLUE, mode) + box[1] + RESET

    if width >= columns + 4 + inner + 2:
        for i, line in enumerate(box, start=5):
            if i < len(artwork):
                artwork[i] += " " * (columns - len(cow[i]) + 4) + line
    else:
        artwork += ["", "HOLYCOW / INIT", "by NeuralHerd"]
    return "\n".join(artwork) + "\n"


def positive_width(value):
    width = int(value)
    if width < 1:
        raise argparse.ArgumentTypeError("width must be positive")
    return width


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--color", choices=("auto", "truecolor", "256", "16", "never"), default="auto")
    parser.add_argument("--width", type=positive_width, help="override the detected terminal column count")
    parser.add_argument("--quiet", action="store_true", help="suppress the banner")
    args = parser.parse_args()
    if args.quiet:
        return
    width = args.width if args.width is not None else shutil.get_terminal_size(fallback=(80, 24)).columns
    mode = color_mode(args.color, os.environ, sys.stdout.isatty())
    sys.stdout.write(render(max(1, width), mode))


if __name__ == "__main__":
    main()
