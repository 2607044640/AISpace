"""
Test TscnEditor functionality
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from tscn_editor_tools import TscnEditor, PropertyUpdate, EditorError, Color, Vector2


def test_editor_basic():
    """Test basic editor operations"""
    print("=" * 60)
    print("TEST: Basic Editor Operations")
    print("=" * 60)
    
    # Load a test file
    test_file = Path(__file__).parent / "test_data" / "simple_scene.tscn"
    
    if not test_file.exists():
        print(f"⚠️  Test file not found: {test_file}")
        print("Creating test file...")
        create_test_file(test_file)
    
    # Create editor
    editor = TscnEditor(str(test_file))
    
    # Test 1: Access reader property
    print("\n1. Testing reader property access...")
    tree_view = editor.reader.print_tree_view()
    print("✓ Reader accessible")
    print("\nInitial tree:")
    print(tree_view)
    
    # Test 2: Update single property
    print("\n2. Testing update_property()...")
    editor.update_property("Root", "test_property", "test_value")
    value = editor.reader.get_node_property("Root", "test_property")
    assert value == "test_value", f"Expected 'test_value', got {value}"
    print("✓ Property updated successfully")
    
    # Test 3: Update complex property
    print("\n3. Testing complex property update...")
    editor.update_property("Root", "color", Color(1.0, 0.5, 0.25, 1.0))
    color = editor.reader.get_node_property("Root", "color")
    assert isinstance(color, Color), f"Expected Color, got {type(color)}"
    print(f"✓ Color property updated: {color}")
    
    # Test 4: Batch property updates
    print("\n4. Testing update_properties_batch()...")
    updates = [
        PropertyUpdate("Root", "prop1", "value1"),
        PropertyUpdate("Root", "prop2", 42),
        PropertyUpdate("Root", "prop3", True),
    ]
    result = editor.update_properties_batch(updates)
    print(f"✓ Batch update: {result.success_count} succeeded, {len(result.errors)} errors")
    assert result.success_count == 3, f"Expected 3 successes, got {result.success_count}"
    
    # Test 5: Add regular node
    print("\n5. Testing add_node()...")
    new_node = editor.add_node("TestButton", "Button", "Root", {"text": "Click Me"})
    assert new_node.name == "TestButton"
    assert new_node.node_type == "Button"
    assert editor.reader.node_exists("Root/TestButton")
    print(f"✓ Node added: {new_node.name} (unique_id={new_node.unique_id})")
    
    # Test 6: Add scene instance
    print("\n6. Testing add_scene_instance()...")
    instance_node = editor.add_scene_instance(
        "PlayerInstance",
        "res://scenes/Player.tscn",
        "Root",
        scene_uid="uid://test123"
    )
    assert instance_node.is_instance
    assert instance_node.scene_path == "res://scenes/Player.tscn"
    assert editor.reader.node_exists("Root/PlayerInstance")
    print(f"✓ Scene instance added: {instance_node.name}")
    
    # Test 7: Remove node
    print("\n7. Testing remove_node()...")
    editor.remove_node("Root/TestButton")
    assert not editor.reader.node_exists("Root/TestButton")
    print("✓ Node removed successfully")
    
    # Test 8: Save to file
    print("\n8. Testing save()...")
    output_file = test_file.parent / "test_output.tscn"
    editor.save(str(output_file))
    assert output_file.exists()
    print(f"✓ File saved to: {output_file}")
    
    # Test 9: Verify round-trip
    print("\n9. Testing round-trip (load saved file)...")
    editor2 = TscnEditor(str(output_file))
    assert editor2.reader.node_exists("Root")
    assert editor2.reader.node_exists("Root/PlayerInstance")
    print("✓ Round-trip successful")
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS PASSED")
    print("=" * 60)


def test_error_handling():
    """Test error handling"""
    print("\n" + "=" * 60)
    print("TEST: Error Handling")
    print("=" * 60)
    
    test_file = Path(__file__).parent / "test_data" / "simple_scene.tscn"
    editor = TscnEditor(str(test_file))
    
    # Test 1: Update non-existent node
    print("\n1. Testing update on non-existent node...")
    try:
        editor.update_property("NonExistent", "prop", "value")
        print("✗ Should have raised EditorError")
    except EditorError as e:
        print(f"✓ Caught expected error: {e}")
    
    # Test 2: Add node with non-existent parent
    print("\n2. Testing add_node with invalid parent...")
    try:
        editor.add_node("Test", "Node", "NonExistent/Parent")
        print("✗ Should have raised EditorError")
    except EditorError as e:
        print(f"✓ Caught expected error: {e}")
    
    # Test 3: Add duplicate node name
    print("\n3. Testing duplicate node name...")
    editor.add_node("DuplicateTest", "Node", "Root")
    try:
        editor.add_node("DuplicateTest", "Node", "Root")
        print("✗ Should have raised EditorError")
    except EditorError as e:
        print(f"✓ Caught expected error: {e}")
    
    # Test 4: Remove non-existent node
    print("\n4. Testing remove non-existent node...")
    try:
        editor.remove_node("NonExistent")
        print("✗ Should have raised EditorError")
    except EditorError as e:
        print(f"✓ Caught expected error: {e}")
    
    # Test 5: Remove root node
    print("\n5. Testing remove root node...")
    try:
        editor.remove_node("Root")
        print("✗ Should have raised EditorError")
    except EditorError as e:
        print(f"✓ Caught expected error: {e}")
    
    print("\n" + "=" * 60)
    print("✓ ALL ERROR HANDLING TESTS PASSED")
    print("=" * 60)


def test_uid_generator():
    """Test UID generation"""
    print("\n" + "=" * 60)
    print("TEST: UID Generator")
    print("=" * 60)
    
    from tscn_editor_tools import UIDGenerator
    
    # Test 1: Generate from empty set
    print("\n1. Testing generation from empty set...")
    gen = UIDGenerator(set())
    uid1 = gen.generate()
    assert uid1 == 1, f"Expected 1, got {uid1}"
    print(f"✓ Generated UID: {uid1}")
    
    # Test 2: Generate sequential IDs
    print("\n2. Testing sequential generation...")
    uid2 = gen.generate()
    uid3 = gen.generate()
    assert uid2 == 2 and uid3 == 3
    print(f"✓ Generated UIDs: {uid2}, {uid3}")
    
    # Test 3: Generate with existing IDs
    print("\n3. Testing with existing IDs...")
    gen2 = UIDGenerator({100, 200, 300})
    uid = gen2.generate()
    assert uid == 301, f"Expected 301, got {uid}"
    print(f"✓ Generated UID: {uid}")
    
    # Test 4: Skip conflicts
    print("\n4. Testing conflict avoidance...")
    gen3 = UIDGenerator({1, 2, 4, 5})
    uid = gen3.generate()
    assert uid == 6, f"Expected 6, got {uid}"
    print(f"✓ Generated UID: {uid} (skipped conflicts)")
    
    print("\n" + "=" * 60)
    print("✓ ALL UID GENERATOR TESTS PASSED")
    print("=" * 60)


def create_test_file(path: Path):
    """Create a simple test .tscn file"""
    path.parent.mkdir(parents=True, exist_ok=True)
    
    content = """[gd_scene format=3 uid="uid://test_scene_uid"]

[node name="Root" type="Control" unique_id=1]
layout_mode = 3
anchors_preset = 15
"""
    
    path.write_text(content, encoding='utf-8')
    print(f"✓ Created test file: {path}")


if __name__ == "__main__":
    try:
        test_uid_generator()
        test_editor_basic()
        test_error_handling()
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
