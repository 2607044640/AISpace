from pathlib import Path
import re

drive_path = Path(r"C:\Users\26070\My Drive\Kiro_Godot_Brain")
latest_file = max(drive_path.glob("AI_Context_Master_*.txt"), key=lambda p: p.stat().st_mtime)

print(f"📊 验证文件: {latest_file.name}")
print(f"📦 文件大小: {latest_file.stat().st_size / (1024*1024):.2f} MB\n")

with open(latest_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 统计
third_party_count = content.count('<third_party_addon')
binary_asset_count = content.count('<binary_asset')

print(f"🔪 第三方插件墓碑: {third_party_count} 个")
print(f"🛡️ 二进制资源索引: {binary_asset_count} 个\n")

# 精确检测：查找第三方插件的完整源码
print("🔍 第三方插件源码泄漏检测（精确模式）:\n")

third_party_addons = [
    'R3.Godot',
    'phantom_camera',
    'godot-jolt',
    'Todo_Manager',
    'godot_state_charts',
    'theme_gen'
]

# 使用正则表达式查找完整的文件块
file_pattern = re.compile(r'<file path="3d-practice/addons\\([^"]+)"[^>]*>(.*?)</file>', re.DOTALL)

leaked_files = []
stub_files = []

for match in file_pattern.finditer(content):
    file_path = match.group(1)
    file_content = match.group(2)
    
    # 检查是否是第三方插件
    addon_name = file_path.split('\\')[0] if '\\' in file_path else file_path.split('/')[0]
    
    if addon_name in third_party_addons:
        # 检查内容类型
        if '<![CDATA[' in file_content:
            # 完整源码！
            leaked_files.append(file_path)
        elif '<third_party_addon' in file_content or '<binary_asset' in file_content:
            # 墓碑或二进制索引
            stub_files.append(file_path)

# 报告结果
if leaked_files:
    print(f"❌ 发现 {len(leaked_files)} 个源码泄漏文件:")
    for f in leaked_files[:10]:
        print(f"  - {f}")
    if len(leaked_files) > 10:
        print(f"  ... 还有 {len(leaked_files) - 10} 个")
else:
    print("✅ 没有发现源码泄漏！")

print(f"\n✅ 第三方插件墓碑/索引文件: {len(stub_files)} 个")

# 按插件分组统计
print("\n📊 按插件分组:")
addon_stats = {}
for f in stub_files:
    addon = f.split('\\')[0] if '\\' in f else f.split('/')[0]
    addon_stats[addon] = addon_stats.get(addon, 0) + 1

for addon, count in sorted(addon_stats.items()):
    print(f"  {addon}: {count} 个文件")

print(f"\n📉 瘦身效果:")
print(f"  修复前: 2.78 MB (包含第三方源码)")
print(f"  修复后: {latest_file.stat().st_size / (1024*1024):.2f} MB")
reduction = 2.78 - latest_file.stat().st_size / (1024*1024)
print(f"  减少: {reduction:.2f} MB ({reduction / 2.78 * 100:.1f}%)")
