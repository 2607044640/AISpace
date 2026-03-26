---
inclusion: manual
---
# Gemini Update Report Generator

<trigger_phrases>
- "Generate Gemini report"
- "Create update for Gemini"
- "Summarize for Gemini"
</trigger_phrases>

<instructions>
Generate a status report to `KiroWorkingSpace/.kiro/TempFolder/GeminiReport_YYYY-MM-DD.md`.

Extract context from the following sources:
- Current conversation history
- `docLastConversationState.md`
- `KiroWorkingSpace/.kiro/TempFolder/` task notes
- Modified files in the current session

Prioritize the "Questions for Gemini" section to maximize value. 
Format the report exactly as specified in `<report_template>`.
</instructions>

<report_template>
# Gemini Update Report
**Date:** YYYY-MM-DD
**Focus:** [Main system/feature worked on]

## Changes Implemented
- [File path]: [Specific addition/refactor/fix]

## Technical Decisions
- [Pattern/Architecture/Library/Optimization]: [Reason/Version/Approach]

## New Dependencies
- [Dependency name] (v[version]) - [Purpose]

## Questions for Gemini
1. [Specific technical implementation question]
2. [Best practices research request]
3. [Alternative approaches to evaluate]
4. [Performance/security concerns to investigate]
5. [Latest updates on dependencies/tools]

## Current State
- **Working:** [What is currently functional]
- **In Progress:** [What is being actively developed]
- **Planned:** [Next immediate steps]
- **Tech Debt:** [Known issues or shortcuts taken]
</report_template>

<examples>
<example>
<section>Changes Implemented</section>
<content>
- `MovementComponent.cs`: Add gravity (9.8f) and jump physics
- `AnimationControllerComponent.cs`: Implement FSM with 5 states
- `Player3D.tscn`: Integrate PhantomCamera3D for third-person view
</content>
</example>

<example>
<section>Technical Decisions</section>
<content>
- Composition over Inheritance: Avoid deep hierarchies, enable component reuse
- PhantomCamera plugin (v2.x): GDScript camera with C# wrapper, collision detection
- Event-driven communication: Components emit `Action<T>`, subscribe in `OnEntityReady()`
</content>
</example>

<example>
<section>Questions for Gemini</section>
<content>
1. Godot C# composition pattern vs Unity ECS - performance comparison?
2. PhantomCamera alternatives for Godot 4.6? Any newer solutions?
3. Event-driven components - memory leak risks with C# events in Godot?
</content>
</example>
</examples>