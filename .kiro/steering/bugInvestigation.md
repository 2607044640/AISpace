---
inclusion: manual
---
<context>
Purpose: Defines strict investigation steps and escalation paths for bug fixing.
</context>

<instructions>
<investigation_workflow>
Read error logs completely before attempting any fixes.
Add targeted debug logging to isolate the failure point.
Apply and test exactly one change per iteration.
Verify compilation successfully passes after every modification.
</investigation_workflow>

<escalation_triggers>
Halt all code modification attempts and escalate immediately if you encounter:
- 3 consecutive failed fix attempts for the same issue (Three-Strike Rule).
- Unclear error messages lacking official documentation.
- Suspected Godot engine or OS platform bugs.
- Deadlocks or timing issues without an obvious root cause.
</escalation_triggers>

<three_strike_execution>
When an escalation trigger is met:
1. Stop generating code fixes immediately.
2. Fill out the template provided in <query_template> with the current context.
3. Output the completed template inside a standard markdown code block so the user can copy it.
</three_strike_execution>
</instructions>

<query_template>
# Bug Report for Gemini

## Environment
- Engine: Godot 4.6.1 stable mono
- Language: C#
- OS: Windows

## Problem
[Provide a precise, one-sentence description of the issue]

## What I Tried
1. [First attempt methodology and exact result]
2. [Second attempt methodology and exact result]
3. [Third attempt methodology and exact result]

## Current Code
```csharp
[Insert the specific, relevant C# code block causing the issue]