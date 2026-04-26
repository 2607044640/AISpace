---
trigger: manual
---

## Objective
Sync project context to Google Drive for Gemini AI and generate human-readable categorized views.

## Core File Paths
- **Script**: `AISpace/CloudSync_Workflow/agent_sync_to_drive.py`
- **Cloud Output (AI)**: `C:\Users\26070\My Drive\Agent_Godot_Brain\AI_Context_Master_YYYYMMDD_HHMMSS.txt` (XML)
- **Local Output (Human)**: `D:\A1GeminiSyncTestForHuman\` (5 TXT files)
- **Backup**: `D:\Agent_Godot_Brain_Backup\` (Manifest/Old files)
- **Changes**: `D:\A1GeminiSyncTestForHuman\AI_Context_Changes.md`

## Architecture Highlights
- **Dual-Output**: Single XML monolith for AI (sorted by priority 01-06), 5 categorized TXT files for humans.
- **Binary Asset Radar**: Detects null bytes `\x00`. Replaces with `<binary_asset type=".png" size_kb="123" />`.
- **Third-Party Filter**: Replaces non-A1/B1 `addons/` files with `<third_party_addon name="X" />`.
- **Change Tracking**: MD5 hash-based diffing. Most recent 5 records marked `<RECENT_CHANGES>`.

## Auto-Sync Triggers
- **Triggers**: `agentStop`, `fileEdited` (`.md`, `.cs`, `.gd`, `.tscn`).
- **Execution**: Runs `SYNC_TO_GEMINI_SILENT.bat` in background.

## Key Functions & Flow
1. `build_dual_sync()`: Main orchestrator. Scans `AISpace/` & `TetrisBackpack/`.
2. `classify_file_to_bucket()`: Priority: `01_important_rules` -> `03_a1_components` -> `04_b1_components` -> `02_other_rules` -> `05_project_core`.
3. `is_binary_file()`: Reads first 1024 bytes.
4. `process_file_to_bucket()`: Writes actual text OR `<stub>` for binaries/addons.

## Configuration & Filters
- **Project Whitelist**: `A1`, `B1` (bypass size limits and addon filter).
- **Agent Whitelist**: `rules_global`, `rules_ide`, `ProjectRules.md`, `docLastConversationState.md`, `ConversationReset.md`.
- **Ignore Rules**: Directories (`.godot`, `.git`, `bin`, `obj`), Extensions (`.png`, `.dll`, `.res`, etc.).

## Troubleshooting
- **Binaries not indexed**: Ensure `is_ignored()` checks directories ONLY, NOT extensions (otherwise binaries don't reach radar).
- **Addon source leaking**: Ensure third-party filter runs AFTER binary radar.
- **Changes empty**: Verify `AI_Context_Manifest.json` exists in Backup dir.

## Quick Commands (PowerShell)
- **Sync**: `cd C:\Godot\AISpace\CloudSync_Workflow; python agent_sync_to_drive.py`
- **View Changes**: `Get-Content "D:\A1GeminiSyncTestForHuman\AI_Context_Changes.md" -Head 20`
- **Verify**: `python verify_binary_indexing.py`, `python final_verify.py`

<system_reminder>
Never guess fixes for sync pipeline issues. Use `test_binary_detection.py` and `test_addon_detection.py` to isolate bugs first.
</system_reminder>
