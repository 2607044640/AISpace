# Last Conversation State
*Updated: 2026-04-09*
## Project Status
- **Engine:** Godot 4.6.1 stable mono
- **Language:** C# only
- **Project:** 3D character controller + Grid inventory system
- **Phase:** Grid-based backpack system fully implemented
## Completed This Session
### Grid Inventory System (Complete)
**Architecture:** 6-layer component system with R3 reactive streams and StateChart integration
**Created Files:**
1. `3d-practice/B1Scripts/Components/BackpackGridComponent.cs` - Data layer (1D array grid logic)
2. `3d-practice/B1Scripts/Resources/ItemDataResource.cs` - Resource layer (Godot Resource for items)
3. `3d-practice/B1Scripts/Components/GridShapeComponent.cs` - Shape layer (runtime rotation)
4. `3d-practice/B1Scripts/Components/DraggableItemComponent.cs` - Input layer (GUI → StateChart bridge)
5. `3d-practice/B1Scripts/Components/FollowMouseUIComponent.cs` - Physics layer (mouse tracking)
6. `3d-practice/B1Scripts/Components/BackpackGridUIComponent.cs` - View layer (coordinate conversion)
**Documentation:**
- `KiroWorkingSpace/.kiro/steering/Godot/GridInventorySystem_Context.md` - Compressed domain rules
### Component Details
**BackpackGridComponent (Data Layer):**
- 1D array storage: `ItemData[] _gridData` (index = y * Width + x)
- Methods: `CanPlaceItem()`, `TryPlaceItem()`, `RemoveItem()`, `GetItemAt()`, `ClearGrid()`
- R3 Subjects: `OnItemPlacedAsObservable`, `OnItemRemovedAsObservable`
- Supports arbitrary item shapes (Tetris-like)
**ItemDataResource (Resource Layer):**
- Inherits `Resource`, marked `[GlobalClass]`
- Export: `ItemID`, `ItemName`, `Icon`, `BaseShape` (Godot.Collections.Array<Vector2I>)
- Editor-creatable .tres files
- Helper methods: `GetCellCount()`, `GetBoundingSize()`, `IsShapeValid()`
**GridShapeComponent (Shape Layer):**
- Runtime shape: `Vector2I[] CurrentLocalCells`
- Rotation matrix (clockwise 90°): `(x, y) → (-y, x)`
- `Rotate90()` applies rotation + `NormalizeShape()` (ensures origin at 0,0)
- R3 Subject: `OnShapeChangedAsObservable` (Subject<Unit>)
**DraggableItemComponent (Input Layer):**
- Export: `Control ClickableArea`, `Node StateChart`
- Subscribe to `ClickableArea.GuiInput` event
- Mouse left press → `StateChart.Call("send_event", "drag_start")` + R3 event
- Mouse left release → `StateChart.Call("send_event", "drag_end")` + R3 event
- Mouse right press → `OnRotateRequestedAsObservable.OnNext(Unit.Default)`
- **Bug Fixed:** Use `StateChart.Call()` directly, NOT `GetParent()?.Call()`
**FollowMouseUIComponent (Physics Layer):**
- Export: `Control TargetUI`, `Vector2 GrabOffset`
- Uses `AutoBindToParentState()` (Power Switch mode)
- Connect `state_entered` → ZIndex +100
- Connect `state_exited` → restore ZIndex
- `_Process()`: `TargetUI.GlobalPosition = GetGlobalMousePosition() + GrabOffset`
- Must be child of Dragging AtomicState
**BackpackGridUIComponent (View Layer):**
- Inherits `Control` (not Node)
- Export: `BackpackGridComponent LogicGrid`, `Vector2 CellSize`, `bool DrawDebugLines`, `Color GridColor`
- Auto-sizes UI: `Size = Width * CellSize.X, Height * CellSize.Y`
- Coordinate conversion:
  - `GlobalToGridPosition()` - Global pixels → Grid coords
  - `GridToLocalPosition()` - Grid coords → Local pixels
  - `GetCellCenterPosition()` - Grid coords → Center pixels
  - `LocalToGridPosition()` - Local pixels → Grid coords
- `_Draw()` renders debug grid lines
- Helper methods: `GetCellRect()`, `GetShapeRect()`, `IsValidGridPosition()`
### Technical Achievements
**R3 Integration:**
- All components use `Subject<T>` for reactive events
- Proper disposal in `_ExitTree()`
- `Subject<Unit>` for parameterless events
**StateChart Integration:**
- DraggableItemComponent bridges GUI input to StateChart
- FollowMouseUIComponent uses Power Switch pattern
- Recommended structure: Root → Idle/Dragging states
**Coordinate System:**
- 1D array with formula: `index = y * Width + x`
- Rotation matrix: `(x,y) → (-y,x)` for 90° clockwise
- Normalization ensures origin at (0,0) after rotation
**Architecture Patterns:**
- Separation of concerns (6 distinct layers)
- Pure data logic (BackpackGridComponent)
- Pure view logic (BackpackGridUIComponent)
- Event-driven communication (R3 Subjects)
- StateChart lifecycle management
## Active Files
**Created:**
- `3d-practice/B1Scripts/Components/BackpackGridComponent.cs`
- `3d-practice/B1Scripts/Resources/ItemDataResource.cs`
- `3d-practice/B1Scripts/Components/GridShapeComponent.cs`
- `3d-practice/B1Scripts/Components/DraggableItemComponent.cs`
- `3d-practice/B1Scripts/Components/FollowMouseUIComponent.cs`
- `3d-practice/B1Scripts/Components/BackpackGridUIComponent.cs`
- `KiroWorkingSpace/.kiro/steering/Godot/GridInventorySystem_Context.md`
**Modified:**
- `3d-practice/B1Scripts/Components/DraggableItemComponent.cs` - Bug fix (StateChart.Call)
## Next Session Tasks
### Immediate (Backpack System)
1. Create item visual component (displays icon + shape overlay)
2. Implement drag preview (semi-transparent item following mouse)
3. Add placement validation visual feedback (green/red highlight)
4. Create backpack UI scene (BackpackGridUIComponent + item slots)
5. Implement item pickup/drop logic
6. Add item rotation on right-click during drag
7. Test with various item shapes (1x1, 2x1, L-shape, T-shape)
### Integration
1. Connect backpack to player inventory data
2. Add item database (ItemDataResource .tres files)
3. Implement item stacking (for 1x1 items)
4. Add item tooltips (hover info)
5. Create item context menu (use, drop, split)
### Polish
1. Add drag/drop sound effects
2. Implement smooth item snap animation
3. Add particle effects for item pickup
4. Create item rarity visual indicators
5. Implement auto-sort functionality
## Critical Context
### Grid System Design Decisions
**Why 1D array?**
- Cache-friendly memory layout
- Simple index calculation
- Easier serialization
- Standard game dev practice
**Why rotation matrix instead of angle?**
- Discrete 90° rotations only
- No floating-point errors
- Instant calculation
- Predictable results
**Why separate shape component?**
- Runtime rotation support
- Decouples data from behavior
- Reusable across item types
- Supports dynamic shape changes
**Why R3 Subject<Unit>?**
- Parameterless events (just notification)
- Subscribers read current state directly
- Consistent with R3 patterns
- Zero allocation
### StateChart Integration Pattern
**Recommended Structure:**
```
ItemEntity (Control)
├── StateChart
│   └── Root (CompoundState, initial="Idle")
│       ├── Idle (AtomicState)
│       │   └── Transition: event="drag_start" → Dragging
│       └── Dragging (AtomicState)
│           ├── FollowMouseUIComponent
│           └── Transition: event="drag_end" → Idle
├── DraggableItemComponent
├── GridShapeComponent
└── [Visual children]
```
**Event Flow:**
1. User clicks → DraggableItemComponent.GuiInput
2. Component sends "drag_start" → StateChart
3. StateChart activates Dragging state
4. FollowMouseUIComponent auto-enabled (Power Switch)
5. Item follows mouse + ZIndex elevated
6. User releases → "drag_end" → back to Idle
7. FollowMouseUIComponent auto-disabled
## Build Status
✅ All 6 components compiled successfully
✅ No errors
⚠️ 5 warnings (phantom_camera plugin, not project code)
## Architecture Principles Applied
1. **Separation of Concerns:** 6 distinct layers, each with single responsibility
2. **Reactive Programming:** R3 Subjects for event streams
3. **State Management:** StateChart controls component lifecycle
4. **Coordinate Abstraction:** View layer handles all pixel↔grid conversions
5. **Resource-Driven Design:** ItemDataResource for editor-friendly configuration
6. **Power Switch Pattern:** Components auto-enable/disable with states
## Next Session Start
1. Read this file to restore context
2. Review `GridInventorySystem_Context.md` for technical rules
3. Create item visual component
4. Build backpack UI scene
5. Test drag-and-drop with debug grid
