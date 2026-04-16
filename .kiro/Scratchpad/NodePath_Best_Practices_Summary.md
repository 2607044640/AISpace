# NodePath 最佳实践 - 最终规则

**日期**: 2026-04-16  
**状态**: ✅ 已更新到 DesignPatterns.md 和 GodotTscnBuilder_Context.md

---

## 🎯 核心规则

### **强制使用 Scene Unique Names (%) + 默认值**

```csharp
// ✅ 正确模式
[Export] public NodePath StateChartNode { get; set; } = "%StateChart";
[Export] public NodePath TargetUI { get; set; } = "%TestItem";
[Export] public NodePath LogicGrid { get; set; } = "%BackpackGridComponent";

public override void _Ready()
{
    // 运行时验证
    var stateChart = GetNodeOrNull<Node>(StateChartNode);
    if (stateChart == null)
    {
        GD.PushError($"[{Name}] StateChart not found at: {StateChartNode}");
        return;
    }
}
```

---

## ❌ 禁止的模式

### 1. 硬编码相对路径
```csharp
// ❌ 禁止
var stateChart = GetParent()?.GetNodeOrNull<Node>("StateChart");
var targetUI = GetNodeOrNull<Control>("../../../..");
var logic = GetNodeOrNull<Component>("../BackpackGridComponent");
```

### 2. 没有默认值的 NodePath
```csharp
// ❌ 禁止
[Export] public NodePath LogicGrid { get; set; }  // 用户必须手动配置
```

### 3. 直接 GetNode 不验证
```csharp
// ❌ 禁止
var stateChart = GetNode<Node>(StateChartNode);  // 找不到会崩溃
```

---

## ✅ 正确的完整模式

```csharp
public partial class MyComponent : Node
{
    // 1. 声明 NodePath 属性，带默认值
    [Export] public NodePath StateChartNode { get; set; } = "%StateChart";
    [Export] public NodePath TargetUI { get; set; } = "%TestItem";
    
    // 2. 缓存节点引用
    private Node _stateChart;
    private Control _targetUI;
    
    public override void _Ready()
    {
        // 3. 查找并验证
        _stateChart = GetNodeOrNull<Node>(StateChartNode);
        if (_stateChart == null)
        {
            GD.PushError($"[{Name}] StateChart not found at: {StateChartNode}");
            return;
        }
        
        _targetUI = GetNodeOrNull<Control>(TargetUI);
        if (_targetUI == null)
        {
            GD.PushError($"[{Name}] TargetUI not found at: {TargetUI}");
            return;
        }
        
        // 4. 初始化逻辑
        InitializeComponent();
    }
}
```

---

## 🔧 Python 生成器的配合

Python 生成器会自动：
1. 标记被引用的节点为 `unique_name_in_owner = true`
2. 生成 `NodePath("%NodeName")` 格式的路径
3. 覆盖 C# 的默认值（如果需要）

```python
# Python 生成器
scene.assign_node_path("MyComponent", "StateChartNode", "StateChart")

# 生成的 .tscn
[node name="StateChart" ...]
unique_name_in_owner = true  # 自动标记

[node name="MyComponent" ...]
StateChartNode = NodePath("%StateChart")  # 覆盖默认值
```

---

## 📊 优势对比

| 特性 | 相对路径 | % + 默认值 |
|------|---------|-----------|
| **可读性** | ❌ `"../../../Node"` 难读 | ✅ `"%Node"` 清晰 |
| **维护性** | ❌ 移动节点就炸 | ✅ 重构安全 |
| **AI 生成** | ❌ 容易算错层级 | ✅ 不需要计算 |
| **自文档化** | ❌ 看不出找什么 | ✅ 一眼看出目标 |
| **运行时验证** | ❌ 通常不验证 | ✅ 强制验证 |
| **Python 覆盖** | ❌ 难以覆盖 | ✅ 自动覆盖 |

---

## 🎓 学习自插件设计

### GodotStateCharts
```gdscript
@export_node_path("StateChartState") var to: NodePath
@onready var _target = get_node_or_null(to)
```

### PhantomCamera
```gdscript
@export_node_path("PhantomCamera2D", "PhantomCamera3D") var target: NodePath
```

**共同点**：
- 使用 `@export_node_path` 暴露属性
- 支持编辑器点选和手动输入（包括 `%`）
- 运行时用 `get_node_or_null` 查找并验证

---

## 📝 已更新的文档

1. ✅ `.kiro/steering/Always/DesignPatterns.md`
   - 添加了 Scene Unique Names 规则
   - 更新了 top_anti_patterns

2. ✅ `KiroWorkingSpace/.kiro/steering/Godot/SceneBuilders/GodotTscnBuilder_Context.md`
   - 添加了禁止相对路径的核心规则
   - 包含 C# 代码示例

3. ✅ `KiroWorkingSpace/builder/core.py`
   - `assign_node_path` 自动标记目标节点为 unique
   - 自动使用 `%` 语法

4. ✅ `KiroWorkingSpace/builder/modules/statechart.py`
   - 状态节点自动标记为 unique
   - Transition 使用 `%` 语法

---

## ✅ 验证

场景已测试，所有功能正常：
- StateChart 状态转换 ✅
- [Export] 属性绑定 ✅
- 拖拽功能 ✅
- 没有任何 NodePath 错误 ✅

---

**规则已完全实施！** 🎉
