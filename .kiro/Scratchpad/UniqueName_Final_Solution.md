# Scene Unique Names - 最终解决方案

**日期**: 2026-04-16  
**状态**: ✅ 已实施并验证

---

## 🎯 核心规则

### **禁止使用相对路径，只能用 % 语法**

```python
# ❌ 禁止
NodePath("../../../NodeName")
NodePath("../../Dragging")
NodePath("..")

# ✅ 必须
NodePath("%NodeName")
NodePath("%Dragging")
NodePath("%BackpackPanel")
```

---

## 💡 为什么？

### 相对路径的问题
- ❌ **AI 容易出错**：需要计算层级，容易算错
- ❌ **人类难读**：`../../../..` 数不清有几层
- ❌ **脆弱**：移动节点就炸
- ❌ **维护成本高**：重构时需要更新所有路径

### Unique Name 的优势
- ✅ **AI 友好**：不需要计算，直接用节点名
- ✅ **人类易读**：`%Dragging` 一眼就懂
- ✅ **稳定**：移动节点不影响路径
- ✅ **维护成本低**：重构时路径自动有效

---

## 🔧 实现方式

### Python 生成器

```python
# 1. assign_node_path 自动标记目标节点为 unique
def assign_node_path(self, target_node_name, property_name, path_to_node_name):
    path_to_node = self.get_node(path_to_node_name)
    
    # 自动标记为 unique
    if not path_to_node.properties.get("unique_name_in_owner"):
        path_to_node.set_property("unique_name_in_owner", True)
    
    # 使用 % 语法
    target_node.set_property(property_name, f'NodePath("%{path_to_node_name}")')

# 2. StateChart 状态节点自动标记为 unique
def add_atomic_state(self, name, parent):
    return self.builder.add_node(name, "Node", parent=parent,
        script=f'ExtResource("{res_id}")',
        unique_name_in_owner=True  # 自动标记
    )
```

### 生成的 .tscn 文件

```gdscript
# 只有需要被查找的节点才标记 unique
[node name="BackpackGridComponent" type="Node" parent="..."]
script = ExtResource("3_res")
unique_name_in_owner = true  # ✅ 被 [Export] 引用，标记为 unique

[node name="BackpackInteractionController" type="Node" parent="..."]
script = ExtResource("4_res")
LogicGrid = NodePath("%BackpackGridComponent")  # ✅ 使用 % 查找
ViewGrid = NodePath("%BackpackPanel")           # ✅ 使用 % 查找

[node name="ColorRect" type="ColorRect" parent="..."]
color = Color(0.2, 0.2, 0.2, 0.5)
# ❌ 不需要被查找，不标记 unique
```

---

## 📝 C# 代码建议

### 当前代码（混乱）

```csharp
// ❌ 相对路径，难读难维护
LogicGrid = GetNodeOrNull<BackpackGridComponent>("BackpackGridComponent");
LogicGrid = GetNodeOrNull<BackpackGridComponent>("../BackpackGridComponent");
ViewGrid = GetNodeOrNull<BackpackGridUIComponent>("..");
var draggable = itemEntity.GetNodeOrNull<DraggableItemComponent>("DraggableItemComponent");
var shapeComponent = itemEntity.GetNodeOrNull<GridShapeComponent>("GridShapeComponent");
itemControl = itemEntity.GetNodeOrNull<Control>(".");
StateChart = GetParent()?.GetNodeOrNull<Node>("StateChart");
TargetUI = GetNodeOrNull<Control>("../../../..");
```

### 推荐代码（清晰）

```csharp
// ✅ Scene Unique Names，清晰易维护
LogicGrid = GetNodeOrNull<BackpackGridComponent>("%BackpackGridComponent");
ViewGrid = GetNodeOrNull<BackpackGridUIComponent>("%BackpackPanel");
var draggable = GetNodeOrNull<DraggableItemComponent>("%DraggableItemComponent");
var shapeComponent = GetNodeOrNull<GridShapeComponent>("%GridShapeComponent");
itemControl = GetNodeOrNull<Control>("%TestItem");
StateChart = GetNodeOrNull<Node>("%StateChart");
TargetUI = GetNodeOrNull<Control>("%TestItem");
```

**优势**：
- 代码自文档化（一眼看出找的是哪个节点）
- 重构安全（移动节点不破坏代码）
- 不需要数 `../` 有几层

---

## ⚠️ 限制

1. **同一场景内节点名必须唯一**
   - 如果动态生成多个同名节点（如多个 `Item`），会冲突
   - 解决方案：给每个实例唯一的名字（`Item1`, `Item2`）

2. **只能在同一场景内查找**
   - 不能跨场景使用 `%`
   - 跨场景引用需要用其他方式（如 Autoload, Groups）

---

## ✅ 验证

场景已测试，所有功能正常：
- StateChart 状态转换 ✅
- [Export] 属性绑定 ✅
- 拖拽功能 ✅
- 没有任何 NodePath 错误 ✅

---

## 📚 参考

- [Godot Scene Unique Nodes 官方文档](https://docs.godotengine.org/en/latest/tutorials/scripting/scene_unique_nodes.html)
- `KiroWorkingSpace/.kiro/steering/Godot/SceneBuilders/GodotTscnBuilder_Context.md` (已更新规则)
