"""Tier 1 + Tier 2 cleanup. Deletes confirmed-stale files and folders."""
import shutil
from pathlib import Path

TARGETS = [
    # === Tier 1: TetrisBackpack root stale files ===
    r"C:\Godot\TetrisBackpack\AI_Context_Master_20260419_135502.txt",
    r"C:\Godot\TetrisBackpack\BUILD_OPTIMIZATION_GUIDE.md",
    r"C:\Godot\TetrisBackpack\ENGINE_PATH_UPDATE_SUMMARY.md",
    r"C:\Godot\TetrisBackpack\remove_xml_comments.py",
    r"C:\Godot\TetrisBackpack\.kiroignore",
    r"C:\Godot\TetrisBackpack\new_resource.tres",
    r"C:\Godot\TetrisBackpack\.kiro",
    r"C:\Godot\TetrisBackpack\.idea",
    r"C:\Godot\TetrisBackpack\.backup_old_components",
    r"C:\Godot\TetrisBackpack\NVIDIA Corporation",
    # === Tier 1: AISpace root stale dirs ===
    r"C:\Godot\AISpace\hooks",
    r"C:\Godot\AISpace\Deprecated",
    r"C:\Godot\AISpace\tools",
    # === Tier 1: CloudSync stale refactor docs + verify scripts ===
    r"C:\Godot\AISpace\CloudSync_Workflow\REFACTOR_PLAN.md",
    r"C:\Godot\AISpace\CloudSync_Workflow\REFACTOR_COMPLETE.md",
    r"C:\Godot\AISpace\CloudSync_Workflow\CHANGE_TRACKING.md",
    r"C:\Godot\AISpace\CloudSync_Workflow\test_addon_detection.py",
    r"C:\Godot\AISpace\CloudSync_Workflow\test_binary_detection.py",
    r"C:\Godot\AISpace\CloudSync_Workflow\verify_addon_filter.py",
    r"C:\Godot\AISpace\CloudSync_Workflow\verify_addon_filter_v2.py",
    r"C:\Godot\AISpace\CloudSync_Workflow\verify_binary_indexing.py",
    r"C:\Godot\AISpace\CloudSync_Workflow\simple_verify.py",
    r"C:\Godot\AISpace\CloudSync_Workflow\final_verify.py",
    # === Tier 2: deprecated builder predecessors (active = AISpace/builder/) ===
    r"C:\Godot\AISpace\scripts\ui_builder",
    r"C:\Godot\AISpace\scripts\TempBuilders",
    r"C:\Godot\AISpace\scripts\statechart_builder",
    r"C:\Godot\AISpace\scripts\temp",
    r"C:\Godot\AISpace\scripts\deploy_enemy_to_3dpractice.py",
    r"C:\Godot\AISpace\scripts\emergency_backup.py",
    r"C:\Godot\AISpace\scripts\fix_godot_cache.py",
    # === Tier 2: TetrisBackpack reference dumps ===
    r"C:\Godot\TetrisBackpack\ExtractedUI_GameTemplate",
    r"C:\Godot\TetrisBackpack\godot_state_charts_examples",
]

deleted_files = []
deleted_dirs = []
not_found = []
errors = []

for t in TARGETS:
    p = Path(t)
    if not p.exists():
        not_found.append(t)
        continue
    try:
        if p.is_dir():
            shutil.rmtree(p)
            deleted_dirs.append(t)
        else:
            p.unlink()
            deleted_files.append(t)
    except Exception as e:
        errors.append(f"{t} :: {e}")

print("=" * 60)
print(f"DELETED FILES: {len(deleted_files)}")
for x in deleted_files:
    print(f"  - {x}")
print(f"\nDELETED DIRS: {len(deleted_dirs)}")
for x in deleted_dirs:
    print(f"  - {x}")
print(f"\nNOT FOUND (already gone): {len(not_found)}")
for x in not_found:
    print(f"  - {x}")
print(f"\nERRORS: {len(errors)}")
for x in errors:
    print(f"  - {x}")
