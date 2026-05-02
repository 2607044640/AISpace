---
trigger: manual
---

<context>
**Tesseract Backpack (TS)** - Grid-based inventory system with drag-and-drop, rotation, StateChart integration, and Backpack Battles-style synergy system. Supports arbitrary item shapes (Tetris-like) with reactive event streams (R3), MVC architecture, and UI micro-interactions.

**Latest Architecture (2026-05-02):**
- **Polygon Merging (Ghost Collision Fix):** `ItemPhysicsComponent` uses `Geometry2D.MergePolygons` (with a 0.5px overlap) to seamlessly fuse multiple grid cells into a single `CollisionPolygon2D`. This eliminates "ghost collisions" where items snagged on internal seams between grid cells.
- **Continuous Collision Detection (CCD):** Physics proxies use `ContinuousCd = CcdMode.CastRay` to prevent high-speed tunneling through the floor when spawned overlapping.
- **Physics-State Authority:** Controller relies on `ItemPhysicsComponent.Freeze` to determine if an item is grabbed from the logic grid or caught mid-air. World-drops preserve their `GlobalPosition` and hand off seamlessly to the physics engine.
- **Out-of-Bounds Respawn Logic:** `LootSpawnAreaController` directly updates the `TopLevel` RigidBody's position and zeros out `LinearVelocity` instead of just moving the UI Control. Supports dynamic `RespawnPointPath` (e.g., `../Fallenpoint`).
- **Normalization Shift Compensation:** `ItemPhysicsComponent` calculates the visual offset caused by `GridShapeComponent.NormalizeShape()` during a physical rotation and applies an inverse shift to the parent `Control`'s `GlobalPosition`, eliminating pixel jumping when picking up rotated items.
- **TopLevel Physics Proxy:** The `RigidBody2D` physics proxy MUST set `TopLevel = true` to break the Godot spatial inheritance chain. This prevents the "death spiral" feedback loop (infinite acceleration) when `_PhysicsProcess` synchronizes coordinates with its parent `Control`.
- **Backpack-Physics Decoupling:** Items inside the backpack set `CollisionLayer/Mask = 0` (NONE) and `Freeze = true`. This prevents them from acting as physical obstacles that could deflect dragged items or interfere with other loot. They only restore `CollisionLayer/Mask = 16` (ITEM_LAYER) and `Freeze = false` when taken out or spawned in the world.
- **Commander Pattern:** Controller delegates spatial math to the View and visual tweens to the Juice component. Result: Declarative logic, zero visual noise in Controller.
- **Spatial Delegation:** `BackpackGridUIComponent` handles all coordinate mapping (`IsPointInside`, `GridToGlobalPosition`). `GridShapeComponent` handles local shape lookups (`GetCellIndexAtLocalPosition`).
- **Juice Delegation:** `UITweenInteractComponent` encapsulates the complex Counter-Transform rotation animation (`PlayRotationAnimation`).
- **Pure Math Decoupling:** Grid mapping uses `mouseGridPos - GetGrabbedCellLogicalOffset()`. Immune to pixel warp or visual UI transforms.
- **Anchor Stability:** `GrabbedCellIndex` pre-calculated at pick-up. Ensures a consistent logical pivot point even across multiple rotations.
- **Focus Preservation:** Node reuse in `GridShapeUIComponent` prevents losing Godot mouse capture during rotation-induced cell rebuilding.
</context>

<layer_1_quick_start>
  <quick_reference>
    - **Project Prefix:** TS (Tesseract)
    - **Rule Storage:** Store ALL rules in `AISpace/`.
    - **Addon Root (Legacy):** `TetrisBackpack/addons/A1TetrisBackpack/` (旧代码库)
    - **New Project Root:** `TetrisBackpack/A1TesseractBackpack/` (新场景和资源)
    - **Scene Naming:** All scene files use `TS` prefix (e.g., `TSItem.tscn`)
    - **Core Path:** `TetrisBackpack/addons/A1TetrisBackpack/Core/` (BackpackGridComponent, BackpackInteractionController, BackpackGridUIComponent)
    - **Items Path:** `TetrisBackpack/addons/A1TetrisBackpack/Items/` (ItemDataResource, GridShapeComponent, GridShapeUIComponent, IItemDataProvider)
    - **UI Path:** `TetrisBackpack/addons/A1TetrisBackpack/UI/` (GridCellUI - Panel-based cell component)
    - **Interaction Path:** `TetrisBackpack/addons/A1TetrisBackpack/Interaction/` (DraggableItemComponent, FollowMouseUIComponent)
    - **Synergies Path:** `TetrisBackpack/addons/A1TetrisBackpack/Synergies/` (SynergyDataResource, SynergyComponent)
    - **MicroUI Path:** `TetrisBackpack/addons/A1TetrisBackpack/MicroUI/` (UITweenInteractComponent)
    - **Core Dependencies:** R3 (Cysharp) for reactive streams, GodotStateCharts for state management.
  </quick_reference>

  <decision_tree>
    - **If handling item pickup:** Record original state + call `LogicGrid.RemoveItem()`. (Why: Prevents the item from occupying its own space during dragging).
    - **If handling item drop:** Check `ViewGrid.GetGlobalRect().HasPoint(mousePos)`. (Why: Ensures placement only occurs within the valid backpack boundaries).
    - **If TryPlaceItem() succeeds:** Execute `PerformSnapToGrid()`. (Why: Aligns the visual item perfectly with the underlying logic grid).
    - **If TryPlaceItem() fails:** Execute `PerformBounceBack()`. (Why: Restores the item to its `OriginalGlobalPos` and re-registers it at `OriginalGridPos`).
  </decision_tree>

  <minimal_workflow>
    1. `BackpackInteractionController._Ready()` registers items and subscribes to R3 streams (`DragStart`, `DragEnd`, `Rotate`).
    2. Left press → `HandleItemPickedUp()`: records state, calls `LogicGrid.RemoveItem()`, and **pre-calculates `GrabbedCellIndex`** (Stable Anchor).
    3. **R3 Preview Stream (Merged):** `Merge(posStream, shapeStream)` select `mouseGridPos - GetGrabbedCellLogicalOffset()` (Pure Math) → `EvaluatePlacementPreview` → `ShowPreview`.
    4. Right click during drag → `HandleItemRotated()` (Commander Style):
       - `shapeComp.Rotate90()` (Logic Order)
       - `followComp.GrabOffset = -newPivot` (Anchor Order)
       - `tweenComp.PlayRotationAnimation(node, newPivot)` (Visual Order — Counter-Transform logic is hidden inside).
    5. Left release → `HandleItemDropped()`: uses `targetGridPos = mouseGridPos - GetGrabbedCellLogicalOffset()` → `TryPlaceItem()` → snap or bounce-back.
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
    - **NEVER use `_Process` for preview/highlight updates.** (Why: Runs every frame even when idle. Use R3 `EveryUpdate + DistinctUntilChanged + TakeUntil` which fires only on grid-boundary crossings and auto-disposes).
    - **NEVER use `Dictionary<Node, T>` for drag state.** (Why: Over-engineering. Player has one mouse → one drag at a time. Use single `ItemDragState _currentDrag` field).
    - **NEVER use `mouse_entered`/`mouse_exited` for grid highlight.** (Why: Signal order is unreliable on fast drags causing ghost-glow bugs. Use math-mapped `GlobalToGridPosition()` in an R3 stream instead).
    - **NEVER overwrite GlobalPosition on drop for world items.** (Why: Reverting `GlobalPosition` destroys the `FollowMouseUIComponent` grab offset. For world drops, just call `EnablePhysics()` and let the engine take over).
    - **NEVER leave RigidBody2D to inherit Control transforms if syncing.** (Why: If `_PhysicsProcess` syncs RB to Control, and RB is a child of Control, a death-spiral positive feedback loop occurs. Always set `TopLevel = true` on the RigidBody2D proxy).
  </top_anti_patterns>
</layer_1_quick_start>

<layer_2_detailed_guide>
  <api_reference>
    | Class | Methods/Properties | Parameters / Types |
    | :--- | :--- | :--- |
    | `BackpackGridComponent` | `CanPlaceItem`, `TryPlaceItem`, `RemoveItem`, `GetItemAt`, `ClearGrid`, `EvaluatePlacementPreview` | `ItemData[] _gridData`, `OnItemPlacedAsObservable`, `OnItemRemovedAsObservable`. `EvaluatePlacementPreview(Vector2I[] shape, Vector2I targetPos)` returns `List<(Vector2I GridPos, CellState State)>` — no short-circuit, evaluates every cell |
    | `BackpackGridUIComponent` | `IsPointInside`, `GetCellCenterLocalPos`, `GlobalToGridPosition`, `GridToLocalPosition`, `LocalToGridPosition`, `IsValidGridPosition`, `RefreshGrid`, `ShowPreview`, `ClearPreview` | `[GlobalClass]`. `IsPointInside(global)` replaces manual Rect checks. `GetCellCenterLocalPos` handles cell-center pixel math. |
    | `BackpackInteractionController` | `RegisterItem`, `GetGrabbedCellLogicalOffset`, `IsItemBeingDragged` | **Commander Role**: orchestrates R3 streams and delegates math/visuals to GridUI/Juice components. |
    | `ItemPhysicsComponent` | `EnablePhysics`, `DisablePhysics`, `ITEM_LAYER`, `NONE` | `TopLevel = true`. Bridges `RigidBody2D` with UI `Control`. Implements Inverse Normalization Shift compensation. Toggles `CollisionLayer/Mask` (16 vs 0) to prevent backpack interference. |
    | `UITweenInteractComponent` | `PlayRotationAnimation`, `AnimateToScale`, `UpdatePivotOffset` | **Juice Component**: Encapsulates all Tween logic and Counter-Transform visual compensation. |
    | `ItemDataResource` | `GetCellCount`, `GetBoundingSize`, `IsShapeValid` | `ItemID`, `ItemName`, `Icon`, `BaseShape` (Array<Vector2I>) |
    | `GridShapeComponent` | `Rotate90`, `NormalizeShape` | `Vector2I[] CurrentLocalCells`, `OnShapeChangedAsObservable` (initialized in `_EnterTree()`) |
    | `IItemDataProvider` | `DataInitialized` event | Interface for parent-to-child data injection (solves _Ready() lifecycle issue) |
    | `GridCellUI` | `SetState`, `OnCellInputAsObservable`, `OnCellHoverAsObservable`, `MouseEntered`, `MouseExited` | Panel-based cell with StyleBoxFlat, states: Normal/Hover/Valid/Invalid |
    | `GridShapeUIComponent` | `SetGroupState`, `ResetGroupState`, `OnGroupInputAsObservable`, `UpdateCellsVisualState` | **View layer** for `GridShapeComponent`. Drives `GridCellUI` instances. Aggregates input events. Handles hover state. |
    | `DraggableItemComponent` | `GuiInput` event handlers | `Control ClickableArea`, `Node StateChart`, `OnDragStartedAsObservable`, `OnDragEndedAsObservable`, `OnRotateRequestedAsObservable` (all initialized in `_EnterTree()`) |
    | `FollowMouseUIComponent` | `AutoBindToParentState`, `OnDragStateEntered`, `OnDragStateExited` | `Control TargetUI`, `Vector2 GrabOffset` |
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
          * GridShapeUIComponent (subscribes in _Ready, generates GridCellUI)
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
    
    *Lifecycle Order (CRITICAL):*
    * `_EnterTree()`: Top-Down (Parent → Child) - Parent initializes all Subjects here.
    * `_Ready()`: Bottom-Up (Child → Parent) - Children subscribe to parent Subjects.
    
    *Placement Preview Stream (R3 — 2026-04-27):*
    ```
    OnDragStarted
      → HandleItemPickedUp() [records _currentDrag, removes from LogicGrid]
      → Observable.EveryUpdate()
          .Select(_ => ViewGrid.GetGlobalMousePosition())
          .Select(mousePos => (inBounds: ViewGrid.IsPointInside(mousePos), gridPos: ViewGrid.GlobalToGridPosition(mousePos)))
          .DistinctUntilChanged()
          .TakeUntil(OnDragEndedAsObservable)
          .Subscribe(state => { ... })
          .AddTo(itemEntity)
    ```
  </technical_specifications>

  <core_rules>
    <rule>
      <description>**CRITICAL: Initialize all Subjects in `_EnterTree()`, NOT `_Ready()`.**</description>
      <rationale>Godot executes `_EnterTree()` Top-Down (Parent before Child), but `_Ready()` Bottom-Up (Child before Parent).</rationale>
      <enforcement>
        1. Parent: `public override void _EnterTree() { OnShapeChangedAsObservable = new Subject<Unit>(); }`
        2. Child: `public override void _Ready() { _parent.OnShapeChangedAsObservable.Subscribe(...); }`
      </enforcement>
    </rule>
    <rule>
      <description>**CRITICAL: Set InteractionArea MouseFilter to Ignore (2), NEVER Stop (1).**</description>
      <rationale>InteractionArea is a rectangular AABB container. Setting to Stop blocks mouse events on L-shape holes.</rationale>
      <enforcement>
        1. Root Node: `mouse_filter = 2` (Ignore)
        2. InteractionArea: `mouse_filter = 2` (Ignore)
        3. GridCellUI children: `mouse_filter = 0` (Pass)
      </enforcement>
    </rule>
    <rule>
      <description>**CRITICAL: Call `AddChild()` BEFORE `.Subscribe().AddTo()`.**</description>
      <rationale>R3's `.AddTo()` requires the node to be in the scene tree for disposal tracking.</rationale>
      <enforcement>
        1. `AddChild(gridCellUI);`
        2. `gridCellUI.OnCellInputAsObservable.Subscribe(...).AddTo(gridCellUI);`
      </enforcement>
    </rule>
  </core_rules>
</layer_2_detailed_guide>

<layer_3_advanced>
  <troubleshooting>
    <error symptom="NullReferenceException when child tries to subscribe to parent Subject">
      <cause>Parent initialized Subject in `_Ready()`, but child's `_Ready()` executes first.</cause>
      <fix>Move Subject initialization to parent's `_EnterTree()`.</fix>
    </error>
    <error symptom="'AddTo does not support to use before enter tree' error">
      <cause>Called `.Subscribe().AddTo(node)` before `AddChild(node)`.</cause>
      <fix>Always call `AddChild()` first.</fix>
    </error>
    <error symptom="L-shape item blocks clicks on empty holes">
      <cause>InteractionArea MouseFilter set to Stop (1).</cause>
      <fix>Set InteractionArea `mouse_filter = 2` (Ignore).</fix>
    </error>
    <error symptom="Item drop not detected after rotation">
      <cause>Rotation triggers `QueueFree()` on the node capturing mouse focus.</cause>
      <fix>Use node reuse in `GridShapeUIComponent` when rebuilding visuals.</fix>
    </error>
    <error symptom="Item jump during rotation">
      <cause>Lack of Counter-Transform visual compensation.</cause>
      <fix>Use `UITweenInteractComponent.PlayRotationAnimation()` to smoothly tween visuals while logic updates instantly.</fix>
    </error>
    <error symptom="Item teleports/jumps when picked up after falling">
      <cause>Physical rotation around origin vs GridShape normalization shift.</cause>
      <fix>In `DisablePhysics()`, calculate the local shift caused by `NormalizeShape` and apply an inverse offset to the host Control's `GlobalPosition`.</fix>
    </error>
    <error symptom="Item accelerates infinitely/bounces wildly on floor">
      <cause>Positive feedback loop between `_PhysicsProcess` setting parent position and child RigidBody inheriting that transform.</cause>
      <fix>Set `TopLevel = true` on the `RigidBody2D` to break the inheritance chain.</fix>
    </error>
    <error symptom="Item continuously respawns out of bounds (infinite falling loop)">
      <cause>Respawn code teleported the UI Control but ignored the `TopLevel` RigidBody, keeping its extreme falling velocity and position intact.</cause>
      <fix>In `LootSpawnAreaController`, directly set the `ItemPhysicsComponent.GlobalPosition` and zero out its `LinearVelocity` and `AngularVelocity`.</fix>
    </error>
    <error symptom="Items sliding against each other suddenly get stuck/snag on invisible edges">
      <cause>"Ghost collisions" caused by internal seams when a RigidBody is composed of multiple adjacent `CollisionShape2D` rectangles.</cause>
      <fix>Use `Geometry2D.MergePolygons` to combine the individual grid cells into a single, seamless `CollisionPolygon2D`.</fix>
    </error>
    <error symptom="Items spawned in the same location fall completely through the floor">
      <cause>Initial overlap creates extreme repulsion force, causing tunneling (passing through floor in a single frame).</cause>
      <fix>Enable Continuous Collision Detection (`ContinuousCd = CcdMode.CastRay`) on the RigidBody2D.</fix>
    </error>
  </troubleshooting>

  <implementation_anchors>
    - **R3 Placement Preview Stream Pattern:** `Merge(posStream, shapeStream)` ensures previews update on both move and rotate. Use **Pure Math Mapping** (`mouseGridPos - GetGrabbedCellLogicalOffset()`) to decouple logic from visual transforms. `DistinctUntilChanged` filters sub-cell jitter.
    - **Commander Pattern (Refinement):** Controller delegates spatial math to `ViewGrid.IsPointInside()` and visual juicing to `TweenComp.PlayRotationAnimation()`. Controller only sends high-level instructions: Rotate → Sync → Animate.
    - **Juice Delegation Pattern:** All Tween logic (Scaling, Counter-Transform Rotation) is moved to `UITweenInteractComponent`. Controller remains clean of implementation details like `TweenDuration` or `EaseType`.
    - **Spatial Delegation Pattern:** All coordinate-aware math (Pixel-to-Grid, Grid-to-Center, Boundary Checks) is moved to `BackpackGridUIComponent`. Controller treats the grid as a pure logical service.
    - **Anchor Stability Pattern:** Pre-calculate `GrabbedCellIndex` at pick-up. This persistent logical index ensures the item rotates around the exact cell the player grabbed, regardless of orientation changes.
    - **Node Reuse Pattern (Focus Preservation):** When updating item visuals during interaction (e.g., rotation), reuse existing `GridCellUI` nodes if the count is identical. Only update their `Position`. This prevents losing Godot mouse capture/focus, which would otherwise suppress the 'mouse release' event.
    - **Interface-Based Data Injection:** `IItemDataProvider` interface with `DataInitialized` event allows parent (TSItemWrapper) to inject data to child (GridShapeComponent) after both are ready.
    - **MVC Controller Concept:** `BackpackInteractionController` bridges `DraggableItemComponent` input with `BackpackGridComponent` backend. Auto-registers items from `ItemsContainerPath` in `_Ready()`.
    - **Power Switch Pattern:** Used by `FollowMouseUIComponent`. Placement strictly under the `Dragging` AtomicState allows `AutoBindToParentState()` to natively handle activation/deactivation hooks.
    - **Micro-Interaction Tweens:** Inside `UITweenInteractComponent`, execute `_currentTween?.Kill()` before starting a new `AnimateToScale()`.
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
    
    <constraint category="Physics & UI Integration">
      <rule>**CRITICAL:** Set `TopLevel = true` on `RigidBody2D` if it's a child of a `Control` and synchronizes its position back to the parent to prevent death-spiral feedback loops.</rule>
      <rule>**CRITICAL:** When transitioning from Physics Rotation to Logic Grid Rotation, calculate the shift caused by `GridShapeComponent.NormalizeShape()` and apply an inverse offset to `GlobalPosition` to prevent visual jumping.</rule>
      <rule>Use `RigidBody2D.Freeze` state as the single source of truth for whether an item was grabbed from the logical grid or caught in mid-air.</rule>
      <rule>In `_Process` (drag), force Physics to follow UI. In `_PhysicsProcess` (fall), force UI to follow Physics.</rule>
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
      <rule>**CRITICAL:** Reuse `GridCellUI` nodes in `GridShapeUIComponent` if cell count is unchanged.</rule>
      <rule>NEVER call `QueueFree()` on the node capturing mouse focus during a drag operation.</rule>
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