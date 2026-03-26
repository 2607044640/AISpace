---
inclusion: manual
---

# Godot UI Builder

<execution>
Write Python script using `.kiro/scripts/ui_builder/godot_ui_builder.py`, then execute to generate `.tscn` file.
</execution>

<workflow>
1. Background: Add `ColorRect` or `PanelContainer` as base layer
2. Margins: Add `MarginContainer` with `use_anchors=True` and `anchors_preset=15`
3. Layout: Use `VBoxContainer`/`HBoxContainer` with `separation` parameter
4. Elements: Add `Button`, `Label`, `ProgressBar` with `size_flags_h`/`size_flags_v`
</workflow>

<api>
**UIBuilder:**
- `UIBuilder(scene_name, scene_uid=None)`
- `create_control(name="Control", fullscreen=True)` - Root node
- `save(output_path)` - Write .tscn file

**Containers:**
- `add_margin_container(name, uniform=None, use_anchors=False, vertical_margin=None, horizontal_margin=None)`
- `add_panel_container(name)`
- `add_scroll_container(name, horizontal_scroll=0, vertical_scroll=2, follow_focus=True)`
- `add_vbox(name, separation=None)`
- `add_hbox(name, separation=None)`

**Elements:**
- `add_color_rect(name, color=(r,g,b,a), use_anchors=False)`
- `add_label(name, text="", align="left", font_size=None, min_size=None, size_flags_h=None)`
- `add_button(name, text="", size_flags_h=None)`
- `add_checkbox(name, text="", size_flags_h=None, button_pressed=False)`
- `add_progress_bar(name, value=0, size_flags_h=None, show_percentage=True)`
- `add_instance(name, scene_path, scene_uid=None)` - Instance prefab

**Utility:**
- `set_property(key, value)` - Chainable property setter
- `get_relative_path_to(target_node)` - Calculate NodePath
</api>

<critical_rules>
**Anchors:**
Use ONLY on root containers. Never on BoxContainer children. Use `size_flags_h`/`size_flags_v` instead.

**Fullscreen Setup:**
```python
margin = root.add_margin_container("Margin", uniform=50, use_anchors=True)
margin.set_property("anchors_preset", 15)
margin.set_property("anchor_right", 1.0)
margin.set_property("anchor_bottom", 1.0)
margin.set_property("grow_horizontal", 2)
margin.set_property("grow_vertical", 2)
```

**Size Flags:**
- `0` = None (fixed-size with `custom_minimum_size`)
- `3` = Fill + Expand (containers, progress bars)
- `4` = Shrink Center (buttons)

**Component Row Pattern:**
```
HBoxContainer (separation=15)
├─ Label (min_size=(150,0), size_flags_h=0)
├─ MainControl (size_flags_h=3)
└─ ActionButton (size_flags_h=4)
```

**Spacing:**
Control via `separation` on BoxContainers. Never wrap children in MarginContainers for spacing.

**ProgressBars:**
Always set `show_percentage=True`.

**NodePaths:**
Use `source_node.get_relative_path_to(target_node)`. Never calculate manually.

**MarginContainerHelper:**
Default script: `res://addons/A1MyAddon/Helpers/MarginContainerHelper.cs`. Set `script=None` to disable.
</critical_rules>

<prefabs>
**Built-in Components:**
- `OptionComponent.tscn` - Label + Dropdown + Reset
- `SliderComponent.tscn` - Label + ProgressBar + Reset
- `ToggleComponent.tscn` - Label + CheckBox + Reset
- `DropdownComponent.tscn` - Label + Display + Arrow + Reset

**Usage:**
```python
vbox.add_instance("MusicVolume", 
                 scene_path="res://A1UIScenes/UIComponents/SliderComponent.tscn")
```

**Standard:**
All prefabs use 150px fixed-width labels (`min_size=(150,0), size_flags_h=0`) for perfect alignment.
</prefabs>

<examples>

<example>
<description>Fullscreen menu</description>
<code>
ui = UIBuilder("MainMenu")
root = ui.create_control("Control", fullscreen=True)
root.add_color_rect("BG", color=(0.1, 0.1, 0.15, 1))

margin = root.add_margin_container("Margin", uniform=50, use_anchors=True)
margin.set_property("anchors_preset", 15)
margin.set_property("anchor_right", 1.0)
margin.set_property("anchor_bottom", 1.0)

vbox = margin.add_vbox("Menu", separation=30)
vbox.add_label("Title", text="Main Menu", align="center", font_size=64)
vbox.add_button("Start", text="Start Game", size_flags_h=4)
vbox.add_button("Quit", text="Quit", size_flags_h=4)

ui.save("res://Scenes/MainMenu.tscn")
</code>
</example>

<example>
<description>Settings row</description>
<code>
row = vbox.add_hbox("VolumeRow", separation=15)
row.add_label("Label", text="Volume:", min_size=(150, 0), size_flags_h=0)
row.add_progress_bar("Bar", value=75, size_flags_h=3, show_percentage=True)
row.add_button("Reset", text="Reset", size_flags_h=4)
</code>
</example>

<example>
<description>Using prefabs</description>
<code>
vbox.add_instance("MusicVolume", scene_path="res://A1UIScenes/UIComponents/SliderComponent.tscn")
vbox.add_instance("Fullscreen", scene_path="res://A1UIScenes/UIComponents/ToggleComponent.tscn")
</code>
</example>

</examples>
