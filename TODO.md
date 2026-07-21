# TODO

The single forward surface: open this file to see every open item and emerging idea. Each forward item lives in exactly one section here. There is deliberately no Done tier: remove shipped lines and record their outcome in `CHANGELOG.md`.

> The actionable tiers (`Plan`, `Chore`, and `Bug`) contain one line per item: no paragraphs, tables, or rationale. An item that needs explanation belongs in `## Draft` under one `###` heading. When a Draft item becomes actionable, promote it to `## Plan` as a single line.
>
> In Draft sections, use no `####` headings or bold-label patterns. Use plain text and lists for sub-structure.
>
> Scope tags in actionable lines use short, lowercase `snake_case` identifiers, such as `[core_discovery]` or `[consumer_verify]`.
>
> This repository holds shared governance only. A line here must describe a change to a rule, workflow, standard, skill, or tool — never game-specific paths, domain names, runtime content, or a consuming project's product plan.

Actionable line format: `[scope] one sentence`

`## Active` holds in-flight or implementation-ready work promoted from `## Plan`.

---

## Active

> Do not delete this reminder text.
> Work currently being implemented or ready to implement. Each entry is a one-line pointer in the same format as `## Plan`.
> Ship an item: remove its line and append the outcome to `CHANGELOG.md`.

Nothing currently in progress.

---

## Plan

Queued work with an agreed shape. Promote only the next eligible line to `## Active`.

- [web_platform] Promote or consolidate overlapping Web consumer-local standards into shared governance after both Web consumers complete their 0.7.0 structure migrations
- [core_workflows] Promote the two Draft invariants below (archived-artifact references, verification result determination) once their placement decisions are made alongside that consolidation

---

## Chore

One line, no rationale, no backing document.

---

## Bug

One line, no rationale, no backing document.

---

## Draft

Ideas that need explanation before they can become a one-line item. Use one `###` heading per idea.

### Archived Artifacts Must Not Remain Referenced From Durable Docs

Closeout moves a completed plan and its specs into the archive, and the archive is pruned on a schedule, so any document that must stay authoritative cannot depend on an archived file remaining present. A consuming project has now had a standards file and a forward-tracker item left pointing at a just-archived plan for context that lived only in that plan, which the next prune would break.

The invariant is that a standard, skill, or other durable or evergreen document must never reference an archived artifact, and a still-forward plan, sketch, or spec should avoid it; in both cases closeout must lift the still-needed content and its context into the referencing document rather than leave a pointer into the archive. Closeout already requires updating evergreen documentation with any stable current-system contract that must remain discoverable — this extends that obligation to every durable reader of a closing artifact, not a single evergreen file.

Promoting it requires deciding whether the rule lands in `core/workflows/closeout_standard.md` as a closeout obligation or in `core/standards/governance_structure_standard.md` as a cross-reference constraint, and whether `commands/closeout.md` should scan a closing artifact's inbound references and inline them as part of archival instead of repointing them at the archive.

### Verification Result Determination

`core/standards/consumer_operations_standard.md` requires every consumer's `test_operations.md` to define failure cross-checking and result reporting, which correctly keeps commands and layers project-owned. Core states no invariant for how a result is established, and a consumer has now had to record one locally after an agent reported a browser suite as passing by reading a filtered slice of its output.

The invariant is that a layer's result is the exit status of its command rather than any view of its output, that piping a verification command into a filter replaces that exit status and discards the failure signal, and that a suite's executed, passed, failed, and skipped counts must be reconciled against the total the suite declares before it is called passing. None of that depends on a runner, framework, or platform.

Promoting it requires deciding whether core states the invariant while consumers continue to own commands and layer lists, or whether result determination stays wholly delegated and each consumer restates it. The first option narrows an existing delegation and so must update `consumer_operations_standard.md` in the same change.
