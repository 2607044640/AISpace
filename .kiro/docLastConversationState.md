<last_conversation_state>
<metadata>
<update_date>2026-04-09</update_date>
<engine>Godot 4.6.1 stable mono</engine>
<language>C# only</language>
<project>3D character controller + Complete Grid Inventory System with Synergies</project>
<phase>Full backpack system with MVC, UI animations, and Backpack Battles-style synergies</phase>
</metadata>

<architecture_overview>
<system>9-layer complete inventory system with R3, StateChart, MVC, and synergy mechanics</system>
<layers>
1. Data Layer: BackpackGridComponent (1D array grid logic)
2. Resource Layer: ItemDataResource, SynergyDataResource (Godot Resources)
3. Shape Layer: GridShapeComponent (Runtime rotation with R3)
4. View Layer: BackpackGridUIComponent (Pixel ↔ Grid coordinate conversion)
5. Controller Layer: BackpackInteractionController (MVC drag state management)
6. Input Layer: DraggableItemComponent (GUI to StateChart bridge)
7. Physics Layer: FollowMouseUIComponent (Mouse tracking via Power Switch)
8. Animation Layer: UITweenInteractComponent (Micro-interactions with logic/visual separation)
9. Synergy Layer: SynergyComponent (Backpack Battles-style item synergies)
</layers>
</architecture_overview>

<file_inventory>
<components>
- BackpackGridComponent.cs (Data layer, 1D array grid)
- BackpackGridUIComponent.cs (View layer, coordinate converter)
- BackpackInteractionController.cs (Controller, drag state, pickup/drop/snap)
- ItemDataResource.cs (Item static config)
- GridShapeComponent.cs (Runtime shape + rotation)
- DraggableItemComponent.cs (Input handler)
- FollowMouseUIComponent.cs (Mouse follower)
- UITweenInteractComponent.cs (UI micro-interactions)
- SynergyDataResource.cs (Synergy config)
- SynergyComponent.cs (Synergy detection)
</components>
<documentation>
- KiroWorkingSpace/.kiro/steering/Godot/GodotBackpackSystem_Context.md (Complete technical reference)
</documentation>
</file_inventory>

<component_specifications>
<component name="BackpackGridComponent">
<type>Data Layer</type>
<state>ItemData[] _gridData (1D array, index = y * Width + x)</state>
<methods>CanPlaceItem(), TryPlaceItem(), RemoveItem(), GetItemAt(), ClearGrid()</methods>
<r3>OnItemPlacedAsObservable, OnItemRemovedAsObservable (Subject<(ItemData, Vector2I)>)</r3>
</component>

<component name="BackpackGridUIComponent">
<type>View Layer (Control)</type>
<exports>BackpackGridComponent LogicGrid, Vector2 CellSize (64x64), bool DrawDebugLines, Color GridColor</exports>
<methods>
- GlobalToGridPosition(Vector2): (globalPos - GlobalPosition) / CellSize → FloorToInt → Clamp
- GridToLocalPosition(Vector2I): gridPos * CellSize
- GetCellCenterPosition(Vector2I): GridToLocalPosition + CellSize/2
- LocalToGridPosition(Vector2): localPos / CellSize → FloorToInt → Clamp
- IsValidGridPosition(), GetCellRect(), GetShapeRect(), RefreshGrid()
</methods>
<auto_sizing>CustomMinimumSize = Size = (Width * CellSize.X, Height * CellSize.Y)</auto_sizing>
<visualization>_Draw() renders grid lines when DrawDebugLines=true</visualization>
</component>

<component name="BackpackInteractionController">
<type>Controller Layer (MVC)</type>
<exports>BackpackGridComponent LogicGrid, BackpackGridUIComponent ViewGrid</exports>
<state>Dictionary<Node, ItemDragState> (OriginalGlobalPos, OriginalGridPos, ShapeComponent, ItemControl)</state>
<methods>
- RegisterItem(Node): Subscribe to DraggableItemComponent events with .AddTo(itemEntity)
- HandleItemPickedUp(): Record state + LogicGrid.RemoveItem() (防自我占用)
- HandleItemDropped(): 
  * Get mouse: ViewGrid.GetGlobalMousePosition() (NOT GetViewport().GetMousePosition())
  * Check range: ViewGrid.GetGlobalRect().HasPoint(mousePos)
  * Try place: LogicGrid.TryPlaceItem()
  * Success: PerformSnapToGrid() (吸附: ViewGrid.GlobalPosition + ViewGrid.GridToLocalPosition(gridPos))
  * Failure: PerformBounceBack() (回弹: restore OriginalGlobalPos + force TryPlaceItem(OriginalGridPos))
- HandleItemRotated(): ShapeComponent.Rotate90()
</methods>
</component>

<component name="ItemDataResource">
<type>Resource Layer</type>
<exports>string ItemID, string ItemName, Texture2D Icon, Array<Vector2I> BaseShape</exports>
<default>BaseShape = { Vector2I.Zero }</default>
<methods>GetCellCount(), GetBoundingSize(), IsShapeValid()</methods>
</component>

<component name="GridShapeComponent">
<type>Shape Layer</type>
<state>Vector2I[] CurrentLocalCells</state>
<methods>
- Rotate90(): Apply (x,y) → (-y,x) + NormalizeShape()
- NormalizeShape(): Ensure min(X,Y) = 0
- ResetShape(), GetBoundingSize(), ContainsCell(), GetCenter()
</methods>
<r3>OnShapeChangedAsObservable (Subject<Unit>)</r3>
</component>

<component name="DraggableItemComponent">
<type>Input Layer</type>
<exports>Control ClickableArea, Node StateChart</exports>
<events>
- Left Press: StateChart.Call("send_event", "drag_start") + OnDragStartedAsObservable.OnNext(Unit.Default)
- Left Release: StateChart.Call("send_event", "drag_end") + OnDragEndedAsObservable.OnNext(Unit.Default)
- Right Press: OnRotateRequestedAsObservable.OnNext(Unit.Default)
</events>
<cleanup>Unsubscribe GuiInput in _ExitTree()</cleanup>
</component>

<component name="FollowMouseUIComponent">
<type>Physics Layer</type>
<exports>Control TargetUI, Vector2 GrabOffset</exports>
<lifecycle>
- AutoBindToParentState() in _Ready() (Power Switch)
- state_entered: ZIndex +100
- state_exited: Restore original ZIndex
- _Process(): TargetUI.GlobalPosition = GetGlobalMousePosition() + GrabOffset
</lifecycle>
<placement>MUST be child of Dragging AtomicState</placement>
</component>

<component name="UITweenInteractComponent">
<type>Animation Layer</type>
<exports>Control InteractionArea, Control VisualTarget, Vector2 HoverScale (1.05), Vector2 PressScale (0.95), float TweenDuration (0.15)</exports>
<principle>Logic/Visual Separation: InteractionArea (Scale=1,1, 坐标计算) + VisualTarget (可缩放, 视觉反馈)</principle>
<states>Normal(1,1) → Hover(1.05) → Press(0.95)</states>
<animation>
- Kill current tween: _currentTween?.Kill()
- Create: GetTree().CreateTween()
- Configure: SetEase(EaseType.Out), SetTrans(TransitionType.Sine)
- Animate: TweenProperty(VisualTarget, "scale", targetScale, TweenDuration)
- PivotOffset: VisualTarget.Size / 2 (中心缩放)
</animation>
</component>

<component name="SynergyDataResource">
<type>Resource Layer</type>
<exports>string[] ProvidedTags, Array<Vector2I> StarOffsets, string RequiredTag, string SynergyEffect</exports>
<example>
- ProvidedTags: ["Food", "Fruit"]
- StarOffsets: [(1,0), (-1,0)]
- RequiredTag: "Food"
- SynergyEffect: "每颗星星 +10% 攻击速度"
</example>
<methods>HasTag(), GetStarCount(), IsValid()</methods>
</component>

<component name="SynergyComponent">
<type>Synergy Layer</type>
<exports>SynergyDataResource SynergyData, GridShapeComponent Shape</exports>
<state>HashSet<Vector2I> ActiveStars, int _rotationCount (0-3)</state>
<r3>OnSynergyChangedAsObservable (Subject<HashSet<Vector2I>>)</r3>
<rotation_tracking>Subscribe to Shape.OnShapeChangedAsObservable → _rotationCount++</rotation_tracking>
<methods>
- CheckSynergies(BackpackGridComponent, Vector2I):
  1. Clear ActiveStars
  2. Foreach StarOffset: Apply rotation → Calculate world pos → Query item → Check tag → Update ActiveStars
  3. Emit OnSynergyChangedAsObservable
- ApplyRotationToOffset(Vector2I, int): Loop apply (x,y) → (-y,x) for rotationCount times
</methods>
</component>
</component_specifications>

<scene_structure>
```
BackpackPanel (BackpackGridUIComponent)
├── BackpackInteractionController
├── BackpackGridComponent (LogicGrid)
└── Items Container
    └── ItemEntity (Control) ← InteractionArea [Scale=1,1]
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
        └── VisualContainer (Control) ← VisualTarget [Scale可变]
            ├── ItemIcon (TextureRect)
            └── StarContainer (Control)
                ├── Star1 (TextureRect) ← 灰色/亮色切换
                └── Star2 (TextureRect)
```
</scene_structure>

<critical_fixes>
<fix>BackpackInteractionController: Use ViewGrid.GetGlobalMousePosition() NOT GetViewport().GetMousePosition() (handles Camera2D/CanvasLayer transforms)</fix>
<fix>DraggableItemComponent: Use StateChart.Call() directly, NOT GetParent()?.Call()</fix>
<fix>UITweenInteractComponent: NEVER scale InteractionArea (破坏坐标系统), only scale VisualTarget</fix>
</critical_fixes>

<design_decisions>
<decision topic="1D Array">Cache-friendly, simplified indexing (y*Width+x), easier serialization</decision>
<decision topic="Rotation Matrix">Discrete 90° rotations (x,y→-y,x) eliminate float errors, instant integer coords</decision>
<decision topic="MVC Controller">Centralized drag state management, prevents scattered logic, enables easy testing</decision>
<decision topic="Logic/Visual Separation">InteractionArea maintains stable coordinates for grid calculations, VisualTarget provides animations without affecting layout</decision>
<decision topic="Synergy Rotation Tracking">Subscribe to Shape changes to auto-update rotation count, ensures star positions always match item orientation</decision>
<decision topic="R3 Subject<Unit>">Parameterless events for pure notification, subscribers query current state directly</decision>
</design_decisions>

<build_status>
<status>Compiled successful</status>
<warnings>5 warnings (PhantomCamera nullability, unused events)</warnings>
</build_status>

<next_session_tasks>
<immediate>
1. Implement SynergyComponent.CheckItemHasTag() (requires ItemData → Node mapping)
2. Create item visual prefab scene with proper node structure
3. Build backpack UI scene with BackpackGridUIComponent
4. Create test ItemDataResource and SynergyDataResource .tres files
5. Test complete drag-drop-rotate-synergy workflow
</immediate>
<integration>
1. Implement ItemData → Node mapping in BackpackInteractionController
2. Add synergy visual feedback (star color changes)
3. Implement synergy effect application system
4. Add drag preview with placement validation (green/red highlight)
</integration>
<polish>
1. Add sound effects (pickup, drop, rotate, synergy activate)
2. Implement smooth snap animation with Tween
3. Add particle effects for synergy activation
4. Implement auto-sort functionality
5. Add item tooltips with synergy info
</polish>
<start_procedure>
1. Read this file + GodotBackpackSystem_Context.md
2. Review scene structure requirements
3. Create item prefab with all components
4. Test in isolation before integration
</start_procedure>
</next_session_tasks>
</last_conversation_state>
