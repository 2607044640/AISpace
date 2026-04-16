# 🎯 快速开始指南

## 一键同步（推荐）

在 `3d-practice` 项目根目录，双击运行 `SYNC_TO_GEMINI.bat`，脚本会自动完成所有工作。

## 首次配置（必须）

1. 安装 [Google Drive 桌面客户端](https://www.google.com/drive/download/)
2. 在 Google Drive 网页端创建文件夹 `Kiro_Godot_Brain`
3. 确认 Google Drive 已映射到 `G:\My Drive\`（如果路径不同，需要修改配置）
4. 编辑 `kiro_sync_to_drive.py`，确认第 11-17 行配置正确：
   ```python
   SOURCE_PROJECT_DIR = r"C:\Godot\3d-practice"  # 你的项目路径
   DRIVE_SYNC_PATH = r"G:\My Drive\Kiro_Godot_Brain"  # 你的 Drive 路径
   CLEAN_BEFORE_SYNC = True  # 是否清空旧文件
   ```
5. **关键步骤：** 在 Gemini 中编辑你的自定义 Gem，在 Knowledge 区域选择**整个 `Kiro_Godot_Brain` 文件夹**（不是单个文件！）

## 工作流程

```
修改代码 → 双击 SYNC_TO_GEMINI.bat → 等待 Drive 同步 → 在 Gemini 开新对话
```

## 同步模式说明

脚本使用**文件夹镜像模式**，而不是 ZIP 压缩：
- ✅ Gemini 可以直接索引和读取每个代码文件
- ✅ 保持原有目录结构，便于 AI 理解项目架构
- ✅ 支持增量更新，Drive 只同步变化的文件
- ❌ 不使用 ZIP（Gemini 无法读取 ZIP 内容）

## 故障排查

**问题：找不到源项目目录**
- 确认 `C:\Godot\3d-practice` 路径是否正确
- 如果项目在其他位置，修改 `kiro_sync_to_drive.py` 中的 `SOURCE_PROJECT_DIR`

**问题：找不到 Google Drive 路径**
- 检查 Drive 客户端是否正在运行（系统托盘查看图标）
- 确认 Drive 映射盘符（可能是 `G:\` 或其他盘符）
- 打开文件资源管理器，查看 Google Drive 的实际路径
- 修改 `kiro_sync_to_drive.py` 中的 `DRIVE_SYNC_PATH` 为实际路径

**问题：Gemini 看不到最新代码**
- 确认 Drive 同步已完成（G 盘图标不再旋转）
- **关键：在 Gemini 中开启新对话**（旧对话不会自动刷新知识库）
- 检查 Gem 的 Knowledge 设置是否选择了**整个文件夹**而不是单个文件
- 确认文件夹内有代码文件（不是空的）
- 尝试在 Gemini 中重新添加 Knowledge 源

**问题：同步的文件太少或太多**
- 太少：检查源目录路径是否正确，查看脚本输出的统计信息
- 太多：检查是否有不需要的文件类型，可在脚本中添加更多 `IGNORE_EXTENSIONS`
- 查看脚本输出的"已过滤"数量，确认过滤规则是否生效

## 高级配置

### 修改源项目路径
编辑 `kiro_sync_to_drive.py` 第 11 行：
```python
SOURCE_PROJECT_DIR = r"C:\Godot\你的项目名"
```

### 修改 Drive 目标路径
编辑 `kiro_sync_to_drive.py` 第 16 行：
```python
DRIVE_SYNC_PATH = r"G:\My Drive\你的文件夹名"
```

### 添加过滤规则
在 `IGNORE_EXTENSIONS` 或 `IGNORE_DIRS` 中添加新的文件类型或目录名。

### 自动化同步
可以配合 Git hooks 或 IDE 的 File Watcher 实现保存时自动同步。

## 文件说明

- `kiro_sync_to_drive.py` - 核心同步脚本
- `SYNC_TO_GEMINI.bat` - 一键启动器（放在 3d-practice 根目录）
- `SYNC_TO_DRIVE.bat` - 备用启动器（可从任意位置运行）
- `SYNC_LOGIC.md` - 架构设计文档
- `README.md` - 本文档
