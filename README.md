# Game Devkit

Shared development governance for game projects across engines and application platforms. The repository is consumed as a pinned Git submodule at `dev/foundation`; projects never follow its remote branch at runtime.

The remote repository may retain the legacy `godot-devkit` name during the migration. Repository naming does not change the layer contract described here.

## Layers

```text
core/                         Engine- and framework-neutral governance
  agent_rules/                Shared operating behavior and defaults
  standards/                  Durable cross-project output contracts
  skills/                     Portable recipes and format references
  workflows/                  Canonical planning, review, and delivery lifecycle
platforms/
  godot/                      GDScript, scene, autoload, and Godot-specific contracts
profiles/
  action-rpg/                 Action-entity architecture; currently constrained to Godot
  sim-management/             Store/System management architecture; currently constrained to Godot
```

`core/standards/governance_structure_standard.md` is the canonical owner for placement, language, extension, README, pointer, and addendum rules. This README is a navigation and installation surface only.

The load order is:

1. `core/agent_rules/foundation_startup.md`
2. The selected platform's `platform_startup.md`
3. Selected profiles in configuration order
4. The consuming project's `dev/agent_rules/agent_startup.md`

Later layers may add narrower detail or explicitly supersede a default. They must not silently copy or fork an earlier rule.

## Consumer Configuration

New consumers declare platform and profile axes independently in `dev/foundation.config.json`:

```json
{
  "schema_version": 2,
  "platform": "godot",
  "profiles": ["action-rpg"]
}
```

The selected platform is required. Profiles are optional and ordered. The consumer verifier rejects unknown platforms, duplicate profiles, unsupported platform/profile combinations, missing canonical documents, competing pointers, and local shared-rule forks.

Legacy Godot consumers may temporarily retain `dev/foundation.profile` with `core`, `action-rpg`, or `sim-management`. Legacy mode assumes the `godot` platform and follows transitional shims below old `core/` paths. A consumer must not keep both configuration files.

## Consumer Layout

```text
dev/
  foundation/                 This repository, pinned to one commit
  foundation.config.json      Selected platform and profiles
  agent_rules/                Project-local environment, permissions, and commands
  standards/                  Project standards and compatibility pointers
  workflows/                  Compatibility pointers and project-only commands
  skills/                     Compatibility pointers and project-only hazard cards
  docs/                       Product design, plans, reports, and archives
  tools/                      Project-owned executable tooling
```

Template repositories may install the foundation below a documented base subtree. Their startup entry must identify that subtree as the effective consumer root.

## Ownership

- Contracts that remain precise across engines and frameworks belong in `core/`.
- Irreducible runtime, framework, file-format, and platform-API contracts belong in `platforms/<platform>/`.
- Reusable architecture and game-paradigm conventions belong in `profiles/<profile>/`; a platform-dependent profile declares the constraint in `consumer_manifest.json`.
- Product rules, runtime owners, schemas, executable commands, permissions, active plans, and historical context belong in the consuming project.

A consuming project keeps shared discovery paths as compatibility pointers. It never copies and maintains local forks of shared rule text.

## Work Lifecycle

`core/workflows/work_lifecycle.md` is the single lifecycle owner for Draft, Main Plan, Child Sketch, Child Implementation Spec, Implementation, Verify, and Closeout transitions. Artifact standards define document quality, and command contracts define safe operations. Platforms may add dedicated commands, but they never fork the core lifecycle or duplicate shared workflows.

## Versioning and Synchronization

This repository is a versioned dependency with three separate operations:

| Operation | Purpose |
| --- | --- |
| Routine consumer sync | Obtain the foundation commit already pinned by the consuming project |
| Publish a devkit release | Release a changed shared contract to the devkit remote |
| Upgrade a consumer | Intentionally move a consuming project to a newer pinned foundation version |

A consumer records one exact foundation commit as a submodule pointer. It must not follow the devkit's default branch directly.

### Routine Consumer Sync

Use this in a consuming project to obtain the foundation version already pinned by that project's branch:

```powershell
git pull --ff-only
git submodule update --init --recursive
```

A detached `HEAD` inside `dev/foundation` is expected. Do not pull or create a branch inside the submodule unless intentionally developing the foundation itself.

Use `git submodule sync --recursive` only after a submodule URL changes or to clear a deliberate local URL override. Syncing URLs does not upgrade the pinned foundation commit.

### Publish a Devkit Release

After changing a shared contract:

```powershell
git pull --ff-only
python tools/verify_canonical_contracts.py
# Review and update VERSION and CHANGELOG for the intended release.
git add <changed-files>
git commit -m "<conventional-commit-message>"
git tag -a vX.Y.Z -m "vX.Y.Z"
git push origin main
git push origin vX.Y.Z
```

Choose the version according to public compatibility impact. Never move, delete, or edit an existing release tag. Both the commit and tag must be published before consumers pin the release.

### Upgrade a Consumer

After the target release is published:

```powershell
git -C dev/foundation fetch --tags
git -C dev/foundation checkout vX.Y.Z
python dev/foundation/tools/verify_consumer.py --root .
```

For a schema-2 migration, replace `dev/foundation.profile` with `dev/foundation.config.json` and update local compatibility pointers to the canonical paths declared by the selected layers before running the verifier. Review, commit, and push the submodule pointer and consumer migration from the consuming project.

## Verification

From a consuming project root:

```powershell
python dev/foundation/tools/verify_consumer.py --root .
```

From this repository root:

```powershell
python tools/verify_canonical_contracts.py
python tools/test_verify_consumer.py
```

The canonical verifier protects semantic baselines, English shared-governance language, core workflow platform neutrality, manifest structure, profile constraints, canonical targets, and legacy shims.

## Canonical Baseline Policy

Shared documents preserve the mature governance contract that predates this layered foundation as the minimum semantic baseline. Generalization may replace project names, paths, examples, and platform execution details, and project-only rules may move to consumer addenda, but it must not silently remove workflow stages, review depth, verification triggers, fallback guidance, or other behavioral contracts.

Compatible cross-project additions may extend that baseline. The canonical verifier protects contracts that have previously been weakened or lost during extraction.

## Runtime Boundary

This repository owns governance prose, artifact contracts, and verification metadata. Runtime implementations remain in templates, applications, or separately versioned addons. A runtime system should move into a shared implementation package only when existing games are expected to receive implementation updates, not merely because several projects follow the same prose standard.
