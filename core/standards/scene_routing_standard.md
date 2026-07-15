# Scene Routing Standard

This document defines how consumer-project scene transitions are registered and executed.

---

# 1. Ownership

`SceneRouter` is the only owner of normal scene transitions. A boot coordinator such as `GameManager` owns boot orchestration only and must not hold scene tables, payload hand-off, or direct gameplay navigation APIs.

Use `SceneRouter.go_to(...)` or a narrow project wrapper such as `SceneRouter.go_to_start_page()` from scenes and systems. Use `SceneRouter.consume_payload()` once from the arriving scene when a transition carries data.

---

# 2. Route Registration

Routes live in the `SceneRegistry` resource embedded in `global/autoloads/scene_router/scene_router.tscn`.

The base registry must include:

- `start_page` — project entry menu.
- The gameplay route named by `SceneRegistry.default_route`.
- `test_runner` — unit-test route used by `--test-unit`.

Add stable route keys that name intent rather than file paths, such as `hub`, `inventory`, or `combat_arena`. Prefer small wrappers on `SceneRouter` for production routes that are called from multiple places.

Preset overlays may replace `scene_router.tscn` to change the default route or add project/template-specific routes. Do not replace `scene_router.gd` unless the router behavior itself changes for every project using that overlay.

---

# 3. Navigation API

Preferred calls:

```gdscript
SceneRouter.go_to_default()
SceneRouter.go_to_start_page()
SceneRouter.go_to(&"detail", {"entity_id": entity.entity_id})
```

Payloads are one-shot hand-offs. The arriving scene owns consumption:

```gdscript
func _ready() -> void:
    var payload: Variant = SceneRouter.consume_payload()
    if payload is Dictionary:
        _load_payload(payload)
```

Do not store long-lived gameplay state in navigation payloads.

---

# 4. Forbidden Patterns

- Do not call `get_tree().change_scene_to_file()` or `get_tree().change_scene_to_packed()` from gameplay scenes except isolated testbeds that intentionally bypass project routing.
- Do not add `GameManager.go_to(...)` or reintroduce scene tables into `GameManager`.
- Do not preload navigable scenes at call sites just to transition to them.
- Do not duplicate route strings across callers when a `SceneRouter.go_to_*()` wrapper would make the intent clearer.

---

# 5. Review Checklist

- New navigable scene is registered in `scene_router.tscn`.
- Caller uses `SceneRouter`.
- If payload is used, the arriving scene consumes it once and handles missing/invalid payload gracefully.
- `--test-unit` still routes through `SceneRouter.go_to_test_runner()`.
- Preset-specific default-route changes replace the registry scene, not `project.godot`'s `run/main_scene` or the shared router script.
