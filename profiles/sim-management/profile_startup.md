# Simulation Management Profile

Use this profile for turn-based, idle, management, or UI-heavy projects where state lives in Stores and mutation is mediated by Managers or Systems.

Project-specific runtime types live in the game-owned domain layer. The reusable layer remains reserved for infrastructure and helpers that can transfer to another game without gameplay-specific changes.

Read the relevant profile standards before changing model ownership, scene data flow, or tutorials:

- `standards/runtime_archetypes.md`
- `standards/store_manager.md`
- `standards/block_scene_data_flow.md`
- `standards/tutorial_standard.md`
- `standards/project_structure.addendum.md`

The project-local layer owns concrete Stores, fixtures, testbeds, save slots, screen flow, and domain terminology.
