<godot_project_rules>

<file_management>
Store ALL architecture rules, steering files, and instructions exclusively in KiroWorkingSpace/.kiro/
</file_management>

<context>
Godot 4.6.1 Mono (C#), 3D character controller, Complete grid inventory system with MVC, UI animations, and Backpack Battles-style synergies. Component architecture (Godot.Composition), R3 reactive framework, StateChart integration.
</context>

<grid_inventory_system>
<location>3d-practice/B1Scripts/Components/, 3d-practice/B1Scripts/Controllers/, 3d-practice/B1Scripts/Resources/</location>
<reference>KiroWorkingSpace/.kiro/steering/Godot/GodotBackpackSystem_Context.md</reference>
<architecture_layers>
1. Data Layer: BackpackGridComponent (1D array logic)
2. Resource Layer: ItemDataResource, SynergyDataResource (Static configs)
3. Shape Layer: GridShapeComponent (Runtime shape/rotation)
4. View Layer: BackpackGridUIComponent (Coordinate conversion)
5. Controller Layer: BackpackInteractionController (MVC drag state)
6. Input Layer: DraggableItemComponent (GUI to StateChart bridge)
7. Physics Layer: FollowMouseUIComponent (Mouse tracking)
8. Animation Layer: UITweenInteractComponent (Micro-interactions)
9. Synergy Layer: SynergyComponent (Item synergies)
</architecture_layers>

<mandatory_directives>
**Grid Logic:**
- MUST use 1D array: ItemData[] _gridData
- MUST use formula: index = y * Width + x
- MUST validate bounds before array access
- MUST clear cells when removing items

**Shape Management:**
- MUST call NormalizeShape() after rotation
- MUST use rotation matrix: (x,y) → (-y,x) for clockwise 90°
- MUST convert Godot.Collections.Array<Vector2I> to Vector2I[] for runtime

**Coordinate Conversion:**
- MUST use ViewGrid.GetGlobalMousePosition() (NOT GetViewport().GetMousePosition())
- MUST route all conversions through BackpackGridUIComponent
- MUST use Mathf.FloorToInt() for pixel-to-grid conversion
- MUST clamp grid coordinates to [0, Width) x [0, Height)

**MVC Controller:**
- MUST maintain drag state in Dictionary<Node, ItemDragState>
- MUST record original position before pickup
- MUST remove item from grid on pickup (防自我占用)
- MUST check mouse in backpack range before placement
- MUST snap to grid on success: ViewGrid.GlobalPosition + ViewGrid.GridToLocalPosition(gridPos)
- MUST bounce back on failure: restore OriginalGlobalPos + force TryPlaceItem(OriginalGridPos)

**UI Animation (Logic/Visual Separation):**
- MUST separate InteractionArea (Scale=1,1) and VisualTarget (可缩放)
- NEVER scale InteractionArea (破坏坐标系统)
- MUST set PivotOffset = Size/2 for center-based scaling
- MUST kill current tween before starting new animation
- MUST use EaseType.Out + TransitionType.Sine

**Synergy System:**
- MUST track rotation count via Shape.OnShapeChangedAsObservable
- MUST apply rotation to StarOffsets: loop (x,y) → (-y,x) for rotationCount times
- MUST query grid at currentGridPos + rotatedOffset
- MUST check ProvidedTags contains RequiredTag
- MUST emit OnSynergyChangedAsObservable after each check

**StateChart Communication:**
- MUST use StateChart.Call("send_event", "event_name")
- NEVER use GetParent()?.Call() when StateChart reference exists
- MUST verify StateChart reference before calling

**Power Switch Pattern:**
- MUST call AutoBindToParentState() in components under AtomicState
- MUST NOT manually call SetProcess() after AutoBind
- MUST connect state_entered/state_exited for custom logic (e.g., ZIndex)
- MUST save original state before modification

**R3 Integration:**
- MUST use Subject<Unit> for parameterless events
- MUST call OnNext(Unit.Default) to emit events
- MUST dispose all Subjects in _ExitTree()
- MUST use .AddTo(itemEntity) when subscribing to item events
</mandatory_directives>
</grid_inventory_system>

<r3_reactive_framework>
<packages>R3, R3.Godot (Cysharp)</packages>
<mandatory_rules>
1. DisposeBag: Initialize CompositeDisposable _disposables in every UI/Component class
2. AddTo: Append .AddTo(_disposables) to EVERY .Subscribe() chain
3. Dispose: Call _disposables.Dispose() in _ExitTree()
4. Thread Safety: Use ObserveOn(GodotProvider.MainThread) after async operations
5. Performance: Add DistinctUntilChanged() to prevent redundant updates
6. Debounce: Use ThrottleFirst on buttons, Debounce on search inputs
</mandatory_rules>
<extensions>
- OnPressedAsObservable(), OnToggledAsObservable(), OnValueChangedAsObservable()
- OnTextChangedAsObservable(), OnItemSelectedAsObservable()
- Observable.EveryUpdate(), Observable.EveryPhysicsUpdate()
</extensions>
</r3_reactive_framework>

<ui_component_helpers>
<location>3d-practice/addons/A1MyAddon/Helpers/</location>
<components>SliderComponentHelper, OptionComponentHelper, ToggleComponentHelper, DropdownComponentHelper</components>
<directives>
- Apply [Tool] and [GlobalClass] attributes
- Execute immediate UI updates in property setters
- Expose all configs via [Export]
- Emit C# events: event Action<T>, event Action ResetRequested
- Subscribe to signals in _Ready() if !Engine.IsEditorHint()
- Unsubscribe in _ExitTree()
</directives>
</ui_component_helpers>

<statechart_pattern>
<directives>
- Position components as children of AtomicState nodes
- Invoke this.AutoBindToParentState() in _Ready()
- Delegate lifecycle to StateChart via SetProcess()
- Request transitions via parent.SendStateEvent("event_name")
- Resolve entities via this.GetEntity<T>()
</directives>
</statechart_pattern>

<component_architecture>
<directives>
- Mark entities with [Entity], call InitializeEntity() in _Ready(), keep logic-free
- Mark components with [Component(typeof(T))], call InitializeComponent() in _Ready()
- Subscribe events in _Ready(), unsubscribe in _ExitTree()
- Locate components via GetRequiredComponentInChildren<T>()
- Couple to abstract base classes (BaseInputComponent), not concrete implementations
</directives>
</component_architecture>

<animation_system>
<location>CharacterAnimationConfig.cs</location>
<directives>
- Map animations as public string constants (AnimationNames)
- Register via RegisterAnim(library, AnimationNames.Name, AnimationResource, Speed, isLoop)
</directives>
</animation_system>

<core_components>
<location>3d-practice/addons/A1MyAddon/CoreComponents/</location>
<components>
GroundMovementComponent, FlyMovementComponent, PlayerInputComponent, BaseInputComponent, 
CharacterRotationComponent, AnimationControllerComponent, CameraControlComponent
</components>
</core_components>

<prohibitions>
- NEVER implement internal state checks (if (_canMove)) inside components
- NEVER query sibling nodes via GetNode()
- NEVER use hardcoded strings for animation playback
- NEVER define Godot [Signal] in C#; use C# events
- NEVER leave R3 subscriptions unbounded
- NEVER execute grid coordinate math in business logic
- NEVER construct grids using 2D arrays (ItemData[,])
- NEVER scale InteractionArea in UI animations
- NEVER use GetViewport().GetMousePosition() for backpack interactions
</prohibitions>

<build_and_debug>
<directives>
- Execute: dotnet build (from 3d-practice root)
- Audit logs: Get-Content "$env:APPDATA\Godot\app_userdata\3dPractice\logs\godot.log" -Tail 50
- C# logging: GD.Print(), GD.PrintErr(), GD.PushWarning()
- Bypass Godot.Composition limitations: GetRequiredComponentInChildren<BaseInputComponent>()
- Assign fallback animations in Godot Editor for missing sequences
</directives>
</build_and_debug>

<scene_structure_requirements>
**Backpack Panel:**
- Root: BackpackGridUIComponent (Control)
- Children: BackpackInteractionController, BackpackGridComponent, Items Container

**Item Entity:**
- Root: Control (InteractionArea, Scale=1,1)
- Children: StateChart, DraggableItemComponent, GridShapeComponent, SynergyComponent, UITweenInteractComponent, VisualContainer
- VisualContainer: Control (VisualTarget, Scale可变)
  - Children: ItemIcon (TextureRect), StarContainer (Control with Star TextureRects)

**StateChart Structure:**
- Root (CompoundState, initial="Idle")
  - Idle (AtomicState) → Transition: "drag_start" → Dragging
  - Dragging (AtomicState) → FollowMouseUIComponent + Transition: "drag_end" → Idle
</scene_structure_requirements>

</godot_project_rules>
