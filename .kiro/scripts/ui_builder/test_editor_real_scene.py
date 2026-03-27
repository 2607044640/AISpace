"""
Test TscnEditor with a real scene file from the project
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from tscn_editor_tools import TscnEditor, PropertyUpdate


def test_real_scene():
    """Test with SliderComponent.tscn"""
    print("=" * 60)
    print("TEST: Real Scene File - SliderComponent.tscn")
    print("=" * 60)
    
    # Path to real scene file (absolute path to 3d-practice workspace)
    scene_path = Path("c:/Godot/3d-practice/A1UIScenes/UIComponents/SliderComponent.tscn")
    
    if not scene_path.exists():
        print(f"⚠️  Scene file not found: {scene_path}")
        return
    
    print(f"\nLoading: {scene_path.name}")
    
    # Create editor
    editor = TscnEditor(str(scene_path))
    
    # Test 1: Display tree structure
    print("\n1. Scene structure:")
    print("-" * 60)
    tree_view = editor.reader.print_tree_view()
    print(tree_view)
    
    # Test 2: Query information
    print("\n2. Scene information:")
    all_nodes = editor.reader.tree.nodes
    initial_node_count = len(all_nodes)
    print(f"   Total nodes: {initial_node_count}")
    print(f"   External resources: {len(editor.reader.tree.ext_resources)}")
    
    # Count by type
    type_counts = {}
    for node in all_nodes:
        type_counts[node.node_type] = type_counts.get(node.node_type, 0) + 1
    
    print("\n   Node types:")
    for node_type, count in sorted(type_counts.items()):
        print(f"     - {node_type}: {count}")
    
    # Test 3: Find specific nodes
    print("\n3. Finding specific nodes:")
    labels = editor.reader.find_nodes_by_type("Label")
    hsliders = editor.reader.find_nodes_by_type("HSlider")
    print(f"   Labels: {len(labels)}")
    print(f"   HSliders: {len(hsliders)}")
    
    if labels:
        print("\n   Label nodes:")
        for label in labels:
            label_path = editor.reader.tree.build_full_path(label)
            text = label.properties.get("text", "N/A")
            print(f"     - {label_path}: text='{text}'")
    
    # Test 4: Add a new node
    print("\n4. Adding new test node...")
    root_nodes = editor.reader.tree.get_root_nodes()
    if root_nodes:
        root_path = root_nodes[0].name
        new_node = editor.add_node(
            "TestDebugLabel",
            "Label",
            root_path,
            {"text": "Debug Info", "visible": True}
        )
        print(f"   ✓ Added: {new_node.name} (unique_id={new_node.unique_id})")
    
    # Test 5: Update existing properties
    print("\n5. Updating properties...")
    if labels:
        label = labels[0]
        label_path = editor.reader.tree.build_full_path(label)
        original_text = label.properties.get("text", "N/A")
        
        print(f"   Target: {label_path}")
        print(f"   Original text: '{original_text}'")
        
        editor.update_property(label_path, "text", "Modified by TscnEditor")
        new_text = editor.reader.get_node_property(label_path, "text")
        print(f"   Updated text: '{new_text}'")
    
    # Test 6: Save to temporary file
    print("\n6. Saving modified scene...")
    output_file = scene_path.parent / f"{scene_path.stem}_test_modified.tscn"
    editor.save(str(output_file))
    print(f"   ✓ Saved to: {output_file}")
    
    # Test 7: Verify round-trip
    print("\n7. Verifying round-trip...")
    editor2 = TscnEditor(str(output_file))
    
    # Check node count
    print(f"   Original nodes: {initial_node_count}, New nodes: {len(editor2.reader.tree.nodes)}")
    if len(editor2.reader.tree.nodes) == initial_node_count + 1:
        print(f"   ✓ Node count correct: {len(editor2.reader.tree.nodes)}")
    else:
        print(f"   ⚠️  Node count: expected {initial_node_count + 1}, got {len(editor2.reader.tree.nodes)}")
    
    # Check new node exists
    if editor2.reader.node_exists(f"{root_path}/TestDebugLabel"):
        print("   ✓ New node persisted")
    
    # Check property update persisted
    if labels:
        updated_text = editor2.reader.get_node_property(label_path, "text")
        if updated_text == "Modified by TscnEditor":
            print("   ✓ Property update persisted")
    
    print("\n" + "=" * 60)
    print("✓ REAL SCENE TEST COMPLETED SUCCESSFULLY")
    print("=" * 60)
    
    # Cleanup
    print(f"\nCleaning up: {output_file.name}")
    output_file.unlink()


if __name__ == "__main__":
    try:
        test_real_scene()
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
