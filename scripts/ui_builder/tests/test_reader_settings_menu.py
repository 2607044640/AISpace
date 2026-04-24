"""
Test TscnReader with SettingsMenuV2.tscn from 3d-practice
"""

import sys
from pathlib import Path

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from tscn_editor_tools.reader import TscnReader


def test_settings_menu():
    """Test TscnReader with SettingsMenuV2.tscn"""
    
    # Use absolute path to 3d-practice workspace
    tscn_path = "c:/Godot/3d-practice/A1UIScenes/SettingsMenuV2.tscn"
    
    if not Path(tscn_path).exists():
        print(f"File not found: {tscn_path}")
        print("Skipping test")
        return
    
    print("=" * 60)
    print("Testing TscnReader with SettingsMenuV2.tscn")
    print("=" * 60 + "\n")
    
    try:
        # Load the file
        reader = TscnReader(tscn_path)
        print(f"✓ Successfully loaded SettingsMenuV2.tscn")
        print(f"  Format: {reader.tree.header.format_version}")
        print(f"  Scene UID: {reader.tree.header.scene_uid}")
        print()
        
        # List external resources
        ext_resources = reader.list_ext_resources()
        print(f"External Resources: {len(ext_resources)}")
        for res in ext_resources[:5]:  # Show first 5
            print(f"  - {res.resource_type}: {Path(res.path).name}")
        if len(ext_resources) > 5:
            print(f"  ... and {len(ext_resources) - 5} more")
        print()
        
        # Count nodes by type
        print("Node Type Statistics:")
        node_types = set(node.node_type for node in reader.tree.nodes)
        for node_type in sorted(node_types):
            count = reader.get_node_count_by_type(node_type)
            print(f"  - {node_type}: {count}")
        print()
        
        # Find specific nodes
        print("Finding Button nodes:")
        buttons = reader.find_nodes_by_type("Button")
        for btn in buttons[:5]:  # Show first 5
            text = btn.properties.get("text", "(no text)")
            print(f"  - {btn.name}: {text}")
        if len(buttons) > 5:
            print(f"  ... and {len(buttons) - 5} more")
        print()
        
        # Print tree view (first 50 lines)
        print("Tree View (first 50 lines):")
        print("-" * 60)
        tree_view = reader.print_tree_view()
        lines = tree_view.split('\n')
        for line in lines[:50]:
            print(line)
        if len(lines) > 50:
            print(f"... and {len(lines) - 50} more lines")
        print("-" * 60)
        print()
        
        print("✓ All operations completed successfully!")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    test_settings_menu()
