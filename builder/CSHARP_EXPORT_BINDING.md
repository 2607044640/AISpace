# C# Export NodePath Binding - The Killer Feature

## Overview

The `assign_node_path()` and `assign_multiple_node_paths()` methods are the killer features for C# architecture in Godot. They eliminate manual NodePath calculation and enable clean MVC separation with pure C# events and R3 reactive extensions.

## The Problem

In traditional Godot workflows:

1. **Manual NodePath Calculation**: You manually write `NodePath("../../UI/Button")` which is error-prone
2. **Godot Signal Connections**: `.tscn` files contain `[connection]` blocks that tightly couple UI to logic
3. **Fragile Refactoring**: Moving nodes breaks hardcoded paths

## The Solution

TscnBuilder automatically calculates and assigns NodePaths to C# [Export] properties:

```python
# 1. Create UI
ui.add_button("ApplyButton", parent="MainVBox", text="Apply")

# 2. Create C# Controller
scene.add_node("SettingsController", "Node", parent=".",
              script=ExtResource("controller_script"))

# 3. Automatically bind
scene.assign_node_path("SettingsController", "ApplyButton", "ApplyButton")
```

Generated TSCN:
```gdscript
[node name="SettingsController" type="Node" parent="."]
script = ExtResource("1_res")
ApplyButton = NodePath("../MainVBox/ApplyButton")
```

## API Reference

### Single Assignment

```python
scene.assign_node_path(
    target_node_name: str,    # Node with [Export] property
    property_name: str,       # Property name
    path_to_node_name: str    # Node to assign
)
```

**Example**:
```python
scene.assign_node_path("Controller", "HealthBar", "HealthBar")
```

### Batch Assignment

```python
scene.assign_multiple_node_paths(
    target_node_name: str,    # Node with [Export] properties
    bindings: dict            # {property_name: node_name}
)
```

**Example**:
```python
scene.assign_multiple_node_paths("Controller", {
    "HealthBar": "HealthBar",
    "StaminaBar": "StaminaBar",
    "ApplyButton": "ApplyButton",
    "CancelButton": "CancelButton"
})
```

## Complete MVC Example

### Python Scene Generation

```python
from builder.core import TscnBuilder
from builder.modules.ui import UIModule

# Create scene
scene = TscnBuilder(root_name="SettingsUI", root_type="Control")
ui = UIModule(scene)
ui.setup_fullscreen_control()

# Build UI
ui.add_vbox("MainVBox", parent=".", separation=10)
ui.add_label("Title", parent="MainVBox", text="Settings", font_size=24)
ui.add_progress_bar("VolumeSlider", parent="MainVBox", value=80)
ui.add_checkbox("FullscreenCheck", parent="MainVBox", button_pressed=True)
ui.add_button("ApplyButton", parent="MainVBox", text="Apply")
ui.add_button("CancelButton", parent="MainVBox", text="Cancel")

# Add C# Controller
controller_res_id = scene.add_ext_resource(
    "Script", 
    "res://Scripts/SettingsController.cs", 
    "uid://controller_uid"
)
scene.add_node("Controller", "Node", parent=".",
              script=f'ExtResource("{controller_res_id}")')

# Bind UI to Controller
scene.assign_multiple_node_paths("Controller", {
    "TitleLabel": "Title",
    "VolumeSlider": "VolumeSlider",
    "FullscreenCheck": "FullscreenCheck",
    "ApplyButton": "ApplyButton",
    "CancelButton": "CancelButton"
})

scene.save("SettingsUI.tscn")
```

### C# Controller Implementation

```csharp
using Godot;
using R3;
using System;

[GlobalClass]
public partial class SettingsController : Node
{
    // [Export] properties automatically bound by TscnBuilder
    [Export] public NodePath TitleLabel { get; set; }
    [Export] public NodePath VolumeSlider { get; set; }
    [Export] public NodePath FullscreenCheck { get; set; }
    [Export] public NodePath ApplyButton { get; set; }
    [Export] public NodePath CancelButton { get; set; }
    
    private CompositeDisposable _disposables = new();
    
    public override void _Ready()
    {
        InitializeComponent();
        BindEvents();
    }
    
    private void InitializeComponent()
    {
        // Get node references
        var titleLabel = GetNode<Label>(TitleLabel);
        var volumeSlider = GetNode<ProgressBar>(VolumeSlider);
        var fullscreenCheck = GetNode<CheckBox>(FullscreenCheck);
        var applyButton = GetNode<Button>(ApplyButton);
        var cancelButton = GetNode<Button>(CancelButton);
    }
    
    private void BindEvents()
    {
        // Pure C# events with R3 reactive extensions
        GetNode<Button>(ApplyButton).OnPressedAsObservable()
            .Subscribe(_ => ApplySettings())
            .AddTo(_disposables);
        
        GetNode<Button>(CancelButton).OnPressedAsObservable()
            .Subscribe(_ => CancelSettings())
            .AddTo(_disposables);
        
        // React to checkbox changes
        GetNode<CheckBox>(FullscreenCheck).OnToggledAsObservable()
            .Subscribe(isFullscreen => UpdateFullscreen(isFullscreen))
            .AddTo(_disposables);
        
        // React to slider changes with debounce
        GetNode<ProgressBar>(VolumeSlider).OnValueChangedAsObservable()
            .Debounce(TimeSpan.FromMilliseconds(100))
            .Subscribe(volume => UpdateVolume(volume))
            .AddTo(_disposables);
    }
    
    private void ApplySettings()
    {
        GD.Print("Settings applied!");
    }
    
    private void CancelSettings()
    {
        GD.Print("Settings cancelled!");
    }
    
    private void UpdateFullscreen(bool isFullscreen)
    {
        DisplayServer.WindowSetMode(
            isFullscreen ? DisplayServer.WindowMode.Fullscreen : DisplayServer.WindowMode.Windowed
        );
    }
    
    private void UpdateVolume(double volume)
    {
        AudioServer.SetBusVolumeDb(0, (float)GD.LinearToDb(volume / 100.0));
    }
    
    public override void _ExitTree()
    {
        _disposables.Dispose();
    }
}
```

## Benefits

### 1. No Manual NodePath Calculation

**Before** (Manual):
```csharp
[Export] public NodePath ApplyButton { get; set; } = new NodePath("../MainMargin/MainVBox/ButtonRow/ApplyButton");
```

**After** (Automatic):
```python
scene.assign_node_path("Controller", "ApplyButton", "ApplyButton")
```

### 2. Refactoring Safety

When you move UI nodes in the hierarchy, TscnBuilder automatically recalculates paths. No broken references.

### 3. Clean Separation of Concerns

- **Python**: Scene structure and layout
- **C#**: Business logic and event handling
- **No mixing**: UI and logic remain decoupled

### 4. Pure C# Events

No Godot signal connections in `.tscn` files. Everything is pure C# with R3 reactive extensions:

```csharp
GetNode<Button>(ApplyButton).OnPressedAsObservable()
    .ThrottleFirst(TimeSpan.FromMilliseconds(500))  // Prevent double-clicks
    .Subscribe(_ => ApplySettings())
    .AddTo(_disposables);
```

### 5. Type Safety

C# compiler catches errors at compile time:

```csharp
var button = GetNode<Button>(ApplyButton);  // Type-safe
button.OnPressedAsObservable()              // IntelliSense support
```

## Advanced Patterns

### Pattern 1: Nested Controllers

```python
# Parent controller
scene.add_node("GameController", "Node", parent=".", script=...)

# Child controllers
scene.add_node("UIController", "Node", parent="GameController", script=...)
scene.add_node("AudioController", "Node", parent="GameController", script=...)

# Bind UI to child controller
scene.assign_multiple_node_paths("UIController", {
    "HealthBar": "HealthBar",
    "StaminaBar": "StaminaBar"
})

# Bind audio controls to audio controller
scene.assign_multiple_node_paths("AudioController", {
    "MasterVolume": "MasterVolumeSlider",
    "MusicVolume": "MusicVolumeSlider"
})
```

### Pattern 2: Cross-Hierarchy Bindings

```python
# UI in one branch
ui.add_button("ActionButton", parent="LeftPanel")

# Controller in another branch
scene.add_node("Controller", "Node", parent="RightPanel", script=...)

# Automatic cross-hierarchy path calculation
scene.assign_node_path("Controller", "ActionButton", "ActionButton")
# Generates: NodePath("../../LeftPanel/ActionButton")
```

### Pattern 3: Dynamic UI Generation

```python
# Generate 10 inventory slots
for i in range(10):
    ui.add_button(f"Slot{i}", parent="InventoryGrid", text=f"Slot {i}")

# Bind all slots to controller
bindings = {f"Slot{i}": f"Slot{i}" for i in range(10)}
scene.assign_multiple_node_paths("InventoryController", bindings)
```

## Error Handling

The API provides clear error messages:

```python
# Non-existent target node
scene.assign_node_path("NonExistentController", "Button", "Button")
# ValueError: Target node 'NonExistentController' not found in registry

# Non-existent path node
scene.assign_node_path("Controller", "Button", "NonExistentButton")
# ValueError: Path-to node 'NonExistentButton' not found in registry
```

## Comparison with Godot Signals

### Traditional Godot Signals (Avoid)

`.tscn` file:
```gdscript
[connection signal="pressed" from="ApplyButton" to="." method="_on_apply_button_pressed"]
```

C# code:
```csharp
private void _on_apply_button_pressed()
{
    // Tightly coupled to signal name
}
```

**Problems**:
- Signal names are strings (no type safety)
- Refactoring breaks connections
- Logic mixed with UI in `.tscn`

### C# Export Binding (Recommended)

`.tscn` file:
```gdscript
[node name="Controller" type="Node" parent="."]
script = ExtResource("1_res")
ApplyButton = NodePath("../MainVBox/ApplyButton")
```

C# code:
```csharp
[Export] public NodePath ApplyButton { get; set; }

public override void _Ready()
{
    GetNode<Button>(ApplyButton).OnPressedAsObservable()
        .Subscribe(_ => ApplySettings())
        .AddTo(_disposables);
}
```

**Benefits**:
- Type-safe node access
- Pure C# events
- Clean separation
- Refactoring-safe

## Best Practices

1. **Use Batch Assignment**: For multiple bindings, use `assign_multiple_node_paths()`
2. **Consistent Naming**: Use same name for UI node and property (e.g., "ApplyButton" for both)
3. **Controller Per Feature**: Create separate controllers for different UI sections
4. **Dispose Subscriptions**: Always call `_disposables.Dispose()` in `_ExitTree()`
5. **Validate in _Ready**: Check that all NodePaths are valid in `_Ready()`

## Testing

See `builder/tests/test_5_export_nodepath_binding.py` for comprehensive tests:

- ✅ Single assignment
- ✅ Batch assignments
- ✅ Cross-hierarchy paths
- ✅ Error handling
- ✅ TSCN format validation

## Conclusion

The C# Export NodePath binding feature transforms Godot C# development by:

1. Eliminating manual NodePath calculation
2. Enabling clean MVC architecture
3. Supporting pure C# events with R3
4. Providing refactoring safety
5. Maintaining type safety

This is the killer feature that makes TscnBuilder essential for serious C# Godot projects.
