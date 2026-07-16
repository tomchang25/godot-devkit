#!/usr/bin/env python3
"""Exercise schema-2 consumer verification with generated temporary consumers."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = json.loads((ROOT / "consumer_manifest.json").read_text(encoding="utf-8"))
VERIFIER = ROOT / "tools" / "verify_consumer.py"


def write_pointer(dev: Path, entry: dict[str, str]) -> None:
    path = dev / entry["local"]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "# Shared Foundation Pointer\n\n"
        f"Canonical document: `dev/foundation/{entry['canonical']}`.\n",
        encoding="utf-8",
    )


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

    platform = config["platform"]
    entries = [
        *MANIFEST["core"]["compatibility_pointers"],
        *MANIFEST["platforms"][platform]["compatibility_pointers"],
    ]
    for entry in entries:
        write_pointer(dev, entry)


def main() -> int:
    failures: list[str] = []

    with tempfile.TemporaryDirectory(prefix="game-devkit-consumer-") as directory:
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

        pointer = root / "dev" / "workflows" / "work_lifecycle.md"
        pointer.write_text(
            "# Shared Foundation Pointer\n\n"
            "Canonical document: `dev/foundation/core/workflows/wrong.md`.\n",
            encoding="utf-8",
        )
        invalid_pointer = run_verifier(root)
        if invalid_pointer.returncode == 0 or "wrong canonical target" not in invalid_pointer.stdout:
            failures.append("wrong schema-2 canonical target was not rejected")

    if failures:
        for failure in failures:
            print(f"consumer-test: ERROR: {failure}")
        return 1

    print("consumer-test: OK (schema-2 valid and invalid fixtures)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
