from pathlib import Path

drive_path = Path(r"C:\Users\26070\My Drive\Kiro_Godot_Brain")
latest = max(drive_path.glob("AI_Context_Master_*.txt"), key=lambda p: p.stat().st_mtime)

print(f"Checking: {latest.name}\n")

with open(latest, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Track addon files
addon_files = {'stub': 0, 'source': 0, 'binary': 0}
current_addon_file = None

for i, line in enumerate(lines):
    # Check if this is an addon file
    if 'path="3d-practice/addons' in line:
        current_addon_file = line.strip()
        # Check next few lines
        for j in range(i+1, min(i+5, len(lines))):
            next_line = lines[j]
            if '<third_party_addon' in next_line:
                addon_files['stub'] += 1
                break
            elif '<binary_asset' in next_line:
                addon_files['binary'] += 1
                break
            elif '<![CDATA[' in next_line:
                addon_files['source'] += 1
                print(f"❌ Source leak: {current_addon_file[:80]}")
                break
            elif '</file>' in next_line:
                break

print(f"\n📊 Addon files breakdown:")
print(f"  🔪 Stubs (third_party_addon): {addon_files['stub']}")
print(f"  🛡️ Binary assets: {addon_files['binary']}")
print(f"  📝 Full source code: {addon_files['source']}")

if addon_files['source'] == 0:
    print(f"\n✅ 绞肉机工作完美！所有第三方插件都被过滤了！")
else:
    print(f"\n❌ 发现 {addon_files['source']} 个源码泄漏！")
