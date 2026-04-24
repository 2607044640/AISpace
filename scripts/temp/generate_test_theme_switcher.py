import sys
sys.path.append('C:/Godot/AISpace/.kiro/scripts/ui_builder/generators')

from godot_ui_builder import UIBuilder, UINode

# Create test scene
ui = UIBuilder("TestThemeSwitcher")

# Root Control (fullscreen)
root = ui.create_control("Control", fullscreen=True)

# Background
root.add_color_rect("BG", color=(0.2, 0.2, 0.2, 1), use_anchors=True)

# Margin
margin = root.add_margin_container("Margin", uniform=40, use_anchors=True, script=None)
margin.set_property("anchors_preset", 15)
margin.set_property("anchor_right", 1.0)
margin.set_property("anchor_bottom", 1.0)
margin.set_property("grow_horizontal", 2)
margin.set_property("grow_vertical", 2)

# VBox
vbox = margin.add_vbox("Content", separation=20)

# Title
vbox.add_label("Title", text="Theme Switcher Test", align="center", font_size=32)

# Add ThemeSwitcherComponent instance
theme_switcher = UINode("ThemeSwitcher", "HBoxContainer", auto_suffix=False)
theme_switcher.properties["layout_mode"] = 2
theme_switcher.properties["_is_instance"] = True
theme_switcher.properties["_scene_path"] = "res://A1UIScenes/UIComponents/ThemeSwitcherComponent.tscn"
theme_switcher.properties["_scene_uid"] = "uid://placeholder_theme_component"
vbox._add_child(theme_switcher)

# Add some sample UI to see theme changes
sample_panel = vbox.add_panel_container("SamplePanel")
sample_inner = sample_panel.add_margin_container("Inner", uniform=20, script=None)
sample_vbox = sample_inner.add_vbox("SampleContent", separation=10)

sample_vbox.add_label("SampleLabel", text="Sample UI Elements", font_size=24)
sample_vbox.add_button("SampleButton1", text="Button 1")
sample_vbox.add_button("SampleButton2", text="Button 2")
sample_vbox.add_checkbox("SampleCheck", text="Checkbox")

# Add external resource for ThemeSwitcherComponent scene
ui.ext_resources.append({
    "type": "PackedScene",
    "path": "res://A1UIScenes/UIComponents/ThemeSwitcherComponent.tscn",
    "id": "1_theme_component",
    "uid": "uid://placeholder_theme_component"
})

# Save
output_path = "C:/Godot/3d-practice/A1UIScenes/TestThemeSwitcher.tscn"
ui.save(output_path)
print(f"Generated: {output_path}")
