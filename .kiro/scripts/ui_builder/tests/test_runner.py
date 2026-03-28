"""
Test runner for tscn_editor_tools
"""

import sys
from pathlib import Path

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from tscn_editor_tools.parser import Parser
from tscn_editor_tools.node_tree import Node_Tree


def test_node_tree():
    """Test Node_Tree with a sample .tscn file"""
    
    # Sample .tscn content
    tscn_content = """[gd_scene format=3 uid="uid://bs256ppml668y"]

[ext_resource type="PackedScene" uid="uid://dbaix0lcy10v2" path="res://A1UIScenes/UIComponents/SliderComponent.tscn" id="1_scene"]
[ext_resource type="Script" uid="uid://abc123" path="res://scripts/test.gd" id="2_script"]

[node name="Root" type="Control" unique_id=480540166]
layout_mode = 3
anchors_preset = 15

[node name="Background" type="ColorRect" parent="Root" unique_id=1633307466]
layout_mode = 1
color = Color(0.12, 0.12, 0.12, 1)

[node name="Container" type="VBoxContainer" parent="Root" unique_id=179320186]
layout_mode = 1

[node name="Button1" type="Button" parent="Root/Container" unique_id=1140248651]
text = "Click Me"

[node name="Button2" type="Button" parent="Root/Container" unique_id=1614754775]
text = "Another Button"

[node name="SliderInstance" type="MarginContainer" parent="Root/Container" instance=ExtResource("1_scene") unique_id=1215484890]
"""
    
    # Parse the content
    parser = Parser(tscn_content)
    header, ext_resources, nodes = parser.parse()
    
    # Create Node_Tree
    tree = Node_Tree(header=header, ext_resources=ext_resources, nodes=nodes)
    
    print("=== Node_Tree Test ===\n")
    
    # Test 1: Get root nodes
    print("Test 1: Get root nodes")
    root_nodes = tree.get_root_nodes()
    print(f"Found {len(root_nodes)} root node(s):")
    for node in root_nodes:
        print(f"  - {node.name} ({node.node_type})")
    assert len(root_nodes) == 1
    assert root_nodes[0].name == "Root"
    print("✓ PASSED\n")
    
    # Test 2: Get nodes by type
    print("Test 2: Get nodes by type (Button)")
    buttons = tree.get_nodes_by_type("Button")
    print(f"Found {len(buttons)} Button node(s):")
    for node in buttons:
        print(f"  - {node.name}")
    assert len(buttons) == 2
    assert buttons[0].name == "Button1"
    assert buttons[1].name == "Button2"
    print("✓ PASSED\n")
    
    # Test 3: Get node by path
    print("Test 3: Get node by path")
    node = tree.get_node_by_path("Root")
    assert node is not None
    assert node.name == "Root"
    print(f"  - Found: {node.name} ({node.node_type})")
    
    node = tree.get_node_by_path("Root/Container")
    assert node is not None
    assert node.name == "Container"
    print(f"  - Found: {node.name} ({node.node_type})")
    
    node = tree.get_node_by_path("Root/Container/Button1")
    assert node is not None
    assert node.name == "Button1"
    print(f"  - Found: {node.name} ({node.node_type})")
    print("✓ PASSED\n")
    
    # Test 4: Get children
    print("Test 4: Get children of 'Root/Container'")
    children = tree.get_children("Root/Container")
    print(f"Found {len(children)} child(ren):")
    for node in children:
        print(f"  - {node.name} ({node.node_type})")
    assert len(children) == 3
    print("✓ PASSED\n")
    
    # Test 5: Build full path
    print("Test 5: Build full path")
    button_node = tree.get_node_by_path("Root/Container/Button1")
    full_path = tree.build_full_path(button_node)
    print(f"  - Full path: {full_path}")
    assert full_path == "Root/Container/Button1"
    print("✓ PASSED\n")
    
    # Test 6: Scene instance metadata
    print("Test 6: Scene instance metadata")
    slider_node = tree.get_node_by_path("Root/Container/SliderInstance")
    assert slider_node is not None
    print(f"  - Node: {slider_node.name}")
    print(f"  - is_instance: {slider_node.is_instance}")
    print(f"  - properties: {slider_node.properties}")
    print(f"  - scene_path: {slider_node.scene_path}")
    print(f"  - scene_uid: {slider_node.scene_uid}")
    assert slider_node.is_instance == True
    assert slider_node.scene_path == "res://A1UIScenes/UIComponents/SliderComponent.tscn"
    assert slider_node.scene_uid == "uid://dbaix0lcy10v2"
    print("✓ PASSED\n")
    
    print("=== All Tests Passed! ===")


if __name__ == "__main__":
    test_node_tree()
