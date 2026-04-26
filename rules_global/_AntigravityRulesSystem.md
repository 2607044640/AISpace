---
trigger: manual
---

## Objective
Guide for Antigravity-specific rules infrastructure, triggers, and file paths.

## Architecture Overview
- **Global Rules (`GEMINI.md`)**: Located at `~\.gemini\GEMINI.md`. Applies across ALL workspaces.
- **Workspace Rules (`.agents\rules\`)**: Located at `C:\Godot\TetrisBackpack\.agents\rules\`. Applies to current project.
- **Single Source of Truth**: Edit in `C:\Godot\AISpace\rules_global\`. Hardlinks replicate edits instantly to `.agents\rules\` and `.windsurf\rules\`.

## Antigravity Trigger Mapping
- **Always On**: `trigger: always_on` (Automatically injected)
- **Manual**: `trigger: manual` (Requires @-mention)
- **Glob**: `trigger: glob` (Fires on matched files, e.g., `**/*.cs`)
- **Model Decision**: AI implicitly decides based on natural language.

## Stop Hook (`agentStop`)
- Fires immediately BEFORE the AI completes its response.
- Used to execute CloudSync (`SYNC_TO_GEMINI_SILENT.bat`) or validate artifacts.
- Configured via Antigravity Settings -> Hooks.

## File Inventory (Key Paths)
- **Universal Rules**: `Always\AGENTS.md`
- **Debug Protocol**: `StableOrOther\BugInvestigation.md`
- **C# Rules**: `Glob\core_godot_rx.md` (`**/*.cs`)
- **App Data Dir**: `C:\Users\26070\.gemini\antigravity\` (Logs: `brain\<conversation-id>\.system_generated\logs\`)

## Common Operations
1. **Add New Rule**: Create in `rules_global\`, add hardlinks in `setup-symlinks.ps1` (for Windsurf AND Antigravity). Re-run script.
2. **Edit Global Rules**: `notepad "C:\Users\26070\.gemini\GEMINI.md"`
3. **Manual CloudSync**: `cd C:\Godot\AISpace\CloudSync_Workflow; python agent_sync_to_drive.py`

<system_reminder>
Never copy-paste rule files. ALWAYS use Windows hardlinks via `setup-symlinks.ps1` so changes propagate across all IDE configurations (`.agents`, `.windsurf`, `AGENTS.md`).
</system_reminder>
