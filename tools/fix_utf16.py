"""Find and fix UTF-16 files containing KiroWorkingSpace (missed by main script)."""
from pathlib import Path
import sys

ROOTS = [Path(r"C:\Godot\AISpace"), Path(r"C:\Godot\3d-practice")]
SKIP = {".git", ".godot", ".vs", ".idea", ".vscode", "bin", "obj",
        "node_modules", "__pycache__", ".import", "build", "dist"}
OLD = "KiroWorkingSpace"
NEW = "AISpace"

apply = "--apply" in sys.argv

found = []
for root in ROOTS:
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(s.lower() in SKIP for s in p.parts):
            continue
        if p.suffix.lower() == ".bak":
            continue
        try:
            b = p.read_bytes()
        except Exception:
            continue
        if b.startswith(b"\xff\xfe"):
            enc = "utf-16-le"
            has_bom = True
        elif b.startswith(b"\xfe\xff"):
            enc = "utf-16-be"
            has_bom = True
        else:
            continue
        try:
            t = b.decode(enc)
        except Exception:
            continue
        if OLD in t:
            count = t.count(OLD)
            found.append((p, enc, count))
            print(f"[{count} hits] {enc}  {p}")
            for i, line in enumerate(t.splitlines(), 1):
                if OLD in line:
                    print(f"    L{i}: {line.strip()[:200]}")
            if apply:
                new_t = t.replace(OLD, NEW)
                # Write back with BOM preserved (encode without BOM, prepend manually if was utf-16-le/be)
                # utf-16 codec writes BOM; utf-16-le/be does not. Preserve original format:
                if enc == "utf-16-le":
                    bak = p.with_suffix(p.suffix + ".bak")
                    bak.write_bytes(b)
                    p.write_bytes(b"\xff\xfe" + new_t.encode("utf-16-le"))
                else:
                    bak = p.with_suffix(p.suffix + ".bak")
                    bak.write_bytes(b)
                    p.write_bytes(b"\xfe\xff" + new_t.encode("utf-16-be"))
                print(f"    -> MODIFIED ({count} replacements)")

print(f"\nTotal UTF-16 files with hits: {len(found)}")
if not apply and found:
    print(">>> Re-run with --apply to fix them.")
