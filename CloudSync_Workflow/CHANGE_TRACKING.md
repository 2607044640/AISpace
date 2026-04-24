# 🔄 变更追踪系统说明

## 📌 功能概述

自动检测和记录 AI 上下文文件的变更，生成类似 `git diff` 的对比报告，帮助 AI 和开发者快速了解项目的演进历史。

---

## 🎯 核心特性

### 1. **自动变更检测**
- 对比前后两次生成的文件清单
- 使用 MD5 哈希快速识别变化的文件
- 分类统计：新增、修改、删除

### 2. **详细 Diff 生成**
- 类似 `git diff` 的 unified diff 格式
- 显示变更行周围的 **5 行上下文**
- 使用 `+` 和 `-` 标记新增和删除的行

### 3. **历史记录管理**
- 保留最近 **5 次**变更记录
- 超过 5 次的旧记录自动清除
- 每次记录包含时间戳和变更摘要

### 4. **性能优化**
- 只对变化的文件生成 diff
- 限制单个 diff 最多 200 行（避免过大）
- 限制最多显示 10 个文件的详细 diff

---

## 📂 生成的文件

### 1. **AI_Context_Manifest.json**
当前文件清单，包含每个文件的哈希值和大小。

```json
{
  "timestamp": "2026-04-19 13:00:00",
  "files": {
    "3d-practice/Player.cs": {
      "hash": "abc123def456...",
      "size": 2048,
      "content": "..."
    }
  }
}
```

### 2. **AI_Context_Manifest_Previous.json**
上一次的文件清单，用于对比。

### 3. **AI_Context_Changes.md**
变更历史记录文件，包含最近 5 次变更的详细对比。

---

## 📊 变更报告格式

### 示例输出：

```markdown
# 🔄 AI Context 变更历史

*保留最近 5 次变更记录*

---

## 📅 变更记录 - 2026-04-19 13:00:00

### 📊 变更摘要
- ✅ 新增文件: 2 个
- 📝 修改文件: 5 个
- ❌ 删除文件: 1 个

### ➕ 新增文件
- `3d-practice/NewFeature.cs`
- `3d-practice/NewComponent.cs`

### ➖ 删除文件
- `3d-practice/OldFile.cs`

### 🔍 详细变更对比

#### 📄 3d-practice/Player.cs

```diff
--- a/3d-practice/Player.cs
+++ b/3d-practice/Player.cs
@@ -10,7 +10,7 @@
 public class Player : CharacterBody3D
 {
     [Export]
-    public float Speed = 5.0f;
+    public float Speed = 10.0f;  // 提升移动速度
     
     public override void _PhysicsProcess(double delta)
     {
```

---

## 🔍 工作原理

### 流程图：

```
第一次运行
    ↓
生成 AI_Context_Master.txt
    ↓
生成 AI_Context_Manifest.json（当前清单）
    ↓
备份为 AI_Context_Manifest_Previous.json
    ↓
（没有上次清单，跳过变更检测）

第二次运行
    ↓
生成新的 AI_Context_Master.txt
    ↓
生成新的 AI_Context_Manifest.json
    ↓
读取 AI_Context_Manifest_Previous.json
    ↓
对比两个清单（哈希值）
    ↓
识别：新增、修改、删除的文件
    ↓
对修改的文件生成 unified diff
    ↓
追加到 AI_Context_Changes.md
    ↓
保留最近 5 次记录
    ↓
备份当前清单为 Previous
```

---

## 🎨 Diff 格式说明

### Unified Diff 格式：

```diff
--- a/文件路径          # 旧版本
+++ b/文件路径          # 新版本
@@ -10,7 +10,7 @@      # 变更位置（旧文件第10行，新文件第10行）
 上下文行1              # 未变更的上下文
 上下文行2
 上下文行3
-删除的行               # 以 - 开头
+新增的行               # 以 + 开头
 上下文行4
 上下文行5
```

### 符号说明：

| 符号 | 含义 |
|------|------|
| `-` | 删除的行（红色） |
| `+` | 新增的行（绿色） |
| ` ` | 未变更的上下文行 |
| `@@` | 变更位置标记 |

---

## 🚀 使用方法

### 1. 正常运行脚本

```bash
python AISpace/.kiro/CloudSync_Workflow/kiro_sync_to_drive.py
```

### 2. 查看变更报告

打开生成的文件：
```
C:\Users\26070\My Drive\Kiro_Godot_Brain\AI_Context_Changes.md
```

### 3. 理解变更

- **新增文件**：项目中添加了新的代码文件
- **修改文件**：现有文件的内容发生了变化
- **删除文件**：文件被移除或重命名

---

## 📋 限制和优化

### 当前限制：

1. **Diff 大小限制**：单个文件最多显示 200 行变更
2. **文件数量限制**：最多显示 10 个文件的详细 diff
3. **历史记录限制**：只保留最近 5 次变更
4. **内容存储**：Manifest 中保存文件内容用于生成 diff（可能占用较多内存）

### 性能优化：

- ✅ 使用 MD5 哈希快速识别变化
- ✅ 只对变化的文件生成 diff
- ✅ 限制 diff 大小避免过大输出
- ✅ 使用 deque 自动管理历史记录数量

---

## 🔧 配置选项

### 可调整的参数：

在 `kiro_sync_to_drive.py` 中：

```python
# 上下文行数（diff 中显示的周围行数）
n=5  # 在 unified_diff() 调用中

# 最大 diff 行数
if len(diff) > 200:  # 可以调整这个数字

# 最多显示的文件数
for diff_info in detailed_diffs[:10]:  # 可以调整这个数字

# 历史记录数量
records_queue = deque(existing_records, maxlen=5)  # 可以调整这个数字
```

---

## 💡 使用场景

### 1. **代码审查**
快速了解自上次同步以来的所有代码变更。

### 2. **AI 上下文更新**
让 AI 知道项目的最新变化，提供更准确的建议。

### 3. **项目演进追踪**
记录项目的发展历史，了解架构演变。

### 4. **Bug 追踪**
当出现新 Bug 时，查看最近的变更帮助定位问题。

---

## 🐛 故障排查

### 问题：没有生成变更报告

**原因**：首次运行或没有上次清单

**解决**：运行两次脚本，第二次会生成变更报告

---

### 问题：Diff 显示不完整

**原因**：Diff 超过 200 行被截断

**解决**：调整 `if len(diff) > 200:` 中的数字

---

### 问题：内存占用过高

**原因**：Manifest 中保存了所有文件内容

**解决**：
1. 减少包含的文件数量
2. 增加文件大小限制
3. 考虑只保存哈希值（需要修改代码）

---

## 📚 相关文件

- `kiro_sync_to_drive.py` - 主脚本
- `AI_Context_Master_*.txt` - 合并的上下文文件
- `AI_Context_Manifest.json` - 当前文件清单
- `AI_Context_Manifest_Previous.json` - 上次文件清单
- `AI_Context_Changes.md` - 变更历史记录

---

**创建日期**: 2026-04-19  
**版本**: 1.0  
**状态**: ✅ 生产就绪
