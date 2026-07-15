# pr-review - review branch and generate PR title and description

Review the current branch against the base branch, then generate a pull request title and description.

Steps:

1. Read `dev/workflows/review_standard.md`, `dev/skills/pr_convention.md`, `dev/standards/change_summary_standard.md`, and `dev/skills/conventional_commits.md` if type/scope rules are unclear.
2. Inspect the branch with read-only git: `git log --oneline <base>..HEAD` and `git diff <base>...HEAD --stat` (assume base is `main` unless told otherwise; never stage, commit, or push).
3. Review `git diff <base>...HEAD` using `dev/workflows/review_standard.md` before drafting PR text.
4. Report findings first, ordered by severity, with file/line references when possible. If there are no findings, say so explicitly and mention residual risks or testing gaps.
5. Write the PR title and description (`## Summary`, `## Changes`, plus `## Testing` / `## Breaking changes` / `## Notes` only when applicable).
6. Output the title and description in a single copy-pasteable block. Do not create files or open a PR.

$ARGUMENTS
