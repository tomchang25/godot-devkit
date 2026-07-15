# Debug Mode Usage

Use this when adding debug-only UI, shortcuts, or diagnostics.

## Check debug state

```gdscript
if not Debug.enabled:
    return
```

Do not check `OS.is_debug_build()` or `SettingsStore.debug_mode` directly from scene/gameplay code.

## React to toggles

```gdscript
func _ready() -> void:
    visible = Debug.enabled
    Debug.toggled.connect(_on_debug_toggled)


func _on_debug_toggled(is_enabled: bool) -> void:
    visible = is_enabled
```

## Add debug-only nodes

```gdscript
if Debug.enabled:
    var button := Button.new()
    button.text = "Debug Action"
    # node-src: debug
    add_child(button)
```

Every debug button handler that mutates game state must guard again:

```gdscript
func _on_debug_action_pressed() -> void:
    if not Debug.enabled:
        return
    _mutate_debug_state()
```

Reusable debug panels may be `.tscn` components only when they are hidden by default, self-gated from `Debug.enabled`, and every mutating handler has the guard above.

## Prefer the shared `DebugPanel` over a one-off block scene

Do not build a new debug block scene from scratch. Instance `res://game/shared/debug_panel/debug_panel.tscn` (`class_name DebugPanel`) in each scene that needs it, keep it hidden by default, and register that scene's actions from `_ready()`:

```gdscript
@onready var _debug_panel: DebugPanel = %DebugPanel


func _wire_debug_panel() -> void:
    _debug_panel.add_action("Complete Current Step", _on_debug_complete_step, "Session")
    _debug_panel.add_action("Grant Test Item", _on_debug_grant_item, "Inventory")


func _on_debug_complete_step() -> void:
    if not Debug.enabled:
        return
    _session_controller.complete_current_step_for_debug()
```

`DebugPanel.add_action()` already wraps the callback with a `Debug.enabled` check, so the button can never fire while debug is off—the guard in the handler is the belt-and-suspenders copy required by `debug_standard.md` §4a, not the only line of defense. See `debug_standard.md` §5 for the full contract.
