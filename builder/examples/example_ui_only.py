"""
Example: UI Only - Generate a scene with only UI components
"""

import sys
sys.path.append("../..")

from builder.core import TscnBuilder
from builder.modules.ui import UIModule

# Initialize Core Scene
scene = TscnBuilder(root_name="SettingsMenu", root_type="Control")

# Attach UI Module
ui = UIModule(scene)
ui.setup_fullscreen_control()

# Build UI Structure
margin = ui.add_margin_container("MainMargin", uniform=20)
vbox = ui.add_vbox("MainVBox", parent="MainMargin", separation=10)

ui.add_label("TitleLabel", parent="MainVBox", text="Settings", align="center", font_size=32)
ui.add_separator("Separator1", parent="MainVBox")

# Audio Section
audio_hbox = ui.add_hbox("AudioSection", parent="MainVBox", separation=10)
ui.add_label("AudioLabel", parent="AudioSection", text="Master Volume:")
ui.add_progress_bar("VolumeBar", parent="AudioSection", value=75, size_flags_h=3)

# Graphics Section
graphics_hbox = ui.add_hbox("GraphicsSection", parent="MainVBox", separation=10)
ui.add_label("GraphicsLabel", parent="GraphicsSection", text="Fullscreen:")
ui.add_checkbox("FullscreenCheck", parent="GraphicsSection", button_pressed=True)

# Buttons
button_hbox = ui.add_hbox("ButtonSection", parent="MainVBox", separation=10)
ui.add_button("ApplyButton", parent="ButtonSection", text="Apply", size_flags_h=3)
ui.add_button("CancelButton", parent="ButtonSection", text="Cancel", size_flags_h=3)

# Export
print(scene.generate_tree_view())
scene.save("c:/Godot/3d-practice/Scenes/SettingsMenu.tscn")
