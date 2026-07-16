# Web React Platform Startup

Load this file after `core/agent_rules/foundation_startup.md` when the consuming project selects the `web-react` platform. This layer owns React lifecycle, TypeScript/TSX naming, DOM accessibility, browser capability, IndexedDB, service worker, Web/PWA contracts, and Web testing guidance. It does not redefine the core work lifecycle, persistence ownership, or runtime state ownership.

## Platform Triggers

- Before adding or reorganizing TypeScript, TSX, hooks, or CSS Modules, read `dev/foundation/platforms/web-react/standards/naming_conventions.md` and the consumer's project-structure standard.
- Before changing a React component, hook, effect, list rendering path, or interaction boundary, read `dev/foundation/platforms/web-react/standards/react_component_standard.md`. Effect work also reads `dev/foundation/platforms/web-react/skills/react-strict-mode-effects.md`.
- Before changing DOM interaction, responsive UI, focus, reduced motion, or assistive state, read `dev/foundation/platforms/web-react/standards/web_accessibility_standard.md`.
- Before changing browser APIs, lifecycle behavior, service workers, cache policy, or installability, read `dev/foundation/platforms/web-react/standards/web_platform_standard.md`; cache work also reads `dev/foundation/platforms/web-react/skills/service-worker-cache-versioning.md`.
- Before changing IndexedDB layout, browser persistence, hydration, or storage recovery, read `dev/foundation/core/standards/persistence_standard.md`, `dev/foundation/platforms/web-react/standards/browser_persistence_standard.md`, and `dev/foundation/platforms/web-react/skills/indexeddb-upgrade-transactions.md`.
- Before adding or running tests, read `dev/foundation/platforms/web-react/standards/testing_standard.md` plus the consumer's `dev/agent_rules/test_operations.md` for concrete test and build commands.

## Project Boundary

The consuming project owns its framework mode, router, server-component policy, browser support matrix, folder layout, package manager, scripts, deployment target, test libraries, and production build commands. The platform must not infer those choices from React alone.
