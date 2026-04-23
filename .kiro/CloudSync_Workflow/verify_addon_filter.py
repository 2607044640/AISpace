from pathlib import Path

# Read the most recent master file
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

# 检查是否还有第三方插件源码泄漏
leak_tests = [
    ('PhantomCamera', 'phantom_camera'),
    ('R3.Godot', 'FrameProviderDispatcher'),
    ('Jolt Physics', 'godot-jolt'),
    ('Todo Manager', 'Todo_Manager')
]

print("🔍 第三方插件源码泄漏检测:")
for plugin_name, keyword in leak_tests:
    # 检查是否有完整的 CDATA 代码块（说明源码被读取了）
    if f'<![CDATA[' in content and keyword in content:
        # 进一步检查是否在 CDATA 内
        lines = content.split('\n')
        in_cdata = False
        leaked = False
        for line in lines:
            if '<![CDATA[' in line:
                in_cdata = True
            if ']]>' in line:
                in_cdata = False
            if in_cdata and keyword in line:
                leaked = True
                break
        
        if leaked:
            print(f"  ❌ {plugin_name}: 源码泄漏！")
        else:
            print(f"  ✅ {plugin_name}: 仅墓碑索引")
    else:
        print(f"  ✅ {plugin_name}: 仅墓碑索引")

# 显示墓碑示例
print("\n📝 第三方插件墓碑示例:")
lines = content.split('\n')
count = 0
for i, line in enumerate(lines):
    if '<third_party_addon' in line and count < 5:
        if i > 0:
            print(f"  {lines[i-1].strip()}")
        print(f"  {line.strip()}")
        print()
        count += 1

# 文件大小对比
print(f"\n📉 瘦身效果:")
print(f"  修复前: 2.78 MB (包含第三方源码)")
print(f"  修复后: {latest_file.stat().st_size / (1024*1024):.2f} MB")
print(f"  减少: {2.78 - latest_file.stat().st_size / (1024*1024):.2f} MB ({(2.78 - latest_file.stat().st_size / (1024*1024)) / 2.78 * 100:.1f}%)")
