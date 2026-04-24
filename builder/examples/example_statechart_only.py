"""
Example: StateChart Only - Generate a scene with only StateChart components
"""

import sys
sys.path.append("../..")

from builder.core import TscnBuilder
from builder.modules.statechart import StateChartModule

# Initialize Core Scene
scene = TscnBuilder(root_name="Player", root_type="CharacterBody3D")
scene.initialize_root()

# Attach StateChart Module
sc = StateChartModule(scene, parent=".")
sc.add_statechart("StateChart")

# Build State Hierarchy
root_state = sc.add_compound_state("Root", parent="StateChart", initial_state="Idle")

# Ground States
sc.add_atomic_state("Idle", parent="Root")
sc.add_atomic_state("Walking", parent="Root")
sc.add_atomic_state("Running", parent="Root")

# Transitions
sc.add_transition("ToWalking", from_state="Idle", to_state="Walking", event="move_start")
sc.add_transition("ToIdle", from_state="Walking", to_state="Idle", event="move_stop")
sc.add_transition("ToRunning", from_state="Walking", to_state="Running", event="sprint_start")
sc.add_transition("ToWalking2", from_state="Running", to_state="Walking", event="sprint_stop")

# Resolve initial states
sc.resolve_initial_states()

# Export
print(scene.generate_tree_view())
scene.save("c:/Godot/TetrisBackpack/Scenes/PlayerStateChart.tscn")
