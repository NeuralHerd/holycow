#!/usr/bin/env python3
"""Set the HolyCow version in VERSION and in every skill's metadata.version.

Usage: python3 scripts/set_version.py 0.2.0
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
VERSION_LINE = re.compile(r'^(  version: )"[^"]*"$', re.M)


def set_version(version: str, root: Path = ROOT) -> list:
    if not SEMVER.match(version):
        raise ValueError(f"{version!r} is not MAJOR.MINOR.PATCH")
    changed = []
    for skill in sorted((root / "skills").glob("*/SKILL.md")):
        text = skill.read_text()
        end = text.index("\n---\n", 4)
        front, count = VERSION_LINE.subn(rf'\g<1>"{version}"', text[:end])
        if count != 1:
            raise ValueError(f"{skill.relative_to(root)} needs exactly one metadata.version line")
        skill.write_text(front + text[end:])
        changed.append(skill.relative_to(root).as_posix())
    (root / "VERSION").write_text(version + "\n")
    return changed


def main(argv: list) -> int:
    if len(argv) != 1:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    try:
        changed = set_version(argv[0])
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(f"VERSION and {len(changed)} skills set to {argv[0]}. Add a CHANGELOG.md section for it.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
