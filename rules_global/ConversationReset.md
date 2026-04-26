---
trigger: manual
---

## Objective
Execute Conversation Reset Protocol to save project state and architectural rules without losing context when conversations degrade.

## Target Files (Read FIRST)
1. `AISpace/docLastConversationState.md` (State tracking)
2. `AISpace/ProjectRules.md` (Hard constraints)
3. `C:\Users\26070\My Drive\Agent_Godot_Brain\AI_Context_Changes.md` (Recent Changes)

## Workflow
1. **READ FIRST**: Read the target files to establish baseline.
2. **THINK SECOND**: Use `mcp_sequential_thinking_sequentialthinking` to synthesize baseline with recent history.
3. **Build Knowledge Inventory**: Note new tasks, current phase, blockers, architectural decisions.
4. **Confidence Score**: Assign (1-10). If < 7: STOP and ask user for clarification.
5. **ACT THIRD (State Reset)**: If >= 7, completely clear and rewrite `docLastConversationState.md` with latest snapshot (Completed, Pending, Next Steps).

<system_reminder>
NEVER clear `ProjectRules.md`. Only APPEND or AMEND it if new project-specific hard constraints were established.
</system_reminder>

<complex_pattern>
  <description>Differentiate State and Rules during reset.</description>
  <rationale>`docLastConversationState.md` is disposable/rewritable. `ProjectRules.md` is the structural constitution.</rationale>
</complex_pattern>