# Web React Platform Startup

Load this file after `core/agent_rules/foundation_startup.md` when the consuming project selects the `web-react` platform. This layer owns React lifecycle, TypeScript/TSX naming, repository structure, the verification command surface, DOM accessibility, browser capability, IndexedDB, service worker, Web/PWA contracts, and Web testing guidance. It does not redefine the core work lifecycle, persistence ownership, or runtime state ownership.

## Platform Triggers

- Before adding, moving, or reorganizing repository directories, source layers, tests, assets, or generated output, read `dev/foundation/platforms/web-react/standards/project_structure_standard.md` and the consumer's project-structure addendum.
- Before adding or renaming npm scripts, changing verification stages, or changing formatter configuration, read `dev/foundation/platforms/web-react/standards/command_surface_standard.md`.
- Before adding or reorganizing TypeScript, TSX, hooks, or CSS Modules, read `dev/foundation/platforms/web-react/standards/naming_conventions.md`.
- Before changing TypeScript control flow, function layout, or code spacing conventions, read `dev/foundation/platforms/web-react/standards/code_style_standard.md`.
- Before changing a React component, hook, effect, list rendering path, or interaction boundary, read `dev/foundation/platforms/web-react/standards/react_component_standard.md`. Effect work also reads `dev/foundation/platforms/web-react/skills/react_strict_mode_effects.md`.
- Before changing DOM interaction, responsive UI, focus, reduced motion, or assistive state, read `dev/foundation/platforms/web-react/standards/web_accessibility_standard.md`.
- Before changing browser APIs, lifecycle behavior, service workers, cache policy, or installability, read `dev/foundation/platforms/web-react/standards/web_platform_standard.md`; cache work also reads `dev/foundation/platforms/web-react/skills/service_worker_cache_versioning.md`.
- Before changing IndexedDB layout, browser persistence, hydration, or storage recovery, read `dev/foundation/core/standards/persistence_standard.md`, `dev/foundation/platforms/web-react/standards/browser_persistence_standard.md`, and `dev/foundation/platforms/web-react/skills/indexeddb_upgrade_transactions.md`.
- Before adding or running tests, read `dev/foundation/platforms/web-react/standards/testing_standard.md` plus the consumer's `dev/agent_rules/test_operations.md` for concrete test and build commands.

## Project Boundary

The consuming project owns its framework mode, router, server-component policy, browser support matrix, package manager, deployment target, test libraries, and concrete tool selection. The platform must not infer those choices from React alone. Repository layout and the verification command surface are platform-owned by the Web project structure and command surface standards; the consumer keeps only a declared structure addendum for deployment-specific trees and feature-level detail.
