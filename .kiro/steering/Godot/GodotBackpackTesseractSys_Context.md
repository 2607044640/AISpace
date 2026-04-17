---
inclusion: manual
---

<context>
**Tesseract Backpack (TS)** - Grid-based inventory system with drag-and-drop, rotation, StateChart integration, and Backpack Battles-style synergy system. Supports arbitrary item shapes (Tetris-like) with reactive event streams (R3), MVC architecture, and UI micro-interactions.
</context>

<layer_1_quick_start>
  <quick_reference>
    - **Project Prefix:** TS (Tesseract)
    - **Rule Storage:** Store ALL rules in `KiroWorkingSpace/.kiro/`.
    - **Addon Root (Legacy):** `3d-practice/addons/A1TetrisBackpack/` (旧代码库)
    - **New Project Root:** `3d-practice/A1TesseractBackpack/` (新场景和资源)
    - **Scene Naming:** All scene files use `TS` prefix (e.g., `TSItem.tscn`)
    - **Core Path:** `3d-practice/addons/A1TetrisBackpack/Core/` (BackpackGridComponent, BackpackInteractionController, BackpackGridUIComponent)
    - **Items Path:** `3d-practice/addons/A1TetrisBackpack/Items/` (ItemDataResource, GridShapeComponent, AutoShapeBuilderComponent)
    - **Interaction Path:** `3d-practice/addons/A1TetrisBackpack/Interaction/` (DraggableItemComponent, FollowMouseUIComponent)
    - **Synergies Path:** `3d-practice/addons/A1TetrisBackpack/Synergies/` (SynergyDataResource, SynergyComponent)
    - **MicroUI Path:** `3d-practice/addons/A1TetrisBackpack/MicroUI/` (UITweenInteractComponent)
    - **Core Dependencies:** R3 (Cysharp) for reactive streams, GodotStateCharts for state management.
  </quick_reference>

  <decision_tree>
    - **If handling item pickup:** Record original state + call `LogicGrid.RemoveItem()`. (Why: Prevents the item from occupying its own space during dragging).
    - **If handling item drop:** Check `ViewGrid.GetGlobalRect().HasPoint(mousePos)`. (Why: Ensures placement only occurs within the valid backpack boundaries).
    - **If TryPlaceItem() succeeds:** Execute `PerformSnapToGrid()`. (Why: Aligns the visual item perfectly with the underlying logic grid).
    - **If TryPlaceItem() fails:** Execute `PerformBounceBack()`. (Why: Restores the item to its `OriginalGlobalPos` and re-registers it at `OriginalGridPos`).
  </decision_tree>

  <minimal_workflow>
    1. Subscribe to `DraggableItemComponent` input via `.AddTo(itemEntity)`.
    2. Left press triggers `drag_start` StateChart event and emits `OnDragStartedAsObservable`.
    3. State changes to `Dragging`; `FollowMouseUIComponent` (Power Switch) elevates ZIndex and tracks mouse via `GlobalPosition`.
    4. Left release triggers `drag_end`; `BackpackInteractionController` converts `ViewGrid.GetGlobalMousePosition()` to grid coordinates.
    5. Controller attempts `LogicGrid.TryPlaceItem()`, executing snap or bounce-back based on result.
  </minimal_workflow>

  <top_anti_patterns>
    - NEVER use 2D arrays for grid mapping. (Why: Violates core `ItemData[] _gridData` 1D array architecture).
    - NEVER scale the `InteractionArea`. (Why: Destroys the UI coordinate system; scale `VisualTarget` instead).
    - NEVER call `GetParent()?.Call()` for StateChart events. (Why: Bypasses direct references and causes silent failures).
    - NEVER use `GetViewport().GetMousePosition()`. (Why: Fails in scaled/nested viewports; always use `ViewGrid.GetGlobalMousePosition()`).
    - NEVER manually call `SetProcess()` on Power Switch components. (Why: `AutoBindToParentState()` manages lifecycle automatically).
  </top_anti_patterns>
</layer_1_quick_start>

<layer_2_detailed_guide>
  <api_reference>
    | Class | Methods/Properties | Parameters / Types |
    | :--- | :--- | :--- |
    | `BackpackGridComponent` | `CanPlaceItem`, `TryPlaceItem`, `RemoveItem`, `GetItemAt`, `ClearGrid` | `ItemData[] _gridData`, `OnItemPlacedAsObservable`, `OnItemRemovedAsObservable` |
    | `BackpackGridUIComponent` | `GlobalToGridPosition`, `GridToLocalPosition`, `GetCellCenterPosition`, `LocalToGridPosition`, `IsValidGridPosition`, `GetCellRect`, `GetShapeRect`, `RefreshGrid`, `SetCellSize`, `ToggleDebugLines` | `[GlobalClass]`, `Vector2 CellSize`, `bool DrawDebugLines`, `Color GridColor` |
    | `BackpackInteractionController` | `RegisterItem`, `HandleItemPickedUp`, `HandleItemDropped`, `HandleItemRotated` | `Dictionary<Node, ItemDragState>` |
    | `ItemDataResource` | `GetCellCount`, `GetBoundingSize`, `IsShapeValid` | `ItemID`, `ItemName`, `Icon`, `BaseShape` (Array<Vector2I>) |
    | `GridShapeComponent` | `Rotate90`, `NormalizeShape` | `Vector2I[] CurrentLocalCells`, `OnShapeChangedAsObservable` |
    | `DraggableItemComponent` | `GuiInput` event handlers | `Control ClickableArea`, `Node StateChart`, `OnRotateRequestedAsObservable` |
    | `FollowMouseUIComponent` | `AutoBindToParentState`, `OnDragStateEntered`, `OnDragStateExited` | `Control TargetUI`, `Vector2 GrabOffset` |
    | `UITweenInteractComponent` | `AnimateToScale`, `UpdatePivotOffset` | `Control InteractionArea`, `Control VisualTarget`, `Vector2 HoverScale`, `Vector2 PressScale`, `float TweenDuration` |
    | `SynergyDataResource` | `HasTag`, `GetStarCount`, `IsValid` | `string[] ProvidedTags`, `Array<Vector2I> StarOffsets`, `string RequiredTag`, `string SynergyEffect` |
    | `SynergyComponent` | `CheckSynergies`, `ApplyRotationToOffset` | `HashSet<Vector2I> ActiveStars`, `int _rotationCount`, `OnSynergyChangedAsObservable` |
  </api_reference>

  <technical_specifications>
    *Scene Tree Hierarchy:*
    * BackpackPanel (BackpackGridUIComponent)
      * BackpackInteractionController
      * BackpackGridComponent (LogicGrid)
      * Items Container
        * ItemEntity (Control) [InteractionArea: Scale ALWAYS 1,1]
          * StateChart
            * Root (CompoundState, initial="Idle")
              * Idle (AtomicState) -> Transition: event="drag_start" -> Dragging
              * Dragging (AtomicState) -> Transition: event="drag_end" -> Idle
                * FollowMouseUIComponent
          * DraggableItemComponent
          * GridShapeComponent
          * SynergyComponent
          * UITweenInteractComponent
          * VisualContainer (Control) [VisualTarget: Scale CAN vary]
            * ItemIcon (TextureRect)
            * StarContainer (Control)
              * Star1 (TextureRect) [Gray/Bright toggle]
              * Star2 (TextureRect)
    
    *Math Formulas & Core Logic:*
    * 1D Array Index: `index = y * Width + x`
    * Clockwise 90° Rotation Matrix: `(x, y) -> (-y, x)`
    * Global to Grid: `FloorToInt((globalPos - GlobalPosition) / CellSize)` -> Clamp
    * Grid to Local: `gridPos * CellSize`
    * Local to Grid: `FloorToInt(localPos / CellSize)` -> Clamp
    * Cell Center: `GridToLocalPosition + CellSize / 2`
    * Synergy World Pos: `currentGridPos + rotatedOffset`

    *Default Values & Magic Numbers:*
    * `CellSize`: `Vector2(64, 64)`
    * `HoverScale`: `Vector2(1.05, 1.05)`
    * `PressScale`: `Vector2(0.95, 0.95)`
    * `TweenDuration`: `0.15f`
    * `ZIndex` during drag: `+100`
  </technical_specifications>

  <core_rules>
    <rule>
      <description>Inherit `Resource` and mark with `[GlobalClass]` for editor-creatable assets, using `Godot.Collections.Array<T>` for exported arrays.</description>
      <rationale>Ensures full compatibility and visibility within the Godot editor inspector.</rationale>
    </rule>
    <rule>
      <description>Separate logic and visual UI by nesting `VisualContainer` inside `InteractionArea`. NEVER scale the `InteractionArea`.</description>
      <rationale>Scaling the InteractionArea corrupts mouse coordinate calculations and grid logic.</rationale>
    </rule>
    <rule>
      <description>Use `Subject<Unit>` for parameterless R3 events, call `OnNext(Unit.Default)` to emit, and dispose all Subjects in `_ExitTree()`.</description>
      <rationale>Prevents severe memory leaks and ensures correct reactive stream lifecycle management.</rationale>
    </rule>
    <rule>
      <description>Call `NormalizeShape()` immediately after applying the `(x,y) -> (-y,x)` rotation matrix.</description>
      <rationale>Ensures the shape's local origin strictly maintains a minimum bound of (0,0).</rationale>
    </rule>
    <rule>
      <description>Apply rotation loops to `StarOffsets` based on `_rotationCount` (tracked via `Shape.OnShapeChangedAsObservable`) during synergy checks.</description>
      <rationale>Ensures Synergy stars accurately follow the item's current geometric orientation.</rationale>
    </rule>
    <rule>
      <description>Set `VisualTarget.PivotOffset = VisualTarget.Size / 2` before any tween animation.</description>
      <rationale>Guarantees all micro-interactions scale uniformly from the exact center of the item.</rationale>
    </rule>
    <rule>
      <description>Set both `CustomMinimumSize` and `Size` using `Vector2(Width * CellSize.X, Height * CellSize.Y)` in `_Ready()`.</description>
      <rationale>Forces the UI Control to correctly enclose the entire physical grid area.</rationale>
    </rule>
    <rule>
      <description>Save `_originalZIndex` before elevating to `+100` on drag, and restore it on drop.</description>
      <rationale>Maintains proper rendering order and prevents permanent UI z-fighting after dragging.</rationale>
    </rule>
  </core_rules>
</layer_2_detailed_guide>

<layer_3_advanced>
  <troubleshooting>
    <error symptom="StateChart events fail to fire on drag">
      <cause>Using parent reference mapping `GetParent()?.Call()` which fails in updated Godot StateCharts.</cause>
      <fix>Use `StateChart.Call("send_event", "event_name")` directly on the referenced `StateChart` node.</fix>
    </error>
    <error symptom="Item shape origin shifts out of bounds after rotation">
      <cause>Failure to re-anchor the shape coordinates after matrix multiplication.</cause>
      <fix>Execute `NormalizeShape()` to dynamically shift the shape array so `min(X)` and `min(Y)` equal `0`.</fix>
    </error>
    <error symptom="Memory leak warnings / Ghost events firing">
      <cause>Dangling GUI Input subscriptions or undisposed R3 Subjects.</cause>
      <fix>Unsubscribe `ClickableArea.GuiInput` and call `Dispose()` on all Subjects in `_ExitTree()`. Use `.AddTo(itemEntity)` for subscriptions.</fix>
    </error>
    <error symptom="Item refuses to place in its original spot after pickup">
      <cause>The grid logic still registers the grid cells as occupied by the dragged item itself.</cause>
      <fix>Call `LogicGrid.RemoveItem()` within `HandleItemPickedUp()` before evaluating drop logic.</fix>
    </error>
  </troubleshooting>

  <implementation_anchors>
    - **MVC Controller Concept:** `BackpackInteractionController` bridges `DraggableItemComponent` input with `BackpackGridComponent` backend. Maintain state via `Dictionary<Node, ItemDragState>`.
    - **Power Switch Pattern:** Used by `FollowMouseUIComponent`. Placement strictly under the `Dragging` AtomicState allows `AutoBindToParentState()` to natively handle activation/deactivation hooks (`state_entered`/`state_exited`) without explicit controller toggling.
    - **Micro-Interaction Tweens:** Inside `UITweenInteractComponent`, execute `_currentTween?.Kill()` before starting a new `AnimateToScale()`. Use `EaseType.Out` and `TransitionType.Sine` for easing math.
    - **Grid Visualization Anchor:** `BackpackGridUIComponent._Draw()` plots `(Width + 1)` vertical lines and `(Height + 1)` horizontal lines when `DrawDebugLines` is true, followed by `QueueRedraw()` on dependency update.
  </implementation_anchors>

  <critical_constraints>
    <constraint category="Grid Logic">
      <rule>Use 1D array for grid storage. Formula: `index = y * Width + x`.</rule>
      <rule>Validate bounds before array access.</rule>
      <rule>Clear grid cells when removing items.</rule>
    </constraint>
    
    <constraint category="Shape Management">
      <rule>Use rotation matrix `(x,y) -> (-y,x)` for clockwise 90°.</rule>
      <rule>Call `NormalizeShape()` after rotation to ensure origin at (0,0).</rule>
      <rule>Convert `Godot.Collections.Array<Vector2I>` to `Vector2I[]` for runtime use.</rule>
    </constraint>
    
    <constraint category="R3 Integration">
      <rule>Use `Subject<Unit>` for parameterless events.</rule>
      <rule>Call `OnNext(Unit.Default)` to emit events.</rule>
      <rule>Dispose all Subjects in `_ExitTree()`.</rule>
      <rule>Use `CompositeDisposable` pattern for subscribers.</rule>
      <rule>Use `.AddTo(itemEntity)` when subscribing to item events (auto-cleanup on item destroy).</rule>
    </constraint>
    
    <constraint category="StateChart Communication">
      <rule>Use `StateChart.Call("send_event", "event_name")` to send events.</rule>
      <rule>NEVER use `GetParent()?.Call()` when StateChart reference exists.</rule>
      <rule>Verify StateChart reference before calling.</rule>
    </constraint>
    
    <constraint category="Power Switch Pattern">
      <rule>Call `AutoBindToParentState()` in components under AtomicState.</rule>
      <rule>NEVER manually call `SetProcess()` after AutoBind.</rule>
      <rule>Connect `state_entered`/`state_exited` for custom logic (e.g., ZIndex).</rule>
      <rule>Save original state (e.g., ZIndex) before modification.</rule>
    </constraint>
    
    <constraint category="Input Handling">
      <rule>Subscribe to `Control.GuiInput` event, NOT override `_GuiInput()`.</rule>
      <rule>Unsubscribe in `_ExitTree()` to prevent memory leaks.</rule>
      <rule>Check `InputEventMouseButton.ButtonIndex` and `Pressed` state.</rule>
    </constraint>
    
    <constraint category="UI Dragging">
      <rule>Elevate ZIndex during drag (recommend +100).</rule>
      <rule>Restore original ZIndex after drag.</rule>
      <rule>Use `GlobalPosition` for mouse tracking (avoid parent transform issues).</rule>
      <rule>Apply `GrabOffset` to maintain grab point.</rule>
    </constraint>
    
    <constraint category="Coordinate Conversion">
      <rule>Use `ViewGrid.GetGlobalMousePosition()` for mouse position (NOT `GetViewport().GetMousePosition()`).</rule>
      <rule>Use `globalPos - GlobalPosition` for global-to-local conversion.</rule>
      <rule>Use `Mathf.FloorToInt()` for pixel-to-grid conversion.</rule>
      <rule>Clamp grid coordinates to valid range [0, Width) x [0, Height).</rule>
      <rule>Multiply by CellSize for grid-to-pixel conversion.</rule>
    </constraint>
    
    <constraint category="MVC Controller Pattern">
      <rule>Maintain drag state in `Dictionary<Node, ItemDragState>`.</rule>
      <rule>Record original position before pickup (for bounce-back).</rule>
      <rule>Remove item from grid on pickup (prevents self-occupation).</rule>
      <rule>Check mouse in backpack range before placement.</rule>
      <rule>Snap to grid on successful placement: `ViewGrid.GlobalPosition + ViewGrid.GridToLocalPosition(gridPos)`.</rule>
      <rule>Bounce back on failed placement: restore `OriginalGlobalPos` + force `TryPlaceItem(OriginalGridPos)`.</rule>
    </constraint>
    
    <constraint category="UI Animation (Logic/Visual Separation)">
      <rule>Separate InteractionArea (Scale=1,1) and VisualTarget (can scale).</rule>
      <rule>NEVER scale InteractionArea (breaks coordinate system).</rule>
      <rule>Set `PivotOffset = Size / 2` for center-based scaling.</rule>
      <rule>Kill current tween before starting new animation.</rule>
      <rule>Use `EaseType.Out` + `TransitionType.Sine` for smooth transitions.</rule>
    </constraint>
    
    <constraint category="Synergy System">
      <rule>Track rotation count via `Shape.OnShapeChangedAsObservable`.</rule>
      <rule>Apply rotation to StarOffsets: loop `(x,y) -> (-y,x)` for `rotationCount` times.</rule>
      <rule>Query grid at `currentGridPos + rotatedOffset`.</rule>
      <rule>Check `ProvidedTags` contains `RequiredTag`.</rule>
      <rule>Emit `OnSynergyChangedAsObservable` after each check.</rule>
    </constraint>
    
    <constraint category="Resource Design">
      <rule>Inherit `Resource` for editor-creatable assets.</rule>
      <rule>Mark with `[GlobalClass]` for editor visibility.</rule>
      <rule>Use `Godot.Collections.Array<T>` for exported arrays (better editor support).</rule>
      <rule>Provide default values for all exported properties.</rule>
    </constraint>
    
    <constraint category="UI Sizing">
      <rule>Set both `CustomMinimumSize` and `Size` in `_Ready()`.</rule>
      <rule>Calculate total size as `Width * CellSize.X` and `Height * CellSize.Y`.</rule>
      <rule>Call `RefreshGrid()` after changing CellSize or LogicGrid dimensions.</rule>
    </constraint>
    
    <constraint category="Grid Visualization">
      <rule>Use `DrawLine()` in `_Draw()` for grid lines.</rule>
      <rule>Draw (Width+1) vertical lines and (Height+1) horizontal lines.</rule>
      <rule>Call `QueueRedraw()` after property changes affecting visualization.</rule>
      <rule>Respect `DrawDebugLines` flag before drawing.</rule>
    </constraint>
    
    <constraint category="Scene Structure">
      <rule>Place FollowMouseUIComponent under Dragging AtomicState (Power Switch).</rule>
      <rule>Place UITweenInteractComponent as sibling to VisualContainer.</rule>
      <rule>Nest VisualContainer inside InteractionArea (logic/visual separation).</rule>
      <rule>Place StarContainer inside VisualContainer for synergy visualization.</rule>
    </constraint>
  </critical_constraints>

  <best_practices>
    <rule>
      <description>Expose internal state changes (Shape, Synergy, Placement) purely through R3 Observables.</description>
      <rationale>Maintains reactive architecture and prevents tight coupling.</rationale>
    </rule>
    <rule>
      <description>Validate `InputEventMouseButton.ButtonIndex` and `.Pressed` states when subscribing to `Control.GuiInput`.</description>
      <rationale>Prevents unintended event handling and ensures precise input control.</rationale>
    </rule>
    <rule>
      <description>Use `GlobalPosition = GetGlobalMousePosition() + GrabOffset` for drag updates.</description>
      <rationale>Bypasses all localized parent transform mutations and ensures accurate positioning.</rationale>
    </rule>
  </best_practices>
</layer_3_advanced>