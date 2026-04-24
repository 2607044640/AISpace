"""
Workspace cleanup & standardization script.
Executes:
 1. Purge *.bak files in AISpace + TetrisBackpack
 2. Purge stray test*.txt / test*.md outside AISpace/temp/
 3. Delete any Scratchpad/ directories
 4. Replace AI monikers (Kiro/Cursor/Cascade/Augment) -> Agent in .md/.txt files
    located under AISpace/ and TetrisBackpack/
Scope: case-preserving via ordered regex replacements.
"""
import os
import re
import shutil
from pathlib import Path

ROOTS = [Path(r"C:\Godot\AISpace"), Path(r"C:\Godot\TetrisBackpack")]
TEMP_DIR = Path(r"C:\Godot\AISpace\temp").resolve()

deleted_bak = []
deleted_tests = []
deleted_scratchpads = []
modified_text_files = []


def is_inside_temp(p: Path) -> bool:
    try:
        p.resolve().relative_to(TEMP_DIR)
        return True
    except ValueError:
        return False


# --- 1 & 2: Delete .bak and stray test*.txt/md ---
for root in ROOTS:
    if not root.exists():
        continue
    for dirpath, dirnames, filenames in os.walk(root):
        # skip .git directories aggressively
        dirnames[:] = [d for d in dirnames if d != '.git']
        for fn in filenames:
            fp = Path(dirpath) / fn
            # .bak purge
            if fn.lower().endswith('.bak'):
                try:
                    fp.unlink()
                    deleted_bak.append(str(fp))
                except Exception as e:
                    print(f"[WARN] Could not delete {fp}: {e}")
                continue
            # stray test*.txt / test*.md outside temp
            low = fn.lower()
            if (low.startswith('test') and (low.endswith('.txt') or low.endswith('.md'))
                    and not is_inside_temp(fp)):
                try:
                    fp.unlink()
                    deleted_tests.append(str(fp))
                except Exception as e:
                    print(f"[WARN] Could not delete {fp}: {e}")

# --- 3: Delete Scratchpad directories ---
for root in ROOTS:
    if not root.exists():
        continue
    for dirpath, dirnames, _ in os.walk(root):
        for d in list(dirnames):
            if d == 'Scratchpad':
                target = Path(dirpath) / d
                try:
                    shutil.rmtree(target)
                    deleted_scratchpads.append(str(target))
                    dirnames.remove(d)
                except Exception as e:
                    print(f"[WARN] Could not remove {target}: {e}")

# --- 4: Terminology standardization ---
# Replace Kiro/Cursor/Cascade/Augment -> Agent (case-preserving for common forms).
# Order matters: handle ALL-CAPS first, then Title-case, then lower-case.
REPLACEMENTS = [
    (re.compile(r'\bKIRO\b'), 'AGENT'),
    (re.compile(r'\bCURSOR\b'), 'AGENT'),
    (re.compile(r'\bCASCADE\b'), 'AGENT'),
    (re.compile(r'\bAUGMENT\b'), 'AGENT'),
    (re.compile(r'\bKiro\b'), 'Agent'),
    (re.compile(r'\bCursor\b'), 'Agent'),
    (re.compile(r'\bCascade\b'), 'Agent'),
    (re.compile(r'\bAugment\b'), 'Agent'),
    (re.compile(r'\bkiro\b'), 'agent'),
    (re.compile(r'\bcursor\b'), 'agent'),
    (re.compile(r'\bcascade\b'), 'agent'),
    (re.compile(r'\baugment\b'), 'agent'),
]

for root in ROOTS:
    if not root.exists():
        continue
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != '.git']
        for fn in filenames:
            if not (fn.lower().endswith('.md') or fn.lower().endswith('.txt')):
                continue
            fp = Path(dirpath) / fn
            try:
                original = fp.read_text(encoding='utf-8')
            except Exception:
                continue
            new = original
            for pat, rep in REPLACEMENTS:
                new = pat.sub(rep, new)
            if new != original:
                try:
                    fp.write_text(new, encoding='utf-8')
                    modified_text_files.append(str(fp))
                except Exception as e:
                    print(f"[WARN] Could not write {fp}: {e}")

# --- Report ---
print("\n" + "=" * 60)
print("CLEANUP SUMMARY")
print("=" * 60)
print(f"\n[.bak files deleted: {len(deleted_bak)}]")
for p in deleted_bak:
    print(f"  - {p}")
print(f"\n[Stray test*.txt/md deleted: {len(deleted_tests)}]")
for p in deleted_tests:
    print(f"  - {p}")
print(f"\n[Scratchpad dirs deleted: {len(deleted_scratchpads)}]")
for p in deleted_scratchpads:
    print(f"  - {p}")
print(f"\n[Text files with terminology updated: {len(modified_text_files)}]")
for p in modified_text_files:
    print(f"  - {p}")
