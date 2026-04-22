---
inclusion: always
---
<layer_1_architecture_and_r3>

  <r3_godot_quirks>
    <rule>
      <description>CRITICAL: Godot _Ready() Execution Order & NullReference Prevention</description>
      <rationale>Children execute _Ready() BEFORE parents. Subscribing to uninitialized parent subjects causes crashes.</rationale>
      <enforcement>
        1. Subjects MUST be initialized on the very FIRST line of `_Ready()` (`MySubject = new Subject<T>();`).
        2. ALWAYS call `MyObservable?.OnNext(value)` immediately after data init so subscribers don't miss the initial state.
        3. Use C# Events + CallDeferred for Parent-Child injection:
           - PARENT: `CallDeferred(() => OnDataReady?.Invoke(data));`
           - CHILD (_Ready): `if (GetParent() is IData p) p.OnDataReady += Handle;`
           - CHILD (_ExitTree): `if (GetParent() is IData p) p.OnDataReady -= Handle;`
      </enforcement>
    </rule>
  </r3_godot_quirks>

  <r3_decision_tree>
    - Physics (Velocity): `Observable.EveryPhysicsUpdate()` (Avoids `ReactiveProperty` GC allocation).
    - UI Updates: Append `.ObserveOn(GodotProvider.MainThread)` for thread safety.
    - Button Clicks: `.ThrottleFirst(TimeSpan)` (Prevents double-clicks. NEVER use `.Throttle()`).
    - Continuous I/O (Sliders): `.Debounce(TimeSpan)` (Waits for settlement).
    - State Flags: Use `ReactiveProperty<T>` (Auto-syncs UI).
    - Discard Payload: Chain `.AsUnitObservable()` when event data is irrelevant but timing is needed.
  </r3_decision_tree>

  <component_architecture>
    <rules>
      - Composition over Inheritance. Entities are Mediators with ZERO business logic.
      - NO sibling cross-referencing. Parent Mediator coordinates via C# events.
      - Memory: Instantiate `CompositeDisposable _disposables = new();`. Dispose strictly in `_ExitTree()`.
      - Performance: Use ValueTuples `(a, b)` instead of anonymous objects in EveryUpdate loops to prevent GC spikes.
    </rules>
    <implementation_steps>
      1. Entity: `[Entity]` -> call `InitializeEntity()` in `_Ready()`.
      2. Component: `[Component(typeof(Parent))]` -> call `InitializeComponent()` in `_Ready()`.
      3. Dependencies: Request via `[ComponentDependency(typeof(T))]`. 
      4. ACCESS (CRITICAL): Access dependencies via auto-generated `parent` and camelCase dependency properties.
      5. Subscribe: In `OnEntityReady()`. Append `.AddTo(_disposables)`.
    </implementation_steps>
  </component_architecture>

</layer_1_architecture_and_r3>

<layer_2_coding_standards>

  <naming_and_access>
    - [Export] Fields: `TypeName_Purpose` (PascalCase). Example: `OptionButton_Theme`, `GridShapeComp`.
    - Private Fields: `_camelCase`. Example: `_currentTween`, `_inputSubject`.
    - Node Access: Use Scene Unique Names (`%Name`). Always use `GetNodeOrNull<T>` + `GD.PushError` check.
  </naming_and_access>

  <documentation_rules>
    - FORBIDDEN: XML comments (`/// <summary>`) or inline comments for standard Godot lifecycle (`_Ready`, `_Process`), simple properties, or standard cleanup.
    - MANDATORY: Inline `//` comments (in Chinese) explaining WHY for custom Rx streams (`.Debounce()`), math formulas, and complex state transitions.
    - STRUCTURE: 3-part structure (Purpose, Example, Algorithm) ONLY for complex non-obvious functions.
  </documentation_rules>

  <api_cheat_sheet>
    <environment>Nuget: `R3`, `R3.Godot`</environment>
    <rx_operators>
      - Where(pred): Filter | Select(func): Transform | CombineLatest: Multi-condition trigger
      - Pairwise(): Emits (prev, curr) | Chunk(time): Batch events | DistinctUntilChanged(): Block duplicates
    </rx_operators>
    <r3_godot_extensions>
      - EveryUpdate() -> _Process | EveryPhysicsUpdate() -> _PhysicsProcess
      - OnPressedAsObservable() | OnToggledAsObservable() | OnValueChangedAsObservable() -> Emits immediately on sub.
    </r3_godot_extensions>
  </api_cheat_sheet>

</layer_2_coding_standards>