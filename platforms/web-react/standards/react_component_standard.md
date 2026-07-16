# React Component Standard

Platform: Web React.

## Responsibility

- Components render state and wire user intent to application commands. They do not own game formulas, persistence layout, or durable state transitions.
- Hooks package React lifecycle or reusable presentation behavior; they do not become hidden domain services.
- Keep feature-specific components, styles, tests, and fixtures near their project-local owner. The consuming project defines the actual folder layout.
- Extract shared components only after their semantics and variation points are stable; repeated markup alone does not establish a reusable contract.

## Types and Identity

- Use named prop types for public components and hooks.
- Avoid `any`, opaque catch-all records, and boolean-flag combinations that encode mutually exclusive modes without a discriminated state.
- List keys use stable domain or content identity. Array indexes are acceptable only for truly static, order-independent presentation with no per-item state.

## Lifecycle

- Rendering is pure. It does not grant rewards, mutate game state, write persistence, register global ownership, or trigger irreversible work.
- Effects coordinate external systems and return symmetrical cleanup where ownership is acquired.
- Async completion cannot overwrite newer state after unmount, dependency change, or request replacement.
- Development remount and Strict Mode replay must not duplicate subscriptions, timers, commands, or writes.

React server components, client boundaries, routing conventions, data-fetching libraries, styling systems, and compiler settings are framework/project decisions, not defaults of this standard.
