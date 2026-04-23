from pathlib import Path

# Read the most recent master file from Google Drive
drive_path = Path(r"C:\Users\26070\My Drive\Kiro_Godot_Brain")
master_files = list(drive_path.glob("AI_Context_Master_*.txt"))

if not master_files:
    print("No master files found!")
    exit(1)

# Get the most recent file
latest_file = max(master_files, key=lambda p: p.stat().st_mtime)
print(f"Checking file: {latest_file.name}")
print(f"File size: {latest_file.stat().st_size / (1024*1024):.2f} MB\n")

# Count binary_asset tags
with open(latest_file, 'r', encoding='utf-8') as f:
    content = f.read()
    
binary_asset_count = content.count('<binary_asset')
print(f"Binary asset entries found: {binary_asset_count}")

# Show a few examples
if binary_asset_count > 0:
    print("\nFirst 5 binary asset entries:")
    lines = content.split('\n')
    count = 0
    for i, line in enumerate(lines):
        if '<binary_asset' in line:
            # Show context (file path from previous line)
            if i > 0:
                print(f"  {lines[i-1].strip()}")
            print(f"  {line.strip()}")
            count += 1
            if count >= 5:
                break
else:
    print("\n❌ NO BINARY ASSETS FOUND! The indexing is not working.")
    print("\nSearching for specific binary files that should be indexed:")
    test_files = ['noto_sans', 'godot-jolt', 'test_paths.txt']
    for test in test_files:
        if test in content:
            print(f"  ✓ Found reference to: {test}")
        else:
            print(f"  ✗ NOT found: {test}")
