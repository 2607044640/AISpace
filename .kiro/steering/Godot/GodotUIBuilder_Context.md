<godot_ui_builder_instructions>

  <file_management>
    <rule>
      <description>Store ALL rules, steering files, and instructions exclusively in `KiroWorkingSpace/.kiro/`.</description>
    </rule>
    <rule>
      <description>Place ALL generated Python scripts inside `C:\Godot\KiroWorkingSpace\.kiro\scripts\temp\`.</description>
      <rationale>Keeps the workspace clean and organized. Create the `temp` folder if it does not exist. NEVER place generated scripts in the project root.</rationale>
    </rule>
  </file_management>

  <scene_management>
    <ui_workflow_best_practices>
      - USE AI to build the entire initial UI layout via UIBuilder generator (`.kiro/scripts/ui_builder/generators/godot_ui_builder.py`).
      - USE AI to batch-modify multiple properties via TscnEditor (`.kiro/scripts/ui_builder/tscn_editor_tools/`).
      - USE AI to generate StateChart scenes via `.kiro/scripts/statechart_builder/godot_statechart_builder.py`.
      - DO NOT use AI to modify small, single-property details. The user must manually edit these directly in the Godot editor to save time and ensure accuracy.
      - DO NOT manually edit `.tscn` files.
    </ui_workflow_best_practices>

    <validation_workflow>
      <description>Execute this mandatory validation workflow after generating or modifying ANY `.tscn` file. NEVER skip validation; parse errors break the entire scene.</description>
      <step_1>Run the Scene: `mcp_godot_run_project(projectPath="c:/Godot/3d-practice", scene="res://A1UIScenes/GameSettings.tscn")`</step_1>
      <step_2>Check for Errors: `mcp_godot_get_debug_output()`</step_2>
      <step_3>Fix Errors: Check array formats (use `PackedStringArray("a", "b")`, not `['a', 'b']`), missing parent attributes (all nodes except first MUST have `parent="."` or `parent="path"`), invalid UIDs (use `mcp_godot_get_uid()`), and property formats (`Color(r,g,b,a)`, `Vector2(x,y)`, `NodePath("path")`).</step_3>
      <step_4>Re-validate: Repeat steps 1-3 until successful.</step_4>
      <step_5>Stop the Scene: `mcp_godot_stop_project()`</step_5>
    </validation_workflow>
  </scene_management>

  <critical_rules>
    <rule>
      <description>NEVER nest MarginContainers inside BoxContainers. Use MarginContainer ONLY for root-level screen margins (with `use_anchors=True`) or inner padding of PanelContainers.</description>
      <rationale>BoxContainers handle their own spacing via the `separation` property. MarginContainer wrappers create redundant node overhead.</rationale>
      <example>
        # WRONG
        vbox = parent.add_vbox("VBox")
        margin1 = vbox.add_margin_container("Wrapper1", uniform=10)  # Redundant!
        margin1.add_button("Button1", text="OK")
        margin2 = vbox.add_margin_container("Wrapper2", uniform=10)  # Redundant!
        margin2.add_button("Button2", text="Cancel")

        # CORRECT
        vbox = parent.add_vbox("VBox", separation=10)  # Spacing handled here
        vbox.add_button("Button1", text="OK")
        vbox.add_button("Button2", text="Cancel")
      </example>
    </rule>

    <rule>
      <description>NEVER calculate NodePaths manually. ALWAYS use `get_relative_path_to(target_node)`.</description>
      <rationale>Manual path calculation is error-prone. Programmatic pathing ensures accuracy for StateChart transitions (`to`), signal connections (`target`), and exported node references.</rationale>
      <example>
        # WRONG
        transition = ground_mode.add_node("ToAir")
        transition.set_property("to", 'NodePath("../../Air/FlyMode")')  # Brain-calculated

        # CORRECT
        ground_mode = root.add_node("GroundMode")
        fly_mode = root.add_node("FlyMode")
        transition = ground_mode.add_node("ToAir")
        exact_path = transition.get_relative_path_to(fly_mode)
        transition.set_property("to", f'NodePath("{exact_path}")')
      </example>
    </rule>

    <rule>
      <description>Use Anchors ONLY on the Root MarginContainer. For child elements, use `size_flags_h` and `size_flags_v` instead.</description>
      <rationale>Children sizes should be managed by their parent containers to maintain responsive layouts.</rationale>
      <example>
        # CORRECT ANCHOR USAGE ON ROOT
        margin = root.add_margin_container("Margin", uniform=30, use_anchors=True)
        margin.set_property("anchors_preset", 15)  # Full rect
        margin.set_property("anchor_right", 1.0)
        margin.set_property("anchor_bottom", 1.0)
        margin.set_property("grow_horizontal", 2)  # Both directions
        margin.set_property("grow_vertical", 2)
      </example>
    </rule>
    
    <rule>
      <description>ALWAYS use `mcp_godot_get_uid` to obtain correct UIDs. NEVER use placeholder or guessed UIDs.</description>
      <rationale>Using incorrect UIDs will break prefab instantiation and scene resource loading.</rationale>
      <example>
        # Get UID first via MCP
        uid_result = mcp_godot_get_uid(
            projectPath="c:/Godot/3d-practice",
            filePath="A1UIScenes/UIComponents/SliderComponent.tscn"
        )
        # Use obtained UID
        vbox.add_instance("MusicVolume", 
                         scene_path="res://A1UIScenes/UIComponents/SliderComponent.tscn",
                         scene_uid="uid://dbaix0lcy10v2")
      </example>
    </rule>

    <rule>
      <description>Ensure all UI component scenes attach their corresponding Helper script.</description>
      <rationale>Prefabs like SliderComponent or ToggleComponent rely on Helper scripts (SliderComponentHelper, etc.) to function. Without them, properties like `LabelText` will fail.</rationale>
    </rule>
  </critical_rules>

  <ui_creation_flow>
    <description>Follow this strict 5-step process when generating UIs.</description>
    <example>
      # 1. Root + Background
      ui = UIBuilder("MenuName", scene_uid="uid://...")
      root = ui.create_control("Control", fullscreen=True)
      root.add_color_rect("BG", color=(0.15, 0.15, 0.15, 1), use_anchors=True)

      # 2. Fullscreen Margin
      margin = root.add_margin_container("Margin", uniform=30, use_anchors=True)
      margin.set_property("anchors_preset", 15)
      margin.set_property("anchor_right", 1.0)
      margin.set_property("anchor_bottom", 1.0)
      margin.set_property("grow_horizontal", 2)
      margin.set_property("grow_vertical", 2)

      # 3. Content Structure
      vbox = margin.add_vbox("Content", separation=20)
      vbox.add_label("Title", text="Settings", align="center", font_size=32)
      settings_section = vbox.add_vbox("Settings", separation=15)

      # 4. Component Rows
      row = settings_section.add_hbox("VolumeRow", separation=15)
      row.add_label("Label", text="Volume:", min_size=(150, 0), size_flags_h=0)
      row.add_progress_bar("Bar", value=75, size_flags_h=3, show_percentage=True)
      row.add_button("Reset", text="Reset", size_flags_h=4)

      # 5. Prefab Instances
      vbox.add_instance("MusicVolume", 
                         scene_path="res://A1UIScenes/UIComponents/SliderComponent.tscn",
                         scene_uid="uid://dbaix0lcy10v2")
    </example>
  </ui_creation_flow>

  <size_flags_reference>
    | Value | Behavior | Use For |
    |-------|----------|---------|
    | `0` | Fixed size | Labels (with `min_size`) |
    | `3` | Fill + Expand | Sliders, progress bars, text fields |
    | `4` | Shrink Center | Buttons, icons |
    
    <example>
      row = vbox.add_hbox("Row", separation=15)
      row.add_label("Label", text="Volume:", min_size=(150, 0), size_flags_h=0)  # Fixed
      row.add_progress_bar("Bar", size_flags_h=3)  # Expands
      row.add_button("Reset", text="Reset", size_flags_h=4)  # Centered
    </example>
  </size_flags_reference>

  <api_reference>
    <ui_builder>
      - `UIBuilder(scene_name, scene_uid=None)`
      - `create_control(name="Control", fullscreen=True)`
      - `save(output_path)`
    </ui_builder>
    <containers>
      - `add_margin_container(name, uniform=None, use_anchors=False, vertical_margin=None, horizontal_margin=None, script=None)`
      - `add_panel_container(name)`
      - `add_scroll_container(name, horizontal_scroll=0, vertical_scroll=2, follow_focus=True)`
      - `add_vbox(name, separation=None)`
      - `add_hbox(name, separation=None)`
    </containers>
    <elements>
      - `add_color_rect(name, color=(r,g,b,a), use_anchors=False)`
      - `add_label(name, text="", align="left", font_size=None, min_size=None, size_flags_h=None)`
      - `add_button(name, text="", size_flags_h=None)`
      - `add_checkbox(name, text="", size_flags_h=None, button_pressed=False)`
      - `add_progress_bar(name, value=0, size_flags_h=None, size_flags_v=None, size_flags_stretch_ratio=None, min_size=None, show_percentage=True)`
      - `add_instance(name, scene_path, scene_uid)` (scene_uid REQUIRED)
      - `add_separator(name, separation=None, style=None)`
    </elements>
    <utility>
      - `set_property(key, value)` (Chainable)
      - `get_relative_path_to(target_node)` (Calculates NodePath)
    </utility>
    
    <tab_container_support>
      <description>Inject this support logic before creating UI to utilize TabContainers.</description>
      <example>
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

        # Usage
        tabs = vbox.add_tab_container("Tabs")
        audio_tab = tabs.add_tab("Audio")
        audio_margin = audio_tab.add_margin_container("Margin", uniform=20, script=None)
        audio_vbox = audio_margin.add_vbox("Content", separation=15)
      </example>
    </tab_container_support>
  </api_reference>

  <prefabs_reference>
    <description>Location: `3d-practice/A1UIScenes/UIComponents/`</description>
    | Prefab | UID | Helper Script UID | Contents |
    |--------|-----|-------------------|----------|
    | `SliderComponent.tscn` | `uid://dbaix0lcy10v2` | `uid://jt7xkk4cigis` | Label + HSlider + SpinBox + Reset |
    | `ToggleComponent.tscn` | `uid://dpf5ovda3xlpv` | `uid://bi3yf7y5ir5ws` | Label + CheckBox + Reset |
    | `DropdownComponent.tscn` | `uid://0st2knyluaer` | `uid://djd3xoidagqxf` | Label + OptionButton + Reset |
    | `OptionComponent.tscn` | `uid://ddxph7didmq` | `uid://cq622dbolkfw0` | Label + Button (PopupMenu) + Reset |
  </prefabs_reference>

  <tscn_editor_tools>
    <description>Location: `KiroWorkingSpace/.kiro/scripts/ui_builder/tscn_editor_tools/`. Use `TscnEditor` to programmatically modify existing scenes in-place.</description>
    <core_files>
      - `parser.py`: Parses .tscn text format.
      - `node_tree.py`: Internal tree representation.
      - `pretty_printer.py`: Formats back to .tscn text.
      - `TscnReader.py`: Read-only API.
      - `TscnEditor.py`: Modification API.
      - `types.py`: Type definitions.
    </core_files>
    
    <rule>
      <description>Rely on TscnEditor's metadata preservation.</description>
      <rationale>It automatically maintains Node unique_ids, Scene UIDs, External resource UIDs, Property formatting (Color, Vector2, NodePath, ExtResource, PackedStringArray), and Hierarchy order.</rationale>
    </rule>

    <example>
      # Read Scene Structure
      from tscn_editor_tools import TscnReader
      reader = TscnReader("3d-practice/A1UIScenes/SettingsMenuV2.tscn")
      print(reader.print_tree_view())
      buttons = reader.find_nodes_by_type("Button")

      # Modify Scene Properties
      from tscn_editor_tools import TscnEditor, PropertyUpdate, Color
      editor = TscnEditor("3d-practice/A1UIScenes/SettingsMenuV2.tscn")
      
      # Single & Array Updates (Lists auto-convert to PackedStringArray)
      editor.update_property("Background_ColorRect", "color", Color(0.2, 0.2, 0.2, 1))
      editor.update_property("NumberFormat", "Items", ["23", "43", "08293"])
      
      # Batch Updates
      updates = [
          PropertyUpdate("BackButton_Button", "text", "返回"),
          PropertyUpdate("MasterVolume", "LabelText", "主音量"),
      ]
      editor.update_properties_batch(updates)
      
      # Add / Remove
      editor.add_node("NewButton", "Button", "MainVBox_VBoxContainer", properties={"text": "New Button"})
      editor.remove_node("OldButton")
      
      # Save (overwrites original by default)
      editor.save() 
    </example>
  </tscn_editor_tools>

  <technical_notes>
    - MarginContainerHelper default script is `res://addons/A1MyAddon/Helpers/MarginContainerHelper.cs`. Disable with `script=None`.
    - ProgressBar requires `show_percentage=True` to display the value text.
    - Separator requires a style resource (e.g., `style="res://path/to/style.tres"` or `style=None`).
  </technical_notes>

</godot_ui_builder_instructions>