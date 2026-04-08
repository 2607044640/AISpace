---
inclusion: manual
---

# Godot UI Builder

<critical_rules>

## File Organization

**ALL generated Python scripts MUST be placed in:**
`C:\Godot\KiroWorkingSpace\.kiro\scripts\temp\`

- Create the `temp` folder if it doesn't exist
- NEVER place generated scripts in project root or other locations
- This keeps the workspace clean and organized

## Mandatory Validation Workflow

**After generating or modifying ANY .tscn file:**

1. **Run the Scene** - Test the scene directly in the running Godot project:
```python
mcp_godot_run_project(projectPath="c:/Godot/3d-practice", scene="res://A1UIScenes/GameSettings.tscn")
```

2. **Check for Errors** - If scene fails to load or has issues:
```python
mcp_godot_get_debug_output()
```

3. **Fix Errors** - Common issues:
   - Array format: Use `PackedStringArray("item1", "item2")`, NOT `['item1', 'item2']`
   - Missing parent attribute: All nodes except first MUST have `parent="."` or `parent="path"`
   - Invalid UID: Use `mcp_godot_get_uid()` to obtain correct UIDs
   - Property format: Color(r,g,b,a), Vector2(x,y), NodePath("path")

4. **Re-validate** - Repeat steps 1-3 until scene runs successfully

5. **Stop the Scene** - Clean up after testing:
```python
mcp_godot_stop_project()
```

**NEVER skip validation.** Parse errors break the entire scene file.

</critical_rules>

## Execution Protocol

Write Python scripts using `.kiro/scripts/ui_builder/generators/godot_ui_builder.py`. Execute to generate `.tscn` files.

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
margin = root.add_margin_container("Margin", uniform=30, use_anchors=True)
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
settings_section = vbox.add_vbox("Settings", separation=15)
```

**4. Component Rows**
```python
row = settings_section.add_hbox("VolumeRow", separation=15)
row.add_label("Label", text="Volume:", min_size=(150, 0), size_flags_h=0)
row.add_progress_bar("Bar", value=75, size_flags_h=3, show_percentage=True)
row.add_button("Reset", text="Reset", size_flags_h=4)
```

**5. Prefab Instances**
```python
# Get UID first via MCP
uid_result = mcp_godot_get_uid(
    projectPath="c:/Godot/3d-practice",
    filePath="A1UIScenes/UIComponents/SliderComponent.tscn"
)
# Use obtained UID
vbox.add_instance("MusicVolume", 
                 scene_path="res://A1UIScenes/UIComponents/SliderComponent.tscn",
                 scene_uid="uid://dbaix0lcy10v2")
```

## Critical Rules

### Spacing: Never Nest MarginContainers in BoxContainers

BoxContainers handle spacing via `separation`. MarginContainer wrappers create redundant nodes.

**Wrong:**
```python
vbox = parent.add_vbox("VBox")
margin1 = vbox.add_margin_container("Wrapper1", uniform=10)  # Redundant!
margin1.add_button("Button1", text="OK")
margin2 = vbox.add_margin_container("Wrapper2", uniform=10)  # Redundant!
margin2.add_button("Button2", text="Cancel")
```

**Correct:**
```python
vbox = parent.add_vbox("VBox", separation=10)  # Spacing handled here
vbox.add_button("Button1", text="OK")
vbox.add_button("Button2", text="Cancel")
```

Use MarginContainer ONLY for:
- Root-level screen margins (with `use_anchors=True`)
- Inner padding of PanelContainers

### NodePaths: Never Calculate Manually

**Wrong:**
```python
transition = ground_mode.add_node("ToAir")
transition.set_property("to", 'NodePath("../../Air/FlyMode")')  # Brain-calculated
```

**Correct:**
```python
ground_mode = root.add_node("GroundMode")
fly_mode = root.add_node("FlyMode")
transition = ground_mode.add_node("ToAir")
exact_path = transition.get_relative_path_to(fly_mode)
transition.set_property("to", f'NodePath("{exact_path}")')
```

Applies to: StateChart transitions (`to`), signal connections (`target`), exported node references.

### Anchors: Use ONLY on Root MarginContainer

```python
margin = root.add_margin_container("Margin", uniform=30, use_anchors=True)
margin.set_property("anchors_preset", 15)  # Full rect
margin.set_property("anchor_right", 1.0)
margin.set_property("anchor_bottom", 1.0)
margin.set_property("grow_horizontal", 2)  # Both directions
margin.set_property("grow_vertical", 2)
```

For children, use `size_flags_h/v` instead.

## Size Flags

| Value | Behavior | Use For |
|-------|----------|---------|
| `0` | Fixed size | Labels (with `min_size`) |
| `3` | Fill + Expand | Sliders, progress bars, text fields |
| `4` | Shrink Center | Buttons, icons |

**Example:**
```python
row = vbox.add_hbox("Row", separation=15)
row.add_label("Label", text="Volume:", min_size=(150, 0), size_flags_h=0)  # Fixed
row.add_progress_bar("Bar", size_flags_h=3)  # Expands
row.add_button("Reset", text="Reset", size_flags_h=4)  # Centered
```

## API Reference

### UIBuilder
- `UIBuilder(scene_name, scene_uid=None)`
- `create_control(name="Control", fullscreen=True)`
- `save(output_path)`

### Containers
- `add_margin_container(name, uniform=None, use_anchors=False, vertical_margin=None, horizontal_margin=None, script=None)`
- `add_panel_container(name)`
- `add_scroll_container(name, horizontal_scroll=0, vertical_scroll=2, follow_focus=True)`
- `add_vbox(name, separation=None)`
- `add_hbox(name, separation=None)`

### Elements
- `add_color_rect(name, color=(r,g,b,a), use_anchors=False)`
- `add_label(name, text="", align="left", font_size=None, min_size=None, size_flags_h=None)`
- `add_button(name, text="", size_flags_h=None)`
- `add_checkbox(name, text="", size_flags_h=None, button_pressed=False)`
- `add_progress_bar(name, value=0, size_flags_h=None, size_flags_v=None, size_flags_stretch_ratio=None, min_size=None, show_percentage=True)`
- `add_instance(name, scene_path, scene_uid)` - **scene_uid REQUIRED, use mcp_godot_get_uid**
- `add_separator(name, separation=None, style=None)`

### Utility
- `set_property(key, value)` - Chainable
- `get_relative_path_to(target_node)` - Calculate NodePath

## Prefabs

**Location:** `3d-practice/A1UIScenes/UIComponents/`

| Prefab | UID | Helper Script UID | Contents |
|--------|-----|-------------------|----------|
| `SliderComponent.tscn` | `uid://dbaix0lcy10v2` | `uid://jt7xkk4cigis` | Label + HSlider + SpinBox + Reset |
| `ToggleComponent.tscn` | `uid://dpf5ovda3xlpv` | `uid://bi3yf7y5ir5ws` | Label + CheckBox + Reset |
| `DropdownComponent.tscn` | `uid://0st2knyluaer` | `uid://djd3xoidagqxf` | Label + OptionButton + Reset |
| `OptionComponent.tscn` | `uid://ddxph7didmq` | `uid://cq622dbolkfw0` | Label + Button (PopupMenu) + Reset |

**CRITICAL:** All component scenes MUST attach their Helper script. Use `mcp_godot_get_uid` to obtain correct UIDs.

**Get Scene UID:**
```python
# Via MCP tool
mcp_godot_get_uid(
    projectPath="c:/Godot/3d-practice",
    filePath="A1UIScenes/UIComponents/DropdownComponent.tscn"
)
# Returns: uid://0st2knyluaer
```

**Usage:**
```python
vbox.add_instance("MusicVolume", 
                 scene_path="res://A1UIScenes/UIComponents/SliderComponent.tscn",
                 scene_uid="uid://dbaix0lcy10v2")
```

## TabContainer Support

Add to script before creating UI:

```python
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

**Usage:**
```python
tabs = vbox.add_tab_container("Tabs")
audio_tab = tabs.add_tab("Audio")
audio_margin = audio_tab.add_margin_container("Margin", uniform=20, script=None)
audio_vbox = audio_margin.add_vbox("Content", separation=15)
```

## Complete Example

```python
ui = UIBuilder("Settings", scene_uid="uid://example123")
root = ui.create_control("Control", fullscreen=True)

# Background
root.add_color_rect("BG", color=(0.15, 0.15, 0.15, 1), use_anchors=True)

# Fullscreen margin
margin = root.add_margin_container("Margin", uniform=30, use_anchors=True, script=None)
margin.set_property("anchors_preset", 15)
margin.set_property("anchor_right", 1.0)
margin.set_property("anchor_bottom", 1.0)
margin.set_property("grow_horizontal", 2)
margin.set_property("grow_vertical", 2)

# Panel + inner margin
panel = margin.add_panel_container("Panel")
inner = panel.add_margin_container("Inner", uniform=20, script=None)

# Content
vbox = inner.add_vbox("Content", separation=20)
vbox.add_label("Title", text="Settings", align="center", font_size=32)

# Prefabs
vbox.add_instance("MusicVolume", 
                 scene_path="res://A1UIScenes/UIComponents/SliderComponent.tscn",
                 scene_uid="uid://dbaix0lcy10v2")
vbox.add_instance("Fullscreen", 
                 scene_path="res://A1UIScenes/UIComponents/ToggleComponent.tscn",
                 scene_uid="uid://dpf5ovda3xlpv")

# Buttons
buttons = vbox.add_hbox("Buttons", separation=15)
buttons.add_button("Apply", text="Apply", size_flags_h=4)
buttons.add_button("Cancel", text="Cancel", size_flags_h=4)

ui.save("res://Scenes/Settings.tscn")
```

## TscnEditor Tools

**Location:** `KiroWorkingSpace/.kiro/scripts/ui_builder/tscn_editor_tools/`

**When to Use:**
- **UIBuilder:** Generate new scenes from scratch
- **TscnEditor:** Modify existing scenes programmatically (直接修改原文件)

**Core Library Files:**
- `parser.py` - Parses .tscn text format into structured data
- `node_tree.py` - Internal tree representation with efficient indices
- `pretty_printer.py` - Formats Node_Tree back to .tscn text
- `TscnReader.py` - Read-only query API (TscnReader)
- `TscnEditor.py` - Modification API (TscnEditor)
- `types.py` - Type definitions (Node, Color, Vector2, etc.)
- `__init__.py` - Package initialization

### Read Scene Structure

```python
from tscn_editor_tools import TscnReader

reader = TscnReader("3d-practice/A1UIScenes/SettingsMenuV2.tscn")

# Visualize hierarchy
print(reader.print_tree_view())

# Query nodes
buttons = reader.find_nodes_by_type("Button")

# Access node via tree API
game_content_node = reader.tree.get_node_by_path("Parent/Child")
children = reader.tree.get_children("Parent/Child")

# Check properties
text = reader.get_node_property("BackButton_Button", "text")
```

### Modify Scene Properties

```python
from tscn_editor_tools import TscnEditor, PropertyUpdate, Color

editor = TscnEditor("3d-practice/A1UIScenes/SettingsMenuV2.tscn")

# Update single property
editor.update_property("Background_ColorRect", "color", Color(0.2, 0.2, 0.2, 1))

# Update array properties (自动转换为 PackedStringArray)
editor.update_property("NumberFormat", "Items", ["23", "43", "08293"])

# Batch updates
updates = [
    PropertyUpdate("BackButton_Button", "text", "返回"),
    PropertyUpdate("ResetButton_Button", "text", "重置"),
    PropertyUpdate("MasterVolume", "LabelText", "主音量"),
]
result = editor.update_properties_batch(updates)

# Add new node
editor.add_node("NewButton", "Button", "MainVBox_VBoxContainer", 
                properties={"text": "New Button"})

# Remove node
editor.remove_node("OldButton")

# Save changes (直接覆盖原文件)
editor.save()  # Overwrites original - THIS IS THE DEFAULT BEHAVIOR
# or
editor.save("output.tscn")  # Save to new file only if needed
```

### Preserve All Metadata

TscnEditor preserves:
- Node unique_id values
- Scene UID in header
- External resource UIDs
- Property formatting (Color, Vector2, NodePath, ExtResource, PackedStringArray)
- Node order and hierarchy

**Round-trip guarantee:** Parse → Modify → Save → Parse produces equivalent structure.

**Array Formatting:** Python lists are automatically converted to `PackedStringArray("item1", "item2")` format.

## Technical Notes

- **MarginContainerHelper:** Default script is `res://addons/A1MyAddon/Helpers/MarginContainerHelper.cs`. Set `script=None` to disable.
- **ProgressBar:** Set `show_percentage=True` to display value text.
- **Separator:** Requires style resource. Use `style="res://path/to/style.tres"` or `style=None`.
- **Component Helper Scripts:** All UI component scenes MUST attach their corresponding Helper script (SliderComponentHelper, ToggleComponentHelper, DropdownComponentHelper, OptionComponentHelper). Without the script, LabelText and other properties will not function.
- **UID Verification:** Always use `mcp_godot_get_uid` to obtain correct UIDs. Never use placeholder or guessed UIDs.
- **TscnEditor Default Behavior:** `editor.save()` directly overwrites the original file. This is intentional for in-place modifications.
