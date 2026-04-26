# Hard Bug: Ghost Nodes — BackpackGridUIComponent

## 症状
运行时出现 **双层 GridCellUI**（60个背景格子生成两次，共120个），视觉上格子重叠。

## 根因（已确认）
`BackpackGridUIComponent` 带 `[Tool]` 属性，导致脚本在**编辑器里也执行** `_EnterTree()` / `_Ready()`。
Godot 编辑器将 `[Tool]` 脚本动态创建的节点写入 `.tscn`（即使设了 `Owner = null` 也无法阻止父节点本身被保存）。
每次场景在编辑器里打开或脚本热重载，就在场景树里创建出新的 Ghost BackpackGridUIComponent 节点（parent 位置不固定），运行时 `%BackpackGridComponent` 全局唯一名称查找让 Ghost 也成功初始化并生成60格。

## Ghost 节点表现
| 时间 | Ghost 父节点 | unique_id |
|---|---|---|
| 第1次发现 | `Background`（ColorRect）| 1234119648 |
| 第2次发现 | `.`（BackpackTest 根）| 471107635 |
| 规律 | 每次编辑器重载后 unique_id 变化，父节点不稳定 |

## 修复措施（三层）
1. **根治**：移除 `BackpackGridUIComponent` 的 `[Tool]` 属性（脚本不再在编辑器运行，Ghost 无法被创建）
2. **清洁**：手动从 `BackpackTest.tscn` 删除所有 Ghost 节点
3. **防复发**：在 `InitializeComponent()` 加 `IsAncestorOf(BackpackGridComp)` 守卫，阻止 Ghost 通过 `%` 全局查找偷偷初始化

## 遗留架构问题（未解决）
`BackpackPanel` 节点本身挂载了 `BackpackGridUIComponent` 脚本（`script = ExtResource("2_res")`）。
这导致"BackpackGridUIComponent 在哪？"的困惑：场景树里没有名为 BackpackGridUIComponent 的独立节点，但功能实际由 BackpackPanel 提供。
**建议**：将 BackpackGridUIComponent 从 BackpackPanel 上剥离，改为一个独立子节点，使架构意图更清晰。（见下方重构方案）

## 推荐重构方案（待执行）
```
BackpackPanel (Control, 纯容器)
├── BackpackGridUIComponent (Control + script)   ← 新增独立节点
│   ├── BackpackGridComponent (Node + script)    ← 移至此处
│   └── BackgroundCanvas (运行时自动创建)
└── ItemsContainer (Control)
    └── TsItem
```
