#!/usr/bin/env python3
"""Exercise schema-2 configuration, scaffolding, and consumer operation contracts."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
VERIFIER = ROOT / "tools" / "verify_consumer.py"
SCAFFOLD = ROOT / "tools" / "scaffold_consumer.py"


def run_verifier(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VERIFIER), "--root", str(root)],
        check=False,
        capture_output=True,
        text=True,
    )


def run_scaffold(root: Path, project_name: str = "Fixture Project") -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(SCAFFOLD),
            "--root",
            str(root),
            "--project-name",
            project_name,
        ],
        check=False,
        capture_output=True,
        text=True,
    )


def build_consumer(root: Path, config: dict[str, Any]) -> None:
    dev = root / "dev"
    dev.mkdir(parents=True)
    (dev / "foundation.config.json").write_text(
        json.dumps(config, indent=2) + "\n",
        encoding="utf-8",
    )


def require_scaffold(root: Path, failures: list[str], label: str) -> bool:
    result = run_scaffold(root)
    if result.returncode != 0:
        failures.append(f"{label} scaffold failed:\n{result.stdout}{result.stderr}")
        return False
    required = (
        root / "dev" / "agent_rules" / "agent_startup.md",
        root / "dev" / "agent_rules" / "git_operations.md",
        root / "dev" / "agent_rules" / "test_operations.md",
    )
    if not all(path.is_file() for path in required):
        failures.append(f"{label} scaffold did not create all required operation rules")
        return False
    return True


def main() -> int:
    failures: list[str] = []

    with tempfile.TemporaryDirectory(prefix="game-devkit-godot-consumer-") as directory:
        root = Path(directory)
        build_consumer(
            root,
            {
                "schema_version": 2,
                "platform": "godot",
                "profiles": ["action-rpg"],
            },
        )
        if require_scaffold(root, failures, "Godot consumer"):
            valid = run_verifier(root)
            if valid.returncode != 0 or "foundation: OK (godot; action-rpg" not in valid.stdout:
                failures.append(f"valid schema-2 consumer failed:\n{valid.stdout}{valid.stderr}")

    with tempfile.TemporaryDirectory(prefix="game-devkit-web-consumer-") as directory:
        root = Path(directory)
        build_consumer(
            root,
            {
                "schema_version": 2,
                "platform": "web-react",
                "profiles": [],
            },
        )
        if require_scaffold(root, failures, "Web React consumer"):
            valid_web = run_verifier(root)
            if valid_web.returncode != 0 or "foundation: OK (web-react; no profiles" not in valid_web.stdout:
                failures.append(f"valid Web React consumer failed:\n{valid_web.stdout}{valid_web.stderr}")

    with tempfile.TemporaryDirectory(prefix="game-devkit-missing-rules-") as directory:
        root = Path(directory)
        build_consumer(
            root,
            {
                "schema_version": 2,
                "platform": "godot",
                "profiles": [],
            },
        )
        missing_rules = run_verifier(root)
        if missing_rules.returncode == 0 or "missing required consumer rule" not in missing_rules.stdout:
            failures.append("consumer without project-local operation rules was not rejected")

    with tempfile.TemporaryDirectory(prefix="game-devkit-missing-reference-") as directory:
        root = Path(directory)
        build_consumer(
            root,
            {
                "schema_version": 2,
                "platform": "godot",
                "profiles": [],
            },
        )
        if require_scaffold(root, failures, "Missing-reference fixture"):
            startup = root / "dev" / "agent_rules" / "agent_startup.md"
            startup.write_text(
                startup.read_text(encoding="utf-8").replace("test_operations.md", "test_policy.md"),
                encoding="utf-8",
            )
            missing_reference = run_verifier(root)
            if missing_reference.returncode == 0 or "must reference 'test_operations.md'" not in missing_reference.stdout:
                failures.append("consumer startup without the test-operations reference was not rejected")

    with tempfile.TemporaryDirectory(prefix="game-devkit-legacy-test-rules-") as directory:
        root = Path(directory)
        build_consumer(
            root,
            {
                "schema_version": 2,
                "platform": "godot",
                "profiles": [],
            },
        )
        if require_scaffold(root, failures, "Legacy-rule fixture"):
            legacy = root / "dev" / "agent_rules" / "godot_tests.md"
            legacy.write_text("# Legacy test owner\n", encoding="utf-8")
            legacy_rules = run_verifier(root)
            if legacy_rules.returncode == 0 or "legacy consumer rule must be removed" not in legacy_rules.stdout:
                failures.append("consumer with a legacy split test owner was not rejected")

    with tempfile.TemporaryDirectory(prefix="game-devkit-existing-rule-") as directory:
        root = Path(directory)
        build_consumer(
            root,
            {
                "schema_version": 2,
                "platform": "godot",
                "profiles": [],
            },
        )
        startup = root / "dev" / "agent_rules" / "agent_startup.md"
        startup.parent.mkdir(parents=True)
        original = "# Existing startup\n\n`git_operations.md` and `test_operations.md`\n"
        startup.write_text(original, encoding="utf-8")
        existing = run_scaffold(root)
        if existing.returncode != 0 or startup.read_text(encoding="utf-8") != original:
            failures.append("consumer scaffold overwrote an existing project-owned rule")

    with tempfile.TemporaryDirectory(prefix="game-devkit-missing-config-") as directory:
        missing_config = run_verifier(Path(directory))
        if missing_config.returncode == 0 or "missing required dev/foundation.config.json" not in missing_config.stdout:
            failures.append("consumer without schema-2 configuration was not rejected")

    if failures:
        for failure in failures:
            print(f"consumer-test: ERROR: {failure}")
        return 1

    print(
        "consumer-test: OK (scaffolded Godot/Web consumers, required operation rules, "
        "legacy-owner rejection, and invalid configuration)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
