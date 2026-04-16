# Bug Report for Gemini

## Environment
- Engine: Godot 4.6.1 stable mono
- Language: C#
- OS: Windows
- Plugin: GodotStateCharts (godot_state_charts addon)

## Problem
StateChart transition fails with error `The target state '../Dragging' of the transition from 'Idle' is not a state`, despite the Dragging state existing in the scene file and the configuration being identical to a working scene.

## Goal
Achieve drag-and-drop functionality where clicking and dragging a UI item (TestItem) makes it follow the mouse cursor.

## What I Tried

### Attempt 1: Fixed delay_in_seconds Double-Quote Issue
**Methodology:**
- Identified that `delay_in_seconds = ""0.0""` (double quotes) was being generated
- Modified `StateChartModule.add_transition()` to use `str(delay)` instead of `f'"{delay}"'`
- Regenerated scene file

**Result:**
- Scene file now has `delay_in_seconds = "0.0"` (single quotes) ✅
- But error persists: `The target state '../Dragging' of the transition from 'Idle' is not a state` ❌

### Attempt 2: Removed delay_in_seconds Property
**Methodology:**
- Tried completely omitting `delay_in_seconds` when delay=0
- Regenerated scene

**Result:**
- StateChart plugin requires `delay_in_seconds` to be present (cannot be empty)
- Reverted this change

### Attempt 3: Verified Scene Configuration Against Working Example
**Methodology:**
- Compared BackpackTest.tscn with working ItemEntity.tscn
- Verified all properties match exactly:
  - `to = NodePath("../Dragging")` ✅
  - `delay_in_seconds = "0.0"` ✅
  - `event = &"drag_start"` ✅
  - Dragging state node exists ✅

**Result:**
- Configuration is identical to working scene
- But error still occurs ❌

## Current Code

### BackpackTest.tscn (Generated Scene - Relevant Section)
```
[node name="StateChart" type="Node" parent="ScreenMargin/MainVBox/BackpackPanel/ItemsContainer/TestItem"]
script = ExtResource("script_StateChart")

[node name="Root" type="Node" parent="ScreenMargin/MainVBox/BackpackPanel/ItemsContainer/TestItem/StateChart"]
script = ExtResource("script_CompoundState")
initial_state = NodePath("Idle")

[node name="Idle" type="Node" parent="ScreenMargin/MainVBox/BackpackPanel/ItemsContainer/TestItem/StateChart/Root"]
script = ExtResource("script_AtomicState")

[node name="ToDragging" type="Node" parent="ScreenMargin/MainVBox/BackpackPanel/ItemsContainer/TestItem/StateChart/Root/Idle"]
script = ExtResource("script_Transition")
to = NodePath("../Dragging")
delay_in_seconds = "0.0"
event = &"drag_start"

[node name="Dragging" type="Node" parent="ScreenMargin/MainVBox/BackpackPanel/ItemsContainer/TestItem/StateChart/Root"]
script = ExtResource("script_AtomicState")

[node name="ToIdle" type="Node" parent="ScreenMargin/MainVBox/BackpackPanel/ItemsContainer/TestItem/StateChart/Root/Dragging"]
script = ExtResource("script_Transition")
to = NodePath("../Idle")
delay_in_seconds = "0.0"
event = &"drag_end"

[node name="FollowMouseUIComponent" type="Node" parent="ScreenMargin/MainVBox/BackpackPanel/ItemsContainer/TestItem/StateChart/Root/Dragging"]
script = ExtResource("5_res")
```

### ItemEntity.tscn (Working Scene - For Comparison)
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

### DraggableItemComponent.cs (Event Sender)
```csharp
private void HandleDragStart()
{
    // 【R3 响应式】通知订阅者
    OnDragStartedAsObservable.OnNext(Unit.Default);
    
    // 【StateChart】发送状态机事件
    if (StateChart != null)
    {
        StateChart.Call("send_event", DragStartEventName);
        GD.Print($"DraggableItemComponent: 发送状态事件 '{DragStartEventName}'");
    }
    
    GD.Print("DraggableItemComponent: 拖拽开始");
}
```

## Error Log
```
DraggableItemComponent: 发送状态事件 'drag_start'
DraggableItemComponent: 拖拽开始
atomic_state.gd:11 @ _handle_transition(): The target state '../Dragging' of the transition from 'Idle' is not a state.
```

## Key Observations

### Differences Between Working and Failing Scenes

1. **Scene Hierarchy Depth:**
   - ItemEntity: `StateChart` is direct child of root node
   - BackpackTest: `StateChart` is deeply nested: `ScreenMargin/MainVBox/BackpackPanel/ItemsContainer/TestItem/StateChart`

2. **Scene Type:**
   - ItemEntity: Standalone scene file (can be instanced)
   - BackpackTest: Complex UI scene with TestItem as a sub-component

3. **Initialization Context:**
   - ItemEntity: Simple, flat structure
   - BackpackTest: Complex UI with multiple containers and components

### What Works
- ✅ DraggableItemComponent successfully sends `drag_start` event
- ✅ StateChart receives the event (error occurs during transition handling)
- ✅ Scene file configuration is syntactically correct
- ✅ All node paths and properties match working example

### What Fails
- ❌ StateChart cannot find `../Dragging` state at runtime
- ❌ Transition never executes
- ❌ Dragging state never activates
- ❌ FollowMouseUIComponent never starts (depends on Dragging state)

## Hypotheses

### Hypothesis 1: Node Initialization Order
The deeply nested StateChart might initialize before its child states (Idle, Dragging) are fully registered, causing the transition to fail when it tries to resolve `NodePath("../Dragging")`.

### Hypothesis 2: NodePath Resolution in Complex Hierarchies
The `../Dragging` relative path might not resolve correctly when the StateChart is deeply nested in a complex UI hierarchy.

### Hypothesis 3: GodotStateCharts Plugin Limitation
The plugin might have issues with StateCharts that are not direct children of the root node or are embedded in complex UI structures.

### Hypothesis 4: Scene Loading/Caching Issue
Despite restarting Godot, there might be a persistent cache or scene loading issue specific to this scene structure.

## Questions for Gemini

1. **Is there a known issue with GodotStateCharts when the StateChart node is deeply nested in a UI hierarchy?**

2. **Does the NodePath resolution `../Dragging` work differently depending on the parent node's position in the scene tree?**

3. **Should we use absolute NodePaths instead of relative paths for deeply nested StateCharts?**

4. **Is there a specific initialization order requirement for StateChart child nodes that we're violating?**

5. **Could the issue be related to Control nodes vs regular Nodes in the hierarchy?**

6. **Should we extract TestItem into a separate scene file (like ItemEntity) instead of embedding it in BackpackTest?**

## Additional Context

### Scene Generation
The scene is generated programmatically using a Python TscnBuilder. The StateChart structure is created using a StateChartModule that wraps the builder API.

### Research Conducted
- ✅ Read GodotStateCharts official documentation
- ✅ Compared with working example scene
- ✅ Verified all configuration properties
- ✅ Tested with Godot restart and cache clearing
- ✅ Confirmed event is being sent correctly

### Files for Reference
- Scene Generator: `KiroWorkingSpace/.kiro/scripts/temp/generate_backpack_test_v2.py`
- StateChart Module: `KiroWorkingSpace/builder/modules/statechart.py`
- Component: `3d-practice/addons/A1TetrisBackpack/Interaction/DraggableItemComponent.cs`
- Generated Scene: `3d-practice/Scenes/BackpackTest.tscn`
- Working Scene: `3d-practice/Scenes/ItemEntity.tscn`
