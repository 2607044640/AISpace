# 🔄 Kiro Sync - 大模型上下文同步工具

## 📖 简介

Kiro Sync 是一个将 Godot 项目代码、配置和规则文档合并成单一 XML 文件的工具，专为大模型（Gemini/Claude）优化。

## 🎯 核心特性

### 1. XML 结构化格式
- 使用 `<tag>` 标签替代纯文本分隔符
- 大模型对 XML 边界识别能力更强
- 使用 `<![CDATA[...]]>` 包裹代码内容，防止解析错误

### 2. 三明治布局（基于位置权重）
```xml
<system_context>
  <section_1_important_rules>    <!-- 顶部：核心规则（高权重） -->
    <file path="..." priority="CRITICAL">...</file>
  </section_1_important_rules>
  
  <section_2_project_code>       <!-- 中间：项目源码 -->
    <file path="..." priority="NORMAL">...</file>
  </section_2_project_code>
  
  <section_3_recent_changes>     <!-- 底部：近期变更（高权重） -->
    <![CDATA[...]]>
  </section_3_recent_changes>
</system_context>
```

### 3. 智能过滤
- **白名单机制**: A1/B1 前缀文件夹完整包含
- **大小限制**: 代码文件 1MB，资源文件 200KB
- **关键文件**: project.godot 等无视大小限制
- **黑名单**: 排除二进制、缓存、IDE 配置

### 4. 变更检测
- MD5 哈希检测文件变化
- 生成 unified diff 格式
- 保留最近 10 次变更记录
- 使用 `<RECENT_CHANGES>` 标记提升 AI 注意力

## 🚀 使用方法

### 手动运行
```bash
python KiroWorkingSpace/.kiro/CloudSync_Workflow/kiro_sync_to_drive.py
```

### 自动运行（Hook）
脚本会在以下情况自动触发：
- 保存 `.md`, `.json`, `.txt` 文件（KiroWorkingSpace）
- 保存 `.cs`, `.gd`, `.tscn` 文件（3d-practice）
- AI 对话结束时（agentStop 事件）

## 📁 输出文件

### Google Drive（供 AI 查看）
- `AI_Context_Master_YYYYMMDD_HHMMSS.txt` - 主上下文文件（XML 格式）
- `AI_Context_Changes.md` - 变更历史记录

### D 盘备份（本地，不同步）
- `AI_Context_Master_*.txt` - 旧文件备份
- `AI_Context_Manifest.json` - 文件清单（用于变更检测）
- `AI_Context_Manifest_Previous.json` - 上次清单

## ⚙️ 配置说明

### 路径配置
```python
SOURCE_PROJECT_DIR = r"C:\Godot\3d-practice"           # Godot 项目目录
KIRO_WORKSPACE_DIR = r"C:\Godot\KiroWorkingSpace\.kiro" # Kiro 规则目录
DRIVE_SYNC_PATH = r"C:\Users\26070\My Drive\Kiro_Godot_Brain" # Google Drive
LOCAL_BACKUP_PATH = r"D:\Kiro_Godot_Brain_Backup"      # 本地备份
```

### 白名单配置
```python
# KiroWorkingSpace 白名单
KIRO_WHITELIST_DIRS = ['steering', 'docs', 'specs']
KIRO_WHITELIST_FILES = ['ProjectRules.md', 'docLastConversationState.md', 'ConversationReset.md']

# 3d-practice 白名单
PROJECT_WHITELIST_PREFIXES = ['A1', 'B1']  # 前缀匹配
PROJECT_WHITELIST_DIRS = ['Scenes', 'Tests']  # 显式文件夹
```

### 大小限制
```python
CODE_MAX_SIZE_MB = 1.0       # 代码文件最大 1MB
RESOURCE_MAX_SIZE_MB = 0.2   # 资源文件最大 200KB
```

### 关键文件（无视大小限制）
```python
CRITICAL_FILES = {
    'project.godot',
    'default_bus_layout.tres',
    '.gitignore',
    '.gitattributes'
}
```

## 🔍 工作流程

1. **扫描文件**
   - KiroWorkingSpace/.kiro/ (白名单模式)
   - 3d-practice/ (扩展名过滤 + 大小限制)

2. **生成 XML 文件**
   - 顶部：核心规则（CRITICAL/HIGH 优先级）
   - 中间：项目源码（NORMAL 优先级）
   - 底部：近期变更（提升 AI 注意力）

3. **变更检测**
   - 计算文件 MD5 哈希
   - 对比上次 Manifest
   - 生成 unified diff

4. **保存文件**
   - XML 文件 → Google Drive
   - Manifest → D 盘
   - 旧文件 → D 盘备份

## 📊 输出示例

### XML 结构
```xml
<system_context>
  <metadata>
    <description>Godot Sensei Project Context Master File</description>
    <generated_time>2026-04-23 00:58:00</generated_time>
  </metadata>

  <section_1_important_rules>
    <file path=".kiro/ProjectRules.md" priority="CRITICAL">
<![CDATA[
... 核心规则内容 ...
]]>
    </file>
  </section_1_important_rules>

  <section_2_project_code>
    <file path="3d-practice/addons/A1TetrisBackpack/..." priority="NORMAL">
<![CDATA[
... 源码内容 ...
]]>
    </file>
  </section_2_project_code>

  <section_3_recent_changes>
    <![CDATA[
# 🔄 AI Context 变更历史
## 📅 20260423_005935
- ➕ 新增: 0 | 📝 修改: 1 | ❌ 删除: 0
...
]]>
  </section_3_recent_changes>
</system_context>
```

### 变更记录
```markdown
# 🔄 AI Context 变更历史

<RECENT_CHANGES>
## 📅 20260423_005935
- ➕ 新增: 0 | 📝 修改: 1 | ❌ 删除: 0

#### .kiro/steering\Always\MainRules.md
```diff
@@ -3,11 +3,11 @@
-    - Recent Changes: `Get-Content "..." -Head <lines>`
+    - Recent Changes: `Get-Content "..." -Head <lines>` (XML 格式测试)
```
</RECENT_CHANGES>
```

## 💡 使用建议

### 给 AI 的提示词
```
请重点关注 <section_1_important_rules> 中 priority="CRITICAL" 的文件，
这些是项目的核心规则。然后查看 <section_3_recent_changes> 了解最新变更。
```

### 选择性查看
- 核心规则: 搜索 `<section_1_important_rules>`
- 项目源码: 搜索 `<section_2_project_code>`
- 近期变更: 搜索 `<section_3_recent_changes>`
- 特定文件: 搜索 `<file path="..."`

### 优先级说明
- `CRITICAL`: 核心配置文件（project.godot, MainRules.md 等）
- `HIGH`: 重要规则文档（steering, docs, specs）
- `NORMAL`: 普通源码文件

## 🛠️ 故障排除

### 问题：脚本运行失败
**检查**:
1. Python 是否安装（需要 Python 3.7+）
2. 路径配置是否正确
3. Google Drive 是否正常同步

### 问题：文件过大
**解决**:
1. 调整 `CODE_MAX_SIZE_MB` 和 `RESOURCE_MAX_SIZE_MB`
2. 添加更多文件到黑名单
3. 排除不必要的文件夹

### 问题：变更检测不工作
**检查**:
1. `D:\Kiro_Godot_Brain_Backup\AI_Context_Manifest.json` 是否存在
2. 文件权限是否正确
3. 查看脚本输出的错误信息

### 问题：Hook 不触发
**检查**:
1. Hook 配置文件是否存在（`.kiro/hooks/`）
2. 查看 Hook 日志（`.kiro/CloudSync_Workflow/logs/`）
3. 使用 Kiro 命令面板检查 Hook 状态

## 📚 相关文档

- **完成报告**: `REFACTOR_COMPLETE.md` - 重构详细说明
- **原始计划**: `REFACTOR_PLAN.md` - 历史参考（已过时）
- **主规则**: `../steering/Always/MainRules.md` - 项目核心规则
- **设计模式**: `../steering/Always/DesignPatterns.md` - 架构模式

## 🔄 版本历史

### v2.0 (2026-04-23) - XML 重构
- ✅ 采用 XML 结构化格式
- ✅ 实现三明治布局
- ✅ 添加优先级标记
- ✅ 使用 CDATA 包裹代码

### v1.0 (2026-04-22) - 初始版本
- ✅ 纯文本分隔符格式
- ✅ 变更检测功能
- ✅ 白名单机制
- ✅ Hook 自动触发

## 📞 支持

如有问题，请查看：
1. 脚本输出的错误信息
2. `REFACTOR_COMPLETE.md` 中的故障排除部分
3. Kiro 日志文件

## 🎉 总结

Kiro Sync 是一个基于大模型认知原理设计的上下文同步工具，采用 XML 结构和三明治布局，智能过滤和变更检测，自动同步到 Google Drive，为 AI 提供最优质的项目上下文。

**核心优势**:
- 🎯 XML 结构（大模型友好）
- 🎯 三明治布局（符合位置权重）
- 🎯 优先级标记（明确重要性）
- 🎯 智能过滤（高信噪比）
- 🎯 变更检测（追踪历史）
- 🎯 自动同步（Hook 触发）
