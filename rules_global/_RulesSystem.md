---
trigger: manual
---

## Objective
Rules Infrastructure Guide. Explains the Windows hardlink architecture powering multi-IDE rule synchronization.

> [!CAUTION]
> **CRITICAL RULE — ONE SOURCE OF TRUTH, ALL OTHERS ARE HARDLINKS**
>
> `rules_global\Always\AGENTS.md` is the **ONLY** file you are ever allowed to edit.
> Every other `AGENTS.md` location (`AISpace\AGENTS.md`, `.windsurf\rules\`, `.agents\rules\`, `rules_ide\Codex\`) is a **Windows hardlink** to this file — they share the same inode and update instantly.
>
> **If you edit any other path, you risk editing an orphan copy that NO IDE picks up.**
> **`TetrisBackpack\AGENTS.md` does NOT exist and must NEVER be recreated.**
>
> To verify a file is hardlinked (not an orphan copy): `fsutil hardlink list "path\to\AGENTS.md"` — output must include `rules_global\Always\AGENTS.md`.
> If it does NOT appear, the file is a rogue orphan and must be **deleted immediately**.

## Hardlink Architecture (Core Principle)
- **Single Source of Truth**: `C:\Godot\AISpace\rules_global\Always\AGENTS.md`
- **All hardlink destinations** (all point to the same inode):
  - `AISpace\AGENTS.md` — Zed / Claude Code / root-lookup IDEs
  - `AISpace\.agents\rules\Always\AGENTS.md` — Antigravity
  - `AISpace\.windsurf\rules\Always\AGENTS.md` — Windsurf
  - `AISpace\rules_ide\Codex\AGENTS.md` — GPT/Codex
- Editing any of the above updates all others instantly (same inode).
- `TetrisBackpack\` has NO `AGENTS.md` — all rules live under `AISpace\`.
- `rules_global\` DOES NOT survive `git clone` (git ignores hardlinks). Re-run setup script after clone.

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
| IDE | Path | Notes |
|---|---|---|
| Windsurf | `AISpace\.windsurf\rules\Always\AGENTS.md` | Reads frontmatter trigger |
| Antigravity | `AISpace\.agents\rules\Always\AGENTS.md` | Always/Manual/Glob |
| GPT/Codex | `AISpace\rules_ide\Codex\AGENTS.md` | workspace-root lookup |
| Zed / Claude Code | `AISpace\AGENTS.md` | root-level AGENTS.md lookup |
| Kiro/Cursor/Cline/Copilot | Add hardlinks to `setup-symlinks.ps1` STEP 4 | |

## Cloud Sync Integration (`agent_sync_to_drive.py`)
- Sync uses explicit whitelists.
- `rules_global\` is INTENTIONALLY EXCLUDED to prevent duplicate content (since `.windsurf\rules\` is already scanned).
- `AISpace\AGENTS.md` (root hardlink) must be in `PROJECT_ROOT_MD_SKIP` in the sync script to avoid duplicate content.

<system_reminder>
Do NOT link this file to `.kiro/steering/`. Kiro defaults to `inclusion: always`, which will bloat the context.
</system_reminder>
