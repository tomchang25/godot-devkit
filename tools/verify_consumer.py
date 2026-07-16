#!/usr/bin/env python3
"""Verify selected foundation layers and required project-local operation contracts."""

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
) -> tuple[str, str | None]:
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
        resolved_platform = None
    else:
        platform_entry = platforms[platform]
        resolved_platform = platform

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
    return f"{platform}; {profile_label}", resolved_platform


def verify_consumer_contract(
    *,
    root: Path,
    platform: str,
    manifest: dict[str, Any],
    errors: list[str],
) -> None:
    contract = manifest.get("consumer_contract", {})
    rules = contract.get("required_rules", {}) if isinstance(contract, dict) else {}
    if not isinstance(rules, dict) or not rules:
        errors.append("consumer manifest has no required operation rules")
        return

    for name, rule in rules.items():
        if not isinstance(rule, dict):
            errors.append(f"invalid consumer rule entry: {name!r}")
            continue
        relative = rule.get("path")
        if not isinstance(relative, str):
            errors.append(f"consumer rule path is missing: {name!r}")
            continue
        path = root / relative
        if not path.is_file():
            errors.append(f"missing required consumer rule: {relative}")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as error:
            errors.append(f"cannot read required consumer rule {relative}: {error}")
            continue

        fragments = rule.get("required_fragments", [])
        if not isinstance(fragments, list) or not all(isinstance(item, str) for item in fragments):
            errors.append(f"invalid required fragments for consumer rule: {name!r}")
            continue
        for fragment in fragments:
            if fragment not in text:
                errors.append(f"consumer rule {relative} must reference {fragment!r}")

    platforms = manifest.get("platforms", {})
    platform_entry = platforms.get(platform, {}) if isinstance(platforms, dict) else {}
    forbidden = platform_entry.get("forbidden_consumer_files", []) if isinstance(platform_entry, dict) else []
    if not isinstance(forbidden, list) or not all(isinstance(item, str) for item in forbidden):
        errors.append(f"invalid forbidden consumer files for platform: {platform!r}")
        return
    for relative in forbidden:
        if (root / relative).exists():
            errors.append(f"legacy consumer rule must be removed after consolidation: {relative}")


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    errors: list[str] = []

    manifest = read_json(MANIFEST, errors)
    config_path = root / manifest.get("config_path", "dev/foundation.config.json")
    if config_path.is_file():
        label, platform = resolve_v2(
            config=read_json(config_path, errors),
            manifest=manifest,
            errors=errors,
        )
        if platform is not None:
            verify_consumer_contract(
                root=root,
                platform=platform,
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
