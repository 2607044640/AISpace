"""
Example: Combined - Generate a scene with both UI and StateChart components
Demonstrates true composition: UI + StateChart in a single entity
"""

import sys
sys.path.append("../..")

from builder.core import TscnBuilder
from builder.modules.ui import UIModule
from builder.modules.statechart import StateChartModule

# Initialize Core Scene
scene = TscnBuilder(root_name="ItemEntity", root_type="Control")

# Attach UI Module
ui = UIModule(scene)
ui.setup_fullscreen_control()

# Build UI Structure
ui.add_texture_rect("ItemIcon", parent=".")
ui.add_label("ItemName", parent=".", text="Sword of Truth", align="center")

# Attach StateChart Module
sc = StateChartModule(scene, parent=".")
sc.add_statechart("StateChart")

# Build State Hierarchy
root_state = sc.add_compound_state("Root", parent="StateChart", initial_state="Idle")

sc.add_atomic_state("Idle", parent="Root")
sc.add_atomic_state("Dragging", parent="Root")
sc.add_atomic_state("Equipped", parent="Root")

# Transitions
sc.add_transition("ToDragging", from_state="Idle", to_state="Dragging", event="drag_start")
sc.add_transition("ToIdle", from_state="Dragging", to_state="Idle", event="drag_end")
sc.add_transition("ToEquipped", from_state="Idle", to_state="Equipped", event="equip")
sc.add_transition("ToIdle2", from_state="Equipped", to_state="Idle", event="unequip")

# Resolve initial states
sc.resolve_initial_states()

# Export
print(scene.generate_tree_view())
scene.save("c:/Godot/3d-practice/Scenes/ItemEntity.tscn")
