# Consumer Operations Standard

This standard defines the required project-local operating contract for every game-devkit consumer. The foundation owns the interface and starter templates; each consuming project owns the concrete project snapshot, permissions, commands, environment constraints, and available verification layers.

## Required Files

Every consumer must provide these files below its effective project root:

| File | Responsibility |
| --- | --- |
| `dev/agent_rules/agent_startup.md` | Project snapshot, selected governance layers, local discovery map, and operation-contract entry points |
| `dev/agent_rules/git_operations.md` | Authoritative project Git permission and failure policy |
| `dev/agent_rules/test_operations.md` | Authoritative project test, validation, environment, pass-criteria, and result-reporting policy |

These are project-owned contracts, not compatibility pointers. They may inherit a shared default by direct reference, but they must state the project's effective policy instead of asking agents to infer it from the foundation or neighboring repositories.

## Load And Ownership

The foundation startup loads first, followed by the selected platform and profiles, then `agent_startup.md`. The project startup must link directly to `git_operations.md` and `test_operations.md` so every Git mutation decision and every agent-run verification operation reaches one project-local authority.

Shared core and platform documents define portable behavior and technical hazards. They do not own a consumer's executable command, package runner, binary path, generated-data setup, CI filter, sandbox restriction, or permission override. Those values belong in the required project-local operation files.

## Agent Startup Contract

`agent_startup.md` must:

- identify the consuming project, selected platform, and selected profiles;
- summarize the project and its effective root closely enough to orient repository work;
- link to `git_operations.md` and `test_operations.md` as required operation contracts;
- route agents to additional project-local rules, standards, workflows, skills, tools, and product documentation by trigger; and
- state explicit project-local overrides without copying shared rule text.

The startup file is a discovery surface. Detailed Git and test procedures belong in their operation files, not inline in startup.

## Git Operations Contract

`git_operations.md` must:

- link to `dev/foundation/core/agent_rules/git_operations.md` as the shared default;
- state whether the project inherits or overrides that default;
- state the effective read, stage, commit, branch, push, and destructive-operation permissions;
- record environment-specific failure handling when Git state can be unreliable; and
- identify who performs operations that agents are not permitted to perform.

An inherited default still requires this project-local file so the effective decision is explicit and discoverable. Do not recreate the shared rule body when a direct reference plus a concise effective-policy statement is sufficient.

## Test Operations Contract

`test_operations.md` is the single source of truth for every agent-run test or platform validation operation in the project. It must:

- define when verification runs and how to choose the narrowest relevant layer;
- list every available layer, such as static checks, import/build checks, unit tests, integration tests, smoke tests, screenshots, or manual-only validation;
- state environment and preparation requirements, including snapshots, generated outputs, dependencies, binary or package-runner selection, and working-tree safety;
- provide the canonical command and pass criteria for each automated layer;
- distinguish setup-only phases from pass/fail phases;
- define expected noise, fallback behavior, failure cross-checking, and result reporting; and
- explicitly mark unavailable or manual-only layers instead of inventing a command.

Project workflow commands may select and sequence layers, but they must link to `test_operations.md` instead of duplicating its commands, pass criteria, caveats, or reporting contract. All new test layers are added to this file first.

For Godot consumers, the former split between `godot_test_check.md` and `godot_tests.md` is forbidden because it creates competing owners for setup and execution. Consolidate their durable content into `test_operations.md`, update callers, then remove both legacy files.

## Result Determination

A verification layer's result is the exit status of its documented command, never an interpretation of its output. Piping a verification command through a filter replaces that exit status and discards the failure signal; run the documented command directly and read its complete result. Before reporting a suite as passing, reconcile its executed, passed, failed, and skipped counts against the total the suite declares; a pass claim based on a filtered or partial view of the output is invalid. Consumers continue to own the concrete commands, layers, and pass criteria; this invariant governs only how any layer's outcome is established.

## Templates And Scaffolding

The manifest maps each required file to a tool-owned starter template. `tools/scaffold_consumer.py` renders the selected platform template into missing consumer paths and never overwrites an existing project-owned contract.

Scaffolded defaults are intentionally conservative. They declare inherited Git behavior and unavailable test layers when project-specific commands are unknown. A template repository or consuming project replaces those defaults with its real environment and tooling contract before relying on automated execution.

## Verification

`tools/verify_consumer.py` verifies that all three required files exist, contain the manifest-declared discovery references, and do not coexist with manifest-declared legacy owners. Verification checks the contract surface; it cannot prove that a project-specific command is operational, so consumers remain responsible for running their documented checks.
