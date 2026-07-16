# Changelog

## 0.4.1

- Remove legacy Godot `core/` platform-pointer shims and require schema-2 `foundation.config.json` consumers to select their platform explicitly.
- Make Probe an optional lifecycle stage before an optional Plan, and move its artifact contract into `core/workflows/` alongside Plan, Sketch, and Implementation Spec.

## 0.4.0

- Establish an engine-neutral governance core with a canonical work lifecycle and governance-structure standard.
- Move irreducible Godot, GDScript, scene, autoload, and engine UI contracts into a dedicated Godot platform layer.
- Generalize shared research, specification, review, staged-review, and verification workflows so consuming projects own concrete tool commands.
- Add schema-2 consumer configuration with independent platform and profile selection.
- Add a minimal Web React platform for React lifecycle, DOM accessibility, browser persistence, IndexedDB, service workers, and PWA/browser capability contracts.
- Promote persistence ownership and state lifecycle rules into core; keep accessibility and testing in the Web React platform until another platform has a concrete shared contract.

## 0.3.0

- Move the simulation-management preset's game-specific runtime archetype tree from reusable infrastructure into a game-owned domain layer.
- Clarify that action-RPG components and entity bases belong in reusable infrastructure only when their contracts are independent of a concrete feature.
- Preserve each profile's runtime ownership model while making feature ownership, authored content, and cross-project reuse distinct placement concerns.

## 0.2.0

- Rebuild canonical governance from Tickstrike's pre-foundation rules while generalizing project-specific examples and paths.
- Restore mature lint, FSM, node-reference, planning, specification, research, review, and closeout contracts that v0.1.0 weakened.
- Keep Tickstrike's clocked grid-enemy FSM rules in a project-local addendum instead of leaking them into shared core or deleting them.
- Add a canonical contract verifier to prevent future shared-rule updates from silently dropping required behavior.

## 0.1.0

- Introduce the shared core/profile layout, compatibility pointers, consumer verifier, and pinned submodule workflow.
