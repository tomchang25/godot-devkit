# Work Lifecycle

This document is the single lifecycle owner for forward work as it moves from an idea into implementation, verification, and closeout. Artifact standards define what a plan, sketch, implementation spec, review, and closeout must contain. Consumer-local documentation rules define where active and archived artifacts live. Other documents may point to this lifecycle, but they must not recreate or silently override the full state machine.

## Canonical Flow

Use this route for medium or large work that needs durable design and reviewable slices:

```text
Draft
-> Main Plan
-> Child Sketch
-> Child Implementation Spec
-> Implementation
-> Verify
-> Child Closeout
-> next child or Main Plan Closeout
```

A sketch is the default exploration stage for a non-trivial child, but it is not a mandatory ceremony. A child whose behavior, ownership seam, and implementation boundary are already small and clear may move directly from the main plan to a codebase-verified implementation spec.

Use this route for narrow work that still crosses enough boundaries to require a verified handoff:

```text
Feature request, actionable probe, or tracked item
-> Standalone Implementation Spec
-> Implementation
-> Verify
-> Standalone Closeout
```

Trivial fixes, copy changes, configuration edits, and other tightly bounded work may proceed with a compact implementation note. Skipping a durable artifact never removes applicable review, verification, or closeout obligations.

## Transition Gates

### Draft to Main Plan

Promote a draft when it needs stable requirements, substructure, explicit ordering, multiple reviewable slices, or a durable link:

1. Create a main plan using `plan_standard.md`.
2. Move the draft's durable intent into the plan instead of retaining two requirement owners.
3. Replace the draft with the consumer's single forward-work pointer.

Before the plan becomes queued or active, its Goal, Requirements, Non-Goals, Acceptance Criteria, and necessary child overview must be complete. Decisions that would materially change product scope or observable behavior must be resolved in conversation rather than parked in the plan.

### Main Plan to Child Sketch

Create a child sketch when the durable behavior is settled but the likely implementation shape, ownership seam, migration boundary, or landing sequence still needs exploration:

1. Create a sibling sketch using `sketch_standard.md`.
2. Point to it from the parent plan's child overview only; do not create an independent forward-work entry.
3. Treat codebase coordinates in the sketch as provisional context rather than implementation authority.

Skip this transition when the child boundary is already narrow and clear enough for direct spec-time verification.

### Sketch to Implementation Spec

Convert the next actionable child into an implementation spec only after product behavior, compatibility promises, scope, and numerical meaning are locked:

1. Re-read the relevant live codebase and create the implementation model using `implementation_spec_standard.md`.
2. Use the sketch as context only. Verify or replace every file, symbol, relationship, and sequencing claim.
3. Update the parent child overview so exactly one artifact is the executable handoff.

An implementation spec never carries unresolved questions. If the live codebase exposes a conflict that would change approved behavior, stop and return to the decision gate instead of silently rewriting the plan.

### Implementation Spec to Implementation

Implementation begins only when all of the following are true:

- The Goal and Summary provide a reviewable approval surface.
- Relational Context covers every relationship inside the Files to Change blast radius.
- Scope, compatibility, migration, recovery behavior, meaningful edge cases, and verification have no unresolved decisions.
- The parent plan or forward-work tracker points to exactly one executable handoff.

Implementation may adapt local technical details when the live code differs from the spec without changing approved behavior. A difference that changes requirements, scope, or compatibility returns to the decision gate.

### Implementation to Verify

Implementation is not complete until the consumer's verification contract has been satisfied:

1. Run the focused checks named by the implementation spec or required by the changed behavior.
2. Follow the consuming project's `dev/agent_rules/lint_before_finish.md` and any triggered platform or project-local validation rules.
3. Return to implementation after a failure and rerun every affected check after the fix.
4. Proceed only when acceptance criteria and required checks pass, or when the user explicitly accepts a documented verification gap.

Core workflows define the obligation to verify. Platforms and consuming projects own the concrete commands because runtimes, package managers, linters, and test harnesses differ.

### Verify to Child Closeout

Use the closeout standard and command contract to:

- Record the durable shipped outcome in the consumer's history owner when the change warrants one.
- Remove the shipped child from the parent overview.
- Archive the implementation spec and archive or remove any superseded sketch.
- Return to the next child while the main plan still has unshipped scope.

### Child Closeout to Main Plan Closeout

Close the main plan after no unshipped children remain and shipped behavior satisfies every acceptance criterion:

1. Update evergreen documentation with any current contract that must remain discoverable.
2. Archive the main plan.
3. Remove its active or queued pointer from the forward-work tracker.
4. Keep completed history only in the consumer's designated history owner; do not retain a competing Done list.

## Review Position

Review is a quality activity that may apply to a plan, sketch, spec, staged snapshot, branch, or implementation. It is not a mandatory tracking state. A review is read-only unless the user also authorizes fixes, and any requested fix returns to the appropriate artifact or implementation stage.

## Operational Commands

Artifact standards define what a correct artifact looks like. Command contracts define how an operation is performed safely.

| Operation | Core command contract | Mutation boundary |
| --- | --- | --- |
| Retrieve focused repository context | `commands/research-context.md` | Read-only |
| Resolve user-authority decisions before a spec | `commands/spec-discuss.md` | Read-only |
| Build a codebase-verified implementation spec | `commands/spec-build.md` | Documentation and tracking only |
| Review a staged snapshot | `commands/stage-review.md` | Read-only |
| Close completed work | `commands/closeout.md` | Documentation and tracking only |
| Suggest a staged commit message | `commands/commit-msg.md` | Read-only |
| Review a branch and draft pull-request text | `commands/pr-review.md` | Read-only |

Platform-only commands, such as a dedicated engine test procedure, may live below `platforms/<platform>/workflows/commands/`. They extend the available operations but never fork this lifecycle or duplicate a core command.

## Tracking States

Consumers may choose different filenames, but each tracked item has one active home and one owner for each direction of time:

- Draft: discussion has substance but no durable plan yet.
- Queued plan: a main plan exists but is not the current execution flow.
- Active: a handoff, implementation, or verification step is in progress or ready to execute.
- Compact item: a small chore or bug does not require a main plan.
- Shipped history: the single durable record of completed outcomes.
- Archive: historical plans and specs that are no longer active authority.

Consumer-local documentation rules define the concrete paths and pointer syntax. They may refine names, but they must preserve single ownership and the transition gates in this lifecycle.
