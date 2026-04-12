---
inclusion: manual
---

<layer_1_quick_start>
  <quick_reference>
    <ul>
      <li>**MUST** execute script via path: `.kiro/scripts/statechart_builder/godot_statechart_builder.py` to generate `.tscn` files.</li>
      <li>**ALWAYS** invoke `AutoBindToParentState()` within component `_Ready()` to bind C# lifecycle (`SetProcess()`) to parent state.</li>
      <li>**MUST** use `parent.SendStateEvent("event_name")` to trigger transitions.</li>
    </ul>
  </quick_reference>
  
  <decision_tree>
    <ul>
      <li>If creating independent gameplay dimensions (e.g., Movement + Action): **ALWAYS** use `ParallelState`. (Why: Allows simultaneous state execution without combinational explosion).</li>
      <li>If creating mutually exclusive states (e.g., Ground OR Fly): **ALWAYS** use `CompoundState`. (Why: Enforces strict active state singularity).</li>
      <li>If attaching component logic: **ALWAYS** use `AtomicState`. (Why: Ensures components only execute in absolute leaf states).</li>
    </ul>
  </decision_tree>
  
  <minimal_workflow>
    <ol>
      <li>Define Dimensions via `ParallelState`.</li>
      <li>Define Exclusions via `CompoundState`.</li>
      <li>Attach Components strictly to `AtomicState` nodes.</li>
    </ol>
  </minimal_workflow>
  
  <top_anti_patterns>
    <ul>
      <li>**PROHIBITED**: Attaching components to `CompoundState` or `ParallelState` nodes. (Why: Components will execute during undefined or overlapping state contexts).</li>
      <li>**PROHIBITED**: Using runtime if-statements for state checks (e.g., `if (_isGrounded)`). (Why: StateChart handles execution lifecycle natively; manual checks violate the Power Switch pattern).</li>
      <li>**PROHIBITED**: Referencing and mutating states directly (e.g., `_groundState.SetActive(false)`). (Why: Bypasses defined state machine transition logic and event streams).</li>
    </ul>
  </top_anti_patterns>
</layer_1_quick_start>

<layer_2_detailed_guide>
  <api_reference>
    <table>
      <tr><th>Class/Context</th><th>Method Signature</th><th>Description</th></tr>
      <tr><td>Builder</td><td>`StateChartBuilder(entity_name, entity_type, entity_script_path, entity_script_uid)`</td><td>Initializes the generation pipeline.</td></tr>
      <tr><td>Builder</td><td>`create_entity_with_statechart()`</td><td>Returns root StateChart node.</td></tr>
      <tr><td>Builder</td><td>`save(output_path)`</td><td>Writes the final `.tscn` file to disk.</td></tr>
      <tr><td>States</td><td>`add_parallel_state(name)`</td><td>Creates node where all children are active simultaneously.</td></tr>
      <tr><td>States</td><td>`add_compound_state(name, initial_state=None)`</td><td>Creates node where one child is active.</td></tr>
      <tr><td>States</td><td>`add_atomic_state(name)`</td><td>Creates leaf node for component attachment.</td></tr>
      <tr><td>Transitions</td><td>`add_transition(name, to_state, event="", delay=0.0)`</td><td>Defines state change trigger.</td></tr>
      <tr><td>Transitions</td><td>`add_expression_guard(name, expression)`</td><td>Adds GDScript expression check child.</td></tr>
      <tr><td>Components</td><td>`add_component(name, script_path, script_uid=None)`</td><td>Attaches script to `AtomicState`.</td></tr>
      <tr><td>Utility</td><td>`get_relative_path_to(target_node)`</td><td>Calculates NodePath for transitions.</td></tr>
    </table>
  </api_reference>

  <technical_specifications>
    <ul>
      <li>**Node Scene Tree Hierarchy:** `StateChart` (Root) -> `ParallelState` | `CompoundState` -> `AtomicState` (Leaf) -> `Transition` -> `ExpressionGuard`.</li>
      <li>**C# Component Acquisition:** Use `this.GetEntity<T>()` and `_entity.GetRequiredComponentInChildren<T>()`.</li>
      <li>**Event Properties:** `SetExpressionProperty("property_name", value)` injects data for `ExpressionGuard` evaluation.</li>
      <li>**Delay Behavior:** Delayed transitions are **ALWAYS** cancelled if the source state exits before the delay completes.</li>
    </ul>
  </technical_specifications>

  <core_rules>
    <rule>
      <description>**MUST** attach components to `AtomicState` nodes exclusively.</description>
      <rationale>Ensures strict leaf-level lifecycle control, preventing component logic from running in parent intermediate states.</rationale>
    </rule>
    <rule>
      <description>**ALWAYS** specify the `initial_state` parameter when creating a `CompoundState`.</description>
      <rationale>A `CompoundState` guarantees exactly one active child; failing to define the default breaks the initialization sequence.</rationale>
    </rule>
    <rule>
      <description>**MUST** use `source_state.get_relative_path_to(target_state)` for transition targets.</description>
      <rationale>Manual pathing string calculations are brittle and will break upon scene tree restructuring.</rationale>
    </rule>
    <rule>
      <description>**MUST** format event names using `snake_case` strictly cast as `StringName` type.</description>
      <rationale>Ensures event routing consistency and optimized string comparison across Godot's C++/C# boundaries.</rationale>
    </rule>
    <rule>
      <description>**ALWAYS** use an empty string `event=""` for automatic transitions triggered by property changes.</description>
      <rationale>Binds the transition evaluation to state entry or `ExpressionGuard` property updates rather than explicit event emissions.</rationale>
    </rule>
  </core_rules>
</layer_2_detailed_guide>

<layer_3_advanced>
  <troubleshooting>
    <error symptom="Components fail to pause or resume execution upon state changes.">
      <cause>Component script is not integrated with the StateChart lifecycle.</cause>
      <fix>**MUST** add `this.AutoBindToParentState();` inside the component's `public override void _Ready()` method.</fix>
    </error>
    <error symptom="Transition path resolution fails during `.tscn` build or runtime.">
      <cause>Node paths were written manually or target node is out of scope.</cause>
      <fix>**ALWAYS** assign `to_state` via exact object reference in Python, delegating resolution to `get_relative_path_to(target_state)`.</fix>
    </error>
  </troubleshooting>

  <code_examples>
    <example>
      <description>Two-State Toggle (Ground/Fly)</description>
      <code>
```python
builder = StateChartBuilder("Player3D", "CharacterBody3D", 
                           entity_script_path="res://B1Scripts/Player3D.cs")
statechart = builder.create_entity_with_statechart()

root = statechart.add_compound_state("Root", initial_state="Ground")

ground = root.add_atomic_state("Ground")
ground.add_component("GroundMovement", "res://Components/GroundMovement.cs")

fly = root.add_atomic_state("Fly")
fly.add_component("FlyMovement", "res://Components/FlyMovement.cs")

ground.add_transition("ToFly", to_state=fly, event="toggle_fly")
fly.add_transition("ToGround", to_state=ground, event="toggle_fly")

builder.save("res://Scenes/Player.tscn")
```
      </code>
    </example>

    <example>
      <description>Parallel Dimensions (Movement + Action)</description>
      <code>
```python
root = statechart.add_parallel_state("Root")

# Movement dimension
movement = root.add_compound_state("Movement", initial_state="Ground")
ground = movement.add_atomic_state("Ground")
ground.add_component("GroundMovement", "res://Components/GroundMovement.cs")

fly = movement.add_atomic_state("Fly")
fly.add_component("FlyMovement", "res://Components/FlyMovement.cs")

ground.add_transition("ToFly", to_state=fly, event="toggle_fly")
fly.add_transition("ToGround", to_state=ground, event="toggle_fly")

# Action dimension
action = root.add_compound_state("Action", initial_state="Normal")
normal = action.add_atomic_state("Normal")
attacked = action.add_atomic_state("Attacked")

normal.add_transition("OnHit", to_state=attacked, event="on_hit")
attacked.add_transition("OnRecover", to_state=normal, event="on_recover", delay=0.5)
```
      </code>
    </example>

    <example>
      <description>Transition with Expression Guard</description>
      <code>
```python
transition = ground.add_transition("ToFly", to_state=fly, event="toggle_fly")
transition.add_expression_guard("ManaCheck", "mana >= 10")

# In C#: stateChart.SetExpressionProperty("mana", currentMana);
```
      </code>
    </example>

    <example>
      <description>Automatic Transition (No Event)</description>
      <code>
```python
transition = idle.add_transition("AutoMove", to_state=moving, event="")
transition.add_expression_guard("VelocityCheck", "velocity > 0.1")

# In C#: stateChart.SetExpressionProperty("velocity", parent.Velocity.Length());
```
      </code>
    </example>
  </code_examples>

  <component_implementation>
    <template>
      <description>Power Switch Component Template</description>
      <code>
```csharp
public partial class GroundMovementComponent : Node
{
    private Player3D _entity;

    public override void _Ready()
    {
        _entity = this.GetEntity<Player3D>();
        this.AutoBindToParentState(); // Bind lifecycle to parent state
        
        var input = _entity.GetRequiredComponentInChildren<BaseInputComponent>();
        input.OnMovementInput += HandleMovementInput;
    }

    public override void _PhysicsProcess(double delta)
    {
        // Only runs when parent state is active
        // NO manual state checks needed (no if (_isGrounded))
        ApplyGravity(delta);
        ApplyMovement(delta);
    }
    
    private void HandleMovementInput(Vector2 input)
    {
        // Component logic here
    }
}
```
      </code>
    </template>

    <event_sending>
      <description>Sending State Events from Components</description>
      <code>
```csharp
// Send event to trigger transition
parent.SendStateEvent("toggle_fly");
parent.SendStateEvent("on_hit");
parent.SendStateEvent("on_recover");
```
      </code>
    </event_sending>

    <signal_connection>
      <description>Connect State Signals in Godot Editor</description>
      <instructions>
        - `GroundMode.state_entered` → `AnimationController.EnterGroundMode()`
        - `FlyMode.state_entered` → `AnimationController.EnterFlyMode()`
        - `Attacked.state_entered` → `VisualEffects.PlayHitEffect()`
      </instructions>
    </signal_connection>
  </component_implementation>

  <anti_pattern_examples>
    <anti_pattern>
      <description>WRONG: Placing components outside AtomicState</description>
      <wrong>
```python
# WRONG
builder.root.add_component("Movement", "res://Movement.cs")
```
      </wrong>
      <correct>
```python
# RIGHT
ground_state.add_component("GroundMovement", "res://GroundMovement.cs")
```
      </correct>
    </anti_pattern>

    <anti_pattern>
      <description>WRONG: Using if-statements for state checks</description>
      <wrong>
```csharp
// WRONG
public override void _PhysicsProcess(double delta)
{
    if (_isGrounded) { ApplyGravity(); }
    if (_isFly) { ApplyFlyPhysics(); }
}
```
      </wrong>
      <correct>
```csharp
// RIGHT: StateChart controls lifecycle automatically
public override void _PhysicsProcess(double delta)
{
    ApplyGravity(); // Only runs when parent state is active
}
```
      </correct>
    </anti_pattern>

    <anti_pattern>
      <description>WRONG: Referencing states directly</description>
      <wrong>
```csharp
// WRONG
_groundState.SetActive(false);
_flyState.SetActive(true);
```
      </wrong>
      <correct>
```csharp
// RIGHT
parent.SendStateEvent("toggle_fly");
```
      </correct>
    </anti_pattern>
  </anti_pattern_examples>

  <implementation_anchors>
    <ul>
      <li>**Power Switch Component Template:**
        <ul>
          <li>`public override void _Ready()` **MUST** contain `this.AutoBindToParentState();`.</li>
          <li>Processing loops (`_PhysicsProcess`, `_Process`) **MUST** omit manual state checks. Execution is guaranteed isolated.</li>
        </ul>
      </li>
      <li>**Guard Injection Anchor:** To satisfy `add_expression_guard("VelocityCheck", "velocity > 0.1")`, C# **MUST** push data via `stateChart.SetExpressionProperty("velocity", parent.Velocity.Length());`.</li>
    </ul>
  </implementation_anchors>

  <best_practices>
    <ul>
      <li>**Power Switch Pattern:** Rely entirely on Godot Node enablement/disablement for state execution. Remove all internal condition tracking.</li>
      <li>**Editor Signal Mapping:** **ALWAYS** map `state_entered` signals to visual controllers (e.g., `AnimationController.EnterGroundMode()`) via the Godot Editor UI rather than hardcoding visual state bindings inside logic components.</li>
    </ul>
  </best_practices>
</layer_3_advanced>