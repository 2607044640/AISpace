# StateChart Component MVC Pattern

## The Most Elegant Workflow

Combining StateChart components with C# Export binding creates the most elegant MVC pattern for Godot:

```python
# 1. Create visual UI (View)
ui.add_button("ApplyButton", parent="MainVBox", text="Apply")
ui.add_progress_bar("VolumeSlider", parent="MainVBox", value=80)

# 2. Create StateChart with states (State Management)
sc.add_statechart("StateChart")
sc.add_compound_state("Root", parent="StateChart", initial_state="Editing")
sc.add_atomic_state("Editing", parent="Root")

# 3. Add C# component to state (Controller)
sc.add_component(
    name="SettingsController",
    parent="Editing",
    script_path="res://B1Scripts/UI/SettingsController.cs",
    script_uid="uid://..."
)

# 4. Bind UI to component [Export] properties automatically! (Wiring)
scene.assign_multiple_node_paths("SettingsController", {
    "ApplyButton": "ApplyButton",
    "VolumeSlider": "VolumeSlider"
})
```

## Why This Pattern is Superior

### 1. State-Based Controllers

Controllers are attached to specific states, so they only run when that state is active:

```python
# Active state has its own controller
sc.add_component("HUDActiveController", parent="Active", ...)

# Paused state has its own controller
sc.add_component("HUDPausedController", parent="Paused", ...)
```

**Benefits**:
- Controllers automatically activate/deactivate with state changes
- No manual enable/disable logic needed
- Clean separation of state-specific behavior

### 2. Automatic Lifecycle Management

C# components in StateChart states have built-in lifecycle hooks:

```csharp
public partial class SettingsController : Node
{
    [Export] public NodePath ApplyButton { get; set; }
    [Export] public NodePath VolumeSlider { get; set; }
    
    private CompositeDisposable _disposables = new();
    
    // Called when state is entered
    public override void OnStateEnter()
    {
        // Setup UI bindings
        GetNode<Button>(ApplyButton).OnPressedAsObservable()
            .Subscribe(_ => ApplySettings())
            .AddTo(_disposables);
        
        GetNode<ProgressBar>(VolumeSlider).OnValueChangedAsObservable()
            .Debounce(TimeSpan.FromMilliseconds(100))
            .Subscribe(volume => UpdateVolume(volume))
            .AddTo(_disposables);
    }
    
    // Called when state is exited
    public override void OnStateExit()
    {
        // Cleanup subscriptions
        _disposables.Dispose();
        _disposables = new();
    }
}
```

### 3. Zero Manual Path Calculation

The `assign_node_path()` method automatically calculates complex relative paths:

```python
# Component is at: StateChart/Root/Editing/SettingsController
# UI is at: MainMargin/MainVBox/ButtonRow/ApplyButton

scene.assign_node_path("SettingsController", "ApplyButton", "ApplyButton")

# Generated TSCN:
# ApplyButton = NodePath("../../../../MainMargin/MainVBox/ButtonRow/ApplyButton")
```

**No manual calculation needed!** The builder handles the `../../../../` traversal automatically.

## Complete Example: Settings Menu

### Python Scene Generation

```python
from builder.core import TscnBuilder
from builder.modules.ui import UIModule
from builder.modules.statechart import StateChartModule

# Create scene
scene = TscnBuilder(root_name="SettingsMenu", root_type="Control")

# Build UI
ui = UIModule(scene)
ui.setup_fullscreen_control()
ui.add_vbox("MainVBox", parent=".", separation=10)
ui.add_progress_bar("MasterVolume", parent="MainVBox", value=80)
ui.add_progress_bar("MusicVolume", parent="MainVBox", value=70)
ui.add_checkbox("Fullscreen", parent="MainVBox", button_pressed=True)
ui.add_button("ApplyButton", parent="MainVBox", text="Apply")
ui.add_button("CancelButton", parent="MainVBox", text="Cancel")

# Create StateChart
sc = StateChartModule(scene, parent=".")
sc.add_statechart("StateChart")
sc.add_compound_state("Root", parent="StateChart", initial_state="Idle")
sc.add_atomic_state("Idle", parent="Root")
sc.add_atomic_state("Editing", parent="Root")
sc.add_atomic_state("Applying", parent="Root")

# Add transitions
sc.add_transition("ToEditing", from_state="Idle", to_state="Editing", event="start_edit")
sc.add_transition("ToApplying", from_state="Editing", to_state="Applying", event="apply")
sc.add_transition("ToIdle", from_state="Applying", to_state="Idle", event="complete")

sc.resolve_initial_states()

# Add C# component to Editing state
sc.add_component(
    name="SettingsController",
    parent="Editing",
    script_path="res://B1Scripts/UI/SettingsController.cs",
    script_uid="uid://settings_controller"
)

# Bind UI to component
scene.assign_multiple_node_paths("SettingsController", {
    "MasterVolume": "MasterVolume",
    "MusicVolume": "MusicVolume",
    "Fullscreen": "Fullscreen",
    "ApplyButton": "ApplyButton",
    "CancelButton": "CancelButton"
})

scene.save("SettingsMenu.tscn")
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
    [Export] public NodePath MasterVolume { get; set; }
    [Export] public NodePath MusicVolume { get; set; }
    [Export] public NodePath Fullscreen { get; set; }
    [Export] public NodePath ApplyButton { get; set; }
    [Export] public NodePath CancelButton { get; set; }
    
    private CompositeDisposable _disposables = new();
    private float _masterVolume;
    private float _musicVolume;
    private bool _fullscreen;
    
    // Called when Editing state is entered
    public override void OnStateEnter()
    {
        GD.Print("SettingsController: State entered - setting up UI");
        
        // Load current settings
        LoadCurrentSettings();
        
        // Bind UI events with R3 reactive extensions
        BindUIEvents();
    }
    
    private void LoadCurrentSettings()
    {
        _masterVolume = AudioServer.GetBusVolumeDb(0);
        _musicVolume = AudioServer.GetBusVolumeDb(1);
        _fullscreen = DisplayServer.WindowGetMode() == DisplayServer.WindowMode.Fullscreen;
        
        // Update UI to reflect current settings
        GetNode<ProgressBar>(MasterVolume).Value = _masterVolume;
        GetNode<ProgressBar>(MusicVolume).Value = _musicVolume;
        GetNode<CheckBox>(Fullscreen).ButtonPressed = _fullscreen;
    }
    
    private void BindUIEvents()
    {
        // Master volume slider with debounce
        GetNode<ProgressBar>(MasterVolume).OnValueChangedAsObservable()
            .Debounce(TimeSpan.FromMilliseconds(100))
            .Subscribe(volume => {
                _masterVolume = (float)volume;
                PreviewMasterVolume(volume);
            })
            .AddTo(_disposables);
        
        // Music volume slider with debounce
        GetNode<ProgressBar>(MusicVolume).OnValueChangedAsObservable()
            .Debounce(TimeSpan.FromMilliseconds(100))
            .Subscribe(volume => {
                _musicVolume = (float)volume;
                PreviewMusicVolume(volume);
            })
            .AddTo(_disposables);
        
        // Fullscreen checkbox
        GetNode<CheckBox>(Fullscreen).OnToggledAsObservable()
            .Subscribe(isFullscreen => {
                _fullscreen = isFullscreen;
            })
            .AddTo(_disposables);
        
        // Apply button with throttle to prevent double-clicks
        GetNode<Button>(ApplyButton).OnPressedAsObservable()
            .ThrottleFirst(TimeSpan.FromMilliseconds(500))
            .Subscribe(_ => ApplySettings())
            .AddTo(_disposables);
        
        // Cancel button
        GetNode<Button>(CancelButton).OnPressedAsObservable()
            .ThrottleFirst(TimeSpan.FromMilliseconds(500))
            .Subscribe(_ => CancelSettings())
            .AddTo(_disposables);
    }
    
    private void PreviewMasterVolume(double volume)
    {
        AudioServer.SetBusVolumeDb(0, (float)GD.LinearToDb(volume / 100.0));
    }
    
    private void PreviewMusicVolume(double volume)
    {
        AudioServer.SetBusVolumeDb(1, (float)GD.LinearToDb(volume / 100.0));
    }
    
    private void ApplySettings()
    {
        GD.Print("Applying settings...");
        
        // Apply fullscreen
        DisplayServer.WindowSetMode(
            _fullscreen ? DisplayServer.WindowMode.Fullscreen : DisplayServer.WindowMode.Windowed
        );
        
        // Save settings to config file
        SaveSettings();
        
        // Trigger state transition to Applying state
        EmitSignal("apply_complete");
    }
    
    private void CancelSettings()
    {
        GD.Print("Canceling settings...");
        
        // Restore original settings
        LoadCurrentSettings();
        
        // Trigger state transition back to Idle
        EmitSignal("cancel");
    }
    
    private void SaveSettings()
    {
        var config = new ConfigFile();
        config.SetValue("audio", "master_volume", _masterVolume);
        config.SetValue("audio", "music_volume", _musicVolume);
        config.SetValue("video", "fullscreen", _fullscreen);
        config.Save("user://settings.cfg");
    }
    
    // Called when Editing state is exited
    public override void OnStateExit()
    {
        GD.Print("SettingsController: State exited - cleaning up");
        
        // Dispose all subscriptions
        _disposables.Dispose();
        _disposables = new();
    }
}
```

## Benefits Summary

### 1. Clean Architecture
- **View**: UI created with UIModule
- **State Management**: StateChart manages state transitions
- **Controller**: C# components handle logic per state
- **Wiring**: Automatic NodePath binding

### 2. Automatic Lifecycle
- Controllers activate when state is entered
- Controllers deactivate when state is exited
- No manual enable/disable needed

### 3. Zero Manual Paths
- `assign_node_path()` calculates all relative paths
- Refactoring-safe (paths recalculated automatically)
- No `../../../../` path errors

### 4. Type-Safe Events
- Pure C# with R3 reactive extensions
- No Godot signals in `.tscn` files
- IntelliSense support
- Compile-time checking

### 5. Scalable
- Multiple controllers per state machine
- Controllers can reference same UI elements
- State-specific behavior isolated

## Comparison with Traditional Approach

### Traditional (Manual)

```csharp
// ❌ Manual NodePath calculation
[Export] public NodePath ApplyButton { get; set; } = 
    new NodePath("../../../../MainMargin/MainVBox/ButtonRow/ApplyButton");

// ❌ Manual lifecycle management
public override void _Ready()
{
    if (_isActive)
    {
        SetupUI();
    }
}

public void SetActive(bool active)
{
    _isActive = active;
    if (active)
    {
        SetupUI();
    }
    else
    {
        CleanupUI();
    }
}
```

### StateChart Component (Automatic)

```python
# ✅ Automatic NodePath calculation
sc.add_component("SettingsController", parent="Editing", ...)
scene.assign_node_path("SettingsController", "ApplyButton", "ApplyButton")
```

```csharp
// ✅ Automatic lifecycle management
[Export] public NodePath ApplyButton { get; set; }

public override void OnStateEnter()
{
    // Automatically called when state is entered
    SetupUI();
}

public override void OnStateExit()
{
    // Automatically called when state is exited
    CleanupUI();
}
```

## Conclusion

The StateChart Component MVC pattern is the most elegant way to build Godot UIs with C#:

1. **Python**: Define structure (UI + StateChart)
2. **C#**: Implement logic (Components)
3. **TscnBuilder**: Wire automatically (NodePath binding)

This is the killer feature that makes TscnBuilder essential for serious C# Godot projects.
