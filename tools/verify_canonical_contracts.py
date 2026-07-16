#!/usr/bin/env python3
"""Guard canonical governance structure and semantic baselines."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "consumer_manifest.json"

REQUIRED: dict[str, tuple[str, ...]] = {
    "core/agent_rules/foundation_startup.md": (
        "core -> platform -> profiles in declared order -> consuming project",
        "foundation.config.json",
        "governance_structure_standard.md",
        "work_lifecycle.md",
    ),
    "core/agent_rules/lint_before_finish.md": (
        "Documentation-only or tracking-only changes",
        "narrowest relevant behavioral test",
        "Core does not invent an engine",
    ),
    "core/standards/governance_structure_standard.md": (
        "## Core-First Placement",
        "## Platform Placement",
        "README files provide navigation",
        "Every governance rule has exactly one canonical owner",
        "## Classification Checklist",
    ),
    "core/standards/persistence_standard.md": (
        "## Ownership Boundary",
        "## Save Envelope",
        "Hydration reaches a settled success",
        "Storage layout version and game payload schema version remain separate",
    ),
    "core/standards/runtime_ownership.md": (
        "# 1. Primary Test",
        "# 2. Controller",
        "# 4. System",
        "# 5. Store",
        "# 6. Service",
        "## State Lifecycle Addendum",
        "Derived state",
        "Multiple entry points that perform the same transition",
    ),
    "core/workflows/work_lifecycle.md": (
        "## Canonical Flow",
        "## Transition Gates",
        "### Implementation to Verify",
        "## Review Position",
        "## Operational Commands",
        "## Tracking States",
    ),
    "core/workflows/closeout_standard.md": (
        "## Child Closeout",
        "## Flow Closeout",
        "## Superseded Work",
        "## Final Verification and Report",
    ),
    "core/workflows/plan_standard.md": (
        "work_lifecycle.md",
        "## Child Decomposition",
        "standalone implementation spec",
        "sketch",
    ),
    "core/workflows/sketch_standard.md": (
        "work_lifecycle.md",
        "Parent Plan: none (standalone sketch)",
        "Candidate files to inspect",
    ),
    "core/workflows/implementation_spec_standard.md": (
        "work_lifecycle.md",
        "Parent Plan: none (standalone spec)",
        "### 2. Summary",
        "### 3. Requirements (standalone only)",
        "### 7. Execution Outline",
        "Target under 800 words",
    ),
    "core/workflows/review_standard.md": (
        "Read the full current contents",
        "Per-File Review Summary",
        "Stale/Redundant Check",
        "Robustness Check",
        "Standards, Lint, And Tests",
        "user's language",
    ),
    "core/workflows/commands/research-context.md": (
        "current ownership",
        "existing behavioral contracts that must survive",
        "Spec-Time Decisions",
        "Do not produce a file-by-file inventory",
    ),
    "core/workflows/commands/spec-build.md": (
        "consuming project's documentation verification contract",
        "Do not run platform runtime checks",
    ),
    "core/workflows/commands/stage-review.md": (
        "non-mutating staged-file checks",
        "stale names or removed behavior",
        "required per-file review summary",
        "robustness result",
    ),
    "platforms/godot/platform_startup.md": (
        "## Platform Triggers",
        "GDScript",
        "serialized scene",
        "never fork a core workflow",
    ),
    "platforms/web-react/platform_startup.md": (
        "## Platform Triggers",
        "React lifecycle",
        "IndexedDB",
        "The consuming project owns its framework mode",
    ),
    "platforms/web-react/standards/react_component_standard.md": (
        "Rendering is pure",
        "List keys use stable domain or content identity",
        "Strict Mode replay",
        "server components",
    ),
    "platforms/web-react/standards/browser_persistence_standard.md": (
        "Database layout version and save-payload schema version are separate owners",
        "Hydration blocks autosave",
        "Define cross-tab ownership or conflict policy",
    ),
    "platforms/web-react/standards/web_accessibility_standard.md": (
        "Use semantic landmarks",
        "Preserve keyboard reachability",
        "Do not communicate state by color alone",
        "ARIA supplements native semantics",
    ),
    "platforms/web-react/standards/testing_standard.md": (
        "## Layers",
        "Domain tests",
        "Application tests",
        "Component tests",
        "Build smoke",
    ),
    "platforms/web-react/skills/indexeddb-upgrade-transactions.md": (
        "versionchange",
        "upgrade transaction",
        "old payload",
    ),
    "platforms/godot/skills/state_machine_pattern.md": (
        "behaviour-delegation",
        "change_state(to)",
        "request_transition(to)",
        "NEVER call `change_state()` inside `_enter()` or `_exit()`",
        "consumer-local skill addendum",
    ),
    "platforms/godot/standards/gdscript_structure_standard.md": (
        "Testbed variant",
        "explicit exception to the global no-hard-wrap-prose rule",
        "# == Inner classes ==",
        "# 6. Inline Sub-section Comments",
        "# 8. Complete Layout Reference",
        "# 13. Component `setup()` Implementation",
        "# 14. Component `.tscn` Default Content",
    ),
    "platforms/godot/standards/component_scene_standard.md": (
        "start at `(0,0)`",
        "neutral placeholder",
        "reviewers should treat that as a smell",
    ),
    "platforms/godot/standards/scene_node_source_standard.md": (
        "standard `Node references` variable group",
        "%UniqueName",
        "@export",
        "# node-ref: allow",
        "An optional note may follow the tag",
        "containing the word \"timer\"",
    ),
    "platforms/godot/standards/scene_routing_standard.md": (
        "`start_page`",
        "`SceneRegistry.default_route`",
        "`test_runner`",
        "Preset overlays",
    ),
    "platforms/godot/standards/settings_overlay_standard.md": (
        "switching save slots",
        "localization keys",
    ),
    "platforms/godot/standards/debug_standard.md": (
        "Each scene that needs debug shortcuts",
        "DebugPanel",
        "if not Debug.enabled",
    ),
}

FORBIDDEN: dict[str, tuple[str, ...]] = {
    "platforms/godot/skills/state_machine_pattern.md": (
        "EnemyTickRuntime",
        "TickEngine",
        "GridEnemy",
    ),
    "platforms/godot/standards/scene_routing_standard.md": (
        "Tickstrike",
        "go_to_arena",
        "go_to_main_menu",
    ),
}

CORE_WORKFLOW_PLATFORM_TERMS = (
    "Godot",
    "GDScript",
    ".gd`",
    ".tscn",
    "/godot-test",
    "SceneRouter",
    "CLAUDE.md",
)

HAN_TEXT = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")


def load_manifest(errors: list[str]) -> dict[str, Any]:
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"invalid consumer manifest: {error}")
        return {}
    if not isinstance(manifest, dict):
        errors.append("consumer manifest must contain a JSON object")
        return {}
    return manifest


def verify_required(errors: list[str]) -> None:
    for relative, required_fragments in REQUIRED.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing canonical document: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for fragment in required_fragments:
            if fragment not in text:
                errors.append(f"missing contract in {relative}: {fragment!r}")

    for relative, forbidden_fragments in FORBIDDEN.items():
        path = ROOT / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for fragment in forbidden_fragments:
            if fragment in text:
                errors.append(f"project-specific contract leaked into {relative}: {fragment!r}")


def verify_language(errors: list[str]) -> None:
    for layer in ("core", "platforms", "profiles"):
        for path in (ROOT / layer).rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            match = HAN_TEXT.search(text)
            if match:
                relative = path.relative_to(ROOT).as_posix()
                line = text.count("\n", 0, match.start()) + 1
                errors.append(f"shared governance must be English: {relative}:{line}")


def verify_core_workflows(errors: list[str]) -> None:
    for path in (ROOT / "core" / "workflows").rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT).as_posix()
        for term in CORE_WORKFLOW_PLATFORM_TERMS:
            if term in text:
                errors.append(f"platform-specific workflow contract leaked into {relative}: {term!r}")


def verify_pointer_entries(
    *,
    entries: Any,
    expected_prefix: str,
    errors: list[str],
) -> set[str]:
    local_paths: set[str] = set()
    if not isinstance(entries, list):
        errors.append(f"manifest pointers for {expected_prefix} must be an array")
        return local_paths

    for entry in entries:
        if not isinstance(entry, dict):
            errors.append(f"invalid pointer entry for {expected_prefix}: {entry!r}")
            continue
        local = entry.get("local")
        canonical = entry.get("canonical")
        if not isinstance(local, str) or not isinstance(canonical, str):
            errors.append(f"invalid pointer paths for {expected_prefix}: {entry!r}")
            continue
        if local in local_paths:
            errors.append(f"duplicate local pointer in {expected_prefix}: {local}")
        local_paths.add(local)
        if not canonical.startswith(expected_prefix):
            errors.append(f"pointer escapes {expected_prefix}: {local} -> {canonical}")
        if not (ROOT / canonical).is_file():
            errors.append(f"manifest points to missing canonical document: {canonical}")
    return local_paths


def verify_manifest(errors: list[str]) -> None:
    manifest = load_manifest(errors)
    if not manifest:
        return
    if manifest.get("schema_version") != 2:
        errors.append("consumer manifest schema_version must be 2")

    core = manifest.get("core", {})
    if not isinstance(core, dict):
        errors.append("consumer manifest core entry must be an object")
        core = {}
    core_startup = core.get("startup")
    if not isinstance(core_startup, str) or not (ROOT / core_startup).is_file():
        errors.append("consumer manifest core startup is missing")
    core_local = verify_pointer_entries(
        entries=core.get("compatibility_pointers"),
        expected_prefix="core/",
        errors=errors,
    )

    platforms = manifest.get("platforms", {})
    if not isinstance(platforms, dict) or not platforms:
        errors.append("consumer manifest must declare at least one platform")
        platforms = {}
    for platform, entry in platforms.items():
        if not isinstance(entry, dict):
            errors.append(f"platform manifest entry must be an object: {platform!r}")
            continue
        startup = entry.get("startup")
        if not isinstance(startup, str) or not (ROOT / startup).is_file():
            errors.append(f"missing platform startup: {platform!r}")
        local_paths = verify_pointer_entries(
            entries=entry.get("compatibility_pointers"),
            expected_prefix=f"platforms/{platform}/",
            errors=errors,
        )
        declared_canonicals = {
            pointer.get("canonical")
            for pointer in entry.get("compatibility_pointers", [])
            if isinstance(pointer, dict) and isinstance(pointer.get("canonical"), str)
        }
        platform_root = ROOT / "platforms" / platform
        actual_canonicals = {
            path.relative_to(ROOT).as_posix()
            for path in platform_root.rglob("*.md")
            if path.relative_to(platform_root).as_posix() != "platform_startup.md"
        }
        for canonical in sorted(actual_canonicals - declared_canonicals):
            errors.append(f"platform canonical is missing from the manifest: {canonical}")
        for canonical in sorted(declared_canonicals - actual_canonicals):
            errors.append(f"platform manifest entry has no canonical file: {canonical}")
        overlap = core_local.intersection(local_paths)
        for local in sorted(overlap):
            errors.append(f"core and platform pointers compete for dev/{local}")
    profiles = manifest.get("profiles", {})
    if not isinstance(profiles, dict):
        errors.append("consumer manifest profiles entry must be an object")
        profiles = {}
    for profile, entry in profiles.items():
        if not isinstance(entry, dict):
            errors.append(f"profile manifest entry must be an object: {profile!r}")
            continue
        startup = entry.get("startup")
        if not isinstance(startup, str) or not (ROOT / startup).is_file():
            errors.append(f"missing profile startup: {profile!r}")
        allowed = entry.get("platforms")
        if not isinstance(allowed, list) or not allowed:
            errors.append(f"profile must declare supported platforms: {profile!r}")
        else:
            for platform in allowed:
                if platform not in platforms:
                    errors.append(f"profile {profile!r} references unknown platform {platform!r}")

def main() -> int:
    errors: list[str] = []
    verify_required(errors)
    verify_language(errors)
    verify_core_workflows(errors)
    verify_manifest(errors)

    if errors:
        for error in errors:
            print(f"canonical: ERROR: {error}")
        return 1

    print(f"canonical: OK ({len(REQUIRED)} semantic baselines, layered manifest)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
