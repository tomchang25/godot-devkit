# Runtime Ownership

This document defines which runtime role may own which state. Naming conventions define the suffix; this standard defines the ownership boundary behind the suffix.

---

# 1. Primary Test

Classify runtime code by lifetime, source of truth, and save/checkpoint requirement before choosing a suffix.

| Question                                                                                     | If yes                                                               | If no                           |
| -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- | ------------------------------- |
| Does the state exist only inside one active scene/session and get discarded with that scene? | It may belong to a `Controller`.                                     | It needs a domain owner.        |
| Must the state survive save/load, checkpoint restore, scene changes, or run resume?          | It belongs to a `Store`, save provider, `System`, or explicit owner. | It may remain scene-local.      |
| Is the state trusted by multiple systems as domain truth?                                    | It belongs to the concept owner.                                     | A controller may coordinate it. |
| Is the script pure computation with no mutable state or side effects?                        | It may be a `Service` or helper.                                     | Do not call it a pure service.  |

---

# 2. Controller

Use `Controller` for scene-scoped scripts that orchestrate runtime flow between scene nodes, UI, and domain owners for the current active session.

A controller may own state that is discarded with the scene, such as the current local phase, pending presentation items, selected interaction mode, pending transition, or session-local modifiers, when the game does not support checkpoint/save restoration for that session.

A controller may call owners to apply durable effects, but it must not silently become a second source of truth for another domain.

Examples:

| Good controller state                         | Reason                                      |
| --------------------------------------------- | ------------------------------------------- |
| Current modal choice                          | UI flow state for the current choice.       |
| Pending presentation items                    | Transition state before nodes are revealed. |
| Current phase in a no-checkpoint minigame      | Scene-local session flow state.             |
| Active targeting or selection mode             | Input/UI flow state.                        |

---

# 3. Domain Owners

State that must outlive the controller, be serialized, be restored from checkpoint, or serve as cross-system truth belongs to the owner of that concept.

Examples:

| Concept                                                         | Owner                                              |
| --------------------------------------------------------------- | -------------------------------------------------- |
| Persisted settings                                              | Settings store/provider.                           |
| Player stat modifiers                                           | Player-stat owner.                                 |
| Session progression that must survive outside the active scene  | Session/progression owner.                          |
| World or board truth                                            | Authority for that world/board domain.              |
| Save payload                                                    | The provider that owns the state being serialized. |

If a scene-local controller state later needs checkpoint, save, or cross-scene resume, promote that state into the relevant owner instead of adding ad-hoc persistence to the controller.

---

## State Lifecycle Addendum

Classify state by lifecycle as well as by runtime role:

- **Presentation state** affects only the current interaction surface, such as selection, filters, transient panels, or draft input. Its controller or feature UI owner keeps it local unless several surfaces require one explicit UI owner.
- **Persisted game state** contains progress, resources, location, and durable operations. The domain owner or application mutation gateway owns it; presentation code does not mutate it directly.
- **Runtime transient state** contains hydration status, pending writes, active capabilities, connection state, and reconstructable coordination. Infrastructure or application orchestration owns it; it is not player progress.
- **Derived state** is computed from canonical state and authored content, such as eligibility, previews, capacity, progress, or unlock state. It is not persisted by default, and memoization never creates a second source of truth.

State-changing commands validate preconditions, produce one coherent next state, return explicit errors for invalid input, and coordinate related logs, accounting results, and dirty-save markers in the same application transaction when consistency requires it. Time, randomness, storage, and external capabilities enter through explicit inputs or narrow adapters.

Multiple entry points that perform the same transition use the same command or resolver so resumed, automated, online, and manually triggered paths cannot drift.

---

# 4. System

Use `System` for a domain coordinator, mutation gateway, save provider, or aggregate owner when a concept is broader than one scene or must mediate mutations for consistency.

A system may own state directly or hold stores depending on the project architecture. It should expose narrow mutation methods so scene code does not bypass invariants.

---

# 5. Store

Use `Store` for a mutable domain state container when the project architecture uses stores. Stores own live fields for one domain and guard their invariants through mutators.

A store is appropriate when state needs serialization, validation, migration, or coordinated access by a system. Do not create a store only to hold short-lived UI flow state that dies with the scene.

---

# 6. Service

Use `Service` only for stateless computation. A service takes inputs, computes outputs, and returns results without owning mutable state, mutating stores, changing scene nodes, opening UI, or applying gameplay side effects.

Examples:

| Good service/helper work                         | Not service work                |
| ------------------------------------------------ | ------------------------------- |
| Select three entries from an input pool.         | Open the selection overlay.     |
| Compute valid board candidates from inputs.      | Mutate authoritative board data. |
| Compute an amount from configuration and modifiers. | Advance the owning session.  |

Code that applies side effects may still be a helper or applier, but do not classify it as a pure service.
