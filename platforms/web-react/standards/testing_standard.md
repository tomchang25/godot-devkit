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
- Browser acceptance suites verify system capabilities, not per-content variants; a new content entry that reuses a proven capability does not add a browser test.

## Golden Fixtures

- A normal test run only asserts against committed golden fixtures and never rewrites them; a divergence stays failing until a human resolves it.
- Regenerate a golden only through the consumer's dedicated update command, and only when the change under review intentionally alters a rule, a value, or content. Review the regenerated fixture line by line and name the behavioral change in the change summary.
- Regenerating a golden to turn a failing test green without an intended behavior change defeats the gate: a determinism regression reaching a golden is a finding, not a formatting chore.

The consumer owns the concrete runner, React test libraries, browser environment, build command, and required CI gates.
