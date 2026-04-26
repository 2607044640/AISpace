---
trigger: manual
---
```xml
<critical_rule>
  <rule>Generator Python scripts MUST be saved to `AISpace/temp/` only. NEVER scatter them in `AISpace/scripts/` or project dirs. The generated `.tscn` output may go to `TetrisBackpack/Scenes/`, but the generator itself is disposable and lives in `AISpace/temp/`.</rule>
</critical_rule>
<layer_1_quick_start>
  <quick_reference>
    - **Core Builder:** `builder.core.TscnBuilder`
    - **UI Module:** `builder.modules.ui.UIModule`
    - **StateChart Module:** `builder.modules.statechart.StateChartModule`
    - **Gold Standard Scene:** `res://A1UIScenes/SettingsMenuV2_Fixed.tscn`
    - **UI Prefabs Directory:** `res://A1UIScenes/UIComponents/`
  </quick_reference>

  <decision_tree>
    - If connecting UI events to code:
      - (Why: Maintain reactivity and avoid broken string references) Use Pure C# Events with R3 reactive extensions. NEVER use Godot native signals.
    - If binding UI nodes to C# `[Export]` properties:
      - (Why: Prevent fragile manual pathing) Use `scene.assign_node_path()` or `scene.assign_multiple_node_paths()`.
    - If adding a standard UI component (Dropdown, Slider, Toggle):
      - (Why: Maintain visual consistency and utilize pre-configured behaviors) Use `ui.add_instance()` pointing to existing `res://A1UIScenes/UIComponents/` prefabs.
    - If creating a main UI panel:
      - (Why: Standardized screen resolution handling) ALWAYS center the layout using `CenterContainer`, anchors (`anchors_preset=8`), or centered fullscreen margins.
  </decision_tree>

  <end_to_end_example>
    <![CDATA[
from builder.core import TscnBuilder
from builder.modules.ui import UIModule

# 1. Create scene
scene = TscnBuilder(root_name="SettingsUI", root_type="Control")

# 2. Build UI (standard nodes - use descriptive names)
ui = UIModule(scene)
ui.setup_fullscreen_control()
ui.add_button("ApplyButton", parent=".", text="Apply")
ui.add_progress_bar("VolumeSlider", parent=".", value=80)

# 3. Add C# Controller (custom script - use class name directly)
controller_res_id = scene.add_ext_resource(
    resource_type="Script", 
    path="res://B1Scripts/UI/SettingsController.cs", 
    uid="uid://controller_uid"
)
scene.add_node("SettingsController", "Node", parent=".",
              script=f'ExtResource("{controller_res_id}")')

# 4. Bind UI to Controller [Export] properties
scene.assign_multiple_node_paths("SettingsController", {
    "ApplyButton": "ApplyButton",
    "VolumeSlider": "VolumeSlider"
})

# 5. Save
scene.save("SettingsUI.tscn")
    ]]>
  </end_to_end_example>

  <top_anti_patterns>
    - **Manual NodePath Calculation in C#:** Using `new NodePath("../Node")` is highly fragile and breaks upon scene hierarchy changes. (Why: TscnBuilder automates accurate path calculation via `assign_node_path`).
    - **Native Godot Signals in `.tscn`:** Using `[connection signal="pressed" ...]` embeds logic inside the scene file. (Why: Pure C# R3 Rx keeps event logic entirely within code and compiler-checked).
    - **Raw Control Node Instantiation:** Using `scene.add_node("MySlider", "HSlider", ...)` bypasses the project's visual themes and standard interactions. (Why: Project standard dictates using the `SliderComponent.tscn` prefab).
  </top_anti_patterns>
</layer_1_quick_start>

<layer_2_detailed_guide>
  <api_reference>
    - `TscnBuilder(root_name, root_type, scene_uid=None)`: Initializes core scene.
    - `scene.initialize_root(**properties)`: Assigns properties to the root node (e.g., `layout_mode=3`).
    - `scene.add_node(name, node_type, parent, **properties)`: Injects a generic node. `parent="."` targets the root. **Naming convention:** For nodes with custom C# scripts, use the script class name directly (e.g., "BackpackGridComponent", "SettingsController"). For standard UI nodes (Label, VBox, ColorRect, Button, etc.), use descriptive names.
    - `scene.get_node(name)`: Retrieves a node reference from the internal registry using the full node name.
    - `scene.add_ext_resource(resource_type, path, uid, resource_id=None)`: Registers external dependencies, deduplicating automatically. Returns resource ID.
    - `scene.add_sub_resource(resource_type, resource_id, **properties)`: Registers inline resources (e.g., Shapes, Materials).
    - `scene.assign_node_path(target_node_name, property_name, path_to_node_name)`: Calculates relative NodePath and injects as an `[Export]` property assignment. Use full node names.
    - `scene.assign_multiple_node_paths(target_node_name, dict_mapping)`: Batch processes NodePath assignments.
    - `scene.generate_tree_view()`: Returns ASCII tree representation for CLI inspection/validation.
    - `scene.save(filepath)`: Writes the formatted `.tscn` file to disk.
    - `UIModule(scene)`: Wraps `TscnBuilder` to provide control-specific abstractions.
    - `ui.setup_fullscreen_control()`: Configures root or targeted parent to occupy the full viewport.
    - `ui.add_instance(name, parent, scene_path, scene_uid)`: Instantiates a prefab as a node.
  </api_reference>

  <implementation_guide>
    - **Step 1:** Initialize `TscnBuilder` and bind required sub-modules (e.g., `UIModule`).
    - **Step 2:** Construct the physical hierarchy top-down. Explicitly declare `parent="Target"` for every node. Ensure UI roots are properly centered or anchored.
    - **Step 3:** Inject any backing C# logic controllers as nodes using `add_ext_resource` and `add_node`.
    - **Step 4:** Perform dependency injection by mapping UI nodes to C# `[Export]` properties using `assign_multiple_node_paths()`.
    - **Step 5:** Execute `scene.save()` to write the output.
    - **Step 6 (MANDATORY):** Test the generated scene using Godot MCP tools:
      - Run: `mcp_godot_run_project(projectPath="c:/Godot/TetrisBackpack", scene="Scenes/YourScene.tscn")`
      - Check output: `mcp_godot_get_debug_output()`
      - Stop: `mcp_godot_stop_project()`
      - Verify NO errors about "未设置" (not set) or NullReferenceException for [Export] properties
      - If errors found, fix the GENERATOR SCRIPT (not the .tscn file manually)
    - **Step 7 (CRITICAL):** If regenerating an existing scene while Godot editor is open:
      - **MUST manually reload the scene in Godot!** Click the "Reload" button (circular arrow) in the scene tab
      - Godot does NOT auto-reload modified .tscn files from disk
      - Without reloading, you'll test the OLD cached version and see OLD errors
      - This is the #1 cause of "but I fixed it and it still doesn't work" confusion
  </implementation_guide>

  <technical_specifications>
    - **Framework Location:** `AISpace/builder/`
    - **Standard Prefab Types:** - `DropdownComponent.tscn`
      - `SliderComponent.tscn`
      - `ToggleComponent.tscn`
      - `OptionComponent.tscn`
      - `ThemeSwitcherComponent.tscn`
    - **Standard Layout Magic Numbers:**
      - Fullscreen Anchors Preset: `15` (`layout_mode=3` / `1`)
      - Centered Anchors Preset: `8`
  </technical_specifications>

  <code_templates>
    <template name="CSharp Rx Event Binding">
      <code><![CDATA[
[Export] public NodePath ApplyButton { get; set; }
[Export] public NodePath VolumeSlider { get; set; }

public override void _Ready()
{
    // Pure C# events with R3 reactive extensions
    GetNode<Button>(ApplyButton).OnPressedAsObservable()
        .ThrottleFirst(TimeSpan.FromMilliseconds(500))
        .Subscribe(_ => ApplySettings())
        .AddTo(_disposables);
    
    GetNode<ProgressBar>(VolumeSlider).OnValueChangedAsObservable()
        .Debounce(TimeSpan.FromMilliseconds(100))
        .Subscribe(volume => UpdateVolume(volume))
        .AddTo(_disposables);
}
      ]]></code>
    </template>

    <template name="UI Prefab Instantiation">
      <code><![CDATA[
# ALWAYS use mcp_godot_get_uid to get correct UID
uid_result = mcp_godot_get_uid(
    projectPath="c:/Godot/TetrisBackpack",
    filePath="A1UIScenes/UIComponents/DropdownComponent.tscn"
)

ui.add_instance(
    name="DisplayMode",
    parent="MainVBox",
    scene_path="res://A1UIScenes/UIComponents/DropdownComponent.tscn",
    scene_uid=uid_result["uid"]
)
      ]]></code>
    </template>
  </code_templates>

  <core_rules>
    <rule>
      <description>**ALWAYS use Scene Unique Names (%) for all NodePath references. NEVER use relative paths.**</description>
      <rationale>Relative paths like "../../../NodeName" are extremely fragile and error-prone for AI generation. They break when hierarchy changes. Humans can click-select in the editor, but AI must calculate paths manually, leading to frequent errors. Scene Unique Names are hierarchy-independent, human-readable, and AI-friendly.</rationale>
      <example>
        # ❌ INCORRECT - Relative paths (fragile, AI-error-prone)
        scene.add_node("Controller", "Node", parent=".", script=ExtResource("script"))
        controller_node = scene.get_node("Controller")
        button_node = scene.get_node("ApplyButton")
        relative_path = controller_node.get_relative_path_to(button_node)  # "../MainVBox/ApplyButton"
        controller_node.set_property("ApplyButton", f'NodePath("{relative_path}")')
        
        # ✅ CORRECT - Scene Unique Names (robust, AI-friendly)
        scene.assign_node_path("Controller", "ApplyButton", "ApplyButton")
        # Automatically generates: ApplyButton = NodePath("%ApplyButton")
        # The target node is auto-marked as unique_name_in_owner=true
      </example>
      <csharp_code_pattern>
        # C# code should also use % syntax for manual GetNode calls
        
        # ❌ INCORRECT - Relative paths in C#
        var button = GetNodeOrNull<Button>("../MainVBox/ApplyButton");
        var parent = GetNodeOrNull<Control>("..");
        var stateChart = GetParent()?.GetNodeOrNull<Node>("StateChart");
        
        # ✅ CORRECT - Scene Unique Names in C#
        var button = GetNodeOrNull<Button>("%ApplyButton");
        var backpackPanel = GetNodeOrNull<Control>("%BackpackPanel");
        var stateChart = GetNodeOrNull<Node>("%StateChart");
        
        # Benefits:
        # - Code is self-documenting (you know exactly which node you're getting)
        # - Refactoring-safe (moving nodes doesn't break code)
        # - No need to count "../" levels
      </csharp_code_pattern>
    </rule>
    
    <rule>
      <description>NEVER generate Godot native signal connections (`[connection]` blocks) in `.tscn` files.</description>
      <rationale>Native `.tscn` signal mappings are extremely prone to breakage upon refactors. All logic must reside in code using C# R3 Rx streams.</rationale>
      <example>
        # INCORRECT
        [connection signal="pressed" from="ApplyButton" to="." method="_on_apply_button_pressed"]

        # CORRECT
        GetNode<Button>(ApplyButton).OnPressedAsObservable().Subscribe(_ => ApplySettings()).AddTo(_disposables);
      </example>
    </rule>

    <rule>
      <description>ALWAYS use `assign_node_path()` for injecting node references into C# Controller `[Export]` properties.</description>
      <rationale>Automating NodePath injection ensures accurate relative path math and auto-updates if the hierarchy structure changes.</rationale>
      <example>
        # INCORRECT
        # In C#: [Export] public NodePath ApplyButton { get; set; } = new NodePath("../MainMargin/MainVBox/ButtonRow/ApplyButton");

        # CORRECT
        # In Python Builder: 
        scene.assign_node_path(target_node_name="SettingsController", property_name="ApplyButton", path_to_node_name="ApplyButton")
      </example>
    </rule>

    <rule>
      <description>ALWAYS utilize standard UI prefabs from `res://A1UIScenes/UIComponents/` when applicable. NEVER build raw Control nodes (OptionButton, HSlider, etc.) if a prefab exists.</description>
      <rationale>Ensures UI component consistency, theme adoption, and centralized visual updates.</rationale>
      <example>
        # INCORRECT
        scene.add_node("OptionList", "OptionButton", parent="Layout")

        # CORRECT
        ui.add_instance("OptionList", parent="Layout", scene_path="res://A1UIScenes/UIComponents/DropdownComponent.tscn", scene_uid="...")
      </example>
    </rule>

    <rule>
      <description>ALWAYS center main UI panels on the screen.</description>
      <rationale>Ensures consistent UX across varying resolutions. Must be accomplished via `CenterContainer`, `anchors_preset=8`, or fullscreen configurations with generous margins.</rationale>
      <example>
        # CORRECT (Anchored Approach)
        scene.add_node("MainPanel", "PanelContainer", parent=".",
              layout_mode=1, anchors_preset=8, offset_left=-300, offset_top=-200, offset_right=300, offset_bottom=200)
      </example>
    </rule>

    <rule>
      <description>ALWAYS verify hierarchy, layout, and theme application against the gold standard: `res://A1UIScenes/SettingsMenuV2_Fixed.tscn`.</description>
      <rationale>The standard scene serves as the verified baseline for all layout conventions.</rationale>
      <example>
        # INCORRECT
        Assuming arbitrary padding/margins without cross-referencing SettingsMenuV2_Fixed.tscn.
      </example>
    </rule>
  </core_rules>
</layer_2_detailed_guide>

<layer_3_advanced>
  <troubleshooting>
    <error symptom="External resources (scripts, scenes) fail to load with 'Resource not found' errors.">
      <cause>Incorrect UID or path provided to `add_ext_resource()`, or the resource file doesn't exist at the specified location.</cause>
      <fix>For scene instances, ALWAYS use `mcp_godot_get_uid()` to retrieve the correct UID. Verify the file path is correct and uses `res://` protocol. Check that the file actually exists in the project.</fix>
    </error>
  </troubleshooting>

  <best_practices>
    - **Composition over Inheritance:** Utilize sub-modules (`UIModule`, `StateChartModule`) attached to the `TscnBuilder` rather than monolithic builder scripts.
    - **Explicit Parent References:** Never chain node creation methods blindly. Always dictate the exact parent using `parent="NodeName"` to ensure the scene tree reflects structural intent.
    - **Node Registry Cross-Referencing:** Utilize the internal node registry. Since all nodes are tracked by name, path assignments and hierarchical lookups are inherently stable.
    - **Validate Before Save:** Always call `scene.generate_tree_view()` before `scene.save()` to visually inspect the hierarchy and catch structural errors early.
    - **Node Naming Convention (MANDATORY):**
      - **For nodes with custom C# scripts:** Use the script class name directly as the node name (e.g., `scene.add_node("BackpackGridComponent", "Node", ...)`, `scene.add_node("SettingsController", "Node", ...)`). This makes the node type immediately visible in the scene tree without needing to hover or check properties.
      - **DO NOT use abbreviated names:** Never use shortened names like "LogicGrid", "Controller", "Draggable", etc. Always use the full class name.
      - **For standard UI nodes:** Use descriptive names without class suffixes (e.g., "ApplyButton", "MainVBox", "Background") since these nodes have recognizable icons in the Godot editor (Label, VBox, ColorRect, Button, StateChart, etc.).
      - **Rationale:** Full class names in the scene tree provide immediate context about what each node does, eliminating the need to inspect properties or hover for tooltips. This significantly improves scene readability and maintenance.
  </best_practices>

  <common_generator_script_errors>
    <error_pattern name="Forgetting to bind [Export] properties for UI component nodes">
      <symptom>C# script reports "[ComponentName]: [PropertyName] 未设置！" during _Ready()</symptom>
      <cause>Generator script only binds NodePaths for Controller nodes, but forgets that UI component nodes (like BackpackGridUIComponent) also have [Export] properties that need binding.</cause>
      <example>
        # INCORRECT - Only binding Controller
        scene.add_node("BackpackPanel", "Control", parent=".", script=ExtResource("backpack_ui_script"))
        scene.add_node("BackpackGridComponent", "Node", parent="BackpackPanel", script=ExtResource("logic_grid_script"))
        scene.add_node("BackpackInteractionController", "Node", parent="BackpackPanel", script=ExtResource("controller_script"))
        
        # Only binding BackpackInteractionController, forgetting BackpackPanel!
        scene.assign_multiple_node_paths("BackpackInteractionController", {
            "LogicGrid": "BackpackGridComponent",
            "ViewGrid": "BackpackPanel"
        })
        
        # CORRECT - Bind ALL nodes with [Export] properties
        scene.assign_node_path("BackpackPanel", "LogicGrid", "BackpackGridComponent")  # Don't forget this!
        scene.assign_multiple_node_paths("BackpackInteractionController", {
            "LogicGrid": "BackpackGridComponent",
            "ViewGrid": "BackpackPanel"
        })
      </example>
      <prevention>
        1. List ALL nodes that have C# scripts attached
        2. For EACH script, check for [Export] properties
        3. For EACH [Export] property, call assign_node_path()
        4. Test with mcp_godot_run_project() to verify NO "未设置" errors
      </prevention>
      <date_discovered>2026-04-15</date_discovered>
    </error_pattern>
    
    <error_pattern name="Calling assign_node_path() before creating target nodes">
      <symptom>Generated .tscn file fails to load in Godot with 'Invalid NodePath' errors, or Python script crashes with KeyError</symptom>
      <cause>Trying to bind NodePaths before the target nodes exist in the scene registry.</cause>
      <example>
        # INCORRECT - Binding before nodes exist
        scene.assign_node_path("Controller", "ApplyButton", "ApplyButton")  # ApplyButton doesn't exist yet!
        ui.add_button("ApplyButton", parent="MainVBox", text="Apply")
        
        # CORRECT - Create nodes first, then bind
        ui.add_button("ApplyButton", parent="MainVBox", text="Apply")
        scene.assign_node_path("Controller", "ApplyButton", "ApplyButton")
      </example>
      <prevention>
        1. Create ALL nodes first using add_node() or ui.add_*()
        2. THEN do all NodePath bindings at the end
        3. Use scene.generate_tree_view() to verify all nodes exist before binding
      </prevention>
      <date_discovered>2026-04-15</date_discovered>
    </error_pattern>
    
    <error_pattern name="Wrong node name in assign_node_path() parameters">
      <symptom>C# script throws NullReferenceException when accessing nodes via [Export] properties, or reports "未设置" errors</symptom>
      <cause>Typo in node name, or using wrong parameter (target_node_name vs path_to_node_name confused).</cause>
      <example>
        # INCORRECT - Typo in node name
        scene.add_node("ApplyButton", "Button", parent="MainVBox")
        scene.assign_node_path("SettingsController", "ApplyButton", "ApplyButon")  # Typo!
        
        # INCORRECT - Parameters reversed
        scene.assign_node_path("ApplyButton", "SettingsController", "ApplyButton")  # Wrong order!
        
        # CORRECT
        scene.assign_node_path("SettingsController", "ApplyButton", "ApplyButton")
      </example>
      <prevention>
        1. Use scene.generate_tree_view() to see exact node names
        2. Remember: assign_node_path(WHO_HAS_EXPORT, PROPERTY_NAME, WHERE_TO_POINT)
        3. Use full script class names for custom script nodes (e.g., "SettingsController", not "Controller")
        4. Test with mcp_godot_run_project() to catch errors early
      </prevention>
      <date_discovered>2026-04-15</date_discovered>
    </error_pattern>
    
    <error_pattern name="Omitting or wrong parent parameter in add_node()">
      <symptom>Scene hierarchy is incorrect - nodes appear in wrong parent or are orphaned</symptom>
      <cause>The `parent` parameter was omitted or specified incorrectly in `add_node()` calls.</cause>
      <example>
        # INCORRECT - Omitting parent
        scene.add_node("ApplyButton", "Button", text="Apply")  # Where does this go?
        
        # INCORRECT - Wrong parent name
        scene.add_node("ApplyButton", "Button", parent="MainBox", text="Apply")  # Typo: should be MainVBox
        
        # CORRECT
        scene.add_node("ApplyButton", "Button", parent="MainVBox", text="Apply")
        scene.add_node("CancelButton", "Button", parent=".", text="Cancel")  # Root child
      </example>
      <prevention>
        1. ALWAYS explicitly specify parent="NodeName" for every node
        2. Use parent="." for root-level children
        3. Verify hierarchy with scene.generate_tree_view() before save()
      </prevention>
      <date_discovered>2026-04-15</date_discovered>
    </error_pattern>
  </common_generator_script_errors>

  <common_tasks_quick_index>
    <task name="Generate Settings UI">See `<end_to_end_example>` in layer_1_quick_start</task>
    <task name="Bind UI to C# Controller">See `<code_templates>` → "CSharp Rx Event Binding" in layer_2_detailed_guide</task>
    <task name="Use UI Prefabs">See `<code_templates>` → "UI Prefab Instantiation" in layer_2_detailed_guide</task>
    <task name="Debug Scene Hierarchy">Use `scene.generate_tree_view()` method (see api_reference)</task>
    <task name="Center UI Layout">See `<core_rules>` → Rule 4 in layer_2_detailed_guide</task>
    <task name="Fix '[Export] property 未设置' errors">See `<common_generator_script_errors>` in layer_3_advanced</task>
  </common_tasks_quick_index>
</layer_3_advanced>
```