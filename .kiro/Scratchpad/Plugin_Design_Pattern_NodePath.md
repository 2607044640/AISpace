# 插件设计模式：如何优雅地引用节点

**日期**: 2026-04-16  
**研究对象**: GodotStateCharts, PhantomCamera

---

## 🔍 研究发现

### StateChart 的设计

```gdscript
# compound_state.gd
@export_node_path("StateChartState") var initial_state: NodePath

@onready var _initial_state: StateChartState = get_node_or_null(initial_state)
```

```gdscript
# transition.gd
@export_node_path("StateChartState") var to: NodePath

# 运行时解析
var _target: StateChartState = get_node_or_null(to)
```

### PhantomCamera 的设计

```gdscript
# phantom_camera_2d.gd
@export_node_path("TileMapLayer", "CollisionShape2D") var limit_target: NodePath

# tween_director_resource.gd
@export_node_path("PhantomCamera2D", "PhantomCamera3D") var from_phantom_cameras: Array[NodePath]
@export_node_path("PhantomCamera2D", "PhantomCamera3D") var to_phantom_cameras: Array[NodePath]
```

---

## 💡 设计模式总结

### GDScript 插件的最佳实践

```gdscript
# 1. 使用 @export_node_path 暴露属性（带类型限制）
@export_node_path("TargetNodeType") var target: NodePath

# 2. 使用 @onready 延迟查找（避免 _ready() 时机问题）
@onready var _target_node = get_node_or_null(target)

# 3. 运行时验证
func _ready():
    if not is_instance_valid(_target_node):
        push_error("Target node not found!")
```

**优势**：
- ✅ 编辑器里可以**点击选择**节点（人类友好）
- ✅ 支持**手动输入**路径，包括 `%` 语法（AI 友好）
- ✅ 有**类型限制**（防止选错类型）
- ✅ 使用 `@onready` 避免初始化时机问题

---

## 🎯 我们的 C# 组件应该怎么做？

### 方案对比

#### 方案 A：Export NodePath（推荐给用户手动配置的场景）

```csharp
public partial class MyComponent : Node
{
    [Export] public NodePath TargetNode { get; set; }
    
    private Control _target;
    
    public override void _Ready()
    {
        _target = GetNodeOrNull<Control>(TargetNode);
        if (_target == null)
        {
            GD.PushError("Target node not found!");
        }
    }
}
```

**适用场景**：
- 用户需要在编辑器里手动配置
- 目标节点不固定
- 需要灵活性

#### 方案 B：Python 生成器自动绑定（推荐给自动化场景）

```python
# Python 生成器
scene.assign_node_path("MyComponent", "TargetNode", "TargetNodeName")

# 生成的 .tscn
[node name="MyComponent" ...]
TargetNode = NodePath("%TargetNodeName")  # 自动生成

# C# 代码不需要 [Export]，直接用
public partial class MyComponent : Node
{
    public NodePath TargetNode { get; set; }  // 从 .tscn 加载
    
    private Control _target;
    
    public override void _Ready()
    {
        _target = GetNodeOrNull<Control>(TargetNode);
    }
}
```

**适用场景**：
- 场景完全由 Python 生成
- 节点关系固定
- 不需要用户手动配置

---

## 📝 当前项目的选择

我们的项目使用**方案 B**（Python 生成器自动绑定）：

### 为什么？
1. ✅ 场景完全由 Python 生成，不需要用户手动配置
2. ✅ 节点关系固定（BackpackGridComponent 总是引用 BackpackGridComponent）
3. ✅ 自动化程度高，减少人为错误

### 当前实现
```python
# Python 生成器
scene.assign_node_path("BackpackInteractionController", "LogicGrid", "BackpackGridComponent")
scene.assign_node_path("BackpackInteractionController", "ViewGrid", "BackpackPanel")

# 生成的 .tscn
[node name="BackpackInteractionController" ...]
LogicGrid = NodePath("%BackpackGridComponent")
ViewGrid = NodePath("%BackpackPanel")

# C# 代码
public partial class BackpackInteractionController : Node
{
    [Export] public NodePath LogicGrid { get; set; }
    [Export] public NodePath ViewGrid { get; set; }
    
    public override void _Ready()
    {
        var logicGrid = GetNodeOrNull<BackpackGridComponent>(LogicGrid);
        var viewGrid = GetNodeOrNull<BackpackGridUIComponent>(ViewGrid);
    }
}
```

**注意**：C# 代码里的 `[Export]` 只是为了让 Godot 知道这个属性可以从 .tscn 加载，不是为了在编辑器里手动配置。

---

## 🔧 改进建议

### 当前 C# 代码的问题

```csharp
// ❌ 问题：硬编码相对路径或节点名
var draggable = itemEntity.GetNodeOrNull<DraggableItemComponent>("DraggableItemComponent");
var stateChart = GetParent()?.GetNodeOrNull<Node>("StateChart");
TargetUI = GetNodeOrNull<Control>("../../../..");
```

### 改进方案 1：使用 % 语法（如果节点已标记 unique）

```csharp
// ✅ 如果节点已标记 unique_name_in_owner=true
var draggable = GetNodeOrNull<DraggableItemComponent>("%DraggableItemComponent");
var stateChart = GetNodeOrNull<Node>("%StateChart");
var targetUI = GetNodeOrNull<Control>("%TestItem");
```

### 改进方案 2：Export NodePath（如果需要灵活性）

```csharp
// ✅ 让 Python 生成器自动绑定
[Export] public NodePath DraggableComponent { get; set; }
[Export] public NodePath StateChartNode { get; set; }
[Export] public NodePath TargetUI { get; set; }

public override void _Ready()
{
    var draggable = GetNodeOrNull<DraggableItemComponent>(DraggableComponent);
    var stateChart = GetNodeOrNull<Node>(StateChartNode);
    var targetUI = GetNodeOrNull<Control>(TargetUI);
}
```

---

## ✅ 结论

1. **GDScript 插件**：使用 `@export_node_path` + `@onready`
2. **C# 自动化场景**：使用 Python 生成器 + `[Export] NodePath`
3. **C# 手动查找**：使用 `%` 语法（前提是节点标记了 unique）
4. **禁止**：硬编码相对路径（`../../../NodeName`）

---

## 📚 参考

- [Godot @export_node_path 文档](https://docs.godotengine.org/en/stable/classes/class_@gdscript.html#class-gdscript-annotation-export-node-path)
- [Godot Scene Unique Nodes 文档](https://docs.godotengine.org/en/latest/tutorials/scripting/scene_unique_nodes.html)
- GodotStateCharts 源码：`compound_state.gd`, `transition.gd`
- PhantomCamera 源码：`phantom_camera_2d.gd`, `tween_director_resource.gd`
