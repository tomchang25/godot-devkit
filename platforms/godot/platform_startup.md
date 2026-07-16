# Godot Platform Startup

Load this file after `core/agent_rules/foundation_startup.md` when the consuming project selects the `godot` platform. This layer owns Godot, GDScript, serialized scene, autoload, engine UI, and engine-validation contracts. It does not redefine the core work lifecycle or shared artifact workflows.

## Platform Triggers

- Before touching any GDScript file, read `dev/foundation/platforms/godot/standards/gdscript_structure_standard.md` and `dev/foundation/platforms/godot/standards/naming_conventions.md`.
- Before creating or restructuring scenes, node references, or runtime children, read `dev/foundation/platforms/godot/standards/scene_node_source_standard.md` and, for reusable components, `dev/foundation/platforms/godot/standards/component_scene_standard.md`.
- Before changing navigation, settings, debug behavior, error guards, registries, theme, or audio, read the matching standard and skill below `dev/foundation/platforms/godot/`.
- Before changing a Godot state-machine implementation, read `dev/foundation/platforms/godot/skills/state_machine_pattern.md` plus any selected profile or project-local addendum.
- Before diagnosing import, UID, or cross-OS filesystem failures, read `dev/foundation/platforms/godot/skills/godot_cross_os_mount_hazard.md` and the consuming project's sandbox rules.

## Verification Boundary

The platform provides engine-specific standards and hazard cards. The consuming project owns concrete lint, import, test, screenshot, and build commands because Godot versions, addons, filesystem environments, and test harnesses differ.

A dedicated Godot command may live below `platforms/godot/workflows/commands/` when it becomes shared by multiple consumers. Platform commands extend the available operations; they never fork a core workflow.
