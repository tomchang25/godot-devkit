# React Strict Mode Effects

Platform: Web React.

React development mode may mount, clean up, and remount an effect to expose unsafe side effects. Do not hide the problem behind a flag that merely forces one execution; make setup repeatable and cleanup complete.

## Hazard

- An effect grants rewards, consumes resources, dispatches a durable command, or writes a save, so replay duplicates the mutation.
- A timer, subscription, event listener, observer, or async callback has no symmetrical cleanup and leaves multiple owners.
- A module/global `didRun` flag leaks across remounts, test isolation, or multiple component instances.

## Safe Shape

1. Explicit application commands own gameplay mutations; render/effect existence never grants authority by itself.
2. Every effect that acquires external ownership returns symmetrical cleanup for the same identity.
3. Async work uses cancellation, request identity, or a disposed guard so stale completion cannot overwrite newer state.
4. Autosave deduplicates by state revision or checkpoint rather than effect invocation count.
5. Tests exercise development replay and verify subscription count, cleanup, and exactly-once durable mutation.

## Review Prompts

- Does remount duplicate a reward, timer, subscription, or persistence write?
- Can an old async result overwrite newer state?
- Does cleanup remove the exact listener, observer, or subscription identity created by setup?
