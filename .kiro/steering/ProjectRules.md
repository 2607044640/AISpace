---
inclusion: manual
---

# Godot Project Rules

<context>
Godot 4.6.1 Mono (C#), 3D character controller with StateChart integration + UI组件系统
Component architecture via Godot.Composition plugin
</context>

## UI组件Helper模式

所有UI组件Helper遵循MarginContainerHelper的设计模式：

**核心特性：**
- `[Tool]` - 编辑器中实时预览
- `[GlobalClass]` - 跨项目复用
- 属性setter立即更新UI - 修改参数即刻生效
- C# event Action模式 - 组件发出事件，父节点订阅
- 零硬编码 - 所有内容通过`[Export]`暴露

**模板结构：**
```csharp
[Tool]
[GlobalClass]
public partial class MyComponentHelper : HBoxContainer
{
    // 暴露配置参数
    private string _labelText = "默认文本";
    [Export] 
    public string LabelText 
    { 
        get => _labelText;
        set
        {
            _labelText = value;
            UpdateLabel(); // setter立即更新UI
        }
    }
    
    // C# event Action（非Godot Signal）
    public event Action<float> ValueChanged;
    
    // 内部引用
    private Label _label;
    
    public override void _Ready()
    {
        _label = GetNodeOrNull<Label>("Label");
        UpdateLabel();
        
        // 仅在运行时连接信号
        if (!Engine.IsEditorHint())
        {
            // 连接Godot控件信号
        }
    }
    
    private void UpdateLabel()
    {
        if (_label != null)
            _label.Text = LabelText;
    }
    
    private void OnValueChanged(double value)
    {
        ValueChanged?.Invoke((float)value);
    }
    
    public override void _ExitTree()
    {
        if (!Engine.IsEditorHint())
        {
            // 取消订阅，防止内存泄漏
        }
    }
}
```

**使用方式：**
```csharp
// 在父场景中
[Export] public SliderComponentHelper MusicSlider { get; set; }

public override void _Ready()
{
    MusicSlider.ValueChanged += (value) => {
        // 处理值改变
    };
}

public override void _ExitTree()
{
    MusicSlider.ValueChanged -= OnMusicVolumeChanged;
}
```

## 可用UI组件

**位置：** `3d-practice/addons/A1MyAddon/Helpers/`

### SliderComponentHelper
- 暴露：`LabelText`, `MinValue`, `MaxValue`, `Step`, `DefaultValue`, `TickCount`, `TicksOnBorders`
- 事件：`event Action<float> ValueChanged`, `event Action ResetRequested`
- 特性：HSlider + SpinBox双向同步，SpinBox带上下箭头

### OptionComponentHelper
- 暴露：`LabelText`, `Options[]`, `DefaultIndex`
- 事件：`event Action<int, string> OptionSelected`, `event Action ResetRequested`
- 特性：点击Button弹出PopupMenu

### ToggleComponentHelper
- 暴露：`LabelText`, `DefaultState`
- 事件：`event Action<bool> Toggled`, `event Action ResetRequested`

### DropdownComponentHelper
- 暴露：`LabelText`, `Items[]`, `DefaultIndex`
- 事件：`event Action<int, string> ItemSelected`, `event Action ResetRequested`
- 特性：使用OptionButton控件

## StateChart Power Switch Pattern

Place components as children of AtomicState nodes. Call `AutoBindToParentState()` in `_Ready()`. StateChart controls component lifecycle via `SetProcess()`.

```csharp
public override void _Ready()
{
    _entity = this.GetEntity<Player3D>();
    this.AutoBindToParentState(); // Binds to parent State node
    
    var input = _entity.GetRequiredComponentInChildren<BaseInputComponent>();
    input.OnMovementInput += HandleMovementInput;
}

public override void _PhysicsProcess(double delta)
{
    // Only runs when parent state is active
    ApplyGravity(delta);
}
```

**Scene Structure:**
```
Entity (CharacterBody3D)
├── StateChart
│   └── Root (ParallelState)
│       ├── Movement (CompoundState, initial=Ground)
│       │   ├── Ground (AtomicState)
│       │   │   └── GroundMovementComponent
│       │   └── Fly (AtomicState)
│       │       └── FlyMovementComponent
│       └── Action (CompoundState, initial=Normal)
├── InputComponent (shared)
├── AnimationControllerComponent (listens to state signals)
└── Other shared components
```

**Send Events:**
```csharp
parent.SendStateEvent("toggle_fly");
```

**Connect Signals in Editor:**
- `GroundMode.state_entered` → `AnimationController.EnterGroundMode()`
- `FlyMode.state_entered` → `AnimationController.EnterFlyMode()`

## Component Architecture

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
        
        var input = this.GetEntity<Player3D>()
            .GetRequiredComponentInChildren<BaseInputComponent>();
        input.OnMovementInput += HandleMovementInput;
    }
    
    public override void _ExitTree()
    {
        if (input != null)
            input.OnMovementInput -= HandleMovementInput;
    }
}
```

**Rules:**
- Entities: `[Entity]`, call `InitializeEntity()`, zero business logic
- Components: `[Component(typeof(T))]`, call `InitializeComponent()`, single responsibility
- Subscribe events in `_Ready()` (not `OnEntityReady()` for StateChart components)
- Unsubscribe in `_ExitTree()` to prevent leaks
- Use `this.GetEntity<T>()` to access entity from StateChart child components
- Use `GetRequiredComponentInChildren<T>()` for component lookup

## Animation System

Single file: `CharacterAnimationConfig.cs`

**Add Animation (2 steps):**
```csharp
// 1. Declare
public const string NewAnim = "NewAnim";
[Export] public Animation NewAnimAnimation;
[Export] public float NewAnimSpeed = 1.0f;

// 2. Register in ApplyAndInitialize()
RegisterAnim(library, AnimationNames.NewAnim, NewAnimAnimation, NewAnimSpeed, isLoop: true);
```

## Input Abstraction

```csharp
BaseInputComponent (abstract)
    ↓
PlayerInputComponent (player)
AIInputComponent (AI)
```

Components depend on `BaseInputComponent`, not concrete implementations.

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
// Emit
public event Action<Vector2> OnMovementInput;
OnMovementInput?.Invoke(inputVector);

// Subscribe
input.OnMovementInput += HandleMovementInput;

// Unsubscribe
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

Never check state in components:
```csharp
if (_canMove) { /* logic */ } // WRONG - StateChart controls lifecycle
```

Never reference siblings directly:
```csharp
GetNode<Component>("../Sibling"); // WRONG - Use events
```

Never hardcode animation names:
```csharp
_animPlayer.Play("Idle"); // WRONG - Use AnimationNames.Idle
```

Never use Godot Signal for C# components:
```csharp
[Signal] public delegate void MyEventHandler(); // WRONG - Use C# event Action
```

## Build & Debug

Build: `dotnet build "3dPractice.sln"`
Runtime logs: `Get-Content "$env:APPDATA\Godot\app_userdata\3dPractice\logs\godot.log" -Tail 50`
C# logging: `GD.Print("msg")`, `GD.PrintErr("err")`, `GD.PushWarning("warn")`

## Known Issues

Godot.Composition doesn't register base classes. Use `GetRequiredComponentInChildren<BaseInputComponent>()` instead of `[ComponentDependency]`.

Flying animations missing: Configure fallback in editor: `FlyIdleAnimation` → `ninja_idle.res`. Code has fallback logic.
