import difflib
import hashlib
import json
import os
import re
import shutil
import sys
from collections import deque
from datetime import datetime
from pathlib import Path

# ==========================================
# ⚙️ AGENT 的配置区
# ==========================================
SOURCE_PROJECT_DIR = r"C:\Godot\TetrisBackpack"
AGENT_WORKSPACE_DIR = r"C:\Godot\AISpace"
DRIVE_SYNC_PATH = r"C:\Users\26070\My Drive\Agent_Godot_Brain"
LOCAL_BACKUP_PATH = r"D:\Agent_Godot_Brain_Backup"
LOCAL_HUMAN_VIEW_PATH = r"D:\A1GeminiSyncTestForHuman"  # 本地人类视图（5个分类文件）
LOCAL_WORKSPACE_MASTER_COPY_DIR = r"C:\Godot\AISpace\SyncMasterCopy"
LOCAL_WORKSPACE_MASTER_COPY_NAME = "AI_Context_Master_Latest.txt"

# rules_global migration: rules live in rules_global/ (replaces .agent/steering/).
# AGENT_WHITELIST_DIRS are whitelisted subdirs under AGENT_WORKSPACE_DIR to deep-scan for .md/.json/.txt.
AGENT_WHITELIST_DIRS = ["rules_global", "rules_ide"]
AGENT_WHITELIST_FILES = ["AGENTS.md", "docLastConversationState.md"]
PROJECT_WHITELIST_PREFIXES = ["A1", "B1"]
PROJECT_WHITELIST_DIRS = ["Scenes"]

CODE_MAX_SIZE_MB = 1.0  # 纯代码文件最大 1MB
RESOURCE_MAX_SIZE_MB = 0.2  # 场景/资源文件最大 200KB

IGNORE_EXTENSIONS = (
    ".png",
    ".jpg",
    ".jpeg",
    ".svg",
    ".webp",
    ".ico",
    ".ogg",
    ".wav",
    ".mp3",
    ".aac",
    ".flac",
    ".glb",
    ".gltf",
    ".fbx",
    ".obj",
    ".blend",
    ".dll",
    ".so",
    ".a",
    ".pdb",
    ".dylib",
    ".res",
    ".spv",
    ".uid",
    ".import",
    ".exe",
    ".bin",
    ".dat",
    ".cache",
)

SILENT_IGNORE_EXTENSIONS = (
    ".import",
    ".uid",
    ".png",
    ".wav",
    ".svg",
    ".so",
    ".dll",
    ".fbx",
    ".ttf",
    ".TMP",
    ".unitypackage",
    ".plist",
)

EXCLUDE_EXTENSIONS = (
    ".sln",
    ".editorconfig",
    ".user",
    ".DotSettings.user",
    ".bak",
    ".tmp",
)

FILENAME_BLACKLIST = {
    "LICENSE.txt",
    "LICENSE",
    "COPYING.txt",
    "COPYING",
    "test_paths.txt",
    "debug.txt",
    "temp.txt",
    "log.txt",
}

CRITICAL_FILES = {
    "project.godot",
    "default_bus_layout.tres",
    ".gitignore",
    ".gitattributes",
}

IGNORE_DIRS = (
    ".godot",
    ".git",
    ".vs",
    ".idea",
    ".vscode",
    "bin",
    "obj",
    "Export",
    "Builds",
    "Library",
    "Temp",
    "temp",
    "node_modules",
    "__pycache__",
    ".backup_old_components",
    "NVIDIA Corporation",
    "AnimationFBX",
    "Animations",
    ".windsurf",
)

# ==========================================
# 🛠️ 核心辅助函数
# ==========================================

# 核心规则文件列表（最高优先级）
IMPORTANT_RULES_FILES = {
    "AGENTS.md",  # 单一真相源（替代 MainRules.md + ProjectRules.md）
    "DesignPatterns.md",
    "ConversationReset.md",
    "docLastConversationState.md",
}

PRIMACY_RECENT_CHANGES_LIMIT = 5

# TetrisBackpack 根目录中的硬链接文件，已通过 AISpace/rules_global/ 同步，跳过避免重复
PROJECT_ROOT_MD_SKIP = {"AGENTS.md", "CLAUDE.md"}


def normalize_virtual_path(path_str):
    return str(path_str).replace("\\", "/")


def extract_virtual_path_from_xml(xml_content):
    match = re.search(r'path="([^"]+)"', xml_content)
    if not match:
        return ""
    return normalize_virtual_path(match.group(1))


def sort_bucket_contents(bucket_key, content_list):
    if bucket_key == "01_important_rules":
        return sorted(content_list, key=important_rules_sort_key)
    return sorted(content_list, key=extract_virtual_path_from_xml)


def important_rules_sort_key(xml_content):
    path = extract_virtual_path_from_xml(xml_content)
    explicit_priority = {
        "AISpace/AGENTS.md": 0,
        "AISpace/rules_global/Always/AGENTS.md": 1,
        "AISpace/rules_ide/Codex/AGENTS.md": 2,
        "AISpace/rules_global/ConversationReset.md": 3,
        "AISpace/docLastConversationState.md": 4,
    }

    if path in explicit_priority:
        return (explicit_priority[path], path)

    if path.endswith("/AGENTS.md"):
        return (10, path)
    if path.endswith("/ConversationReset.md"):
        return (20, path)
    if path.endswith("/DesignPatterns.md"):
        return (30, path)
    if path.endswith("/docLastConversationState.md"):
        return (40, path)
    return (99, path)


def extract_recent_change_entries(changes_content, limit=PRIMACY_RECENT_CHANGES_LIMIT):
    if not changes_content.strip():
        return []

    normalized_content = changes_content.replace(
        "# 🔄 CRITICAL AI_Context_Changes.md — AI Context 变更历史\n\n", ""
    )
    normalized_content = normalized_content.replace(
        "# 🔄 AI Context 变更历史\n\n", ""
    )
    normalized_content = normalized_content.replace("<RECENT_CHANGES>\n", "")
    normalized_content = normalized_content.replace("</RECENT_CHANGES>\n", "")

    entries = [
        entry.strip()
        for entry in re.split(r"\n---\n", normalized_content)
        if entry.strip().startswith("##")
    ]
    return entries[:limit]


def build_primacy_changes_content(changes_content):
    recent_change_entries = extract_recent_change_entries(changes_content)
    if not recent_change_entries:
        return ""

    return (
        "# 🔄 CRITICAL AI_Context_Changes.md — AI Context 变更历史\n\n"
        "<RECENT_CHANGES>\n"
        + "\n---\n".join(recent_change_entries)
        + "\n</RECENT_CHANGES>\n"
    )


def write_primacy_recent_changes_section(f, primacy_changes_content):
    if not primacy_changes_content:
        return

    recent_change_count = len(extract_recent_change_entries(primacy_changes_content))

    f.write(
        "  <section name='00_primacy_boost' description='Read This First'>\n"
    )
    f.write(
        "    <instruction>Read this section first. Treat these recent changes and the next rules section as highest-priority context.</instruction>\n"
    )
    f.write(f"    <urgent_recent_changes count='{recent_change_count}'>\n")
    f.write("      <![CDATA[\n")
    f.write(primacy_changes_content)
    if not primacy_changes_content.endswith("\n"):
        f.write("\n")
    f.write("      ]]>\n")
    f.write("    </urgent_recent_changes>\n")
    f.write("  </section>\n\n")


def load_changes_content(drive_path, human_path):
    candidate_files = [
        drive_path / "AI_Context_Changes.md",
        human_path / "AI_Context_Changes.md",
    ]

    for changes_file in candidate_files:
        if changes_file.exists():
            with open(changes_file, "r", encoding="utf-8") as f:
                content = f.read()
            return content.replace(
                "# 🔄 AI Context 变更历史\n\n",
                "# 🔄 CRITICAL AI_Context_Changes.md — AI Context 变更历史\n\n",
            )

    return ""


def archive_existing_master_files(drive_path, backup_folder):
    for old_file in drive_path.glob("AI_Context_Master_*.txt"):
        target_path = backup_folder / old_file.name
        try:
            if target_path.exists():
                target_path.unlink()
            shutil.move(str(old_file), str(target_path))
        except Exception as e:
            print(
                f"⚠️ [Agent Sync] 归档旧 Master 失败，跳过该文件: {old_file.name} | {e}"
            )


def cleanup_workspace_master_copy_files(workspace_copy_dir):
    for old_file in workspace_copy_dir.glob("AI_Context_Master*.txt"):
        try:
            old_file.unlink()
        except Exception as e:
            print(
                f"⚠️ [Agent Sync] 清理工作区 Master 副本失败，跳过该文件: {old_file.name} | {e}"
            )


def cleanup_local_human_view_files(human_path):
    for old_file in human_path.glob("*.txt"):
        try:
            old_file.unlink()
        except Exception as e:
            print(
                f"⚠️ [Agent Sync] 清理本地视图失败，跳过该文件: {old_file.name} | {e}"
            )


def write_human_view_file(local_file, content_list, description, timestamp):
    target_file = local_file

    try:
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(f"# HUMAN VIEW - CATEGORY: {local_file.stem}\n")
            f.write(f"# {description}\n")
            f.write(f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# 文件数量: {len(content_list)}\n\n")
            f.write("=" * 80 + "\n\n")

            for xml_content in content_list:
                f.write(xml_content)
    except Exception:
        target_file = local_file.with_name(f"{local_file.stem}_{timestamp}.txt")
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(f"# HUMAN VIEW - CATEGORY: {local_file.stem}\n")
            f.write(f"# {description}\n")
            f.write(f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# 文件数量: {len(content_list)}\n\n")
            f.write("=" * 80 + "\n\n")

            for xml_content in content_list:
                f.write(xml_content)

    return target_file


def sync_workspace_master_copy(master_file, workspace_copy_dir):
    cleanup_workspace_master_copy_files(workspace_copy_dir)
    target_file = workspace_copy_dir / LOCAL_WORKSPACE_MASTER_COPY_NAME
    shutil.copy2(master_file, target_file)
    return target_file


def classify_file_to_bucket(file_path, source_path, agent_path):
    """
    将文件分类到5个桶之一

    优先级规则（从高到低）：
    1. 核心规则文件 → 01_important_rules
    2. 路径包含 A1 → 03_a1_components
    3. 路径包含 B1 → 04_b1_components
    4. AISpace/ 目录下 → 02_other_rules
    5. 其他 → 05_project_core

    返回: bucket_key (str)
    """
    file_name = file_path.name

    # 优先级1：核心规则文件
    if file_name in IMPORTANT_RULES_FILES:
        return "01_important_rules"

    # 获取相对路径字符串（兼容 Python 3.7+）
    try:
        if agent_path:
            try:
                rel_path_str = str(file_path.relative_to(agent_path)).replace("\\", "/")
                is_in_agent = True
            except ValueError:
                is_in_agent = False
        else:
            is_in_agent = False

        if not is_in_agent:
            try:
                rel_path_str = str(file_path.relative_to(source_path)).replace(
                    "\\", "/"
                )
            except ValueError:
                rel_path_str = str(file_path)
    except:
        rel_path_str = str(file_path)

    # 优先级2：A1 组件
    if "A1" in rel_path_str or "/A1" in rel_path_str or "\\A1" in str(file_path):
        return "03_a1_components"

    # 优先级3：B1 组件
    if "B1" in rel_path_str or "/B1" in rel_path_str or "\\B1" in str(file_path):
        return "04_b1_components"

    # 优先级4：其他规则文件（检查是否在 agent_path 下）
    if agent_path and is_in_agent:
        return "02_other_rules"

    # 优先级5：项目核心
    return "05_project_core"


def is_ignored(file_name, root_path):
    """
    Check if a file/directory should be ignored based on directory blacklist.
    Note: Extension-based filtering is handled separately in the binary indexing logic.
    """
    path_parts = root_path.replace("\\", "/").split("/")
    return any(ignored_dir in path_parts for ignored_dir in IGNORE_DIRS)


def is_binary_file(filepath):
    """
    终极防御：通过读取文件头部检测空字节，判断是否为真正的二进制文件。
    比扩展名检测可靠 100 倍。

    原理：文本文件极少包含真正的空字节 \x00
    """
    try:
        with open(filepath, "rb") as f:
            chunk = f.read(1024)
            # 检测空字节
            if b"\x00" in chunk:
                return True
    except Exception:
        pass
    return False


def calculate_file_hash(file_path):
    md5_hash = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
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

    if file_suffix in [".tscn", ".tres", ".json"]:
        if file_size_mb > RESOURCE_MAX_SIZE_MB:
            return False, f"Resource too large ({file_size_mb:.2f}MB)"
    elif file_suffix in [".cs", ".gd"]:
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

        if top_folder == "addons" and len(path_parts) > 1:
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
    print("🌊 [Agent Sync] 启动双路同步：AI 巨无霸 (云端) + 人类分类视图 (本地)...")

    source_path = Path(SOURCE_PROJECT_DIR)
    agent_path = Path(AGENT_WORKSPACE_DIR)
    drive_path = Path(DRIVE_SYNC_PATH)
    human_path = Path(LOCAL_HUMAN_VIEW_PATH)
    workspace_copy_path = Path(LOCAL_WORKSPACE_MASTER_COPY_DIR)

    if not source_path.exists():
        print(f"❌ 找不到源目录: {SOURCE_PROJECT_DIR}")
        return

    # 创建目标文件夹
    drive_path.mkdir(parents=True, exist_ok=True)
    human_path.mkdir(parents=True, exist_ok=True)
    workspace_copy_path.mkdir(parents=True, exist_ok=True)

    # 备份旧文件
    backup_folder = Path(LOCAL_BACKUP_PATH)
    backup_folder.mkdir(exist_ok=True)

    # 清理云端旧的 Master 文件
    archive_existing_master_files(drive_path, backup_folder)

    # 清理本地旧的分类文件
    cleanup_local_human_view_files(human_path)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 初始化5个分类存储桶
    buckets = {
        "01_important_rules": [],
        "02_other_rules": [],
        "03_a1_components": [],
        "04_b1_components": [],
        "05_project_core": [],
    }

    # Manifest 用于变更检测
    current_manifest = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "files": {},
    }

    print(f"🔍 [Agent Sync] 开始单次扫描并分类...")

    # ========== 扫描 AISpace/ (包含 rules_global/) ==========
    if agent_path.exists():
        # 处理根目录白名单文件
        for filename in AGENT_WHITELIST_FILES:
            file_path = agent_path / filename
            if file_path.exists():
                # 🛡️ 二进制雷达
                if is_binary_file(file_path):
                    file_size_kb = file_path.stat().st_size / 1024
                    stub_content = f'<binary_asset type="{file_path.suffix}" size_kb="{file_size_kb:.2f}" />\n'
                    process_file_to_bucket(
                        file_path,
                        f"AISpace/{filename}",
                        buckets,
                        current_manifest,
                        source_path,
                        agent_path,
                        override_content=stub_content,
                    )
                    continue
                process_file_to_bucket(
                    file_path,
                    f"AISpace/{filename}",
                    buckets,
                    current_manifest,
                    source_path,
                    agent_path,
                )

        # 处理白名单子目录
        for whitelist_dir in AGENT_WHITELIST_DIRS:
            dir_path = agent_path / whitelist_dir
            if dir_path.exists():
                for root, _, files in os.walk(dir_path):
                    for file in files:
                        if (
                            file.endswith((".md", ".json", ".txt"))
                            and file not in FILENAME_BLACKLIST
                        ):
                            f_path = Path(root) / file
                            rel_path = f_path.relative_to(agent_path)

                            # 🛡️ 二进制雷达
                            if is_binary_file(f_path):
                                file_size_kb = f_path.stat().st_size / 1024
                                stub_content = f'<binary_asset type="{f_path.suffix}" size_kb="{file_size_kb:.2f}" />\n'
                                process_file_to_bucket(
                                    f_path,
                                    f"AISpace/{rel_path}",
                                    buckets,
                                    current_manifest,
                                    source_path,
                                    agent_path,
                                    override_content=stub_content,
                                )
                                continue

                            process_file_to_bucket(
                                f_path,
                                f"AISpace/{rel_path}",
                                buckets,
                                current_manifest,
                                source_path,
                                agent_path,
                            )

    # ========== 扫描 TetrisBackpack/ 项目 ==========
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

            # 跳过 TetrisBackpack 根目录的 AI-rules 硬链接（已通过 AISpace/rules_global/ 同步，避免重复）
            if len(rel_path.parts) == 1 and file in PROJECT_ROOT_MD_SKIP:
                continue

            # 彻底屏蔽无用扩展名（不生成占位符）
            if file.endswith(SILENT_IGNORE_EXTENSIONS):
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
                    process_file_to_bucket(
                        file_path,
                        f"TetrisBackpack/{rel_path}",
                        buckets,
                        current_manifest,
                        source_path,
                        agent_path,
                        override_content=stub_content,
                    )
                except Exception:
                    pass
                continue

            # 🔪 第三方 Addons 绞肉机：只保留 A1/B1 自定义插件源码
            path_parts = rel_path.parts
            if len(path_parts) > 1 and path_parts[0] == "addons":
                addon_name = path_parts[1]
                is_custom_addon = any(
                    addon_name.startswith(p) for p in PROJECT_WHITELIST_PREFIXES
                )

                if not is_custom_addon:
                    # 第三方插件：只留墓碑，不读源码
                    stub_content = f'<third_party_addon name="{addon_name}" />\n'
                    try:
                        process_file_to_bucket(
                            file_path,
                            f"TetrisBackpack/{rel_path}",
                            buckets,
                            current_manifest,
                            source_path,
                            agent_path,
                            override_content=stub_content,
                        )
                    except Exception:
                        pass
                    continue

            is_critical = file in CRITICAL_FILES
            is_whitelisted = is_in_whitelist_folder(file_path, source_path)

            # 白名单文件也必须是代码/文本后缀
            valid_extensions = (
                ".cs",
                ".gd",
                ".tscn",
                ".tres",
                ".md",
                ".json",
                ".cfg",
                ".xml",
                ".csproj",
                ".godot",
                ".gdshader",
                ".shader",
            )

            if is_critical or file.endswith(valid_extensions):
                if not is_critical and not is_whitelisted:
                    should_include, _ = should_include_file(file_path)
                    if not should_include:
                        continue

                process_file_to_bucket(
                    file_path,
                    f"TetrisBackpack/{rel_path}",
                    buckets,
                    current_manifest,
                    source_path,
                    agent_path,
                )

    # 统计
    total_files = sum(len(bucket) for bucket in buckets.values())
    print(f"\n📊 [Agent Sync] 扫描完成，共分类 {total_files} 个文件")
    for key, bucket in buckets.items():
        print(f"   {key}: {len(bucket)} 个文件")

    # 读取变更记录
    recent_changes_content = load_changes_content(drive_path, human_path)
    primacy_changes_content = build_primacy_changes_content(recent_changes_content)

    for bucket_key in buckets:
        buckets[bucket_key] = sort_bucket_contents(bucket_key, buckets[bucket_key])

    # ========== 输出 A：云端 AI 巨无霸 (单一 XML 文件) ==========
    print(f"\n📝 [Agent Sync] 生成云端 AI 巨无霸...")
    master_file = drive_path / f"AI_Context_Master_{timestamp}.txt"

    with open(master_file, "w", encoding="utf-8") as f:
        f.write("<system_context>\n")
        f.write("  <metadata>\n")
        f.write(
            "    <description>Godot CsArchitect (构筑师) Project Context Master File (Dual-Sync)</description>\n"
        )
        f.write(
            f"    <generated_time>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</generated_time>\n"
        )
        f.write("  </metadata>\n\n")
        write_primacy_recent_changes_section(f, primacy_changes_content)

        # 按顺序拼接所有桶的内容
        bucket_names = {
            "01_important_rules": "Important Rules",
            "02_other_rules": "Other Rules",
            "03_a1_components": "A1 Components",
            "04_b1_components": "B1 Components",
            "05_project_core": "Project Core",
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
    workspace_master_copy_file = sync_workspace_master_copy(
        master_file, workspace_copy_path
    )
    print(f"   ✅ 工作区副本: {workspace_master_copy_file.name}")

    # ========== 输出 B：本地人类分类视图 (5个独立文件) ==========
    print(f"\n📝 [Agent Sync] 生成本地人类分类视图...")

    bucket_descriptions = {
        "01_important_rules": "核心规则文件 (MainRules, DesignPatterns, ProjectRules 等)",
        "02_other_rules": "其他规则和文档 (steering, docs, specs)",
        "03_a1_components": "A1 前缀组件 (用户自定义)",
        "04_b1_components": "B1 前缀组件 (用户自定义)",
        "05_project_core": "项目核心文件 (Scenes, Tests, 其他源码)",
    }

    for key, content_list in buckets.items():
        if not content_list:
            continue

        local_file = write_human_view_file(
            human_path / f"{key}.txt",
            content_list,
            bucket_descriptions[key],
            timestamp,
        )

        local_size_mb = local_file.stat().st_size / (1024 * 1024)
        print(f"   ✅ {key}.txt ({local_size_mb:.2f} MB, {len(content_list)} 文件)")

    # ========== 处理 Manifest 与变更检测 ==========
    process_manifest_and_changes(current_manifest, backup_folder, human_path, timestamp)

    print(f"\n✨ [Agent Sync] 双路同步完成！")
    print(f"   🌐 云端 (AI): {master_file}")
    print(f"   🤖 工作区副本 (AI): {workspace_master_copy_file}")
    print(f"   🏠 本地 (人): {human_path}")


def process_file_to_bucket(
    file_path,
    virtual_path,
    buckets,
    manifest_dict,
    source_path,
    agent_path,
    override_content=None,
):
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
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            if not content.strip():
                return  # 跳过空文件

            # 确定优先级
            file_name = file_path.name
            if file_name in IMPORTANT_RULES_FILES or file_name in CRITICAL_FILES:
                priority = "CRITICAL"
            elif file_name in AGENT_WHITELIST_FILES:
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
            if not content.endswith("\n"):
                xml_content += "\n"
            xml_content += "]]>\n"

        xml_content += "    </file>\n\n"

        # 分类到对应的桶
        bucket_key = classify_file_to_bucket(file_path, source_path, agent_path)
        buckets[bucket_key].append(xml_content)

        # 记录到 Manifest（只记录真实文件，不记录占位符）
        if override_content is None:
            f_hash = calculate_file_hash(file_path)
            if f_hash:
                manifest_dict["files"][str(virtual_path)] = {
                    "hash": f_hash,
                    "size": file_path.stat().st_size,
                    "content": content,
                }

    except Exception as e:
        # 错误文件也要记录
        xml_content = f'    <file path="{virtual_path}" error="{str(e)}" />\n'
        bucket_key = classify_file_to_bucket(file_path, source_path, agent_path)
        buckets[bucket_key].append(xml_content)


def process_manifest_and_changes(
    current_manifest, backup_folder, human_path, timestamp
):
    manifest_file = backup_folder / "AI_Context_Manifest.json"
    previous_manifest_file = backup_folder / "AI_Context_Manifest_Previous.json"

    # 保存当前 Manifest
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(current_manifest, f, indent=2, ensure_ascii=False)

    previous_manifest = {}
    if previous_manifest_file.exists():
        with open(previous_manifest_file, "r", encoding="utf-8") as f:
            previous_manifest = json.load(f)

    if previous_manifest:
        has_changes, changes, detailed_diffs = generate_change_report(
            current_manifest, previous_manifest
        )
        if has_changes:
            append_to_changes_file(changes, detailed_diffs, human_path, timestamp)

    shutil.copy(manifest_file, previous_manifest_file)


def generate_change_report(current_manifest, previous_manifest):
    changes = {"added": [], "modified": [], "deleted": []}
    detailed_diffs = []

    curr_files = set(current_manifest.get("files", {}).keys())
    prev_files = set(previous_manifest.get("files", {}).keys())

    changes["added"] = list(curr_files - prev_files)
    changes["deleted"] = list(prev_files - curr_files)

    for file_path in curr_files & prev_files:
        if (
            current_manifest["files"][file_path]["hash"]
            != previous_manifest["files"][file_path]["hash"]
        ):
            changes["modified"].append(file_path)

    for file_path in changes["modified"][:20]:
        curr_content = current_manifest["files"][file_path].get("content", "")
        prev_content = previous_manifest["files"][file_path].get("content", "")

        diff = list(
            difflib.unified_diff(
                prev_content.splitlines(keepends=True),
                curr_content.splitlines(keepends=True),
                n=5,
            )
        )

        if diff:
            if len(diff) > 200:
                diff = diff[:200] + [f"\n... (diff截断, 共 {len(diff)} 行)\n"]
            detailed_diffs.append({"file": file_path, "diff": "".join(diff)})

    return (
        bool(changes["added"] or changes["modified"] or changes["deleted"]),
        changes,
        detailed_diffs,
    )


def append_to_changes_file(changes, detailed_diffs, human_path, timestamp):
    changes_file = human_path / "AI_Context_Changes.md"

    existing_records = []
    if changes_file.exists():
        with open(changes_file, "r", encoding="utf-8") as f:
            content = f.read()
            content = content.replace("# 🔄 CRITICAL AI_Context_Changes.md — AI Context 变更历史\n\n", "")
            content = content.replace("# 🔄 AI Context 变更历史\n\n", "")
            content = content.replace("<RECENT_CHANGES>\n", "")
            content = content.replace("</RECENT_CHANGES>\n", "")
            existing_records = [
                r.strip()
                for r in content.split("\n---\n")
                if r.strip() and r.startswith("##")
            ]

    new_record = f"## 📅 {timestamp}\n"
    new_record += f"- ➕ 新增: {len(changes['added'])} | 📝 修改: {len(changes['modified'])} | ❌ 删除: {len(changes['deleted'])}\n\n"

    if detailed_diffs:
        for d in detailed_diffs[:10]:
            new_record += f"#### {d['file']}\n```diff\n{d['diff']}```\n"

    records_queue = deque(existing_records, maxlen=10)  # 保留最近10次即可
    records_queue.appendleft(new_record)

    with open(changes_file, "w", encoding="utf-8") as f:
        f.write("# 🔄 CRITICAL AI_Context_Changes.md — AI Context 变更历史\n\n<RECENT_CHANGES>\n")
        f.write("\n---\n".join(list(records_queue)))
        f.write("\n</RECENT_CHANGES>\n")


if __name__ == "__main__":
    try:
        build_dual_sync()
    except Exception as e:
        print(f"❌ 运行错误: {e}")
        import traceback

        traceback.print_exc()
        if sys.stdin.isatty():
            input("\n按 Enter 键退出...")
