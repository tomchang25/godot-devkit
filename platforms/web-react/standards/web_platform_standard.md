# Web Platform Standard

Platform: Web React.

## Capability and Lifecycle

- Check browser capabilities before use and provide an explicit unsupported or degraded path when a capability is optional.
- Do not assume background timers, animation frames, visibility events, or service worker lifecycle events occur at precise intervals.
- Reconcile elapsed state from explicit timestamps or checkpoints after visibility resume, hydration, or reload; do not replay a guessed number of missed timer callbacks.
- Clean up browser listeners, observers, media queries, timers, and async ownership when their React owner unmounts or dependencies change.

## PWA and Caching

- Register production service workers only in environments whose deployment contract supports them. Development must not cache hot-reload or local build artifacts.
- Navigation documents, content-addressed assets, mutable runtime data, and API responses use strategies appropriate to their versioning and failure behavior rather than one blanket cache policy.
- Cache cleanup is application-scoped and never deletes unrelated origin caches.
- A deployment update must not silently mix incompatible application code, content, and persistence schemas inside one active transaction.

## Project-Owned Decisions

The consuming project defines supported browsers, responsive breakpoints, installability requirements, deployment host, router, rendering mode, offline promise, and build tooling. Browser availability alone does not require a PWA or offline cache.
