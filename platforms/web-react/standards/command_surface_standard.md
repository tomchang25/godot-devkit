# Command Surface Standard

Platform: Web React.

This standard is the canonical owner of the npm script vocabulary, the aggregate verification contract, and the shared formatter configuration for Web game consumers. Concrete tool selection (bundler, linter, boundary checker, test runner) remains project-owned; the names and semantics of the scripts are not. Executable environment detail and pass criteria remain owned by the consumer's `test_operations.md`.

## Required Scripts

Every consumer's `package.json` provides at least:

- `dev` — start the local development server.
- `build` — produce the production output in `dist/`.
- `verify` — the single aggregate gate described below.
- `format` — apply canonical formatting to the repository.
- `test` — run the unit suite once.

Additional project scripts (such as `test:e2e`, watch modes, or shell wrappers) are welcome, but they must not fork or dilute the meaning of the required names. A script named `check` must not exist as an alternate aggregate gate.

## The `verify` Contract

`npm run verify` is the one command that answers "is this change deliverable". It runs these stages in order and stops on the first failure:

1. Format check (formatter in check mode, no writes).
2. Typecheck (the TypeScript compiler with no emit).
3. Lint.
4. Boundary check (the machine-checked import boundaries required by the Web project structure standard).
5. Unit tests.
6. Production build.

A project may prepend a governance or consumer-verification stage before stage 1. Browser acceptance suites stay outside `verify` in their own script because of their runtime cost; the consumer's `test_operations.md` states when they are required.

A stage's result is the exit status of its command. Piping a stage through a filter that replaces that exit status discards the failure signal and is forbidden inside `verify`.

## Formatting

The canonical formatter is Prettier with this shared configuration, stored as `prettier.config.mjs`:

```js
export default {
  endOfLine: "lf",
  printWidth: 120,
  proseWrap: "preserve",
  semi: true,
  singleQuote: false,
  tabWidth: 2,
  trailingComma: "all",
  useTabs: false,
};
```

Consumers do not fork these settings per project. A project that genuinely needs a deviation records it as an explicit addendum naming this standard and the reason.
