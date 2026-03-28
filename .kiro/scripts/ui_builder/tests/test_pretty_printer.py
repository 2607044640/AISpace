"""
Test Pretty_Printer round-trip: parse -> print -> parse
"""

import sys
from pathlib import Path

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from tscn_editor_tools.parser import Parser
from tscn_editor_tools.node_tree import Node_Tree
from tscn_editor_tools.pretty_printer import Pretty_Printer


def test_pretty_printer():
    """Test Pretty_Printer with round-trip parsing"""
    
    # Sample .tscn content
    original_tscn = """[gd_scene format=3 uid="uid://bs256ppml668y"]

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
    
    print("=== Pretty_Printer Test ===\n")
    
    # Test 1: Parse original
    print("Test 1: Parse original .tscn")
    parser1 = Parser(original_tscn)
    header1, ext_resources1, nodes1 = parser1.parse()
    tree1 = Node_Tree(header=header1, ext_resources=ext_resources1, nodes=nodes1)
    print(f"  - Parsed {len(nodes1)} nodes")
    print("✓ PASSED\n")
    
    # Test 2: Print to text
    print("Test 2: Print Node_Tree to text")
    printer = Pretty_Printer()
    printed_tscn = printer.print_tree(tree1)
    print("  - Generated .tscn text:")
    print("--- START ---")
    print(printed_tscn)
    print("--- END ---")
    print("✓ PASSED\n")
    
    # Test 3: Parse printed text
    print("Test 3: Parse printed text (round-trip)")
    parser2 = Parser(printed_tscn)
    header2, ext_resources2, nodes2 = parser2.parse()
    tree2 = Node_Tree(header=header2, ext_resources=ext_resources2, nodes=nodes2)
    print(f"  - Parsed {len(nodes2)} nodes")
    print("✓ PASSED\n")
    
    # Test 4: Compare trees
    print("Test 4: Compare original and round-trip trees")
    
    # Compare headers
    assert header1.format_version == header2.format_version, "Format version mismatch"
    assert header1.scene_uid == header2.scene_uid, "Scene UID mismatch"
    print("  - Headers match ✓")
    
    # Compare ext_resources
    assert len(ext_resources1) == len(ext_resources2), "ExtResource count mismatch"
    for i, (res1, res2) in enumerate(zip(ext_resources1, ext_resources2)):
        assert res1.resource_type == res2.resource_type, f"ExtResource {i} type mismatch"
        assert res1.uid == res2.uid, f"ExtResource {i} uid mismatch"
        assert res1.path == res2.path, f"ExtResource {i} path mismatch"
        assert res1.resource_id == res2.resource_id, f"ExtResource {i} id mismatch"
    print("  - ExtResources match ✓")
    
    # Compare nodes
    assert len(nodes1) == len(nodes2), f"Node count mismatch: {len(nodes1)} vs {len(nodes2)}"
    for i, (node1, node2) in enumerate(zip(nodes1, nodes2)):
        assert node1.name == node2.name, f"Node {i} name mismatch: {node1.name} vs {node2.name}"
        assert node1.node_type == node2.node_type, f"Node {i} type mismatch"
        assert node1.unique_id == node2.unique_id, f"Node {i} unique_id mismatch"
        assert node1.parent_path == node2.parent_path, f"Node {i} parent_path mismatch"
        assert node1.is_instance == node2.is_instance, f"Node {i} is_instance mismatch"
        
        # Compare properties (excluding internal metadata)
        props1 = {k: v for k, v in node1.properties.items() if not k.startswith('_')}
        props2 = {k: v for k, v in node2.properties.items() if not k.startswith('_')}
        assert props1.keys() == props2.keys(), f"Node {i} ({node1.name}) property keys mismatch"
        
        for key in props1.keys():
            val1 = props1[key]
            val2 = props2[key]
            # Compare by string representation for complex types
            assert str(val1) == str(val2), f"Node {i} ({node1.name}) property '{key}' mismatch: {val1} vs {val2}"
    
    print("  - Nodes match ✓")
    print("✓ PASSED\n")
    
    # Test 5: Verify scene instance metadata
    print("Test 5: Verify scene instance metadata preserved")
    slider1 = tree1.get_node_by_path("Root/Container/SliderInstance")
    slider2 = tree2.get_node_by_path("Root/Container/SliderInstance")
    
    assert slider1.is_instance == slider2.is_instance, "is_instance mismatch"
    assert slider1.scene_path == slider2.scene_path, "scene_path mismatch"
    assert slider1.scene_uid == slider2.scene_uid, "scene_uid mismatch"
    
    print(f"  - Scene instance: {slider2.name}")
    print(f"  - scene_path: {slider2.scene_path}")
    print(f"  - scene_uid: {slider2.scene_uid}")
    print("✓ PASSED\n")
    
    print("=== All Tests Passed! ===")
    print("\nRound-trip property verified: Parse → Print → Parse produces equivalent tree")


if __name__ == "__main__":
    test_pretty_printer()
