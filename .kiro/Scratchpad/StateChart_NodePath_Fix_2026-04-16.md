# StateChart Transition NodePath Bug - FIXED

**Date**: 2026-04-16  
**Status**: ✅ RESOLVED  
**Credit**: Godot Sensei (Godot Architect)

---

## Problem Summary

StateChart transitions were failing with error:
```
The target state '../Dragging' of the transition from 'Idle' is not a state
```

This prevented drag-and-drop functionality from working.

---

## Root Cause

The Python scene generator (`statechart.py`) was calculating NodePath from the **parent state** (Idle) instead of from the **Transition node itself** (ToDragging).

### Tree Structure
```
Root (StateChart/Root)
├── Idle (State)
│   └── ToDragging (Transition)  <-- NodePath calculated FROM here
└── Dragging (State)              <-- NodePath points TO here
```

### Wrong Calculation
- From `Idle` to `Dragging` = `../Dragging` ❌
- This goes: Idle → (up to Root) → Dragging
- But the NodePath is stored on `ToDragging`, not `Idle`!

### Correct Calculation
- From `ToDragging` to `Dragging` = `../../Dragging` ✅
- This goes: ToDragging → (up to Idle) → (up to Root) → Dragging

---

## Secondary Issue

`delay_in_seconds` was being output as string `"0.0"` instead of raw float `0.0`.

In Godot .tscn syntax:
- ❌ `delay_in_seconds = "0.0"` (string - WRONG)
- ✅ `delay_in_seconds = 0.0` (float - CORRECT)

---

## Fix Implementation

Modified `add_transition()` method in `KiroWorkingSpace/builder/modules/statechart.py`:

### Before (Broken)
```python
def add_transition(self, name: str, from_state: str, to_state: str,
                  event: str = "", delay: float = 0.0) -> TscnNode:
    # ... node creation ...
    
    # WRONG: Calculates path from parent state
    from_node = self.builder.get_node(from_state)
    to_node = self.builder.get_node(to_state)
    relative_path = from_node.get_relative_path_to(to_node)
    
    # WRONG: Outputs delay as string
    transition_node.set_property("delay_in_seconds", f'"{delay}"')
```

### After (Fixed)
```python
def add_transition(self, name: str, from_state: str, to_state: str,
                  event: str = "", delay: float = 0.0) -> TscnNode:
    # ... validation ...
    
    # CORRECT: Create transition node first
    transition_node = self.builder.add_node(name, "Node", parent=from_state,
        script=f'ExtResource("{res_id}")'
    )
    
    # CORRECT: Calculate path FROM transition node TO target
    relative_path = transition_node.get_relative_path_to(to_node)
    
    # CORRECT: Set properties
    transition_node.set_property("to", f'NodePath("{relative_path}")')
    transition_node.set_property("delay_in_seconds", delay)  # Raw float
```

---

## Verification

Generated scene `3d-practice/Scenes/BackpackTest.tscn` now contains:

```gdscript
[node name="ToDragging" type="Node" parent="..."]
script = ExtResource("script_Transition")
to = NodePath("../../Dragging")      # ✅ Correct path
delay_in_seconds = 0.0               # ✅ Raw float
event = &"drag_start"
```

---

## Prevention Guidelines

1. **Always calculate NodePath from the node that holds the property**, not from its parent
2. **Create the node first**, then calculate relative paths
3. **Never quote numeric values** in .tscn files (floats, ints, bools)
4. **Test StateChart transitions** immediately after scene generation

---

## Related Files

- `KiroWorkingSpace/builder/modules/statechart.py` (fixed)
- `KiroWorkingSpace/.kiro/scripts/temp/generate_backpack_test_v2.py` (scene generator)
- `3d-practice/Scenes/BackpackTest.tscn` (regenerated with fix)
- `3d-practice/addons/A1TetrisBackpack/Interaction/DraggableItemComponent.cs`
- `3d-practice/addons/A1TetrisBackpack/Interaction/FollowMouseUIComponent.cs`
