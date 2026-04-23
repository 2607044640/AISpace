#  Kiro Cloud Sync System - AI 快速上手指南

##  系统概览

**目的**: 将项目上下文同步到 Google Drive，供 Gemini AI 阅读，同时生成人类可读的分类视图。

**核心脚本**: `KiroWorkingSpace/.kiro/CloudSync_Workflow/kiro_sync_to_drive.py`

**输出位置**:
-  **云端 (AI)**: `C:\Users\26070\My Drive\Kiro_Godot_Brain\AI_Context_Master_YYYYMMDD_HHMMSS.txt` (单一 XML 文件)
-  **本地 (人类)**: `D:\A1GeminiSyncTestForHuman\` (5 个分类文件)
-  **备份**: `D:\Kiro_Godot_Brain_Backup\` (Manifest 和旧文件)

---

##  核心功能

### 1 双路输出架构 (Dual-Output)

**Output A - 云端 AI 巨无霸**:
- 单一 XML 文件，按优先级排序
- 包含 6 个 section：
  1. `01_important_rules` - 核心规则 (MainRules, DesignPatterns, ProjectRules)
  2. `02_other_rules` - 其他文档 (steering, docs, specs)
  3. `03_a1_components` - A1 前缀组件
  4. `04_b1_components` - B1 前缀组件
  5. `05_project_core` - 项目核心文件
  6. `06_recent_changes` - 最近变更记录

**Output B - 本地人类分类视图**:
- 5 个独立 TXT 文件 (对应前 5 个 section)
- 方便人类快速查看和调试

### 2 二进制雷达 (Binary Asset Indexing)

**问题**: 二进制文件 (图片、字体、DLL) 如果直接读取会产生乱码，污染 AI 上下文。

**解决方案**: 
- 使用 `is_binary_file()` 检测空字节 (`\x00`)
- 生成元数据占位符：`<binary_asset type=".png" size_kb="123.45" />`
- AI 可以看到资源存在，但不会被乱码污染

**效果**: 1,213 个二进制资源被索引，文件大小从 5.64 MB 降至 2.56 MB

### 3 第三方 Addons 绞肉机 (Third-Party Addon Filter)

**问题**: 第三方插件源码 (PhantomCamera, R3.Godot, Jolt Physics) 对 AI 无阅读价值，浪费上下文。

**解决方案**:
- 检测 `addons/` 目录下的文件
- 只保留 A1/B1 前缀的自定义插件源码
- 第三方插件生成墓碑：`<third_party_addon name="phantom_camera" />`

**效果**: 356 个第三方文件被过滤，文件大小从 2.78 MB 降至 1.50 MB (减少 46%)

### 4 Git-Style 变更追踪 (Change Tracking)

**功能**:
- 使用 MD5 哈希检测文件变更
- 生成 unified diff 格式 (带 +/- 标记)
- 保留最近 10 次变更记录
- 最近 5 次标记为 `<RECENT_CHANGES>`

**输出**: `C:\Users\26070\My Drive\Kiro_Godot_Brain\AI_Context_Changes.md`

### 5 自动同步 Hooks

**触发时机**:
- `agentStop`: AI 执行完成后
- `fileEdited`: 保存 `.md`, `.cs`, `.gd`, `.tscn` 等文件时

**执行**: 后台运行 `SYNC_TO_GEMINI_SILENT.bat`

---

##  关键函数说明

### `build_dual_sync()`
主函数，协调整个同步流程：
1. 扫描 KiroWorkingSpace/.kiro/ 和 3d-practice/
2. 分类文件到 5 个桶
3. 生成云端 XML 和本地分类文件
4. 处理 Manifest 和变更检测

### `process_file_to_bucket(file_path, virtual_path, buckets, manifest_dict, source_path, kiro_path, override_content=None)`
处理单个文件：
- `override_content=None`: 正常读取文本文件
- `override_content="<stub>"`: 使用占位符（二进制/第三方插件）

### `is_binary_file(filepath)`
二进制检测：
- 读取前 1024 字节
- 检测空字节 `\x00`
- 返回 True/False

### `classify_file_to_bucket(file_path, source_path, kiro_path)`
文件分类逻辑（优先级从高到低）：
1. 核心规则文件  `01_important_rules`
2. 路径包含 A1  `03_a1_components`
3. 路径包含 B1  `04_b1_components`
4. .kiro/ 目录  `02_other_rules`
5. 其他  `05_project_core`

---

##  关键配置

### 白名单机制

**项目白名单前缀**:
```python
PROJECT_WHITELIST_PREFIXES = ['A1', 'B1']
```
- A1/B1 开头的文件夹会绕过大小限制
- 第三方插件过滤时，A1/B1 插件保留源码

**Kiro 白名单**:
```python
KIRO_WHITELIST_DIRS = ['steering', 'docs', 'specs']
KIRO_WHITELIST_FILES = ['ProjectRules.md', 'docLastConversationState.md', 'ConversationReset.md']
```

### 忽略规则

**扩展名黑名单**:
```python
IGNORE_EXTENSIONS = (
    '.png', '.jpg', '.svg',  # 图片
    '.ogg', '.wav', '.mp3',  # 音频
    '.glb', '.fbx', '.obj',  # 模型
    '.dll', '.so', '.pdb',   # 库文件
    '.res', '.uid', '.import' # Godot 元数据
)
```

**目录黑名单**:
```python
IGNORE_DIRS = (
    '.godot', '.git', '.vs', 'bin', 'obj',
    'AnimationFBX', 'Animations'
)
```

---

##  常见操作

### 手动运行同步
```bash
cd KiroWorkingSpace/.kiro/CloudSync_Workflow
python kiro_sync_to_drive.py
```

### 查看最近变更
```powershell
Get-Content "C:\Users\26070\My Drive\Kiro_Godot_Brain\AI_Context_Changes.md" -Head 50
```

### 验证二进制索引
```bash
cd KiroWorkingSpace/.kiro/CloudSync_Workflow
python verify_binary_indexing.py
```

### 验证第三方插件过滤
```bash
cd KiroWorkingSpace/.kiro/CloudSync_Workflow
python final_verify.py
```

---

##  故障排查

### 问题 1: 二进制文件未被索引
**症状**: 文件数量少于预期，或文件大小异常大（包含乱码）

**原因**: `is_ignored()` 函数在二进制检测前就过滤了文件

**解决**: 确保 `is_ignored()` 只检查目录黑名单，不检查扩展名：
```python
def is_ignored(file_name, root_path):
    #  错误：if file_name.endswith(IGNORE_EXTENSIONS): return True
    #  正确：只检查目录
    path_parts = root_path.replace('\\', '/').split('/')
    return any(ignored_dir in path_parts for ignored_dir in IGNORE_DIRS)
```

### 问题 2: 第三方插件源码泄漏
**症状**: 文件大小过大，包含 PhantomCamera/R3.Godot 源码

**检查**: 确保 Addons 绞肉机逻辑在二进制雷达之后：
```python
# 1. 二进制雷达
if is_binary_file(file_path) or file.endswith(IGNORE_EXTENSIONS):
    # ... 生成 binary_asset 占位符
    continue

# 2. 第三方 Addons 绞肉机
if len(path_parts) > 1 and path_parts[0] == 'addons':
    addon_name = path_parts[1]
    if not any(addon_name.startswith(p) for p in PROJECT_WHITELIST_PREFIXES):
        # ... 生成 third_party_addon 占位符
        continue
```

### 问题 3: 变更检测不工作
**症状**: `AI_Context_Changes.md` 为空或不更新

**检查**:
1. Manifest 文件是否存在：`D:\Kiro_Godot_Brain_Backup\AI_Context_Manifest.json`
2. 文件哈希是否正确计算
3. `process_manifest_and_changes()` 是否被调用

---

##  性能指标

| 指标 | 数值 |
|------|------|
| 总文件数 | 1,793 |
| 文本文件 | 580 |
| 二进制资源索引 | 1,213 |
| 第三方插件墓碑 | 356 |
| 云端文件大小 | 1.50 MB |
| 瘦身效果 | -46% (从 2.78 MB) |

---

##  设计原则

1. **单次扫描，多路输出**: 只遍历文件系统一次，同时生成云端和本地输出
2. **内存桶分类**: 使用 5 个 List 作为"桶"，在内存中完成分类
3. **占位符优先**: 遇到二进制/第三方文件，立即生成占位符并 `continue`
4. **XML 原生格式**: AI 对 XML 的理解优于纯文本分隔符
5. **三明治结构**: 重要内容放顶部和底部（LLM 位置权重高）

---

##  相关文件

- **主脚本**: `KiroWorkingSpace/.kiro/CloudSync_Workflow/kiro_sync_to_drive.py`
- **静默执行**: `KiroWorkingSpace/.kiro/CloudSync_Workflow/SYNC_TO_GEMINI_SILENT.bat`
- **Hooks**: `KiroWorkingSpace/.kiro/hooks/auto-sync-*.json`
- **验证脚本**: `KiroWorkingSpace/.kiro/CloudSync_Workflow/verify_*.py`

---

##  快速命令参考

```powershell
# 手动同步
cd C:\Godot\KiroWorkingSpace\.kiro\CloudSync_Workflow
python kiro_sync_to_drive.py

# 查看最近变更（前 20 行）
Get-Content "C:\Users\26070\My Drive\Kiro_Godot_Brain\AI_Context_Changes.md" -Head 20

# 验证二进制索引
python verify_binary_indexing.py

# 验证第三方插件过滤
python final_verify.py

# 测试二进制检测
python test_binary_detection.py

# 测试插件检测逻辑
python test_addon_detection.py
```

---

**最后更新**: 2026-04-23  
**维护者**: Kiro AI Assistant  
**架构师**: 用户
