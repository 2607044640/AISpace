# StateChart Transition 更好的解决方案

**日期**: 2026-04-16  
**问题**: 相对路径 `../../Dragging` 太脆弱，层级一变就炸

---

## 用户痛点

> "你AI看的那么麻烦，不确定有几层，父节点有几个人类能看，AI看个屁，能不能有其他函数，全局找这个节点？"

**核心问题**：
- ❌ 相对路径 `NodePath("../../Dragging")` 依赖层级结构
- ❌ 层级一变，路径就失效
- ❌ 人类难读，AI 也难算
- ❌ 维护成本高

---

## 解决方案对比

### 方案 1: Godot Scene Unique Nodes (推荐！)

**原理**: 用 `%` 符号标记节点，全局查找，不管层级

#### 实现步骤

1. **在 Godot 编辑器中标记状态节点**：
   - 右键点击 `Dragging` 状态节点
   - 选择 "Access as Unique Name"
   - 节点名旁边会出现 `%` 符号

2. **Python 生成器使用 unique name**：
```python
def add_transition(self, name, from_state, to_state, event="", delay=0.0):
    # 不需要计算相对路径！
    # 直接用 % 符号 + 节点名
    transition_node = self.builder.add_node(name, "Node", parent=from_state,
        script=f'ExtResource("{res_id}")')
    
    # ✅ 使用 unique name，不管层级多深
    transition_node.set_property("to", f'NodePath("%{to_state}")')
    transition_node.set_property("delay_in_seconds", delay)
    
    if event:
        transition_node.set_property("event", f'&"{event}"')
```

3. **生成的 .tscn 文件**：
```gdscript
[node name="ToDragging" type="Node" parent="StateChart/Root/Idle"]
to = NodePath("%Dragging")    # ✅ 全局查找，不管层级！
delay_in_seconds = 0.0
event = &"drag_start"
```

#### 优点
- ✅ 不依赖层级结构
- ✅ 人类易读：`%Dragging` 一眼就懂
- ✅ AI 易生成：不需要计算相对路径
- ✅ 维护成本低：移动节点不影响路径
- ✅ Godot 原生支持，性能好（有缓存）

#### 限制
- ⚠️ 只能在同一个场景内查找（不能跨场景）
- ⚠️ 节点名必须唯一（同一场景内不能有重名）

---

### 方案 2: Export 属性 + 编辑器拖拽

**原理**: 在 Transition 脚本中暴露 `[Export]` 属性，让用户在编辑器里拖拽绑定

#### 实现（需要修改 GodotStateCharts 插件源码）

```gdscript
# transition.gd (插件源码)
extends Node
class_name Transition

@export var to: NodePath  # 已有的属性
@export var event: StringName
@export var delay_in_seconds: float = 0.0

# 或者改成直接引用节点（更直观）
@export var target_state: Node  # 新增：直接拖拽目标状态节点
```

#### 优点
- ✅ 最直观：在编辑器里拖拽绑定
- ✅ 不会出错：编辑器自动计算路径
- ✅ 支持跨场景引用

#### 缺点
- ❌ 需要修改插件源码
- ❌ 无法用 Python 自动生成（必须手动绑定）
- ❌ 不适合我们的场景生成器工作流

---

### 方案 3: 绝对路径（不推荐）

```python
# 从 StateChart 根节点开始的绝对路径
transition_node.set_property("to", f'NodePath("Root/Dragging")')
```

#### 缺点
- ❌ 破坏场景实例化（Instancing）
- ❌ 无法复用场景
- ❌ 官方文档明确不推荐

---

## 推荐方案：Scene Unique Nodes

**为什么选这个**：
1. ✅ Godot 原生支持，不需要改插件
2. ✅ 完美适配我们的 Python 生成器工作流
3. ✅ 人类和 AI 都易读易维护
4. ✅ 性能好（Godot 有缓存机制）

**实施计划**：
1. 修改 `statechart.py` 的 `add_transition()` 方法
2. 改用 `NodePath("%{to_state}")` 格式
3. 在场景生成器中，给所有状态节点标记 unique name
4. 更新文档和示例

---

## 代码对比

### 当前方案（相对路径）
```python
# ❌ 复杂：需要计算相对路径
transition_node = self.builder.add_node(name, "Node", parent=from_state, ...)
relative_path = transition_node.get_relative_path_to(to_node)  # "../../Dragging"
transition_node.set_property("to", f'NodePath("{relative_path}")')
```

### 新方案（Unique Name）
```python
# ✅ 简单：直接用节点名
transition_node = self.builder.add_node(name, "Node", parent=from_state, ...)
transition_node.set_property("to", f'NodePath("%{to_state}")')  # "%Dragging"
```

---

## 参考资料

- [Godot Scene Unique Nodes 官方文档](https://docs.godotengine.org/en/latest/tutorials/scripting/scene_unique_nodes.html)
- [GodotStateCharts 官方文档 - Transitions](https://derkork.github.io/godot-statecharts/usage/events-and-transitions)

---

## 下一步

- [ ] 验证 GodotStateCharts 是否支持 `%` 语法（需要测试）
- [ ] 如果支持，修改 `statechart.py`
- [ ] 更新场景生成器，自动标记状态节点为 unique
- [ ] 更新文档
