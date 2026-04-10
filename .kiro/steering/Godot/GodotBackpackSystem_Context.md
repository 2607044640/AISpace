---
inclusion: manual
---
  
<context>
Grid-based inventory system with drag-and-drop, rotation, StateChart integration, and Backpack Battles-style synergy system. Supports arbitrary item shapes (Tetris-like) with reactive event streams (R3), MVC architecture, and UI micro-interactions.
</context>

<architecture>

**Component Hierarchy:**
```
Data Layer:       BackpackGridComponent (1D array grid logic)
Resource Layer:   ItemDataResource, SynergyDataResource (static configs)
Shape Layer:      GridShapeComponent (runtime shape + rotation)
View Layer:       BackpackGridUIComponent (coordinate converter + visualizer)
Controller Layer: BackpackInteractionController (MVC controller, drag state management)
Input Layer:      DraggableItemComponent (GUI input → StateChart bridge)
Physics Layer:    FollowMouseUIComponent (mouse tracking via Power Switch)
Animation Layer:  UITweenInteractComponent (micro-interactions with logic/visual separation)
Synergy Layer:    SynergyComponent (Backpack Battles-style item synergies)
```

**File Paths:**
- Components: `3d-practice/B1Scripts/Components/`
- Controllers: `3d-practice/B1Scripts/Controllers/`
- Resources: `3d-practice/B1Scripts/Resources/`

**Scene Structure:**

```
BackpackPanel (BackpackGridUIComponent)
├── BackpackInteractionController
├── BackpackGridComponent (LogicGrid)
└── Items Container
    └── ItemEntity (Control) ← InteractionArea [Scale 永远是 1,1]
        ├── StateChart
        │   └── Root (CompoundState, initial="Idle")
        │       ├── Idle (AtomicState)
        │       │   └── Transition: event="drag_start" → Dragging
        │       └── Dragging (AtomicState)
        │           ├── FollowMouseUIComponent
        │           └── Transition: event="drag_end" → Idle
        ├── DraggableItemComponent
        ├── GridShapeComponent
        ├── SynergyComponent
        ├── UITweenInteractComponent
        └── VisualContainer (Control) ← VisualTarget [Scale 可以变化]
            ├── ItemIcon (TextureRect)
            └── StarContainer (Control)
                ├── Star1 (TextureRect) ← 灰色/亮色切换
                └── Star2 (TextureRect)
```

**Dependencies:**
- R3 (Cysharp) - Reactive streams
- GodotStateCharts - State machine plugin

</architecture>

<modifications>

**BackpackGridComponent:**
- 1D array storage: `ItemData[] _gridData` (size = Width * Height)
- Index formula: `index = y * Width + x`
- Methods: `CanPlaceItem()`, `TryPlaceItem()`, `RemoveItem()`, `GetItemAt()`, `ClearGrid()`
- R3 Subjects: `OnItemPlacedAsObservable`, `OnItemRemovedAsObservable`
- Dispose Subjects in `_ExitTree()`

**BackpackGridUIComponent:**
- Inherits `Control`, marked `[GlobalClass]`
- Export: `BackpackGridComponent LogicGrid`, `Vector2 CellSize` (default 64x64), `bool DrawDebugLines`, `Color GridColor`
- Auto-sizing: `CustomMinimumSize = Size = new Vector2(Width * CellSize.X, Height * CellSize.Y)`
- Coordinate conversion methods:
  - `GlobalToGridPosition(Vector2)`: `(globalPos - GlobalPosition) / CellSize` → FloorToInt → Clamp
  - `GridToLocalPosition(Vector2I)`: `gridPos * CellSize`
  - `GetCellCenterPosition(Vector2I)`: `GridToLocalPosition + CellSize / 2`
  - `LocalToGridPosition(Vector2)`: `localPos / CellSize` → FloorToInt → Clamp
- `_Draw()`: DrawLine for horizontal/vertical grid lines when `DrawDebugLines = true`
- Helper methods: `IsValidGridPosition()`, `GetCellRect()`, `GetShapeRect()`, `RefreshGrid()`, `SetCellSize()`, `ToggleDebugLines()`

**BackpackInteractionController:**
- Inherits `Node`, marked `[GlobalClass]`
- Export: `BackpackGridComponent LogicGrid`, `BackpackGridUIComponent ViewGrid`
- State management: `Dictionary<Node, ItemDragState>` (OriginalGlobalPos, OriginalGridPos, ShapeComponent, ItemControl)
- `RegisterItem(Node)`: Subscribe to DraggableItemComponent events using `.AddTo(itemEntity)`
- `HandleItemPickedUp()`: Record state + `LogicGrid.RemoveItem()` (防自我占用)
- `HandleItemDropped()`: 
  - Get mouse position: `ViewGrid.GetGlobalMousePosition()` (NOT `GetViewport().GetMousePosition()`)
  - Check range: `ViewGrid.GetGlobalRect().HasPoint(mousePos)`
  - Try place: `LogicGrid.TryPlaceItem()`
  - Success: `PerformSnapToGrid()` (吸附)
  - Failure: `PerformBounceBack()` (回弹)
- `HandleItemRotated()`: Call `ShapeComponent.Rotate90()`

**ItemDataResource:**
- Inherits `Resource`, marked `[GlobalClass]`
- Export properties: `ItemID`, `ItemName`, `Icon`, `BaseShape` (Godot.Collections.Array<Vector2I>)
- Default shape: `{ Vector2I.Zero }`
- Helper methods: `GetCellCount()`, `GetBoundingSize()`, `IsShapeValid()`

**GridShapeComponent:**
- Runtime shape: `Vector2I[] CurrentLocalCells`
- Rotation matrix (clockwise 90°): `(x, y) → (-y, x)`
- `Rotate90()` applies rotation + calls `NormalizeShape()`
- `NormalizeShape()` ensures min(X,Y) = 0
- R3 Subject: `OnShapeChangedAsObservable` (Subject<Unit>)
- Dispose Subject in `_ExitTree()`

**DraggableItemComponent:**
- Export: `Control ClickableArea`, `Node StateChart`
- Subscribe to `ClickableArea.GuiInput` event
- Mouse left press → `StateChart.Call("send_event", "drag_start")` + `OnDragStartedAsObservable.OnNext(Unit.Default)`
- Mouse left release → `StateChart.Call("send_event", "drag_end")` + `OnDragEndedAsObservable.OnNext(Unit.Default)`
- Mouse right press → `OnRotateRequestedAsObservable.OnNext(Unit.Default)` (no StateChart event)
- Unsubscribe `GuiInput` in `_ExitTree()`
- **Bug Fix:** Use `StateChart.Call()` directly, NOT `GetParent()?.Call()`

**FollowMouseUIComponent:**
- Export: `Control TargetUI`, `Vector2 GrabOffset`
- Call `AutoBindToParentState()` in `_Ready()` (Power Switch mode)
- Connect `state_entered` → `OnDragStateEntered()` (ZIndex +100)
- Connect `state_exited` → `OnDragStateExited()` (restore ZIndex)
- `_Process()`: `TargetUI.GlobalPosition = GetGlobalMousePosition() + GrabOffset`
- Save `_originalZIndex` for restoration

**UITweenInteractComponent:**
- Inherits `Node`, marked `[GlobalClass]`
- Export: `Control InteractionArea`, `Control VisualTarget`, `Vector2 HoverScale` (1.05), `Vector2 PressScale` (0.95), `float TweenDuration` (0.15)
- **Logic/Visual Separation**: InteractionArea (Scale=1,1, 坐标计算) + VisualTarget (可缩放, 视觉反馈)
- Three states: Normal(1,1) → Hover(1.05) → Press(0.95)
- `AnimateToScale()`: 
  - Kill current tween: `_currentTween?.Kill()`
  - Create tween: `GetTree().CreateTween()`
  - Configure: `SetEase(EaseType.Out)`, `SetTrans(TransitionType.Sine)`
  - Animate: `TweenProperty(VisualTarget, "scale", targetScale, TweenDuration)`
- `UpdatePivotOffset()`: `VisualTarget.PivotOffset = VisualTarget.Size / 2` (中心缩放)
- Event handlers: `mouse_entered` → Hover, `mouse_exited` → Normal, `gui_input` (Left Press) → Press, (Left Release) → Hover

**SynergyDataResource:**
- Inherits `Resource`, marked `[GlobalClass]`
- Export: `string[] ProvidedTags`, `Array<Vector2I> StarOffsets`, `string RequiredTag`, `string SynergyEffect`
- Helper methods: `HasTag()`, `GetStarCount()`, `IsValid()`

**SynergyComponent:**
- Inherits `Node`, marked `[GlobalClass]`
- Export: `SynergyDataResource SynergyData`, `GridShapeComponent Shape`
- State: `HashSet<Vector2I> ActiveStars`, `int _rotationCount` (0-3)
- R3 Subject: `OnSynergyChangedAsObservable` (Subject<HashSet<Vector2I>>)
- Subscribe to `Shape.OnShapeChangedAsObservable` → `_rotationCount++` (追踪旋转)
- `CheckSynergies(BackpackGridComponent, Vector2I)`:
  1. Clear ActiveStars
  2. Foreach StarOffset in SynergyData.StarOffsets
  3. Apply rotation: `ApplyRotationToOffset(starOffset, _rotationCount)`
  4. Calculate world position: `starWorldPos = currentGridPos + rotatedOffset`
  5. Query item: `logicGrid.GetItemAt(starWorldPos)`
  6. Check tag: `item.SynergyData.HasTag(RequiredTag)`
  7. If match: `ActiveStars.Add(rotatedOffset)`
  8. Emit: `OnSynergyChangedAsObservable.OnNext(ActiveStars)`
- `ApplyRotationToOffset()`: Loop apply `(x,y) → (-y,x)` for `rotationCount` times

</modifications>

<directives>

**Grid Logic:**
- MUST use 1D array for grid storage. NEVER use 2D array.
- MUST use formula `index = y * Width + x` for coordinate conversion.
- MUST validate bounds before array access.
- MUST clear grid cells when removing items.

**Shape Management:**
- MUST call `NormalizeShape()` after rotation to ensure origin at (0,0).
- MUST use rotation matrix `(x,y) → (-y,x)` for clockwise 90°.
- MUST convert `Godot.Collections.Array<Vector2I>` to `Vector2I[]` for runtime use.

**R3 Integration:**
- MUST use `Subject<Unit>` for parameterless events.
- MUST call `OnNext(Unit.Default)` to emit events.
- MUST dispose all Subjects in `_ExitTree()`.
- MUST use `CompositeDisposable` pattern for subscribers.
- MUST use `.AddTo(itemEntity)` when subscribing to item events (auto-cleanup on item destroy).

**StateChart Communication:**
- MUST use `StateChart.Call("send_event", "event_name")` to send events.
- NEVER use `GetParent()?.Call()` when StateChart reference exists.
- MUST verify StateChart reference before calling.

**Power Switch Pattern:**
- MUST call `AutoBindToParentState()` in components under AtomicState.
- MUST NOT manually call `SetProcess()` after AutoBind.
- MUST connect `state_entered`/`state_exited` for custom logic (e.g., ZIndex).
- MUST save original state (e.g., ZIndex) before modification.

**Input Handling:**
- MUST subscribe to `Control.GuiInput` event, NOT override `_GuiInput()`.
- MUST unsubscribe in `_ExitTree()` to prevent memory leaks.
- MUST check `InputEventMouseButton.ButtonIndex` and `Pressed` state.

**UI Dragging:**
- MUST elevate ZIndex during drag (recommend +100).
- MUST restore original ZIndex after drag.
- MUST use `GlobalPosition` for mouse tracking (avoid parent transform issues).
- MUST apply `GrabOffset` to maintain grab point.

**Coordinate Conversion:**
- MUST use `ViewGrid.GetGlobalMousePosition()` for mouse position (NOT `GetViewport().GetMousePosition()`).
- MUST use `globalPos - GlobalPosition` for global-to-local conversion.
- MUST use `Mathf.FloorToInt()` for pixel-to-grid conversion.
- MUST clamp grid coordinates to valid range [0, Width) x [0, Height).
- MUST multiply by CellSize for grid-to-pixel conversion.

**MVC Controller Pattern:**
- MUST maintain drag state in `Dictionary<Node, ItemDragState>`.
- MUST record original position before pickup (for bounce-back).
- MUST remove item from grid on pickup (防自我占用).
- MUST check mouse in backpack range before placement.
- MUST snap to grid on successful placement: `ViewGrid.GlobalPosition + ViewGrid.GridToLocalPosition(gridPos)`.
- MUST bounce back on failed placement: restore `OriginalGlobalPos` + force `TryPlaceItem(OriginalGridPos)`.

**UI Animation (Logic/Visual Separation):**
- MUST separate InteractionArea (Scale=1,1) and VisualTarget (可缩放).
- NEVER scale InteractionArea (破坏坐标系统).
- MUST set `PivotOffset = Size / 2` for center-based scaling.
- MUST kill current tween before starting new animation.
- MUST use `EaseType.Out` + `TransitionType.Sine` for smooth transitions.

**Synergy System:**
- MUST track rotation count via `Shape.OnShapeChangedAsObservable`.
- MUST apply rotation to StarOffsets: loop `(x,y) → (-y,x)` for `rotationCount` times.
- MUST query grid at `currentGridPos + rotatedOffset`.
- MUST check `ProvidedTags` contains `RequiredTag`.
- MUST emit `OnSynergyChangedAsObservable` after each check.

**Resource Design:**
- MUST inherit `Resource` for editor-creatable assets.
- MUST mark with `[GlobalClass]` for editor visibility.
- MUST use `Godot.Collections.Array<T>` for exported arrays (better editor support).
- MUST provide default values for all exported properties.

**UI Sizing:**
- MUST set both `CustomMinimumSize` and `Size` in `_Ready()`.
- MUST calculate total size as `Width * CellSize.X` and `Height * CellSize.Y`.
- MUST call `RefreshGrid()` after changing CellSize or LogicGrid dimensions.

**Grid Visualization:**
- MUST use `DrawLine()` in `_Draw()` for grid lines.
- MUST draw (Width+1) vertical lines and (Height+1) horizontal lines.
- MUST call `QueueRedraw()` after property changes affecting visualization.
- MUST respect `DrawDebugLines` flag before drawing.

**Scene Structure:**
- MUST place FollowMouseUIComponent under Dragging AtomicState (Power Switch).
- MUST place UITweenInteractComponent as sibling to VisualContainer.
- MUST nest VisualContainer inside InteractionArea (logic/visual separation).
- MUST place StarContainer inside VisualContainer for synergy visualization.

</directives>
