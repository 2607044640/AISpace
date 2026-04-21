import os
import shutil
from pathlib import Path
from datetime import datetime

# ==========================================
# ⚙️ KIRO 的配置区
# ==========================================
# 
# 📌 脚本目的：
# 将 Godot 项目的所有代码、配置、规则文档合并成单一 TXT 文件，供 AI (Gemini/Claude) 消化。
# 这是一个 RAG (Retrieval-Augmented Generation) 系统的数据预处理脚本。
#
# 🎯 核心设计原则：
# 1. 高信噪比：只包含对 AI 理解项目有价值的文件
# 2. 分级过滤：不同文件类型使用不同的大小阈值
# 3. 关键文件优先：某些小文件虽小但极其重要（如 project.godot）
# 4. 避免序列化数据：大型场景文件通常是节点序列化，对理解架构无帮助
#
# ⚠️ 重要注意事项：
# - 备份文件夹在本地 D 盘，不会上传到 Google Drive（节省同步时间）
# - 关键文件（CRITICAL_FILES）无视大小限制，确保重要配置不被遗漏
# - .tres 文件受 200KB 限制，如有重要数据资源请加入 CRITICAL_FILES
# - 强制使用 UTF-8 编码，防止多语言注释导致崩溃
#
# 🔧 如何添加关键文件：
# 如果你的项目有重要的大型配置文件（如 ItemDatabase.tres），请添加到 CRITICAL_FILES 集合中。
# 关键文件会跳过所有大小和扩展名检查，无条件包含在合并文件中。
#
# ==========================================

# 你的 Godot 项目源目录（绝对路径）
SOURCE_PROJECT_DIR = r"C:\Godot\3d-practice"

# Kiro 工作空间目录（包含规则和文档）
KIRO_WORKSPACE_DIR = r"C:\Godot\KiroWorkingSpace\.kiro"

# KiroWorkingSpace 白名单：只包含这些子目录
# 
# 📌 为什么排除 Scratchpad？
# Scratchpad 是"工作记忆"目录，包含：
# - 临时 Bug 修复记录（已修复的问题）
# - 调试日志和思考过程
# - 一次性的分析报告
# 这些内容对 AI 理解当前代码架构没有帮助，反而会引入噪音。
# 
# 如果 Scratchpad 中有重要的架构决策，应该提炼后移到 docs/ 或 steering/ 目录。
#
KIRO_WHITELIST_DIRS = ['steering', 'docs', 'specs']

# KiroWorkingSpace 白名单：根目录的这些文件
KIRO_WHITELIST_FILES = ['ProjectRules.md', 'docLastConversationState.md', 'ConversationReset.md']

# 你的 Google Drive 本地映射文件夹路径
# 注意：Google Drive 桌面版路径取决于同步模式
# - Mirror files (镜像模式): C:\Users\[用户名]\My Drive\
# - Stream files (流式模式): G:\My Drive\
# 如果你的路径不同，请修改这里
DRIVE_SYNC_PATH = r"C:\Users\26070\My Drive\Kiro_Godot_Brain"

# ==========================================
# 🎯 文件大小阈值配置（分级策略）
# ==========================================
# 
# 设计理由：
# - 纯代码文件（.cs, .gd）：超过 1MB 通常是机器生成或包含大量重复逻辑，阅读价值递减
# - Godot 资源文件（.tscn, .tres, .json）：超过 200KB 几乎全是节点序列化数据，对理解架构无帮助
# - 着色器文件（.gdshader, .shader）：通常很小，包含视觉逻辑，不限制
# - 配置文件（.cfg, .xml, .godot）：通常很小且信息密度高，不限制
#
# ⚠️ 特别说明：
# .tres 文件有两种用途：
# 1. 场景资源（材质、网格）→ 通常是序列化数据，应该限制
# 2. 数据资源（ItemDatabase.tres）→ 可能是手写配置，如果重要请加入 CRITICAL_FILES
#
CODE_MAX_SIZE_MB = 1.0       # 纯代码文件最大 1MB
RESOURCE_MAX_SIZE_MB = 0.2   # 场景/资源文件最大 200KB

# ==========================================
# 🚫 文件过滤配置
# ==========================================
#
# 过滤策略（四层防御）：
# 第一层：关键文件白名单（CRITICAL_FILES）→ 无条件包含，跳过所有检查
# 第二层：扩展名白名单 → 基础过滤，只处理代码和配置文件
# 第三层：大小阈值检查 → 分级限制，防止序列化数据污染
# 第四层：文件名黑名单 → 排除法律文本和临时文件
#
# AI 不需要看的"泥沙"后缀（二进制和资源文件）
IGNORE_EXTENSIONS = (
    '.png', '.jpg', '.jpeg', '.svg', '.webp', '.ico',
    '.ogg', '.wav', '.mp3', '.aac', '.flac',
    '.glb', '.gltf', '.fbx', '.obj', '.blend',
    '.dll', '.so', '.a', '.pdb', '.dylib',
    '.res', '.spv', '.uid', '.import',
    '.exe', '.bin', '.dat', '.cache'
)

# 低价值文件类型（IDE 配置和编辑器设置）
EXCLUDE_EXTENSIONS = (
    '.sln',              # Visual Studio Solution 文件
    '.editorconfig',     # 编辑器格式化规则
    '.user',             # 用户特定配置
    '.DotSettings.user'  # Rider 用户配置
)

# 特定文件名黑名单（法律文本和临时文件）
FILENAME_BLACKLIST = {
    'LICENSE.txt', 'LICENSE', 'COPYING.txt', 'COPYING',
    'test_paths.txt', 'debug.txt', 'temp.txt', 'log.txt'
}

# 关键配置文件白名单（即使不在扩展名白名单中也要包含）
# 
# ⭐ 这些文件虽小但极其重要，无视大小和扩展名限制
# 
# 为什么需要这个白名单？
# - project.godot：包含 InputMap（按键映射）和 Autoload（全局单例），AI 必须理解
# - default_bus_layout.tres：音频总线配置，理解音效系统的关键
# - .gitignore：反映项目结构，帮助 AI 区分源码和生成文件
#
# 🔧 如何添加你的关键文件：
# 如果你有重要的大型数据文件（如 ItemDatabase.tres 超过 200KB），请添加到这里：
# CRITICAL_FILES = {
#     'project.godot',
#     'default_bus_layout.tres',
#     '.gitignore',
#     '.gitattributes',
#     'YourImportantFile.tres',  # 👈 在这里添加
# }
#
CRITICAL_FILES = {
    'project.godot',           # Godot 项目配置（InputMap, Autoload）
    'default_bus_layout.tres', # 音频总线配置
    '.gitignore',              # Git 忽略规则（反映项目结构）
    '.gitattributes'           # Git 属性配置
}

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

def should_include_file(file_path):
    """
    检查文件是否应该包含在合并中（分级大小阈值策略）
    
    返回: (should_include: bool, reason: str)
    
    设计理念：
    - 不同文件类型有不同的价值密度
    - 大型场景文件通常是节点序列化数据，对理解架构无帮助
    - 纯代码文件超过 1MB 通常是机器生成或重复逻辑
    - 着色器和配置文件通常很小且信息密度高，不限制
    
    ⚠️ 重要：此函数不检查 CRITICAL_FILES 中的文件
    关键文件在调用此函数前已被跳过检查
    """
    file_name = file_path.name
    file_suffix = file_path.suffix.lower()
    
    # 检查文件名黑名单
    if file_name in FILENAME_BLACKLIST:
        return False, f"文件名黑名单: {file_name}"
    
    # 检查排除的扩展名
    if file_suffix in EXCLUDE_EXTENSIONS:
        return False, f"低价值文件类型: {file_suffix}"
    
    # 获取文件大小
    try:
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
    except Exception as e:
        return False, f"无法读取文件大小: {e}"
    
    # 分级阈值检查
    if file_suffix in ['.tscn', '.tres', '.json']:
        # Godot 资源文件：严格限制（200KB）
        # 注意：.tres 包含场景资源和数据资源
        # - 场景资源（如材质、网格）：通常是序列化数据，应该限制
        # - 数据资源（如 ItemDatabase.tres）：可能是手写配置，如果重要请加入 CRITICAL_FILES
        if file_size_mb > RESOURCE_MAX_SIZE_MB:
            return False, f"资源文件过大 ({file_size_mb:.2f} MB > {RESOURCE_MAX_SIZE_MB} MB)"
    
    elif file_suffix in ['.cs', '.gd']:
        # 纯代码文件：适度限制（1MB）
        if file_size_mb > CODE_MAX_SIZE_MB:
            return False, f"代码文件过大 ({file_size_mb:.2f} MB > {CODE_MAX_SIZE_MB} MB)"
    
    elif file_suffix in ['.gdshader', '.shader']:
        # 着色器文件：通常很小，不限制
        # 包含视觉特效代码（高亮、描边、水体等）
        pass
    
    # 其他文件类型（.md, .cfg, .xml, .csproj, .godot）不限制大小
    return True, ""

def build_pure_code_package():
    """
    将所有纯代码合并为单一文本文件，喂给 AI 瞬间消化！
    
    工作流程：
    1. 扫描 KiroWorkingSpace/.kiro/ 中的规则和文档（白名单模式）
    2. 扫描 3d-practice/ 项目中的代码和配置（扩展名过滤 + 大小限制）
    3. 合并成单一 TXT 文件，使用清晰的分隔符
    4. 旧文件备份到本地 D 盘（不上传到 Google Drive）
    5. 输出详细统计信息（文件数、行数、过滤原因）
    
    输出文件命名：AI_Context_Master_YYYYMMDD_HHMMSS.txt
    
    ⚠️ 注意事项：
    - 所有文件读取强制使用 UTF-8 编码（防止多语言注释崩溃）
    - 空文件会被跳过（节省分隔符空间）
    - 关键文件（CRITICAL_FILES）无视所有限制
    - 备份文件夹在 D:\Kiro_Godot_Brain_Backup（本地，不同步）
    """
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
    
    # 清理旧文件：移动到本地备份文件夹（避免上传到 Google Drive）
    backup_folder = Path(r"D:\Kiro_Godot_Brain_Backup")
    if drive_path.exists():
        existing_files = list(drive_path.glob("AI_Context_Master_*.txt"))
        if existing_files:
            print(f"🗂️  [Kiro Sync] 发现 {len(existing_files)} 个旧文件，移动到本地备份文件夹...")
            print(f"   📁 备份位置: {backup_folder}")
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
    
    # 统计变量
    added_files_count = 0
    total_lines = 0
    skipped_files_count = 0
    
    # 分段统计
    section1_files = 0
    section1_lines = 0
    section2_files = 0
    section2_lines = 0
    
    # 过滤原因统计
    skip_reasons = {}
    
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
                                
                                # 跳过空文件
                                if not content.strip():
                                    skipped_files_count += 1
                                    skip_reasons['空文件'] = skip_reasons.get('空文件', 0) + 1
                                    continue
                                
                                master_file.write(content)
                                if not content.endswith('\n'):
                                    master_file.write('\n')
                                master_file.write('\n')
                                
                                lines = content.count('\n')
                                total_lines += lines
                                section1_lines += lines
                                added_files_count += 1
                                section1_files += 1
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
                                    
                                    # 检查文件名黑名单
                                    if file in FILENAME_BLACKLIST:
                                        skipped_files_count += 1
                                        skip_reasons['文件名黑名单'] = skip_reasons.get('文件名黑名单', 0) + 1
                                        continue
                                    
                                    rel_path = file_path.relative_to(kiro_path)
                                    
                                    master_file.write("\n" + "=" * 80 + "\n")
                                    master_file.write(f"📂 FILE: .kiro/{rel_path}\n")
                                    master_file.write("=" * 80 + "\n\n")
                                    
                                    try:
                                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                            content = f.read()
                                            
                                            # 跳过空文件
                                            if not content.strip():
                                                skipped_files_count += 1
                                                skip_reasons['空文件'] = skip_reasons.get('空文件', 0) + 1
                                                continue
                                            
                                            master_file.write(content)
                                            if not content.endswith('\n'):
                                                master_file.write('\n')
                                            master_file.write('\n')
                                            
                                            lines = content.count('\n')
                                            total_lines += lines
                                            section1_lines += lines
                                            added_files_count += 1
                                            section1_files += 1
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
                        skip_reasons['二进制/缓存文件'] = skip_reasons.get('二进制/缓存文件', 0) + 1
                        continue
                    
                    # 检查是否是关键配置文件（优先级最高）
                    is_critical = file in CRITICAL_FILES
                    
                    # 只处理纯代码和配置文件（排除低价值文件）
                    # 关键文件无需检查扩展名
                    if is_critical or file.endswith(('.cs', '.gd', '.tscn', '.tres', '.md', '.json', '.cfg', '.xml', '.csproj', '.godot', '.gdshader', '.shader')):
                        file_path = Path(root) / file
                        
                        # 关键文件跳过大小检查
                        if not is_critical:
                            # 应用分级大小阈值检查
                            should_include, reason = should_include_file(file_path)
                            if not should_include:
                                skipped_files_count += 1
                                # 统计跳过原因
                                skip_reasons[reason.split(':')[0]] = skip_reasons.get(reason.split(':')[0], 0) + 1
                                continue
                        
                        rel_path = file_path.relative_to(source_path)
                        
                        # 为 AI 写入醒目的文件分隔符和路径
                        master_file.write("\n" + "=" * 80 + "\n")
                        master_file.write(f"📂 FILE: 3d-practice/{rel_path}\n")
                        master_file.write("=" * 80 + "\n\n")
                        
                        # 读取文件内容并写入（强制 UTF-8 编码）
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                
                                # 跳过空文件
                                if not content.strip():
                                    skipped_files_count += 1
                                    skip_reasons['空文件'] = skip_reasons.get('空文件', 0) + 1
                                    continue
                                
                                master_file.write(content)
                                if not content.endswith('\n'):
                                    master_file.write('\n')
                                master_file.write('\n')
                                
                                lines = content.count('\n')
                                total_lines += lines
                                section2_lines += lines
                                added_files_count += 1
                                section2_files += 1
                                
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
        print(f"\n   📈 分段统计:")
        print(f"      Section 1 (规则文档): {section1_files} 文件, {section1_lines:,} 行")
        print(f"      Section 2 (项目代码): {section2_files} 文件, {section2_lines:,} 行")
        
        if skip_reasons:
            print(f"\n   🔍 过滤原因统计:")
            for reason, count in sorted(skip_reasons.items(), key=lambda x: x[1], reverse=True):
                print(f"      {reason}: {count} 个文件")
        
        print(f"\n   🚀 已输出至: {final_output_path}")
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
