# Closeout Standard

Closeout removes completed work from forward-looking surfaces, records the durable outcome in the consumer's shipped-history owner, and archives artifacts that no longer hold active authority. Closeout never stages, commits, pushes, rewrites history, or opens a pull request unless the user separately authorizes that operation.

`work_lifecycle.md` owns the entry conditions and state transitions around closeout. This file owns closeout quality and artifact outcomes. `commands/closeout.md` owns the operational procedure for detecting and processing a concrete completed scope.

## Determine Scope

1. Identify the delivered boundary from the user's request, the selected plan or spec, and the relevant working snapshot.
2. If available evidence cannot distinguish which child or flow is complete, stop and ask rather than guessing progress.
3. Read the parent plan, executable spec, applicable acceptance criteria, and actual verification results.

## Child Closeout

When a plan child is complete:

1. Confirm that its acceptance criteria are satisfied and required checks have run or have an explicitly accepted gap.
2. Record one outcome-focused history entry when the change warrants durable shipped history. Pure governance or tracking maintenance may omit a product changelog entry.
3. Remove the child from the parent overview instead of retaining a checked row.
4. Archive the implementation spec. Archive a superseded sketch only when its historical reasoning remains useful; otherwise remove it.
5. Keep the main plan's forward-work pointer until the whole flow is complete.

## Flow Closeout

When a main plan is complete:

1. Confirm that no child or acceptance criterion remains unshipped.
2. Update evergreen documentation with any stable current-system contract that must remain discoverable. Do not copy plan history into the evergreen document.
3. Archive the main plan.
4. Remove its active or queued forward-work pointer and preserve the consumer's required empty-section marker, if any.
5. Record the delivered outcome in the shipped-history owner. Do not retain a Done list in the tracker or plan.

## Superseded Work

- Archive a superseded plan, sketch, or spec and add a short pointer to the replacing decision or artifact when that relationship remains useful.
- Remove its active pointer or replace it with the single pointer to the new owner.
- Never leave old and new executable handoffs active for the same scope.

## Final Verification and Report

1. Search the tracker, parent plan, and active plan directory for stale pointers or competing authorities.
2. Run the consuming project's applicable documentation and governance checks from `core/agent_rules/lint_before_finish.md`.
3. Inspect the final diff and keep unrelated user changes out of the closeout scope.
4. Report the newly available outcome, durable architecture or schema decisions, checks that ran, migration version when applicable, and explicitly deferred work.

Lead with observable results rather than a list of edited files.
