# Godot 4 GuiInput Event Not Firing - Research Findings

## Date: 2026-04-15
## Issue: TestItem Control node not receiving mouse input despite proper size and MouseFilter=Stop

---

## Key Findings from Web Research

### 1. Control Node Tree Order Matters (CRITICAL)
**Source:** https://forum.godotengine.org/t/cant-receive-mouse-input-from-control-node/37636

> "The tree order of control nodes matters when receiving signals: My ColorRect was at the top of the tree and some other lower placed VBoxContainer (mouse_filter was on Stop) stopped the signal before it could reach the ColorRect"

**Implication:** Parent Control nodes (ItemsContainer, BackpackPanel) might be blocking input to TestItem even if TestItem is properly configured.

**Solution:** Set parent containers' mouse_filter to IGNORE (not STOP) so they don't intercept mouse events.

---

### 2. GUI Input Event Propagation Rules
**Source:** https://docs.godotengine.org/en/stable/tutorials/inputs/inputevent.html

Key points from official documentation:
- "GUI mouse events also travel up the scene tree, subject to the Control.mouse_filter restrictions"
- "Since these events target specific Controls, only direct ancestors of the targeted Control node receive the event"
- Control._gui_input() is called when mouse is inside the control's bounding box
- Events are filtered by z-order, mouse_filter, focus, and bounding box

**Event Processing Order:**
1. Node._input() - called first on all nodes
2. Control._gui_input() - called on GUI controls that pass mouse_filter checks
3. Node._shortcut_input() - for keyboard/joypad shortcuts
4. Node._unhandled_input() - for gameplay input

---

### 3. C# GuiInput Event Subscription vs Method Override
**Source:** Multiple forum posts

**CRITICAL ISSUE:** In our current code, we're doing:
```csharp
ClickableArea.GuiInput += HandleGuiInput;  // Event subscription
```

**Problem:** This approach might not work reliably in C#. The proper way is to:
1. Attach script directly to the Control node
2. Override the _GuiInput() method

**Correct Pattern (GDScript equivalent):**
```gdscript
func _gui_input(event: InputEvent) -> void:
    if event is InputEventMouseButton:
        # Handle input
```

**C# Equivalent:**
```csharp
public override void _GuiInput(InputEvent @event)
{
    if (@event is InputEventMouseButton mouseEvent)
    {
        // Handle input
    }
}
```

---

### 4. Mouse Filter Settings
**Source:** https://github.com/godotengine/godot/issues/62599

Three mouse_filter modes:
- **STOP:** Captures mouse input and doesn't allow pass-through (blocks children)
- **PASS:** Captures mouse input but passes it on if not accepted
- **IGNORE:** Ignores mouse input completely and passes to children

**For our case:**
- TestItem should have mouse_filter = STOP (to receive input)
- ItemsContainer should have mouse_filter = IGNORE (to not block TestItem)
- BackpackPanel should have mouse_filter = IGNORE (to not block TestItem)

---

## Current Architecture Problem

Our scene tree:
```
BackpackPanel (Control) - mouse_filter = ?
└── ItemsContainer (Control) - mouse_filter = ?
    └── TestItem (Control) - mouse_filter = Stop ✓
        ├── DraggableItemComponent (Node) - subscribes to GuiInput event ✗
        └── ClickableBackground (ColorRect)
```

**Issues:**
1. DraggableItemComponent is a separate Node trying to subscribe to parent Control's GuiInput event
2. Parent containers (ItemsContainer, BackpackPanel) might have mouse_filter = Stop, blocking input
3. Event subscription approach might not work in C# - should override _GuiInput() instead

---

## Recommended Solutions (in order of preference)

### Solution 1: Fix Parent Mouse Filters (EASIEST)
Set ItemsContainer and BackpackPanel mouse_filter to IGNORE:
```python
scene.add_node("ItemsContainer", "Control", parent="BackpackPanel",
    layout_mode=2,
    mouse_filter=2  # IGNORE
)
```

### Solution 2: Attach Script Directly to TestItem
Instead of separate DraggableItemComponent, attach script directly to TestItem and override _GuiInput():
```csharp
public partial class TestItem : Control
{
    public override void _GuiInput(InputEvent @event)
    {
        if (@event is InputEventMouseButton mouseEvent)
        {
            GD.Print($"Mouse event: {mouseEvent.ButtonIndex}, Pressed={mouseEvent.Pressed}");
            // Handle drag logic
        }
    }
}
```

### Solution 3: Use _Input() Instead of _GuiInput()
_Input() is called on all nodes regardless of mouse position:
```csharp
public override void _Input(InputEvent @event)
{
    if (@event is InputEventMouseButton mouseEvent)
    {
        // Check if mouse is inside TestItem bounds
        if (GetGlobalRect().HasPoint(GetGlobalMousePosition()))
        {
            // Handle drag logic
        }
    }
}
```

---

## Next Steps

1. Check ItemsContainer and BackpackPanel mouse_filter settings in scene file
2. Try Solution 1 first (set parent mouse_filters to IGNORE)
3. If that doesn't work, try Solution 2 (override _GuiInput directly on TestItem)
4. Add debug prints to verify which nodes are receiving input

---

## References
- https://forum.godotengine.org/t/cant-receive-mouse-input-from-control-node/37636
- https://docs.godotengine.org/en/stable/tutorials/inputs/inputevent.html
- https://forum.godotengine.org/t/on-gui-input-dont-working/120362
