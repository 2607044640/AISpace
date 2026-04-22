import os
import shutil
from pathlib import Path
from datetime import datetime
import hashlib
import json
import difflib
from collections import deque

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

# 3d-practice 项目白名单：以这些前缀开头的文件夹完整包含（不受大小限制）
# 
# 📌 设计理念：
# 用户使用 A1/B1 前缀标记自己创建的内容（插件、场景、脚本）
# 这些文件夹应该被完整包含，即使某些文件超过大小限制
# 
# 示例：
# - A1TetrisBackpack/ (背包系统插件)
# - A1UIPresets/ (UI 预设)
# - B1Scripts/ (核心脚本)
# - addons/A1TetrisBackpack/ (插件代码)
#
# 🔧 如何添加新前缀：
# 如果你使用其他前缀标记自己的内容，添加到这里：
# PROJECT_WHITELIST_PREFIXES = ['A1', 'B1', 'MyPrefix']
#
PROJECT_WHITELIST_PREFIXES = ['A1', 'B1']

# 3d-practice 项目白名单：这些特定文件夹也完整包含
# 
# 📌 用于不符合前缀规则但仍然重要的文件夹
#
PROJECT_WHITELIST_DIRS = ['Scenes', 'Tests']

# 你的 Google Drive 本地映射文件夹路径
# 注意：Google Drive 桌面版路径取决于同步模式
# - Mirror files (镜像模式): C:\Users\[用户名]\My Drive\
# - Stream files (流式模式): G:\My Drive\
# 如果你的路径不同，请修改这里
DRIVE_SYNC_PATH = r"C:\Users\26070\My Drive\Kiro_Godot_Brain"

# 本地备份文件夹（不上传到 Google Drive）
# 用于存放：旧的合并文件、清单文件（Manifest）、完整合并文件（用于 diff）
LOCAL_BACKUP_PATH = r"D:\Kiro_Godot_Brain_Backup"

# ==========================================
# 📂 文件分类配置（可扩展架构）
# ==========================================
#
# 设计理念：将项目文件按重要性和功能分类，生成多个小文件供 AI 选择性查看
# 
# 分类策略：
# 1. ImportantRules - 核心规则文件（MainRules.md, DesignPatterns.md）
# 2. OtherRules - 其他规则和文档（steering, docs, specs 中的其他文件）
# 3. A1_Components - 用户自定义 A1 前缀组件
# 4. B1_Components - 用户自定义 B1 前缀组件
# 5. ProjectCore - 项目核心文件（Scenes, Tests, 其他）
#
# 🔧 如何添加新分类：
# 在 FILE_CATEGORIES 字典中添加新条目，指定文件名和过滤条件
#
FILE_CATEGORIES = {
    'important_rules': {
        'filename': '01_ImportantRules.txt',
        'description': '核心规则文件',
        'files': ['steering/Always/MainRules.md', 'steering/Always/DesignPatterns.md']
    },
    'other_rules': {
        'filename': '02_OtherRules.txt',
        'description': '其他规则和文档',
        'exclude_files': ['steering/Always/MainRules.md', 'steering/Always/DesignPatterns.md']
    },
    'a1_components': {
        'filename': '03_A1_Components.txt',
        'description': 'A1 前缀组件',
        'prefix': 'A1'
    },
    'b1_components': {
        'filename': '04_B1_Components.txt',
        'description': 'B1 前缀组件',
        'prefix': 'B1'
    },
    'project_core': {
        'filename': '05_ProjectCore.txt',
        'description': '项目核心文件',
        'exclude_prefixes': ['A1', 'B1']
    }
}

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

def calculate_file_hash(file_path):
    """
    计算文件的 MD5 哈希值
    
    用于快速检测文件是否发生变化，避免逐行对比大文件
    """
    md5_hash = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            # 分块读取，避免大文件占用过多内存
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()
    except Exception as e:
        return None

def should_include_file(file_path):
    """
    检查文件是否应该包含在合并中（分级大小阈值策略）
    
    返回: (should_include: bool, reason: str)
    
    设计理念：
    - 不同文件类型有不同的价值密度
    - 大型场景文件通常是节点序列化数据，对理解架构无帮助
    - 纯代码文件超过 1MB 通常是机器生成或重复逻辑
    - 着色器和配置文件通常很小且信息密度高，不限制
    
    ⚠️ 重要：此函数不检查 CRITICAL_FILES 和白名单文件夹中的文件
    关键文件和白名单文件夹在调用此函数前已被跳过检查
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

def is_in_whitelist_folder(file_path, source_path):
    """
    检查文件是否在白名单文件夹中
    
    白名单文件夹的文件不受大小限制，完整包含
    
    参数:
        file_path: 文件的完整路径
        source_path: 项目根目录路径
    
    返回:
        bool: 是否在白名单文件夹中
    """
    try:
        rel_path = file_path.relative_to(source_path)
        path_parts = rel_path.parts
        
        if len(path_parts) == 0:
            return False
        
        # 检查顶层文件夹是否以白名单前缀开头
        top_folder = path_parts[0]
        for prefix in PROJECT_WHITELIST_PREFIXES:
            if top_folder.startswith(prefix):
                return True
        
        # 检查是否在显式白名单文件夹中
        if top_folder in PROJECT_WHITELIST_DIRS:
            return True
        
        # 检查 addons 子文件夹
        if top_folder == 'addons' and len(path_parts) > 1:
            addon_folder = path_parts[1]
            for prefix in PROJECT_WHITELIST_PREFIXES:
                if addon_folder.startswith(prefix):
                    return True
        
        return False
    except Exception:
        return False

def build_pure_code_package():
    """
    将所有纯代码合并为单一文本文件，喂给 AI 瞬间消化！
    
    工作流程：
    1. 扫描 KiroWorkingSpace/.kiro/ 中的规则和文档（白名单模式）
    2. 扫描 3d-practice/ 项目中的代码和配置（扩展名过滤 + 大小限制）
    3. 合并成单一 TXT 文件，使用清晰的分隔符
    4. 生成文件清单（Manifest）用于变更检测
    5. 对比上次清单，生成变更报告
    6. 旧文件备份到本地 D 盘（不上传到 Google Drive）
    7. 输出详细统计信息（文件数、行数、过滤原因）
    
    输出文件命名：AI_Context_Master_YYYYMMDD_HHMMSS.txt
    
    ⚠️ 注意事项：
    - 所有文件读取强制使用 UTF-8 编码（防止多语言注释崩溃）
    - 空文件会被跳过（节省分隔符空间）
    - 关键文件（CRITICAL_FILES）无视所有限制
    - 备份文件夹在 D:\Kiro_Godot_Brain_Backup（本地，不同步）
    - 变更检测：对比文件哈希，只对变化的文件生成 diff
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
    backup_folder = Path(LOCAL_BACKUP_PATH)
    backup_folder.mkdir(exist_ok=True)
    
    if drive_path.exists():
        existing_files = list(drive_path.glob("AI_Context_Master_*.txt"))
        if existing_files:
            print(f"🗂️  [Kiro Sync] 发现 {len(existing_files)} 个旧文件，移动到本地备份文件夹...")
            print(f"   📁 备份位置: {backup_folder}")
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
    
    # 文件清单（用于变更检测）
    current_manifest = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'files': {}
    }
    
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
                                
                                # 记录到清单（用于变更检测）
                                file_hash = calculate_file_hash(file_path)
                                if file_hash:
                                    current_manifest['files'][f'.kiro/{filename}'] = {
                                        'hash': file_hash,
                                        'size': file_path.stat().st_size,
                                        'content': content  # 保存内容用于生成 diff
                                    }
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
                                            
                                            # 记录到清单（用于变更检测）
                                            file_hash = calculate_file_hash(file_path)
                                            if file_hash:
                                                current_manifest['files'][str(rel_path)] = {
                                                    'hash': file_hash,
                                                    'size': file_path.stat().st_size,
                                                    'content': content  # 保存内容用于生成 diff
                                                }
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
                    
                    # 检查是否在白名单文件夹中（优先级第二）
                    file_path = Path(root) / file
                    is_whitelisted = is_in_whitelist_folder(file_path, source_path)
                    
                    # 只处理纯代码和配置文件（排除低价值文件）
                    # 关键文件和白名单文件无需检查扩展名
                    if is_critical or is_whitelisted or file.endswith(('.cs', '.gd', '.tscn', '.tres', '.md', '.json', '.cfg', '.xml', '.csproj', '.godot', '.gdshader', '.shader')):
                        
                        # 关键文件和白名单文件跳过大小检查
                        if not is_critical and not is_whitelisted:
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
                                
                                # 记录到清单（用于变更检测）
                                file_hash = calculate_file_hash(file_path)
                                if file_hash:
                                    current_manifest['files'][str(rel_path)] = {
                                        'hash': file_hash,
                                        'size': file_path.stat().st_size,
                                        'content': content  # 保存内容用于生成 diff
                                    }
                                
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
        
        # ========== 变更检测和报告生成 ==========
        print(f"\n🔄 [Change Detection] 开始变更检测...")
        
        # 清单文件保存到本地备份文件夹（不上传到 Google Drive）
        manifest_folder = Path(LOCAL_BACKUP_PATH)
        manifest_folder.mkdir(exist_ok=True)
        
        manifest_file = manifest_folder / "AI_Context_Manifest.json"
        try:
            with open(manifest_file, 'w', encoding='utf-8') as f:
                json.dump(current_manifest, f, indent=2, ensure_ascii=False)
            print(f"   ✅ 文件清单已保存: {manifest_file}")
        except Exception as e:
            print(f"   ⚠️  保存清单失败: {e}")
        
        # 读取上一次的清单
        previous_manifest_file = manifest_folder / "AI_Context_Manifest_Previous.json"
        previous_manifest = {}
        
        if previous_manifest_file.exists():
            try:
                with open(previous_manifest_file, 'r', encoding='utf-8') as f:
                    previous_manifest = json.load(f)
                print(f"   ✅ 已加载上次清单: {previous_manifest_file}")
            except Exception as e:
                print(f"   ⚠️  读取上次清单失败: {e}")
        else:
            print(f"   ℹ️  首次运行，没有上次清单")
        
        # 生成变更报告（变更文件保存到 Google Drive，供 AI 查看）
        if previous_manifest:
            has_changes, changes, detailed_diffs = generate_change_report(
                current_manifest, previous_manifest, drive_path
            )
            
            if has_changes:
                print(f"\n   📊 检测到变更:")
                print(f"      ✅ 新增: {len(changes['added'])} 个文件")
                print(f"      📝 修改: {len(changes['modified'])} 个文件")
                print(f"      ❌ 删除: {len(changes['deleted'])} 个文件")
                
                # 追加到变更历史文件（保存到 Google Drive）
                append_to_changes_file(changes, detailed_diffs, drive_path, timestamp)
            else:
                print(f"   ℹ️  没有检测到文件变更")
        
        # 备份当前清单为"上次清单"（保存到本地）
        try:
            shutil.copy(manifest_file, previous_manifest_file)
            print(f"   ✅ 清单已备份为上次清单")
        except Exception as e:
            print(f"   ⚠️  备份清单失败: {e}")
        
        print("\n✨ 现在，去 Gemini 的自定义 Gem 里，只关联这一个 TXT 文件即可！")
        print("💡 删除之前的文件夹，只选择这个单一文件作为 Knowledge 源")
        
    except Exception as e:
        print(f"❌ [Kiro Sync] 融合失败: {e}")
        import traceback
        traceback.print_exc()

def generate_change_report(current_manifest, previous_manifest, drive_path):
    """
    生成变更报告，对比当前和上一次的文件清单
    
    返回: (has_changes: bool, change_summary: dict, detailed_diffs: list)
    """
    changes = {
        'added': [],      # 新增的文件
        'modified': [],   # 修改的文件
        'deleted': []     # 删除的文件
    }
    
    detailed_diffs = []
    
    current_files = set(current_manifest.get('files', {}).keys())
    previous_files = set(previous_manifest.get('files', {}).keys())
    
    # 检测新增文件
    changes['added'] = list(current_files - previous_files)
    
    # 检测删除文件
    changes['deleted'] = list(previous_files - current_files)
    
    # 检测修改文件（哈希值不同）
    for file_path in current_files & previous_files:
        current_hash = current_manifest['files'][file_path]['hash']
        previous_hash = previous_manifest['files'][file_path]['hash']
        
        if current_hash != previous_hash:
            changes['modified'].append(file_path)
    
    # 生成详细 diff（只对修改的文件）
    print(f"\n🔍 [Change Detection] 生成详细变更对比...")
    for file_path in changes['modified'][:20]:  # 限制最多20个文件，避免过大
        try:
            # 读取当前文件内容
            current_content = current_manifest['files'][file_path].get('content', '')
            previous_content = previous_manifest['files'][file_path].get('content', '')
            
            if not current_content or not previous_content:
                continue
            
            # 生成 unified diff
            diff = list(difflib.unified_diff(
                previous_content.splitlines(keepends=True),
                current_content.splitlines(keepends=True),
                fromfile=f"a/{file_path}",
                tofile=f"b/{file_path}",
                lineterm='',
                n=5  # 上下文行数
            ))
            
            if diff:
                # 限制 diff 大小
                if len(diff) > 200:
                    diff = diff[:200] + [f"\n... (diff 太长，已截断，共 {len(diff)} 行变更)\n"]
                
                detailed_diffs.append({
                    'file': file_path,
                    'diff': ''.join(diff)
                })
        except Exception as e:
            print(f"   ⚠️  生成 diff 失败: {file_path} - {e}")
    
    has_changes = bool(changes['added'] or changes['modified'] or changes['deleted'])
    
    return has_changes, changes, detailed_diffs

def append_to_changes_file(changes, detailed_diffs, drive_path, timestamp):
    """
    将变更记录追加到 AI_Context_Changes.md 文件
    
    保留最近20次记录，超过的自动删除
    最新记录在最前面（倒序排列）
    最近5次用 <RECENT_CHANGES> 标记提升 AI 注意力
    """
    changes_file = drive_path / "AI_Context_Changes.md"
    
    # 读取现有记录
    existing_records = []
    if changes_file.exists():
        try:
            with open(changes_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # 移除标题和标记
                content = content.replace('# 🔄 AI Context 变更历史', '')
                content = content.replace('*保留最近 20 次变更记录，最新记录在最前面*', '')
                content = content.replace('<RECENT_CHANGES>', '')
                content = content.replace('</RECENT_CHANGES>', '')
                
                # 按分隔符拆分记录
                records = content.split('\n---\n')
                
                # 过滤掉空记录
                existing_records = [r.strip() for r in records if r.strip() and r.strip().startswith('##')]
        except Exception as e:
            print(f"   ⚠️  读取现有变更记录失败: {e}")
    
    # 生成新记录
    new_record = f"""## 📅 变更记录 - {timestamp}

### 📊 变更摘要
- ✅ 新增文件: {len(changes['added'])} 个
- 📝 修改文件: {len(changes['modified'])} 个
- ❌ 删除文件: {len(changes['deleted'])} 个

"""
    
    # 添加新增文件列表
    if changes['added']:
        new_record += "### ➕ 新增文件\n"
        for file_path in changes['added'][:10]:  # 最多显示10个
            new_record += f"- `{file_path}`\n"
        if len(changes['added']) > 10:
            new_record += f"- ... 还有 {len(changes['added']) - 10} 个文件\n"
        new_record += "\n"
    
    # 添加删除文件列表
    if changes['deleted']:
        new_record += "### ➖ 删除文件\n"
        for file_path in changes['deleted'][:10]:
            new_record += f"- `{file_path}`\n"
        if len(changes['deleted']) > 10:
            new_record += f"- ... 还有 {len(changes['deleted']) - 10} 个文件\n"
        new_record += "\n"
    
    # 添加详细 diff
    if detailed_diffs:
        new_record += "### 🔍 详细变更对比\n\n"
        for diff_info in detailed_diffs[:10]:  # 最多显示10个文件的 diff
            new_record += f"#### 📄 {diff_info['file']}\n\n"
            new_record += "```diff\n"
            new_record += diff_info['diff']
            new_record += "\n```\n\n"
        
        if len(detailed_diffs) > 10:
            new_record += f"*... 还有 {len(detailed_diffs) - 10} 个文件的变更未显示*\n\n"
    
    # 使用 deque 管理最近20次记录
    # existing_records 已经是按时间倒序（最新在前）
    records_queue = deque(existing_records, maxlen=20)
    
    # 把新记录加到开头（最新的位置）
    records_queue.appendleft(new_record)
    
    # 直接转换为列表，不需要反转
    records_list = list(records_queue)
    
    # 写入文件
    try:
        with open(changes_file, 'w', encoding='utf-8') as f:
            f.write("# 🔄 AI Context 变更历史\n\n")
            f.write("*保留最近 20 次变更记录，最新记录在最前面*\n\n")
            f.write("---\n\n")
            
            # 前5次用 <RECENT_CHANGES> 标记
            if len(records_list) > 0:
                f.write("<RECENT_CHANGES>\n\n")
                recent_records = records_list[:5]
                f.write('\n---\n\n'.join(recent_records))
                f.write("\n\n</RECENT_CHANGES>\n\n")
                
                # 剩余记录
                if len(records_list) > 5:
                    f.write("---\n\n")
                    older_records = records_list[5:]
                    f.write('\n---\n\n'.join(older_records))
            else:
                f.write('\n---\n\n'.join(records_list))
        
        print(f"   ✅ 变更记录已保存: {changes_file}")
        print(f"   📊 当前保留 {len(records_list)} 次历史记录（最近 {min(5, len(records_list))} 次已标记为重点）")
    except Exception as e:
        print(f"   ❌ 保存变更记录失败: {e}")

if __name__ == '__main__':
    try:
        build_pure_code_package()
    except Exception as e:
        print(f"❌ [Kiro Sync] 错误: {e}")
        import traceback
        traceback.print_exc()
        input("\n按 Enter 键退出...")
