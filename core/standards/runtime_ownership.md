# Runtime Ownership

This document defines which runtime role may own which state. Naming conventions define the suffix; this standard defines the ownership boundary behind the suffix without requiring a specific preset architecture.

---

# 1. Primary Test

Classify runtime code by lifetime, source of truth, and save/checkpoint requirement before choosing a suffix.

| Question | If yes | If no |
| -------- | ------ | ----- |
| Does the state exist only inside one active scene/session and get discarded with that scene? | It may belong to a `Controller`. | It needs a domain owner. |
| Must the state survive save/load, checkpoint restore, scene changes, or run resume? | It belongs to a save provider, domain owner, or preset-specific state container. | It may remain scene-local. |
| Is the state trusted by multiple systems as domain truth? | It belongs to the concept owner. | A controller may coordinate it. |
| Is the script pure computation with no mutable state or side effects? | It may be a `Service` or helper. | Do not call it a pure service. |

---

# 2. Controller

Use `Controller` for scene-scoped scripts that orchestrate runtime flow between scene nodes, UI, and domain owners for the current active session.

A controller may own state that is discarded with the scene, such as current offer, selected interaction mode, pending transition, preview selection, current wave index in a no-checkpoint scene, or other UI/session flow state.

A controller may call owners to apply durable effects, but it must not silently become a second source of truth for another domain.

---

# 3. Domain Owners

State that must outlive the controller, be serialized, be restored from checkpoint, or serve as cross-system truth belongs to the owner of that concept.

Examples:

| Concept | Owner |
| ------- | ----- |
| Persisted settings | Settings store/provider. |
| Save payload | The provider that owns the state being serialized. |
| Cross-scene gameplay state | Project or preset-specific owner. |
| Terrain, stats, economy, or progression truth | The authority for that concept. |

If a scene-local controller state later needs checkpoint, save, or cross-scene resume, promote that state into the relevant owner instead of adding ad-hoc persistence to the controller.

---

# 4. System And Store

The base layer does not require a `System` or `Store` architecture. If a project or preset introduces those names, use `System` for domain coordination or mutation mediation and `Store` for mutable domain state containers, not for short-lived UI flow state that dies with one scene.

---

# 5. Service

Use `Service` only for stateless computation. A service takes inputs, computes outputs, and returns results without owning mutable state, mutating stores, changing scene nodes, opening UI, or applying gameplay side effects.

Code that applies side effects may still be a helper or applier, but do not classify it as a pure service.
