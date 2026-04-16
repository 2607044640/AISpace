# 为什么 initial_state 必须用 %，而 transition 不需要？

**日期**: 2026-04-16  
**观察**: `initial_state = NodePath("%Idle")` 必须用 `%`，否则警告。但 `to = NodePath("../../Dragging")` 不用 `%` 也能工作。

---

## 核心原因：解析时机不同

### 1. **initial_state 在 _ready() 时解析（节点树未完全构建）**

```gdscript
# CompoundState 的 _ready() 伪代码
func _ready():
    # 此时子节点可能还没完全加载！
    var initial = get_node(initial_state)  # 如果用相对路径可能找不到
    if initial:
        activate_state(initial)
```

**问题**：
- Godot 的 `_ready()` 调用顺序是**从子节点到父节点**
- 当 `CompoundState` 的 `_ready()` 执行时，它的子状态节点可能还没完全初始化
- 相对路径 `NodePath("Idle")` 可能找不到节点（因为 `Idle` 还没准备好）
- **Unique Name (`%Idle`) 使用延迟查找机制**，等到真正需要时才解析，此时节点树已完全构建

### 2. **transition 的 to 在运行时解析（节点树已完全构建）**

```gdscript
# Transition 的 _handle_transition() 伪代码
func _handle_transition():
    # 此时整个场景已经完全加载并运行了！
    var target = get_node(to)  # 相对路径可以正常工作
    if target:
        switch_to_state(target)
```

**为什么可以用相对路径**：
- Transition 只在**运行时**（收到事件后）才解析 `to` 路径
- 此时整个节点树已经完全构建并初始化完成
- 相对路径 `../../Dragging` 可以正常工作，因为所有节点都已存在

---

## 技术细节：Godot 的 _ready() 调用顺序

```
场景树：
StateChart
└── Root (CompoundState)
    ├── Idle (AtomicState)
    └── Dragging (AtomicState)

_ready() 调用顺序：
1. Idle._ready()          ← 子节点先执行
2. Dragging._ready()      ← 子节点先执行
3. Root._ready()          ← 父节点后执行（此时需要找 initial_state）
4. StateChart._ready()    ← 根节点最后执行
```

**问题场景**：
- 当 `Root._ready()` 执行时，它需要激活 `initial_state`
- 如果用相对路径 `NodePath("Idle")`，此时 `Idle` 虽然已经 `_ready()` 了，但可能还没完全注册到场景树
- **Unique Name 机制绕过了这个问题**，因为它使用全局查找，不依赖即时的节点树状态

---

## 为什么之前 ../Dragging 失败，../../Dragging 成功？

**这是两个不同的问题！**

### 问题 1：相对路径层级算错（已修复）
```
❌ 错误：to = NodePath("../Dragging")
   从 ToDragging 节点出发：ToDragging → Idle → Dragging（找不到！）

✅ 正确：to = NodePath("../../Dragging")
   从 ToDragging 节点出发：ToDragging → Idle → Root → Dragging（找到了！）
```

### 问题 2：initial_state 需要 unique name（设计限制）
```
❌ 不稳定：initial_state = NodePath("Idle")
   在 _ready() 时解析，可能找不到子节点

✅ 稳定：initial_state = NodePath("%Idle")
   延迟查找，等节点树完全构建后再解析
```

---

## 最佳实践建议

### 方案 A：全部使用 Unique Name（推荐）
```python
# 所有状态标记为 unique
def add_atomic_state(self, name, parent):
    return self.builder.add_node(name, "Node", parent=parent,
        script=f'ExtResource("{res_id}")',
        unique_name_in_owner=True
    )

# initial_state 和 transition 都用 %
compound_node.set_property("initial_state", f'NodePath("%{initial_name}")')
transition_node.set_property("to", f'NodePath("%{to_state}")')
```

**优点**：
- ✅ 统一风格，易维护
- ✅ 不依赖层级结构
- ✅ 移动节点不会破坏路径
- ✅ 人类和 AI 都易读

### 方案 B：混合使用（可行但不推荐）
```python
# initial_state 必须用 %
compound_node.set_property("initial_state", f'NodePath("%{initial_name}")')

# transition 可以用相对路径
relative_path = transition_node.get_relative_path_to(to_node)
transition_node.set_property("to", f'NodePath("{relative_path}")')
```

**缺点**：
- ❌ 风格不统一
- ❌ 相对路径依然脆弱
- ❌ 维护成本高

---

## 总结

| 属性 | 解析时机 | 是否必须用 % | 原因 |
|------|---------|-------------|------|
| `initial_state` | `_ready()` 时 | **是** | 子节点可能未完全初始化 |
| `transition.to` | 运行时（收到事件后） | 否 | 节点树已完全构建 |

**推荐**：全部使用 Unique Name (`%`)，统一风格，避免所有潜在问题。

---

## 参考资料

- [GodotStateCharts 官方文档 - Nodes](https://derkork.github.io/godot-statecharts/usage/nodes)
- [Godot Scene Unique Nodes 官方文档](https://docs.godotengine.org/en/latest/tutorials/scripting/scene_unique_nodes.html)
