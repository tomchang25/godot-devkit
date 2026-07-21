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

---

## Chore

One line, no rationale, no backing document.

---

## Bug

One line, no rationale, no backing document.

---

## Draft

Ideas that need explanation before they can become a one-line item. Use one `###` heading per idea.
