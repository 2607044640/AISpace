"""
Test 10: StateChart Component with C# Export Binding
Tests the complete MVC workflow: UI + StateChart + Component + Automatic Binding
"""

import sys
sys.path.append("../..")

from builder.core import TscnBuilder
from builder.modules.ui import UIModule
from builder.modules.statechart import StateChartModule

print("=" * 60)
print("TEST 10: StateChart Component with C# Export Binding")
print("=" * 60)

# ============================================================
# STEP 1: Create UI
# ============================================================

print("\n📝 STEP 1: Creating UI...")

scene = TscnBuilder(root_name="PlayerHUD", root_type="Control")
ui = UIModule(scene)
ui.setup_fullscreen_control()

ui.add_vbox("MainVBox", parent=".", separation=10)
ui.add_label("HealthLabel", parent="MainVBox", text="Health")
ui.add_progress_bar("HealthBar", parent="MainVBox", value=100)
ui.add_label("ManaLabel", parent="MainVBox", text="Mana")
ui.add_progress_bar("ManaBar", parent="MainVBox", value=100)
ui.add_button("PauseButton", parent="MainVBox", text="Pause")
ui.add_label("StatusLabel", parent="MainVBox", text="")

print("✅ UI created with 7 controls")

# ============================================================
# STEP 2: Create StateChart
# ============================================================

print("\n📝 STEP 2: Creating StateChart...")

sc = StateChartModule(scene, parent=".")
sc.add_statechart("HUDStateChart")

sc.add_compound_state("Root", parent="HUDStateChart", initial_state="Active")
sc.add_atomic_state("Active", parent="Root")
sc.add_atomic_state("Paused", parent="Root")
sc.add_atomic_state("Hidden", parent="Root")

sc.add_transition("ToPaused", from_state="Active", to_state="Paused", event="pause")
sc.add_transition("ToActive", from_state="Paused", to_state="Active", event="resume")
sc.add_transition("ToHidden", from_state="Active", to_state="Hidden", event="hide")
sc.add_transition("ToActive2", from_state="Hidden", to_state="Active", event="show")

sc.resolve_initial_states()

print("✅ StateChart created with 3 states and 4 transitions")

# ============================================================
# STEP 3: Add C# Components to States
# ============================================================

print("\n📝 STEP 3: Adding C# components to states...")

# Add HUDActiveController to Active state
sc.add_component(
    name="HUDActiveController",
    parent="Active",
    script_path="res://B1Scripts/UI/HUDActiveController.cs",
    script_uid="uid://hud_active_controller"
)

# Add HUDPausedController to Paused state
sc.add_component(
    name="HUDPausedController",
    parent="Paused",
    script_path="res://B1Scripts/UI/HUDPausedController.cs",
    script_uid="uid://hud_paused_controller"
)

print("✅ 2 components added to states")

# ============================================================
# STEP 4: Bind UI to Components
# ============================================================

print("\n📝 STEP 4: Binding UI to components...")

# Bind Active state component to UI
scene.assign_multiple_node_paths("HUDActiveController", {
    "HealthBar": "HealthBar",
    "ManaBar": "ManaBar",
    "StatusLabel": "StatusLabel",
    "PauseButton": "PauseButton"
})

# Bind Paused state component to UI
scene.assign_multiple_node_paths("HUDPausedController", {
    "StatusLabel": "StatusLabel",
    "PauseButton": "PauseButton"
})

print("✅ HUDActiveController: 4 bindings")
print("✅ HUDPausedController: 2 bindings")

# ============================================================
# STEP 5: Verify
# ============================================================

print("\n📋 Verifying component bindings:")

active_ctrl = scene.get_node("HUDActiveController")
paused_ctrl = scene.get_node("HUDPausedController")

assert "HealthBar" in active_ctrl.properties
assert "ManaBar" in active_ctrl.properties
assert "StatusLabel" in active_ctrl.properties
assert "PauseButton" in active_ctrl.properties
print("  ✅ HUDActiveController has all 4 bindings")

assert "StatusLabel" in paused_ctrl.properties
assert "PauseButton" in paused_ctrl.properties
print("  ✅ HUDPausedController has all 2 bindings")

# Verify NodePath format
assert active_ctrl.properties["HealthBar"] == 'NodePath("../../../../MainVBox/HealthBar")'
assert paused_ctrl.properties["StatusLabel"] == 'NodePath("../../../../MainVBox/StatusLabel")'
print("  ✅ NodePath format correct")

# Verify components are children of correct states
assert active_ctrl.parent.name == "Active"
assert paused_ctrl.parent.name == "Paused"
print("  ✅ Components attached to correct states")

# ============================================================
# STEP 6: Generate TSCN and Verify
# ============================================================

print("\n📝 Generating TSCN...")

tscn_content = scene.generate_tscn()

# Verify TSCN contains component nodes with bindings
assert '[node name="HUDActiveController" type="Node" parent="HUDStateChart/Root/Active"]' in tscn_content
assert '[node name="HUDPausedController" type="Node" parent="HUDStateChart/Root/Paused"]' in tscn_content
assert 'HealthBar = NodePath("../../../../MainVBox/HealthBar")' in tscn_content
assert 'ManaBar = NodePath("../../../../MainVBox/ManaBar")' in tscn_content
print("  ✅ TSCN format correct with component bindings")

# Generate tree view
print("\nGenerated Tree Structure:")
print(scene.generate_tree_view())
print("\n" + "=" * 60)

scene.save("c:/Godot/3d-practice/Scenes/Test_StateChart_Component_Binding.tscn")

print("\n✅ Test 10 Complete: StateChart component binding validated")
print("   - UI: 7 controls")
print("   - StateChart: 3 states, 4 transitions")
print("   - Components: 2 (HUDActiveController, HUDPausedController)")
print("   - Bindings: 6 total (4 + 2)")
print("   - Demonstrates complete MVC pattern with state-based controllers")
print("=" * 60)
