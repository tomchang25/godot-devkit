# Change Summary Standard

Use this standard whenever summarizing completed work in commit messages, review notes, PR titles/descriptions, CHANGELOG entries, closeout output, or other post-cleanup summaries.

## Core Rule

Describe the durable outcome, not the paperwork or step-by-step mechanics.

- Prefer one compact, general summary when it accurately covers the shipped work.
- Split into multiple bullets only when the work contains clearly separate user-visible, system-visible, or rule-visible outcomes that would be misleading if combined.
- Keep summaries plain, concise, and outcome-focused.
- Avoid hype language, speculative performance claims, and implementation mechanics unless the implementation detail is necessary to identify the behavior or fix.
- Do not list file-by-file edits, command executions, TODO updates, CHANGELOG updates, plan archival, or closeout bookkeeping unless that process artifact is the primary product of the change.

## Scope By Artifact

- Commit subject: conventional style, imperative or concise outcome phrase, no trailing period.
- Commit body: 0-3 bullets by default, each bullet describing one logical outcome.
- PR title: conventional style, describing the PR as a whole rather than its largest commit.
- PR description: summarize logical changes, not the raw commit list.
- Review findings: state behavior risks, regressions, missing tests, or standards violations first; include file/line references when possible.
- CHANGELOG entry: record the shipped outcome under the current version; do not include commit refs or process-only maintenance.
- Closeout summary: report documentation cleanup separately from the change summary; do not make archive/TODO/CHANGELOG work sound like product work.

## Examples

Good commit body:

```text
- Add route payload validation to SceneRouter transitions
- Surface invalid route IDs through the debug gate
```

Bad commit body:

```text
- Edited scene_router.gd
- Updated TODO.md and archived the plan
- Ran closeout
```

Good CHANGELOG entry:

```text
- 2026-06-28 - [scene_routing] SceneRouter now reports invalid route IDs before attempting a transition
```

Bad CHANGELOG entry:

```text
- 2026-06-28 - [scene_routing] Modified SceneRouter, updated tests, changed TODO, and moved plan files
```

Good PR Changes section:

```text
- Add route payload validation before scene changes
- Gate invalid route feedback through Debug so release builds stay quiet
```

Bad PR Changes section:

```text
- Commit abc123: add validation helper
- Commit def456: update docs
- Commit fedcba: closeout
```
