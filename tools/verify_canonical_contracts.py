#!/usr/bin/env python3
"""Guard canonical governance against accidental semantic regressions."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

REQUIRED: dict[str, tuple[str, ...]] = {
    "core/agent_rules/lint_before_finish.md": (
        "Docs-only or TODO-only changes",
        "narrowest relevant test/check",
    ),
    "core/skills/state_machine_pattern.md": (
        "behaviour-delegation",
        "change_state(to)",
        "request_transition(to)",
        "NEVER call `change_state()` inside `_enter()` or `_exit()`",
        "consumer-local skill addendum",
    ),
    "core/standards/gdscript_structure_standard.md": (
        "Testbed variant",
        "explicit exception to the global no-hard-wrap-prose rule",
        "# == Inner classes ==",
        "# 6. Inline Sub-section Comments",
        "# 8. Complete Layout Reference",
        "# 13. Component `setup()` Implementation",
        "# 14. Component `.tscn` Default Content",
    ),
    "core/standards/component_scene_standard.md": (
        "start at `(0,0)`",
        "neutral placeholder",
        "reviewers should treat that as a smell",
    ),
    "core/standards/scene_node_source_standard.md": (
        "standard `Node references` variable group",
        "%UniqueName",
        "@export",
        "# node-ref: allow",
        "An optional note may follow the tag",
        "containing the word \"timer\"",
    ),
    "core/standards/scene_routing_standard.md": (
        "`start_page`",
        "`SceneRegistry.default_route`",
        "`test_runner`",
        "Preset overlays",
    ),
    "core/standards/runtime_ownership.md": (
        "# 1. Primary Test",
        "# 2. Controller",
        "# 4. System",
        "# 5. Store",
        "# 6. Service",
    ),
    "core/standards/settings_overlay_standard.md": (
        "switching save slots",
        "localization keys",
    ),
    "core/standards/debug_standard.md": (
        "Each scene that needs debug shortcuts",
        "DebugPanel",
        "if not Debug.enabled",
    ),
    "core/workflows/plan_standard.md": (
        "## Child Decomposition",
        "standalone implementation spec",
        "sketch",
    ),
    "core/workflows/implementation_spec_standard.md": (
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
        "Summary` in Traditional Chinese",
    ),
    "core/workflows/commands/research-context.md": (
        "current ownership",
        "existing behavioral contracts that must survive",
        "Spec-Time Decisions",
        "Do not produce a file-by-file inventory",
    ),
    "core/workflows/commands/stage-review.md": (
        "all staged .gd and .tscn files",
        "stale names or removed behavior",
        "required per-file review summary",
        "robustness result",
    ),
}

FORBIDDEN: dict[str, tuple[str, ...]] = {
    "core/skills/state_machine_pattern.md": (
        "EnemyTickRuntime",
        "TickEngine",
        "GridEnemy",
    ),
    "core/standards/scene_routing_standard.md": (
        "Tickstrike",
        "go_to_arena",
        "go_to_main_menu",
    ),
}


def main() -> int:
    errors: list[str] = []

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

    if errors:
        for error in errors:
            print(f"canonical: ERROR: {error}")
        return 1

    print(f"canonical: OK ({len(REQUIRED)} documents)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
