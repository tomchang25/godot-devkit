# Lint Before Finishing

Before finishing, run the non-mutating verification required by the consuming project for every changed file. The project-local startup and verification rules own the concrete package runner, linter, formatter check, test harness, build command, and sandbox procedure.

## Scope verification to the work

- Documentation-only or tracking-only changes: run the consumer's documentation and governance checks on the changed files. Do not substitute a full application build unless the consumer requires it.
- Source, configuration, serialized artifact, or data changes: run the applicable static checks on every changed file plus the narrowest relevant behavioral test.
- Runtime, persistence, migration, data-loading, or navigation behavior changes: run the focused regression or compatibility checks required by the touched contract.
- Dedicated platform validation is selected by the platform and project layers. Core does not invent an engine, browser, package manager, or test command.

Prefer the smallest verification that proves the touched surface. Do not run broad tests for documentation-only work.

See the consuming project's `dev/agent_rules/test_operations.md`, standards-enforcement contract, and startup document for available commands, active checks, and failure-reporting requirements.
