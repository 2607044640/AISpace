"""
Test 5: C# Export NodePath Binding
Validates automatic NodePath assignment to [Export] properties
"""

import sys
sys.path.append("../..")

from builder.core import TscnBuilder
from builder.modules.ui import UIModule

print("=" * 60)
print("TEST 5: C# Export NodePath Binding")
print("=" * 60)

# Initialize scene
scene = TscnBuilder(root_name="TestExportBinding", root_type="Control")
ui = UIModule(scene)
ui.setup_fullscreen_control()

# Create UI hierarchy
ui.add_vbox("MainVBox", parent=".", separation=10)
ui.add_hbox("Row1", parent="MainVBox", separation=5)
ui.add_button("Button1", parent="Row1", text="Button 1")
ui.add_button("Button2", parent="Row1", text="Button 2")

ui.add_hbox("Row2", parent="MainVBox", separation=5)
ui.add_label("Label1", parent="Row2", text="Label 1")
ui.add_progress_bar("Progress1", parent="Row2", value=50)

ui.add_vbox("NestedVBox", parent="MainVBox", separation=5)
ui.add_checkbox("Check1", parent="NestedVBox", text="Checkbox 1")
ui.add_checkbox("Check2", parent="NestedVBox", text="Checkbox 2")

# Add controller
controller_res_id = scene.add_ext_resource("Script", 
                                          "res://TestController.cs", 
                                          "uid://test_controller")
scene.add_node("Controller", "Node", parent=".",
              script=f'ExtResource("{controller_res_id}")')

# Test 1: Single assignment
print("\n📝 Test 1: Single NodePath assignment")
scene.assign_node_path("Controller", "Button1", "Button1")
controller = scene.get_node("Controller")
assert "Button1" in controller.properties
assert controller.properties["Button1"] == 'NodePath("../MainVBox/Row1/Button1")'
print("✅ Single assignment works correctly")

# Test 2: Multiple assignments
print("\n📝 Test 2: Batch NodePath assignments")
scene.assign_multiple_node_paths("Controller", {
    "Button2": "Button2",
    "Label1": "Label1",
    "Progress1": "Progress1",
    "Check1": "Check1",
    "Check2": "Check2"
})

assert controller.properties["Button2"] == 'NodePath("../MainVBox/Row1/Button2")'
assert controller.properties["Label1"] == 'NodePath("../MainVBox/Row2/Label1")'
assert controller.properties["Progress1"] == 'NodePath("../MainVBox/Row2/Progress1")'
assert controller.properties["Check1"] == 'NodePath("../MainVBox/NestedVBox/Check1")'
assert controller.properties["Check2"] == 'NodePath("../MainVBox/NestedVBox/Check2")'
print("✅ Batch assignments work correctly")

# Test 3: Cross-hierarchy paths
print("\n📝 Test 3: Cross-hierarchy NodePath calculation")
scene.add_node("SiblingController", "Node", parent=".",
              script=f'ExtResource("{controller_res_id}")')
scene.assign_node_path("SiblingController", "Button1", "Button1")

sibling = scene.get_node("SiblingController")
assert sibling.properties["Button1"] == 'NodePath("../MainVBox/Row1/Button1")'
print("✅ Cross-hierarchy paths calculated correctly")

# Test 4: Error handling
print("\n📝 Test 4: Error handling for invalid nodes")
try:
    scene.assign_node_path("NonExistentNode", "Prop", "Button1")
    print("❌ Should have raised ValueError for non-existent target node")
except ValueError as e:
    assert "not found in registry" in str(e)
    print("✅ Correctly raises error for non-existent target node")

try:
    scene.assign_node_path("Controller", "Prop", "NonExistentButton")
    print("❌ Should have raised ValueError for non-existent path node")
except ValueError as e:
    assert "not found in registry" in str(e)
    print("✅ Correctly raises error for non-existent path node")

# Test 5: Generate TSCN and verify format
print("\n📝 Test 5: TSCN generation with NodePath properties")
tscn_content = scene.generate_tscn()

# Verify NodePath format in generated TSCN
assert 'Button1 = NodePath("../MainVBox/Row1/Button1")' in tscn_content
assert 'Button2 = NodePath("../MainVBox/Row1/Button2")' in tscn_content
assert 'Label1 = NodePath("../MainVBox/Row2/Label1")' in tscn_content
assert 'Progress1 = NodePath("../MainVBox/Row2/Progress1")' in tscn_content
assert 'Check1 = NodePath("../MainVBox/NestedVBox/Check1")' in tscn_content
assert 'Check2 = NodePath("../MainVBox/NestedVBox/Check2")' in tscn_content
print("✅ TSCN format correct with NodePath properties")

# Generate tree view
print("\nGenerated Tree Structure:")
print(scene.generate_tree_view())
print("\n" + "=" * 60)

# Save scene
scene.save("c:/Godot/TetrisBackpack/Scenes/Test_Export_NodePath_Binding.tscn")

print("\n✅ Test 5 Complete: All NodePath binding tests passed")
print("   - Single assignment: ✅")
print("   - Batch assignments: ✅")
print("   - Cross-hierarchy paths: ✅")
print("   - Error handling: ✅")
print("   - TSCN format validation: ✅")
print("=" * 60)
