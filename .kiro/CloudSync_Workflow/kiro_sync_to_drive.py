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
SOURCE_PROJECT_DIR = r"C:\Godot\3d-practice"
KIRO_WORKSPACE_DIR = r"C:\Godot\KiroWorkingSpace\.kiro"
DRIVE_SYNC_PATH = r"C:\Users\26070\My Drive\Kiro_Godot_Brain"
LOCAL_BACKUP_PATH = r"D:\Kiro_Godot_Brain_Backup"
LOCAL_HUMAN_VIEW_PATH = r"D:\A1GeminiSyncTestForHuman"  # 本地人类视图（5个分类文件）

KIRO_WHITELIST_DIRS = ['steering', 'docs', 'specs']
KIRO_WHITELIST_FILES = ['ProjectRules.md', 'docLastConversationState.md', 'ConversationReset.md']
PROJECT_WHITELIST_PREFIXES = ['A1', 'B1']
PROJECT_WHITELIST_DIRS = ['Scenes', 'Tests']

CODE_MAX_SIZE_MB = 1.0       # 纯代码文件最大 1MB
RESOURCE_MAX_SIZE_MB = 0.2   # 场景/资源文件最大 200KB

IGNORE_EXTENSIONS = (
    '.png', '.jpg', '.jpeg', '.svg', '.webp', '.ico',
    '.ogg', '.wav', '.mp3', '.aac', '.flac',
    '.glb', '.gltf', '.fbx', '.obj', '.blend',
    '.dll', '.so', '.a', '.pdb', '.dylib',
    '.res', '.spv', '.uid', '.import',
    '.exe', '.bin', '.dat', '.cache'
)

EXCLUDE_EXTENSIONS = ('.sln', '.editorconfig', '.user', '.DotSettings.user')

FILENAME_BLACKLIST = {
    'LICENSE.txt', 'LICENSE', 'COPYING.txt', 'COPYING',
    'test_paths.txt', 'debug.txt', 'temp.txt', 'log.txt'
}

CRITICAL_FILES = {
    'project.godot',
    'default_bus_layout.tres',
    '.gitignore',
    '.gitattributes'
}

IGNORE_DIRS = (
    '.godot', '.git', '.vs', '.idea', '.vscode',
    'bin', 'obj', 'Export', 'Builds', 'Library',
    'Temp', 'node_modules', '__pycache__',
    '.backup_old_components', 'NVIDIA Corporation',
    'AnimationFBX', 'Animations'
)

# ==========================================
# 🛠️ 核心辅助函数
# ==========================================

# 核心规则文件列表（最高优先级）
IMPORTANT_RULES_FILES = {
    'MainRules.md',
    'DesignPatterns.md',
    'ProjectRules.md',
    'ConversationReset.md',
    'docLastConversationState.md'
}

def classify_file_to_bucket(file_path, source_path, kiro_path):
    """
    将文件分类到5个桶之一
    
    优先级规则（从高到低）：
    1. 核心规则文件 → 01_important_rules
    2. 路径包含 A1 → 03_a1_components
    3. 路径包含 B1 → 04_b1_components
    4. .kiro/ 目录下 → 02_other_rules
    5. 其他 → 05_project_core
    
    返回: bucket_key (str)
    """
    file_name = file_path.name
    
    # 优先级1：核心规则文件
    if file_name in IMPORTANT_RULES_FILES:
        return '01_important_rules'
    
    # 获取相对路径字符串（兼容 Python 3.7+）
    try:
        if kiro_path:
            try:
                rel_path_str = str(file_path.relative_to(kiro_path)).replace('\\', '/')
                is_in_kiro = True
            except ValueError:
                is_in_kiro = False
        else:
            is_in_kiro = False
        
        if not is_in_kiro:
            try:
                rel_path_str = str(file_path.relative_to(source_path)).replace('\\', '/')
            except ValueError:
                rel_path_str = str(file_path)
    except:
        rel_path_str = str(file_path)
    
    # 优先级2：A1 组件
    if 'A1' in rel_path_str or '/A1' in rel_path_str or '\\A1' in str(file_path):
        return '03_a1_components'
    
    # 优先级3：B1 组件
    if 'B1' in rel_path_str or '/B1' in rel_path_str or '\\B1' in str(file_path):
        return '04_b1_components'
    
    # 优先级4：其他规则文件（检查是否在 kiro_path 下）
    if kiro_path and is_in_kiro:
        return '02_other_rules'
    
    # 优先级5：项目核心
    return '05_project_core'
def is_ignored(file_name, root_path):
    """
    Check if a file/directory should be ignored based on directory blacklist.
    Note: Extension-based filtering is handled separately in the binary indexing logic.
    """
    path_parts = root_path.replace('\\', '/').split('/')
    return any(ignored_dir in path_parts for ignored_dir in IGNORE_DIRS)

def is_binary_file(filepath):
    """
    终极防御：通过读取文件头部检测空字节，判断是否为真正的二进制文件。
    比扩展名检测可靠 100 倍。
    
    原理：文本文件极少包含真正的空字节 \x00
    """
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(1024)
            # 检测空字节
            if b'\x00' in chunk:
                return True
    except Exception:
        pass
    return False

def calculate_file_hash(file_path):
    md5_hash = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()
    except Exception:
        return None

def should_include_file(file_path):
    file_name = file_path.name
    file_suffix = file_path.suffix.lower()
    
    if file_name in FILENAME_BLACKLIST:
        return False, f"Blacklist: {file_name}"
    
    if file_suffix in EXCLUDE_EXTENSIONS:
        return False, f"Low-value type: {file_suffix}"
    
    try:
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
    except Exception as e:
        return False, f"Size read error: {e}"
    
    if file_suffix in ['.tscn', '.tres', '.json']:
        if file_size_mb > RESOURCE_MAX_SIZE_MB:
            return False, f"Resource too large ({file_size_mb:.2f}MB)"
    elif file_suffix in ['.cs', '.gd']:
        if file_size_mb > CODE_MAX_SIZE_MB:
            return False, f"Code too large ({file_size_mb:.2f}MB)"
    
    return True, ""

def is_in_whitelist_folder(file_path, source_path):
    try:
        rel_path = file_path.relative_to(source_path)
        path_parts = rel_path.parts
        
        if not path_parts:
            return False
        
        top_folder = path_parts[0]
        if any(top_folder.startswith(p) for p in PROJECT_WHITELIST_PREFIXES):
            return True
        
        if top_folder in PROJECT_WHITELIST_DIRS:
            return True
        
        if top_folder == 'addons' and len(path_parts) > 1:
            addon_folder = path_parts[1]
            if any(addon_folder.startswith(p) for p in PROJECT_WHITELIST_PREFIXES):
                return True
        
        return False
    except Exception:
        return False

# ==========================================
# 🚀 核心构建逻辑 (双路输出：AI 巨无霸 + 人类分类视图)
# ==========================================
def build_dual_sync():
    print("🌊 [Kiro Sync] 启动双路同步：AI 巨无霸 (云端) + 人类分类视图 (本地)...")
    
    source_path = Path(SOURCE_PROJECT_DIR)
    kiro_path = Path(KIRO_WORKSPACE_DIR)
    drive_path = Path(DRIVE_SYNC_PATH)
    human_path = Path(LOCAL_HUMAN_VIEW_PATH)
    
    if not source_path.exists():
        print(f"❌ 找不到源目录: {SOURCE_PROJECT_DIR}")
        return
    
    # 创建目标文件夹
    drive_path.mkdir(parents=True, exist_ok=True)
    human_path.mkdir(parents=True, exist_ok=True)
    
    # 备份旧文件
    backup_folder = Path(LOCAL_BACKUP_PATH)
    backup_folder.mkdir(exist_ok=True)
    
    # 清理云端旧的 Master 文件
    for old_file in drive_path.glob("AI_Context_Master_*.txt"):
        shutil.move(str(old_file), str(backup_folder / old_file.name))
    
    # 清理本地旧的分类文件
    for old_file in human_path.glob("*.txt"):
        old_file.unlink()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 初始化5个分类存储桶
    buckets = {
        '01_important_rules': [],
        '02_other_rules': [],
        '03_a1_components': [],
        '04_b1_components': [],
        '05_project_core': []
    }
    
    # Manifest 用于变更检测
    current_manifest = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'files': {}
    }
    
    print(f"🔍 [Kiro Sync] 开始单次扫描并分类...")
    
    # ========== 扫描 KiroWorkingSpace/.kiro/ ==========
    if kiro_path.exists():
        # 处理根目录白名单文件
        for filename in KIRO_WHITELIST_FILES:
            file_path = kiro_path / filename
            if file_path.exists():
                # 🛡️ 二进制雷达
                if is_binary_file(file_path):
                    file_size_kb = file_path.stat().st_size / 1024
                    stub_content = f'<binary_asset type="{file_path.suffix}" size_kb="{file_size_kb:.2f}" />\n'
                    process_file_to_bucket(file_path, f".kiro/{filename}", buckets, current_manifest, source_path, kiro_path, override_content=stub_content)
                    continue
                process_file_to_bucket(file_path, f".kiro/{filename}", buckets, current_manifest, source_path, kiro_path)
        
        # 处理白名单子目录
        for whitelist_dir in KIRO_WHITELIST_DIRS:
            dir_path = kiro_path / whitelist_dir
            if dir_path.exists():
                for root, _, files in os.walk(dir_path):
                    for file in files:
                        if file.endswith(('.md', '.json', '.txt')) and file not in FILENAME_BLACKLIST:
                            f_path = Path(root) / file
                            rel_path = f_path.relative_to(kiro_path)
                            
                            # 🛡️ 二进制雷达
                            if is_binary_file(f_path):
                                file_size_kb = f_path.stat().st_size / 1024
                                stub_content = f'<binary_asset type="{f_path.suffix}" size_kb="{file_size_kb:.2f}" />\n'
                                process_file_to_bucket(f_path, f".kiro/{rel_path}", buckets, current_manifest, source_path, kiro_path, override_content=stub_content)
                                continue
                            
                            process_file_to_bucket(f_path, f".kiro/{rel_path}", buckets, current_manifest, source_path, kiro_path)
    
    # ========== 扫描 3d-practice/ 项目 ==========
    for root, dirs, files in os.walk(source_path):
        dirs[:] = [d for d in dirs if not is_ignored(d, os.path.join(root, d))]
        if is_ignored("", root):
            continue
        
        for file in files:
            file_path = Path(root) / file
            rel_path = file_path.relative_to(source_path)
            
            # 检查是否是被忽略的目录中的文件
            if is_ignored(file, root):
                continue
            
            # 🛡️ 二进制雷达：检测二进制文件或被忽略的扩展名
            if is_binary_file(file_path) or file.endswith(IGNORE_EXTENSIONS):
                # 计算文件大小
                try:
                    file_size_kb = file_path.stat().st_size / 1024
                    file_ext = file_path.suffix.lower()
                    
                    # 构造二进制占位符（元数据索引）
                    stub_content = f'<binary_asset type="{file_ext}" size_kb="{file_size_kb:.2f}" />\n'
                    
                    # 记录到对应的桶（让 AI 知道这里有个资源文件）
                    process_file_to_bucket(file_path, f"3d-practice/{rel_path}", buckets, current_manifest, source_path, kiro_path, override_content=stub_content)
                except Exception:
                    pass
                continue
            
            # 🔪 第三方 Addons 绞肉机：只保留 A1/B1 自定义插件源码
            path_parts = rel_path.parts
            if len(path_parts) > 1 and path_parts[0] == 'addons':
                addon_name = path_parts[1]
                is_custom_addon = any(addon_name.startswith(p) for p in PROJECT_WHITELIST_PREFIXES)
                
                if not is_custom_addon:
                    # 第三方插件：只留墓碑，不读源码
                    stub_content = f'<third_party_addon name="{addon_name}" />\n'
                    try:
                        process_file_to_bucket(file_path, f"3d-practice/{rel_path}", buckets, current_manifest, source_path, kiro_path, override_content=stub_content)
                    except Exception:
                        pass
                    continue
            
            is_critical = file in CRITICAL_FILES
            is_whitelisted = is_in_whitelist_folder(file_path, source_path)
            
            # 白名单文件也必须是代码/文本后缀
            valid_extensions = ('.cs', '.gd', '.tscn', '.tres', '.md', '.json', '.cfg', '.xml', '.csproj', '.godot', '.gdshader', '.shader')
            
            if is_critical or file.endswith(valid_extensions):
                if not is_critical and not is_whitelisted:
                    should_include, _ = should_include_file(file_path)
                    if not should_include:
                        continue
                
                process_file_to_bucket(file_path, f"3d-practice/{rel_path}", buckets, current_manifest, source_path, kiro_path)
    
    # 统计
    total_files = sum(len(bucket) for bucket in buckets.values())
    print(f"\n📊 [Kiro Sync] 扫描完成，共分类 {total_files} 个文件")
    for key, bucket in buckets.items():
        print(f"   {key}: {len(bucket)} 个文件")
    
    # 读取变更记录
    changes_file = drive_path / "AI_Context_Changes.md"
    recent_changes_content = ""
    if changes_file.exists():
        with open(changes_file, 'r', encoding='utf-8') as f:
            recent_changes_content = f.read()
    
    # ========== 输出 A：云端 AI 巨无霸 (单一 XML 文件) ==========
    print(f"\n📝 [Kiro Sync] 生成云端 AI 巨无霸...")
    master_file = drive_path / f"AI_Context_Master_{timestamp}.txt"
    
    with open(master_file, 'w', encoding='utf-8') as f:
        f.write("<system_context>\n")
        f.write("  <metadata>\n")
        f.write("    <description>Godot Sensei Project Context Master File (Dual-Sync)</description>\n")
        f.write(f"    <generated_time>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</generated_time>\n")
        f.write("  </metadata>\n\n")
        
        # 按顺序拼接所有桶的内容
        bucket_names = {
            '01_important_rules': 'Important Rules',
            '02_other_rules': 'Other Rules',
            '03_a1_components': 'A1 Components',
            '04_b1_components': 'B1 Components',
            '05_project_core': 'Project Core'
        }
        
        for key in sorted(buckets.keys()):
            f.write(f"  <section name='{key}' description='{bucket_names[key]}'>\n")
            for xml_content in buckets[key]:
                f.write(xml_content)
            f.write(f"  </section>\n\n")
        
        # 变更日志永远放在最后
        f.write("  <section name='06_recent_changes' description='Recent Changes'>\n")
        if recent_changes_content:
            f.write("    <![CDATA[\n")
            f.write(recent_changes_content)
            f.write("    ]]>\n")
        else:
            f.write("    <no_recent_changes />\n")
        f.write("  </section>\n")
        
        f.write("</system_context>\n")
    
    master_size_mb = master_file.stat().st_size / (1024 * 1024)
    print(f"   ✅ 云端文件: {master_file.name} ({master_size_mb:.2f} MB)")
    
    # ========== 输出 B：本地人类分类视图 (5个独立文件) ==========
    print(f"\n📝 [Kiro Sync] 生成本地人类分类视图...")
    
    bucket_descriptions = {
        '01_important_rules': '核心规则文件 (MainRules, DesignPatterns, ProjectRules 等)',
        '02_other_rules': '其他规则和文档 (steering, docs, specs)',
        '03_a1_components': 'A1 前缀组件 (用户自定义)',
        '04_b1_components': 'B1 前缀组件 (用户自定义)',
        '05_project_core': '项目核心文件 (Scenes, Tests, 其他源码)'
    }
    
    for key, content_list in buckets.items():
        if not content_list:
            continue
        
        local_file = human_path / f"{key}.txt"
        with open(local_file, 'w', encoding='utf-8') as f:
            f.write(f"# HUMAN VIEW - CATEGORY: {key}\n")
            f.write(f"# {bucket_descriptions[key]}\n")
            f.write(f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# 文件数量: {len(content_list)}\n\n")
            f.write("=" * 80 + "\n\n")
            
            for xml_content in content_list:
                f.write(xml_content)
        
        local_size_mb = local_file.stat().st_size / (1024 * 1024)
        print(f"   ✅ {key}.txt ({local_size_mb:.2f} MB, {len(content_list)} 文件)")
    
    # ========== 处理 Manifest 与变更检测 ==========
    process_manifest_and_changes(current_manifest, backup_folder, drive_path, timestamp)
    
    print(f"\n✨ [Kiro Sync] 双路同步完成！")
    print(f"   🌐 云端 (AI): {master_file}")
    print(f"   🏠 本地 (人): {human_path}")

def process_file_to_bucket(file_path, virtual_path, buckets, manifest_dict, source_path, kiro_path, override_content=None):
    """
    处理单个文件：读取内容，分类到桶，记录到 Manifest
    
    参数:
        override_content: 如果提供，则使用该内容而不是读取文件（用于二进制文件占位符）
    """
    try:
        # 如果提供了覆盖内容（二进制占位符），直接使用
        if override_content is not None:
            content = override_content
            priority = "ASSET_INDEX"
        else:
            # 正常读取文本文件
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            if not content.strip():
                return  # 跳过空文件
            
            # 确定优先级
            file_name = file_path.name
            if file_name in IMPORTANT_RULES_FILES or file_name in CRITICAL_FILES:
                priority = "CRITICAL"
            elif file_name in KIRO_WHITELIST_FILES:
                priority = "HIGH"
            else:
                priority = "NORMAL"
        
        # 生成 XML 格式的内容
        xml_content = f'    <file path="{virtual_path}" priority="{priority}">\n'
        
        # 对于占位符内容，直接写入（已经是 XML 格式）
        if override_content is not None:
            xml_content += override_content
        else:
            # 对于正常内容，使用 CDATA 包裹
            xml_content += "<![CDATA[\n"
            xml_content += content
            if not content.endswith('\n'):
                xml_content += '\n'
            xml_content += "]]>\n"
        
        xml_content += "    </file>\n\n"
        
        # 分类到对应的桶
        bucket_key = classify_file_to_bucket(file_path, source_path, kiro_path)
        buckets[bucket_key].append(xml_content)
        
        # 记录到 Manifest（只记录真实文件，不记录占位符）
        if override_content is None:
            f_hash = calculate_file_hash(file_path)
            if f_hash:
                manifest_dict['files'][str(virtual_path)] = {
                    'hash': f_hash,
                    'size': file_path.stat().st_size,
                    'content': content
                }
    
    except Exception as e:
        # 错误文件也要记录
        xml_content = f'    <file path="{virtual_path}" error="{str(e)}" />\n'
        bucket_key = classify_file_to_bucket(file_path, source_path, kiro_path)
        buckets[bucket_key].append(xml_content)

def process_manifest_and_changes(current_manifest, backup_folder, drive_path, timestamp):
    manifest_file = backup_folder / "AI_Context_Manifest.json"
    previous_manifest_file = backup_folder / "AI_Context_Manifest_Previous.json"
    
    # 保存当前 Manifest
    with open(manifest_file, 'w', encoding='utf-8') as f:
        json.dump(current_manifest, f, indent=2, ensure_ascii=False)
    
    previous_manifest = {}
    if previous_manifest_file.exists():
        with open(previous_manifest_file, 'r', encoding='utf-8') as f:
            previous_manifest = json.load(f)
    
    if previous_manifest:
        has_changes, changes, detailed_diffs = generate_change_report(current_manifest, previous_manifest)
        if has_changes:
            append_to_changes_file(changes, detailed_diffs, drive_path, timestamp)
    
    shutil.copy(manifest_file, previous_manifest_file)

def generate_change_report(current_manifest, previous_manifest):
    changes = {'added': [], 'modified': [], 'deleted': []}
    detailed_diffs = []
    
    curr_files = set(current_manifest.get('files', {}).keys())
    prev_files = set(previous_manifest.get('files', {}).keys())
    
    changes['added'] = list(curr_files - prev_files)
    changes['deleted'] = list(prev_files - curr_files)
    
    for file_path in curr_files & prev_files:
        if current_manifest['files'][file_path]['hash'] != previous_manifest['files'][file_path]['hash']:
            changes['modified'].append(file_path)
    
    for file_path in changes['modified'][:20]:
        curr_content = current_manifest['files'][file_path].get('content', '')
        prev_content = previous_manifest['files'][file_path].get('content', '')
        
        diff = list(difflib.unified_diff(
            prev_content.splitlines(keepends=True),
            curr_content.splitlines(keepends=True),
            n=5
        ))
        
        if diff:
            if len(diff) > 200:
                diff = diff[:200] + [f"\n... (diff截断, 共 {len(diff)} 行)\n"]
            detailed_diffs.append({'file': file_path, 'diff': ''.join(diff)})
    
    return bool(changes['added'] or changes['modified'] or changes['deleted']), changes, detailed_diffs

def append_to_changes_file(changes, detailed_diffs, drive_path, timestamp):
    changes_file = drive_path / "AI_Context_Changes.md"
    
    existing_records = []
    if changes_file.exists():
        with open(changes_file, 'r', encoding='utf-8') as f:
            content = f.read()
            content = content.replace('# 🔄 AI Context 变更历史\n\n', '')
            content = content.replace('<RECENT_CHANGES>\n', '')
            content = content.replace('</RECENT_CHANGES>\n', '')
            existing_records = [r.strip() for r in content.split('\n---\n') if r.strip() and r.startswith('##')]
    
    new_record = f"## 📅 {timestamp}\n"
    new_record += f"- ➕ 新增: {len(changes['added'])} | 📝 修改: {len(changes['modified'])} | ❌ 删除: {len(changes['deleted'])}\n\n"
    
    if detailed_diffs:
        for d in detailed_diffs[:10]:
            new_record += f"#### {d['file']}\n```diff\n{d['diff']}```\n"
    
    records_queue = deque(existing_records, maxlen=10)  # 保留最近10次即可
    records_queue.appendleft(new_record)
    
    with open(changes_file, 'w', encoding='utf-8') as f:
        f.write("# 🔄 AI Context 变更历史\n\n<RECENT_CHANGES>\n")
        f.write('\n---\n'.join(list(records_queue)))
        f.write("\n</RECENT_CHANGES>\n")

if __name__ == '__main__':
    try:
        build_dual_sync()
    except Exception as e:
        print(f"❌ 运行错误: {e}")
        import traceback
        traceback.print_exc()
        input("\n按 Enter 键退出...")
