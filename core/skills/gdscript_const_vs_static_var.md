# GDScript `const` vs `static var` for Built Collections

## Overview

A `const` may only hold a **constant expression** — a value the compiler can fold at parse time (literals, other consts, and `preload`). The moment a collection literal contains a value produced by a _call_ — a constructor, a static factory, a `Callable` reference — it is no longer a constant expression and must be a `static var`, not a `const`.

This bites hardest on **manifest/registry arrays** built from helper calls, because they parse fine in the editor but fail under a **clean headless import** (`rm -rf .godot` + `--import`), which is exactly the path CI and the screenshot/testbed harnesses take.

---

## The failure

```gdscript
# ❌ fails on clean headless import
const REGISTRY: Array[Dictionary] = [
    _entry("storage", "Storage", StorageFixtures.seed_storage_state, SceneRouter.go_to_storage),
]
```

Each `_entry(...)` is a function call, and `StorageFixtures.seed_storage_state` / `SceneRouter.go_to_storage` are `Callable` references — none are constant expressions. The editor's warm cache hides this, but a cold import reports:

```
Assigned value for constant "REGISTRY" isn't a constant expression.
```

The parse error aborts the import, so the autoload never loads and the harness exits before doing anything.

---

## The fix

```gdscript
# ✅ static var — evaluated at class load, calls allowed
static var registry: Array[Dictionary] = [
    _entry("storage", "Storage", StorageFixtures.seed_storage_state, SceneRouter.go_to_storage),
]
```

`static var` is initialized when the class is first loaded rather than folded at parse time, so constructor calls and `Callable` references are legal. It stays a single shared instance, which is what a manifest/registry wants.

---

## When each is correct

| Right-hand side                                             | Use          |
| ----------------------------------------------------------- | ------------ |
| Literal (`42`, `"x"`, `[1, 2]`, `{}`)                       | `const`      |
| Another `const` or an `enum` value                          | `const`      |
| `preload("res://...")`                                      | `const`      |
| A constructor call (`Vector2(...)`, `_entry(...)`)          | `static var` |
| A `Callable` reference (`SomeClass.some_method`)            | `static var` |
| Any array/dict whose **elements** come from the above calls | `static var` |

Rule of thumb: if building the value requires _running code_, it cannot be `const`.

---

## Project application

Registries, testbed manifests, screenshot pilots, and other collections built from factories or `Callable` references must use `static var` for this reason. A consuming project may document concrete examples in its local standards, but the constant-expression rule is universal.
