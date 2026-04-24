---
trigger: manual
---
<godot_statechart_module_rules>
  <critical_rule>
    <rule>MUST explicitly read `AISpace/.windsurf/rules/Godot/SceneBuilders/GodotTscnBuilder_Context.md` before proceeding with any StateChart builder operations.</rule>
    <rule>MUST explicitly read `AISpace/.windsurf/rules/Godot/SceneBuilders/GodotTscnBuilder_Context.md` before proceeding with any StateChart builder operations.</rule>
    <rule>MUST explicitly read `AISpace/.windsurf/rules/Godot/SceneBuilders/GodotTscnBuilder_Context.md` before proceeding with any StateChart builder operations.</rule>
    <rule>Generator Python scripts MUST be saved to `AISpace/temp/` only. NEVER scatter them in `AISpace/scripts/` or project dirs. The generated `.tscn` output may go to `TetrisBackpack/Scenes/`, but the generator itself is disposable and lives in `AISpace/temp/`.</rule>
  </critical_rule>
  <layer_1_quick_start>
    <quick_reference>
      <item>Location: `AISpace/builder/modules/statechart.py`</item>
      <item>Dependency: MUST read `#GodotTscnBuilder_Context.md` and requires `godot_state_charts` addon.</item>
      <item>Initialization: `sc = StateChartModule(scene, parent=".")` followed by `sc.add_statechart("StateChart")`.</item>
      <item>Finalization: `sc.resolve_initial_states()` MUST be called before `scene.save()`.</item>
    </quick_reference>
    <decision_tree>
      <node condition="Need mutually exclusive child states">Use `add_compound_state()` (Why: Only one child is active at a time; requires `initial_state`).</node>
      <node condition="Need leaf states">Use `add_atomic_state()` (Why: End-point states that execute logic and cannot have children).</node>
      <node condition="Need simultaneous active states">Use `add_parallel_state()` (Why: Good for independent systems like Animation + Audio running together).</node>
      <node condition="Need MVC logic bound to a state">Use `add_component()` (Why: Attaches a C# script directly to the state node, activating/deactivating with state changes).</node>
    </decision_tree>
    <end_to_end_example>
      <code><![CDATA[
from builder.core import TscnBuilder
from builder.modules.statechart import StateChartModule

scene = TscnBuilder(root_name="Player", root_type="CharacterBody3D")
scene.initialize_root()

sc = StateChartModule(scene, parent=".")
sc.add_statechart("StateChart")

sc.add_compound_state("Root", parent="StateChart", initial_state="Idle")
sc.add_atomic_state("Idle", parent="Root")

sc.resolve_initial_states()
scene.save("Player.tscn")
      ]]></code>
    </end_to_end_example>
    <top_anti_patterns>
      <rule>
        <description>NEVER use node objects for `from_state` and `to_state` in transitions.</description>
        <rationale>The API expects exact string names to build internal NodePaths.</rationale>
        <example>
          <![CDATA[
# INCORRECT
sc.add_transition("ToWalk", from_state=idle_node, to_state=walk_node)

# CORRECT
sc.add_transition("ToWalk", from_state="Idle", to_state="Walking")
          ]]>
        </example>
      </rule>
      <rule>
        <description>NEVER save the scene without calling `resolve_initial_states()`.</description>
        <rationale>Initial states in `add_compound_state` are stored as string references. `resolve_initial_states()` converts them to engine-required NodePaths.</rationale>
        <example>
          <![CDATA[
# INCORRECT
sc.add_compound_state("Root", parent="StateChart", initial_state="Idle")
scene.save("Player.tscn") # CRASH/CORRUPTION

# CORRECT
sc.add_compound_state("Root", parent="StateChart", initial_state="Idle")
sc.resolve_initial_states()
scene.save("Player.tscn")
          ]]>
        </example>
      </rule>
    </top_anti_patterns>
  </layer_1_quick_start>

  <layer_2_detailed_guide>
    <api_reference>
      <method signature="StateChartModule(scene, parent)">Initializes the module. `scene` is the TscnBuilder instance.</method>
      <method signature="add_statechart(name)">Creates the root StateChart node. MUST be the first statechart call.</method>
      <method signature="add_compound_state(name, parent, initial_state)">Adds a state with mutually exclusive children. `initial_state` is a string.</method>
      <method signature="add_atomic_state(name, parent)">Adds a leaf state that executes logic.</method>
      <method signature="add_parallel_state(name, parent)">Adds a state where all child states are active simultaneously.</method>
      <method signature="add_transition(name, from_state, to_state, event=None, delay=0.0)">Adds state transition. Omit `event` for automatic transitions.</method>
      <method signature="add_expression_guard(name, parent, expression)">Adds GDScript conditional logic (`expression`) to a transition.</method>
      <method signature="add_component(name, parent, script_path, script_uid)">Attaches a C# script directly to an atomic or compound state.</method>
      <method signature="resolve_initial_states()">Iterates all CompoundStates and injects the resolved NodePath for `initial_state`.</method>
    </api_reference>
    <implementation_guide>
      <step>1. Initialize the `TscnBuilder` and add necessary non-state child nodes (e.g., AnimationPlayer).</step>
      <step>2. Initialize `StateChartModule` and call `add_statechart("Name")`.</step>
      <step>3. Build the state hierarchy explicitly specifying string parents (`add_compound_state`, `add_atomic_state`).</step>
      <step>4. Define string-based transitions with `add_transition()` and optional `add_expression_guard()`.</step>
      <step>5. Attach MVC logic using `add_component()` on specific states, and use `scene.assign_multiple_node_paths()` to bind UI/Scene nodes to C# Exports.</step>
      <step>6. MANDATORY: Call `sc.resolve_initial_states()` immediately before `scene.save()`.</step>
    </implementation_guide>
    <technical_specifications>
      <list>
        <item>StateChart UID: `uid://couw105c3bde4`</item>
        <item>CompoundState UID: `uid://jk2jm1g6q853`</item>
        <item>AtomicState UID: `uid://cytafq8i1y8qm`</item>
        <item>ParallelState UID: `uid://c1vp0ojjvaby1`</item>
        <item>Transition UID: `uid://cf1nsco3w0mf6`</item>
        <item>ExpressionGuard UID: `uid://b4xy2kqvvx8yx`</item>
      </list>
    </technical_specifications>
    <code_templates>
      <template name="Complete_Player_State_Machine">
        <code><![CDATA[
from builder.core import TscnBuilder
from builder.modules.statechart import StateChartModule

scene = TscnBuilder(root_name="Player", root_type="CharacterBody3D")
scene.initialize_root()
scene.add_node("AnimationPlayer", "AnimationPlayer", parent=".")
scene.add_node("AudioStreamPlayer", "AudioStreamPlayer", parent=".")

sc = StateChartModule(scene, parent=".")
sc.add_statechart("StateChart")

# States
sc.add_compound_state("Root", parent="StateChart", initial_state="Ground")
sc.add_compound_state("Ground", parent="Root", initial_state="Idle")
sc.add_atomic_state("Idle", parent="Ground")
sc.add_atomic_state("Walking", parent="Ground")
sc.add_atomic_state("Running", parent="Ground")

sc.add_compound_state("Air", parent="Root", initial_state="Falling")
sc.add_atomic_state("Jumping", parent="Air")
sc.add_atomic_state("Falling", parent="Air")

# Transitions
sc.add_transition("ToWalking", from_state="Idle", to_state="Walking", event="move_start")
sc.add_transition("ToIdle", from_state="Walking", to_state="Idle", event="move_stop")
sc.add_transition("ToJumping", from_state="Ground", to_state="Jumping", event="jump")

# Components & Bindings
sc.add_component(
    name="IdleComponent",
    parent="Idle",
    script_path="res://B1Scripts/Components/IdleComponent.cs",
    script_uid="uid://idle_component"
)
scene.assign_multiple_node_paths("IdleComponent", {
    "AnimationPlayer": "AnimationPlayer",
    "AudioPlayer": "AudioStreamPlayer"
})

sc.resolve_initial_states()
scene.save("Player.tscn")
        ]]></code>
      </template>
      <template name="StateChart_Component_MVC_Pattern_With_CSharp">
        <code><![CDATA[
# 1. PYTHON GENERATOR SCRIPT
from builder.core import TscnBuilder
from builder.modules.ui import UIModule
from builder.modules.statechart import StateChartModule

scene = TscnBuilder(root_name="SettingsMenu", root_type="Control")
ui = UIModule(scene)
ui.setup_fullscreen_control()
ui.add_vbox("MainVBox", parent=".", separation=10)
ui.add_button("ApplyButton", parent="MainVBox", text="Apply")
ui.add_button("CancelButton", parent="MainVBox", text="Cancel")

sc = StateChartModule(scene, parent=".")
sc.add_statechart("StateChart")
sc.add_compound_state("Root", parent="StateChart", initial_state="Idle")
sc.add_atomic_state("Idle", parent="Root")
sc.add_atomic_state("Editing", parent="Root")

sc.add_transition("ToEditing", from_state="Idle", to_state="Editing", event="start_edit")
sc.add_transition("ToIdle", from_state="Editing", to_state="Idle", event="cancel")

sc.add_component(
    name="SettingsController",
    parent="Editing",
    script_path="res://B1Scripts/UI/SettingsController.cs",
    script_uid="uid://settings_controller"
)

scene.assign_multiple_node_paths("SettingsController", {
    "ApplyButton": "ApplyButton",
    "CancelButton": "CancelButton"
})

sc.resolve_initial_states()
scene.save("SettingsMenu.tscn")

# =========================================================

// 2. C# COMPONENT (res://B1Scripts/UI/SettingsController.cs)
public partial class SettingsController : Node
{
    [Export] public NodePath ApplyButton { get; set; }
    [Export] public NodePath CancelButton { get; set; }
    
    private CompositeDisposable _disposables = new();
    
    public override void OnStateEnter()
    {
        GetNode<Button>(ApplyButton).OnPressedAsObservable()
            .Subscribe(_ => ApplySettings())
            .AddTo(_disposables);
            
        GetNode<Button>(CancelButton).OnPressedAsObservable()
            .Subscribe(_ => CancelSettings())
            .AddTo(_disposables);
    }
    
    public override void OnStateExit()
    {
        _disposables.Dispose();
        _disposables = new();
    }
}
        ]]></code>
      </template>
    </code_templates>
    <core_rules>
      <rule>
        <description>ALWAYS track and specify `parent` for EVERY state and transition explicitly using string names.</description>
        <rationale>Ensures the exact structural hierarchy dictated by the StateChart plugin is replicated in the raw `.tscn` file.</rationale>
      </rule>
    </core_rules>
  </layer_2_detailed_guide>

  <layer_3_advanced>
    <troubleshooting>
      <error symptom="StateChart fails to initialize or enter the first state. Engine throws null reference or missing NodePath error at runtime.">
        <cause>The generated `.tscn` file has string literal values instead of `NodePath` objects for the `initial_state` properties of `CompoundState` nodes.</cause>
        <fix>Ensure `sc.resolve_initial_states()` is called exactly once, right before `scene.save()`.</fix>
      </error>
      <error symptom="Transitions don't fire or throw 'State not found' errors.">
        <cause>The `from_state` or `to_state` parameters in `add_transition()` don't match actual state names, or node objects were passed instead of strings.</cause>
        <fix>ALWAYS use exact string names for `from_state` and `to_state`. Verify state names with `scene.generate_tree_view()`. Never pass node objects.</fix>
      </error>
      <error symptom="Component script fails to attach to state or throws 'Script not found' error.">
        <cause>Incorrect `script_path` or `script_uid` in `add_component()`, or the C# script file doesn't exist.</cause>
        <fix>Verify the script file exists at the specified path. For custom scripts, use `mcp_godot_get_uid()` to retrieve the correct UID.</fix>
      </error>
      <error symptom="Component can't access scene nodes via [Export] NodePath properties.">
        <cause>NodePath bindings were not set up using `scene.assign_node_path()` or `scene.assign_multiple_node_paths()`.</cause>
        <fix>After calling `sc.add_component()`, immediately call `scene.assign_multiple_node_paths(component_name, {...})` to bind required nodes.</fix>
      </error>
      <error symptom="Parallel states don't activate simultaneously or only one child is active.">
        <cause>Used `add_compound_state()` instead of `add_parallel_state()` for the parent state.</cause>
        <fix>Use `sc.add_parallel_state()` for states where all children should be active simultaneously (e.g., Animation + Audio systems).</fix>
      </error>
    </troubleshooting>

    <best_practices>
      <rule>
        <description>ALWAYS use the State-Based Component MVC pattern for binding Logic/UI to States.</description>
        <rationale>Attaching distinct C# scripts (`add_component`) to specific AtomicStates allows the logic to automatically activate (`OnStateEnter`) and garbage collect/deactivate (`OnStateExit`) naturally with the state machine's flow, ensuring pure Single Responsibility Principle.</rationale>
      </rule>
      <rule>
        <description>ALWAYS assign shared dependencies (e.g., `AnimationPlayer`) via `assign_multiple_node_paths` mapped against component `[Export]` properties.</description>
        <rationale>Keeps the components decoupled from scene-tree assumptions, allowing the TscnBuilder to guarantee exact NodePath injection.</rationale>
      </rule>
      <rule>
        <description>ALWAYS call `sc.resolve_initial_states()` as the last step before `scene.save()`.</description>
        <rationale>This is non-negotiable. Forgetting this step will result in corrupted `.tscn` files that crash Godot on load.</rationale>
      </rule>
      <rule>
        <description>Use `add_expression_guard()` for conditional transitions instead of complex event logic.</description>
        <rationale>Guards keep transition logic declarative and testable. Complex conditions should be evaluated in GDScript expressions rather than buried in C# event handlers.</rationale>
      </rule>
    </best_practices>

    <common_tasks_quick_index>
      <task name="Build Player State Machine">See `<code_templates>` → "Complete_Player_State_Machine" in layer_2_detailed_guide</task>
      <task name="Attach C# Component to State">See `<api_reference>` → `add_component()` method in layer_2_detailed_guide</task>
      <task name="Create StateChart with UI">See `<code_templates>` → "StateChart_Component_MVC_Pattern_With_CSharp" in layer_2_detailed_guide</task>
      <task name="Add Conditional Transitions">See `<api_reference>` → `add_expression_guard()` method in layer_2_detailed_guide</task>
      <task name="Debug State Hierarchy">Use `scene.generate_tree_view()` after building states, before `resolve_initial_states()`</task>
    </common_tasks_quick_index>
  </layer_3_advanced>
</godot_statechart_module_rules>