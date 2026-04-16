import os
import shutil
from pathlib import Path
from datetime import datetime

# ==========================================
# ⚙️ KIRO 的配置区
# ==========================================

# 你的 Godot 项目源目录（绝对路径）
SOURCE_PROJECT_DIR = r"C:\Godot\3d-practice"

# Kiro 工作空间目录（包含规则和文档）
KIRO_WORKSPACE_DIR = r"C:\Godot\KiroWorkingSpace\.kiro"

# KiroWorkingSpace 白名单：只包含这些子目录
KIRO_WHITELIST_DIRS = ['steering', 'docs', 'specs']

# KiroWorkingSpace 白名单：根目录的这些文件
KIRO_WHITELIST_FILES = ['ProjectRules.md', 'docLastConversationState.md', 'ConversationReset.md']

# 你的 Google Drive 本地映射文件夹路径
# 注意：Google Drive 桌面版通常映射为 "G:\My Drive\"
# 如果你的路径不同，请修改这里
DRIVE_SYNC_PATH = r"G:\My Drive\Kiro_Godot_Brain"

# AI 不需要看的"泥沙"后缀
IGNORE_EXTENSIONS = (
    '.png', '.jpg', '.jpeg', '.svg', '.webp', '.ico',
    '.ogg', '.wav', '.mp3', '.aac', '.flac',
    '.glb', '.gltf', '.fbx', '.obj', '.blend',
    '.dll', '.so', '.a', '.pdb', '.dylib',
    '.res', '.spv', '.uid', '.import',
    '.exe', '.bin', '.dat', '.cache'
)

# AI 不需要看的"下水道"目录
IGNORE_DIRS = (
    '.godot', '.git', '.vs', '.idea', '.vscode',
    'bin', 'obj', 'Export', 'Builds', 'Library',
    'Temp', 'node_modules', '__pycache__',
    '.backup_old_components', 'NVIDIA Corporation',
    'AnimationFBX', 'Animations'  # 动画和模型资源目录
)

def is_ignored(file_name, root_path):
    """检查文件或路径是否应该被忽略"""
    if file_name.endswith(IGNORE_EXTENSIONS):
        return True
    
    # 将路径统一为正斜杠以便精确匹配目录名
    normalized_path = root_path.replace('\\', '/')
    path_parts = normalized_path.split('/')
    
    for ignored_dir in IGNORE_DIRS:
        if ignored_dir in path_parts:
            return True
    
    return False

def build_pure_code_package():
    """将所有纯代码合并为单一文本文件，喂给 AI 瞬间消化！"""
    print("🌊 [Kiro Sync] 启动终极融合器，准备合成 100% 纯度上下文砖块...")
    print(f"📂 [Kiro Sync] 源项目目录: {SOURCE_PROJECT_DIR}")
    print(f"📂 [Kiro Sync] Kiro 规则目录: {KIRO_WORKSPACE_DIR}")
    
    # 检查源目录是否存在
    source_path = Path(SOURCE_PROJECT_DIR)
    if not source_path.exists():
        print(f"❌ 错误: 找不到源项目目录 '{SOURCE_PROJECT_DIR}'")
        print("💡 请检查 SOURCE_PROJECT_DIR 配置是否正确")
        input("\n按 Enter 键退出...")
        return
    
    kiro_path = Path(KIRO_WORKSPACE_DIR)
    if not kiro_path.exists():
        print(f"⚠️  警告: 找不到 Kiro 工作空间 '{KIRO_WORKSPACE_DIR}'")
        print("💡 将只同步项目代码，不包含规则文档")
        kiro_path = None
    
    # 确定目标路径
    drive_path = Path(DRIVE_SYNC_PATH)
    
    # 创建目标文件夹
    if not drive_path.exists():
        print(f"📁 [Kiro Sync] 创建目标文件夹: {DRIVE_SYNC_PATH}")
        try:
            drive_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"❌ 无法创建目录: {e}")
            print("💡 将在源项目目录生成文件")
            drive_path = source_path
    
    # 清理旧文件：移动到备份文件夹（放在外面）
    backup_folder = drive_path.parent / "Kiro_Godot_Brain_Backup"
    if drive_path.exists():
        existing_files = list(drive_path.glob("AI_Context_Master_*.txt"))
        if existing_files:
            print(f"🗂️  [Kiro Sync] 发现 {len(existing_files)} 个旧文件，移动到备份文件夹...")
            backup_folder.mkdir(exist_ok=True)
            for old_file in existing_files:
                try:
                    shutil.move(str(old_file), str(backup_folder / old_file.name))
                    print(f"   ✅ 已备份: {old_file.name}")
                except Exception as e:
                    print(f"   ⚠️  备份失败: {old_file.name} - {e}")
    
    # 核心：生成单一巨无霸文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    master_file_name = f"AI_Context_Master_{timestamp}.txt"
    final_output_path = drive_path / master_file_name
    
    added_files_count = 0
    total_lines = 0
    skipped_files_count = 0
    
    print(f"🔍 [Kiro Sync] 开始扫描并融合代码...")
    
    # 用 utf-8 编码打开单一文件，准备疯狂写入
    try:
        with open(final_output_path, 'w', encoding='utf-8') as master_file:
            master_file.write("# 🤖 Godot Sensei 专属项目上下文库\n")
            master_file.write("# 包含所有核心 C# 脚本、场景、配置和项目规则\n")
            master_file.write(f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # ========== 第一部分：Kiro 规则和文档 ==========
            if kiro_path:
                master_file.write("\n" + "=" * 80 + "\n")
                master_file.write("📚 SECTION 1: KIRO WORKSPACE - 项目规则与架构文档\n")
                master_file.write("=" * 80 + "\n\n")
                
                # 处理根目录的白名单文件
                for filename in KIRO_WHITELIST_FILES:
                    file_path = kiro_path / filename
                    if file_path.exists():
                        master_file.write("\n" + "=" * 80 + "\n")
                        master_file.write(f"📂 FILE: .kiro/{filename}\n")
                        master_file.write("=" * 80 + "\n\n")
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                master_file.write(content)
                                if not content.endswith('\n'):
                                    master_file.write('\n')
                                master_file.write('\n')
                                total_lines += content.count('\n')
                                added_files_count += 1
                        except Exception as e:
                            master_file.write(f"// [文件读取失败: {e}]\n\n")
                
                # 处理白名单子目录
                for whitelist_dir in KIRO_WHITELIST_DIRS:
                    dir_path = kiro_path / whitelist_dir
                    if dir_path.exists():
                        for root, dirs, files in os.walk(dir_path):
                            for file in files:
                                if file.endswith(('.md', '.json', '.txt')):
                                    file_path = Path(root) / file
                                    rel_path = file_path.relative_to(kiro_path)
                                    
                                    master_file.write("\n" + "=" * 80 + "\n")
                                    master_file.write(f"📂 FILE: .kiro/{rel_path}\n")
                                    master_file.write("=" * 80 + "\n\n")
                                    
                                    try:
                                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                            content = f.read()
                                            master_file.write(content)
                                            if not content.endswith('\n'):
                                                master_file.write('\n')
                                            master_file.write('\n')
                                            total_lines += content.count('\n')
                                            added_files_count += 1
                                    except Exception as e:
                                        master_file.write(f"// [文件读取失败: {e}]\n\n")
            
            # ========== 第二部分：3d-practice 项目代码 ==========
            master_file.write("\n" + "=" * 80 + "\n")
            master_file.write("💻 SECTION 2: 3D-PRACTICE PROJECT - 项目源代码\n")
            master_file.write("=" * 80 + "\n\n")
            
            # 遍历源目录
            for root, dirs, files in os.walk(source_path):
                # 过滤掉忽略的目录
                dirs[:] = [d for d in dirs if not is_ignored(d, os.path.join(root, d))]
                
                if is_ignored("", root):
                    continue
                
                for file in files:
                    if is_ignored(file, root):
                        skipped_files_count += 1
                        continue
                    
                    # 只处理纯代码和配置文件
                    if file.endswith(('.cs', '.gd', '.tscn', '.tres', '.md', '.json', '.cfg', '.xml', '.txt', '.csproj', '.sln', '.editorconfig')):
                        file_path = Path(root) / file
                        rel_path = file_path.relative_to(source_path)
                        
                        # 为 AI 写入醒目的文件分隔符和路径
                        master_file.write("\n" + "=" * 80 + "\n")
                        master_file.write(f"📂 FILE: 3d-practice/{rel_path}\n")
                        master_file.write("=" * 80 + "\n\n")
                        
                        # 读取文件内容并写入
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                master_file.write(content)
                                if not content.endswith('\n'):
                                    master_file.write('\n')
                                master_file.write('\n')
                                total_lines += content.count('\n')
                                added_files_count += 1
                                
                                # 每 50 个文件显示一次进度
                                if added_files_count % 50 == 0:
                                    print(f"   已融合 {added_files_count} 个文件...")
                        except Exception as e:
                            master_file.write(f"// [文件读取失败: {e}]\n\n")
                            print(f"   ⚠️  读取失败: {file} - {e}")
        
        file_size_mb = final_output_path.stat().st_size / (1024 * 1024)
        
        print(f"\n✅ [Kiro Sync] 融合成功！")
        print(f"   📊 将 {added_files_count} 个文件融合成了一块 {file_size_mb:.2f} MB 的砖块！")
        print(f"   📜 包含纯代码约 {total_lines:,} 行")
        print(f"   🗑️  已过滤 {skipped_files_count} 个噪音文件")
        print(f"   🚀 已输出至: {final_output_path}")
        print("\n✨ 现在，去 Gemini 的自定义 Gem 里，只关联这一个 TXT 文件即可！")
        print("💡 删除之前的文件夹，只选择这个单一文件作为 Knowledge 源")
        
    except Exception as e:
        print(f"❌ [Kiro Sync] 融合失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    try:
        build_pure_code_package()
    except Exception as e:
        print(f"❌ [Kiro Sync] 错误: {e}")
        import traceback
        traceback.print_exc()
        input("\n按 Enter 键退出...")
