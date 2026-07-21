Review the currently git-staged files against any referenced plan spec and the shared review standard.

## Scope

The review scope is staged files only. Do not include unstaged or untracked files unless they are needed as related codebase context.

## Steps

1. Read `core/workflows/review_standard.md` and apply it to the staged-file scope.
2. Run `git diff --cached --name-only` to get staged files.
3. Run `git diff --cached --stat` for a summary.
4. If a plan/spec file is among the staged files under `dev/docs/plans/`, read it as the spec.
5. Read the full current contents of every staged file that can be reviewed as text, then read the staged diff with `git diff --cached -- <file>` to understand the exact staged changes.
6. Search related repository context for changed APIs, constants, identifiers, artifact paths, events, schemas, command workflows, and standards references. Explicitly search for stale names or removed behavior introduced by the staged diff.
7. Run the non-mutating staged-file checks required by `core/agent_rules/lint_before_finish.md` and the consuming project's verification rules for the file types in scope. Do not substitute a platform-specific command that the consumer has not selected.
8. Apply the review standard's robustness cases to the full current contents, not only the changed hunks.
9. Report findings and summary using `core/workflows/review_standard.md`, including the required per-file review summary, stale/redundant result, robustness result, and standards/lint/test result.

## Reporting Language

Follow `core/workflows/review_standard.md`. Keep required verdict labels (`pass`, `needs changes`, `blocked`) in English.
