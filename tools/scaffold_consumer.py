#!/usr/bin/env python3
"""Create missing project-local operation contracts from foundation templates."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


FOUNDATION = Path(__file__).resolve().parent.parent
MANIFEST = FOUNDATION / "consumer_manifest.json"
TOKEN = re.compile(r"\{\{([A-Z_]+)\}\}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="consuming project root")
    parser.add_argument(
        "--project-name",
        default=None,
        help="display name used in generated rules; defaults to the root directory name",
    )
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(f"invalid JSON in {path}: {error}") from error
    if not isinstance(value, dict):
        raise RuntimeError(f"expected a JSON object in {path}")
    return value


def resolve_template(rule: dict[str, Any], platform: str) -> Path:
    template = rule.get("template")
    if template is None:
        platform_templates = rule.get("platform_templates", {})
        if not isinstance(platform_templates, dict):
            raise RuntimeError("rule platform_templates must be an object")
        template = platform_templates.get(platform)
    if not isinstance(template, str):
        raise RuntimeError(f"no consumer template for platform {platform!r}")
    path = FOUNDATION / template
    if not path.is_file():
        raise RuntimeError(f"consumer template does not exist: {template}")
    return path


def render_template(path: Path, values: dict[str, str]) -> str:
    text = path.read_text(encoding="utf-8")

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in values:
            raise RuntimeError(f"unknown template token {key!r} in {path}")
        return values[key]

    rendered = TOKEN.sub(replace, text)
    if TOKEN.search(rendered):
        raise RuntimeError(f"unresolved template token in {path}")
    return rendered


def main() -> int:
    args = parse_args()
    root = args.root.resolve()

    try:
        manifest = read_json(MANIFEST)
        config_path = root / manifest.get("config_path", "dev/foundation.config.json")
        if not config_path.is_file():
            raise RuntimeError("missing required dev/foundation.config.json")
        config = read_json(config_path)
        expected_schema = manifest.get("schema_version")
        if config.get("schema_version") != expected_schema:
            raise RuntimeError(
                f"unsupported foundation config schema: {config.get('schema_version')!r}; "
                f"expected {expected_schema!r}"
            )

        platform = config.get("platform")
        platforms = manifest.get("platforms", {})
        if not isinstance(platform, str) or not isinstance(platforms, dict) or platform not in platforms:
            raise RuntimeError(f"unknown foundation platform: {platform!r}")

        profiles = config.get("profiles", [])
        if not isinstance(profiles, list) or not all(isinstance(item, str) for item in profiles):
            raise RuntimeError("foundation config profiles must be an array of strings")
        if len(profiles) != len(set(profiles)):
            raise RuntimeError("foundation config profiles must not contain duplicates")
        profile_manifest = manifest.get("profiles", {})
        if not isinstance(profile_manifest, dict):
            raise RuntimeError("consumer manifest profiles must be an object")
        for profile in profiles:
            entry = profile_manifest.get(profile)
            if not isinstance(entry, dict):
                raise RuntimeError(f"unknown foundation profile: {profile!r}")
            allowed_platforms = entry.get("platforms", [])
            if platform not in allowed_platforms:
                raise RuntimeError(f"profile {profile!r} does not support platform {platform!r}")

        contract = manifest.get("consumer_contract", {})
        rules = contract.get("required_rules", {}) if isinstance(contract, dict) else {}
        if not isinstance(rules, dict) or not rules:
            raise RuntimeError("consumer manifest has no required operation rules")

        project_name = (args.project_name or root.name).strip()
        if not project_name:
            raise RuntimeError("project name must not be empty")
        values = {
            "PROJECT_NAME": project_name,
            "PLATFORM": platform,
            "PROFILES": ", ".join(profiles) if profiles else "no profiles",
        }

        jobs: list[tuple[Path, str]] = []
        for name, rule in rules.items():
            if not isinstance(rule, dict):
                raise RuntimeError(f"consumer rule entry must be an object: {name!r}")
            relative = rule.get("path")
            if not isinstance(relative, str):
                raise RuntimeError(f"consumer rule path is missing: {name!r}")
            template = resolve_template(rule, platform)
            jobs.append((root / relative, render_template(template, values)))
    except RuntimeError as error:
        print(f"consumer-scaffold: ERROR: {error}")
        return 1

    created: list[str] = []
    skipped: list[str] = []
    for destination, content in jobs:
        relative = destination.relative_to(root).as_posix()
        if destination.exists():
            skipped.append(relative)
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")
        created.append(relative)

    for relative in created:
        print(f"consumer-scaffold: created {relative}")
    for relative in skipped:
        print(f"consumer-scaffold: kept existing {relative}")
    print(f"consumer-scaffold: OK ({len(created)} created, {len(skipped)} existing)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
