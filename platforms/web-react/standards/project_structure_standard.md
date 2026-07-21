# Web Project Structure Standard

Platform: Web React.

This standard is the canonical owner of repository layout, root directory vocabulary, source layer vocabulary, and import boundary rules for Web game consumers. A consuming project keeps a project-local structure addendum only for trees this standard does not name (deployment shells, server concerns) and for feature-level placement detail. TypeScript and directory naming spelling remains owned by `naming_conventions.md`.

## Repository Root

```text
src/        Production application source and packaged runtime assets
test/       Automated test source
assets/     General references and editable source material; never imported at runtime
public/     Only platform files that require stable URLs
dist/       Generated build output; ignored by Git
dev/        Pinned foundation, governance, documentation, and project tooling
```

Root directories use singular names. A plural root directory indicates an instance collection that belongs under a narrower owner rather than at the repository root; see the directory naming rules in `naming_conventions.md`.

- `dist/` is exclusively the generated output of the production build command. The generated-output directory is named `dist/`, never `build/`, and Git ignores its contents. Build tooling source does not live there; it belongs under `dev/tools/` or the project's declared script tree. Source code and tools must not depend on a pre-existing `dist/`.
- `assets/` is the library for references, editable source files, and unoptimized material. It sits outside the runtime module graph and is never imported by application code. Every runtime asset is copied or exported into `src/content/<feature>/assets/` and imported through source code so the bundler can fingerprint and package it.
- `public/` is reserved for platform files that require stable URLs, such as a Web manifest, service worker, or favicon. Normal game content does not belong there. A project that needs none of these omits `public/` entirely.
- `test/` owns all automated test source: `test/unit/` for domain, content, and runtime tests, and `test/e2e/` for browser acceptance tests. Test files do not live beside production modules. Unit test paths mirror the relevant `src/` ownership path when practical. Runtime-selectable scenarios remain in `src/harness/`; assertions and runner-specific code belong in `test/`.
- Deployment shells and server concerns (a desktop wrapper tree, a worker entry, a database migration tree) are project-owned root trees. The project structure addendum declares each one and states that it is outside the game layer vocabulary below.

## Source Layers

```text
src/
  app/            Application composition, route shell, bootstrap, global styles
  content/        Authored game data grouped by feature, plus feature-owned runtime assets
  core/           Deterministic rules, state, commands, and semantic events
  harness/        Deterministic scenarios, debug API, and semantic mirrors
  platform/       Adapters for browser, storage, desktop shell, and distribution APIs
  presentation/   Canvas or WebGL renderers and animation timelines (earned)
  runtime/        Orchestration between core, presentation, and UI
  shared/         Proven cross-feature source with no narrower owner (earned)
  ui/             Feature-owned React interfaces, hooks, and styles
```

- `core/` owns deterministic gameplay state, rules, commands, and semantic events. Core modules import only other core modules. They never import a UI framework, renderer, DOM or browser global, platform adapter, asset file, or asset URL; core refers to textures, audio, and effects by semantic identifier. When core groups record and state type definitions into a directory, that directory is named `model/`.
- `content/` owns authored game data — definitions, layouts, configuration, and numeric records — grouped by gameplay feature, plus package-ready runtime assets under `content/<feature>/assets/`. Content may construct or type data through core contracts only. It never owns mutable run state or presentation flow.
- `runtime/` coordinates command execution, snapshots, semantic event routing, and presentation completion. It does not reimplement gameplay outcomes.
- `platform/` owns adapters for browser capabilities, persistence, desktop shells, distribution platforms, and other external APIs. Adapters may implement runtime-owned port contracts; they never call into UI.
- `ui/` owns feature-scoped React components, hooks, and styles. A feature-root component keeps its styles, tests fixtures, and helpers close; do not build repository-wide `components/`, `hooks/`, or `utils/` trees organized by artifact type.
- `app/` owns application assembly: routing, document metadata, global styles, and the bootstrap entry. The bootstrap entry stays minimal and accumulates no gameplay or presentation logic.
- `harness/` owns deterministic scenario definitions, scenario discovery, debug APIs, and semantic mirrors used by tests and manual inspection.
- `presentation/` and `shared/` are earned layers: create them when the owning work actually exists, never in advance. `presentation/` maps core snapshots and semantic events to renderer objects and animation timelines; animation lifetime never controls whether an entity remains logically active. `shared/` holds source (and `shared/assets/`) with demonstrated cross-feature ownership and no more precise owner; it is not a default or miscellaneous location.

## Import Boundaries

- `core` imports nothing outside `core`.
- `content` imports only `core` contracts.
- `runtime` and `platform` never import `ui`, `shared`, or `app`.
- `ui` reaches platform capabilities through `runtime`, never by importing `platform` or `app` directly.
- Nothing imports `harness` except `app`. The route shell is the only harness wiring point, so the harness stays a test seam rather than a rule bypass.
- Cross-layer imports use the project's path alias so a boundary crossing is visible in the import specifier; relative `../` paths do not cross layer roots.

## Enforcement

Layer boundaries are machine-checked by a dependency rule tool selected by the project and run inside the aggregate verification command. The boundary prose and the rule configuration change in the same commit: a rule the prose does not describe, or prose the rule does not enforce, is the drift this pairing exists to prevent. A boundary violation means code is in the wrong place; the fix is moving the code per the placement test, not widening the rule.

## Placement Test

Before adding or moving a project file:

1. Deterministic gameplay state, rules, or semantic events go in `core/`.
2. Authored definitions and feature-owned runtime assets go in `content/<feature>/`.
3. Flow coordination and state mutation gateways go in `runtime/`.
4. Code that touches a browser or host API goes in `platform/`.
5. A feature's components, hooks, or styles go in the owning `ui/<feature>/`.
6. Visual or audio realization goes in `presentation/` once that layer is earned.
7. Cross-feature source with multiple current owners goes in `shared/` once that layer is earned.
8. Routes, document metadata, global CSS, and bootstrap wiring go in `app/`.
9. Assertions go in `test/`, source material in root `assets/`, generated output in `dist/`, and development artifacts in `dev/`.
