# Component Design Log - 2026-04-23

## Refactor: BackpackGridUIComponent - Visual Language Unification

### Date: 2026-04-23
### Status: ✅ Completed

---

## Design Decision 1: Replace Primitive _Draw() with GridCellUI Factory

### Problem
- BackpackGridUIComponent used primitive `_Draw()` API to render grid lines
- Visual style inconsistent: background = white lines, items = transparent body + glowing border
- Maintenance burden: two different rendering systems

### Solution
- **Deleted**: `_Draw()` method, `DrawDebugLines` boolean, `GridColor` property
- **Added**: `GenerateBackgroundGrid()` factory method
- **Architecture Shift**: From "Renderer" to "Factory"

### Implementation Details

**New State:**
```csharp
private readonly List<GridCellUI> _backgroundCells = new();
private Control _gridContainer; // Must have MouseFilter = Ignore
```

**New Export:**
```csharp
[Export] public NodePath GridContainerPath { get; set; } = "%GridContainer";
```

**Factory Method:**
```csharp
private void GenerateBackgroundGrid()
{
    // 1. Clear old grid
    foreach (var cell in _backgroundCells) cell.QueueFree();
    _backgroundCells.Clear();
    
    // 2. Nested loop: for x in [0, Width), for y in [0, Height)
    for (int y = 0; y < BackpackGridComp.Height; y++)
    {
        for (int x = 0; x < BackpackGridComp.Width; x++)
        {
            var gridCellUI = new GridCellUI
            {
                Size = CellSize,
                Position = new Vector2(x * CellSize.X, y * CellSize.Y),
                Name = $"BackgroundCell_{x}_{y}",
                MouseFilter = MouseFilterEnum.Pass // Future: hover effects
            };
            
            // CRITICAL: AddChild() before SetState()
            _gridContainer.AddChild(gridCellUI);
            _backgroundCells.Add(gridCellUI);
            
            gridCellUI.SetState(GridCellUI.CellState.Normal);
        }
    }
}
```

### Benefits
1. **Visual Consistency**: Background and items now use identical GridCellUI rendering
2. **Maintainability**: Single source of truth for grid cell appearance
3. **Extensibility**: Background cells can now respond to hover events (future feature)
4. **Architecture Clarity**: BackpackGridUIComponent is now clearly a "Factory + Coordinate Converter"

### MouseFilter Architecture
```
BackpackPanel (BackpackGridUIComponent)
├── GridContainer (MouseFilter = Ignore) ← Transparent to mouse
│   ├── GridCellUI (0,0) (MouseFilter = Pass) ← Can receive hover
│   ├── GridCellUI (0,1) (MouseFilter = Pass)
│   └── ...
├── Item1 (TetrisDraggableItem) ← Can be clicked through GridContainer
└── Item2
```

---

## Design Decision 2: ItemCellGroupController Hover Effect

### Problem
- Items had no visual feedback on mouse hover
- User couldn't tell which item was "hot" (ready to interact)

### Solution
- Subscribe to `GridCellUI.MouseEntered` and `MouseExited` signals
- Trigger `SetGroupState(CellState.Hover)` on enter
- Trigger `ResetGroupState()` on exit

### Implementation
```csharp
// In RebuildCells(), after AddChild():
gridCellUI.MouseEntered += () => SetGroupState(GridCellUI.CellState.Hover);
gridCellUI.MouseExited += () => ResetGroupState();
```

### Effect
- Entire item (all GridCellUI cells) lights up white/glowing when mouse hovers
- Provides clear visual feedback for interaction readiness

---

## Design Decision 3: BackpackInteractionController Remains Necessary

### Clarification
Even though pure visual drag-and-drop works without BackpackInteractionController, it remains **architecturally necessary** for:

1. **Logical Drop Validation**: Checking if placement is valid (no overlap, within bounds)
2. **Overlap Prevention**: Ensuring items don't occupy the same grid cells
3. **State Management**: Tracking original positions for bounce-back
4. **MVC Separation**: Keeping business logic separate from visual components

### Rationale
- Visual drag = UI layer (FollowMouseUIComponent)
- Logical validation = Controller layer (BackpackInteractionController)
- Data storage = Model layer (BackpackGridComponent)

Removing the controller would violate MVC architecture and force business logic into UI components.

---

## Files Modified

1. **BackpackGridUIComponent.cs**
   - Deleted: `_Draw()`, `DrawDebugLines`, `GridColor`, `DrawGridLines()`, `ToggleDebugLines()`
   - Added: `_gridContainer`, `_backgroundCells`, `GridContainerPath`, `GenerateBackgroundGrid()`
   - Modified: `InitializeComponent()`, `RefreshGrid()`

2. **ItemCellGroupController.cs**
   - Modified: `RebuildCells()` - added MouseEntered/MouseExited subscriptions

3. **Scratchpad/ComponentDesign_20260423.md**
   - Created: This design log

---

## User Action Required

### 1. Scene Configuration
Open the Backpack Background Scene and:
1. Create a `Control` node named `GridContainer`
2. Set `GridContainer.MouseFilter = Ignore` (value 2)
3. Make it a child of `BackpackPanel` (BackpackGridUIComponent)
4. Assign `GridContainer` to `BackpackGridUIComponent.GridContainerPath` in inspector

### 2. Sync Filter Check
Ensure the following directories are tracked in Cloud Sync filters:
- `3d-practice/addons/A1TetrisBackpack/UI/` (contains GridCellUI.cs)
- `3d-practice/addons/A1TetrisBackpack/Core/` (contains BackpackGridUIComponent.cs)
- `3d-practice/addons/A1TetrisBackpack/Items/` (contains ItemCellGroupController.cs)

If any files are missing from AI context, adjust sync filters to include them.

---

## Architecture Principles Applied

1. **Visual Language Unification**: All grid cells (background + items) use GridCellUI
2. **Factory Pattern**: BackpackGridUIComponent generates static background grid
3. **MouseFilter Layering**: GridContainer = Ignore, GridCellUI = Pass, Items = Ignore
4. **MVC Separation**: Controller remains for business logic, UI handles visuals only
5. **Godot Lifecycle**: AddChild() before any subscriptions or state changes

---

## Performance Notes

- Background grid is **static** (generated once in _Ready)
- No per-frame _Draw() calls (performance improvement)
- GridCellUI uses StyleBoxFlat (GPU-accelerated rendering)
- Total background cells: Width × Height (e.g., 10×10 = 100 cells)

---

## Future Enhancements

1. **Background Hover Effects**: Subscribe to `OnCellHoverAsObservable` for background cells
2. **Grid Resize**: Add `RegenerateGrid()` method for dynamic grid size changes
3. **Cell Pooling**: Reuse GridCellUI instances instead of QueueFree() for better performance
4. **Custom Cell Styles**: Allow per-cell style overrides (e.g., special cells, locked cells)

---

**Logged by**: Kiro AI Assistant  
**Reviewed by**: User  
**Architecture Compliance**: ✅ Passed (DesignPatterns.md, ProjectRules.md)


---

## Bug Fix: Mouse Slipping Off Top-Left Edge During Drag (2026-04-23 Final)

### Problem
When dragging an item, if the mouse cursor is at the exact top-left corner (0,0) of the GridCellUI, moving the mouse slightly left or up causes it to exit the cell bounds, triggering MouseExited and breaking the hover effect.

### Failed Approach (REVERTED)
- ❌ Modified `ItemCellGroupController` to offset GridCellUI Position by `+ new Vector2(2f, 2f)`
- ❌ This broke pixel-perfect grid alignment with the backpack background
- ❌ Architectural violation: ItemCellGroupController should not compensate for drag behavior

### Root Cause
The issue only occurs **during dragging** ("拿的时候"). The mouse cursor sits exactly at the item's top-left edge, making it easy to slip off.

### Correct Solution
**Offset the item relative to the mouse during drag**, not the GridCellUI relative to the grid.

**Implementation:**
1. `FollowMouseUIComponent` already has `GrabOffset` property (default `Vector2.Zero`)
2. User must set `GrabOffset = (-15, -15)` in Inspector
3. This shifts the item UP and LEFT relative to the mouse
4. Result: Mouse cursor sits 15px DOWN and RIGHT from the top-left corner, safely inside the cell

### User Action Required
1. Open `TSItem.tscn` (or ItemEntity scene) in Godot Editor
2. Navigate to: `StateChart → Root → Dragging → FollowMouseUIComponent`
3. In Inspector, set:
   - `Grab Offset X: -15`
   - `Grab Offset Y: -15`
4. Save scene

### Code Verification
- ✅ `ItemCellGroupController.cs`: Position is clean, no offset garbage
- ✅ `FollowMouseUIComponent.cs`: GrabOffset property exists and is used in `_Process()`

### Architecture Principle
**Separation of Concerns:**
- `ItemCellGroupController`: Manages grid-aligned cell generation (static positioning)
- `FollowMouseUIComponent`: Manages drag behavior (dynamic positioning with offset)

**Never mix grid logic with drag logic.**

---

**Bug Fixed**: 2026-04-23 Final  
**Correct Approach**: GrabOffset in FollowMouseUIComponent  
**Reverted**: Naive Position offset in ItemCellGroupController


---

## Refactor: BackpackGridUIComponent Auto-Generation (2026-04-23 Final)

### Goal
Automate background grid generation like Unreal PreConstruct. No manual node creation required.

### Implementation

**Step 1: Auto-Create BackgroundCanvas in _EnterTree()**
```csharp
public override void _EnterTree()
{
    _backgroundCanvas = GetNodeOrNull<Control>("BackgroundCanvas");
    if (_backgroundCanvas == null)
    {
        _backgroundCanvas = new Control
        {
            Name = "BackgroundCanvas",
            MouseFilter = MouseFilterEnum.Ignore
        };
        AddChild(_backgroundCanvas);
    }
    else
    {
        _backgroundCanvas.MouseFilter = MouseFilterEnum.Ignore;
    }
}
```

**Step 2: Generate GridCellUI in _Ready()**
```csharp
private void GenerateBackgroundGrid()
{
    for (int y = 0; y < BackpackGridComp.Height; y++)
    {
        for (int x = 0; x < BackpackGridComp.Width; x++)
        {
            var gridCellUI = new GridCellUI
            {
                Size = CellSize,
                Position = new Vector2(x * CellSize.X, y * CellSize.Y),
                Name = $"BackgroundCell_{x}_{y}",
                MouseFilter = MouseFilterEnum.Pass
            };
            
            _backgroundCanvas.AddChild(gridCellUI);
            _backgroundCells.Add(gridCellUI);
            
            gridCellUI.SetState(GridCellUI.CellState.Normal);
        }
    }
}
```

### Changes
- ✅ Removed `GridContainerPath` Export property
- ✅ Removed `_gridContainer` field
- ✅ Added `_backgroundCanvas` auto-creation in `_EnterTree()`
- ✅ Background grid now appears automatically upon entering scene tree

### Whole-Item Hover
Already implemented in `ItemCellGroupController.cs`:
```csharp
gridCellUI.MouseEntered += () => SetGroupState(GridCellUI.CellState.Hover);
gridCellUI.MouseExited += () => ResetGroupState();
```

Mousing over any cell triggers `SetGroupState(Hover)` for ALL cells in the item.

### Compilation
✅ Build succeeded with 7 warning(s) in 3.9s

---

**Refactor Complete**: 2026-04-23 Final  
**Auto-Generation**: BackgroundCanvas created in _EnterTree  
**Unified Hover**: Whole item glows white on mouse enter
