from pathlib import Path

PROJECT_WHITELIST_PREFIXES = ['A1', 'B1']

# Test with REAL files
test_files = [
    r'C:\Godot\3d-practice\addons\R3.Godot\FrameProviderDispatcher.cs',
    r'C:\Godot\3d-practice\addons\phantom_camera\plugin.cfg',
    r'C:\Godot\3d-practice\addons\A1TetrisBackpack\GridShapeComponent.cs'
]

print("Testing addon detection logic:\n")

for f in test_files:
    p = Path(f)
    if not p.exists():
        print(f"❌ File not found: {p.name}\n")
        continue
        
    rel = p.relative_to(Path(r'C:\Godot\3d-practice'))
    parts = rel.parts
    
    print(f"File: {p.name}")
    print(f"  Relative path: {rel}")
    print(f"  Path parts: {parts}")
    print(f"  parts[0]: '{parts[0]}'")
    
    if len(parts) > 1 and parts[0] == 'addons':
        addon_name = parts[1]
        is_custom = any(addon_name.startswith(prefix) for prefix in PROJECT_WHITELIST_PREFIXES)
        print(f"  Addon name: '{addon_name}'")
        print(f"  Is custom (A1/B1): {is_custom}")
        print(f"  Should be filtered: {not is_custom}")
    else:
        print(f"  Not in addons folder")
    
    print()
