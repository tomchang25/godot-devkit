# Foundation Startup

## Required Load Order

This repository is the shared governance foundation. In a consuming project:

1. Read this file.
2. Read `dev/foundation.config.json` when it exists. Load the selected platform startup from `dev/foundation/platforms/<platform>/platform_startup.md`, then load every selected profile startup from `dev/foundation/profiles/<profile>/profile_startup.md`.
3. Read the consuming project's `dev/agent_rules/agent_startup.md` for its snapshot, environment, tools, permissions, verification commands, and explicit project-local overrides.

When working inside a template subtree, treat the template's documented base directory as the consuming project root so the same `dev/` paths resolve below that base.

If the foundation submodule is missing or uninitialized, stop repository-specific work and ask for `git submodule update --init --recursive`. Shared rules must not be guessed from local compatibility pointers.

## Precedence

Load layers in this order:

```text
core -> platform -> profiles in declared order -> consuming project
```

Core rules are the default. A later layer may add narrower detail or explicitly supersede an earlier default when its scope requires a different contract. A superseding layer must name the conflict and replacement directly; silence does not override an earlier rule.

Do not copy a shared rule into a consuming project. Keep compatibility files as pointers and place only the project-specific delta in a local addendum.

## Shared Triggers

- Before adding, moving, or classifying governance documents, read `core/standards/governance_structure_standard.md`.
- Before introducing a Controller, System, Store, Service, manager, save provider, or another runtime state owner, read `core/standards/runtime_ownership.md` plus the selected profiles and relevant project-local standards.
- Before changing canonical, transient, presentation, or derived state ownership, read `core/standards/runtime_ownership.md` plus the selected profile.
- Before changing persistence, hydration, save scheduling, a persisted schema, or a compatibility promise, read `core/standards/persistence_standard.md`, `core/agent_rules/save_migrations.md`, and the platform and project-local persistence contracts.
- Before creating or updating probes, plans, sketches, implementation specs, reviews, closeouts, PR text, or change summaries, read `core/workflows/work_lifecycle.md`, the matching workflow, and `core/standards/change_summary_standard.md` where a delivered outcome is being summarized.
- Before release or compatibility assessment, read `core/skills/semantic_versioning.md`.

Platform and project-local startup rules add triggers for source formats, runtime APIs, accessibility, tests, linters, generated data, sandbox procedures, and build commands. Core documentation must not invent those execution details.
