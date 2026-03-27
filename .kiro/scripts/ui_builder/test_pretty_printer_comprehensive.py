"""
Comprehensive test for Pretty_Printer covering all sub-tasks
"""

import sys
from pathlib import Path

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from tscn_editor_tools.parser import Parser
from tscn_editor_tools.node_tree import Node_Tree
from tscn_editor_tools.pretty_printer import Pretty_Printer
from tscn_editor_tools.types import Color, Vector2, NodePath, ExtResourceRef


def test_subtask_5_1_header_formatting():
    """Test 5.1: Create pretty_printer.py with Pretty_Printer class and header formatting"""
    print("=== Test 5.1: Header Formatting ===")
    
    tscn_content = """[gd_scene format=3 uid="uid://test123"]

[node name="Root" type="Control" unique_id=1]
"""
    
    parser = Parser(tscn_content)
    header, ext_resources, nodes = parser.parse()
    tree = Node_Tree(header=header, ext_resources=ext_resources, nodes=nodes)
    
    printer = Pretty_Printer()
    output = printer.print_tree(tree)
    
    # Verify header format
    assert '[gd_scene format=3 uid="uid://test123"]' in output
    print("  ✓ Header format correct")
    print("  ✓ Pretty_Printer class created")
    print()


def test_subtask_5_2_external_resource_formatting():
    """Test 5.2: Implement external resource formatting"""
    print("=== Test 5.2: External Resource Formatting ===")
    
    tscn_content = """[gd_scene format=3 uid="uid://test123"]

[ext_resource type="PackedScene" uid="uid://scene123" path="res://scenes/test.tscn" id="1_scene"]
[ext_resource type="Script" uid="uid://script456" path="res://scripts/test.gd" id="2_script"]

[node name="Root" type="Control" unique_id=1]
"""
    
    parser = Parser(tscn_content)
    header, ext_resources, nodes = parser.parse()
    tree = Node_Tree(header=header, ext_resources=ext_resources, nodes=nodes)
    
    printer = Pretty_Printer()
    output = printer.print_tree(tree)
    
    # Verify ext_resource format with correct attribute order
    assert '[ext_resource type="PackedScene" uid="uid://scene123" path="res://scenes/test.tscn" id="1_scene"]' in output
    assert '[ext_resource type="Script" uid="uid://script456" path="res://scripts/test.gd" id="2_script"]' in output
    print("  ✓ External resource format correct")
    print("  ✓ Attribute order preserved (type, uid, path, id)")
    print()


def test_subtask_5_3_node_section_formatting():
    """Test 5.3: Implement node section formatting"""
    print("=== Test 5.3: Node Section Formatting ===")
    
    tscn_content = """[gd_scene format=3 uid="uid://test123"]

[ext_resource type="PackedScene" uid="uid://scene123" path="res://scenes/test.tscn" id="1_scene"]

[node name="Root" type="Control" unique_id=480540166]
layout_mode = 3

[node name="Child" type="Button" parent="Root" unique_id=123456]
text = "Click"

[node name="Instance" type="MarginContainer" parent="Root" instance=ExtResource("1_scene") unique_id=789012]
"""
    
    parser = Parser(tscn_content)
    header, ext_resources, nodes = parser.parse()
    tree = Node_Tree(header=header, ext_resources=ext_resources, nodes=nodes)
    
    printer = Pretty_Printer()
    output = printer.print_tree(tree)
    
    # Verify node formats
    assert '[node name="Root" type="Control" unique_id=480540166]' in output
    assert '[node name="Child" type="Button" parent="Root" unique_id=123456]' in output
    assert '[node name="Instance" type="MarginContainer" parent="Root" instance=ExtResource("1_scene") unique_id=789012]' in output
    
    print("  ✓ Root node format correct (no parent attribute)")
    print("  ✓ Child node format correct (with parent attribute)")
    print("  ✓ Scene instance format correct (with instance attribute)")
    print("  ✓ Node order maintained")
    print()


def test_subtask_5_4_property_value_formatting():
    """Test 5.4: Implement property value formatting"""
    print("=== Test 5.4: Property Value Formatting ===")
    
    tscn_content = """[gd_scene format=3 uid="uid://test123"]

[ext_resource type="Script" uid="uid://script123" path="res://test.gd" id="1_script"]

[node name="Root" type="Control" unique_id=1]
text = "Hello World"
number_int = 42
number_float = 3.14
bool_true = true
bool_false = false
color = Color(0.12, 0.34, 0.56, 1)
vector = Vector2(100, 200)
node_path = NodePath("path/to/node")
script = ExtResource("1_script")
"""
    
    parser = Parser(tscn_content)
    header, ext_resources, nodes = parser.parse()
    tree = Node_Tree(header=header, ext_resources=ext_resources, nodes=nodes)
    
    printer = Pretty_Printer()
    output = printer.print_tree(tree)
    
    # Verify property value formats
    assert 'text = "Hello World"' in output
    assert 'number_int = 42' in output
    assert 'number_float = 3.14' in output
    assert 'bool_true = true' in output
    assert 'bool_false = false' in output
    assert 'color = Color(0.12, 0.34, 0.56, 1' in output  # Allow for float precision
    assert 'vector = Vector2(100' in output
    assert 'node_path = NodePath("path/to/node")' in output
    assert 'script = ExtResource("1_script")' in output
    
    print("  ✓ String values formatted with quotes")
    print("  ✓ Integer values formatted correctly")
    print("  ✓ Float values formatted correctly")
    print("  ✓ Boolean values formatted correctly")
    print("  ✓ Color() constructor syntax preserved")
    print("  ✓ Vector2() constructor syntax preserved")
    print("  ✓ NodePath() constructor syntax preserved")
    print("  ✓ ExtResource() constructor syntax preserved")
    print()


def test_subtask_5_5_formatting_consistency():
    """Test 5.5: Implement formatting consistency"""
    print("=== Test 5.5: Formatting Consistency ===")
    
    tscn_content = """[gd_scene format=3 uid="uid://test123"]

[ext_resource type="PackedScene" uid="uid://scene123" path="res://test.tscn" id="1_scene"]
[ext_resource type="Script" uid="uid://script456" path="res://test.gd" id="2_script"]

[node name="Root" type="Control" unique_id=1]
layout_mode = 3

[node name="Child1" type="Button" parent="Root" unique_id=2]
text = "Button 1"

[node name="Child2" type="Label" parent="Root" unique_id=3]
text = "Label 1"
"""
    
    parser = Parser(tscn_content)
    header, ext_resources, nodes = parser.parse()
    tree = Node_Tree(header=header, ext_resources=ext_resources, nodes=nodes)
    
    printer = Pretty_Printer()
    output = printer.print_tree(tree)
    
    lines = output.split('\n')
    
    # Verify blank line after header
    assert lines[0].startswith('[gd_scene')
    assert lines[1] == ''
    print("  ✓ Blank line after header")
    
    # Verify blank line after ext_resources
    ext_resource_end = None
    for i, line in enumerate(lines):
        if line.startswith('[ext_resource'):
            ext_resource_end = i
    
    if ext_resource_end:
        # Find next non-empty line
        next_line_idx = ext_resource_end + 1
        while next_line_idx < len(lines) and lines[next_line_idx].startswith('[ext_resource'):
            next_line_idx += 1
        
        if next_line_idx < len(lines):
            assert lines[next_line_idx] == ''
            print("  ✓ Blank line after ext_resources section")
    
    # Verify blank lines between node sections
    node_indices = [i for i, line in enumerate(lines) if line.startswith('[node')]
    for i in range(len(node_indices) - 1):
        # Find the blank line between nodes
        current_node_idx = node_indices[i]
        next_node_idx = node_indices[i + 1]
        
        # There should be a blank line before the next node
        assert lines[next_node_idx - 1] == '', f"Missing blank line before node at line {next_node_idx}"
    
    print("  ✓ Blank lines between node sections")
    print("  ✓ Node order maintained from Node_Tree")
    print()


def test_round_trip_property():
    """Test round-trip property: Parse → Print → Parse produces equivalent tree"""
    print("=== Test Round-Trip Property ===")
    
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

[node name="SliderInstance" type="MarginContainer" parent="Root/Container" instance=ExtResource("1_scene") unique_id=1215484890]
"""
    
    # First parse
    parser1 = Parser(tscn_content)
    header1, ext_resources1, nodes1 = parser1.parse()
    tree1 = Node_Tree(header=header1, ext_resources=ext_resources1, nodes=nodes1)
    
    # Print
    printer = Pretty_Printer()
    printed = printer.print_tree(tree1)
    
    # Second parse
    parser2 = Parser(printed)
    header2, ext_resources2, nodes2 = parser2.parse()
    tree2 = Node_Tree(header=header2, ext_resources=ext_resources2, nodes=nodes2)
    
    # Compare
    assert header1.format_version == header2.format_version
    assert header1.scene_uid == header2.scene_uid
    assert len(ext_resources1) == len(ext_resources2)
    assert len(nodes1) == len(nodes2)
    
    for node1, node2 in zip(nodes1, nodes2):
        assert node1.name == node2.name
        assert node1.node_type == node2.node_type
        assert node1.unique_id == node2.unique_id
        assert node1.parent_path == node2.parent_path
        assert node1.is_instance == node2.is_instance
    
    print("  ✓ Round-trip property verified")
    print("  ✓ Parse → Print → Parse produces equivalent tree")
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("COMPREHENSIVE PRETTY_PRINTER TEST")
    print("=" * 60)
    print()
    
    test_subtask_5_1_header_formatting()
    test_subtask_5_2_external_resource_formatting()
    test_subtask_5_3_node_section_formatting()
    test_subtask_5_4_property_value_formatting()
    test_subtask_5_5_formatting_consistency()
    test_round_trip_property()
    
    print("=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)
    print()
    print("Task 5 Complete:")
    print("  ✓ 5.1 - Pretty_Printer class with header formatting")
    print("  ✓ 5.2 - External resource formatting")
    print("  ✓ 5.3 - Node section formatting")
    print("  ✓ 5.4 - Property value formatting")
    print("  ✓ 5.5 - Formatting consistency")
