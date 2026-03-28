"""
Task 7: Checkpoint - Validate TscnReader API
Comprehensive test of all TscnReader query methods with SettingsMenuV2.tscn
"""

import sys
from pathlib import Path

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from tscn_editor_tools.reader import TscnReader
from tscn_editor_tools.types import Color


def get_settings_menu_path():
    """Get path to SettingsMenuV2.tscn"""
    script_dir = Path(__file__).parent.resolve()
    workspace_root = script_dir.parent.parent.parent.parent
    tscn_path = workspace_root / "3d-practice" / "A1UIScenes" / "SettingsMenuV2.tscn"
    
    if not tscn_path.exists():
        raise FileNotFoundError(f"SettingsMenuV2.tscn not found at: {tscn_path}")
    
    return str(tscn_path)


def test_initialization():
    """Test 1: TscnReader initialization"""
    print("=" * 70)
    print("Test 1: TscnReader Initialization")
    print("=" * 70)
    
    tscn_path = get_settings_menu_path()
    reader = TscnReader(tscn_path)
    
    print(f"✓ Loaded: {Path(tscn_path).name}")
    print(f"✓ Format version: {reader.tree.header.format_version}")
    print(f"✓ Scene UID: {reader.tree.header.scene_uid}")
    print(f"✓ Total nodes: {len(reader.tree.nodes)}")
    print(f"✓ External resources: {len(reader.tree.ext_resources)}")
    print()
    
    return reader


def test_find_nodes_by_name(reader):
    """Test 2: find_nodes_by_name method"""
    print("=" * 70)
    print("Test 2: find_nodes_by_name()")
    print("=" * 70)
    
    # Test 1: Find root node
    nodes = reader.find_nodes_by_name("SettingsMenuV2_Control")
    assert len(nodes) == 1, f"Expected 1 node, got {len(nodes)}"
    assert nodes[0].node_type == "Control"
    print(f"✓ Found 'SettingsMenuV2_Control': {nodes[0].node_type}")
    
    # Test 2: Find button
    nodes = reader.find_nodes_by_name("BackButton_Button")
    assert len(nodes) == 1
    assert nodes[0].node_type == "Button"
    print(f"✓ Found 'BackButton_Button': {nodes[0].node_type}")
    
    # Test 3: Find scene instance
    nodes = reader.find_nodes_by_name("MasterVolume")
    assert len(nodes) == 1
    assert nodes[0].is_instance == True
    print(f"✓ Found 'MasterVolume': instance={nodes[0].is_instance}")
    
    # Test 4: Non-existent node
    nodes = reader.find_nodes_by_name("NonExistentNode")
    assert len(nodes) == 0
    print(f"✓ Non-existent node returns empty list")
    
    print()


def test_find_nodes_by_type(reader):
    """Test 3: find_nodes_by_type method"""
    print("=" * 70)
    print("Test 3: find_nodes_by_type()")
    print("=" * 70)
    
    # Test 1: Find all Button nodes
    buttons = reader.find_nodes_by_type("Button")
    print(f"✓ Found {len(buttons)} Button nodes:")
    for btn in buttons:
        print(f"    - {btn.name}")
    assert len(buttons) == 2  # BackButton and ResetButton
    
    # Test 2: Find all MarginContainer nodes
    margins = reader.find_nodes_by_type("MarginContainer")
    print(f"✓ Found {len(margins)} MarginContainer nodes")
    assert len(margins) > 5
    
    # Test 3: Find VBoxContainer nodes
    vboxes = reader.find_nodes_by_type("VBoxContainer")
    print(f"✓ Found {len(vboxes)} VBoxContainer nodes")
    assert len(vboxes) >= 4
    
    # Test 4: Find Label nodes
    labels = reader.find_nodes_by_type("Label")
    print(f"✓ Found {len(labels)} Label node(s)")
    assert len(labels) == 1
    
    # Test 5: Non-existent type
    nodes = reader.find_nodes_by_type("NonExistentType")
    assert len(nodes) == 0
    print(f"✓ Non-existent type returns empty list")
    
    print()


def test_find_nodes_by_property(reader):
    """Test 4: find_nodes_by_property method"""
    print("=" * 70)
    print("Test 4: find_nodes_by_property()")
    print("=" * 70)
    
    # Test 1: Find by text property
    nodes = reader.find_nodes_by_property("text", "Back")
    assert len(nodes) == 1
    assert nodes[0].name == "BackButton_Button"
    print(f"✓ Found node with text='Back': {nodes[0].name}")
    
    # Test 2: Find by layout_mode
    nodes = reader.find_nodes_by_property("layout_mode", 3)
    print(f"✓ Found {len(nodes)} nodes with layout_mode=3")
    assert len(nodes) >= 1
    
    # Test 3: Find by Color property
    color = Color(0.12, 0.12, 0.12, 1.0)
    nodes = reader.find_nodes_by_property("color", color)
    assert len(nodes) >= 1
    print(f"✓ Found {len(nodes)} node(s) with color={color}")
    
    # Test 4: Find by boolean property
    nodes = reader.find_nodes_by_property("visible", False)
    print(f"✓ Found {len(nodes)} nodes with visible=False")
    assert len(nodes) >= 1
    
    # Test 5: Find by custom property (scene instance)
    nodes = reader.find_nodes_by_property("LabelText", "Master")
    assert len(nodes) == 1
    assert nodes[0].name == "MasterVolume"
    print(f"✓ Found scene instance with LabelText='Master': {nodes[0].name}")
    
    # Test 6: Non-existent property
    nodes = reader.find_nodes_by_property("nonexistent_prop", "value")
    assert len(nodes) == 0
    print(f"✓ Non-existent property returns empty list")
    
    print()


def test_get_node_property(reader):
    """Test 5: get_node_property method"""
    print("=" * 70)
    print("Test 5: get_node_property()")
    print("=" * 70)
    
    # Test 1: Get text property (use full path)
    back_button_path = "MainMargin_MarginContainer/MainVBox_VBoxContainer/ButtonsMargin_MarginContainer/Buttons_HBoxContainer/BackButton_Button"
    text = reader.get_node_property(back_button_path, "text")
    assert text == "Back"
    print(f"✓ BackButton text: '{text}'")
    
    # Test 2: Get Color property
    color = reader.get_node_property("Background_ColorRect", "color")
    assert isinstance(color, Color)
    assert color.r == 0.12
    print(f"✓ Background color: {color}")
    
    # Test 3: Get numeric property
    layout_mode = reader.get_node_property("SettingsMenuV2_Control", "layout_mode")
    assert layout_mode == 3
    print(f"✓ Root layout_mode: {layout_mode}")
    
    # Test 4: Get boolean property
    audio_path = "MainMargin_MarginContainer/MainVBox_VBoxContainer/Tabs_TabContainer/Audio"
    visible = reader.get_node_property(audio_path, "visible")
    assert visible == False
    print(f"✓ Audio tab visible: {visible}")
    
    # Test 5: Get scene instance property
    default_value = reader.get_node_property("MainMargin_MarginContainer/MainVBox_VBoxContainer/Tabs_TabContainer/Audio/AudioMargin_MarginContainer/AudioContent_VBoxContainer/MasterVolume", "DefaultValue")
    assert default_value == 100.0
    print(f"✓ MasterVolume DefaultValue: {default_value}")
    
    # Test 6: Non-existent property
    value = reader.get_node_property(back_button_path, "nonexistent")
    assert value is None
    print(f"✓ Non-existent property returns None")
    
    # Test 7: Non-existent node
    value = reader.get_node_property("NonExistent/Path", "text")
    assert value is None
    print(f"✓ Property from non-existent node returns None")
    
    print()


def test_get_node_properties(reader):
    """Test 6: get_node_properties method"""
    print("=" * 70)
    print("Test 6: get_node_properties()")
    print("=" * 70)
    
    # Test 1: Get all properties from button (use full path)
    back_button_path = "MainMargin_MarginContainer/MainVBox_VBoxContainer/ButtonsMargin_MarginContainer/Buttons_HBoxContainer/BackButton_Button"
    props = reader.get_node_properties(back_button_path)
    assert "text" in props
    assert props["text"] == "Back"
    print(f"✓ BackButton_Button has {len(props)} properties:")
    for key, value in list(props.items())[:5]:  # Show first 5
        print(f"    - {key}: {value}")
    if len(props) > 5:
        print(f"    ... and {len(props) - 5} more")
    
    # Test 2: Get properties from ColorRect
    props = reader.get_node_properties("Background_ColorRect")
    assert "color" in props
    assert isinstance(props["color"], Color)
    print(f"✓ Background_ColorRect has {len(props)} properties")
    
    # Test 3: Get properties from scene instance
    props = reader.get_node_properties("MainMargin_MarginContainer/MainVBox_VBoxContainer/Tabs_TabContainer/Audio/AudioMargin_MarginContainer/AudioContent_VBoxContainer/MasterVolume")
    assert "DefaultValue" in props
    assert "LabelText" in props
    print(f"✓ MasterVolume has {len(props)} properties (scene instance)")
    
    # Test 4: Non-existent node
    props = reader.get_node_properties("NonExistent/Path")
    assert len(props) == 0
    print(f"✓ Non-existent node returns empty dict")
    
    print()


def test_node_exists(reader):
    """Test 7: node_exists method"""
    print("=" * 70)
    print("Test 7: node_exists()")
    print("=" * 70)
    
    # Test 1: Root node exists
    assert reader.node_exists("SettingsMenuV2_Control") == True
    print(f"✓ 'SettingsMenuV2_Control' exists")
    
    # Test 2: Child node exists
    assert reader.node_exists("Background_ColorRect") == True
    print(f"✓ 'Background_ColorRect' exists")
    
    # Test 3: Deeply nested node exists (use full path)
    back_button_path = "MainMargin_MarginContainer/MainVBox_VBoxContainer/ButtonsMargin_MarginContainer/Buttons_HBoxContainer/BackButton_Button"
    assert reader.node_exists(back_button_path) == True
    print(f"✓ Deeply nested 'BackButton_Button' exists")
    
    # Test 4: Scene instance exists
    assert reader.node_exists("MainMargin_MarginContainer/MainVBox_VBoxContainer/Tabs_TabContainer/Audio/AudioMargin_MarginContainer/AudioContent_VBoxContainer/MasterVolume") == True
    print(f"✓ Scene instance 'MasterVolume' exists")
    
    # Test 5: Non-existent node
    assert reader.node_exists("NonExistentNode") == False
    print(f"✓ 'NonExistentNode' does not exist")
    
    # Test 6: Non-existent path
    assert reader.node_exists("SettingsMenuV2_Control/NonExistent/Path") == False
    print(f"✓ Invalid path does not exist")
    
    print()


def test_get_node_count_by_type(reader):
    """Test 8: get_node_count_by_type method"""
    print("=" * 70)
    print("Test 8: get_node_count_by_type()")
    print("=" * 70)
    
    # Test 1: Count Button nodes
    count = reader.get_node_count_by_type("Button")
    assert count == 2
    print(f"✓ Button count: {count}")
    
    # Test 2: Count MarginContainer nodes
    count = reader.get_node_count_by_type("MarginContainer")
    print(f"✓ MarginContainer count: {count}")
    assert count > 5
    
    # Test 3: Count VBoxContainer nodes
    count = reader.get_node_count_by_type("VBoxContainer")
    print(f"✓ VBoxContainer count: {count}")
    assert count >= 4
    
    # Test 4: Count Control nodes (root)
    count = reader.get_node_count_by_type("Control")
    assert count == 1
    print(f"✓ Control count: {count}")
    
    # Test 5: Count Label nodes
    count = reader.get_node_count_by_type("Label")
    assert count == 1
    print(f"✓ Label count: {count}")
    
    # Test 6: Non-existent type
    count = reader.get_node_count_by_type("NonExistentType")
    assert count == 0
    print(f"✓ NonExistentType count: {count}")
    
    print()


def test_list_ext_resources(reader):
    """Test 9: list_ext_resources method"""
    print("=" * 70)
    print("Test 9: list_ext_resources()")
    print("=" * 70)
    
    ext_resources = reader.list_ext_resources()
    assert len(ext_resources) == 3
    print(f"✓ Found {len(ext_resources)} external resources:\n")
    
    for i, res in enumerate(ext_resources, 1):
        print(f"  Resource {i}:")
        print(f"    - Type: {res.resource_type}")
        print(f"    - UID: {res.uid}")
        print(f"    - Path: {res.path}")
        print(f"    - ID: {res.resource_id}")
        print()
        
        assert res.resource_type == "PackedScene"
        assert res.uid.startswith("uid://")
        assert res.path.startswith("res://")
    
    # Verify specific resources
    slider = ext_resources[0]
    assert slider.path == "res://A1UIScenes/UIComponents/SliderComponent.tscn"
    assert slider.resource_id == "1_scene"
    print(f"✓ SliderComponent resource verified")
    
    toggle = ext_resources[1]
    assert toggle.path == "res://A1UIScenes/UIComponents/ToggleComponent.tscn"
    assert toggle.resource_id == "2_scene"
    print(f"✓ ToggleComponent resource verified")
    
    dropdown = ext_resources[2]
    assert dropdown.path == "res://A1UIScenes/UIComponents/DropdownComponent.tscn"
    assert dropdown.resource_id == "3_scene"
    print(f"✓ DropdownComponent resource verified")
    
    print()


def test_print_tree_view(reader):
    """Test 10: print_tree_view method"""
    print("=" * 70)
    print("Test 10: print_tree_view()")
    print("=" * 70)
    
    tree_view = reader.print_tree_view()
    
    # Verify output is not empty
    assert tree_view is not None
    assert len(tree_view) > 0
    print(f"✓ Tree view generated ({len(tree_view)} characters)")
    
    # Verify expected content
    assert "SettingsMenuV2_Control" in tree_view
    print(f"✓ Contains root node name")
    
    assert "Control" in tree_view
    print(f"✓ Contains node types")
    
    assert "unique_id=" in tree_view
    print(f"✓ Contains unique_id annotations")
    
    assert "INSTANCE:" in tree_view
    print(f"✓ Contains scene instance annotations")
    
    assert "├──" in tree_view or "└──" in tree_view
    print(f"✓ Contains tree structure characters")
    
    # Check for specific nodes
    assert "BackButton_Button" in tree_view
    assert "MasterVolume" in tree_view
    print(f"✓ Contains expected node names")
    
    # Check for properties inline
    assert "text:" in tree_view or "color:" in tree_view
    print(f"✓ Contains inline properties")
    
    print(f"\n{'=' * 70}")
    print("Tree View Output:")
    print('=' * 70)
    print(tree_view)
    print('=' * 70)
    print()


def run_all_tests():
    """Run all TscnReader API validation tests"""
    print("\n" + "=" * 70)
    print("TASK 7: CHECKPOINT - VALIDATE TscnReader API")
    print("Testing with SettingsMenuV2.tscn")
    print("=" * 70)
    print()
    
    try:
        # Initialize reader
        reader = test_initialization()
        
        # Run all query method tests
        test_find_nodes_by_name(reader)
        test_find_nodes_by_type(reader)
        test_find_nodes_by_property(reader)
        test_get_node_property(reader)
        test_get_node_properties(reader)
        test_node_exists(reader)
        test_get_node_count_by_type(reader)
        test_list_ext_resources(reader)
        test_print_tree_view(reader)
        
        # Summary
        print("=" * 70)
        print("✓✓✓ ALL TscnReader API TESTS PASSED ✓✓✓")
        print("=" * 70)
        print()
        print("Summary:")
        print("  ✓ find_nodes_by_name() - Working correctly")
        print("  ✓ find_nodes_by_type() - Working correctly")
        print("  ✓ find_nodes_by_property() - Working correctly")
        print("  ✓ get_node_property() - Working correctly")
        print("  ✓ get_node_properties() - Working correctly")
        print("  ✓ node_exists() - Working correctly")
        print("  ✓ get_node_count_by_type() - Working correctly")
        print("  ✓ list_ext_resources() - Working correctly")
        print("  ✓ print_tree_view() - Working correctly")
        print()
        print("TscnReader API is fully validated and ready for use!")
        print()
        
    except Exception as e:
        print(f"\n✗✗✗ TEST FAILED ✗✗✗")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    run_all_tests()
