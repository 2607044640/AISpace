"""
Validation test for Task 4: Checkpoint - Validate parser and tree construction
Tests Parser and Node_Tree with SettingsMenuV2.tscn (10,800 chars)
"""

import sys
from pathlib import Path

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from tscn_editor_tools.parser import Parser
from tscn_editor_tools.node_tree import Node_Tree
from tscn_editor_tools.types import Color, Vector2, ExtResourceRef


def load_settings_menu():
    """Load SettingsMenuV2.tscn file"""
    # Get the workspace root (C:\Godot)
    # From: C:\Godot\KiroWorkingSpace\.kiro\scripts\ui_builder
    # To:   C:\Godot\3d-practice\A1UIScenes\SettingsMenuV2.tscn
    script_dir = Path(__file__).parent.resolve()  # ui_builder
    workspace_root = script_dir.parent.parent.parent.parent  # Go up to C:\Godot
    tscn_path = workspace_root / "3d-practice" / "A1UIScenes" / "SettingsMenuV2.tscn"
    
    if not tscn_path.exists():
        raise FileNotFoundError(f"SettingsMenuV2.tscn not found at: {tscn_path.resolve()}")
    
    with open(tscn_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"✓ Loaded SettingsMenuV2.tscn ({len(content)} chars)\n")
    return content


def validate_header(header):
    """Validate header parsing"""
    print("=== Test 1: Header Parsing ===")
    print(f"Format version: {header.format_version}")
    print(f"Scene UID: {header.scene_uid}")
    
    assert header.format_version == 3, f"Expected format=3, got {header.format_version}"
    assert header.scene_uid == "uid://bs256ppml668y", f"Expected uid://bs256ppml668y, got {header.scene_uid}"
    
    print("✓ PASSED\n")


def validate_ext_resources(ext_resources):
    """Validate external resource parsing"""
    print("=== Test 2: External Resources ===")
    print(f"Total ext_resources: {len(ext_resources)}")
    
    assert len(ext_resources) == 3, f"Expected 3 ext_resources, got {len(ext_resources)}"
    
    # Validate first ext_resource
    res1 = ext_resources[0]
    print(f"\nExtResource 1:")
    print(f"  type: {res1.resource_type}")
    print(f"  uid: {res1.uid}")
    print(f"  path: {res1.path}")
    print(f"  id: {res1.resource_id}")
    
    assert res1.resource_type == "PackedScene"
    assert res1.uid == "uid://dbaix0lcy10v2"
    assert res1.path == "res://A1UIScenes/UIComponents/SliderComponent.tscn"
    assert res1.resource_id == "1_scene"
    
    # Validate second ext_resource
    res2 = ext_resources[1]
    print(f"\nExtResource 2:")
    print(f"  type: {res2.resource_type}")
    print(f"  uid: {res2.uid}")
    print(f"  path: {res2.path}")
    print(f"  id: {res2.resource_id}")
    
    assert res2.resource_type == "PackedScene"
    assert res2.uid == "uid://dpf5ovda3xlpv"
    assert res2.path == "res://A1UIScenes/UIComponents/ToggleComponent.tscn"
    assert res2.resource_id == "2_scene"
    
    # Validate third ext_resource
    res3 = ext_resources[2]
    print(f"\nExtResource 3:")
    print(f"  type: {res3.resource_type}")
    print(f"  uid: {res3.uid}")
    print(f"  path: {res3.path}")
    print(f"  id: {res3.resource_id}")
    
    assert res3.resource_type == "PackedScene"
    assert res3.uid == "uid://0st2knyluaer"
    assert res3.path == "res://A1UIScenes/UIComponents/DropdownComponent.tscn"
    assert res3.resource_id == "3_scene"
    
    print("\n✓ PASSED\n")


def validate_nodes(nodes):
    """Validate node parsing"""
    print("=== Test 3: Node Parsing ===")
    print(f"Total nodes: {len(nodes)}")
    
    # Count expected nodes manually from the file
    # Root + Background + MainMargin + MainVBox + Tabs + Audio (6 nodes) + Video (8 nodes) + 
    # Controls (4 nodes) + Game (5 nodes) + ButtonsMargin + Buttons + BackButton + ResetButton
    # Let's just verify we have a reasonable number
    assert len(nodes) > 30, f"Expected at least 30 nodes, got {len(nodes)}"
    
    # Validate root node
    root = nodes[0]
    print(f"\nRoot node:")
    print(f"  name: {root.name}")
    print(f"  type: {root.node_type}")
    print(f"  unique_id: {root.unique_id}")
    print(f"  parent_path: {root.parent_path}")
    
    assert root.name == "SettingsMenuV2_Control"
    assert root.node_type == "Control"
    assert root.unique_id == 480540166
    assert root.parent_path == "."
    
    # Validate a child node
    background = nodes[1]
    print(f"\nSecond node (Background):")
    print(f"  name: {background.name}")
    print(f"  type: {background.node_type}")
    print(f"  unique_id: {background.unique_id}")
    print(f"  parent_path: {background.parent_path}")
    
    assert background.name == "Background_ColorRect"
    assert background.node_type == "ColorRect"
    assert background.unique_id == 1633307466
    assert background.parent_path == "."
    
    # Find and validate a scene instance node
    scene_instances = [n for n in nodes if n.is_instance]
    print(f"\nScene instances found: {len(scene_instances)}")
    assert len(scene_instances) > 0, "Expected at least one scene instance"
    
    # Check first scene instance (MasterVolume)
    master_volume = None
    for node in nodes:
        if node.name == "MasterVolume":
            master_volume = node
            break
    
    assert master_volume is not None, "MasterVolume node not found"
    print(f"\nScene instance (MasterVolume):")
    print(f"  name: {master_volume.name}")
    print(f"  is_instance: {master_volume.is_instance}")
    print(f"  unique_id: {master_volume.unique_id}")
    
    assert master_volume.is_instance == True
    assert master_volume.unique_id == 211444140
    
    print("\n✓ PASSED\n")


def validate_properties(nodes):
    """Validate property parsing with various types"""
    print("=== Test 4: Property Parsing ===")
    
    # Find Background node with Color property
    background = None
    for node in nodes:
        if node.name == "Background_ColorRect":
            background = node
            break
    
    assert background is not None, "Background_ColorRect not found"
    
    # Validate Color property
    color = background.properties.get("color")
    print(f"Color property: {color}")
    assert isinstance(color, Color), f"Expected Color type, got {type(color)}"
    assert color.r == 0.12
    assert color.g == 0.12
    assert color.b == 0.12
    assert color.a == 1.0
    print("✓ Color property parsed correctly")
    
    # Validate numeric properties
    layout_mode = background.properties.get("layout_mode")
    print(f"layout_mode: {layout_mode} (type: {type(layout_mode).__name__})")
    assert layout_mode == 1
    assert isinstance(layout_mode, int)
    print("✓ Integer property parsed correctly")
    
    anchor_right = background.properties.get("anchor_right")
    print(f"anchor_right: {anchor_right} (type: {type(anchor_right).__name__})")
    assert anchor_right == 1.0
    assert isinstance(anchor_right, float)
    print("✓ Float property parsed correctly")
    
    # Validate string property
    back_button = None
    for node in nodes:
        if node.name == "BackButton_Button":
            back_button = node
            break
    
    assert back_button is not None, "BackButton_Button not found"
    text = back_button.properties.get("text")
    print(f"text property: '{text}' (type: {type(text).__name__})")
    assert text == "Back"
    assert isinstance(text, str)
    print("✓ String property parsed correctly")
    
    # Validate boolean property
    audio_tab = None
    for node in nodes:
        if node.name == "Audio":
            audio_tab = node
            break
    
    assert audio_tab is not None, "Audio tab not found"
    visible = audio_tab.properties.get("visible")
    print(f"visible property: {visible} (type: {type(visible).__name__})")
    assert visible == False
    assert isinstance(visible, bool)
    print("✓ Boolean property parsed correctly")
    
    # Validate scene instance properties
    master_volume = None
    for node in nodes:
        if node.name == "MasterVolume":
            master_volume = node
            break
    
    assert master_volume is not None
    default_value = master_volume.properties.get("DefaultValue")
    print(f"DefaultValue property: {default_value} (type: {type(default_value).__name__})")
    assert default_value == 100.0
    print("✓ Scene instance property parsed correctly")
    
    label_text = master_volume.properties.get("LabelText")
    print(f"LabelText property: '{label_text}' (type: {type(label_text).__name__})")
    assert label_text == "Master"
    print("✓ Scene instance string property parsed correctly")
    
    print("\n✓ PASSED\n")


def validate_node_tree_indices(tree):
    """Validate Node_Tree index building and query methods"""
    print("=== Test 5: Node_Tree Indices and Queries ===")
    
    # Test get_root_nodes
    # In Godot .tscn format, nodes with parent="." are children of the root
    # Only nodes without a parent attribute are true root nodes
    root_nodes = tree.get_root_nodes()
    print(f"Root nodes (parent='.'): {len(root_nodes)}")
    for node in root_nodes:
        print(f"  - {node.name} (parent={node.parent_path})")
    
    # The first node should be the scene root
    assert len(root_nodes) >= 1, "Expected at least 1 root node"
    assert root_nodes[0].name == "SettingsMenuV2_Control"
    print("✓ get_root_nodes() works correctly")
    
    # Test get_node_by_path
    root = tree.get_node_by_path("SettingsMenuV2_Control")
    assert root is not None
    assert root.name == "SettingsMenuV2_Control"
    print("✓ get_node_by_path() for root works")
    
    background = tree.get_node_by_path("Background_ColorRect")
    assert background is not None
    assert background.name == "Background_ColorRect"
    print("✓ get_node_by_path() for child works")
    
    # Test nested path
    button = tree.get_node_by_path("MainMargin_MarginContainer/MainVBox_VBoxContainer/ButtonsMargin_MarginContainer/Buttons_HBoxContainer/BackButton_Button")
    assert button is not None
    assert button.name == "BackButton_Button"
    print("✓ get_node_by_path() for deeply nested node works")
    
    # Test get_nodes_by_type
    buttons = tree.get_nodes_by_type("Button")
    print(f"Button nodes: {len(buttons)}")
    assert len(buttons) == 2  # BackButton and ResetButton
    button_names = [b.name for b in buttons]
    assert "BackButton_Button" in button_names
    assert "ResetButton_Button" in button_names
    print("✓ get_nodes_by_type() works correctly")
    
    margin_containers = tree.get_nodes_by_type("MarginContainer")
    print(f"MarginContainer nodes: {len(margin_containers)}")
    assert len(margin_containers) > 5  # Multiple margin containers in the scene
    print("✓ get_nodes_by_type() for common type works")
    
    # Test get_children
    root_children = tree.get_children(".")
    print(f"Root children (parent='.'): {len(root_children)}")
    assert len(root_children) >= 1
    print("✓ get_children() for root works")
    
    main_vbox_children = tree.get_children("MainMargin_MarginContainer/MainVBox_VBoxContainer")
    print(f"MainVBox children: {len(main_vbox_children)}")
    assert len(main_vbox_children) == 2  # Tabs_TabContainer and ButtonsMargin_MarginContainer
    print("✓ get_children() for nested node works")
    
    # Test build_full_path
    full_path = tree.build_full_path(button)
    expected_path = "MainMargin_MarginContainer/MainVBox_VBoxContainer/ButtonsMargin_MarginContainer/Buttons_HBoxContainer/BackButton_Button"
    assert full_path == expected_path
    print(f"✓ build_full_path() works correctly")
    
    print("\n✓ PASSED\n")


def validate_scene_instances(tree):
    """Validate scene instance metadata resolution"""
    print("=== Test 6: Scene Instance Metadata ===")
    
    # Find MasterVolume scene instance
    master_volume = tree.get_node_by_path("MainMargin_MarginContainer/MainVBox_VBoxContainer/Tabs_TabContainer/Audio/AudioMargin_MarginContainer/AudioContent_VBoxContainer/MasterVolume")
    
    assert master_volume is not None, "MasterVolume not found"
    print(f"Node: {master_volume.name}")
    print(f"  is_instance: {master_volume.is_instance}")
    print(f"  scene_path: {master_volume.scene_path}")
    print(f"  scene_uid: {master_volume.scene_uid}")
    
    assert master_volume.is_instance == True
    assert master_volume.scene_path == "res://A1UIScenes/UIComponents/SliderComponent.tscn"
    assert master_volume.scene_uid == "uid://dbaix0lcy10v2"
    print("✓ Scene instance metadata resolved correctly")
    
    # Find AudioToggle (ToggleComponent instance)
    audio_toggle = tree.get_node_by_path("MainMargin_MarginContainer/MainVBox_VBoxContainer/Tabs_TabContainer/Audio/AudioMargin_MarginContainer/AudioContent_VBoxContainer/AudioToggle")
    
    assert audio_toggle is not None, "AudioToggle not found"
    print(f"\nNode: {audio_toggle.name}")
    print(f"  is_instance: {audio_toggle.is_instance}")
    print(f"  scene_path: {audio_toggle.scene_path}")
    print(f"  scene_uid: {audio_toggle.scene_uid}")
    
    assert audio_toggle.is_instance == True
    assert audio_toggle.scene_path == "res://A1UIScenes/UIComponents/ToggleComponent.tscn"
    assert audio_toggle.scene_uid == "uid://dpf5ovda3xlpv"
    print("✓ Second scene instance metadata resolved correctly")
    
    print("\n✓ PASSED\n")


def main():
    """Run all validation tests"""
    print("=" * 60)
    print("Task 4: Checkpoint - Validate Parser and Tree Construction")
    print("Testing with SettingsMenuV2.tscn")
    print("=" * 60)
    print()
    
    try:
        # Load file
        content = load_settings_menu()
        
        # Parse
        print("Parsing file...")
        parser = Parser(content)
        header, ext_resources, nodes = parser.parse()
        print("✓ Parsing completed\n")
        
        # Create Node_Tree
        print("Building Node_Tree...")
        tree = Node_Tree(header=header, ext_resources=ext_resources, nodes=nodes)
        print("✓ Node_Tree built\n")
        
        # Run validation tests
        validate_header(header)
        validate_ext_resources(ext_resources)
        validate_nodes(nodes)
        validate_properties(nodes)
        validate_node_tree_indices(tree)
        validate_scene_instances(tree)
        
        # Summary
        print("=" * 60)
        print("✓✓✓ ALL VALIDATION TESTS PASSED ✓✓✓")
        print("=" * 60)
        print()
        print("Summary:")
        print(f"  - Header: format={header.format_version}, uid={header.scene_uid}")
        print(f"  - External Resources: {len(ext_resources)}")
        print(f"  - Nodes: {len(nodes)}")
        print(f"  - Scene Instances: {len([n for n in nodes if n.is_instance])}")
        print(f"  - Node Types: {len(tree._nodes_by_type)}")
        print()
        print("Parser and Node_Tree are working correctly!")
        
    except Exception as e:
        print(f"\n✗✗✗ VALIDATION FAILED ✗✗✗")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
