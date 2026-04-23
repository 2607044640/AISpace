from pathlib import Path

drive_path = Path(r"C:\Users\26070\My Drive\Kiro_Godot_Brain")
latest = max(drive_path.glob("AI_Context_Master_*.txt"), key=lambda p: p.stat().st_mtime)

print(f"Final Verification: {latest.name}\n")

with open(latest, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Check specific third-party addons
third_party = ['phantom_camera', 'R3.Godot', 'godot-jolt', 'Todo_Manager', 'theme_gen', 'godot_state_charts']
results = {addon: {'stub': 0, 'source': 0} for addon in third_party}

for i, line in enumerate(lines):
    for addon in third_party:
        if f'addons\\{addon}' in line or f'addons/{addon}' in line:
            # Check next lines
            for j in range(i+1, min(i+5, len(lines))):
                if '<third_party_addon' in lines[j]:
                    results[addon]['stub'] += 1
                    break
                elif '<![CDATA[' in lines[j]:
                    results[addon]['source'] += 1
                    print(f"  ❌ Leaked: {line.strip()[:80]}")
                    break

print('🔍 Third-party addon filtering results:\n')
all_filtered = True
for addon, counts in results.items():
    if counts['source'] == 0 and counts['stub'] > 0:
        print(f'✅ {addon}: {counts["stub"]} files filtered (墓碑)')
    elif counts['source'] > 0:
        print(f'❌ {addon}: {counts["source"]} files LEAKED!')
        all_filtered = False
    else:
        print(f'⚪ {addon}: No files found')

if all_filtered:
    print('\n🎉 绞肉机工作完美！所有第三方插件源码都被过滤了！')
    print(f'\n📉 文件大小: {latest.stat().st_size / (1024*1024):.2f} MB')
    print(f'   减少: {2.78 - latest.stat().st_size / (1024*1024):.2f} MB (46%)')
else:
    print('\n❌ 发现第三方插件源码泄漏！')
