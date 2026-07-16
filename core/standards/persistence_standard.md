# Persistence Standard

Persistence is an infrastructure boundary around canonical game state. Domain rules and presentation code must not depend on storage names, file layouts, object stores, database handles, or platform transaction APIs.

## Ownership Boundary

- Persisted game state has one runtime owner. A persistence adapter serializes and restores that owner's state; it does not become a second state authority.
- Domain code consumes explicit state and returns results. Application orchestration decides when to load, migrate, resolve elapsed time, and write checkpoints.
- Storage layout version and game payload schema version remain separate when the platform exposes both concepts.

## Save Envelope

Every save format carries enough metadata to identify its payload schema and temporal checkpoint. The concrete serialization format is platform- and project-owned, but the envelope must provide equivalents of:

- A monotonic payload schema version.
- The time or logical checkpoint at which the state was committed.
- The canonical persisted state payload.

Additional integrity, slot, build, or content-version metadata belongs in the project contract when required.

## Requirements

- Hydration reaches a settled success, absent-save, or explicit failure state before automatic writes may replace existing storage.
- Writes occur at explicit checkpoints or through a bounded scheduler; rendering or frame frequency must not determine persistence frequency.
- Payload migration is sequential and follows `dev/agent_rules/save_migrations.md`.
- Concurrent session or process ownership is explicitly defined before the project claims multi-session safety.
- A storage failure preserves the in-memory session whenever safely possible and exposes persistence as unavailable or degraded; it must not silently replace an unreadable payload with defaults.
- Offline or elapsed-time resolution starts from the last committed checkpoint and uses the project's canonical time-resolution contract.

## Verification

Persistence changes cover new saves, absent saves, supported old payloads, interrupted writes, unavailable storage, hydration/write ordering, and round-trip behavior. Platform addenda add transaction, quota, locking, connection, filesystem, or application-lifecycle cases.
