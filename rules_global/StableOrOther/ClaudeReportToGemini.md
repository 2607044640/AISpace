---
trigger: manual
---

## Objective
Generate a Gemini Update Report when crossing AI boundaries.

## Trigger Phrases
- "Generate Gemini report"
- "Create update for Gemini"
- "Summarize for Gemini"

## Workflow
1. Read current conversation history, `docLastConversationState.md`, and recent task notes in `AISpace/TempFolder/`.
2. Review files modified during the current session.
3. Write the report exactly matching the `<report_template>` to `AISpace/TempFolder/GeminiReport_YYYY-MM-DD.md`.
4. Prioritize the "Questions for Gemini" section to maximize cross-agent value.

<template name="report_template">
<code><![CDATA[
# Gemini Update Report
**Date:** YYYY-MM-DD
**Focus:** [Main system/feature worked on]

## Changes Implemented
- [File path]: [Specific addition/refactor/fix]

## Technical Decisions
- [Pattern/Architecture/Library]: [Reason/Version/Approach]

## Questions for Gemini
1. [Specific technical implementation question]
2. [Best practices research request]
3. [Performance/security concerns to investigate]

## Current State
- **Working:** [What is functional]
- **In Progress:** [What is actively developed]
- **Planned:** [Next immediate steps]
- **Tech Debt:** [Shortcuts taken]
]]></code>
</template>

<complex_pattern>
  <description>Examples of Technical Decisions and Questions</description>
  <rationale>Provides concrete context for the next AI session.</rationale>
  <example>
    Technical Decisions:
    - Composition over Inheritance: Avoid deep hierarchies, enable reuse.
    - PhantomCamera plugin (v2.x): GDScript camera with C# wrapper.
    Questions:
    1. Godot C# composition pattern vs Unity ECS - performance comparison?
    2. Event-driven components - memory leak risks with C# events in Godot?
  </example>
</complex_pattern>