# Bug Report for Gemini

## Environment
- Engine: Godot 4.6.1 stable mono
- Language: C#
- OS: Windows

## Problem
Control node GuiInput event subscription in C# does not fire despite proper size (64x64), MouseFilter=Stop, and parent containers set to MouseFilter=Ignore.

## What I Tried

### Attempt 1: Fixed TestItem Size (Zero Size Bug)
**Methodology:** 
- Identified that TestItem had zero size (offset_right = offset_left = 128, offset_bottom = offset_top = 128)
- Modified generator to set proper offsets: offset_right=192, offset_bottom=192
- This gave TestItem a proper 64x64 size

**Result:** 
- TestItem now has correct size: `ClickableArea 尺寸 = (64, 64), 位置 = (128, 128)`
- MouseFilter confirmed as Stop
- But GuiInput event still never fires - no debug prints appear when clicking

### Attempt 2: Added Debug Logging
**Methodology:**
- Added debug prints in HandleGuiInput() to detect ANY input events
- Added debug prints showing TestItem size and MouseFilter at initialization
- Verified all components initialize successfully

**Result:**
- Initialization logs show everything correct:
  - `DraggableItemComponent: 自动使用父节点 'TestItem' 作为 ClickableArea`
  - `DraggableItemComponent: ClickableArea 尺寸 = (64, 64), 位置 = (128, 128)`
  - `DraggableItemComponent: ClickableArea.MouseFilter = Stop`
  - `DraggableItemComponent: 已订阅 TestItem 的 GuiInput 事件`
- But when clicking on TestItem, HandleGuiInput() is NEVER called - no debug prints appear

### Attempt 3: Fixed Parent Container Mouse Filters
**Methodology:**
- Research revealed parent Control nodes with MouseFilter=Stop block input to children
- Set BackpackPanel.mouse_filter = 2 (IGNORE)
- Set ItemsContainer.mouse_filter = 2 (IGNORE)
- Regenerated scene and tested

**Result:**
- Scene regenerated successfully with parent containers set to IGNORE
- All components still initialize correctly
- But clicking on TestItem STILL produces no debug output - HandleGuiInput() never called

## Current Code

### DraggableItemComponent.cs (Event Subscription Approach)
```csharp
public partial class DraggableItemComponent : Node
{
    [Export] public Control ClickableArea { get; set; }
    [Export] public Node StateChart { get; set; }
    
    public override void _Ready()
    {
        OnDragStartedAsObservable = new Subject<Unit>();
        OnDragEndedAsObservable = new Subject<Unit>();
        OnRotateRequestedAsObservable = new Subject<Unit>();
        
        CallDeferred(MethodName.InitializeComponent);
    }
    
    private void InitializeComponent()
    {
        // Auto-find ClickableArea if not set
        if (ClickableArea == null)
        {
            ClickableArea = GetParent() as Control;
            if (ClickableArea != null)
            {
                GD.Print($"DraggableItemComponent: 自动使用父节点 '{ClickableArea.Name}' 作为 ClickableArea");
                GD.Print($"DraggableItemComponent: ClickableArea 尺寸 = {ClickableArea.Size}, 位置 = {ClickableArea.Position}");
                GD.Print($"DraggableItemComponent: ClickableArea.MouseFilter = {ClickableArea.MouseFilter}");
            }
        }
        
        // Subscribe to GUI input event
        if (ClickableArea != null)
        {
            ClickableArea.GuiInput += HandleGuiInput;  // ← THIS SUBSCRIPTION DOESN'T WORK
            GD.Print($"DraggableItemComponent: 已订阅 {ClickableArea.Name} 的 GuiInput 事件");
        }
        
        // Auto-find StateChart
        if (StateChart == null)
        {
            StateChart = GetParent()?.GetNodeOrNull("StateChart");
            if (StateChart != null)
            {
                GD.Print("DraggableItemComponent: 自动找到 StateChart 节点");
            }
        }
    }
    
    private void HandleGuiInput(InputEvent @event)
    {
        // THIS METHOD IS NEVER CALLED!
        GD.Print($"DraggableItemComponent: 接收到输入事件 {@event.GetType().Name}");
        
        if (@event is not InputEventMouseButton mouseEvent)
            return;
        
        GD.Print($"DraggableItemComponent: 鼠标按键事件 - Button={mouseEvent.ButtonIndex}, Pressed={mouseEvent.Pressed}");
        
        if (mouseEvent.ButtonIndex == MouseButton.Left && mouseEvent.Pressed)
        {
            HandleDragStart();
        }
        else if (mouseEvent.ButtonIndex == MouseButton.Left && !mouseEvent.Pressed)
        {
            HandleDragEnd();
        }
        else if (mouseEvent.ButtonIndex == MouseButton.Right && mouseEvent.Pressed)
        {
            HandleRotateRequest();
        }
    }
}
```

### Scene Structure (BackpackTest.tscn)
```
BackpackPanel (Control) - mouse_filter=2 (IGNORE) ✓
└── ItemsContainer (Control) - mouse_filter=2 (IGNORE) ✓
    └── TestItem (Control) - mouse_filter=0 (STOP), size=64x64 ✓
        ├── ClickableBackground (ColorRect) - anchored to fill parent
        ├── StateChart (Node)
        ├── DraggableItemComponent (Node) ← Subscribes to parent's GuiInput
        └── [other components...]
```

## Research Findings

From Godot documentation and forums:
1. **Control tree order matters** - parent Controls with MouseFilter=Stop block children
2. **GuiInput propagation** - Events target specific Controls based on mouse position and bounding box
3. **C# event subscription concern** - Some forum posts suggest overriding `_GuiInput()` method instead of subscribing to GuiInput event

## Suspected Issues

1. **C# Event Subscription Pattern:** The pattern `ClickableArea.GuiInput += HandleGuiInput` might not work in C# Godot. GDScript uses `func _gui_input(event)` override instead.

2. **Component Architecture:** DraggableItemComponent is a separate Node trying to subscribe to its parent Control's GuiInput event. This might not be supported.

3. **Possible Solutions to Test:**
   - Override `_GuiInput()` method directly on TestItem Control instead of event subscription
   - Use `_Input()` method with manual bounds checking instead of GuiInput
   - Attach script directly to TestItem Control rather than separate component

## Question for Gemini

Why does `ClickableArea.GuiInput += HandleGuiInput` event subscription in C# never trigger the HandleGuiInput method, even though:
- ClickableArea is a valid Control with proper size (64x64)
- MouseFilter is set to Stop
- Parent containers have MouseFilter=Ignore
- The subscription appears successful (no errors)
- All initialization logs confirm correct setup

Is event subscription to GuiInput not supported in C# Godot? Should we override `_GuiInput()` method instead?
