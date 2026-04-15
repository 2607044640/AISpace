# BackpackTest 场景 Bug 修复指南

## 问题诊断结果

### 测试执行
```
mcp_godot_run_project(projectPath="c:/Godot/3d-practice", scene="Scenes/BackpackTest.tscn")
mcp_godot_get_debug_output()
mcp_godot_stop_project()
```

### 发现的错误
```
ERROR: BackpackInteractionController: LogicGrid 未设置！
ERROR: BackpackInteractionController: ViewGrid 未设置！
ERROR: FollowMouseUIComponent: TargetUI 未设置！
WARNING: DraggableItemComponent: ClickableArea 未设置
ERROR: UITweenInteractComponent: VisualTarget 未设置！
ERROR: BackpackGridUIComponent: LogicGrid 未设置！
```

## 根本原因分析

### 问题 1: BackpackPanel 缺少 LogicGrid 绑定
- **节点**: `BackpackPanel` (有 `BackpackGridUIComponent` 脚本)
- **脚本期望**: `[Export] public BackpackGridComponent LogicGrid { get; set; }`
- **当前状态**: 生成器脚本没有为 `BackpackPanel` 设置 `LogicGrid` 属性
- **影响**: BackpackGridUIComponent 无法访问逻辑网格，导致坐标转换失败

### 问题 2: 其他组件的 NodePath 绑定已正确生成
- `Controller` 的 `LogicGrid` 和 `ViewGrid` ✓ 已生成
- `FollowMouseUI` 的 `TargetUI` ✓ 已生成
- `Draggable` 的 `ClickableArea` 和 `StateChart` ✓ 已生成
- `TweenInteract` 的 `InteractionArea` 和 `VisualTarget` ✓ 已生成
- `Synergy` 的 `Shape` ✓ 已生成

## 修复方案

### 需要修改的文件
`KiroWorkingSpace/.kiro/scripts/temp/generate_backpack_test_v2.py`

### 修复位置
在第 289 行之前（NodePath 绑定部分），添加：

```python
# ============================================================
# 19. 绑定所有 NodePath
# ============================================================

# BackpackPanel 绑定（新增！）
scene.assign_node_path("BackpackPanel", "LogicGrid", "LogicGrid")

# Controller 绑定
scene.assign_multiple_node_paths("Controller", {
    "LogicGrid": "LogicGrid",
    "ViewGrid": "BackpackPanel"
})

# ... 其余绑定保持不变 ...
```

### 为什么需要这个修复？

1. **BackpackPanel 节点有脚本**: 它附加了 `BackpackGridUIComponent.cs`
2. **脚本有 [Export] 属性**: `LogicGrid` 需要引用逻辑网格组件
3. **生成器遗漏了绑定**: 只绑定了 `Controller`，忘记了 `BackpackPanel` 自己也需要绑定

### 验证修复的步骤

1. 修改生成器脚本（添加上述代码）
2. 重新运行生成器：
   ```bash
   cd KiroWorkingSpace
   python .kiro/scripts/temp/generate_backpack_test_v2.py
   ```
3. 使用 Godot MCP 工具测试：
   ```python
   mcp_godot_run_project(projectPath="c:/Godot/3d-practice", scene="Scenes/BackpackTest.tscn")
   mcp_godot_get_debug_output()
   mcp_godot_stop_project()
   ```
4. 确认输出中：
   - ✓ 没有 "未设置" 错误
   - ✓ 看到 "BackpackGridUIComponent: 初始化完成" 消息
   - ✓ 看到 "BackpackInteractionController: 初始化完成" 消息

## 关键教训

### 规则：检查所有带脚本的节点
生成场景时，必须检查 **每个** 附加了 C# 脚本的节点：
1. 读取脚本文件
2. 查找所有 `[Export]` 属性
3. 为每个属性调用 `assign_node_path()`

### 常见遗漏模式
- ✗ 只绑定 Controller 节点
- ✗ 忘记 UI 组件节点（如 BackpackPanel）
- ✗ 忘记 Component 节点（如 Draggable, Shape）
- ✓ 系统化检查所有脚本的所有 [Export] 属性

## 下一步操作

用户需要：
1. 打开 `KiroWorkingSpace/.kiro/scripts/temp/generate_backpack_test_v2.py`
2. 在第 289 行之前添加：
   ```python
   # BackpackPanel 绑定
   scene.assign_node_path("BackpackPanel", "LogicGrid", "LogicGrid")
   ```
3. 保存文件
4. 重新运行生成器脚本
5. 使用 Godot MCP 工具测试验证

AI 不应该直接修改 .tscn 文件，而应该修复生成器脚本，让它生成正确的输出。
