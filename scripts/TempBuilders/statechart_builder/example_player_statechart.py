"""
Example: Generate Player3D StateChart with Movement and Action states
Demonstrates the Power Switch pattern - components bound to states
"""

import sys
sys.path.append("C:/Godot/AISpace/.kiro/scripts/statechart_builder")
from godot_statechart_builder import StateChartBuilder

# Create builder for Player3D entity
builder = StateChartBuilder(
    entity_name="Player3D",
    entity_type="CharacterBody3D",
    entity_script_path="res://B1Scripts/Player3D.cs",
    entity_script_uid="uid://yhmx8fery0rh"
)

# Create entity with StateChart
statechart = builder.create_entity_with_statechart()

# Root ParallelState (allows Movement and Action to run simultaneously)
root = statechart.add_parallel_state("Root")

# === Movement Branch (Compound: Ground OR Fly) ===
movement = root.add_compound_state("Movement", initial_state="GroundMode")

# GroundMode state
ground = movement.add_atomic_state("GroundMode")
ground.add_component(
    "GroundMovementComponent",
    script_path="res://addons/A1MyAddon/CoreComponents/GroundMovementComponent.cs",
    script_uid="uid://qmkylfkevs6i"
)
# Transition: toggle_fly -> FlyMode
fly_mode_ref = None  # Will be set after creating FlyMode

# FlyMode state
fly = movement.add_atomic_state("FlyMode")
fly.add_component(
    "FlyMovementComponent",
    script_path="res://addons/A1MyAddon/CoreComponents/FlyMovementComponent.cs",
    script_uid="uid://jvlxnylo7us3"
)

# Add transitions (now that both states exist)
ground.add_transition("Transition", to_state=fly, event="toggle_fly")
fly.add_transition("Transition", to_state=ground, event="toggle_fly")

# === Action Branch (Compound: Normal OR Attacked OR Dead) ===
action = root.add_compound_state("Action", initial_state="Normal")

# Normal state (player can move and act)
normal = action.add_atomic_state("Normal")

# Attacked state (player is hit, input disabled)
attacked = action.add_atomic_state("Attacked")

# Dead state (game over)
dead = action.add_atomic_state("Dead")

# Transitions can be added later if needed:
# normal.add_transition("OnHit", to_state=attacked, event="on_hit")
# attacked.add_transition("OnRecover", to_state=normal, event="on_recover", delay=0.5)
# normal.add_transition("OnDeath", to_state=dead, event="on_death")

# Generate tree view for inspection
print("\n=== StateChart Structure ===")
print(builder.generate_tree_view())

# Save to file
output_path = "C:/Godot/3d-practice/Scenes/Player3D_Generated.tscn"
builder.save(output_path)

print("\n=== Usage ===")
print("1. Components are children of AtomicState nodes")
print("2. When state activates, components activate (SetProcess(true))")
print("3. When state deactivates, components deactivate (SetProcess(false))")
print("4. Send events: parent.SendStateEvent('toggle_fly')")
print("5. Connect state signals in editor: GroundMode.state_entered -> AnimationController.EnterGroundMode()")
