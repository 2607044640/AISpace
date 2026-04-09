# Godot Project Rules
<context>
Godot 4.6.1 Mono (C#), 3D character controller + Grid inventory system
Component architecture via custom Godot.Composition source generator
R3 reactive framework for event management
StateChart for lifecycle control
</context>
## Grid Inventory System (NEW)
**Location:** `3d-practice/B1Scripts/Components/`, `3d-practice/B1Scripts/Resources/`
### Component Architecture
**6-Layer System:**
1. **Data Layer:** `BackpackGridComponent` - 1D array grid logic
2. **Resource Layer:** `ItemDataResource` - Static item configuration
3. **Shape Layer:** `GridShapeComponent` - Runtime shape + rotation
4. **Input Layer:** `DraggableItemComponent` - GUI input → StateChart bridge
5. **Physics Layer:** `FollowMouseUIComponent` - Mouse tracking (Power Switch)
6. **View Layer:** `BackpackGridUIComponent` - Coordinate conversion
### Mandatory Rules
**Grid Logic:**
- MUST use 1D array: `ItemData[] _gridData`
- MUST use formula: `index = y * Width + x`
- MUST validate bounds before array access
- MUST clear cells when removing items
**Shape Management:**
- MUST call `NormalizeShape()` after rotation
- MUST use rotation matrix: `(x,y) → (-y,x)` for 90° clockwise
- MUST convert `Godot.Collections.Array<Vector2I>` to `Vector2I[]` for runtime
**StateChart Communication:**
- MUST use `StateChart.Call("send_event", "event_name")`
- NEVER use `GetParent()?.Call()` when StateChart reference exists
- MUST verify StateChart reference before calling
**Coordinate Conversion:**
- MUST use `BackpackGridUIComponent` for all pixel↔grid conversions
- NEVER manually calculate coordinates in business logic
- MUST use `GlobalToGridPosition()` for mouse input
- MUST use `GridToLocalPosition()` for item placement
**R3 Integration:**
- MUST use `Subject<Unit>` for parameterless events
- MUST call `OnNext(Unit.Default)` to emit
- MUST dispose all Subjects in `_ExitTree()`
See `GridInventorySystem_Context.md` for complete technical reference.
## R3 Reactive Framework
**NuGet:** `R3` + `R3.Godot`
### Mandatory Pattern
```csharp
using R3;
public partial class MyUI : Control
{
    private readonly CompositeDisposable _disposables = new();
    
    public override void _Ready()
    {
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
### Rules
1. Every UI class must have `CompositeDisposable _disposables`
2. Every `.Subscribe()` must end with `.AddTo(_disposables)`
3. Call `_disposables.Dispose()` in `_ExitTree()`
4. Use `ObserveOn(GodotProvider.MainThread)` after async
5. Add `DistinctUntilChanged()` to high-frequency streams
### R3.Godot Extensions
```csharp
_button.OnPressedAsObservable()           // Button.Pressed
_toggle.OnToggledAsObservable()           // BaseButton.Toggled (emits current state)
_slider.OnValueChangedAsObservable()      // Range.ValueChanged (emits current value)
_lineEdit.OnTextChangedAsObservable()     // LineEdit.TextChanged
_optionButton.OnItemSelectedAsObservable() // OptionButton.ItemSelected (emits current)
Observable.EveryUpdate()                  // _Process frame
Observable.EveryPhysicsUpdate()           // _PhysicsProcess frame
```
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
            UpdateLabel();
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
StateChart.Call("send_event", "event_name"); // Direct call
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
**Location:** `3d-practice/B1Scripts/Components/`
- `BackpackGridComponent` - Grid data logic
- `GridShapeComponent` - Item shape + rotation
- `DraggableItemComponent` - Drag input handler
- `FollowMouseUIComponent` - Mouse follower
- `BackpackGridUIComponent` - Coordinate converter
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
StateChart.Call("send_event", "drag_start");
```
**Component Lookup:**
```csharp
var entity = this.GetEntity<Player3D>();
var input = entity.GetRequiredComponentInChildren<BaseInputComponent>();
```
**Coordinate Conversion:**
```csharp
var gridPos = backpackUI.GlobalToGridPosition(GetGlobalMousePosition());
item.Position = backpackUI.GridToLocalPosition(new Vector2I(2, 3));
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
_button.OnPressedAsObservable().Subscribe(_ => DoSomething()); // MEMORY LEAK
```
❌ Manual coordinate calculation:
```csharp
int gridX = (int)(mousePos.X / 64); // WRONG - Use BackpackGridUIComponent
```
❌ 2D array for grid:
```csharp
ItemData[,] grid = new ItemData[10, 6]; // WRONG - Use 1D array
```
## Build & Debug
Build: `dotnet build` (run in 3d-practice directory)
Logs: `Get-Content "$env:APPDATA\Godot\app_userdata\3dPractice\logs\godot.log" -Tail 50`
C# logging: `GD.Print()`, `GD.PrintErr()`, `GD.PushWarning()`
## Known Issues
- Godot.Composition doesn't register base classes - use `GetRequiredComponentInChildren<BaseInputComponent>()`
- Flying animations missing - configure fallback in editor
