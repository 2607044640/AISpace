---
inclusion: always
---
<layer_1_architecture_and_r3>
<prime_directive>
    <rule>
      <description>CRITICAL: Future-Proof, Extensible & Generic Design ONLY</description>
      <rationale>Short-sighted logic, hardcoding, and overly specific designs create technical debt. Every implementation must anticipate future system scaling and requirement changes.</rationale>
      <enforcement>
        1. ARCHITECTURE: Solve the CLASS of problem, not the specific instance. Systems must be decoupled, modular, and parameterized.
        2. CODE: Maximally utilize Generics (<T>), Interfaces, and abstraction layers. ZERO hardcoded edge-cases or magic numbers. 
        3. NAMING: Strictly use domain-agnostic, high-level abstract terminology. Do not tie names to current specific visual or gameplay manifestations.
        4. EVOLUTION: Before writing any logic or rule, ask: "Will this break or require refactoring if the system scales by 100x or adds 5 new variants?" If yes, redesign it.
      </enforcement>
    </rule>
  </prime_directive>
  <r3_godot_quirks>
    <rule>
      <description>CRITICAL: Godot Lifecycle (_EnterTree vs _Ready) & Initialization</description>
      <rationale>Godot executes `_EnterTree()` Top-Down (Parent before Child), but `_Ready()` Bottom-Up (Child before Parent). Using _Ready for parent data init causes NullReference in children.</rationale>
      <enforcement>
        1. INIT IN ENTER_TREE: All `Subject<T>` instantiations and core data (`new Subject<T>()`) MUST be done in the Parent's `public override void _EnterTree()`.
        2. SAFE CHILD READY: Children can safely subscribe to Parent Subjects in their own `_Ready()` because the Parent's `_EnterTree()` has already executed.
        3. AVOID CALLDEFERRED: Do not use `CallDeferred` for cross-frame delays. Use `await ToSignal(GetTree(), SceneTree.SignalName.ProcessFrame);` to preserve C# async stack traces and readability.
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