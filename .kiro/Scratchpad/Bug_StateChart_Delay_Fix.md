# StateChart Transition Delay Bug 修复

## 问题描述

运行场景时出现大量错误：
```
expression_util.gd:8 @ evaluate_expression(): (delay of /root/BackpackTest/.../ToDragging) 
Expression parse error. Tried to parse expression: '' but got error: 'Expected expression.'

atomic_state.gd:11 @ _handle_transition(): 
The target state '../Dragging' of the transition from 'Idle' is not a state.
```

## 根本原因

`StateChartModule.add_transition()` 方法在生成 transition 节点时，总是设置 `delay_in_seconds` 属性：

```python
properties = {
    "script": f'ExtResource("{res_id}")',
    "to": f'NodePath("{relative_path}")',
    "delay_in_seconds": f'"{delay}"'  # ← 问题：即使 delay=0 也会生成 "0.0"
}
```

这导致生成的场景文件中：
```
[node name="ToDragging" ...]
to = NodePath("../Dragging")
delay_in_seconds = ""0.0""  # ← 双重转义，Godot 无法解析
event = &"drag_start"
```

Godot StateChart 插件尝试解析 `delay_in_seconds` 作为表达式，但遇到空字符串或格式错误的值时失败。

## 解决方案

**只在 delay > 0 时才设置 `delay_in_seconds` 属性**：

```python
properties = {
    "script": f'ExtResource("{res_id}")',
    "to": f'NodePath("{relative_path}")'
}

# Only add delay if it's greater than 0
if delay > 0:
    properties["delay_in_seconds"] = f'"{delay}"'

if event:
    properties["event"] = f'&"{event}"'
```

## 修复后的场景文件

```
[node name="ToDragging" type="Node" parent=".../Idle"]
script = ExtResource("script_Transition")
to = NodePath("../Dragging")
event = &"drag_start"
# delay_in_seconds 属性不再存在（当 delay=0 时）
```

## 影响范围

- **文件**: `KiroWorkingSpace/builder/modules/statechart.py`
- **方法**: `StateChartModule.add_transition()`
- **影响**: 所有使用 StateChart 的场景生成器

## 验证方法

1. 重新生成场景
2. 检查场景文件中不再有 `delay_in_seconds = ""`
3. 运行场景，确认没有 expression parse error
4. 测试状态转换（drag_start / drag_end）正常工作

## 关键教训

- Godot 的可选属性应该完全省略，而不是设置为空值或默认值
- StateChart 插件会尝试将 `delay_in_seconds` 作为 GDScript 表达式解析
- Python f-string 的引号转义需要特别注意，避免双重转义
