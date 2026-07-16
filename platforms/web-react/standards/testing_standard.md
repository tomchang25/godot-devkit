# Web React Testing Standard

Platform: Web React.

## Layers

- **Domain tests** cover formulas, eligibility, progression, elapsed-time resolution, and pure payload migrations without React or browser APIs.
- **Application tests** cover commands, repository orchestration, save scheduling, hydration ordering, and recovery across domain and browser-adapter boundaries.
- **Component tests** cover visible information, disabled and error states, keyboard interaction, focus behavior, and state-to-view mapping through the DOM.
- **Build smoke** proves that the consumer's production bundle can be assembled and started under its deployment configuration.

## Rules

- Pass time, randomness, browser capabilities, and storage through explicit inputs or adapters.
- Assert observable behavior rather than component internals or hook implementation details.
- Each practical bug fix includes a regression test at the layer that owns the broken behavior.
- Snapshot tests do not replace assertions for important text, ARIA state, interaction, formulas, persistence, or migration outcomes.
- Tests that touch IndexedDB, browser globals, service workers, timers, or global listeners isolate and clean up their ownership.
- A production build does not replace focused component, application, or domain regression coverage.

The consumer owns the concrete runner, React test libraries, browser environment, build command, and required CI gates.
