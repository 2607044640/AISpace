---
inclusion: always
---

<layer_1_quick_start>

  <quick_reference>
    - **Package Requirements:** Install `R3` and `R3.Godot` via NuGet.
    - **Rule Storage:** Save and enforce all architectural rules in `KiroWorkingSpace/.kiro/`.
    - **Component Parent Access:** Rely on the auto-generated `parent` property.
    - **Component Dependency Access:** Rely on auto-generated camelCase properties (e.g., `inputComponent`).
  </quick_reference>

  <decision_tree>
    - If managing high-frequency physics data (e.g., Velocity):
      - **ALWAYS** use standard properties and poll via `Observable.EveryPhysicsUpdate()`. (Why: `ReactiveProperty<T>` introduces severe allocation overhead on every frame).
    - If modifying UI from an asynchronous stream:
      - **ALWAYS** append `.ObserveOn(GodotProvider.MainThread)`. (Why: Godot UI operations are thread-restricted; bypassing causes immediate crashes).
    - If handling instant button presses or immediate actions:
      - **ALWAYS** use `.ThrottleFirst(TimeSpan)`. (Why: Prevents double-clicks while acting instantly. **NEVER** use standard `.Throttle()`).
    - If processing continuous streams linked to I/O or heavy computation (e.g., sliders, resize):
      - **ALWAYS** use `.Debounce(TimeSpan)`. (Why: Prevents performance locking by waiting for stream settlement).
  </decision_tree>

  <top_anti_patterns>
    - **Using hardcoded string literals in `GetNode()`:** `GetNode<Control>("VisualContainer")`. (Why: Creates brittle coupling and breaks refactoring. **ALWAYS** use `[Export] NodePath` with `%` defaults).
    - **Declaring `NodePath` without defaults:** `[Export] public NodePath Target { get; set; }`. (Why: Forces manual configuration and is error-prone. Use `= "%Target"`).
    - **Direct sibling component access:** `sibling.DoSomething()`. (Why: Violates single responsibility and creates unmaintainable spaghetti code. Signal upward to the Mediator).
    - **Tightly coupling nodes using `GetNode<T>()` without `[Export]`:** Dependencies **MUST** be injected via `[Export]`.
    - **Stuffing `if-else` logic into `_PhysicsProcess`:** (Why: Scales poorly. Use Finite State Machines).
    - **Hardcoding magic values or animation names:** (Why: Prevents designer tweaking. Expose via `[Export]`).
    - **Subscribing to events inside `_Ready()`:** (Why: Fails if dependencies aren't loaded. Use `OnEntityReady()` instead).
  </top_anti_patterns>

</layer_1_quick_start>

<layer_2_detailed_guide>

  <api_reference>
    | C# Attributes | Target | Purpose |
    |---|---|---|
    | `[Entity]` | Entity Classes | Marks a node as a root Mediator. |
    | `[Component(typeof(T))]` | Component Classes | Binds a single-responsibility component to a parent entity type. |
    | `[ComponentDependency(typeof(T))]` | Component Classes | Explicitly requests another component on the same entity. |
    | `[Export]` | Properties | Exposes node references and magic values to the Godot Inspector. |
    | `[GlobalClass]` | Core Components | Exposes mechanics to the Godot Editor for cross-project reuse. |

    | R3 Reactive Operators | Input -> Output | Action |
    |---|---|---|
    | `Where(predicate)` | `T -> T` | Filters stream payloads based on a condition. |
    | `CombineLatest` | `IObservable[] -> T[]` | Triggers logic upon multiple stream conditions resolving. |
    | `Select` | `T -> U` | Transforms a stream payload to a new type. |
    | `Pairwise()` | `T -> (T prev, T curr)` | Emits the previous and current state simultaneously. |
    | `Chunk(TimeSpan)` | `T -> T[]` | Batches high-volume stream events. |
    | `.DistinctUntilChanged()`| `T -> T` | Blocks identical consecutive payloads. |
    | `.AsUnitObservable()` | `T -> Unit` | Discards payload data when only the trigger timing matters. |

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
    1. Declare an Entity using `[Entity]` and call `InitializeEntity()` inside `_Ready()`.
    2. Create independent Components using `[Component(typeof(ParentType))]` and call `InitializeComponent()` inside `_Ready()`.
    3. Declare inter-component needs using `[ComponentDependency(typeof(OtherComponent))]`.
    4. Subscribe to events strictly inside `OnEntityReady()` and map updates to `.AddTo(_disposables)`.
    5. Clean up by calling `_disposables.Dispose()` strictly inside `_ExitTree()`.
  </implementation_guide>

  <core_rules>
    <rule>
      <description>**ALWAYS** design systems using "Composition over Inheritance".</description>
    </rule>
    <rule>
      <description>Entities **MUST** act exclusively as Mediators and contain ZERO business logic.</description>
    </rule>
    <rule>
      <description>**NEVER** allow sibling components to reference each other directly.</description>
      <rationale>Direct sibling coupling violates single responsibility. Parent Mediator **MUST** coordinate between siblings via C# events.</rationale>
    </rule>
    
    <!-- Documentation Rules: Apply based on function complexity -->
    <rule>
      <description>Trivial functions (lifecycle hooks, simple getters): Omit documentation entirely.</description>
      <rationale>Prevents noise and wasted lines explaining self-evident code.</rationale>
    </rule>
    <rule>
      <description>Simple functions: Use single-sentence summary or inline comments.</description>
      <rationale>Maintains flexibility without forcing rigid structures.</rationale>
    </rule>
    <rule>
      <description>Complex/logic-heavy functions: Apply mandatory 3-part structure (目的/Purpose, 示例/Example, 算法/Algorithm).</description>
      <rationale>Ensures logic execution steps map strictly 1:1 to code.</rationale>
    </rule>
    
    <rule>
      <description>**ALWAYS** use Scene Unique Names (`%`) for `NodePath` properties with default values.</description>
      <rationale>Hardcoded strings create brittle coupling and break refactoring. Default values eliminate manual configuration burden.</rationale>
      <example>
        [Export] public NodePath StateChartNode { get; set; } = "%StateChart";
        
        public override void _Ready()
        {
            var stateChart = GetNodeOrNull&lt;Node&gt;(StateChartNode);
            if (stateChart == null)
            {
                GD.PushError($"[{Name}] StateChart not found: {StateChartNode}");
                return;
            }
        }
      </example>
    </rule>
    <rule>
      <description>**ALWAYS** initialize R3 Subjects in `_Ready()` before any subscription can occur.</description>
      <rationale>Godot's `_Ready()` executes child-to-parent. Subscribers may attempt to access Subjects before initialization, causing `NullReferenceException`.</rationale>
      <example>
        public Subject&lt;Unit&gt; OnShapeChanged { get; private set; }
        
        public override void _Ready()
        {
            OnShapeChanged = new Subject&lt;Unit&gt;();  // Initialize FIRST
            // ... rest of initialization
        }
      </example>
    </rule>
    <rule>
      <description>**ALWAYS** instantiate a `CompositeDisposable _disposables = new();` inside EVERY reactive UI or Component class.</description>
    </rule>
    <rule>
      <description>**ALWAYS** subscribe to events inside `OnEntityReady()` and **NEVER** inside `_Ready()`.</description>
    </rule>
    <rule>
      <description>**ALWAYS** use `.DistinctUntilChanged()` on two-way bindings and high-frequency UI updates.</description>
    </rule>
    <rule>
      <description>**ALWAYS** use ValueTuples `(a, b)` instead of anonymous objects `new { a, b }` inside `EveryUpdate` loops.</description>
      <rationale>Anonymous objects trigger heap allocation, causing Garbage Collection (GC) spikes and frame drops.</rationale>
    </rule>
  </core_rules>

</layer_2_detailed_guide>

<layer_3_advanced>

  <troubleshooting>
    <error symptom="Memory leaks and degraded performance over time.">
      <cause>Reactive subscriptions or C# events were not cleanly detached upon node removal, leaving zombie objects in memory.</cause>
      <fix>**ALWAYS** call `_disposables.Dispose()` strictly inside the `_ExitTree()` override of the component.</fix>
    </error>
    <error symptom="Infinite UI loops or massive CPU spikes during state updates.">
      <cause>A two-way binding or high-frequency data stream is continuously echoing state changes back and forth without a termination condition.</cause>
      <fix>Insert `.DistinctUntilChanged()` into the subscription chain to aggressively drop duplicate payloads before they trigger logic.</fix>
    </error>
    <error symptom="Cross-thread crash or UI freezing exception when using async streams.">
      <cause>An asynchronous task attempted to manipulate a Godot Node property directly from a background worker thread.</cause>
      <fix>Append `.ObserveOn(GodotProvider.MainThread)` immediately before the `.Subscribe()` block to force UI execution back to the main thread.</fix>
    </error>
    <error symptom="Micro-stutters or frame drops during gameplay (GC Spikes).">
      <cause>Memory is being dynamically allocated on the heap during an `Observable.EveryUpdate()` or `Observable.EveryPhysicsUpdate()` loop using anonymous objects.</cause>
      <fix>Use struct-based ValueTuples instead of anonymous objects.</fix>
      <example>
        // Use ValueTuples
        Observable.EveryUpdate()
            .Select(_ =&gt; (player.Position, enemy.Position))
            .Subscribe(tuple =&gt; { ... });
      </example>
    </error>
    <error symptom="NullReferenceException when subscribing to Observable or calling Subject.OnNext().">
      <cause>R3 Subject was declared but never initialized in `_Ready()`.</cause>
      <fix>Initialize ALL Subjects at the top of `_Ready()`: `OnShapeChanged = new Subject&lt;Unit&gt;();`</fix>
    </error>
    <error symptom="Component receives null data or misses initialization events.">
      <cause>Godot's `_Ready()` executes child-to-parent. Child subscribed to parent's event, but parent fires event before child's `_Ready()` completes.</cause>
      <fix>Use C# `event Action&lt;T&gt;` pattern. Parent fires event in `_Ready()`. Child subscribes in `_Ready()`. Godot guarantees child subscribes first. **ALWAYS** unsubscribe in `_ExitTree()`.</fix>
      <example>
        // Parent
        public event Action&lt;ItemData&gt; OnDataReady;
        
        public override void _Ready() 
        { 
            CallDeferred(() =&gt; OnDataReady?.Invoke(data)); 
        }
        
        // Child
        public override void _Ready()
        {
            if (GetParent() is IDataProvider provider)
                provider.OnDataReady += InitializeWithData;
        }
        
        public override void _ExitTree()
        {
            if (GetParent() is IDataProvider provider)
                provider.OnDataReady -= InitializeWithData;  // Prevent memory leak
        }
      </example>
    </error>
    <error symptom="NullReferenceException thrown during `InitializeComponent()` or `_Ready()`.">
      <cause>A component attempted to access a dependency or subscribe to a sibling event before the entity's component tree finished loading.</cause>
      <fix>Move all subscription and communication logic strictly into `OnEntityReady()`.</fix>
    </error>
  </troubleshooting>

  <best_practices>
    - **Payload Discarding:** Streamline logic by chaining `.AsUnitObservable()` when the pipeline only needs to know *when* an event happened, not *what* the payload contained.
    - **State Abstraction:** Use `ReactiveProperty<T>` for discrete, non-continuous state changes so UI elements automatically sync via single-subscription.
    - **Editor Parity:** Take full advantage of `R3.Godot` extensions like `OnToggledAsObservable()` because they immediately emit current state upon subscription, ensuring UI aligns instantly with backend state.
    - **Enforcement Protocol:** 1. Before writing ANY `GetNode()` call, ask: "Is this a hardcoded string?"
      2. If yes, **IMMEDIATELY** create `[Export] NodePath` property with `%` default.
      3. If you catch yourself violating these rules, **STOP** and refactor before continuing.
      4. Code review checklist: Search for `GetNode(` and verify ALL calls use NodePath variables.
  </best_practices>

</layer_3_advanced>
