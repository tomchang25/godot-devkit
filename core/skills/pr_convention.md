# Pull Request Convention

A lightweight convention for PR titles and descriptions. Extends `conventional_commits.md` and `dev/standards/change_summary_standard.md`; read those first. This document only covers PR-level differences.

## Title

The PR title follows the same format as a commit subject line:

```text
<type>[optional scope][!]: <description>
```

- Use the same types, scopes, and `!` breaking-change marker as `conventional_commits.md`.
- Describe the PR as a whole, not its largest commit.
- If the PR mixes types, pick the type of the primary change.
- The title becomes the squash-merge commit subject, so it must stand alone in the git log: imperative mood, no trailing period, ideally 72 characters or fewer.

## Description

Use these sections in this order. `## Summary` and `## Changes` are required; the rest appear only when useful.

### `## Summary`

Write 1-3 sentences explaining what changed and why. Lead with the problem or goal, not the implementation.

### `## Changes`

Summarize the logical changes the PR makes. Use prose for simple PRs or a bullet list with one logical change per `-` bullet. Summarize logical changes, not commits; the two do not need to map 1:1.

For large PRs, group changes under `###` subheadings inside `## Changes`. Default to grouping by area or module because that usually matches how a reviewer reads the diff.

### `## Testing`

List commands run and any meaningful manual verification. If no tests were run, say so and explain why.

### `## Breaking changes`

Required whenever the title carries `!` or any commit has a `BREAKING CHANGE:` footer. State what breaks and the migration path.

### `## Notes`

Optional reviewer context: known limitations, follow-up work, review focus areas, or screenshots for UI changes.

## Rules

- Follow `dev/standards/change_summary_standard.md` for tone, content, and administrative-housekeeping exclusions.
- Do not paste the commit list as the description.
- Do not hard-wrap prose at a column boundary.
- Reference issues/plans with closing keywords where supported, such as `Closes #123`, at the end of the Summary rather than as a separate section.

## Example

```text
feat(scene_routing): validate route payloads before transitions

## Summary

Scene transitions now validate route IDs and payload shape before attempting to change scenes, making navigation failures easier to diagnose during development.

## Changes

- Add route payload validation before scene changes
- Surface invalid route feedback through the debug gate
- Cover invalid route IDs in routing tests

## Testing

- `python dev/tools/lint_standards.py --root .`
- `godot_console --headless --path . --test-unit` from a safe snapshot
```
