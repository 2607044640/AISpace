---
inclusion: manual
---
<bug_investigation_rules>
  <layer_1_quick_start>
    <quick_reference>
      - Tool: `mcp_sequential_thinking_sequentialthinking`
      - Core Rule: Three-Strike Rule (Maximum 3 failed fix attempts before escalation)
    </quick_reference>
    
    <decision_tree>
      - IF Confidence Score < 7 OR core concepts are blind spots:
        - ACTION: ALWAYS trigger web search or documentation lookup. (Why: NEVER guess missing facts to prevent hallucinations.)
      - IF Confidence Score >= 7 AND search is complete:
        - ACTION: Proceed with execution. (Why: High confidence threshold met.)
      - IF 3 consecutive fix attempts fail for the same issue:
        - ACTION: Halt execution and escalate immediately. (Why: Prevents infinite loops and wasted context tokens.)
      - IF encountered deadlocks, timing issues, or suspected Godot/OS bugs:
        - ACTION: Halt execution and escalate. (Why: Out of scope for standard logical bug fixing.)
    </decision_tree>
    
    <top_anti_patterns>
      <rule>
        <description>NEVER apply multiple changes per iteration.</description>
        <rationale>Simultaneous changes mask the root cause and make compilation failures harder to isolate.</rationale>
      </rule>
      <rule>
        <description>NEVER attempt a code fix before completely reading all error logs.</description>
        <rationale>Partial context leads to incorrect assumptions and improper fixes.</rationale>
      </rule>
    </top_anti_patterns>
  </layer_1_quick_start>

  <layer_2_detailed_guide>
    <api_reference>
      - Tool: `mcp_sequential_thinking_sequentialthinking`
      - Purpose: Enforces mandatory logic sequence prior to executing any fixes.
    </api_reference>

    <implementation_guide>
      <step>Execute `mcp_sequential_thinking_sequentialthinking` to catalog Knowledge Inventory (explicit known facts).</step>
      <step>Pinpoint Blind Spots (missing, unfamiliar, or uncertain concepts).</step>
      <step>Assign a Confidence Score (1-10). Trigger search if < 7.</step>
      <step>Read error logs completely and add targeted debug logging to isolate the failure point.</step>
      <step>Apply EXACTLY ONE change per iteration and verify compilation passes successfully after the modification.</step>
    </implementation_guide>

    <technical_specifications>
      - Engine Target: Godot 4.6.1 stable mono
      - Language Target: C#
      - OS Target: Windows
    </technical_specifications>

    <core_rules>
      <rule>
        <description>ALWAYS halt code modification and output the Escalation Template upon meeting any escalation trigger.</description>
        <rationale>Escalation triggers indicate system-level issues or unsolvable state loops that require human intervention.</rationale>
      </rule>
    </core_rules>

    <code_templates>
      <template name="escalation_query_template">
        <code><![CDATA[
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