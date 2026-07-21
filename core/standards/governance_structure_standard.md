# Governance Structure Standard

This standard defines language, placement, ownership, and extension rules for shared governance documents. It is the canonical classification contract for this repository and its consumers. README files provide navigation; they do not own placement rules that are absent here.

## Language

Canonical governance documents in `core/`, `platforms/`, and `profiles/` are written in English. Code identifiers, commands, paths, and manifest keys retain their exact spelling.

Consuming projects may choose another language for product design, plans, reports, and project-local instructions. A project-local document that is promoted into shared governance must be translated into English as part of the promotion.

## Document File Naming

Governance and development documentation filenames use `snake_case`: lowercase words separated by underscores, with numeric ordering fields where a flow needs them (`port_08_c_wave_phase_orchestration`) and the artifact type as a dotted suffix (`.sketch.md`, `.implementation_spec.md`, `.probe.md`, `.addendum.md`). This applies to files under governance directories and consumer `dev/` documentation trees. Apply the rule to new documents; existing kebab-case filenames are renamed only in deliberate sweeps that update every inbound reference in the same change.

## Core-First Placement

Place a governance contract in `core/` whenever its meaning can remain correct across engines, frameworks, operating environments, and game architectures. Generalize examples and execution details before concluding that a platform copy is necessary.

Core owns:

- Agent behavior that is independent of a concrete toolchain.
- Planning, research, specification, review, delivery, and closeout workflows.
- Cross-project durable output contracts such as change summaries, lifecycle ownership, and runtime responsibility vocabulary.
- Format references and hazard cards whose contract does not require one engine or framework.

Core workflows state obligations and decision boundaries. They delegate concrete commands to the consuming project's startup, verification, and tooling contracts.

## Platform Placement

Use `platforms/<platform>/` only when removing the platform dependency would make the document vague, incomplete, or misleading. A platform document must depend directly on a runtime, framework, file format, platform API, or platform-specific validation procedure.

Examples include:

- Engine language and serialized scene-format rules.
- Framework lifecycle hazards and component APIs.
- Browser storage, service worker, and DOM-specific behavior.
- Dedicated engine import, build, screenshot, or test procedures.

Do not place a document in a platform merely because its first consumer uses that platform. Extract the general contract to core and keep only the irreducible technical addendum in the platform.

A platform may add commands that have no engine-neutral equivalent. It must not fork the canonical work lifecycle or create platform copies of core Plan, Sketch, Implementation Spec, Review, or Closeout workflows.

## Profile Placement

Use `profiles/<profile>/` for architecture or game-paradigm conventions that apply to multiple projects but not every game. Profiles describe patterns such as distributed action entities, simulation stores, management flows, or incremental-time resolution.

A profile should be platform-neutral when its contract can be expressed without implementation coordinates. A profile that genuinely depends on one platform must declare that platform constraint in `consumer_manifest.json`; do not pretend it is portable.

Profiles may add or explicitly supersede a core or platform default. A superseding document must name the earlier rule, explain the conflict, and state the replacement. Silence never overrides an earlier layer.

## Project-Local Placement

Keep a contract in the consuming project when it depends on that project's:

- Product rules, authored content, active plans, or historical context.
- Folder layout, runtime owners, data schema, save format, or migration history.
- Package manager, executable commands, CI environment, sandbox restrictions, or test harness.
- Explicit permissions or delivery policy.

Project-local rules may refine shared defaults and may explicitly supersede them when the architecture requires it. They must not copy a shared rule for convenience.

Every consumer implements the required project-local startup, Git, and test operation interfaces defined by `consumer_operations_standard.md`. The interface is shared; the effective permissions, environment constraints, and executable commands remain project-owned.

## Canonical Ownership

Every governance rule has exactly one canonical owner.

- A consumer reads canonical files directly from its pinned foundation instead of recreating them at compatibility paths.
- An addendum contains only the narrower platform, profile, or project-specific delta and links to the earlier owner.
- A README indexes canonical owners and explains how to enter the governance system. It does not become a second source of truth.
- A startup file defines load order and trigger-based reading. It links to standards instead of restating their full contracts.
- A manifest records machine-checkable layer availability, profile constraints, and startup paths. It does not replace the human-readable standard.

## Governance Artifact Placement

Classify a file by the primary thing it governs:

| Directory | Primary responsibility |
| --- | --- |
| `agent_rules/` | What an agent may or must do while operating |
| `workflows/` | How work and development artifacts move from idea to delivery |
| `standards/` | What a correct repository artifact or durable contract looks like |
| `skills/` | A focused recipe, format reference, or concrete hazard card |
| `tools/` | Executable validators, generators, hooks, and tool-owned resources |
| Consumer `docs/` | Actual product design, system documentation, plans, reports, and archives |

A filename containing `standard` does not determine its directory. Artifact formats and lifecycle transitions belong in workflows; durable output contracts belong in standards.

## Classification Checklist

Before adding or moving a governance document, answer in order:

1. Can the contract remain precise across platforms after replacing platform-specific examples and commands? If yes, place it in core.
2. Does the remaining contract require a concrete runtime, framework, file format, or platform API? If yes, place that delta in the platform.
3. Does it describe a reusable game architecture or paradigm rather than a technology? If yes, place it in a profile and declare any unavoidable platform constraint.
4. Does it depend on one product, repository layout, tool command, schema, or permission model? If yes, keep it project-local.
5. Does another document already own the rule? If yes, update that owner and add only a direct link or explicit addendum here.

When classification remains ambiguous, prefer the narrowest existing canonical owner that avoids duplication. Do not create a new layer or parallel standard for a hypothetical future consumer.

## Change Requirements

Changes to governance structure must update every affected discovery and verification surface in the same change:

- Startup load order and trigger maps.
- README navigation.
- `consumer_manifest.json`.
- Canonical and consumer verifiers.
- Consumer templates and scaffolding when a required project-local interface changes.
- Release notes when the public consumer contract changes.

A structural refactor is incomplete while an old path still appears canonical, a new owner is undiscoverable, or layer startup cannot reach the current owner.
