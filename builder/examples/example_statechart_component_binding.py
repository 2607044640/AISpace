"""
Example: StateChart Component with C# Export Binding
Demonstrates the elegant MVC pattern: UI + StateChart + C# Components + Automatic Binding

This shows the complete workflow:
1. Create visual UI (View)
2. Create StateChart with states (State Management)
3. Add C# components to states (Controller)
4. Bind UI to component [Export] properties automatically (Wiring)
"""

import sys
sys.path.append("../..")

from builder.core import TscnBuilder
from builder.modules.ui import UIModule
from builder.modules.statechart import StateChartModule

print("=" * 70)
print("StateChart Component with C# Export Binding Example")
print("=" * 70)

# ============================================================
# STEP 1: Create Visual UI (View Layer)
# ============================================================

print("\n📝 STEP 1: Creating visual UI...")

scene = TscnBuilder(root_name="SettingsMenu", root_type="Control")
ui = UIModule(scene)
ui.setup_fullscreen_control()

# Background
ui.add_color_rect("Background", parent=".", color=(0.1, 0.1, 0.15, 1), use_anchors=True)

# Main layout
ui.add_margin_container("MainMargin", parent=".", uniform=40)
ui.add_vbox("MainVBox", parent="MainMargin", separation=20)

# Title
ui.add_label("TitleLabel", parent="MainVBox", text="Game Settings", 
             align="center", font_size=32)
ui.add_separator("TitleSep", parent="MainVBox")

# Audio section
ui.add_label("AudioTitle", parent="MainVBox", text="Audio Settings", font_size=20)
ui.add_vbox("AudioSection", parent="MainVBox", separation=10)

ui.add_hbox("MasterVolumeRow", parent="AudioSection", separation=10)
ui.add_label("MasterVolumeLabel", parent="MasterVolumeRow", text="Master Volume:", min_size=(150, 0))
ui.add_progress_bar("MasterVolumeSlider", parent="MasterVolumeRow", value=80, size_flags_h=3)

ui.add_hbox("MusicVolumeRow", parent="AudioSection", separation=10)
ui.add_label("MusicVolumeLabel", parent="MusicVolumeRow", text="Music Volume:", min_size=(150, 0))
ui.add_progress_bar("MusicVolumeSlider", parent="MusicVolumeRow", value=70, size_flags_h=3)

ui.add_separator("AudioSep", parent="MainVBox")

# Graphics section
ui.add_label("GraphicsTitle", parent="MainVBox", text="Graphics Settings", font_size=20)
ui.add_vbox("GraphicsSection", parent="MainVBox", separation=10)

ui.add_hbox("FullscreenRow", parent="GraphicsSection", separation=10)
ui.add_label("FullscreenLabel", parent="FullscreenRow", text="Fullscreen:", min_size=(150, 0))
ui.add_checkbox("FullscreenCheckbox", parent="FullscreenRow", button_pressed=True)

ui.add_hbox("VSyncRow", parent="GraphicsSection", separation=10)
ui.add_label("VSyncLabel", parent="VSyncRow", text="VSync:", min_size=(150, 0))
ui.add_checkbox("VSyncCheckbox", parent="VSyncRow", button_pressed=True)

ui.add_separator("GraphicsSep", parent="MainVBox")

# Button row
ui.add_hbox("ButtonRow", parent="MainVBox", separation=15)
ui.add_button("ApplyButton", parent="ButtonRow", text="Apply Changes", size_flags_h=3)
ui.add_button("ResetButton", parent="ButtonRow", text="Reset to Defaults", size_flags_h=3)
ui.add_button("CancelButton", parent="ButtonRow", text="Cancel", size_flags_h=3)

# Status label
ui.add_label("StatusLabel", parent="MainVBox", text="", align="center", font_size=14)

print("✅ UI created with 20+ controls")

# ============================================================
# STEP 2: Create StateChart (State Management Layer)
# ============================================================

print("\n📝 STEP 2: Creating StateChart for state management...")

sc = StateChartModule(scene, parent=".")
sc.add_statechart("StateChart")

# Root state
sc.add_compound_state("Root", parent="StateChart", initial_state="Idle")

# Menu states
sc.add_atomic_state("Idle", parent="Root")
sc.add_atomic_state("Editing", parent="Root")
sc.add_atomic_state("Applying", parent="Root")
sc.add_atomic_state("Resetting", parent="Root")

# Transitions
sc.add_transition("ToEditing", from_state="Idle", to_state="Editing", event="start_edit")
sc.add_transition("ToIdle", from_state="Editing", to_state="Idle", event="cancel")
sc.add_transition("ToApplying", from_state="Editing", to_state="Applying", event="apply")
sc.add_transition("ToResetting", from_state="Editing", to_state="Resetting", event="reset")
sc.add_transition("BackToIdle1", from_state="Applying", to_state="Idle", event="complete")
sc.add_transition("BackToIdle2", from_state="Resetting", to_state="Idle", event="complete")

sc.resolve_initial_states()

print("✅ StateChart created with 4 states and 6 transitions")

# ============================================================
# STEP 3: Add C# Component to State (Controller Layer)
# ============================================================

print("\n📝 STEP 3: Adding C# SettingsController component to Editing state...")

# Add SettingsController component to the Editing state
# This component will handle all the settings logic when in edit mode
sc.add_component(
    name="SettingsController",
    parent="Editing",
    script_path="res://B1Scripts/UI/SettingsController.cs",
    script_uid="uid://settings_controller_uid"
)

print("✅ SettingsController component added to Editing state")

# ============================================================
# STEP 4: Bind UI to Component [Export] Properties (Wiring Layer)
# ============================================================

print("\n📝 STEP 4: Automatically binding UI controls to SettingsController [Export] properties...")

# This is the magic! Automatically calculate NodePaths and assign them
# to the component's [Export] properties
scene.assign_multiple_node_paths("SettingsController", {
    # Audio controls
    "MasterVolumeSlider": "MasterVolumeSlider",
    "MusicVolumeSlider": "MusicVolumeSlider",
    
    # Graphics controls
    "FullscreenCheckbox": "FullscreenCheckbox",
    "VSyncCheckbox": "VSyncCheckbox",
    
    # Buttons
    "ApplyButton": "ApplyButton",
    "ResetButton": "ResetButton",
    "CancelButton": "CancelButton",
    
    # Status
    "StatusLabel": "StatusLabel"
})

print("✅ 8 UI controls automatically bound to SettingsController")

# ============================================================
# STEP 5: Verify and Save
# ============================================================

print("\n📋 Verifying NodePath assignments:")
controller = scene.get_node("SettingsController")
for prop in ["ApplyButton", "MasterVolumeSlider", "FullscreenCheckbox"]:
    if prop in controller.properties:
        print(f"  ✅ SettingsController.{prop} = {controller.properties[prop]}")

print("\n" + "=" * 70)
print("Generated Scene Structure:")
print("=" * 70)
print(scene.generate_tree_view())
print("=" * 70)

scene.save("c:/Godot/TetrisBackpack/Scenes/Example_StateChart_Component_Binding.tscn")

print("\n✅ Scene generated successfully!")
print("\n" + "=" * 70)
print("ELEGANT MVC PATTERN DEMONSTRATED:")
print("=" * 70)
print("""
1. Visual UI (View):
   - Created with UIModule
   - 20+ controls (sliders, checkboxes, buttons, labels)

2. StateChart (State Management):
   - 4 states: Idle, Editing, Applying, Resetting
   - 6 transitions between states
   - Clean state machine architecture

3. C# Component (Controller):
   - SettingsController attached to Editing state
   - Handles all settings logic
   - Pure C# with R3 reactive extensions

4. Automatic Binding (Wiring):
   - 8 UI controls bound to component [Export] properties
   - Zero manual NodePath calculation
   - Refactoring-safe

Generated TSCN contains:
  [node name="SettingsController" type="Node" parent="StateChart/Root/Editing"]
  script = ExtResource("...")
  MasterVolumeSlider = NodePath("../../../../../MainMargin/MainVBox/AudioSection/MasterVolumeRow/MasterVolumeSlider")
  ApplyButton = NodePath("../../../../../MainMargin/MainVBox/ButtonRow/ApplyButton")
  ...

In your C# SettingsController.cs:
  [Export] public NodePath MasterVolumeSlider { get; set; }
  [Export] public NodePath ApplyButton { get; set; }
  
  public override void OnStateEnter()
  {
      // State entered - setup UI bindings
      GetNode<ProgressBar>(MasterVolumeSlider).OnValueChangedAsObservable()
          .Debounce(TimeSpan.FromMilliseconds(100))
          .Subscribe(volume => UpdateMasterVolume(volume))
          .AddTo(_disposables);
      
      GetNode<Button>(ApplyButton).OnPressedAsObservable()
          .ThrottleFirst(TimeSpan.FromMilliseconds(500))
          .Subscribe(_ => ApplySettings())
          .AddTo(_disposables);
  }
  
  public override void OnStateExit()
  {
      // State exited - cleanup
      _disposables.Dispose();
  }
""")
print("=" * 70)
