"""
Test suite for TscnReader component
"""

import sys
from pathlib import Path
import tempfile

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from tscn_editor_tools.reader import TscnReader


def create_test_tscn_file():
    """Create a temporary .tscn file for testing"""
    tscn_content = """[gd_scene format=3 uid="uid://bs256ppml668y"]

[ext_resource type="PackedScene" uid="uid://dbaix0lcy10v2" path="res://A1UIScenes/UIComponents/SliderComponent.tscn" id="1_scene"]
[ext_resource type="Script" uid="uid://abc123" path="res://scripts/test.gd" id="2_script"]

[node name="SettingsMenu" type="Control" unique_id=480540166]
layout_mode = 3
anchors_preset = 15

[node name="Background" type="ColorRect" parent="SettingsMenu" unique_id=1633307466]
layout_mode = 1
color = Color(0.12, 0.12, 0.12, 1)

[node name="MainContainer" type="VBoxContainer" parent="SettingsMenu" unique_id=179320186]
layout_mode = 1

[node name="TitleLabel" type="Label" parent="SettingsMenu/MainContainer" unique_id=1140248651]
text = "Settings"

[node name="AudioButton" type="Button" parent="SettingsMenu/MainContainer" unique_id=1614754775]
text = "Audio Settings"

[node name="VideoButton" type="Button" parent="SettingsMenu/MainContainer" unique_id=1215484890]
text = "Video Settings"

[node name="SliderInstance" type="MarginContainer" parent="SettingsMenu/MainContainer" instance=ExtResource("1_scene") unique_id=2000000001]

[node name="ScriptedNode" type="Node" parent="SettingsMenu" unique_id=3000000001]
script = ExtResource("2_script")
"""
    
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.tscn', delete=False, encoding='utf-8')
    temp_file.write(tscn_content)
    temp_file.close()
    
    return temp_file.name


def test_reader_initialization():
    """Test TscnReader initialization and file loading"""
    print("=== Test 1: Reader Initialization ===")
    
    temp_file = create_test_tscn_file()
    
    try:
        reader = TscnReader(temp_file)
        assert reader.tree is not None
        assert reader.tree.header.format_version == 3
        assert reader.tree.header.scene_uid == "uid://bs256ppml668y"
        print("✓ Reader initialized successfully")
        print(f"✓ Format version: {reader.tree.header.format_version}")
        print(f"✓ Scene UID: {reader.tree.header.scene_uid}")
        print("✓ PASSED\n")
        return reader, temp_file
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        raise


def test_find_nodes_by_name(reader):
    """Test finding nodes by exact name match"""
    print("=== Test 2: Find Nodes by Name ===")
    
    # Find existing node
    nodes = reader.find_nodes_by_name("AudioButton")
    assert len(nodes) == 1
    assert nodes[0].name == "AudioButton"
    assert nodes[0].node_type == "Button"
    print(f"✓ Found 'AudioButton': {nodes[0].node_type}")
    
    # Find non-existent node
    nodes = reader.find_nodes_by_name("NonExistent")
    assert len(nodes) == 0
    print("✓ Non-existent node returns empty list")
    
    print("✓ PASSED\n")


def test_find_nodes_by_type(reader):
    """Test finding nodes by type"""
    print("=== Test 3: Find Nodes by Type ===")
    
    # Find all Button nodes
    buttons = reader.find_nodes_by_type("Button")
    assert len(buttons) == 2
    print(f"✓ Found {len(buttons)} Button nodes:")
    for btn in buttons:
        print(f"  - {btn.name}")
    
    # Find Label nodes
    labels = reader.find_nodes_by_type("Label")
    assert len(labels) == 1
    assert labels[0].name == "TitleLabel"
    print(f"✓ Found {len(labels)} Label node: {labels[0].name}")
    
    # Find non-existent type
    nodes = reader.find_nodes_by_type("NonExistentType")
    assert len(nodes) == 0
    print("✓ Non-existent type returns empty list")
    
    print("✓ PASSED\n")


def test_find_nodes_by_property(reader):
    """Test finding nodes by property value"""
    print("=== Test 4: Find Nodes by Property ===")
    
    # Find nodes with specific text
    nodes = reader.find_nodes_by_property("text", "Audio Settings")
    assert len(nodes) == 1
    assert nodes[0].name == "AudioButton"
    print(f"✓ Found node with text='Audio Settings': {nodes[0].name}")
    
    # Find nodes with layout_mode
    nodes = reader.find_nodes_by_property("layout_mode", 1)
    print(f"✓ Found {len(nodes)} nodes with layout_mode=1")
    
    # Find non-existent property
    nodes = reader.find_nodes_by_property("nonexistent_prop", "value")
    assert len(nodes) == 0
    print("✓ Non-existent property returns empty list")
    
    print("✓ PASSED\n")


def test_get_node_property(reader):
    """Test getting single property value"""
    print("=== Test 5: Get Node Property ===")
    
    # Get existing property
    text = reader.get_node_property("SettingsMenu/MainContainer/TitleLabel", "text")
    assert text == "Settings"
    print(f"✓ TitleLabel text: '{text}'")
    
    # Get Color property
    color = reader.get_node_property("SettingsMenu/Background", "color")
    assert color is not None
    print(f"✓ Background color: {color}")
    
    # Get non-existent property
    value = reader.get_node_property("SettingsMenu", "nonexistent")
    assert value is None
    print("✓ Non-existent property returns None")
    
    # Get property from non-existent node
    value = reader.get_node_property("NonExistent/Path", "text")
    assert value is None
    print("✓ Property from non-existent node returns None")
    
    print("✓ PASSED\n")


def test_get_node_properties(reader):
    """Test getting all properties for a node"""
    print("=== Test 6: Get Node Properties ===")
    
    # Get properties from node with multiple properties
    props = reader.get_node_properties("SettingsMenu/MainContainer/AudioButton")
    assert "text" in props
    assert props["text"] == "Audio Settings"
    print(f"✓ AudioButton has {len(props)} properties")
    print(f"  - text: {props['text']}")
    
    # Get properties from non-existent node
    props = reader.get_node_properties("NonExistent/Path")
    assert len(props) == 0
    print("✓ Non-existent node returns empty dict")
    
    print("✓ PASSED\n")


def test_node_exists(reader):
    """Test checking if node path exists"""
    print("=== Test 7: Node Exists ===")
    
    # Check existing nodes
    assert reader.node_exists("SettingsMenu") == True
    print("✓ 'SettingsMenu' exists")
    
    assert reader.node_exists("SettingsMenu/MainContainer/AudioButton") == True
    print("✓ 'SettingsMenu/MainContainer/AudioButton' exists")
    
    # Check non-existent node
    assert reader.node_exists("NonExistent") == False
    print("✓ 'NonExistent' does not exist")
    
    assert reader.node_exists("SettingsMenu/NonExistent/Path") == False
    print("✓ 'SettingsMenu/NonExistent/Path' does not exist")
    
    print("✓ PASSED\n")


def test_get_node_count_by_type(reader):
    """Test counting nodes by type"""
    print("=== Test 8: Get Node Count by Type ===")
    
    # Count Button nodes
    count = reader.get_node_count_by_type("Button")
    assert count == 2
    print(f"✓ Button count: {count}")
    
    # Count Control nodes
    count = reader.get_node_count_by_type("Control")
    assert count == 1
    print(f"✓ Control count: {count}")
    
    # Count non-existent type
    count = reader.get_node_count_by_type("NonExistentType")
    assert count == 0
    print(f"✓ NonExistentType count: {count}")
    
    print("✓ PASSED\n")


def test_list_ext_resources(reader):
    """Test listing external resources"""
    print("=== Test 9: List External Resources ===")
    
    ext_resources = reader.list_ext_resources()
    assert len(ext_resources) == 2
    print(f"✓ Found {len(ext_resources)} external resources:")
    
    for res in ext_resources:
        print(f"  - {res.resource_type}: {res.path} (id={res.resource_id})")
        assert res.resource_type in ["PackedScene", "Script"]
        assert res.uid.startswith("uid://")
    
    print("✓ PASSED\n")


def test_print_tree_view(reader):
    """Test tree visualization"""
    print("=== Test 10: Print Tree View ===")
    
    tree_view = reader.print_tree_view()
    assert tree_view is not None
    assert len(tree_view) > 0
    
    # Check for expected content
    assert "SettingsMenu" in tree_view
    assert "Control" in tree_view
    assert "AudioButton" in tree_view
    assert "INSTANCE:" in tree_view  # Scene instance annotation
    assert "[script]" in tree_view  # Script marker
    assert "├──" in tree_view or "└──" in tree_view  # Tree characters
    
    print("Tree View Output:")
    print("-" * 60)
    print(tree_view)
    print("-" * 60)
    print("✓ PASSED\n")


def run_all_tests():
    """Run all TscnReader tests"""
    print("\n" + "=" * 60)
    print("TscnReader Test Suite")
    print("=" * 60 + "\n")
    
    try:
        # Test 1: Initialization
        reader, temp_file = test_reader_initialization()
        
        # Test 2-10: Query methods
        test_find_nodes_by_name(reader)
        test_find_nodes_by_type(reader)
        test_find_nodes_by_property(reader)
        test_get_node_property(reader)
        test_get_node_properties(reader)
        test_node_exists(reader)
        test_get_node_count_by_type(reader)
        test_list_ext_resources(reader)
        test_print_tree_view(reader)
        
        # Cleanup
        Path(temp_file).unlink()
        
        print("=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"\n✗ TEST SUITE FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    run_all_tests()
