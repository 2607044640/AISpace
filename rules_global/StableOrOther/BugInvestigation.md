---
trigger: manual
---

## Quick Reference
- **Tool**: `mcp_sequential_thinking_sequentialthinking`
- **Core Rule**: 3-Strike Rule (Max 3 failed fix attempts before escalation)
- **Engine Context**: Godot 4.6.1 stable mono, C#, Windows

## Decision Tree
- IF Confidence < 7 OR blind spots: ALWAYS trigger web/doc search. (Why: NEVER guess missing facts)
- IF Confidence >= 7 AND search complete: Proceed with execution.
- IF 3 consecutive fails for same issue: Check `AISpace/hardbugs/` directory for historical solutions. If no solution is found, HALT and escalate. (Why: Prevents infinite loops while leveraging past fixes)
- IF deadlocks, timing issues, Godot/OS bugs: Check `hardbugs/`, then HALT and escalate.

## Implementation Workflow
1. Execute `mcp_sequential_thinking_sequentialthinking` to catalog Knowledge Inventory.
2. Pinpoint blind spots and assign Confidence Score (1-10).
3. Trigger search if Confidence < 7.
4. Read error logs completely; add targeted debug logging.
5. Apply EXACTLY ONE change per iteration and verify compilation.

## Best Practices
- Delete documentation ruthlessly if it's generic programming advice.
- Implement and verify functionality incrementally.
- Save permanent docs, steering files, and specs strictly outside the Scratchpad directory.

<system_reminder>
ALWAYS halt execution and output the Escalation Template upon meeting any escalation trigger. System-level issues or unsolvable state loops require human intervention.
</system_reminder>

<template name="escalation_query_template">
<code><![CDATA[
# Bug Report for Gemini

## Environment
- Engine: Godot 4.6.1 stable mono | C# | Windows

## Problem
[Provide a precise, one-sentence description of the issue]

## What I Tried
1. [First attempt methodology and exact result]
2. [Second attempt methodology and exact result]
3. [Third attempt methodology and exact result]

## Current Code
```csharp
[Insert specific, relevant C# code block]
```

## Error Logs
[Paste complete error output from Godot console or dotnet build]

## Question
[Specific aspect needing clarification or alternative approach?]
]]></code>
</template>
