#!/usr/bin/env python3
"""Verify that a project consumes the pinned foundation without local rule forks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


FOUNDATION = Path(__file__).resolve().parent.parent
MANIFEST = FOUNDATION / "consumer_manifest.json"
POINTER_HEADER = "# Shared Foundation Pointer"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="consuming Godot project root")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    dev = root / "dev"
    errors: list[str] = []

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    profile_path = dev / "foundation.profile"
    if not profile_path.is_file():
        errors.append("missing dev/foundation.profile")
        profile = ""
    else:
        profile = profile_path.read_text(encoding="utf-8").strip()
        if profile not in manifest["profiles"]:
            errors.append(f"unknown foundation profile: {profile!r}")
        elif profile != "core" and not (FOUNDATION / "profiles" / profile / "profile_startup.md").is_file():
            errors.append(f"missing profile startup for {profile!r}")

    for relative in manifest["compatibility_pointers"]:
        pointer = dev / relative
        canonical = f"dev/foundation/core/{relative}"
        if not pointer.is_file():
            errors.append(f"missing compatibility pointer: dev/{relative}")
            continue
        text = pointer.read_text(encoding="utf-8")
        if not text.startswith(POINTER_HEADER):
            errors.append(f"local shared-rule fork: dev/{relative}")
        if canonical not in text:
            errors.append(f"wrong canonical target: dev/{relative} -> {canonical}")
        if not (FOUNDATION / "core" / relative).is_file():
            errors.append(f"missing canonical document: {canonical}")

    if errors:
        for error in errors:
            print(f"foundation: ERROR: {error}")
        return 1

    print(f"foundation: OK ({profile}, {len(manifest['compatibility_pointers'])} pointers)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
