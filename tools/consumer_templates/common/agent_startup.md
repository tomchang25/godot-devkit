# Agent Startup

## Required Startup

Read `dev/foundation/core/agent_rules/foundation_startup.md`, the `{{PLATFORM}}` platform startup, and the selected profiles before this file. This file is the authoritative project-local startup layer for {{PROJECT_NAME}}.

## Project Snapshot

{{PROJECT_NAME}} is a `{{PLATFORM}}` consumer using {{PROFILES}}. Extend this section with the product snapshot, effective project root, repository structure, runtime owners, and toolchain facts that agents need before project work.

## Required Operation Contracts

- Read `dev/agent_rules/git_operations.md` before any Git mutation or when Git state is unreliable.
- Read `dev/agent_rules/test_operations.md` before running any test, build, import, screenshot, smoke, or other platform validation operation.

## Project-Local Discovery

Read additional files under `dev/agent_rules/`, `dev/standards/`, `dev/workflows/`, `dev/skills/`, and `dev/docs/` when their trigger applies. Add project-specific trigger links here without copying shared foundation rules.
