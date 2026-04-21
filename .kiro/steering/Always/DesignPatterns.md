---
inclusion: always
---

<layer_1_quick_start>

  <meta_rules>
    <critical_rule>
      <description>R3 Subject Initialization is MANDATORY and MUST be the FIRST operation in _Ready()</description>
      <rationale>Uninitialized Subjects cause NullReferenceException. Godot's child-to-parent _Ready() execution means children may subscribe before parent initializes.</rationale>
      <enforcement>ALWAYS write MySubject = new Subject&lt;T&gt;(); as the FIRST line in _Ready() for ANY class exposing Observable properties.</enforcement>
    </critical_rule>
    
    <critical_rule>
      <description>Parent-Child data injection MUST use C# event + CallDeferred pattern</description>
      <rationale>Godot _Ready() executes child-to-parent. Direct data access in child _Ready() will fail because parent hasn't initialized yet.</rationale>
      <enforcement>ALWAYS use Interface + C# event pattern. Parent fires event via CallDeferred. Child subscribes in _Ready() and unsubscribes in _ExitTree().</enforcement>
    </critical_rule>
    
    <critical_rule>
      <description>Observable events MUST be triggered after data initialization</description>
      <rationale>Subscribers expect to receive events when data changes. Forgetting OnNext() leaves subscribers waiting indefinitely.</rationale>
      <enforcement>ALWAYS call MyObservable?.OnNext(value) immediately after initializing or modifying data that subscribers depend on.</enforcement>
    </critical_rule>
  </meta_rules>

  <quick_reference>
    - Install `R3` and `R3.Godot` via NuGet
    - Access components via auto-generated `parent` property and camelCase dependency properties
  </quick_reference>

  <decision_tree>
    - High-frequency physics (Velocity): Use standard properties + `Observable.EveryPhysicsUpdate()`. (Why: `ReactiveProperty<T>` causes allocation overhead)
    - Async UI updates: Append `.ObserveOn(GodotProvider.MainThread)`. (Why: Godot UI is thread-restricted)
    - Button presses: Use `.ThrottleFirst(TimeSpan)`. (Why: Prevents double-clicks. NEVER use `.Throttle()`)
    - Continuous streams (sliders, I/O): Use `.Debounce(TimeSpan)`. (Why: Waits for stream settlement)
  </decision_tree>

</layer_1_quick_start>

<layer_2_detailed_guide>

  <api_reference>
    | C# Attributes | Target | Purpose |
    |---|---|---|
    | `[Entity]` | Entity Classes | Marks node as root Mediator. |
    | `[Component(typeof(T))]` | Component Classes | Binds single-responsibility component to parent entity. |
    | `[ComponentDependency(typeof(T))]` | Component Classes | Explicitly requests another component on same entity. |
    | `[Export]` | Properties | Exposes node references/values to Godot Inspector. |
    | `[GlobalClass]` | Core Components | Exposes mechanics to Godot Editor for cross-project reuse. |

    | R3 Reactive Operators | Input -> Output | Action |
    |---|---|---|
    | `Where(predicate)` | `T -> T` | Filters stream payloads based on condition. |
    | `CombineLatest` | `IObservable[] -> T[]` | Triggers upon multiple stream conditions resolving. |
    | `Select` | `T -> U` | Transforms stream payload to new type. |
    | `Pairwise()` | `T -> (T prev, T curr)` | Emits previous and current state simultaneously. |
    | `Chunk(TimeSpan)` | `T -> T[]` | Batches high-volume stream events. |
    | `.DistinctUntilChanged()`| `T -> T` | Blocks identical consecutive payloads. |
    | `.AsUnitObservable()` | `T -> Unit` | Discards payload data when only timing matters. |

    | R3.Godot Integration | Source | Target Stream |
    |---|---|---|
    | `Observable.EveryUpdate()` | Global | Mapped to Godot `_Process`. |
    | `Observable.EveryPhysicsUpdate()`| Global | Mapped to Godot `_PhysicsProcess`. |
    | `.OnPressedAsObservable()` | Button Nodes | Triggers on button click. |
    | `.OnToggledAsObservable()` | Toggle Nodes | Emits state immediately upon subscription. |
    | `.OnValueChangedAsObservable()`| Sliders/Inputs | Emits state immediately upon subscription. |
    | `.OnItemSelectedAsObservable()`| Dropdowns | Emits state immediately upon subscription. |
  </api_reference>

  <implementation_guide>
    - Step 1: Declare `[Entity]` and call `InitializeEntity()` in `_Ready()`.
    - Step 2: Declare `[Component(typeof(Parent))]` and call `InitializeComponent()` in `_Ready()`.
    - Step 3: Declare peer dependencies via `[ComponentDependency(typeof(T))]`.
    - Step 4: Subscribe to events in `OnEntityReady()` and append `.AddTo(_disposables)`.
    - Step 5: Clean up by calling `_disposables.Dispose()` in `_ExitTree()`.
  </implementation_guide>

  <core_rules>
    <rule>
      <description>ALWAYS design systems using Composition over Inheritance.</description>
    </rule>
    <rule>
      <description>Entities MUST act exclusively as Mediators and contain ZERO business logic.</description>
    </rule>
    <rule>
      <description>NEVER allow sibling components to reference each other directly. Parent Mediator MUST coordinate via C# events.</description>
    </rule>
    
    <!-- Documentation Rules -->
    <rule>
      <description>ALWAYS omit documentation for trivial functions like lifecycle hooks or simple getters.</description>
    </rule>
    <rule>
      <description>ALWAYS use single-sentence summaries or inline comments for simple functions.</description>
    </rule>
    <rule>
      <description>ALWAYS apply mandatory 3-part structure (目的/Purpose, 示例/Example, 算法/Algorithm) for complex functions.</description>
    </rule>
    
    <!-- Naming Convention Rules -->
    <rule>
      <description>ALWAYS use TypeName_Purpose format (PascalCase) for fields/properties. Abbreviate Component to Comp. Use semanticRename tool for batch renaming.</description>
      <rationale>Enables bidirectional search and eliminates cognitive overhead.</rationale>
      <example>
        ✅ CORRECT: OptionButton_Theme, PopupMenu_MenuOption, GridShapeComp
        ❌ FORBIDDEN: GridShapeComponent, GridShape_Node, _themeDropdown
      </example>
    </rule>
    
    <!-- Godot Node Rules -->
    <rule>
      <description>ALWAYS use GetNodeOrNull + null check with GD.PushError for node access.</description>
    </rule>
    <rule>
      <description>ALWAYS use Scene Unique Names (%) for NodePath properties with default values.</description>
      <example>
        [Export] public NodePath StateChartNode { get; set; } = "%StateChart";
        
        public override void _Ready()
        {
            var stateChart = GetNodeOrNull&lt;Node&gt;(StateChartNode);
            if (stateChart == null) { GD.PushError($"[{Name}] StateChart not found"); return; }
        }
      </example>
    </rule>
    
    <!-- R3 Reactive Rules -->
    <rule>
      <description>ALWAYS initialize R3 Subjects in _Ready() before any subscriptions occur.</description>
      <rationale>Godot _Ready() executes child-to-parent. Uninitialized Subjects throw NullReferenceException.</rationale>
      <example>
        public Subject&lt;Unit&gt; OnShapeChanged { get; private set; }
        
        public override void _Ready()
        {
            OnShapeChanged = new Subject&lt;Unit&gt;();  // Initialize FIRST
        }
      </example>
    </rule>
    <rule>
      <description>ALWAYS instantiate CompositeDisposable _disposables = new(); inside EVERY reactive class.</description>
    </rule>
    <rule>
      <description>ALWAYS call _disposables.Dispose() in _ExitTree() to prevent memory leaks.</description>
    </rule>
    <rule>
      <description>ALWAYS use .DistinctUntilChanged() on two-way bindings and high-frequency UI updates.</description>
    </rule>
    <rule>
      <description>ALWAYS use ValueTuples (a, b) instead of anonymous objects new { a, b } inside EveryUpdate loops.</description>
      <rationale>Prevents GC spikes.</rationale>
    </rule>
    
    <!-- Parent-Child Communication Rules -->
    <rule>
      <description>ALWAYS use C# event + CallDeferred for parent-child node communication.</description>
      <rationale>Godot _Ready() executes child-to-parent. Child subscribes first, parent fires deferred.</rationale>
      <example>
        // Parent
        public event Action&lt;ItemData&gt; OnDataReady;
        
        public override void _Ready()
        {
            var data = LoadItemData();
            CallDeferred(() => OnDataReady?.Invoke(data));
        }
        
        // Child
        public override void _Ready()
        {
            if (GetParent() is IDataProvider provider)
                provider.OnDataReady += HandleData;
        }
        
        public override void _ExitTree()
        {
            if (GetParent() is IDataProvider provider)
                provider.OnDataReady -= HandleData;  // Prevent memory leak
        }
      </example>
    </rule>
    <rule>
      <description>ALWAYS subscribe to Entity-Component events inside OnEntityReady() and NEVER inside _Ready().</description>
    </rule>
  </core_rules>

</layer_2_detailed_guide>

<layer_3_advanced>

  <troubleshooting>
    <error symptom="NullReferenceException subscribing to R3 Observable">
      <cause>Subject never instantiated in _Ready().</cause>
      <fix>Initialize Subject in _Ready() first line: MySubject = new Subject&lt;T&gt;();</fix>
    </error>
    
    <error symptom="Observable subscriber never receives initial event">
      <cause>Parent forgets OnNext() after data init.</cause>
      <fix>Call OnNext() immediately after data initialization.</fix>
    </error>
    
    <error symptom="NullReferenceException child accessing parent data in _Ready()">
      <cause>Godot _Ready() child-to-parent execution order.</cause>
      <fix>Use C# event + CallDeferred. Parent fires deferred, child subscribes in _Ready().</fix>
    </error>
    
    <error symptom="Unexpected runtime behavior not caught by dotnet build">
      <cause>Runtime errors silenced or logic bugs.</cause>
      <fix>Check Godot log: $env:APPDATA/Godot/app_userdata/Tesseract_Backpack/logs/godot.log</fix>
    </error>
    
    <error symptom="Implementation violates user architecture">
      <cause>Blindly pivoting without user approval.</cause>
      <fix>Re-read docLastConversationState.md, request authorization.</fix>
    </error>
    
    <error symptom="mcp_godot_export_mesh_library fails">
      <cause>Missing required node type.</cause>
      <fix>Ensure target is MeshInstance3D.</fix>
    </error>
  </troubleshooting>

  <best_practices>
    - Chain `.AsUnitObservable()` when payload data is irrelevant to streamline logic.
    - Use `ReactiveProperty<T>` for discrete state changes to auto-sync UI elements.
    - Leverage `R3.Godot` extensions (e.g., `OnToggledAsObservable`) to instantly align UI with backend state upon subscription.
  </best_practices>

</layer_3_advanced>
