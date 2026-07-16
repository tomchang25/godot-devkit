# Sketch Standard

Use this standard to produce an exploratory child document between a plan and an implementation spec. A sketch is a thinking and decomposition artifact: it can record a candidate implementation shape, relevant codebase context, risks, and sequencing notes before the final spec is written.

A sketch is not an executable handoff. It records provisional implementation-facing context, risks, and candidate shapes; the implementation spec author verifies or replaces every codebase claim against the current codebase.

## Use This For

- A plan child that needs implementation-facing thought before it is ready for a verified spec.
- A risky seam where the plan's durable design is clear, but the likely code movement needs discussion.
- A handoff from design discussion to the later spec author, especially when multiple candidate shapes were considered.

Do not use this for:

- Final implementation handoff. Use an implementation spec.
- Durable product/design intent. Use a plan.
- Early problem observation with no chosen direction. Use a probe.
- Trivial bug fixes or chores. Use a compact implementation note.

## Output Structure

The first line under the title is always the parent marker:

```md
Parent Plan: `<plan_filename.md>`
```

For standalone sketches, write:

```md
Parent Plan: none (standalone sketch)
```

### 1. Goal

One to three sentences: what slice of the parent plan this sketch explores and why that slice exists.

### 2. Summary

Optional but encouraged. Capture the current conclusion of the design or codebase discussion in a scannable shape: short paragraphs, context-specific bullets, or a compact table when comparison matters. This is not an approval surface for implementation; the later spec owns final approval. Do not force a fixed heading template, but make it clear why this slice exists, what direction is currently favored, what the later spec must verify, and what the expected outcome is if the sketch holds up.

### 3. Requirements (standalone sketch only)

Most sketches are plan children and omit this section because the parent plan owns requirements. Include Requirements only if the sketch temporarily stands alone before a plan is written.

### 4. Sketch

The main body. Use prose, bullets, or small tables as useful.

Allowed:

- Candidate implementation shapes and trade-offs.
- Codebase evidence gathered so far, including file paths, class names, method names, fields, and high-level call relationships.
- Risks, seams, and wrong shapes the later spec author should inspect.
- Notes about what likely belongs in the final spec's Relational Context or Files to Change.

Required framing:

- Treat every codebase claim as provisional. Use language like "likely", "candidate", or "verify" when the claim has not been freshly checked.
- Do not present a Files to Change table as final. If listing likely files helps, label it `Candidate files to inspect`.
- Do not write instructions that assume the later implementation agent will execute the sketch directly.

### 5. Non-Goals

Numbered list of exclusions, especially things that are tempting to fold into the later spec but belong to another child or plan.

### 6. Acceptance Criteria

Numbered behavioral outcomes copied or sliced from the parent plan. Keep them observable and code-coordinate free.

## Rules

1. Write entirely in English.
2. No open questions; unresolved decisions are resolved in conversation before the sketch is handed off. If the goal is to preserve unresolved discussion, write a probe instead.
3. The first line under the title is `Parent Plan: ...`; use the parent plan filename for plan children and `Parent Plan: none (standalone sketch)` for standalone sketches.
4. Do not hard-wrap prose lines. Tables and code blocks are exempt.
5. Sketches may include codebase context, but they do not create implementation authority. The later spec-time codebase read wins every disagreement.
6. Requirements live in the parent plan whenever there is one; the sketch slices and interprets them but does not duplicate the source of truth.
7. Keep future scope out. If another child owns it, put it in Non-Goals or leave it in the parent plan.

## Lifecycle

- Plan-child sketches live at `dev/docs/plans/<parent_scope>_<NN>_<slug>.sketch.md` and are pointed to only from the parent plan's child overview table; they get no separate `TODO.md` line. For non-trivial plan children, this is the default child artifact before the implementation spec.
- A sketch becomes actionable by being rewritten into a sibling implementation spec named `dev/docs/plans/<parent_scope>_<NN>_<slug>.implementation_spec.md`. The spec may replace the sketch file or live alongside it only while the conversation needs both; before implementation handoff, the parent plan should point to the spec.
- When the child ships, archive the spec and cut the child from the parent plan. Archive or delete the sketch if it still exists.

## Template

```md
# <Title>

Parent Plan: `<plan_filename.md>` <!-- or: Parent Plan: none (standalone sketch) -->

## Goal

<One to three sentences.>

## Summary

<Optional current conclusion in short paragraphs, context-specific bullets, or a compact table. Avoid fixed boilerplate headings.>

## Requirements

<Standalone sketches only. Omit for plan children.>

## Sketch

- <Candidate implementation shape, codebase context, risk, or seam to inspect.>
- <Use provisional language for unverified claims.>

## Non-Goals

1. <Explicit exclusion.>
2. <Explicit exclusion.>

## Acceptance Criteria

1. <Observable outcome.>
2. <Observable outcome.>
```
