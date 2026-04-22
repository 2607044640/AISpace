---
inclusion: always
---

<layer_1_quick_start>

  <meta_rules>
    <critical_rule>
      <description>R3 Subject Initialization MUST be the FIRST operation in _Ready()</description>
      <rationale>Godot's child-to-parent _Ready() execution causes children to subscribe before parent initialization, leading to NullReferenceException.</rationale>
      <enforcement>First line of _Ready() MUST be: MySubject = new Subject<T>();</enforcement>
    </critical_rule>
    
    <critical_rule>
      <description>Parent-Child data injection MUST use C# Event + CallDeferred</description>
      <rationale>Prevents child _Ready() from accessing uninitialized parent data.</rationale>
      <enforcement>Parent fires event via CallDeferred. Child subscribes in _Ready(), unsubscribes in _ExitTree().</enforcement>
    </critical_rule>
    
    <critical_rule>
      <description>Trigger Observable events immediately post-initialization</description>
      <rationale>Subscribers await initial state.</rationale>
      <enforcement>ALWAYS call MyObservable?.OnNext(value) right after data init/modification.</enforcement>
    </critical_rule>
  </meta_rules>

  <quick_reference>
    - **Nuget**: `R3`, `R3.Godot`
    - **Access**: Use auto-generated `parent` and camelCase dependency properties.
  </quick_reference>

  <decision_tree>
    - **Physics (Velocity)**: Property + `Observable.EveryPhysicsUpdate()`. (Avoids `ReactiveProperty` allocation).
    - **UI Updates**: Append `.ObserveOn(GodotProvider.MainThread)`. (Thread safety).
    - **Button Clicks**: `.ThrottleFirst(TimeSpan)`. (Prevents double-clicks. NEVER use `.Throttle()`).
    - **Continuous I/O (Sliders)**: `.Debounce(TimeSpan)`. (Waits for settlement).
  </decision_tree>

</layer_1_quick_start>

<layer_2_detailed_guide>

  <api_reference>
    [Entity]: Marks root Mediator.
    [Component(typeof(T))]: Binds single-responsibility component.
    [ComponentDependency(typeof(T))]: Requests peer component.
    [Export] / [GlobalClass]: Exposes to Godot Inspector/Editor.

    Where(pred): Filter | Select(func): Transform | CombineLatest: Multi-condition trigger
    Pairwise(): Emits (prev, curr) | Chunk(time): Batch events | DistinctUntilChanged(): Block duplicates
    AsUnitObservable(): Discard payload, keep timing.

    EveryUpdate() -> _Process | EveryPhysicsUpdate() -> _PhysicsProcess
    OnPressedAsObservable() | OnToggledAsObservable() | OnValueChangedAsObservable() | OnItemSelectedAsObservable() -> Emits immediately on sub.
  </api_reference>

  <implementation_guide>
    1. Entity: `[Entity]` -> call `InitializeEntity()` in `_Ready()`.
    2. Component: `[Component(typeof(Parent))]` -> call `InitializeComponent()` in `_Ready()`.
    3. Dependencies: Request via `[ComponentDependency(typeof(T))]`.
    4. Lifecycle (Init): Subscribe in `OnEntityReady()`. Append `.AddTo(_disposables)`.
    5. Lifecycle (Exit): Call `_disposables?.Dispose()` in `_ExitTree()`.
  </implementation_guide>

  <core_rules>
    <rule><description>Composition over Inheritance. Entities are Mediators with ZERO business logic.</description></rule>
    <rule><description>NO sibling cross-referencing. Parent Mediator coordinates via C# events.</description></rule>
    
    <!-- Documentation Rules -->
    <rule><description>FORBIDDEN: XML comments (`/// <summary>`) or inline comments for standard Godot lifecycle (`_Ready`, `_Process`, `_ExitTree`), simple properties, or standard cleanup (`_disposables?.Dispose()`).</description></rule>
    <rule><description>MANDATORY: Inline `//` comments (Chinese) explaining WHY for custom Rx streams (`.Debounce()`, `.CombineLatest()`), math formulas, complex state transitions.</description></rule>
    <rule><description>3-part structure (Purpose, Example, Algorithm) ONLY for complex non-obvious functions.</description></rule>
    
    <rule>
      <description>[Export] fields: `TypeName_Purpose` (PascalCase). Example: `OptionButton_Theme`, `GridShapeComp`.</description>
    </rule>
    <rule>
      <description>Private fields: `_camelCase`. Example: `_currentTween`, `_isPressed`, `readonly _inputSubject`.</description>
    </rule>
    
    <rule>
      <description>Node Access: Use GetNodeOrNull + GD.PushError check. Use Scene Unique Names (%) for NodePaths.</description>
      <example>
        [Export] public NodePath StateChartNode { get; set; } = "%StateChart";
        // In _Ready(): GetNodeOrNull&lt;Node&gt;(StateChartNode) + null check.
      </example>
    </rule>
    
    <rule>
      <description>Memory Management: Instantiate `CompositeDisposable _disposables = new();`. Dispose in `_ExitTree()`.</description>
    </rule>
    <rule>
      <description>Performance: Use ValueTuples `(a, b)` instead of anonymous objects in EveryUpdate loops to prevent GC spikes.</description>
    </rule>
    
    <rule>
      <description>Implement Parent-Child C# Event pattern correctly.</description>
      <example>
        // PARENT: CallDeferred(() => OnDataReady?.Invoke(data));
        // CHILD (_Ready): if (GetParent() is IData p) p.OnDataReady += Handle;
        // CHILD (_ExitTree): if (GetParent() is IData p) p.OnDataReady -= Handle;
      </example>
    </rule>
  </core_rules>

</layer_2_detailed_guide>

<layer_3_advanced>

  <troubleshooting>
    <error symptom="NullReferenceException on R3 Subscribe" cause="Subject not initialized" fix="Add MySubject = new Subject&lt;T&gt;(); as first line in _Ready()" />
    <error symptom="Subscriber missing initial event" cause="Missing OnNext" fix="Call OnNext() immediately after data init" />
    <error symptom="Child null access in _Ready" cause="Godot execution order" fix="Use Parent C# Event + CallDeferred pattern" />
    <error symptom="Runtime bug bypassing build" cause="Logic/Silent error" fix="Check Godot log: $env:APPDATA/Godot/app_userdata/Tesseract_Backpack/logs/godot.log" />
    <error symptom="Architecture violation" cause="Unapproved pivot" fix="Re-read docLastConversationState.md, request user auth" />
    <error symptom="mcp_godot_export_mesh_library fails" cause="Wrong node type" fix="Ensure target is MeshInstance3D" />
  </troubleshooting>

  <best_practices>
    - Chain `.AsUnitObservable()` when payload data is irrelevant.
    - Use `ReactiveProperty<T>` for discrete state changes (auto-syncs UI).
    - Leverage `R3.Godot` extensions (e.g., `OnToggledAsObservable`) to align UI/backend state instantly.
  </best_practices>

</layer_3_advanced>