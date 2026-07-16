#!/usr/bin/env python3
"""Exercise schema-2 consumer configuration with generated temporary consumers."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
VERIFIER = ROOT / "tools" / "verify_consumer.py"


def run_verifier(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VERIFIER), "--root", str(root)],
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

        valid_web = run_verifier(root)
        if valid_web.returncode != 0 or "foundation: OK (web-react; no profiles" not in valid_web.stdout:
            failures.append(f"valid Web React consumer failed:\n{valid_web.stdout}{valid_web.stderr}")

    with tempfile.TemporaryDirectory(prefix="game-devkit-missing-config-") as directory:
        missing_config = run_verifier(Path(directory))
        if missing_config.returncode == 0 or "missing required dev/foundation.config.json" not in missing_config.stdout:
            failures.append("consumer without schema-2 configuration was not rejected")

    if failures:
        for failure in failures:
            print(f"consumer-test: ERROR: {failure}")
        return 1

    print("consumer-test: OK (Godot and Web React schema-2 fixtures plus invalid configuration)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
