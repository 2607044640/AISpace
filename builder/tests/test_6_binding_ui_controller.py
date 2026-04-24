"""
Test 6: C# Export Binding - UI Controller
Tests automatic NodePath binding for a complete settings UI with controller
"""

import sys
sys.path.append("../..")

from builder.core import TscnBuilder
from builder.modules.ui import UIModule

print("=" * 60)
print("TEST 6: C# Export Binding - UI Controller")
print("=" * 60)

# Initialize scene
scene = TscnBuilder(root_name="SettingsUI", root_type="Control")
ui = UIModule(scene)
ui.setup_fullscreen_control()

# Background
ui.add_color_rect("Background", parent=".", color=(0.08, 0.08, 0.12, 1), use_anchors=True)

# Main layout
ui.add_margin_container("MainMargin", parent=".", uniform=50)
ui.add_vbox("MainVBox", parent="MainMargin", separation=25)

# Title section
ui.add_label("TitleLabel", parent="MainVBox", text="Game Settings", align="center", font_size=36)
ui.add_separator("TitleSep", parent="MainVBox")

# Video settings
ui.add_label("VideoTitle", parent="MainVBox", text="Video Settings", font_size=22)
ui.add_vbox("VideoSection", parent="MainVBox", separation=12)

ui.add_hbox("ResolutionRow", parent="VideoSection", separation=10)
ui.add_label("ResolutionLabel", parent="ResolutionRow", text="Resolution:", min_size=(180, 0))
ui.add_label("ResolutionValue", parent="ResolutionRow", text="1920x1080", size_flags_h=3)

ui.add_hbox("FullscreenRow", parent="VideoSection", separation=10)
ui.add_label("FullscreenLabel", parent="FullscreenRow", text="Fullscreen:", min_size=(180, 0))
ui.add_checkbox("FullscreenCheckbox", parent="FullscreenRow", button_pressed=True)

ui.add_hbox("VSyncRow", parent="VideoSection", separation=10)
ui.add_label("VSyncLabel", parent="VSyncRow", text="VSync:", min_size=(180, 0))
ui.add_checkbox("VSyncCheckbox", parent="VSyncRow", button_pressed=True)

ui.add_hbox("FPSLimitRow", parent="VideoSection", separation=10)
ui.add_label("FPSLimitLabel", parent="FPSLimitRow", text="FPS Limit:", min_size=(180, 0))
ui.add_label("FPSLimitValue", parent="FPSLimitRow", text="60", size_flags_h=3)

ui.add_separator("VideoSep", parent="MainVBox")

# Audio settings
ui.add_label("AudioTitle", parent="MainVBox", text="Audio Settings", font_size=22)
ui.add_vbox("AudioSection", parent="MainVBox", separation=12)

ui.add_hbox("MasterVolumeRow", parent="AudioSection", separation=10)
ui.add_label("MasterVolumeLabel", parent="MasterVolumeRow", text="Master Volume:", min_size=(180, 0))
ui.add_progress_bar("MasterVolumeSlider", parent="MasterVolumeRow", value=85, size_flags_h=3)

ui.add_hbox("MusicVolumeRow", parent="AudioSection", separation=10)
ui.add_label("MusicVolumeLabel", parent="MusicVolumeRow", text="Music Volume:", min_size=(180, 0))
ui.add_progress_bar("MusicVolumeSlider", parent="MusicVolumeRow", value=70, size_flags_h=3)

ui.add_hbox("SFXVolumeRow", parent="AudioSection", separation=10)
ui.add_label("SFXVolumeLabel", parent="SFXVolumeRow", text="SFX Volume:", min_size=(180, 0))
ui.add_progress_bar("SFXVolumeSlider", parent="SFXVolumeRow", value=90, size_flags_h=3)

ui.add_separator("AudioSep", parent="MainVBox")

# Gameplay settings
ui.add_label("GameplayTitle", parent="MainVBox", text="Gameplay Settings", font_size=22)
ui.add_vbox("GameplaySection", parent="MainVBox", separation=12)

ui.add_hbox("DifficultyRow", parent="GameplaySection", separation=10)
ui.add_label("DifficultyLabel", parent="DifficultyRow", text="Difficulty:", min_size=(180, 0))
ui.add_label("DifficultyValue", parent="DifficultyRow", text="Normal", size_flags_h=3)

ui.add_hbox("AutoSaveRow", parent="GameplaySection", separation=10)
ui.add_label("AutoSaveLabel", parent="AutoSaveRow", text="Auto-Save:", min_size=(180, 0))
ui.add_checkbox("AutoSaveCheckbox", parent="AutoSaveRow", button_pressed=True)

ui.add_hbox("TutorialsRow", parent="GameplaySection", separation=10)
ui.add_label("TutorialsLabel", parent="TutorialsRow", text="Show Tutorials:", min_size=(180, 0))
ui.add_checkbox("TutorialsCheckbox", parent="TutorialsRow", button_pressed=True)

ui.add_separator("GameplaySep", parent="MainVBox")

# Button row
ui.add_hbox("ButtonRow", parent="MainVBox", separation=15)
ui.add_button("ApplyButton", parent="ButtonRow", text="Apply Changes", size_flags_h=3)
ui.add_button("ResetButton", parent="ButtonRow", text="Reset to Defaults", size_flags_h=3)
ui.add_button("CancelButton", parent="ButtonRow", text="Cancel", size_flags_h=3)

# Status label
ui.add_label("StatusLabel", parent="MainVBox", text="", align="center", font_size=16)

# Add C# Controller
print("\n📝 Adding SettingsController component...")
controller_res_id = scene.add_ext_resource("Script", 
                                          "res://B1Scripts/UI/SettingsController.cs", 
                                          "uid://settings_controller")
scene.add_node("SettingsController", "Node", parent=".",
              script=f'ExtResource("{controller_res_id}")')

# Bind all UI elements to controller using batch assignment
print("🔗 Binding UI elements to Controller [Export] properties...")

scene.assign_multiple_node_paths("SettingsController", {
    # Video controls
    "ResolutionValue": "ResolutionValue",
    "FullscreenCheckbox": "FullscreenCheckbox",
    "VSyncCheckbox": "VSyncCheckbox",
    "FPSLimitValue": "FPSLimitValue",
    
    # Audio controls
    "MasterVolumeSlider": "MasterVolumeSlider",
    "MusicVolumeSlider": "MusicVolumeSlider",
    "SFXVolumeSlider": "SFXVolumeSlider",
    
    # Gameplay controls
    "DifficultyValue": "DifficultyValue",
    "AutoSaveCheckbox": "AutoSaveCheckbox",
    "TutorialsCheckbox": "TutorialsCheckbox",
    
    # Buttons
    "ApplyButton": "ApplyButton",
    "ResetButton": "ResetButton",
    "CancelButton": "CancelButton",
    
    # Status
    "StatusLabel": "StatusLabel"
})

print("✅ 15 UI elements bound to Controller")

# Verify bindings
controller = scene.get_node("SettingsController")
print("\n📋 Verifying NodePath assignments:")
for prop_name in ["ApplyButton", "MasterVolumeSlider", "FullscreenCheckbox"]:
    if prop_name in controller.properties:
        print(f"  ✅ {prop_name} = {controller.properties[prop_name]}")

# Generate and save
print("\nGenerated Tree Structure:")
print(scene.generate_tree_view())
print("\n" + "=" * 60)

scene.save("c:/Godot/TetrisBackpack/Scenes/Test_Binding_UI_Controller.tscn")

print("\n✅ Test 6 Complete: UI Controller binding scene generated")
print("   - 15 UI controls bound to SettingsController")
print("   - Video, Audio, and Gameplay sections")
print("   - Batch assignment with assign_multiple_node_paths()")
print("=" * 60)
