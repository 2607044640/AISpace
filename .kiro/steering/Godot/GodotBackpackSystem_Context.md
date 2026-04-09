---
inclusion: manual
---

<context>
Grid-based inventory system with drag-and-drop, rotation, and StateChart integration. Supports arbitrary item shapes (Tetris-like) with reactive event streams (R3).
</context>

<architecture>

**Component Hierarchy:**
```
Data Layer:    BackpackGridComponent (1D array grid logic)
Resource Layer: ItemDataResource (static item config)
Shape Layer:   GridShapeComponent (runtime shape + rotation)
Input Layer:   DraggableItemComponent (GUI input → StateChart bridge)
Physics Layer: FollowMouseUIComponent (mouse tracking via Power Switch)
```

**File Paths:**
- Components: `3d-practice/B1Scripts/Components/`
- Resources: `3d-practice/B1Scripts/Resources/`

**Core Classes:**
- `BackpackGridComponent : Node` - Grid data manager (Width x Height → 1D array)
- `ItemDataResource : Resource` - Godot resource (ItemID, ItemName, Icon, BaseShape)
- `GridShapeComponent : Node` - Shape manager (CurrentLocalCells, Rotate90)
- `DraggableItemComponent : Node` - Input handler (GuiInput → StateChart events)
- `FollowMouseUIComponent : Node` - Mouse follower (挂载在 Dragging AtomicState 下)

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

**Resource Design:**
- MUST inherit `Resource` for editor-creatable assets.
- MUST mark with `[GlobalClass]` for editor visibility.
- MUST use `Godot.Collections.Array<T>` for exported arrays (better editor support).
- MUST provide default values for all exported properties.

**Documentation:**
- MUST include 3-part structure for complex logic: 目的 → 示例 → 算法.
- MUST explain rotation matrix derivation in comments.
- MUST document StateChart integration patterns.
- OMIT documentation for trivial lifecycle methods (_Ready, _ExitTree).

</directives>
