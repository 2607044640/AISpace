---
trigger: manual
---

## Objective
Rules Infrastructure Guide. Explains the Windows hardlink architecture powering multi-IDE rule synchronization.

> [!CAUTION]
> **CRITICAL RULE — ONE SOURCE OF TRUTH, ALL OTHERS ARE HARDLINKS**
>
> `rules_global\Always\AGENTS.md` is the **ONLY** file you are ever allowed to edit.
> Every other `AGENTS.md` location (TetrisBackpack, .windsurf, .agents, Codex) is a **Windows hardlink** to this file — they share the same inode and update instantly.
>
> **If you edit any other path (e.g. `AISpace\AGENTS.md`, `TetrisBackpack\AGENTS.md`), you are editing a copy that NO IDE will pick up, or you risk breaking the hardlink chain.**
>
> To verify a file is hardlinked (not an orphan copy): `fsutil hardlink list "path\to\AGENTS.md"` — output must include `rules_global\Always\AGENTS.md`.
> If it does NOT appear, the file is a rogue orphan and must be **deleted immediately**.

## Hardlink Architecture (Core Principle)
- **Single Source of Truth**: `C:\Godot\AISpace\rules_global\`
- **Shared Destinations**: `.windsurf\rules\`, `AISpace\.agents\rules\`, `TetrisBackpack\AGENTS.md`
- **Codex Destination**: `AISpace\AGENTS.md`
- Shared destinations are Windows hardlinks to `rules_global\`.
- Codex workspace-root lookup now hardlinks directly to `rules_global\Always\AGENTS.md`.
- Editing a hardlinked source updates every destination linked to that source instantly. No syncing/copying needed.
- `rules_global\` DOES NOT survive `git clone` (git ignores hardlinks).

## Quick Operations
- **Edit Rule**: Open file in `rules_global\`. Edit directly.
- **Fresh Clone / First Run**:
  1. `powershell -ExecutionPolicy Bypass -File "C:\Godot\AISpace\temp\build_rules_global.ps1"`
  2. `powershell -ExecutionPolicy Bypass -File "C:\Godot\AISpace\scripts\setup-symlinks.ps1"`
- **Verify Hardlinks**: `fsutil hardlink list "C:\Godot\AISpace\rules_global\AGENTS.md"`

## Adding New Rules or IDEs
1. **New Rule**: Create in `rules_global\`, add to `setup-symlinks.ps1` (STEP 2), re-run script.
2. **New IDE**: Add hardlink path (e.g., `.cursorrules`) to `setup-symlinks.ps1` (STEP 4), pointing to `AGENTS.md`.

## IDE Support Matrix
- **Windsurf**: `.windsurf\rules\**` (reads frontmatter)
- **Antigravity**: `.agents\rules\**` (Always/Manual/Glob)
- **GPT/Codex**: `AISpace\AGENTS.md` (workspace-root lookup)
- **Zed/Claude Code**: `TetrisBackpack\AGENTS.md` (root lookup)
- **Kiro/Cursor/Cline/Copilot**: Handled via root-level hardlinks in STEP 4.

## Cloud Sync Integration (`agent_sync_to_drive.py`)
- Sync uses explicit whitelists.
- `rules_global\` is INTENTIONALLY EXCLUDED to prevent duplicate content (since `.windsurf\rules\` is already scanned).
- Hardlinks in `TetrisBackpack\` root (e.g., `AGENTS.md`) must be added to `PROJECT_ROOT_MD_SKIP` in the sync script.

<system_reminder>
Do NOT link this file to `.kiro/steering/`. Kiro defaults to `inclusion: always`, which will bloat the context.
</system_reminder>
