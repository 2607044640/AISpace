import os
from pathlib import Path

def is_binary_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(1024)
            if b'\x00' in chunk:
                return True
    except Exception:
        pass
    return False

# Test files
test_files = [
    r'C:\Godot\3d-practice\icon.svg',
    r'C:\Godot\3d-practice\project.godot',
    r'C:\Godot\3d-practice\3dPractice.csproj',
]

print("Testing binary detection:")
for f in test_files:
    if Path(f).exists():
        result = is_binary_file(f)
        size_kb = Path(f).stat().st_size / 1024
        print(f'{Path(f).name}: {"BINARY" if result else "TEXT"} ({size_kb:.2f} KB)')
    else:
        print(f'{f}: NOT FOUND')

# Count binary files in project
source_path = Path(r'C:\Godot\3d-practice')
binary_count = 0
text_count = 0

IGNORE_EXTENSIONS = (
    '.png', '.jpg', '.jpeg', '.svg', '.webp', '.ico',
    '.ogg', '.wav', '.mp3', '.aac', '.flac',
    '.glb', '.gltf', '.fbx', '.obj', '.blend',
    '.dll', '.so', '.a', '.pdb', '.dylib',
    '.res', '.spv', '.uid', '.import',
    '.exe', '.bin', '.dat', '.cache'
)

IGNORE_DIRS = (
    '.godot', '.git', '.vs', '.idea', '.vscode',
    'bin', 'obj', 'Export', 'Builds', 'Library',
    'Temp', 'node_modules', '__pycache__',
    '.backup_old_components', 'NVIDIA Corporation',
    'AnimationFBX', 'Animations'
)

print("\nScanning project for binary files...")
for root, dirs, files in os.walk(source_path):
    # Filter out ignored directories
    dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
    
    for file in files:
        file_path = Path(root) / file
        
        # Skip ignored extensions
        if file.endswith(IGNORE_EXTENSIONS):
            continue
        
        # Check if binary
        if is_binary_file(file_path):
            binary_count += 1
            print(f"  BINARY: {file_path.relative_to(source_path)}")
        else:
            text_count += 1

print(f"\nResults:")
print(f"  Binary files detected: {binary_count}")
print(f"  Text files: {text_count}")
print(f"  Total: {binary_count + text_count}")
