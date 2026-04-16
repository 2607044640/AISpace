# GodotStateCharts 研究笔记

## 来源
- 官方文档：https://derkork.github.io/godot-statecharts/usage/events-and-transitions
- GitHub：https://github.com/derkork/godot-statecharts

## 关键发现

### 1. Transition 的 NodePath 配置

从文档中没有直接看到 NodePath 的配置示例，但是提到：

> "When you send an event, it can trigger one or more transitions."

### 2. Transition 的属性

Transition 节点有以下属性：
- `event`: 触发事件的名称（可以为空，表示自动转换）
- `to`: 目标状态的 NodePath
- `delay_in_seconds`: 延迟时间（表达式字符串）

### 3. 延迟转换的重要说明

> "Transition delay is an expression, which means you can not only put in a number of seconds, but also use expressions to calculate the delay."

**关键**：`delay_in_seconds` 是一个**表达式**，使用 Godot Expression 类进行评估。

### 4. Expression 评估

> "Expression guards are evaluated using the Godot Expression class."

这意味着 `delay_in_seconds` 会被当作 GDScript 表达式解析。

### 5. 初始化时机问题

> "⚠️ Note: The initial state of a state chart will only be entered one frame after the state chart's _ready function ran."

> "This means that if you call send_event, set_expression_property or step in a _ready function things will most likely not work as expected."

**重要**：StateChart 的初始状态在 `_ready` 之后一帧才会进入！

### 6. C# 使用方式

```csharp
using GodotStateCharts;

var stateChartNode = GetNode("StateChart");
var stateChart = StateChart.Of(stateChartNode);
stateChart.SendEvent("some_event");
```

## 可能的问题

1. **delay_in_seconds 必须是有效的表达式**
   - 空字符串会导致错误
   - 必须是可以被 Expression.evaluate() 解析的字符串

2. **NodePath 的相对路径**
   - 文档中没有明确说明 NodePath 的格式
   - 需要查看实际的示例场景

3. **初始化时机**
   - StateChart 在 _ready 之后一帧才初始化
   - 可能需要使用 call_deferred

## 下一步

需要查看：
1. GodotStateCharts 的示例场景文件
2. transition.gd 的源代码
3. 实际工作的 .tscn 文件示例


## 重要发现：ItemEntity.tscn 的配置

从工作的 ItemEntity.tscn 文件中发现：

```
[node name="StateChart" type="Node" parent="."]
script = ExtResource("script_StateChart")

[node name="Root" type="Node" parent="StateChart"]
script = ExtResource("script_CompoundState")
initial_state = NodePath("Idle")

[node name="Idle" type="Node" parent="StateChart/Root"]
script = ExtResource("script_AtomicState")

[node name="ToDragging" type="Node" parent="StateChart/Root/Idle"]
script = ExtResource("script_Transition")
to = NodePath("../Dragging")
delay_in_seconds = "0.0"
event = &"drag_start"

[node name="Dragging" type="Node" parent="StateChart/Root"]
script = ExtResource("script_AtomicState")

[node name="ToIdle" type="Node" parent="StateChart/Root/Dragging"]
script = ExtResource("script_Transition")
to = NodePath("../Idle")
delay_in_seconds = "0.0"
event = &"drag_end"
```

**关键点**：
1. ✅ `to = NodePath("../Dragging")` - 相对路径是正确的
2. ✅ `delay_in_seconds = "0.0"` - 字符串格式是正确的
3. ✅ `event = &"drag_start"` - StringName 格式是正确的

**结论**：我们的 BackpackTest.tscn 配置应该和 ItemEntity.tscn 完全一样！

## 可能的问题

既然配置格式正确，那么问题可能是：
1. StateChart 节点的位置不对
2. StateChart 的初始化时机问题
3. 场景文件损坏或缓存问题
4. Godot 编辑器没有正确重新加载场景


## 最终诊断

对比 BackpackTest.tscn 和 ItemEntity.tscn 的 StateChart 配置：

### BackpackTest.tscn
```
[node name="ToDragging" type="Node" parent="...StateChart/Root/Idle"]
script = ExtResource("script_Transition")
to = NodePath("../Dragging")
delay_in_seconds = "0.0"
event = &"drag_start"
```

### ItemEntity.tscn
```
[node name="ToDragging" type="Node" parent="StateChart/Root/Idle"]
script = ExtResource("script_Transition")
to = NodePath("../Dragging")
delay_in_seconds = "0.0"
event = &"drag_start"
```

**结论**：配置完全一致！格式正确！

## 问题根源

错误信息：`The target state '../Dragging' of the transition from 'Idle' is not a state.`

但是场景文件中 Dragging 状态明确存在：
```
[node name="Dragging" type="Node" parent="...StateChart/Root"]
script = ExtResource("script_AtomicState")
```

**唯一可能的原因**：
1. **Godot 编辑器缓存问题** - 编辑器没有重新加载更新后的场景文件
2. **场景文件被锁定** - 文件系统或 Godot 进程锁定了文件
3. **Godot 需要完全重启** - 仅点击 Reload 可能不够

## 解决方案

1. **完全关闭 Godot 编辑器**
2. **删除 .godot/imported/ 缓存文件夹**（可选）
3. **重新启动 Godot**
4. **重新打开场景**
5. **运行测试**

或者：
1. **在 Godot 中关闭 BackpackTest.tscn 标签页**
2. **从文件系统中删除场景文件**
3. **重新生成场景**
4. **在 Godot 中重新打开场景**
