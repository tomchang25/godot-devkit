# Godot Devkit

Shared development governance for Tom Chang's Godot 4.6 projects. This repository is consumed as a pinned Git submodule; projects never follow the remote branch at runtime.

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
2. the selected profile's `profile_startup.md`, when a project selects a profile
3. the consuming project's local `dev/agent_rules/agent_startup.md`

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

## Updating a consumer

```powershell
git -C dev/foundation fetch --tags
git -C dev/foundation checkout <tag-or-commit>
git add dev/foundation
```

Review the pointer update and run the consuming project's narrow validation before committing it. Do not point consumers at an unpinned branch checkout.

Verify the consumer contract with:

```powershell
python dev/foundation/tools/verify_consumer.py --root .
```

The verifier checks the selected profile, canonical documents, and compatibility pointers so a project cannot silently recreate a local shared-rule fork.

## Ownership boundary

This repository owns shared prose and workflow contracts. Runtime implementations such as FSM, Hitbox/Hurtbox, SceneRouter, and default autoloads remain in `godot-template`. A runtime system should move to a separately versioned addon only when existing games are expected to receive implementation updates.
