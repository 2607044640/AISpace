# TscnEditor Usage Guide

## Overview

The TscnEditor provides a safe, programmatic way to modify Godot .tscn scene files while preserving all UIDs, formatting, and references.

## Basic Usage

```python
from tscn_editor_tools import TscnEditor, PropertyUpdate, Color, Vector2

# Load a scene file
editor = TscnEditor("path/to/scene.tscn")

# Access read-only query interface
tree_view = editor.reader.print_tree_view()
print(tree_view)

# Update a single property
editor.update_property("Root/Button", "text", "Click Me!")

# Update multiple properties
updates = [
    PropertyUpdate("Root/Button1", "text", "Button 1"),
    PropertyUpdate("Root/Button2", "text", "Button 2"),
    PropertyUpdate("Root/Label", "text", "Label Text"),
]
result = editor.update_properties_batch(updates)
print(f"Updated {result.success_count} properties")

# Add a new node
new_node = editor.add_node(
    name="NewButton",
    node_type="Button",
    parent_path="Root",
    properties={"text": "New Button", "visible": True}
)

# Add a scene instance
instance = editor.add_scene_instance(
    name="PlayerInstance",
    scene_path="res://scenes/Player.tscn",
    parent_path="Root",
    scene_uid="uid://abc123"
)

# Remove a node (and all children)
editor.remove_node("Root/OldButton")

# Save changes
editor.save()  # Saves to original file
# or
editor.save("path/to/output.tscn")  # Save to different file
```

## Query Operations

```python
# Check if node exists
if editor.reader.node_exists("Root/Button"):
    print("Button exists")

# Find nodes by type
buttons = editor.reader.find_nodes_by_type("Button")
for button in buttons:
    print(f"Found button: {button.name}")

# Find nodes by name
nodes = editor.reader.find_nodes_by_name("MyButton")

# Find nodes by property
red_nodes = editor.reader.find_nodes_by_property("color", Color(1, 0, 0, 1))

# Get node property
text = editor.reader.get_node_property("Root/Label", "text")

# Get all properties
props = editor.reader.get_node_properties("Root/Button")
```

## Complex Property Types

```python
from tscn_editor_tools import Color, Vector2, NodePath

# Update color property
editor.update_property("Root/ColorRect", "color", Color(1.0, 0.5, 0.25, 1.0))

# Update vector property
editor.update_property("Root/Node2D", "position", Vector2(100, 200))

# Update node path property
editor.update_property("Root/Button", "focus_neighbor_left", NodePath("../OtherButton"))
```

## Error Handling

```python
from tscn_editor_tools import EditorError

try:
    editor.update_property("NonExistent", "prop", "value")
except EditorError as e:
    print(f"Error: {e}")

try:
    editor.add_node("Duplicate", "Node", "Root")
    editor.add_node("Duplicate", "Node", "Root")  # Raises EditorError
except EditorError as e:
    print(f"Cannot add duplicate: {e}")
```

## UID Generation

The editor automatically generates unique IDs for new nodes:

```python
from tscn_editor_tools import UIDGenerator

# Manual UID generation (rarely needed)
existing_ids = {1, 2, 3, 100, 200}
generator = UIDGenerator(existing_ids)

new_id = generator.generate()  # Returns 201
```

## Best Practices

1. **Always use the reader property for queries** - Don't modify the tree directly
2. **Batch updates when possible** - More efficient than multiple single updates
3. **Validate before removing** - Check node exists and isn't a root node
4. **Save to a different file first** - Test changes before overwriting originals
5. **Use try-except for error handling** - Catch EditorError for invalid operations

## Integration Example

```python
def update_all_button_texts(scene_path: str, new_text: str):
    """Update all button texts in a scene"""
    editor = TscnEditor(scene_path)
    
    # Find all buttons
    buttons = editor.reader.find_nodes_by_type("Button")
    
    # Create batch updates
    updates = []
    for button in buttons:
        button_path = editor.reader.tree.build_full_path(button)
        updates.append(PropertyUpdate(button_path, "text", new_text))
    
    # Apply updates
    result = editor.update_properties_batch(updates)
    
    # Save changes
    editor.save()
    
    return result.success_count

# Usage
count = update_all_button_texts("scenes/menu.tscn", "Click Here")
print(f"Updated {count} buttons")
```

## Testing

Run the test suite to verify functionality:

```bash
# Basic tests
python .kiro/scripts/ui_builder/test_editor.py

# Comprehensive tests
python .kiro/scripts/ui_builder/test_editor_comprehensive.py

# Real scene file tests
python .kiro/scripts/ui_builder/test_editor_real_scene.py
```

## Architecture

- **TscnEditor**: Main modification interface
- **TscnReader**: Read-only query interface (accessed via `editor.reader`)
- **UIDGenerator**: Generates unique IDs for new nodes
- **Pretty_Printer**: Formats Node_Tree back to .tscn text
- **Parser**: Converts .tscn text to Node_Tree (used internally)

All modifications preserve:
- Node unique_id values (except for new nodes)
- Scene UID in file header
- External resource UIDs
- Property formatting (Color, Vector2, etc.)
- Node order and hierarchy
