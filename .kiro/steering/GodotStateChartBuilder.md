---
inclusion: manual
---

# Godot StateChart Builder

<execution>
Write Python script using `.kiro/scripts/statechart_builder/godot_statechart_builder.py`, then execute to generate `.tscn` file.
</execution>

<power_switch_pattern>
StateChart controls component lifecycle via `SetProcess()`. Components are children of State nodes. When state activates, components activate. When state deactivates, components deactivate.

Call `AutoBindToParentState()` in component `_Ready()` to bind lifecycle to parent state.

**Benefits:** Zero state conditionals in components. No `if (_isGrounded)` checks.
</power_switch_pattern>

<workflow>
1. Define Dimensions: Use `ParallelState` for independent dimensions (Movement + Action)
2. Define Exclusions: Use `CompoundState` for mutually exclusive states (Ground OR Fly)
3. Attach Components: Add components to `AtomicState` nodes only
</workflow>

<api>
**StateChartBuilder:**
- `StateChartBuilder(entity_name, entity_type, entity_script_path, entity_script_uid)`
- `create_entity_with_statechart()` - Returns StateChart node
- `save(output_path)` - Write .tscn file

**States:**
- `add_parallel_state(name)` - All children active simultaneously
- `add_compound_state(name, initial_state=None)` - One child active (requires `initial_state`)
- `add_atomic_state(name)` - Leaf state (attach components here)

**Transitions:**
- `add_transition(name, to_state, event="", delay=0.0)` - State change trigger
- `add_expression_guard(name, expression)` - Condition check (GDScript expression)

**Components:**
- `add_component(name, script_path, script_uid=None)` - Attach to AtomicState

**Utility:**
- `get_relative_path_to(target_node)` - Calculate NodePath for transitions
</api>

<critical_rules>
**Component Placement:**
Components MUST be children of `AtomicState` only. Never attach to `CompoundState` or `ParallelState`.

**Initial State:**
`CompoundState` MUST specify `initial_state` parameter.

**Transition Targets:**
Use `source_state.get_relative_path_to(target_state)`. Never calculate manually.

**Event Names:**
Use snake_case (`toggle_fly`, `on_hit`, `on_death`). Events are StringName type.

**Automatic Transitions:**
Empty `event=""` triggers automatically when state enters or expression properties change.

**Delayed Transitions:**
If state exits before delay completes, transition cancels.
</critical_rules>

<node_types>
- **StateChart:** Root container. Routes events to active states.
- **ParallelState:** All children active simultaneously. Use for independent dimensions.
- **CompoundState:** One child active at a time. Use for mutual exclusion.
- **AtomicState:** Leaf node. Attach components here.
- **Transition:** State change wire. Triggered by events or automatically.
- **ExpressionGuard:** Condition check. Child of Transition.
</node_types>

<examples>

<example>
<description>Two-state toggle</description>
<code>
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
</code>
</example>

<example>
<description>Parallel dimensions</description>
<code>
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
</code>
</example>

<example>
<description>Transition with guard</description>
<code>
transition = ground.add_transition("ToFly", to_state=fly, event="toggle_fly")
transition.add_expression_guard("ManaCheck", "mana >= 10")

# In C#: stateChart.SetExpressionProperty("mana", currentMana);
</code>
</example>

<example>
<description>Automatic transition</description>
<code>
transition = idle.add_transition("AutoMove", to_state=moving, event="")
transition.add_expression_guard("VelocityCheck", "velocity > 0.1")

# In C#: stateChart.SetExpressionProperty("velocity", parent.Velocity.Length());
</code>
</example>

</examples>

<component_implementation>
**C# Component:**
```csharp
public partial class GroundMovementComponent : Node
{
    private Player3D _entity;
    
    public override void _Ready()
    {
        _entity = this.GetEntity<Player3D>();
        this.AutoBindToParentState(); // Bind lifecycle
        
        var input = _entity.GetRequiredComponentInChildren<BaseInputComponent>();
        input.OnMovementInput += HandleMovementInput;
    }
    
    public override void _PhysicsProcess(double delta)
    {
        // Only runs when parent state is active
        ApplyGravity(delta);
        ApplyMovement(delta);
    }
}
```

**Send Events:**
```csharp
parent.SendStateEvent("toggle_fly");
parent.SendStateEvent("on_hit");
```

**Connect Signals:**
In Godot editor:
- `GroundMode.state_entered` → `AnimationController.EnterGroundMode()`
- `FlyMode.state_entered` → `AnimationController.EnterFlyMode()`
</component_implementation>

<anti_patterns>
**NEVER place components outside AtomicState:**
```python
# WRONG
builder.root.add_component("Movement", "res://Movement.cs")

# RIGHT
ground_state.add_component("GroundMovement", "res://GroundMovement.cs")
```

**NEVER use if-statements for state checks:**
```csharp
// WRONG
if (_isGrounded) { ApplyGravity(); }

// RIGHT: StateChart controls lifecycle automatically
```

**NEVER reference states directly:**
```csharp
// WRONG
_groundState.SetActive(false);

// RIGHT
parent.SendStateEvent("toggle_fly");
```
</anti_patterns>
