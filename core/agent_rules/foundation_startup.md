# Foundation Startup

## Required Load Order

This repository is the shared governance layer. In a consuming project:

1. Read this file.
2. Read `dev/foundation.profile` from the consuming project. If it names `action-rpg` or `sim-management`, read `dev/foundation/profiles/<profile>/profile_startup.md`.
3. Read the consuming project's `dev/agent_rules/agent_startup.md` for its snapshot, environment, tools, and project-specific rules.

When working inside `godot-template/base`, treat `base/` as the consuming project root. The same paths then resolve below `base/dev/`.

If the submodule is missing or uninitialized, stop repository-specific work and ask for `git submodule update --init --recursive`. Shared rules must not be guessed from compatibility pointer files.

## Precedence

Core rules are the default. A selected profile may add paradigm-specific rules. A consuming project may add project-specific detail or explicitly supersede a default when its architecture requires it. A later layer must state the conflict and replacement directly; silence does not override an earlier rule.

Do not copy a shared rule into a consuming project. Keep compatibility files as one-line pointers and edit the canonical file here.

## Shared Triggers

- Adding, renaming, or restructuring GDScript: read `core/standards/gdscript_structure_standard.md` and `core/standards/naming_conventions.md`.
- Creating scenes, node references, or runtime children: read `core/standards/scene_node_source_standard.md` and, for reusable components, `core/standards/component_scene_standard.md`.
- Introducing a Controller, System, Store, Service, manager, or save provider: read `core/standards/runtime_ownership.md` plus the selected profile.
- Changing navigation, settings, debug behavior, error guards, registries, theme, or audio: read the matching standard and skill under `core/` before editing.
- Creating plans, sketches, specs, reviews, PR text, or closeout summaries: follow the matching file under `core/workflows/` and `core/standards/change_summary_standard.md`.
- Before release or compatibility assessment: read `core/skills/semantic_versioning.md`.

Project-local startup rules decide which tests, linters, generated-data commands, and sandbox procedures are available. Core documentation must not invent those project-specific commands.
