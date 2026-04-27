# =============================================================================
# setup-symlinks.ps1
# Single source of truth: AISpace\rules_global\
#
# rules_global\ is the ONE folder you edit. This script wires hardlinks so:
#   - .windsurf\rules\ links: always_on AGENTS.md + glob-triggered context files
#   - AISpace\AGENTS.md and rules_ide\Codex\AGENTS.md point to rules_global\Always\AGENTS.md
#   - TetrisBackpack\AGENTS.md points to rules_global\Always\AGENTS.md  (Zed/Claude Code)
#   - AISpace\.agents\rules\ links: Antigravity workspace rules (Always On + Glob)
#
# Manual-trigger files live ONLY in rules_global\ (no .windsurf copies).
# @-mention them directly from rules_global\subfolder\filename in any IDE.
#
# WHY hardlinks instead of symlinks:
#   - File symlinks require admin or Developer Mode on Windows.
#   - Hardlinks on the same NTFS volume need NO elevation.
#   - Editing through ANY hardlink path updates all of them instantly.
#
# USAGE (run after every fresh clone, or when adding a new IDE):
#   powershell -ExecutionPolicy Bypass -File "C:\Godot\AISpace\scripts\setup-symlinks.ps1"
#
# IDEMPOTENT: Safe to run multiple times. Existing links are replaced cleanly.
# =============================================================================

$ErrorActionPreference = "Stop"

$Root      = "C:\Godot"
$GlobalDir = "$Root\AISpace\rules_global"
$CodexDir  = "$Root\AISpace\rules_ide\Codex"
$WR        = "$Root\AISpace\.windsurf\rules"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
function Write-Header([string]$msg) {
    Write-Host ""
    Write-Host "=== $msg ===" -ForegroundColor Cyan
}

function Create-HardLink([string]$Dest, [string]$Source) {
    if (-not (Test-Path $Source)) {
        Write-Host "  [SKIP] Source not found: $Source" -ForegroundColor Red
        return
    }
    $destDir = Split-Path $Dest -Parent
    if (-not (Test-Path $destDir)) {
        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
    }
    if (Test-Path $Dest) {
        Remove-Item -Path $Dest -Force
    }
    New-Item -ItemType HardLink -Path $Dest -Value $Source | Out-Null
    $rel = $Dest.Replace($Root, "").TrimStart("\")
    $srcRel = $Source.Replace($Root, "").TrimStart("\")
    Write-Host "  Linked: $rel  <-  $srcRel" -ForegroundColor Green
}

# ---------------------------------------------------------------------------
# STEP 1 — Verify rules_global\ exists and has content
# ---------------------------------------------------------------------------
Write-Header "Verifying rules_global source"
if (-not (Test-Path $GlobalDir)) {
    Write-Host "  MISSING: $GlobalDir" -ForegroundColor Red
    Write-Host "  Run temp\build_rules_global.ps1 first to initialise rules_global\." -ForegroundColor Red
    exit 1
}
$count = (Get-ChildItem $GlobalDir -Filter "*.md").Count
Write-Host "  OK: $GlobalDir ($count .md files)" -ForegroundColor Green

# ---------------------------------------------------------------------------
# STEP 2 — Wire .windsurf\rules\** → rules_global\
#
# Format: Create-HardLink  <destination in .windsurf>  <source in rules_global>
# The .windsurf paths are where Windsurf reads the files.
# rules_global is where you edit them.
# ---------------------------------------------------------------------------
Write-Header "Wiring .windsurf\rules\ -> rules_global (always_on + glob only)"

# always_on — must be in .windsurf for Windsurf to auto-load
Create-HardLink "$WR\Always\AGENTS.md"              "$GlobalDir\Always\AGENTS.md"

# Lean domain-specific glob rules (Phase 2 & 3 of AI Rules Optimization Protocol)
# NOTE: GodotBackpackTesseractSys_Context.md is manual-only — @-mention from rules_global\Godot\ directly.
Create-HardLink "$WR\Godot\core_godot_rx.md"  "$GlobalDir\Glob\core_godot_rx.md"
Create-HardLink "$WR\Godot\domain_grid.md"    "$GlobalDir\Glob\domain_grid.md"
Create-HardLink "$WR\Godot\domain_ui.md"      "$GlobalDir\Glob\domain_ui.md"

# NOTE: Windsurf-only automation hooks (AutoCompile_OnCsEdit.md, AutoSync_OnFileEdit.md)
# live ONLY in .windsurf\rules\Godot\ (trigger: glob). Zed/Claude cannot parse glob triggers.
# Do NOT add them here — they must NOT exist in rules_global\.

# Manual-trigger files are NOT hardlinked back to .windsurf.
# They exist only in rules_global\subfolder\ and are @-mentioned from there.
Write-Host "  (manual files: rules_global only, no .windsurf copy)" -ForegroundColor DarkGray

# ---------------------------------------------------------------------------
# STEP 3 — Wire workspace-root AGENTS.md files (Codex + Zed/Claude Code)
# ---------------------------------------------------------------------------
Write-Header "Wiring Codex and workspace-root AGENTS.md files"
Create-HardLink "$CodexDir\AGENTS.md" "$GlobalDir\Always\AGENTS.md"
Create-HardLink "$Root\AISpace\AGENTS.md" "$GlobalDir\Always\AGENTS.md"
Create-HardLink "$Root\TetrisBackpack\AGENTS.md" "$GlobalDir\Always\AGENTS.md"

# ---------------------------------------------------------------------------
# STEP 3b — Wire TetrisBackpack\.agents\rules\ (Antigravity)
#
# Antigravity reads from .agents\rules\ (same trigger model as .windsurf\rules\).
# Always On  → .agents\rules\Always\
# Glob       → .agents\rules\Glob\
# ---------------------------------------------------------------------------
$AG = "$Root\AISpace\.agents\rules"
Write-Header "Wiring AISpace\.agents\rules\ (Antigravity)"

# Always On — injected into every Antigravity conversation
Create-HardLink "$AG\Always\AGENTS.md"        "$GlobalDir\Always\AGENTS.md"

# Glob — domain-specific lean rules (auto-trigger on file match)
Create-HardLink "$AG\Glob\AutoSync_OnFileEdit.md" "$GlobalDir\Glob\AutoSync_OnFileEdit.md"
Create-HardLink "$AG\Glob\core_godot_rx.md"       "$GlobalDir\Glob\core_godot_rx.md"
Create-HardLink "$AG\Glob\domain_grid.md"         "$GlobalDir\Glob\domain_grid.md"
Create-HardLink "$AG\Glob\domain_ui.md"           "$GlobalDir\Glob\domain_ui.md"


# ---------------------------------------------------------------------------
# STEP 4 — Future IDEs (uncomment the block for each new IDE, then re-run)
#
# All entries point at $GlobalDir\AGENTS.md — zero extra maintenance.
# Check the IDE docs for the exact filename/path it expects.
# ---------------------------------------------------------------------------
Write-Header "Future IDEs (currently disabled)"

# --- Kiro (.kiro/steering/ — use inclusion: always in frontmatter) -----------
# Note: Kiro ignores Windsurf's "trigger:" frontmatter. Add "inclusion: always"
# to AGENTS.md frontmatter if you want Kiro to auto-load it.
# Create-HardLink "$Root\TetrisBackpack\.kiro\steering\AGENTS.md" "$GlobalDir\Always\AGENTS.md"

# --- Cursor (.cursorrules at project root) -----------------------------------
# Create-HardLink "$Root\TetrisBackpack\.cursorrules" "$GlobalDir\Always\AGENTS.md"

# --- Cline (.clinerules at project root) -------------------------------------
# Create-HardLink "$Root\TetrisBackpack\.clinerules" "$GlobalDir\Always\AGENTS.md"

# --- GitHub Copilot ----------------------------------------------------------
# Create-HardLink "$Root\TetrisBackpack\.github\copilot-instructions.md" "$GlobalDir\Always\AGENTS.md"

# --- Generic .rules (VS Code extensions, explicit Zed override, etc.) --------
# Create-HardLink "$Root\TetrisBackpack\.rules" "$GlobalDir\Always\AGENTS.md"

Write-Host "  (Uncomment the relevant block above and re-run this script)" -ForegroundColor DarkGray

# ---------------------------------------------------------------------------
# DONE
# ---------------------------------------------------------------------------
Write-Host ""
Write-Host "All done!" -ForegroundColor Green
Write-Host ""
Write-Host "Edit rules here (single folder):" -ForegroundColor White
Write-Host "  AISpace\rules_global\"           -ForegroundColor Yellow
Write-Host ""
Write-Host "Active hardlinks for AGENTS.md:"  -ForegroundColor DarkCyan
fsutil hardlink list "$GlobalDir\Always\AGENTS.md"
Write-Host ""
if (Test-Path "$Root\AISpace\AGENTS.md") {
    Write-Host "Verified: AISpace\\AGENTS.md exists for Codex root lookup." -ForegroundColor Green
} else {
    Write-Host "ERROR: AISpace\\AGENTS.md is missing after link setup." -ForegroundColor Red
    exit 1
}
Write-Host ""
Write-Host "To add a new IDE: uncomment its block in STEP 4 and re-run." -ForegroundColor DarkCyan
