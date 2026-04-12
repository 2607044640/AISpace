---
inclusion: manual
---

<document_structure>

  <layer_1_quick_start>
    <quick_reference>
      * **Script Output Path:** All generated Python scripts MUST be placed in `C:\Godot\KiroWorkingSpace\.kiro\scripts\temp\`
      * **UI Generator Path:** `.kiro/scripts/ui_builder/generators/godot_ui_builder.py`
      * **StateChart Generator Path:** `.kiro/scripts/statechart_builder/godot_statechart_builder.py`
      * **TscnEditor Path:** `.kiro/scripts/ui_builder/tscn_editor_tools/`
      * **Validation Command:** `mcp_godot_run_project(projectPath="c:/Godot/3d-practice", scene="res://A1UIScenes/...")`
      * **UID Fetch Command:** `mcp_godot_get_uid(projectPath="c:/Godot/3d-practice", filePath="...")`
    </quick_reference>

    <decision_tree>
      * If you need to build an entire initial UI layout from scratch -> Use `UIBuilder` generator. (Why: It rapidly constructs correct node hierarchies and handles repetitive boilerplate efficiently.)
      * If you need to programmatically batch-modify multiple properties in an existing UI -> Use `TscnEditor`. (Why: It reads and modifies the `.tscn` text directly without breaking existing UUIDs, external references, or node order.)
      * If you need to tweak a single layout margin, color, or minor visual detail -> Edit manually in the Godot Editor. (Why: Using AI for single-property micro-tweaks is slow, inaccurate, and wastes time.)
    </decision_tree>

    <end_to_end_example>
      <![CDATA[
# 1. Generate the UI script
from ui_builder.generators.godot_ui_builder import UIBuilder

ui = UIBuilder("HelloWorldMenu", scene_uid="uid://example_hello_123")
root = ui.create_control("Control", fullscreen=True)
root.add_color_rect("BG", color=(0.1, 0.1, 0.1, 1), use_anchors=True)

vbox = root.add_vbox("Content", separation=20)
vbox.add_label("Greeting", text="Hello World", align="center", font_size=48)
vbox.add_button("StartBtn", text="Start", size_flags_h=4)

# MUST save to the designated temp directory or standard scene folder
ui.save("res://A1UIScenes/HelloWorldMenu.tscn")

# 2. Terminal / Validation Commands (Run via MCP)
# Execute this to test the scene visually:
# mcp_godot_run_project(projectPath="c:/Godot/3d-practice", scene="res://A1UIScenes/HelloWorldMenu.tscn")

# If it fails, check errors:
# mcp_godot_get_debug_output()

# When done testing, shut it down:
# mcp_godot_stop_project()
      ]]>
    </end_to_end_example>

    <top_anti_patterns>
      * **Manually calculating NodePaths.** (Why: Hardcoding strings like `"../../Air/FlyMode"` leads to fatal path mismatches if the hierarchy changes; always use `get_relative_path_to(target)` to let the script resolve it.)
      * **Nesting `MarginContainer` wrappers inside `BoxContainers`.** (Why: It creates redundant nodes and clutters the tree; BoxContainers inherently handle spacing between elements using the `separation` property.)
      * **Saving generated scripts outside the `temp` directory.** (Why: Placing generated scripts in the project root litters the KiroWorkingSpace and violates strict workspace file organization rules.)
    </top_anti_patterns>
  </layer_1_quick_start>

  <layer_2_detailed_guide>
    <api_reference>
      **UIBuilder Class**
      * `UIBuilder(scene_name: str, scene_uid: str = None)`
      * `create_control(name="Control", fullscreen=True)`
      * `save(output_path: str)`

      **Containers (Methods on UINode)**
      * `add_margin_container(name, uniform=None, use_anchors=False, vertical_margin=None, horizontal_margin=None, script=None)`
      * `add_panel_container(name)`
      * `add_scroll_container(name, horizontal_scroll=0, vertical_scroll=2, follow_focus=True)`
      * `add_vbox(name, separation=None)`
      * `add_hbox(name, separation=None)`
      * `add_tab_container(name)` *(Requires manual monkey-patch)*
      * `add_tab(name)` *(Requires manual monkey-patch)*

      **Elements (Methods on UINode)**
      * `add_color_rect(name, color=(r,g,b,a), use_anchors=False)`
      * `add_label(name, text="", align="left", font_size=None, min_size=None, size_flags_h=None)`
      * `add_button(name, text="", size_flags_h=None)`
      * `add_checkbox(name, text="", size_flags_h=None, button_pressed=False)`
      * `add_progress_bar(name, value=0, size_flags_h=None, size_flags_v=None, size_flags_stretch_ratio=None, min_size=None, show_percentage=True)`
      * `add_instance(name, scene_path, scene_uid)`
      * `add_separator(name, separation=None, style=None)`
      
      **Utility (Methods on UINode)**
      * `set_property(key, value)` *(Chainable)*
      * `get_relative_path_to(target_node)`

      **TscnEditor Tools**
      * `TscnReader(filepath: str)`
          * `print_tree_view()`
          * `find_nodes_by_type(node_type: str)`
          * `get_node_property(node_name: str, property: str)`
          * `tree.get_node_by_path(path: str)`
          * `tree.get_children(path: str)`
      * `TscnEditor(filepath: str)`
          * `update_property(node_name: str, property: str, value: Any)`
          * `update_properties_batch(updates: List[PropertyUpdate])`
          * `add_node(name: str, node_type: str, parent_path: str, properties: dict)`
          * `remove_node(node_name: str)`
          * `save(filepath: str = None)`
    </api_reference>

    <core_rules>
      **5-Step UI Creation Workflow:**
      1.  **Root + Background:** Establish the base `Control` node and an anchored `ColorRect` for the background.
      2.  **Fullscreen Margin:** Apply a `MarginContainer` with anchors preset 15 to map the safe zones.
      3.  **Content Structure:** Divide the space logically using `VBoxContainer` or `HBoxContainer`.
      4.  **Component Rows:** Populate the containers with raw elements (`Label`, `ProgressBar`, `Button`) utilizing `size_flags_h/v`.
      5.  **Prefab Instances:** Inject reusable UI elements with exact UIDs (fetched via `mcp_godot_get_uid`).

      **Size Flags Matrix (`size_flags_h/v`):**
      | Value | Godot Behavior | Common Use Case |
      | :--- | :--- | :--- |
      | `0` | Fixed size | Labels (using `min_size`) |
      | `3` | Fill + Expand | Sliders, progress bars, text input fields |
      | `4` | Shrink Center | Buttons, centered icons |

      **Standard UI Prefabs & UIDs:**
      | Prefab Name | Scene UID | Helper Script UID |
      | :--- | :--- | :--- |
      | `SliderComponent.tscn` | `uid://dbaix0lcy10v2` | `uid://jt7xkk4cigis` |
      | `ToggleComponent.tscn` | `uid://dpf5ovda3xlpv` | `uid://bi3yf7y5ir5ws` |
      | `DropdownComponent.tscn`| `uid://0st2knyluaer` | `uid://djd3xoidagqxf` |
      | `OptionComponent.tscn` | `uid://ddxph7didmq` | `uid://cq622dbolkfw0` |
      *(Note: Component Helper Scripts are mandatory for prefab functionality).*
    </core_rules>

    <code_templates>
      **1. Monkey-Patching TabContainers**
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

      **2. TscnEditor Batch Modification**
      ```python
      from tscn_editor_tools import TscnEditor, PropertyUpdate, Color

      editor = TscnEditor("3d-practice/A1UIScenes/SettingsMenu.tscn")
      
      updates = [
          PropertyUpdate("ApplyButton_Button", "text", "Apply Changes"),
          PropertyUpdate("CancelButton_Button", "text", "Discard"),
          PropertyUpdate("ListFormat", "Items", ["Item A", "Item B"]) # Auto PackedStringArray
      ]
      editor.update_properties_batch(updates)
      
      editor.save() # Overwrites original file
      ```
    </code_templates>
  </layer_2_detailed_guide>

  <layer_3_advanced>
    <troubleshooting>
      * **Symptom:** Scene fails to parse or load in Godot Editor.
          * *Cause:* Python lists were passed to an array property without specific handling.
          * *Fix:* Ensure you are outputting arrays in the Godot native format: `PackedStringArray("item1", "item2")`. (Note: `TscnEditor` does this automatically, but raw text modifications or edge cases in `UIBuilder` might fail).
      * **Symptom:** Nodes are placed at the root level instead of inside their intended containers.
          * *Cause:* Missing `parent="."` or `parent="path"` attribute on the `.tscn` node entry.
          * *Fix:* Verify that the `UIBuilder` generator correctly appended the child to its `UINode` parent.
      * **Symptom:** Instanced prefabs appear broken or lack custom properties like `LabelText`.
          * *Cause:* The instanced component is missing its corresponding helper script, or an invalid/guessed UID was passed to `add_instance`.
          * *Fix:* Always query actual UIDs with `mcp_godot_get_uid` and verify the helper scripts (`uid://jt7xkk4cigis` etc.) are attached to the source prefabs.
    </troubleshooting>

    <best_practices>
      * **Anchoring Discipline:** Use anchors (`use_anchors=True`, `anchors_preset=15`) strictly on the root `Control` and the immediate root `MarginContainer`. Everything nested below should rely exclusively on Godot's BoxContainer flow and `size_flags_h/v`.
      * **Mandatory Validation Loop:** NEVER skip validation. Use `mcp_godot_run_project` after generating/editing a `.tscn` file. Because `.tscn` relies on exact text parsing, a single malformed property string breaks the whole file. 
      * **TscnEditor Destructive Default:** Calling `editor.save()` with no arguments will *overwrite the original file*. This is the intended behavior for iterative in-place modifications, but be mindful of your data state before executing.
    </best_practices>
  </layer_3_advanced>

</document_structure>