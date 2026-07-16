# Browser Persistence Addendum

Platform: Web React. Read core `persistence_standard.md` first.

## Boundary

- Domain rules and React components access persisted state through application-owned repository interfaces; they do not know database names, object-store names, indexes, or live transactions.
- IndexedDB is the default browser storage for non-trivial game saves and structured content. `localStorage` is limited to small, synchronous preferences or bootstrap hints whose loss does not corrupt canonical progress.
- Database layout version and save-payload schema version are separate owners.

## Lifecycle and Recovery

- Hydration blocks autosave from replacing an existing payload until load and migration settle.
- Handle blocked upgrades, version-change notifications, transaction aborts, quota failures, private-mode restrictions, and unavailable storage as explicit states.
- Close stale connections when a version change requires another page to upgrade.
- Define cross-tab ownership or conflict policy before claiming multi-tab safety. A broadcast channel or storage event is coordination transport, not an ownership policy by itself.
- Preserve the in-memory session when safe after storage failure and expose persistence as unavailable; do not silently overwrite unreadable data with defaults.

## Verification

Cover fresh databases, supported old database layouts, supported old payloads, blocked upgrades, hydration/autosave ordering, quota or write failure, transaction abort, and cross-tab version-change behavior where the product supports multiple tabs.
