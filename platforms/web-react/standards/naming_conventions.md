# TypeScript and React Naming Conventions

Platform: Web React.

- TypeScript source files use `kebab-case.ts`; files that contain JSX use `kebab-case.tsx`.
- React components and exported types use `PascalCase`.
- Functions, variables, parameters, and object properties use `camelCase` unless an external schema requires another spelling.
- Hooks use `useXxx` and follow React's hook rules.
- Module-level immutable constants use `UPPER_SNAKE_CASE` only when they represent stable constants rather than ordinary local values.
- CSS Module class names use `camelCase`.
- Test files use `<subject>.test.ts` or `<subject>.test.tsx` unless the consumer's selected test runner requires another discoverable suffix.
- Persisted keys and domain identifiers remain stable after release; renaming a code symbol does not silently rename persisted or authored identifiers.

Avoid vague owners such as `Manager`, `Helper`, or `Utils`. When a runtime gateway uses `System`, `Store`, `Service`, or another architectural noun, its canonical standard or project addendum must define the responsibility.
