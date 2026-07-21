# IndexedDB Upgrade Transactions

Platform: Web React.

IndexedDB object stores and indexes may change only inside the `versionchange` transaction created by `onupgradeneeded`. Once that transaction becomes inactive, later schema operations fail or leave the application without the expected layout.

## Hazard

- `onupgradeneeded` awaits fetch, a timer, or another promise that is not part of the upgrade transaction.
- Application payload version is reused as the IndexedDB database version, coupling storage layout and game-state migrations.
- An old connection in another tab blocks upgrade without an explicit blocked state or recovery path.
- A failed read immediately writes default state and destroys the original payload.

## Safe Shape

1. Database version describes object-store/index layout; save-envelope version describes game payload schema.
2. The upgrade callback performs synchronous schema operations and transaction-owned requests only.
3. Pure payload migration runs after a successful open and writes back only after the full migration succeeds.
4. Handle `blocked`, `versionchange`, quota failure, restricted storage, and transaction abort while preserving a playable degraded session when safe.
5. Tests cover a fresh database, supported old layouts, old payloads, blocked upgrades, aborted transactions, and write failure.

## Review Prompts

- Is this change a database-layout migration or a payload-schema migration, and is the correct version owner changing?
- Does the upgrade transaction cross an unsafe async boundary?
- Can autosave replace the old payload before hydration and migration settle?
