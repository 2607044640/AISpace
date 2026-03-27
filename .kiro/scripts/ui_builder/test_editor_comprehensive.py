"""
Comprehensive test of TscnEditor with real scene files
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from tscn_editor_tools import TscnEditor, PropertyUpdate, Color, Vector2


def test_with_real_scene():
    """Test with a real scene file from the project"""
    print("=" * 60)
    print("TEST: Real Scene File Operations")
    print("=" * 60)
    
    # Find a real .tscn file to test with
    test_scenes = [
        "A1UIScenes/UIComponents/SliderComponent.tscn",
        "A1UIScenes/Menus/SettingsMenuV2_Control.tscn",
    ]
    
    test_file = None
    for scene_path in test_scenes:
        full_path = Path(__file__).parent.parent.parent.parent / scene_path
        if full_path.exists():
            test_file = full_path
            break
    
    if test_file is None:
        print("⚠️  No real scene files found, skipping test")
        return
    
    print(f"\nUsing test file: {test_file.name}")
    
    # Create editor
    editor = TscnEditor(str(test_file))
    
    # Test 1: Display initial tree
    print("\n1. Initial scene structure:")
    print("-" * 60)
    tree_view = editor.reader.print_tree_view()
    print(tree_view)
    
    # Test 2: Query nodes
    print("\n2. Querying nodes...")
    all_nodes = editor.reader.tree.nodes
    print(f"   Total nodes: {len(all_nodes)}")
    
    # Count by type
    type_counts = {}
    for node in all_nodes:
        type_counts[node.node_type] = type_counts.get(node.node_type, 0) + 1
    
    print("   Node types:")
    for node_type, count in sorted(type_counts.items()):
        print(f"     - {node_type}: {count}")
    
    # Test 3: Find specific nodes
    print("\n3. Finding specific nodes...")
    buttons = editor.reader.find_nodes_by_type("Button")
    labels = editor.reader.find_nodes_by_type("Label")
    print(f"   Buttons found: {len(buttons)}")
    print(f"   Labels found: {len(labels)}")
    
    # Test 4: Add a new node to the scene
    print("\n4. Adding new test node...")
    root_nodes = editor.reader.tree.get_root_nodes()
    if root_nodes:
        root_path = root_nodes[0].name
        new_node = editor.add_node(
            "TestLabel",
            "Label",
            root_path,
            {"text": "Test Label", "visible": False}
        )
        print(f"   ✓ Added: {new_node.name} (unique_id={new_node.unique_id})")
    
    # Test 5: Update properties on existing nodes
    print("\n5. Updating properties...")
    if labels:
        label_path = editor.reader.tree.build_full_path(labels[0])
        original_text = labels[0].properties.get("text", "N/A")
        print(f"   Original text: {original_text}")
        
        editor.update_property(label_path, "text", "Modified Text")
        new_text = editor.reader.get_node_property(label_path, "text")
        print(f"   Updated text: {new_text}")
    
    # Test 6: Save to temporary file
    print("\n6. Saving modified scene...")
    output_file = test_file.parent / f"{test_file.stem}_modified.tscn"
    editor.save(str(output_file))
    print(f"   ✓ Saved to: {output_file}")
    
    # Test 7: Verify round-trip
    print("\n7. Verifying round-trip...")
    editor2 = TscnEditor(str(output_file))
    new_tree_view = editor2.reader.print_tree_view()
    
    # Check that TestLabel exists
    if editor2.reader.node_exists(f"{root_path}/TestLabel"):
        print("   ✓ New node persisted correctly")
    else:
        print("   ✗ New node not found after round-trip")
    
    # Check node count
    if len(editor2.reader.tree.nodes) == len(all_nodes) + 1:
        print(f"   ✓ Node count correct: {len(editor2.reader.tree.nodes)}")
    else:
        print(f"   ✗ Node count mismatch: expected {len(all_nodes) + 1}, got {len(editor2.reader.tree.nodes)}")
    
    print("\n" + "=" * 60)
    print("✓ REAL SCENE TEST COMPLETED")
    print("=" * 60)


def test_batch_operations():
    """Test batch operations on multiple nodes"""
    print("\n" + "=" * 60)
    print("TEST: Batch Operations")
    print("=" * 60)
    
    # Create a test scene with multiple nodes
    test_file = Path(__file__).parent / "test_data" / "batch_test.tscn"
    create_batch_test_file(test_file)
    
    editor = TscnEditor(str(test_file))
    
    print("\n1. Initial scene:")
    print(editor.reader.print_tree_view())
    
    # Test batch updates
    print("\n2. Performing batch updates...")
    updates = [
        PropertyUpdate("Root/Button1", "text", "Updated Button 1"),
        PropertyUpdate("Root/Button2", "text", "Updated Button 2"),
        PropertyUpdate("Root/Button3", "text", "Updated Button 3"),
        PropertyUpdate("Root/Label1", "text", "Updated Label"),
    ]
    
    result = editor.update_properties_batch(updates)
    print(f"   ✓ Batch update: {result.success_count} succeeded")
    if result.errors:
        print(f"   Errors: {result.errors}")
    
    # Verify updates
    print("\n3. Verifying updates...")
    for update in updates:
        value = editor.reader.get_node_property(update.node_path, update.property_key)
        if value == update.property_value:
            print(f"   ✓ {update.node_path}: {value}")
        else:
            print(f"   ✗ {update.node_path}: expected {update.property_value}, got {value}")
    
    print("\n" + "=" * 60)
    print("✓ BATCH OPERATIONS TEST COMPLETED")
    print("=" * 60)


def test_recursive_removal():
    """Test recursive node removal"""
    print("\n" + "=" * 60)
    print("TEST: Recursive Node Removal")
    print("=" * 60)
    
    # Create a test scene with nested nodes
    test_file = Path(__file__).parent / "test_data" / "nested_test.tscn"
    create_nested_test_file(test_file)
    
    editor = TscnEditor(str(test_file))
    
    print("\n1. Initial scene:")
    print(editor.reader.print_tree_view())
    
    initial_count = len(editor.reader.tree.nodes)
    print(f"\n   Initial node count: {initial_count}")
    
    # Remove a parent node (should remove all children)
    print("\n2. Removing 'Root/Container' (should remove all children)...")
    editor.remove_node("Root/Container")
    
    final_count = len(editor.reader.tree.nodes)
    print(f"   Final node count: {final_count}")
    print(f"   Removed: {initial_count - final_count} nodes")
    
    print("\n3. Final scene:")
    print(editor.reader.print_tree_view())
    
    # Verify children are gone
    if not editor.reader.node_exists("Root/Container"):
        print("\n   ✓ Parent removed")
    if not editor.reader.node_exists("Root/Container/Child1"):
        print("   ✓ Child1 removed")
    if not editor.reader.node_exists("Root/Container/Child1/GrandChild"):
        print("   ✓ GrandChild removed")
    
    print("\n" + "=" * 60)
    print("✓ RECURSIVE REMOVAL TEST COMPLETED")
    print("=" * 60)


def create_batch_test_file(path: Path):
    """Create a test file with multiple nodes"""
    path.parent.mkdir(parents=True, exist_ok=True)
    
    content = """[gd_scene format=3 uid="uid://batch_test"]

[node name="Root" type="Control" unique_id=1]

[node name="Button1" type="Button" parent="Root" unique_id=2]
text = "Button 1"

[node name="Button2" type="Button" parent="Root" unique_id=3]
text = "Button 2"

[node name="Button3" type="Button" parent="Root" unique_id=4]
text = "Button 3"

[node name="Label1" type="Label" parent="Root" unique_id=5]
text = "Label"
"""
    
    path.write_text(content, encoding='utf-8')


def create_nested_test_file(path: Path):
    """Create a test file with nested nodes"""
    path.parent.mkdir(parents=True, exist_ok=True)
    
    content = """[gd_scene format=3 uid="uid://nested_test"]

[node name="Root" type="Control" unique_id=1]

[node name="Container" type="VBoxContainer" parent="Root" unique_id=2]

[node name="Child1" type="Button" parent="Root/Container" unique_id=3]
text = "Child 1"

[node name="Child2" type="Button" parent="Root/Container" unique_id=4]
text = "Child 2"

[node name="GrandChild" type="Label" parent="Root/Container/Child1" unique_id=5]
text = "Grand Child"
"""
    
    path.write_text(content, encoding='utf-8')


if __name__ == "__main__":
    try:
        test_with_real_scene()
        test_batch_operations()
        test_recursive_removal()
        
        print("\n" + "=" * 60)
        print("🎉 ALL COMPREHENSIVE TESTS COMPLETED SUCCESSFULLY")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
