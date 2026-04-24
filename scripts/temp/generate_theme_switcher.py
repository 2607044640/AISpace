import sys
sys.path.append('C:/Godot/AISpace/.kiro/scripts/ui_builder/generators')

from godot_ui_builder import UIBuilder, UINode

# Create ThemeSwitcherComponent
ui = UIBuilder("ThemeSwitcherComponent")

# Root HBoxContainer with ThemeSwitcherComponentHelper script
root = UINode("ThemeSwitcherComponent", "HBoxContainer", auto_suffix=False)
root.properties["custom_minimum_size"] = "Vector2(400, 40)"
root.properties["theme_override_constants/separation"] = 15
root.properties["script"] = 'ExtResource("1_helper_script")'
root.properties["_script_path"] = "res://addons/A1MyAddon/Helpers/ThemeSwitcherComponentHelper.cs"
ui.root = root

# Label
label = root.add_label("Label", text="Theme:", min_size=(100, 0), size_flags_h=0)

# OptionButton (Dropdown)
dropdown = UINode("ThemeDropdown", "OptionButton", auto_suffix=False)
dropdown.properties["layout_mode"] = 2
dropdown.properties["size_flags_horizontal"] = 3  # Fill + Expand
root._add_child(dropdown)

# Reset Button
reset = root.add_button("ResetButton", text="Reset", size_flags_h=4)

# Manually add external resource for the helper script
ui.ext_resources.append({
    "type": "Script",
    "path": "res://addons/A1MyAddon/Helpers/ThemeSwitcherComponentHelper.cs",
    "id": "1_helper_script",
    "uid": "uid://placeholder_theme_helper"
})

# Save
output_path = "C:/Godot/3d-practice/A1UIScenes/UIComponents/ThemeSwitcherComponent.tscn"
ui.save(output_path)
print(f"Generated: {output_path}")
