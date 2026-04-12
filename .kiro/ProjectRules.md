<layer_1_quick_start>
  <quick_reference>
    - **Rule/Arch Storage**: `KiroWorkingSpace/.kiro/` (ALL steering/instruction files).
    - **Build Command**: `dotnet build` (Execute from 3d-practice root).
    - **Log Audit**: `Get-Content "$env:APPDATA\Godot\app_userdata\Tesseract_Backpack\logs\godot.log" -Tail 50`.
  </quick_reference>

  <architecture_layers>
    1. **Data Layer**: BackpackGridComponent (1D array logic: `ItemData[] _gridData`, formula: `index = y * Width + x`)
    2. **Resource Layer**: ItemDataResource, SynergyDataResource (Static configuration data)
    3. **Shape Layer**: GridShapeComponent (Runtime shape/rotation management)
    4. **View Layer**: BackpackGridUIComponent (Coordinate conversion between screen/grid space)
    5. **Controller Layer**: BackpackInteractionController (MVC drag state management)
    6. **Input Layer**: DraggableItemComponent (GUI input to StateChart bridge)
    7. **Physics Layer**: FollowMouseUIComponent (Mouse position tracking)
    8. **Animation Layer**: UITweenInteractComponent (Micro-interactions and visual feedback)
    9. **Synergy Layer**: SynergyComponent (Item synergy detection and management)
  </architecture_layers>

  <decision_tree>
    - **Grid Data Modeling**: MUST use 1D Arrays (`ItemData[]`). (Why: Ensures contiguous memory allocation and aligns with BackpackGridComponent architecture).
    - **Mouse Coordinate Resolution**: MUST use `ViewGrid.GetGlobalMousePosition()`. (Why: Isolates coordinate logic from Viewport scaling aberrations).
    - **Component Inter-Communication**: MUST use C# Events (`event Action<T>`) and R3 Observables. (Why: Godot `[Signal]` is strictly prohibited in C# architecture).
  </decision_tree>

  <end_to_end_example>
    <![CDATA[
    // Core Entity-Component initialization with StateChart & R3 binding
    [GlobalClass, Component(typeof(DraggableItemComponent))]
    public partial class DraggableItemComponent : BaseInputComponent 
    {
        private CompositeDisposable _disposables = new();

        public override void _Ready() 
        {
            this.AutoBindToParentState(); // Bind to StateChart AtomicState
            
            // Map R3 subscription to lifecycle
            Observable.EveryUpdate()
                .ObserveOn(GodotProvider.MainThread)
                .Subscribe(_ => ProcessDragState())
                .AddTo(_disposables);
        }

        public override void _ExitTree() 
        {
            _disposables.Dispose(); // Prevent memory leaks
        }
    }
    // Validation: dotnet build
    ]]>
  </end_to_end_example>

  <top_anti_patterns>
    - **Scaling the InteractionArea Root**: Scaling MUST target `VisualTarget` only. (Why: Scaling the parent `InteractionArea` destroys global UI coordinate conversions and drag snapping).
    - **Using 2D Arrays (`ItemData[,]`)**: Grid logic MUST be 1D. (Why: Violates the centralized math constraint `index = y * Width + x`).
    - **Unbounded R3 Subscriptions**: Failing to append `.AddTo(_disposables)`. (Why: Triggers compounding memory leaks and phantom execution cycles upon node removal).
    - **Querying Siblings via `GetNode()`**: Component discovery MUST use `GetRequiredComponentInChildren<T>()`. (Why: Hardcoded node paths break Godot.Composition modularity).
  </top_anti_patterns>

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
    - NEVER use string-based StateChart.Call() when StateChart reference exists
  </prohibitions>
</layer_1_quick_start>

<layer_2_detailed_guide>
  <api_reference>
    - **Component Fetching**: `GetRequiredComponentInChildren<T>()`, `GetEntity<T>()`
    - **Component Lifecycle**: `InitializeEntity()`, `InitializeComponent()`
    - **StateChart API**: `AutoBindToParentState()`, `StateChart.Call("send_event", "event_name")`, `SendStateEvent(string)`
    - **R3 Lifecycle**: `CompositeDisposable.Dispose()`, `.AddTo(CompositeDisposable)`
    - **R3 Data Streams**: `Subject<Unit>`, `OnNext(Unit.Default)`, `DistinctUntilChanged()`, `ObserveOn(GodotProvider.MainThread)`
    - **R3 Event Wrappers**: `OnPressedAsObservable()`, `OnToggledAsObservable()`, `OnValueChangedAsObservable()`, `OnTextChangedAsObservable()`, `OnItemSelectedAsObservable()`, `Observable.EveryUpdate()`, `Observable.EveryPhysicsUpdate()`
    - **Math Helpers**: `Mathf.FloorToInt()`
    - **Grid Conversions**: `ViewGrid.GetGlobalMousePosition()`, `ViewGrid.GridToLocalPosition(Vector2I)`
    - **Animation Sync**: `RegisterAnim(library, AnimationNames.Name, AnimationResource, Speed, isLoop)`
  </api_reference>

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

  <implementation_guide>
    - **Step 1: Define Grid & Shape Data**: Initialize `ItemData[] _gridData`. Convert shapes using `Vector2I[]` array bounds mapping.
    - **Step 2: Initialize Entities**: Mark root nodes with `[Entity]` and sub-nodes with `[Component(typeof(T))]`. Call `InitializeEntity()` and `InitializeComponent()` sequentially.
    - **Step 3: Setup StateChart Bindings**: Nest action components under `AtomicState` nodes. Call `this.AutoBindToParentState()` inside `_Ready()`.
    - **Step 4: Hook UI Coordinates**: Map mouse input via `ViewGrid.GetGlobalMousePosition()` exclusively. Round via `Mathf.FloorToInt()`.
    - **Step 5: Enforce Animation Separation**: Setup micro-interactions using `UITweenInteractComponent`, targeting only the `VisualContainer` sub-node. Kill active tweens before instantiating new ones.
  </implementation_guide>

  <technical_specifications>
    - **Grid Math Formula**: `index = y * Width + x`
    - **Coordinate Bounds Checking**: MUST clamp grid coordinates to `[0, Width)` x `[0, Height)`
    - **Shape Rotation Matrix (90-deg Clockwise)**: `(x,y) -> (-y,x)`
    - **UI Animation Constraints**: 
      - Pivot: `PivotOffset = Size/2` (Center-based scaling)
      - Easing: `EaseType.Out` + `TransitionType.Sine`
  </technical_specifications>

  <scene_structure_requirements>
    **Backpack Panel:**
    - Root: BackpackGridUIComponent (Control)
      - BackpackInteractionController
      - BackpackGridComponent
      - Items Container

    **Item Entity:**
    - Root: Control (InteractionArea, Scale=1,1)
      - StateChart
      - DraggableItemComponent
      - GridShapeComponent
      - SynergyComponent
      - UITweenInteractComponent
      - VisualContainer: Control (VisualTarget, Scale可变)
        - ItemIcon: TextureRect
        - StarContainer: Control
          - Star: TextureRect (multiple)

    **StateChart Structure:**
    - Root: CompoundState (initial="Idle")
      - Idle: AtomicState
        - Transition: "drag_start" → Dragging
      - Dragging: AtomicState
        - Contains: FollowMouseUIComponent
        - Transition: "drag_end" → Idle
  </scene_structure_requirements>

  <code_templates>
    <template name="SynergyRotationImplementation">
      <code><![CDATA[
      // CORRECT implementation of Synergy Star offset rotation tracking
      Shape.OnShapeChangedAsObservable.Subscribe(rotationCount => {
          for (int i = 0; i < StarOffsets.Length; i++) {
              Vector2I currentOffset = OriginalStarOffsets[i];
              for (int r = 0; r < rotationCount; r++) {
                  currentOffset = new Vector2I(-currentOffset.Y, currentOffset.X);
              }
              StarOffsets[i] = currentOffset;
          }
          CheckSynergiesAndEmit(); // Fire OnSynergyChangedAsObservable
      }).AddTo(_disposables);
      ]]></code>
    </template>

    <template name="MVC_DragStateReversion">
      <code><![CDATA[
      // CORRECT bounce-back resolution on placement failure
      if (!TryPlaceItem(OriginalGridPos)) {
          VisualTarget.GlobalPosition = OriginalGlobalPos;
          ForcePlaceItem(OriginalGridPos); // Guaranteed safety fallback
      }
      ]]></code>
    </template>
  </code_templates>

  <core_rules>
    <rule>
      <description>ALWAYS use `Mathf.FloorToInt()` and `ViewGrid.GetGlobalMousePosition()` for placement resolution.</description>
      <rationale>Prevents float-point precision drift and Viewport scaling mismatches when translating screen space to 1D array indices.</rationale>
      <example>
        # CORRECT
        Vector2 localMousePos = ViewGrid.GetLocalMousePosition();
        int gridX = Mathf.FloorToInt(localMousePos.X / CellSize.X);
        int gridY = Mathf.FloorToInt(localMousePos.Y / CellSize.Y);
        
        # INCORRECT
        int gridX = (int)(GetViewport().GetMousePosition().X / CellSize.X);
      </example>
    </rule>

    <rule>
      <description>NEVER modify `InteractionArea` (Root) Scale values.</description>
      <rationale>The root node establishes the collision footprint and global coordinate basis. Scaling it breaks raycasts and coordinate conversions.</rationale>
      <example>
        # CORRECT
        VisualTarget.Scale = new Vector2(1.1f, 1.1f);
        
        # INCORRECT
        this.Scale = new Vector2(1.1f, 1.1f); // Violates coordinate integrity
      </example>
    </rule>

    <rule>
      <description>PROHIBITED: Implementing internal state checks (e.g., `if (_canMove)`) inside logic components.</description>
      <rationale>Breaks StateChart architecture. Component enablement/execution MUST be governed entirely by StateChart lifecycle states (`AutoBindToParentState()`).</rationale>
      <example>
        # CORRECT
        // Handled strictly by parent state via AutoBindToParentState()
        public override void _Process(double delta) { ExecuteMovement(); }
        
        # INCORRECT
        public override void _Process(double delta) { if (_isDragging) ExecuteMovement(); }
      </example>
    </rule>
    
    <rule>
      <description>ALWAYS execute `DisposeBag` teardown in `_ExitTree()`.</description>
      <rationale>R3 framework defaults to unbounded lifecycles. Failing to dispose triggers memory leaks in Godot environments.</rationale>
      <example>
        # CORRECT
        public override void _ExitTree() { _disposables.Dispose(); }
      </example>
    </rule>
  </core_rules>
</layer_2_detailed_guide>

<layer_3_advanced>
  <troubleshooting>
    <error symptom="Item bounces back despite visual appearance of valid placement location.">
      <cause>Self-occupation collision. The item's origin indices were not cleared from the array before calculating the drop trajectory.</cause>
      <fix>Call `RemoveItemFromGrid()` immediately upon pickup (triggering "drag_start" transition) to free the indices BEFORE the user attempts drop validation.</fix>
    </error>
    <error symptom="Animation micro-interactions (hover/click) stutter or jitter randomly.">
      <cause>Concurrent/overlapping tweens competing for the same `VisualTarget.Scale` property without termination.</cause>
      <fix>Maintain a persistent reference to the active `Tween`. ALWAYS invoke `_activeTween?.Kill()` before starting `GetTree().CreateTween()`.</fix>
    </error>
    <error symptom="Synergies trigger on the wrong side of the item after rotating.">
      <cause>Failure to stack the 90-degree rotational matrix loop on `StarOffsets` based on total modulo rotation counts.</cause>
      <fix>Apply `(x,y) -> (-y,x)` transform in a loop `r` times, where `r = RotationCount % 4`. Emit `OnSynergyChangedAsObservable` explicitly post-calculation.</fix>
    </error>
    <error symptom="Events firing multiple times per frame in UI Helpers.">
      <cause>Absence of emission filtering on R3 data streams.</cause>
      <fix>Chain `.DistinctUntilChanged()` to the reactive stream. Apply `.ThrottleFirst()` to buttons or `.Debounce()` to high-frequency inputs (Search).</fix>
    </error>
  </troubleshooting>

  <best_practices>
    - **Entity Component Disconnection**: Couple logic to abstract classes (`BaseInputComponent`) rather than concrete variants.
    - **UI Helper Automation**: Apply `[Tool]` and `[GlobalClass]` attributes to UI Helpers (Sliders, Dropdowns, Toggles). Execute immediate structural updates directly inside property setters to maintain WYSIWYG editor synchronicity.
    - **Animation Configuration**: Map animations strictly as public string constants in `AnimationNames` and bind them structurally via `CharacterAnimationConfig.cs` using `RegisterAnim`. No hardcoded string execution permitted.
    - **State Recovery**: Before initiating visual ZIndex manipulation or drag overrides, snapshot the `OriginalGlobalPos` and Original State to ensure atomic reversibility.
  </best_practices>
</layer_3_advanced>