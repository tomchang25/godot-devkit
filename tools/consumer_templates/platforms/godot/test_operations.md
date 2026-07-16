# Test Operations

This file is the authoritative project-local test and Godot validation contract for {{PROJECT_NAME}}. Every agent-run test, import, headless check, screenshot, smoke test, or build validation must follow this file.

## When To Run

Use the narrowest available layer that proves the changed behavior. Documentation-only work does not require Godot execution unless the project declares otherwise.

## Environment And Preparation

No project-specific Godot binary, working-tree safety decision, snapshot procedure, generated-output setup, or dependency installation command is declared by the scaffold. Agents must not invent these details. Record the real environment contract here before enabling automated Godot execution.

## Available Layers

No automated Godot layer is enabled by the scaffold. Declare each available static, import, headless, unit, integration, smoke, screenshot, or build layer here. Mark runtime, visual, timing, animation, input, or other unautomated behavior as manual-only when applicable.

## Commands And Pass Criteria

No project-specific command is declared by the scaffold. For every enabled layer, provide its canonical command, setup boundary, timeout or polling behavior, pass criteria, expected noise, and failure cross-check procedure.

## Result Reporting

Report every layer actually run, the source state tested, the pass/fail result, any expected noise that affected interpretation, and every verification gap or manual-only boundary.
