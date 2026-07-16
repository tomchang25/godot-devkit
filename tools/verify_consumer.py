#!/usr/bin/env python3
"""Verify that a project selects supported layers from its pinned foundation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


FOUNDATION = Path(__file__).resolve().parent.parent
MANIFEST = FOUNDATION / "consumer_manifest.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="consuming game project root")
    return parser.parse_args()


def read_json(path: Path, errors: list[str]) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"invalid JSON in {path}: {error}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"expected a JSON object in {path}")
        return {}
    return value


def resolve_v2(
    *,
    config: dict[str, Any],
    manifest: dict[str, Any],
    errors: list[str],
) -> str:
    expected_schema = manifest.get("schema_version")
    if config.get("schema_version") != expected_schema:
        errors.append(
            f"unsupported foundation config schema: {config.get('schema_version')!r}; expected {expected_schema!r}"
        )

    core = manifest.get("core", {})
    core_startup = core.get("startup") if isinstance(core, dict) else None
    if not isinstance(core_startup, str) or not (FOUNDATION / core_startup).is_file():
        errors.append("missing foundation core startup")

    platform = config.get("platform")
    platforms = manifest.get("platforms", {})
    if not isinstance(platform, str) or platform not in platforms:
        errors.append(f"unknown foundation platform: {platform!r}")
        platform_entry: dict[str, Any] = {}
    else:
        platform_entry = platforms[platform]

    selected_profiles = config.get("profiles", [])
    if not isinstance(selected_profiles, list) or not all(isinstance(item, str) for item in selected_profiles):
        errors.append("foundation config profiles must be an array of strings")
        selected_profiles = []
    elif len(selected_profiles) != len(set(selected_profiles)):
        errors.append("foundation config profiles must not contain duplicates")

    profile_manifest = manifest.get("profiles", {})
    for profile in selected_profiles:
        entry = profile_manifest.get(profile)
        if not isinstance(entry, dict):
            errors.append(f"unknown foundation profile: {profile!r}")
            continue
        allowed_platforms = entry.get("platforms", [])
        if platform not in allowed_platforms:
            errors.append(f"profile {profile!r} does not support platform {platform!r}")
        startup = entry.get("startup")
        if not isinstance(startup, str) or not (FOUNDATION / startup).is_file():
            errors.append(f"missing profile startup for {profile!r}")

    startup = platform_entry.get("startup")
    if platform_entry and (not isinstance(startup, str) or not (FOUNDATION / startup).is_file()):
        errors.append(f"missing platform startup for {platform!r}")

    profile_label = ", ".join(selected_profiles) if selected_profiles else "no profiles"
    return f"{platform}; {profile_label}"


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    errors: list[str] = []

    manifest = read_json(MANIFEST, errors)
    config_path = root / manifest.get("config_path", "dev/foundation.config.json")
    if config_path.is_file():
        label = resolve_v2(
            config=read_json(config_path, errors),
            manifest=manifest,
            errors=errors,
        )
    else:
        errors.append("missing required dev/foundation.config.json")
        label = "unknown platform"

    if errors:
        for error in errors:
            print(f"foundation: ERROR: {error}")
        return 1

    print(f"foundation: OK ({label})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
