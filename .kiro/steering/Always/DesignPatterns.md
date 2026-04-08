---
inclusion: always
---

<GodotDesignPatterns>

<CoreArchitecture>
- ENFORCE "Composition over Inheritance". Avoid deep hierarchies.
- Break entities into single-responsibility Components.
- Treat Root node ONLY as a Mediator coordinating components.
</CoreArchitecture>

<DecouplingRules>
- Call Down, Signal Up: Parents call child methods. Children emit C# `event/Action` upwards.
- Isolate Siblings: Components MUST NOT reference each other directly.
- Inject Dependencies: ALWAYS use `[Export]`, NEVER hardcode `GetNode<T>()`.
- Extract Magic Values: Hardcode ZERO specific content (e.g., animation names). Expose via `[Export]`.
</DecouplingRules>

<BehavioralRules>
- Implement FSMs instead of monolithic `_PhysicsProcess` with endless `if-else`.
- Decouple logic triggers: e.g., Movement MUST emit `OnJumped`, NEVER call AudioPlayer directly.
- Add `[GlobalClass]` to core components for cross-project reuse.
</BehavioralRules>

</GodotDesignPatterns>

<GodotCompositionRules>

<EntityRules>
- Declare as `partial class` with `[Entity]` attribute.
- Call `InitializeEntity()` in `_Ready()`.
- Contain ZERO business logic.
</EntityRules>

<ComponentRules>
- Declare as `partial class` with `[Component(typeof(ParentType))]`.
- Call `InitializeComponent()` in `_Ready()`.
- Declare dependencies using `[ComponentDependency(typeof(OtherComponent))]`.
- Subscribe to events strictly in `OnEntityReady()`, NEVER in `_Ready()`.
- Unsubscribe in `_ExitTree()` to prevent memory leaks.
</ComponentRules>

<ComponentCommunication>
- Access entity via auto-generated `parent` property.
- Access dependencies via auto-generated camelCase properties (e.g., `inputComponent`).
- Emit events using `public event Action<T> OnSomething;`.
- NEVER call sibling component methods directly.
</ComponentCommunication>

</GodotCompositionRules>

<ReactiveExtensions>

<Dependencies>
- Install NuGet packages: `R3` and `R3.Godot`.
</Dependencies>

<MandatoryRules>
- **DisposeBag:** Initialize `CompositeDisposable _disposables = new();` in EVERY UI/Component class.
- **AddTo:** Append `.AddTo(_disposables)` to EVERY `.Subscribe()` chain.
- **Dispose:** Call `_disposables.Dispose()` strictly inside `_ExitTree()`.
- **Thread Safety:** ALWAYS chain `.ObserveOn(GodotProvider.MainThread)` after async operations before updating UI.
- **Input Responsiveness:** ALWAYS use `.ThrottleFirst(TimeSpan)` on buttons/instant actions. NEVER use `.Throttle()`.
- **High-Cost Operations:** ALWAYS use `.Debounce(TimeSpan)` on high-frequency streams (slider move, resize) linked to I/O or heavy computation.
- **Circular Guard:** ALWAYS use `.DistinctUntilChanged()` in two-way bindings and high-frequency streams to prevent infinite loops and redundant redraws.
- **Zero-GC Sampling:** In `EveryUpdate` loops, ALWAYS use ValueTuples `(a, b)` instead of anonymous objects `new { a, b }`.
</MandatoryRules>

<CoreMechanics>
- **Discrete State:** Use `ReactiveProperty<T>`. UI subscribes exactly ONCE for auto-updates.
- **Physics Data:** NEVER use `ReactiveProperty<T>` for high-frequency physics (e.g., Velocity). Use standard properties and poll via `Observable.EveryUpdate()`.
- **Loop Mapping:** Map `Observable.EveryUpdate()` to `_Process`. Map `Observable.EveryPhysicsUpdate()` to `_PhysicsProcess`.
- **Payload Discarding:** Use `.AsUnitObservable()` when only the trigger event matters.
</CoreMechanics>

<GodotExtensions>
- Prefer `R3.Godot` extensions (e.g., `_button.OnPressedAsObservable()`) over manual event binding.
- Rely on extensions that emit current state immediately for UI consistency: `OnToggledAsObservable()`, `OnValueChangedAsObservable()`, `OnItemSelectedAsObservable()`.
</GodotExtensions>

<EssentialOperators>
| Operator | Use Case |
|---|---|
| `Where(predicate)` | Filter events |
| `CombineLatest` | Multi-condition logic |
| `Select` | Transform value |
| `Pairwise()` | Get (previous, current) |
| `Chunk(TimeSpan)` | Batch events |
</EssentialOperators>

</ReactiveExtensions>