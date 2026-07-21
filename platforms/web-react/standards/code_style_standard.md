# Code Style Standard

Platform: Web React.

This standard owns TypeScript and TSX control-flow and layout conventions. Formatting configuration is owned by `command_surface_standard.md`; identifier and filename spelling by `naming_conventions.md`. The consumer binds these conventions to its concrete formatter and linter rules and machine-enforces them where its tooling can.

## Control Flow

- Every `if`, `else`, `for`, `for...of`, `for...in`, `while`, and `do...while` body uses braces, including a single statement.
- Use an early return or continue for a simple guard. Do not add an `else` after a branch that always exits.
- Use `if` and `else` for mutually exclusive outcomes that share one decision, keeping the branches aligned and explicit.

## Logical Spacing

- Separate adjacent logical phases in a function with one blank line. Typical phases are guards, input retrieval and validation, deterministic state updates, presentation or asynchronous scheduling, result settlement, and cleanup.
- Keep statements that implement one atomic operation together; do not add blank lines between every declaration, condition, or call merely to create visual space.
- Use a short comment only when a phase boundary is not evident from the code itself.
- Semantic phase boundaries remain a review requirement because a linter cannot reliably infer program intent; do not introduce a blanket blank-line rule that separates every statement.
