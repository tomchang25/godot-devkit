# Foundation Startup

## Required Load Order

This repository is the shared governance foundation. In a consuming project:

1. Read this file.
2. Read `dev/foundation.config.json` when it exists. Load the selected platform startup from `dev/foundation/platforms/<platform>/platform_startup.md`, then load every selected profile startup from `dev/foundation/profiles/<profile>/profile_startup.md`.
3. Read the consuming project's `dev/agent_rules/agent_startup.md` for its snapshot, environment, tools, and explicit project-local overrides. That startup must route Git decisions to `dev/agent_rules/git_operations.md` and test or validation operations to `dev/agent_rules/test_operations.md`.

When working inside a template subtree, treat the template's documented base directory as the consuming project root so the same `dev/` paths resolve below that base.

If the foundation submodule is missing or uninitialized, stop repository-specific work and ask for `git submodule update --init --recursive`. Shared rules must not be guessed from consumer-local files.

## Path Resolution

In canonical foundation documents, a path starting with `core/`, `platforms/`, or `profiles/` resolves from the foundation repository root — in a consuming project, below `dev/foundation/`; in a template, below the documented base subtree's `dev/foundation/`. A path starting with `dev/` (without `foundation/`) resolves from the consuming project root and always names a project-owned file, as do `TODO.md` and `CHANGELOG.md`. A canonical document must never reference a foundation-owned file through a consumer-local `dev/` path.

## Precedence

Load layers in this order:

```text
core -> platform -> profiles in declared order -> consuming project
```

Core rules are the default. A later layer may add narrower detail or explicitly supersede an earlier default when its scope requires a different contract. A superseding layer must name the conflict and replacement directly; silence does not override an earlier rule.

Do not copy a shared rule into a consuming project. Read it directly from the pinned foundation and place only the project-specific delta in a local addendum.

## Shared Triggers

- Before adding, moving, or classifying governance documents, read `core/standards/governance_structure_standard.md`.
- Before creating or changing the required project-local startup, Git, or test operation contracts, read `core/standards/consumer_operations_standard.md`.
- Before any Git mutation or recovery operation, read the consuming project's `dev/agent_rules/git_operations.md`.
- Before running any test, build, import, screenshot, smoke, or other platform validation operation, read the consuming project's `dev/agent_rules/test_operations.md`.
- Before introducing a Controller, System, Store, Service, manager, save provider, or another runtime state owner, read `core/standards/runtime_ownership.md` plus the selected profiles and relevant project-local standards.
- Before changing canonical, transient, presentation, or derived state ownership, read `core/standards/runtime_ownership.md` plus the selected profile.
- Before changing persistence, hydration, save scheduling, a persisted schema, or a compatibility promise, read `core/standards/persistence_standard.md`, `core/agent_rules/save_migrations.md`, and the platform and project-local persistence contracts.
- Before creating or updating probes, plans, sketches, implementation specs, reviews, closeouts, PR text, or change summaries, read `core/workflows/work_lifecycle.md`, the matching workflow, and `core/standards/change_summary_standard.md` where a delivered outcome is being summarized.
- Before finishing any change, read `core/agent_rules/lint_before_finish.md` and run the consuming project's non-mutating verification scoped to the touched files.
- Before release or compatibility assessment, read `core/skills/semantic_versioning.md`.

Platform and project-local startup rules add triggers for source formats, runtime APIs, accessibility, tests, linters, generated data, sandbox procedures, and build commands. Core documentation must not invent those execution details.
