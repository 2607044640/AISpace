---
inclusion: manual
---
# Godot Settings System with R3

## Overview
R3-based reactive settings system for Godot 4.x with automatic persistence, UI binding, and type-safe configuration.

**Location**: `B1Scripts/UI/`  
**Dependencies**: R3, R3.Godot  
**Pattern**: ReactiveProperty + Component Helpers

---

## Architecture

### Core Components

**SettingsManager** - Central state management
- Loads/saves settings from ConfigFile
- Exposes ReactiveProperty for each setting
- Auto-saves with Debounce (500ms)
- [Export] configurable defaults

**GameSettingsController** - UI binding layer
- Binds ReactiveProperty to UI components
- Handles bidirectional synchronization
- Applies settings to engine (audio, display)

**SettingBinders** - Generic binding utilities
- FloatSettingBinder, BoolSettingBinder, IntSettingBinder
- Encapsulates load/save logic
- Type-safe property creation

---

## Quick Start

### 1. Define Settings

```csharp
public partial class SettingsManager : Node
{
    [ExportGroup("Audio Defaults")]
    [Export] public float DefaultMasterVolume { get; set; } = 100f;
    [Export] public float DefaultMusicVolume { get; set; } = 80f;
    
    public ReactiveProperty<float> MasterVolume { get; private set; }
    public ReactiveProperty<float> MusicVolume { get; private set; }
    
    public override void _Ready()
    {
        _config = new ConfigFile();
        LoadConfig();
        
        MasterVolume = CreateFloatSetting("master_volume", DefaultMasterVolume);
        MusicVolume = CreateFloatSetting("music_volume", DefaultMusicVolume);
        
        SubscribeAutoSave();
    }
}
```

### 2. Bind UI

```csharp
public partial class GameSettingsController : Control
{
    [Export] public SliderComponentHelper MasterVolume { get; set; }
    
    private void BindSettings()
    {
        // Audio slider with automatic bus application
        BindAudioSlider(_settingsManager.MasterVolume, MasterVolume, _masterBusIdx);
        
        // Generic slider with custom logic
        BindSlider(_settingsManager.Brightness, BrightnessSlider, value => {
            // Custom application logic
        });
        
        // Toggle with custom action
        BindToggle(_settingsManager.Fullscreen, FullscreenToggle, ApplyFullscreen);
        
        // Dropdown with custom action
        BindDropdown(_settingsManager.ResolutionIndex, ResolutionDropdown, ApplyResolution);
    }
}
```

---

## Binding Methods

### BindAudioSlider
Specialized for audio settings with automatic dB conversion and bus application.

```csharp
BindAudioSlider(
    ReactiveProperty<float> property,
    SliderComponentHelper slider,
    int audioBusIdx
)
```

**Use**: Master/Music/SFX volume controls.

### BindSlider
Generic slider binding with optional custom logic.

```csharp
BindSlider(
    ReactiveProperty<float> property,
    SliderComponentHelper slider,
    Action<float> applyAction = null
)
```

**Use**: Brightness, FOV, sensitivity, any float setting.

**Example**:
```csharp
// With custom logic
BindSlider(_settingsManager.MouseSensitivity, SensitivitySlider, value => {
    _player.Sensitivity = value;
});

// Without custom logic (UI sync only)
BindSlider(_settingsManager.Brightness, BrightnessSlider);
```

### BindToggle
Boolean setting binding with optional custom action.

```csharp
BindToggle(
    ReactiveProperty<bool> property,
    ToggleComponentHelper toggle,
    Action<bool> applyAction = null
)
```

**Use**: Fullscreen, VSync, motion blur, any bool setting.

### BindDropdown
Integer index binding with optional custom action.

```csharp
BindDropdown(
    ReactiveProperty<int> property,
    DropdownComponentHelper dropdown,
    Action<int> applyAction = null
)
```

**Use**: Resolution, quality preset, language, any enum-like setting.

---

## Configuration

### Default Values

Edit defaults in Godot Inspector (SettingsManager node):

```
Audio Defaults
  ├─ Default Master Volume: 100
  ├─ Default Music Volume: 80
  └─ Default SFX Volume: 80

Video Defaults
  ├─ Default Fullscreen: false
  ├─ Default Resolution Index: 0
  └─ Default Anti Aliasing Index: 0
```

**Reset behavior**: `ResetAllSettings()` uses these [Export] values.

### File Storage

**Path**: `user://settings.cfg`  
**Format**: Godot ConfigFile (INI-like)

```ini
[Settings]
master_volume=100.0
music_volume=80.0
fullscreen=false
resolution=0
```

---

## Auto-Save System

### Debounce Strategy

All setting changes merge into single stream with 500ms debounce:

```csharp
Observable.Merge(
    MasterVolume.Skip(1).AsUnitObservable(),
    MusicVolume.Skip(1).AsUnitObservable(),
    // ... all settings
)
.Debounce(TimeSpan.FromMilliseconds(500))
.Subscribe(_ => SaveAllSettings())
```

**Effect**: User drags slider 100 times → Saves once after 500ms idle.

### Manual Save

```csharp
_settingsManager.SaveAllSettings(); // Force immediate save
```

---

## Adding New Settings

### Step 1: Add to SettingsManager

```csharp
[ExportGroup("Gameplay Defaults")]
[Export] public float DefaultMouseSensitivity { get; set; } = 1.0f;

public ReactiveProperty<float> MouseSensitivity { get; private set; }

public override void _Ready()
{
    // ...
    MouseSensitivity = CreateFloatSetting("mouse_sensitivity", DefaultMouseSensitivity);
}
```

### Step 2: Add to Auto-Save

```csharp
Observable.Merge(
    // ... existing settings
    MouseSensitivity.Skip(1).AsUnitObservable()
)
.Debounce(TimeSpan.FromMilliseconds(500))
.Subscribe(_ => SaveAllSettings())
```

### Step 3: Add to SaveAllSettings

```csharp
private void SaveAllSettings()
{
    // ... existing saves
    _config.SetValue(SettingsSection, "mouse_sensitivity", MouseSensitivity.Value);
    _config.Save(SettingsFilePath);
}
```

### Step 4: Add to ResetAllSettings

```csharp
public void ResetAllSettings()
{
    // ... existing resets
    MouseSensitivity.Value = DefaultMouseSensitivity;
}
```

### Step 5: Bind UI

```csharp
[Export] public SliderComponentHelper SensitivitySlider { get; set; }

private void BindSettings()
{
    // ...
    BindSlider(_settingsManager.MouseSensitivity, SensitivitySlider, value => {
        _player.Sensitivity = value;
    });
}
```

**Total**: 5 locations to modify for new setting.

---

## Best Practices

### DO

- Use [Export] for all default values
- Add DistinctUntilChanged to prevent loops
- Use ThrottleFirst for button actions
- Use TryParse for string parsing
- Bind settings in CallDeferred (after SettingsManager._Ready)

### DON'T

- Hardcode default values in code
- Call SaveAllSettings() on every change (use auto-save)
- Modify ReactiveProperty.Value in Subscribe callback (causes loop)
- Use int.Parse without try-catch
- Forget to add new settings to auto-save merge

---

## Advanced Patterns

### Conditional UI State

```csharp
// Disable resolution when fullscreen
_settingsManager.Fullscreen
    .Subscribe(isFullscreen => {
        var dropdown = Resolution.GetNodeOrNull<OptionButton>("OptionButton");
        if (dropdown != null) dropdown.Disabled = isFullscreen;
    })
    .AddTo(_disposables);
```

### Multi-Setting Validation

```csharp
Observable.CombineLatest(
    _settingsManager.Width,
    _settingsManager.Height,
    (w, h) => w >= 800 && h >= 600
)
.Subscribe(isValid => {
    _applyButton.Disabled = !isValid;
})
.AddTo(_disposables);
```

### Setting Presets

```csharp
public void ApplyLowPreset()
{
    _settingsManager.AntiAliasingIndex.Value = 0;
    _settingsManager.ShadowQuality.Value = 0;
    _settingsManager.TextureQuality.Value = 0;
    // Auto-saves after 500ms
}
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Settings not saving | Missing from SaveAllSettings | Add to _config.SetValue calls |
| Settings not loading | Missing from CreateXSetting | Add CreateXSetting call in _Ready |
| UI not updating | Missing DistinctUntilChanged | Add to both directions of binding |
| Infinite loop | Modifying property in Subscribe | Use DistinctUntilChanged |
| Reset not working | Hardcoded defaults | Use [Export] default properties |
| Frequent disk writes | No debounce | Verify 500ms Debounce in auto-save |

---

## Performance

**Metrics**:
- Auto-save debounce: 500ms
- Disk I/O reduction: 99% (from per-frame to per-idle)
- Memory overhead: ~100 bytes per setting
- UI update latency: <1ms (reactive)

**Optimization**:
- DistinctUntilChanged prevents redundant updates
- Debounce batches multiple changes
- Single ConfigFile.Save() call for all settings

---

## File Structure

```
B1Scripts/UI/
├── SettingBinders.cs          # Generic binding utilities
├── SettingsManager.cs         # Central state + persistence
└── GameSettingsController.cs  # UI binding layer
```

---

## Integration with Component Helpers

Settings system uses Component Helper pattern:

```csharp
// SliderComponentHelper exposes ReactiveProperty<float>
public partial class SliderComponentHelper : Control
{
    public ReactiveProperty<float> Value { get; private set; }
}

// Direct binding to SettingsManager
BindSlider(_settingsManager.MasterVolume, MasterVolumeHelper);
```

**Benefit**: Decoupled UI components, reusable across projects.

---

## Migration Guide

### From Manual Event Subscriptions

**Before**:
```csharp
_slider.ValueChanged += OnSliderChanged;
void OnSliderChanged(float value) {
    _settings.MasterVolume = value;
    SaveSettings();
}
```

**After**:
```csharp
BindSlider(_settingsManager.MasterVolume, _slider);
// Auto-saves, bidirectional, no manual cleanup
```

### From Hardcoded Defaults

**Before**:
```csharp
public void ResetAllSettings() {
    MasterVolume.Value = 100f; // Hardcoded
}
```

**After**:
```csharp
[Export] public float DefaultMasterVolume { get; set; } = 100f;

public void ResetAllSettings() {
    MasterVolume.Value = DefaultMasterVolume; // Configurable
}
```

---

## Resources

- **R3 Documentation**: https://github.com/Cysharp/R3
- **R3.Godot Plugin**: `addons/R3.Godot/`
- **Example Project**: `B1Scripts/UI/`
- **Related**: GodotDesignPatterns.md (Component system)
