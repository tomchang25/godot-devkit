# Action RPG Profile

Use this profile for real-time, spatial, many-entity projects where behavior is distributed across entity and component nodes.

Concrete feature behavior stays with its owning game feature. Only capability components and entity bases whose contracts are independent of a specific feature belong in the reusable layer.

Read the profile standards when changing entity composition or folder ownership:

- `standards/component_architecture.md`
- `standards/project_structure.addendum.md`

The project-local layer owns concrete components, input loops, pooling policy, save points, and gameplay-specific FSMs.
