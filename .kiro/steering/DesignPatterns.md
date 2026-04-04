---
inclusion: always
---

# Godot Design Patterns

<context>
Detailed examples and patterns: See `addons/CoreComponents/ARCHITECTURE.md`
</context>

<GodotDesignPatterns>

<CoreArchitecture>
- ENFORCE "Composition over Inheritance". Avoid deep hierarchies.
- Break entities into single-responsibility child Nodes (Components).
- The Root node (e.g., `Player`) acts ONLY as a "Mediator" coordinating its components.
</CoreArchitecture>

<DecouplingRule>
- Call Down, Signal Up: Parents call child methods. Children emit C# `event/Action` upwards.
- Sibling Isolation: Components MUST NOT reference each other directly.
- Injection: Always use `[Export]` instead of hardcoding `GetNode<T>()`.
</DecouplingRule>

<Reusability>
- Add `[GlobalClass]` to core components for cross-project reuse.
- Hardcode ZERO specific content (e.g., animation names). Expose them via `[Export]`.
</Reusability>

<AntiPatterns_NEVER_DO_THIS>
- NEVER write monolithic `_PhysicsProcess` with endless `if-else`. Use FSMs.
- NEVER tightly couple logic (e.g., Movement should emit `OnJumped`, not call AudioPlayer directly).
</AntiPatterns_NEVER_DO_THIS>

</GodotDesignPatterns>

---

<GodotCompositionRules>

## Entity Rules
- Must be `partial class` with `[Entity]` attribute
- Call `InitializeEntity()` in `_Ready()`
- Zero business logic - container only

## Component Rules
- Must be `partial class` with `[Component(typeof(ParentType))]`
- Call `InitializeComponent()` in `_Ready()`
- Use `[ComponentDependency(typeof(OtherComponent))]` for dependencies
- Subscribe events in `OnEntityReady()`, NOT `_Ready()`
- Unsubscribe in `_ExitTree()` to prevent leaks

## Auto-Generated Variables
- `parent` - Access entity (e.g., `parent.Velocity`)
- `componentName` - Access dependencies (lowercase first letter: `InputComponent` → `inputComponent`)

## Communication
- Components emit events: `public event Action<T> OnSomething;`
- Other components subscribe in `OnEntityReady()`
- Never use `GetNode()` for components
- Never call component methods directly across siblings

## Lifecycle
```
Entity._Ready() → InitializeEntity()
  → Component._Ready() → InitializeComponent()
    → Dependencies resolved
      → Component.OnEntityReady() → Subscribe events
```

**Critical:** Dependencies are null in `_Ready()`. Always subscribe in `OnEntityReady()`.

</GodotCompositionRules>

---

<ReactiveExtensions>

## R3 Reactive Framework

**NuGet:** `R3` + `R3.Godot` (Cysharp, 3.5k stars)

### Core Pattern

```csharp
using R3;

public partial class MyUI : Control
{
    private readonly CompositeDisposable _disposables = new();
    
    public override void _Ready()
    {
        // Single-parameter event (using R3.Godot extension)
        _slider.OnValueChangedAsObservable()
            .Subscribe(v => HandleValue(v))
            .AddTo(_disposables);
        
        // Multi-parameter event (manual conversion required)
        Observable.FromEvent<Action<int, string>, (int, string)>(
            conversion: h => (i, s) => h((i, s)),
            addHandler: h => _dropdown.ItemSelected += h,
            removeHandler: h => _dropdown.ItemSelected -= h
        )
        .Subscribe(x => {
            var (index, text) = x;
            HandleSelection(index, text);
        })
        .AddTo(_disposables);
        
        // Button click (using R3.Godot extension)
        _button.OnPressedAsObservable()
            .Subscribe(_ => HandleClick())
            .AddTo(_disposables);
    }
    
    public override void _ExitTree()
    {
        _disposables.Dispose();
    }
}
```

### Reactive State (ReactiveProperty)

Use `ReactiveProperty<T>` for observable data. UI subscribes once and auto-updates on value changes.

```csharp
// In logic/component
public readonly ReactiveProperty<int> Health = new(100);
public readonly ReactiveProperty<bool> IsAlive = new(true);

// In UI
health.Subscribe(hp => _healthBar.Value = hp).AddTo(_disposables);
isAlive.Subscribe(alive => _deathOverlay.Visible = !alive).AddTo(_disposables);
```

**Rules:**
- Use for discrete state (health, menu open, item count)
- NOT for high-frequency physics data (velocity, position) - use direct properties instead

### Essential Operators

| Operator | Use Case | Example |
|----------|----------|---------|
| `DistinctUntilChanged()` | Prevent redundant UI updates | `isGrounded.DistinctUntilChanged()` - only trigger on state change |
| `ThrottleFirst(TimeSpan)` | Button debounce | `_saveButton.OnPressedAsObservable().ThrottleFirst(0.5s)` |
| `Debounce(TimeSpan)` | Search input delay | `_searchBox.OnTextChangedAsObservable().Debounce(0.3s)` |
| `Where(predicate)` | Filter events | `.Where(hp => hp < 20)` - only when low health |
| `CombineLatest` | Multi-condition logic | Enable submit only if name valid AND age >= 18 |
| `Select` | Transform value | `.Select(v => v * 100)` - convert to percentage |
| `Pairwise()` | Get (previous, current) | Calculate damage delta for animation |
| `Chunk(TimeSpan)` | Batch events | Combine multiple hits in 0.5s window |

### Advanced Patterns

**Multi-condition UI:**
```csharp
Observable.CombineLatest(
    _nameInput.OnTextChangedAsObservable(),
    _ageInput.OnValueChangedAsObservable(),
    (name, age) => !string.IsNullOrEmpty(name) && age >= 18
)
.Subscribe(isValid => _submitButton.Disabled = !isValid)
.AddTo(_disposables);
```

**Async + Thread Safety:**
```csharp
Observable.FromAsync(async ct => await FetchDataAsync(ct))
    .ObserveOn(GodotProvider.MainThread) // CRITICAL: return to main thread
    .Subscribe(data => _label.Text = data)
    .AddTo(_disposables);
```

**Frame-based polling:**
```csharp
Observable.EveryUpdate()
    .Select(_ => _player.Velocity)
    .DistinctUntilChanged()
    .Subscribe(v => _speedLabel.Text = $"{v.Length():F1}")
    .AddTo(_disposables);
```

### Mandatory Rules

1. **DisposeBag**: Every UI class must have `CompositeDisposable _disposables`
2. **AddTo**: Every `.Subscribe()` must end with `.AddTo(_disposables)`
3. **Dispose**: Call `_disposables.Dispose()` in `_ExitTree()`
4. **Thread Safety**: Use `ObserveOn(GodotProvider.MainThread)` after async operations
5. **Performance**: Add `DistinctUntilChanged()` to prevent redundant updates
6. **Debounce**: Use `ThrottleFirst` on buttons to prevent spam clicks

### R3.Godot Extensions

R3.Godot plugin provides built-in helpers (note the `On` prefix):

```csharp
_button.OnPressedAsObservable()           // Button.Pressed event
_toggle.OnToggledAsObservable()           // BaseButton.Toggled event (returns current state on subscribe)
_slider.OnValueChangedAsObservable()      // Range.ValueChanged event (returns current value on subscribe)
_lineEdit.OnTextChangedAsObservable()     // LineEdit.TextChanged event
_lineEdit.OnTextSubmittedAsObservable()   // LineEdit.TextSubmitted event
_optionButton.OnItemSelectedAsObservable() // OptionButton.ItemSelected event (returns current selection on subscribe)
Observable.EveryUpdate()                  // Runs every _Process frame
Observable.EveryPhysicsUpdate()           // Runs every _PhysicsProcess frame
```

**Prefer extensions over `FromEvent` when available. Extensions with "current value on subscribe" emit the current state immediately, ensuring UI consistency.**

### Advanced Optimization

**AsUnitObservable()** - Convert value stream to action stream:
```csharp
_slider.OnValueChangedAsObservable()
    .AsUnitObservable()  // Discard value, only care that it changed
    .Subscribe(_ => SaveSettings())
    .AddTo(_disposables);
```

**Thread Safety (Async):**
```csharp
Observable.FromAsync(async ct => await FetchDataAsync(ct))
    .ObserveOn(GodotProvider.MainThread)  // CRITICAL: jump back to main thread
    .Subscribe(data => _label.Text = data)
    .AddTo(_disposables);
```

**Performance Rule:** Use `DistinctUntilChanged()` on all high-frequency streams (physics, frame updates) to prevent redundant UI redraws.

### Anti-Patterns

❌ **Missing AddTo:**
```csharp
_button.OnPressedAsObservable().Subscribe(_ => DoSomething()); // MEMORY LEAK
```

✅ **Correct:**
```csharp
_button.OnPressedAsObservable().Subscribe(_ => DoSomething()).AddTo(_disposables);
```

❌ **ReactiveProperty for physics:**
```csharp
public ReactiveProperty<Vector3> Velocity = new(); // BAD: updates every frame
```

✅ **Use direct property + polling:**
```csharp
public Vector3 Velocity { get; set; }
Observable.EveryUpdate().Select(_ => Velocity).DistinctUntilChanged()...
```

❌ **Async without thread switch:**
```csharp
Observable.FromAsync(async ct => await FetchAsync(ct))
    .Subscribe(data => _label.Text = data); // CRASH: wrong thread
```

✅ **Correct:**
```csharp
Observable.FromAsync(async ct => await FetchAsync(ct))
    .ObserveOn(GodotProvider.MainThread)
    .Subscribe(data => _label.Text = data)
    .AddTo(_disposables);
```

</ReactiveExtensions>
