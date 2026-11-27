#!/usr/bin/env python3
"""Print the body of one CHANGELOG.md version section, for GitHub release notes.

Usage: python3 scripts/changelog_section.py 0.1.0
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

CHANGELOG = Path(__file__).resolve().parent.parent / "CHANGELOG.md"


def section(version: str, text: str) -> str:
    match = re.search(rf"^## \[{re.escape(version)}\][^\n]*\n(.*?)(?=^## \[|^\[[^\]]+\]: |\Z)", text, re.M | re.S)
    if not match or not match.group(1).strip():
        raise LookupError(f"CHANGELOG.md has no entries for {version}")
    return match.group(1).strip() + "\n"


def main(argv: list) -> int:
    if len(argv) != 1:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    try:
        print(section(argv[0], CHANGELOG.read_text()), end="")
    except LookupError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
