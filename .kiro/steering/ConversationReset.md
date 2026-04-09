---
inclusion: manual
---

<instructions>
Execute the Conversation Reset Protocol when the conversation context becomes too long. Save the current project state by reading, clearing, and rewriting the designated state files from scratch. Maintain all rule and steering files exclusively within `KiroWorkingSpace/.kiro/`.
</instructions>

<target_files>
Read these files to understand the state upon starting a fresh session. Update these exact files when resetting:
1. `KiroWorkingSpace/.kiro/docLastConversationState.md`
2. `KiroWorkingSpace/.kiro/ProjectRules.md`
</target_files>

<workflow>
1. Read the files listed in `<target_files>` to capture the current project state.
2. Clear the existing contents of each file completely.
3. Rewrite each file from scratch to reflect the most up-to-date context, rules, and objectives.
</workflow>

<examples>
<example>
<input>Conversation context is degrading due to length.</input>
<expected_behavior>Read `docLastConversationState.md` to grasp current progress. Clear its contents. Write a new, concise summary of the latest completed tasks and pending blockers. Repeat this overwrite process for the remaining three files. Initialize fresh session.</expected_behavior>
</example>
</examples>