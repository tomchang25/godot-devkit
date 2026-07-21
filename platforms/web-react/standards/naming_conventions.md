# TypeScript and React Naming Conventions

Platform: Web React.

- Directory names use `kebab-case`.
- A directory that groups a concept uses a singular name (`content/`, `model/`, `test/`); only a directory whose children are variants or instances of one thing uses a plural name (`enemies/`, `ports/`). Repository root directories are always singular — a plural root directory signals an instance collection that belongs under a narrower owner; see the Web project structure standard.
- TypeScript source files use `kebab-case.ts`; files that contain JSX use `kebab-case.tsx`. This includes files whose primary export is a `PascalCase` class or component: the export keeps its `PascalCase` name while the file stays `kebab-case` (`game-runtime.ts` exporting `GameRuntime`).
- React components and exported types use `PascalCase`.
- Functions, variables, parameters, and object properties use `camelCase` unless an external schema requires another spelling.
- Hooks use `useXxx` and follow React's hook rules.
- Module-level immutable constants use `UPPER_SNAKE_CASE` only when they represent stable constants rather than ordinary local values.
- CSS Module class names use `camelCase`.
- Test files use `<subject>.test.ts` or `<subject>.test.tsx` unless the consumer's selected test runner requires another discoverable suffix.
- A file whose kind matters to a runner, loader, or reader declares that kind as a dotted role suffix: `<name>.<role>.<ext>`. Shared roles are `.test` (unit tests), `.spec` (browser acceptance tests), `.scenario` (harness scenarios), `.module.css` (CSS Modules), and `.addendum.md` (project addenda to a shared standard). Roles are singular. Filenames produced or consumed by an asset pipeline are owned by that pipeline's dedicated asset standard and are exempt from this list.
- A content or content-contract file is named `<domain>-<role>.ts` with a singular domain and an explicit role suffix: `-definitions` for authored records, `-catalog` for assembled catalog access, `-schema` for content contracts, `-validation` for validation. Bare domain-noun data files (`ports.ts`) are not used; the role is always visible in the name.
- Persisted keys and domain identifiers remain stable after release; renaming a code symbol does not silently rename persisted or authored identifiers.

Avoid vague owners such as `Manager`, `Helper`, or `Utils`. When a runtime gateway uses `System`, `Store`, `Service`, or another architectural noun, its canonical standard or project addendum must define the responsibility.
