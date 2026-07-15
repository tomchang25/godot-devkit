# Godot Devkit

Shared development governance for Godot 4.6 projects. This repository is consumed as a pinned Git submodule; projects never follow the remote branch at runtime.

## Layers

```text
core/                         Rules that apply across Godot project paradigms
  agent_rules/                Shared agent behavior and execution defaults
  standards/                  Output and architecture standards
  skills/                     Repeatable Godot/GDScript recipes and hazard cards
  workflows/                  Planning, review, and delivery workflows
profiles/
  action-rpg/                 Real-time, entity-distributed component conventions
  sim-management/             Store/System, turn/idle, and UI-heavy conventions
```

The load order is:

1. `core/agent_rules/foundation_startup.md`
2. The selected profile's `profile_startup.md`, when a project selects a profile
3. The consuming project's local `dev/agent_rules/agent_startup.md`

Later layers may add project detail or explicitly supersede a core default. They must not silently copy and fork a core rule.

## Consumer layout

Game repositories install this repository at `dev/foundation`:

```text
dev/
  foundation/                 This repository, pinned to one commit
  foundation.profile          `action-rpg`, `sim-management`, or `core`
  agent_rules/                Project-local execution and environment rules
  standards/                  Project-specific standards and compatibility pointers
  docs/                       Project plans and design documentation
  tools/                      Project-owned executable tooling
```

The Godot template installs it at `base/dev/foundation`, so composed projects receive the same `dev/foundation` layout.

## Ownership

Place a change according to who should receive it:

- Cross-project rules, standards, skills, and workflows belong in `core/`.
- Rules specific to one architecture paradigm belong in the matching `profiles/<profile>/` directory.
- Project-specific rules, environment details, runtime content, and product plans belong in the consuming project.

A consuming project must keep compatibility files as pointers to canonical documents. Do not copy and maintain local forks of shared rules.

## Versioning and synchronization

This repository is a versioned dependency with three separate workflows:

| Workflow                 | Purpose                                                                        |
| ------------------------ | ------------------------------------------------------------------------------ |
| Routine consumer sync    | Obtain the foundation commit already pinned by the consuming project's branch. |
| Publish a devkit release | Release a changed shared contract to the devkit remote.                        |
| Upgrade a consumer       | Intentionally move a consuming project to a newer pinned foundation version.   |

A consumer records one exact foundation commit as a submodule pointer. It must not follow the devkit `main` branch directly.

### Routine consumer sync

Use this in a consuming project to obtain the foundation version already pinned by that project's branch:

```powershell
git pull --ff-only
git submodule update --init --recursive
```

`git pull` updates the consuming project, including any changed submodule pointer. `git submodule update` checks out the exact foundation commit recorded by that pointer.

A detached `HEAD` inside `dev/foundation` is expected. Do not run `git pull` inside the submodule or create a branch there unless you are intentionally developing the devkit itself.

Use this only when a submodule URL in `.gitmodules` has changed, or to clear a deliberate local URL override:

```powershell
git submodule sync --recursive
```

`git submodule sync` updates remote URL configuration only; it does not upgrade the pinned foundation version.

### Publish a devkit release

Use this in the devkit repository after changing a shared contract:

```powershell
git pull --ff-only
# Edit the shared contract and release metadata.
python tools/verify_canonical_contracts.py
git add <changed-files>
git commit -m "<conventional-commit-message>"
git tag -a vX.Y.Z -m "vX.Y.Z"
git push origin main
git push origin vX.Y.Z
```

Choose the version according to public compatibility impact. Do not move, delete, or edit an existing release tag; publish a new version instead.

Both the commit and its tag must be published before consumers can reliably pin the release.

### Upgrade a consumer's pinned foundation version

Use this in a consuming project after the target devkit tag has been published:

```powershell
git -C dev/foundation fetch --tags
git -C dev/foundation checkout vX.Y.Z
git add dev/foundation
python dev/foundation/tools/verify_consumer.py --root .
git commit -m "chore(devkit): bump foundation to vX.Y.Z"
git push
```

This intentionally changes the consuming project's submodule pointer. Review, validate, commit, and push that pointer change with the consuming project.

Do not point consumers at an unpinned branch checkout.

## Verification

Verify a consumer contract from the consuming project root:

```powershell
python dev/foundation/tools/verify_consumer.py --root .
```

The verifier checks the selected profile, canonical documents, and compatibility pointers so a project cannot silently recreate a local shared-rule fork.

Validate the canonical governance contract from the devkit repository root:

```powershell
python tools/verify_canonical_contracts.py
```

## Canonical baseline policy

Starting with v0.2.0, shared documents preserve the mature governance contract that predates this foundation as the minimum semantic baseline. Generalization may replace project names, paths, and examples, and project-only rules may move to consumer addenda, but it must not silently remove workflow stages, review depth, lint/test triggers, fallback guidance, or other behavioral contracts.

Compatible cross-project additions may extend that baseline. The canonical contract verifier protects the sections that were accidentally weakened in v0.1.0.

## Runtime boundary

This repository owns shared prose and workflow contracts. Runtime implementations such as FSM, Hitbox/Hurtbox, SceneRouter, and default autoloads remain in `godot-template`. A runtime system should move to a separately versioned addon only when existing games are expected to receive implementation updates.
