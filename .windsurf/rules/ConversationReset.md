---
trigger: manual
---

<instructions>
Execute the Conversation Reset Protocol when the conversation context becomes too long or degraded. The goal is to save the current project state and preserve architectural rules without losing critical context.
</instructions>

<target_files>
Read these files FIRST to understand the baseline state before updating:
1. `AISpace/docLastConversationState.md` (State tracking)
2. `AISpace/ProjectRules.md` (Hard constraints)
3. Recent Changes: `Get-Content "C:\Users\26070\My Drive\Kiro_Godot_Brain\AI_Context_Changes.md" -Head <lines>`
</target_files>

<workflow>
1. READ FIRST: Read the files listed in `<target_files>` to establish the baseline project state.
2. THINK SECOND: Execute `mcp_sequential_thinking_sequentialthinking` to synthesize the baseline state with the recent conversation history.
3. Build Knowledge Inventory: What new tasks were completed? Current phase? Pending blockers? New architectural decisions?
4. Assign Confidence Score (1-10). If < 7: STOP. Ask the user for clarification before proceeding.
5. ACT THIRD (STATE RESET): If Confidence >= 7, completely clear `docLastConversationState.md` and rewrite it from scratch with the latest snapshot (Completed, Pending, Next Steps).
6. ACT FOURTH (RULE PRESERVATION): NEVER clear `ProjectRules.md`. Only APPEND or AMEND it if new project-specific hard constraints were established. 
</workflow>

<core_rules>
<rule>
  <description>ALWAYS differentiate between State and Rules during a reset.</description>
  <rationale>`docLastConversationState.md` is a disposable snapshot that should be completely rewritten. `ProjectRules.md` is the structural constitution that must only be appended to or gently amended.</rationale>
</rule>
</core_rules>