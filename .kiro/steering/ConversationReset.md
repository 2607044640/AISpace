---
inclusion: manual
---

<instructions>
Execute the Conversation Reset Protocol when the conversation context becomes too long. Save the current project state by analyzing recent progress, clearing, and rewriting the designated state files from scratch. Maintain all rule and steering files exclusively within `KiroWorkingSpace/.kiro/`.
</instructions>

<target_files>
Read these files FIRST to understand the baseline state before updating:
1. `KiroWorkingSpace/.kiro/docLastConversationState.md`
2. `KiroWorkingSpace/.kiro/ProjectRules.md`
</target_files>

<workflow>
1. READ FIRST: Read the files listed in `<target_files>` to establish the baseline project state.
2. THINK SECOND: Execute `mcp_sequential_thinking_sequentialthinking` to synthesize the baseline state with the recent conversation history.
3. Build Knowledge Inventory: What new tasks were completed since the last state update? Current phase? Pending blockers? Architectural decisions?
4. Identify Blind Spots: Are there unrecorded decisions, temporary workarounds, or new technical debt?
5. Assign Confidence Score (1-10). If < 7: STOP. Ask the user for clarification before proceeding.
6. ACT THIRD: If Confidence Score is >= 7, clear the existing contents of each target file completely.
7. REWRITE: Rewrite each file from scratch to reflect the newly synthesized, up-to-date context, rules, and objectives.
</workflow>

<core_rules>
<rule>
  <description>ALWAYS read `<target_files>` BEFORE executing `mcp_sequential_thinking_sequentialthinking`.</description>
  <rationale>The AI must ground its thinking in the current saved state, not just degraded conversation memory.</rationale>
</rule>
<rule>
  <description>ALWAYS verify Confidence Score >= 7 before clearing any files.</description>
  <rationale>Ensures sufficient understanding of the project state to prevent irreversible loss of critical information.</rationale>
</rule>
</core_rules>

<examples>
<example>
<input>Conversation context is degrading due to length. Please reset.</input>
<expected_behavior>
1. Read `docLastConversationState.md` and `ProjectRules.md` to get baseline.
2. Execute sequential thinking.
3. Knowledge Inventory: Synthesize baseline with recent tasks, pending blockers, etc.
4. Blind Spots: Identify unrecorded decisions or workarounds.
5. Confidence check: Score is 8/10.
6. Clear contents of target files.
7. Write concise, updated summaries preserving all critical information.
8. Initialize fresh session.
</expected_behavior>
</example>
</examples>