---
inclusion: manual
---

# Godot UI Builder

## Execution Protocol

Write Python scripts using `.kiro/scripts/ui_builder/godot_ui_builder.py`. Execute to generate `.tscn` files.

**Never manually edit .tscn files.**
**Never calculate NodePaths manually.** Use `get_relative_path_to()`.

## 5-Step UI Creation

**1. Root + Background**
```python
ui = UIBuilder("MenuName", scene_uid="uid://...")
root = ui.create_control("Control", fullscreen=True)
root.add_color_rect("BG", color=(0.15, 0.15, 0.15, 1), use_anchors=True)
```

**2. Fullscreen Margin**
```python
margin = root.add_margin_container("Margin", uniform=30, use_anchors=True, script=None)
margin.set_property("anchors_preset", 15)
margin.set_property("anchor_right", 1.0)
margin.set_property("anchor_bottom", 1.0)
margin.set_property("grow_horizontal", 2)
margin.set_property("grow_vertical", 2)
```

**3. Content Structure**
```python
vbox = margin.add_vbox("Content", separation=20)
vbox.add_label("Title", text="Settings", align="center", font_size=32)
```

**4. Component Rows**
```python
row = vbox.add_hbox("Row", separation=15)
row.add_label("Label", text="Volume:", min_size=(150, 0), size_flags_h=0)
row.add_progress_bar("Bar", value=75, size_flags_h=3)
row.add_button("Reset", text="Reset", size_flags_h=4)
```

**5. Prefab Instances**
```python
vbox.add_instance("MusicVolume", 
                 scene_path="res://A1UIScenes/UIComponents/SliderComponent.tscn",
                 scene_uid="uid://dbaix0lcy10v2")
```

## Critical Rules

**Spacing:** Use `separation` on BoxContainers. Never nest MarginContainers inside BoxContainers for spacing.

**Anchors:** Use `use_anchors=True` ONLY on root MarginContainer. Use `size_flags_h/v` for children.

**NodePaths:** Always use `get_relative_path_to()`. Never write paths like `"../../Node"`.

## Size Flags

- `0` = Fixed (use with `min_size`)
- `3` = Fill + Expand (sliders, text fields)
- `4` = Shrink Center (buttons)

## Available Prefabs

Location: `3d-practice/A1UIScenes/UIComponents/`

- `SliderComponent.tscn` (uid://dbaix0lcy10v2)
- `ToggleComponent.tscn` (uid://dpf5ovda3xlpv)
- `DropdownComponent.tscn` (uid://5b9ifgnj5kmv5d)
- `OptionComponent.tscn` (uid://ddxph7didmq)

All use 150px fixed-width labels.

## API Reference

**UIBuilder:**
- `UIBuilder(scene_name, scene_uid=None)`
- `create_control(name, fullscreen=True)`
- `save(output_path)`

**Containers:**
- `add_margin_container(name, uniform=None, use_anchors=False, script=None)`
- `add_vbox(name, separation=None)`
- `add_hbox(name, separation=None)`
- `add_panel_container(name)`
- `add_scroll_container(name, horizontal_scroll=0, vertical_scroll=2)`

**Elements:**
- `add_color_rect(name, color=(r,g,b,a), use_anchors=False)`
- `add_label(name, text="", align="left", font_size=None, min_size=None, size_flags_h=None)`
- `add_button(name, text="", size_flags_h=None)`
- `add_checkbox(name, text="", size_flags_h=None, button_pressed=False)`
- `add_progress_bar(name, value=0, size_flags_h=None, show_percentage=True)`
- `add_instance(name, scene_path, scene_uid=None)`

**Utility:**
- `set_property(key, value)`
- `get_relative_path_to(target_node)`

## TabContainer Support

```python
# Extend UINode to add TabContainer
def add_tab_container(self, name: str):
    node = UINode(name, "TabContainer")
    node.properties["layout_mode"] = 2
    node.properties["size_flags_vertical"] = 3
    return self._add_child(node)

def add_tab(self, name: str):
    node = UINode(name, "MarginContainer", auto_suffix=False)
    node.properties["layout_mode"] = 2
    return self._add_child(node)

UINode.add_tab_container = add_tab_container
UINode.add_tab = add_tab
```

## Complete Example

```python
ui = UIBuilder("Settings", scene_uid="uid://example")
root = ui.create_control("Control", fullscreen=True)
root.add_color_rect("BG", color=(0.1, 0.1, 0.12, 1), use_anchors=True)

margin = root.add_margin_container("Margin", uniform=40, use_anchors=True, script=None)
margin.set_property("anchors_preset", 15)
margin.set_property("anchor_right", 1.0)
margin.set_property("anchor_bottom", 1.0)
margin.set_property("grow_horizontal", 2)
margin.set_property("grow_vertical", 2)

vbox = margin.add_vbox("Content", separation=20)
vbox.add_label("Title", text="Settings", align="center", font_size=48)

tabs = vbox.add_tab_container("Tabs")

# Audio tab
audio = tabs.add_tab("Audio")
audio_margin = audio.add_margin_container("Margin", uniform=20, script=None)
audio_vbox = audio_margin.add_vbox("Content", separation=15)
audio_vbox.add_instance("Master", 
                       scene_path="res://A1UIScenes/UIComponents/SliderComponent.tscn",
                       scene_uid="uid://dbaix0lcy10v2")

# Buttons
buttons = vbox.add_hbox("Buttons", separation=15)
buttons.add_button("Back", text="Back", size_flags_h=4)

ui.save("res://A1UIScenes/Settings.tscn")
```
