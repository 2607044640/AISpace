---
trigger: glob
globs: TetrisBackpack/B1Scripts/UI/**/*.cs,**/SettingsManager*.cs,**/GameSettings*.cs,**/SettingBinders*.cs
---

<layer_1_quick_start>
  <quick_reference>
    - **System Location**: `B1Scripts/UI/`
    - **Core Scripts**: `SettingsManager.cs`, `GameSettingsController.cs`, `SettingBinders.cs`
    - **Save Path**: `user://settings.cfg`
    - **Debounce Timer**: 500ms (Global Setting State Save)
  </quick_reference>

  <decision_tree>
    - If binding Master, Music, or SFX volume: **ALWAYS** use `BindAudioSlider` (Why: Automatically handles dB conversion and audio bus application).
    - If binding FOV, Brightness, or continuous values: **ALWAYS** use `BindSlider` (Why: Maps float values linearly to UI components).
    - If binding VSync, Fullscreen, or booleans: **ALWAYS** use `BindToggle` (Why: Maps boolean state directly to toggle switches).
    - If binding Resolutions, Quality, or Enums: **ALWAYS** use `BindDropdown` (Why: Maps integer indices directly to UI options).
  </decision_tree>

  <minimal_workflow>
    1. Define the setting in `SettingsManager` using an `[Export]` default value and a `ReactiveProperty<T>`.
    2. Add the `ReactiveProperty.Skip(1).AsUnitObservable()` to the `Observable.Merge` block for Auto-Save tracking.
    3. Add the `_config.SetValue` and `_config.Save` logic to the `SaveAllSettings()` method.
    4. Apply the `[Export]` default value assignment inside the `ResetAllSettings()` method.
    5. Bind the UI component using the appropriate `Bind*` method in `GameSettingsController`.
  </minimal_workflow>

  <top_anti_patterns>
    - **PROHIBITED**: Calling `SaveAllSettings()` on every value change. (Why: Generates excessive disk I/O; system relies on 500ms debounce).
    - **PROHIBITED**: Modifying `ReactiveProperty.Value` inside its own `Subscribe` callback. (Why: Triggers infinite recursive update loops).
    - **PROHIBITED**: Hardcoding default fallback values in reset functions. (Why: Breaks inspector configurability; `[Export]` properties must dictate defaults).
    - **PROHIBITED**: Parsing integer values without `try-catch` or `TryParse`. (Why: Unexpected config file corruption will crash the boot sequence).
  </top_anti_patterns>
</layer_1_quick_start>

<layer_2_detailed_guide>
  <api_reference>
    - `BindAudioSlider(ReactiveProperty<float> property, SliderComponentHelper slider, int audioBusIdx)`
    - `BindSlider(ReactiveProperty<float> property, SliderComponentHelper slider, Action<float> applyAction = null)`
    - `BindToggle(ReactiveProperty<bool> property, ToggleComponentHelper toggle, Action<bool> applyAction = null)`
    - `BindDropdown(ReactiveProperty<int> property, DropdownComponentHelper dropdown, Action<int> applyAction = null)`
    - `SliderComponentHelper.Value` -> `ReactiveProperty<float>`
    - `SettingsManager.ResetAllSettings()`
    - `SettingsManager.SaveAllSettings()`
  </api_reference>

  <code_examples>
    <example name="Define Settings in SettingsManager">
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
    </example>

    <example name="Bind UI in GameSettingsController">
      ```csharp
      public partial class GameSettingsController : Control
      {
          [Export] public SliderComponentHelper MasterVolume { get; set; }
          [Export] public ToggleComponentHelper FullscreenToggle { get; set; }
          [Export] public DropdownComponentHelper ResolutionDropdown { get; set; }

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
    </example>

    <example name="Auto-Save Configuration">
      ```csharp
      private void SubscribeAutoSave()
      {
          Observable.Merge(
              MasterVolume.Skip(1).AsUnitObservable(),
              MusicVolume.Skip(1).AsUnitObservable(),
              Fullscreen.Skip(1).AsUnitObservable(),
              ResolutionIndex.Skip(1).AsUnitObservable()
              // ... all settings
          )
          .Debounce(TimeSpan.FromMilliseconds(500))
          .Subscribe(_ => SaveAllSettings())
          .AddTo(_disposables);
      }
      ```
    </example>

    <example name="Config File Format">
      ```ini
      [Settings]
      master_volume=100.0
      music_volume=80.0
      sfx_volume=80.0
      fullscreen=false
      resolution_index=0
      anti_aliasing_index=0
      ```
    </example>
  </code_examples>

  <adding_new_settings>
    <step number="1" title="Add to SettingsManager">
      ```csharp
      [ExportGroup("Gameplay Defaults")]
      [Export] public float DefaultMouseSensitivity { get; set; } = 1.0f;
      public ReactiveProperty<float> MouseSensitivity { get; private set; }
      
      public override void _Ready()
      {
          // ... existing code
          MouseSensitivity = CreateFloatSetting("mouse_sensitivity", DefaultMouseSensitivity);
      }
      ```
    </step>

    <step number="2" title="Add to Auto-Save">
      ```csharp
      Observable.Merge(
          // ... existing settings
          MouseSensitivity.Skip(1).AsUnitObservable()
      )
      .Debounce(TimeSpan.FromMilliseconds(500))
      .Subscribe(_ => SaveAllSettings())
      ```
    </step>

    <step number="3" title="Add to SaveAllSettings">
      ```csharp
      private void SaveAllSettings()
      {
          // ... existing saves
          _config.SetValue(SettingsSection, "mouse_sensitivity", MouseSensitivity.Value);
          _config.Save(SettingsFilePath);
      }
      ```
    </step>

    <step number="4" title="Add to ResetAllSettings">
      ```csharp
      public void ResetAllSettings()
      {
          // ... existing resets
          MouseSensitivity.Value = DefaultMouseSensitivity;
      }
      ```
    </step>

    <step number="5" title="Bind UI">
      ```csharp
      [Export] public SliderComponentHelper SensitivitySlider { get; set; }
      
      private void BindSettings()
      {
          // ... existing bindings
          BindSlider(_settingsManager.MouseSensitivity, SensitivitySlider, value => {
              _player.Sensitivity = value;
          });
      }
      ```
    </step>
  </adding_new_settings>

  <technical_specifications>
    - **Save Format**: Godot ConfigFile (INI-like format).
    - **Default Settings Hierarchy**:
      - Audio Defaults: `DefaultMasterVolume` (100f), `DefaultMusicVolume` (80f), `DefaultSFXVolume` (80f).
      - Video Defaults: `DefaultFullscreen` (false), `DefaultResolutionIndex` (0), `DefaultAntiAliasingIndex` (0).
    - **Auto-Save Aggregation**: Uses `Observable.Merge()` combining all setting streams into a single stream.
    - **Debounce Specification**: `TimeSpan.FromMilliseconds(500)` applied prior to invoking `SaveAllSettings()`.
    - **Initialization Order**: `SettingsManager._Ready()` → Load ConfigFile → Create ReactiveProperties → `GameSettingsController` bindings (CallDeferred).
  </technical_specifications>

  <core_rules>
    <rule>
      <description>**ALWAYS** use `[Export]` properties to define fallback defaults in `SettingsManager`.</description>
      <rationale>Ensures values like `100f` for volume or `0` for resolution indices are adjustable via the Godot Inspector without code compilation.</rationale>
    </rule>
    <rule>
      <description>**ALWAYS** use `DistinctUntilChanged` when establishing bidirectional bindings.</description>
      <rationale>Prevents redundant UI updates and avoids recursive infinite loops between the engine state and UI state.</rationale>
    </rule>
    <rule>
      <description>**MUST** execute UI setting bindings in `CallDeferred` or after `SettingsManager._Ready` is fully resolved.</description>
      <rationale>Guarantees that `ReactiveProperty` instances are fully initialized from the config file before the UI attempts to read or mutate them.</rationale>
    </rule>
    <rule>
      <description>**MUST** use `ThrottleFirst` for all interactive button actions that mutate settings.</description>
      <rationale>Prevents multi-click spamming from queueing multiple heavy UI layout recalculations or configuration saves.</rationale>
    </rule>
  </core_rules>
</layer_2_detailed_guide>

<layer_3_advanced>
  <troubleshooting>
    <error symptom="Settings not saving">
      <cause>The new setting property was not injected into the `_config.SetValue` calls inside `SaveAllSettings()`.</cause>
      <fix>Append the `_config.SetValue` invocation for the specific variable inside the `SaveAllSettings()` method block.</fix>
    </error>
    <error symptom="Settings not loading">
      <cause>The configuration creation step is missing from `_Ready`.</cause>
      <fix>Add the respective `CreateXSetting` function call inside `SettingsManager._Ready()` utilizing the correct configuration string key.</fix>
    </error>
    <error symptom="UI not updating">
      <cause>Missing `DistinctUntilChanged` modifier on the observable chain.</cause>
      <fix>Apply `.DistinctUntilChanged()` to both directions of the UI/State binding layer.</fix>
    </error>
    <error symptom="Infinite loop crash or freeze">
      <cause>The code is modifying the `ReactiveProperty.Value` inside its own `.Subscribe()` closure.</cause>
      <fix>Remove the internal assignment or implement strict `.DistinctUntilChanged()` gatekeeping to break the execution cycle.</fix>
    </error>
    <error symptom="Reset to defaults not working correctly">
      <cause>The `ResetAllSettings()` method is resetting variables to hardcoded magic numbers instead of exposed properties.</cause>
      <fix>Change hardcoded values in the reset function to point to their corresponding `[Export]` variables (e.g., `DefaultMasterVolume`).</fix>
    </error>
    <error symptom="Frequent disk writes during slider drag">
      <cause>The save event is attached per-frame or per-value-change without a debounce buffer.</cause>
      <fix>Wrap the UI save execution in a `.Debounce(TimeSpan.FromMilliseconds(500))` modifier.</fix>
    </error>
  </troubleshooting>

  <advanced_patterns>
    <pattern name="Conditional UI State">
      ```csharp
      // Disable resolution dropdown when fullscreen is enabled
      _settingsManager.Fullscreen
          .Subscribe(isFullscreen => {
              var dropdown = Resolution.GetNodeOrNull<OptionButton>("OptionButton");
              if (dropdown != null) dropdown.Disabled = isFullscreen;
          })
          .AddTo(_disposables);
      ```
    </pattern>

    <pattern name="Multi-Setting Validation">
      ```csharp
      // Enable Apply button only when resolution is valid
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
    </pattern>

    <pattern name="Quality Presets">
      ```csharp
      public void ApplyLowPreset()
      {
          _settingsManager.AntiAliasingIndex.Value = 0;
          _settingsManager.ShadowQuality.Value = 0;
          _settingsManager.TextureQuality.Value = 0;
          // Auto-saves after 500ms debounce (single disk write)
      }
      ```
    </pattern>
  </advanced_patterns>

  <file_structure>
    ```
    B1Scripts/UI/
    ├── SettingBinders.cs          # Generic binding utilities
    ├── SettingsManager.cs         # Central state + persistence
    └── GameSettingsController.cs  # UI binding layer
    ```
  </file_structure>

  <performance_metrics>
    - Auto-save debounce: 500ms
    - Disk I/O reduction: 99% (from per-frame to per-idle)
    - Memory overhead: ~100 bytes per setting
    - UI update latency: <1ms (reactive)
  </performance_metrics>

  <migration_guide>
    <from pattern="Manual Event Subscriptions">
      <before>
        ```csharp
        _slider.ValueChanged += OnSliderChanged;
        
        void OnSliderChanged(float value) {
            _settings.MasterVolume = value;
            SaveSettings();
        }
        ```
      </before>
      <after>
        ```csharp
        BindSlider(_settingsManager.MasterVolume, _slider);
        // Auto-saves, bidirectional, no manual cleanup
        ```
      </after>
    </from>

    <from pattern="Hardcoded Defaults">
      <before>
        ```csharp
        public void ResetAllSettings() {
            MasterVolume.Value = 100f; // Hardcoded
        }
        ```
      </before>
      <after>
        ```csharp
        [Export] public float DefaultMasterVolume { get; set; } = 100f;
        
        public void ResetAllSettings() {
            MasterVolume.Value = DefaultMasterVolume; // Configurable
        }
        ```
      </after>
    </from>
  </migration_guide>

  <best_practices>
    - **Performance Constraint**: The system overhead **MUST** maintain ~100 bytes per setting with less than 1ms latency for reactive UI updates.
    - **File Directory Integrity**: All system configuration files **MUST** be stored in `AISpace/`.
    - **Migration Standard**: **NEVER** use manual event subscriptions (e.g., `_slider.ValueChanged += OnSliderChanged`); **ALWAYS** migrate legacy manual C# events to generic `SettingBinders` to eliminate manual unsubscription lifecycle management.
    - **Payload Discarding**: Streamline logic by chaining `.AsUnitObservable()` when the pipeline only needs to know *when* an event happened, not *what* the payload contained.
    - **State Abstraction**: Use `ReactiveProperty<T>` for discrete, non-continuous state changes so UI elements automatically sync via single-subscription.
    - **Editor Parity**: Take full advantage of `R3.Godot` extensions like `OnToggledAsObservable()` because they immediately emit current state upon subscription, ensuring UI aligns instantly with backend state.
  </best_practices>

  <integration_notes>
    - Settings system uses Component Helper pattern for UI binding
    - Component Helpers expose `ReactiveProperty<T>` for direct binding to SettingsManager
    - Example: `SliderComponentHelper.Value` → `ReactiveProperty<float>`
    - Benefit: Decoupled UI components, reusable across projects
    - Related: See DesignPatterns.md for Component architecture details
  </integration_notes>
</layer_3_advanced>