"""
Example: C# Export NodePath Binding
Demonstrates automatic binding of UI nodes to C# Controller [Export] properties

This is the killer feature for C# architecture:
- No manual NodePath calculation
- No Godot signal connections
- Pure C# events and R3 reactive extensions
- Clean MVC separation
"""

import sys
sys.path.append("../..")

from builder.core import TscnBuilder
from builder.modules.ui import UIModule

print("=" * 60)
print("C# Export NodePath Binding Example")
print("=" * 60)

# ============================================================
# PART 1: Create UI Structure
# ============================================================

scene = TscnBuilder(root_name="GameSettingsUI", root_type="Control")
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

# Audio Section
ui.add_label("AudioTitle", parent="MainVBox", text="Audio Settings", font_size=20)
ui.add_vbox("AudioSection", parent="MainVBox", separation=10)

ui.add_hbox("MasterVolumeRow", parent="AudioSection", separation=10)
ui.add_label("MasterVolumeLabel", parent="MasterVolumeRow", text="Master Volume:", min_size=(150, 0))
ui.add_progress_bar("MasterVolumeSlider", parent="MasterVolumeRow", value=80, size_flags_h=3)

ui.add_hbox("MusicVolumeRow", parent="AudioSection", separation=10)
ui.add_label("MusicVolumeLabel", parent="MusicVolumeRow", text="Music Volume:", min_size=(150, 0))
ui.add_progress_bar("MusicVolumeSlider", parent="MusicVolumeRow", value=70, size_flags_h=3)

ui.add_hbox("SFXVolumeRow", parent="AudioSection", separation=10)
ui.add_label("SFXVolumeLabel", parent="SFXVolumeRow", text="SFX Volume:", min_size=(150, 0))
ui.add_progress_bar("SFXVolumeSlider", parent="SFXVolumeRow", value=90, size_flags_h=3)

ui.add_separator("AudioSep", parent="MainVBox")

# Graphics Section
ui.add_label("GraphicsTitle", parent="MainVBox", text="Graphics Settings", font_size=20)
ui.add_vbox("GraphicsSection", parent="MainVBox", separation=10)

ui.add_hbox("FullscreenRow", parent="GraphicsSection", separation=10)
ui.add_label("FullscreenLabel", parent="FullscreenRow", text="Fullscreen:", min_size=(150, 0))
ui.add_checkbox("FullscreenCheckbox", parent="FullscreenRow", button_pressed=True)

ui.add_hbox("VSyncRow", parent="GraphicsSection", separation=10)
ui.add_label("VSyncLabel", parent="VSyncRow", text="VSync:", min_size=(150, 0))
ui.add_checkbox("VSyncCheckbox", parent="VSyncRow", button_pressed=True)

ui.add_hbox("QualityRow", parent="GraphicsSection", separation=10)
ui.add_label("QualityLabel", parent="QualityRow", text="Quality:", min_size=(150, 0))
ui.add_label("QualityValue", parent="QualityRow", text="High", size_flags_h=3)

ui.add_separator("GraphicsSep", parent="MainVBox")

# Gameplay Section
ui.add_label("GameplayTitle", parent="MainVBox", text="Gameplay Settings", font_size=20)
ui.add_vbox("GameplaySection", parent="MainVBox", separation=10)

ui.add_hbox("DifficultyRow", parent="GameplaySection", separation=10)
ui.add_label("DifficultyLabel", parent="DifficultyRow", text="Difficulty:", min_size=(150, 0))
ui.add_label("DifficultyValue", parent="DifficultyRow", text="Normal", size_flags_h=3)

ui.add_hbox("AutoSaveRow", parent="GameplaySection", separation=10)
ui.add_label("AutoSaveLabel", parent="AutoSaveRow", text="Auto-Save:", min_size=(150, 0))
ui.add_checkbox("AutoSaveCheckbox", parent="AutoSaveRow", button_pressed=True)

ui.add_separator("GameplaySep", parent="MainVBox")

# Button Row
ui.add_hbox("ButtonRow", parent="MainVBox", separation=15)
ui.add_button("ApplyButton", parent="ButtonRow", text="Apply", size_flags_h=3)
ui.add_button("ResetButton", parent="ButtonRow", text="Reset to Defaults", size_flags_h=3)
ui.add_button("CancelButton", parent="ButtonRow", text="Cancel", size_flags_h=3)

# Status Label
ui.add_label("StatusLabel", parent="MainVBox", text="", align="center", font_size=14)

# ============================================================
# PART 2: Add C# Controller Component
# ============================================================

# Add controller as a child of the root
# In real usage, you'd provide the actual script UID via mcp_godot_get_uid
controller_script_path = "res://B1Scripts/UI/GameSettingsController.cs"
controller_script_uid = "uid://placeholder_controller"

# Register the script as external resource
controller_res_id = scene.add_ext_resource("Script", controller_script_path, controller_script_uid)

# Add controller node
scene.add_node("SettingsController", "Node", parent=".",
              script=f'ExtResource("{controller_res_id}")')

# ============================================================
# PART 3: Automatically Bind UI to Controller [Export] Properties
# ============================================================

print("\n🔗 Binding UI nodes to Controller [Export] properties...")

# Method 1: Individual bindings (explicit and clear)
scene.assign_node_path("SettingsController", "MasterVolumeSlider", "MasterVolumeSlider")
scene.assign_node_path("SettingsController", "MusicVolumeSlider", "MusicVolumeSlider")
scene.assign_node_path("SettingsController", "SFXVolumeSlider", "SFXVolumeSlider")

# Method 2: Batch bindings (cleaner for many controls)
scene.assign_multiple_node_paths("SettingsController", {
    "FullscreenCheckbox": "FullscreenCheckbox",
    "VSyncCheckbox": "VSyncCheckbox",
    "AutoSaveCheckbox": "AutoSaveCheckbox",
    "ApplyButton": "ApplyButton",
    "ResetButton": "ResetButton",
    "CancelButton": "CancelButton",
    "StatusLabel": "StatusLabel",
    "QualityValue": "QualityValue",
    "DifficultyValue": "DifficultyValue"
})

print("✅ All UI nodes bound to Controller properties")

# ============================================================
# PART 4: Generate and Save
# ============================================================

print("\nGenerated Tree Structure:")
print(scene.generate_tree_view())
print("\n" + "=" * 60)

scene.save("c:/Godot/TetrisBackpack/Scenes/Example_CSharp_Export_Binding.tscn")

print("\n✅ Scene generated successfully!")
print("\nThe generated TSCN contains automatic NodePath assignments like:")
print('  MasterVolumeSlider = NodePath("../MainMargin/MainVBox/AudioSection/MasterVolumeRow/MasterVolumeSlider")')
print('  ApplyButton = NodePath("../MainMargin/MainVBox/ButtonRow/ApplyButton")')
print("\nIn your C# Controller, you can now use:")
print("  [Export] public NodePath MasterVolumeSlider { get; set; }")
print("  [Export] public NodePath ApplyButton { get; set; }")
print("\nAnd access them via:")
print("  var slider = GetNode<ProgressBar>(MasterVolumeSlider);")
print("  var button = GetNode<Button>(ApplyButton);")
print("\nOr with R3 reactive extensions:")
print("  GetNode<Button>(ApplyButton).OnPressedAsObservable()")
print("    .Subscribe(_ => ApplySettings())")
print("    .AddTo(_disposables);")
print("=" * 60)
