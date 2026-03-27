"""
Example usage of TscnReader for querying .tscn files
"""

import sys
from pathlib import Path

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from tscn_editor_tools import TscnReader


def main():
    """Demonstrate TscnReader usage"""
    
    # Load a .tscn file
    tscn_path = "c:/Godot/3d-practice/A1UIScenes/SettingsMenuV2.tscn"
    
    if not Path(tscn_path).exists():
        print(f"File not found: {tscn_path}")
        print("Please update the path to a valid .tscn file")
        return
    
    print("=" * 60)
    print("TscnReader Usage Examples")
    print("=" * 60 + "\n")
    
    # Initialize reader
    reader = TscnReader(tscn_path)
    print(f"Loaded: {Path(tscn_path).name}\n")
    
    # Example 1: Find all buttons
    print("Example 1: Find all Button nodes")
    buttons = reader.find_nodes_by_type("Button")
    for btn in buttons:
        text = btn.properties.get("text", "(no text)")
        print(f"  - {btn.name}: '{text}'")
    print()
    
    # Example 2: Find nodes by name
    print("Example 2: Find node by name")
    nodes = reader.find_nodes_by_name("BackButton_Button")
    if nodes:
        node = nodes[0]
        print(f"  Found: {node.name} ({node.node_type})")
        print(f"  Text: {node.properties.get('text', 'N/A')}")
    print()
    
    # Example 3: Check if node exists
    print("Example 3: Check if node path exists")
    path = "SettingsMenuV2_Control/MainMargin_MarginContainer"
    exists = reader.node_exists(path)
    print(f"  Path '{path}': {exists}")
    print()
    
    # Example 4: Get node property
    print("Example 4: Get specific property")
    color = reader.get_node_property("SettingsMenuV2_Control/Background_ColorRect", "color")
    print(f"  Background color: {color}")
    print()
    
    # Example 5: Count nodes by type
    print("Example 5: Node type statistics")
    for node_type in ["Button", "Label", "MarginContainer", "VBoxContainer"]:
        count = reader.get_node_count_by_type(node_type)
        print(f"  {node_type}: {count}")
    print()
    
    # Example 6: List external resources
    print("Example 6: External resources")
    ext_resources = reader.list_ext_resources()
    for res in ext_resources:
        print(f"  - {res.resource_type}: {Path(res.path).name}")
    print()
    
    # Example 7: Find scene instances
    print("Example 7: Find scene instances")
    instances = [node for node in reader.tree.nodes if node.is_instance]
    print(f"  Found {len(instances)} scene instances:")
    for inst in instances[:5]:
        print(f"  - {inst.name}: {Path(inst.scene_path).name if inst.scene_path else 'N/A'}")
    print()
    
    # Example 8: Print tree view
    print("Example 8: Tree visualization (first 30 lines)")
    print("-" * 60)
    tree_view = reader.print_tree_view()
    lines = tree_view.split('\n')
    for line in lines[:30]:
        print(line)
    if len(lines) > 30:
        print(f"... and {len(lines) - 30} more lines")
    print("-" * 60)


if __name__ == "__main__":
    main()
