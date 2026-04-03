---
inclusion: manual
---

# Godot Project Rules

<context>
Godot 4.6.1 Mono (C#), 3D character controller + UI system
Component architecture via custom Godot.Composition source generator
R3 reactive framework for event management
</context>

## R3 Reactive Framework (NEW)

**NuGet:** `R3` + `R3.Godot`

### Mandatory Pattern

```csharp
using R3;

public partial class MyUI : Control
{
    private readonly CompositeDisposable _disposables = new();
    
    public override void _Ready()
    {
        _button.PressedAsObservable()
            .Subscribe(_ => HandleClick())
            .AddTo(_disposables);
    }
    
    public override void _ExitTree()
    {
        _disposables.Dispose();
    }
}
```

### Rules
1. Every UI class must have `CompositeDisposable _disposables`
2. Every `.Subscribe()` must end with `.AddTo(_disposables)`
3. Call `_disposables.Dispose()` in `_ExitTree()`
4. Use `ObserveOn(GodotProvider.MainThread)` after async
5. Add `DistinctUntilChanged()` to high-frequency streams

### Essential Operators
- `DistinctUntilChanged()` - Prevent redundant updates
- `ThrottleFirst(TimeSpan)` - Button debounce
- `Debounce(TimeSpan)` - Search input delay
- `CombineLatest` - Multi-condition logic
- `Where(predicate)` - Filter events

See `DesignPatterns.md` for complete reference.

## UI Component Helper Pattern

All UI components follow MarginContainerHelper design:

**Core Features:**
- `[Tool]` - Editor live preview
- `[GlobalClass]` - Cross-project reuse
- Property setter updates UI immediately
- C# `event Action` (NOT Godot Signal)
- Zero hardcoding via `[Export]`

**Template:**
```csharp
[Tool]
[GlobalClass]
public partial class MyComponentHelper : HBoxContainer
{
    private string _labelText = "Default";
    [Export] 
    public string LabelText 
    { 
        get => _labelText;
        set
        {
            _labelText = value;
            UpdateLabel(); // Immediate update
        }
    }
    
    public event Action<float> ValueChanged;
    
    private Label _label;
    
    public override void _Ready()
    {
        _label = GetNodeOrNull<Label>("Label");
        UpdateLabel();
        
        if (!Engine.IsEditorHint())
        {
            // Connect signals
        }
    }
    
    private void UpdateLabel()
    {
        if (_label != null)
            _label.Text = LabelText;
    }
    
    public override void _ExitTree()
    {
        if (!Engine.IsEditorHint())
        {
            // Unsubscribe
        }
    }
}
```

## Available UI Components

**Location:** `3d-practice/addons/A1MyAddon/Helpers/`

- `SliderComponentHelper` - HSlider + SpinBox sync
- `OptionComponentHelper` - Button + PopupMenu
- `ToggleComponentHelper` - CheckBox wrapper
- `DropdownComponentHelper` - OptionButton wrapper

All emit `event Action` and `event Action ResetRequested`.

## StateChart Power Switch Pattern

Components as children of AtomicState nodes. Call `AutoBindToParentState()` in `_Ready()`. StateChart controls lifecycle via `SetProcess()`.

```csharp
public override void _Ready()
{
    _entity = this.GetEntity<Player3D>();
    this.AutoBindToParentState();
    
    var input = _entity.GetRequiredComponentInChildren<BaseInputComponent>();
    input.OnMovementInput += HandleMovementInput;
}
```

**Scene Structure:**
```
Entity (CharacterBody3D)
├── StateChart
│   └── Root (ParallelState)
│       ├── Movement (CompoundState)
│       │   ├── Ground (AtomicState)
│       │   │   └── GroundMovementComponent
│       │   └── Fly (AtomicState)
│       │       └── FlyMovementComponent
│       └── Action (CompoundState)
├── InputComponent
├── AnimationControllerComponent
└── Other components
```

**Send Events:**
```csharp
parent.SendStateEvent("toggle_fly");
```

## Component Architecture (Godot.Composition)

**Entity:**
```csharp
[Entity]
public partial class Player3D : CharacterBody3D
{
    public override void _Ready()
    {
        InitializeEntity();
    }
}
```

**Component:**
```csharp
[Component(typeof(CharacterBody3D))]
[GlobalClass]
public partial class GroundMovementComponent : Node
{
    public override void _Ready()
    {
        InitializeComponent();
        this.AutoBindToParentState();
    }
    
    public override void _ExitTree()
    {
        // Unsubscribe events
    }
}
```

**Rules:**
- Entities: `[Entity]`, call `InitializeEntity()`, zero logic
- Components: `[Component(typeof(T))]`, call `InitializeComponent()`
- Subscribe in `_Ready()` (NOT `OnEntityReady()` for StateChart)
- Unsubscribe in `_ExitTree()`
- Use `this.GetEntity<T>()` from StateChart children
- Use `GetRequiredComponentInChildren<T>()` for lookup

## Animation System

Single file: `CharacterAnimationConfig.cs`

**Add Animation:**
```csharp
// 1. Declare
public const string NewAnim = "NewAnim";
[Export] public Animation NewAnimAnimation;
[Export] public float NewAnimSpeed = 1.0f;

// 2. Register
RegisterAnim(library, AnimationNames.NewAnim, NewAnimAnimation, NewAnimSpeed, isLoop: true);
```

## Input Abstraction

```
BaseInputComponent (abstract)
    ↓
PlayerInputComponent | AIInputComponent
```

Components depend on `BaseInputComponent`, not concrete types.

## Available Components

**Location:** `3d-practice/addons/A1MyAddon/CoreComponents/`

- `GroundMovementComponent` - Gravity, jump, ground physics
- `FlyMovementComponent` - 3D flight, no gravity
- `PlayerInputComponent` - Keyboard/gamepad input
- `BaseInputComponent` - Abstract input base
- `CharacterRotationComponent` - Face movement direction
- `AnimationControllerComponent` - Animation playback
- `CameraControlComponent` - PhantomCamera3D control

## Code Patterns

**Events:**
```csharp
public event Action<Vector2> OnMovementInput;
OnMovementInput?.Invoke(inputVector);

input.OnMovementInput += HandleMovementInput;
input.OnMovementInput -= HandleMovementInput;
```

**StateChart:**
```csharp
parent.SendStateEvent("toggle_fly");
```

**Component Lookup:**
```csharp
var entity = this.GetEntity<Player3D>();
var input = entity.GetRequiredComponentInChildren<BaseInputComponent>();
```

## Prohibited Patterns

❌ State checks in components:
```csharp
if (_canMove) { /* logic */ } // WRONG - StateChart controls lifecycle
```

❌ Direct sibling references:
```csharp
GetNode<Component>("../Sibling"); // WRONG - Use events
```

❌ Hardcoded animation names:
```csharp
_animPlayer.Play("Idle"); // WRONG - Use AnimationNames.Idle
```

❌ Godot Signal for C# components:
```csharp
[Signal] public delegate void MyEventHandler(); // WRONG - Use event Action
```

❌ Missing R3 AddTo:
```csharp
_button.PressedAsObservable().Subscribe(_ => DoSomething()); // MEMORY LEAK
```

## Build & Debug

Build: `dotnet build "3dPractice.sln"`
Logs: `Get-Content "$env:APPDATA\Godot\app_userdata\3dPractice\logs\godot.log" -Tail 50`
C# logging: `GD.Print()`, `GD.PrintErr()`, `GD.PushWarning()`

## Known Issues

- Godot.Composition doesn't register base classes - use `GetRequiredComponentInChildren<BaseInputComponent>()`
- Flying animations missing - configure fallback in editor
