---
inclusion: manual
---

<context>
**Tesseract Backpack (TS)** - Grid-based inventory system with drag-and-drop, rotation, StateChart integration, and Backpack Battles-style synergy system. Supports arbitrary item shapes (Tetris-like) with reactive event streams (R3), MVC architecture, and UI micro-interactions.

**Latest Architecture (2026-04-23):**
- **Lifecycle Management:** Subjects initialize in `_EnterTree()` (Top-Down), children subscribe in `_Ready()` (Bottom-Up)
- **UI Component System:** GridCellUI (transparent body + glowing border) + ItemCellGroupController (event aggregator)
- **MouseFilter Architecture:** Root + InteractionArea = Ignore (2), GridCellUI = Pass (0) - solves L-shape AABB bug
- **Event Flow:** Multiple GridCellUI → ItemCellGroupController (aggregator) → DraggableItemComponent
</context>

<layer_1_quick_start>
  <quick_reference>
    - **Project Prefix:** TS (Tesseract)
    - **Rule Storage:** Store ALL rules in `KiroWorkingSpace/.kiro/`.
    - **Addon Root (Legacy):** `3d-practice/addons/A1TetrisBackpack/` (旧代码库)
    - **New Project Root:** `3d-practice/A1TesseractBackpack/` (新场景和资源)
    - **Scene Naming:** All scene files use `TS` prefix (e.g., `TSItem.tscn`)
    - **Core Path:** `3d-practice/addons/A1TetrisBackpack/Core/` (BackpackGridComponent, BackpackInteractionController, BackpackGridUIComponent)
    - **Items Path:** `3d-practice/addons/A1TetrisBackpack/Items/` (ItemDataResource, GridShapeComponent, ItemCellGroupController, IItemDataProvider)
    - **UI Path:** `3d-practice/addons/A1TetrisBackpack/UI/` (GridCellUI - Panel-based cell component)
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
    - **NEVER set InteractionArea MouseFilter to Stop (0).** (Why: Creates rectangular AABB that blocks L-shape holes, preventing clicks on backpack grid underneath).
    - **NEVER initialize Subjects in `_Ready()`.** (Why: Child `_Ready()` executes before parent `_Ready()`, causing NullReferenceException when children try to subscribe).
    - **NEVER call `.AddTo()` before `AddChild()`.** (Why: R3 requires node to be in scene tree before subscription disposal tracking).
  </top_anti_patterns>
</layer_1_quick_start>

<layer_2_detailed_guide>
  <api_reference>
    | Class | Methods/Properties | Parameters / Types |
    | :--- | :--- | :--- |
    | `BackpackGridComponent` | `CanPlaceItem`, `TryPlaceItem`, `RemoveItem`, `GetItemAt`, `ClearGrid` | `ItemData[] _gridData`, `OnItemPlacedAsObservable`, `OnItemRemovedAsObservable` |
    | `BackpackGridUIComponent` | `GlobalToGridPosition`, `GridToLocalPosition`, `GetCellCenterPosition`, `LocalToGridPosition`, `IsValidGridPosition`, `GetCellRect`, `GetShapeRect`, `RefreshGrid`, `SetCellSize`, `GenerateBackgroundGrid` | `[GlobalClass]`, `Vector2 CellSize`, `Control GridContainer`, `List<GridCellUI> _backgroundCells` (Factory pattern for background grid) |
    | `BackpackInteractionController` | `RegisterItem`, `HandleItemPickedUp`, `HandleItemDropped`, `HandleItemRotated` | `Dictionary<Node, ItemDragState>` |
    | `ItemDataResource` | `GetCellCount`, `GetBoundingSize`, `IsShapeValid` | `ItemID`, `ItemName`, `Icon`, `BaseShape` (Array<Vector2I>) |
    | `GridShapeComponent` | `Rotate90`, `NormalizeShape` | `Vector2I[] CurrentLocalCells`, `OnShapeChangedAsObservable` (initialized in `_EnterTree()`) |
    | `IItemDataProvider` | `DataInitialized` event | Interface for parent-to-child data injection (solves _Ready() lifecycle issue) |
    | `GridCellUI` | `SetState`, `OnCellInputAsObservable`, `OnCellHoverAsObservable`, `MouseEntered`, `MouseExited` | Panel-based cell with StyleBoxFlat, states: Normal/Hover/Valid/Invalid |
    | `ItemCellGroupController` | `SetGroupState`, `ResetGroupState`, `OnGroupInputAsObservable` | Event aggregator for multiple GridCellUI instances, includes hover effect subscriptions |
    | `DraggableItemComponent` | `GuiInput` event handlers | `Control ClickableArea`, `Node StateChart`, `OnDragStartedAsObservable`, `OnDragEndedAsObservable`, `OnRotateRequestedAsObservable` (all initialized in `_EnterTree()`) |
    | `FollowMouseUIComponent` | `AutoBindToParentState`, `OnDragStateEntered`, `OnDragStateExited` | `Control TargetUI`, `Vector2 GrabOffset` |
    | `UITweenInteractComponent` | `AnimateToScale`, `UpdatePivotOffset` | `Control InteractionArea`, `Control VisualTarget`, `Vector2 HoverScale`, `Vector2 PressScale`, `float TweenDuration` |
    | `SynergyDataResource` | `HasTag`, `GetStarCount`, `IsValid` | `string[] ProvidedTags`, `Array<Vector2I> StarOffsets`, `string RequiredTag`, `string SynergyEffect` |
    | `SynergyComponent` | `CheckSynergies`, `ApplyRotationToOffset` | `HashSet<Vector2I> ActiveStars`, `int _rotationCount`, `OnSynergyChangedAsObservable` |
  </api_reference>

  <technical_specifications>
    *Scene Tree Hierarchy (Updated 2026-04-23):*
    * BackpackPanel (BackpackGridUIComponent)
      * BackpackInteractionController
      * BackpackGridComponent (LogicGrid)
      * Items Container
        * TetrisDraggableItem (Control) [ROOT: MouseFilter = Ignore (2)]
          * StateChart
            * Root (CompoundState, initial="Idle")
              * Idle (AtomicState) -> Transition: event="drag_start" -> Dragging
              * Dragging (AtomicState) -> Transition: event="drag_end" -> Idle
                * FollowMouseUIComponent
          * GridShapeComponent (initializes Subject in _EnterTree)
          * ItemCellGroupController (subscribes in _Ready, generates GridCellUI)
          * DraggableItemComponent (subscribes in _Ready)
          * InteractionArea (Control) [MouseFilter = Ignore (2), NEVER use Stop!]
            * GridCellUI (Panel) [MouseFilter = Pass (0), dynamically generated]
              * (Multiple instances for L-shape, each handles own input)
            * ItemIcon (TextureRect) [MouseFilter = Ignore (2)]
    
    *MouseFilter Architecture (CRITICAL):*
    * Root Node (TetrisDraggableItem): `mouse_filter = 2` (Ignore) - Transparent to mouse
    * InteractionArea: `mouse_filter = 2` (Ignore) - Transparent to mouse, allows children to receive events
    * GridCellUI (children): `mouse_filter = 0` (Pass) - Receives mouse events and bubbles up
    * ItemIcon: `mouse_filter = 2` (Ignore) - Decorative only
    
    **Why Ignore on InteractionArea?**
    - InteractionArea is a rectangular container (AABB bounding box)
    - If set to Stop (0), it blocks mouse events on L-shape holes
    - Setting to Ignore (2) makes it "transparent" - mouse passes through to GridCellUI children
    - GridCellUI children are positioned exactly at occupied cells, no holes
    - Result: Only actual item cells respond to clicks, holes pass through to backpack grid
    
    *Lifecycle Order (CRITICAL):*
    * `_EnterTree()`: Top-Down (Parent → Child)
      - Parent initializes all Subjects here: `new Subject<T>()`
      - Parent initializes core data structures
    * `_Ready()`: Bottom-Up (Child → Parent)
      - Children can safely subscribe to parent Subjects
      - Parent's _EnterTree has already executed
    
    *Event Flow Architecture:*
    * User clicks GridCellUI → GridCellUI.OnCellInputAsObservable emits
    * ItemCellGroupController aggregates all GridCellUI events → OnGroupInputAsObservable
    * DraggableItemComponent subscribes to aggregated stream → handles drag/rotate logic
    
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
    * `MouseFilter.Ignore`: `2`
    * `MouseFilter.Pass`: `0`
    * `MouseFilter.Stop`: `1` (NEVER use on InteractionArea!)
  </technical_specifications>

  <core_rules>
    <rule>
      <description>**CRITICAL: Initialize all Subjects in `_EnterTree()`, NOT `_Ready()`.**</description>
      <rationale>Godot executes `_EnterTree()` Top-Down (Parent before Child), but `_Ready()` Bottom-Up (Child before Parent). If parent initializes Subjects in `_Ready()`, children's `_Ready()` runs first and encounters null Subjects, causing NullReferenceException.</rationale>
      <enforcement>
        1. Parent: `public override void _EnterTree() { OnShapeChangedAsObservable = new Subject<Unit>(); }`
        2. Child: `public override void _Ready() { _parent.OnShapeChangedAsObservable.Subscribe(...); }`
      </enforcement>
    </rule>
    <rule>
      <description>**CRITICAL: Set InteractionArea MouseFilter to Ignore (2), NEVER Stop (1).**</description>
      <rationale>InteractionArea is a rectangular AABB container. If set to Stop, it blocks mouse events on L-shape holes, preventing clicks on backpack grid underneath. Setting to Ignore makes it transparent - mouse passes through to GridCellUI children positioned at actual occupied cells.</rationale>
      <enforcement>
        1. Root Node: `mouse_filter = 2` (Ignore)
        2. InteractionArea: `mouse_filter = 2` (Ignore)
        3. GridCellUI children: `mouse_filter = 0` (Pass) - receives events
      </enforcement>
    </rule>
    <rule>
      <description>**CRITICAL: Call `AddChild()` BEFORE `.Subscribe().AddTo()`.**</description>
      <rationale>R3's `.AddTo()` requires the node to be in the scene tree for disposal tracking. Calling `.AddTo()` before `AddChild()` throws "AddTo does not support to use before enter tree" error.</rationale>
      <enforcement>
        1. `AddChild(gridCellUI);` // Add to scene tree first
        2. `gridCellUI.OnCellInputAsObservable.Subscribe(...).AddTo(gridCellUI);` // Then subscribe
      </enforcement>
    </rule>
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
    <error symptom="NullReferenceException when child tries to subscribe to parent Subject">
      <cause>Parent initialized Subject in `_Ready()`, but child's `_Ready()` executes first (Bottom-Up execution order).</cause>
      <fix>Move Subject initialization to parent's `_EnterTree()` (Top-Down execution). Children can then safely subscribe in their `_Ready()`.</fix>
    </error>
    <error symptom="'AddTo does not support to use before enter tree' error">
      <cause>Called `.Subscribe().AddTo(node)` before `AddChild(node)`.</cause>
      <fix>Always call `AddChild()` first, then `.Subscribe().AddTo()`. R3 requires node to be in scene tree for disposal tracking.</fix>
    </error>
    <error symptom="L-shape item blocks clicks on empty holes, preventing backpack grid interaction">
      <cause>InteractionArea MouseFilter set to Stop (1), creating rectangular AABB that blocks mouse events.</cause>
      <fix>Set InteractionArea `mouse_filter = 2` (Ignore). This makes it transparent - mouse passes through to GridCellUI children at actual occupied cells.</fix>
    </error>
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
    - **Godot Lifecycle Pattern (_EnterTree vs _Ready):** Parent components initialize Subjects in `_EnterTree()` (Top-Down execution), allowing children to safely subscribe in `_Ready()` (Bottom-Up execution). This solves the classic "child tries to subscribe before parent initializes" problem.
    - **Event Aggregator Pattern:** `ItemCellGroupController` aggregates input events from multiple `GridCellUI` instances into a single `OnGroupInputAsObservable` stream. This solves the L-shape AABB problem by having discrete clickable cells instead of one large rectangular hitbox.
    - **MouseFilter Architecture:** Root and InteractionArea use `Ignore (2)` to be transparent to mouse, while GridCellUI children use `Pass (0)` to receive events. This allows L-shape holes to pass clicks through to the backpack grid underneath.
    - **Interface-Based Data Injection:** `IItemDataProvider` interface with `DataInitialized` event allows parent (TSItemWrapper) to inject data to child (GridShapeComponent) after both are ready, solving the _Ready() execution order issue.
    - **MVC Controller Concept:** `BackpackInteractionController` bridges `DraggableItemComponent` input with `BackpackGridComponent` backend. Maintain state via `Dictionary<Node, ItemDragState>`.
    - **Power Switch Pattern:** Used by `FollowMouseUIComponent`. Placement strictly under the `Dragging` AtomicState allows `AutoBindToParentState()` to natively handle activation/deactivation hooks (`state_entered`/`state_exited`) without explicit controller toggling.
    - **Micro-Interaction Tweens:** Inside `UITweenInteractComponent`, execute `_currentTween?.Kill()` before starting a new `AnimateToScale()`. Use `EaseType.Out` and `TransitionType.Sine` for easing math.
    - **Grid Visualization Anchor:** `BackpackGridUIComponent._Draw()` plots `(Width + 1)` vertical lines and `(Height + 1)` horizontal lines when `DrawDebugLines` is true, followed by `QueueRedraw()` on dependency update.
  </implementation_anchors>

  <critical_constraints>
    <constraint category="Godot Lifecycle (_EnterTree vs _Ready)">
      <rule>**CRITICAL:** Initialize all Subjects in `_EnterTree()`, NOT `_Ready()`.</rule>
      <rule>Godot executes `_EnterTree()` Top-Down (Parent → Child), but `_Ready()` Bottom-Up (Child → Parent).</rule>
      <rule>Parent: `public override void _EnterTree() { OnShapeChangedAsObservable = new Subject<Unit>(); }`</rule>
      <rule>Child: `public override void _Ready() { _parent.OnShapeChangedAsObservable.Subscribe(...).AddTo(this); }`</rule>
      <rule>NEVER use `CallDeferred` to work around lifecycle issues - use proper _EnterTree initialization.</rule>
      <rule>For cross-frame delays, use `await ToSignal(GetTree(), SceneTree.SignalName.ProcessFrame)` instead of CallDeferred.</rule>
    </constraint>
    
    <constraint category="MouseFilter Architecture (L-Shape AABB Solution)">
      <rule>**CRITICAL:** Root node (TetrisDraggableItem): `mouse_filter = 2` (Ignore).</rule>
      <rule>**CRITICAL:** InteractionArea: `mouse_filter = 2` (Ignore) - NEVER use Stop (1)!</rule>
      <rule>GridCellUI children: `mouse_filter = 0` (Pass) - receives mouse events.</rule>
      <rule>ItemIcon: `mouse_filter = 2` (Ignore) - decorative only.</rule>
      <rule>**Why Ignore on InteractionArea?** It's a rectangular AABB. Stop would block L-shape holes.</rule>
      <rule>Ignore makes InteractionArea transparent - mouse passes through to GridCellUI children.</rule>
      <rule>GridCellUI positioned at actual occupied cells - no holes, perfect hit detection.</rule>
    </constraint>
    
    <constraint category="R3 Subscription Order">
      <rule>**CRITICAL:** Call `AddChild(node)` BEFORE `.Subscribe().AddTo(node)`.</rule>
      <rule>R3 requires node to be in scene tree for disposal tracking.</rule>
      <rule>Calling `.AddTo()` before `AddChild()` throws "AddTo does not support to use before enter tree".</rule>
      <rule>Correct order: 1. `AddChild(gridCellUI);` 2. `gridCellUI.OnCellInputAsObservable.Subscribe(...).AddTo(gridCellUI);`</rule>
    </constraint>
    
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