"""
Pretty_Printer: Converts Node_Tree back to .tscn text format
"""

from typing import Any
from .node_tree import Node_Tree
from .types import Header, ExtResource, Node, Color, Vector2, NodePath, ExtResourceRef


class Pretty_Printer:
    """
    Formats Node_Tree back into valid .tscn text format.
    
    Preserves:
    - Original formatting for property values (Color, Vector2, etc.)
    - Node order from Node_Tree
    - UIDs and references
    - Blank lines between sections for readability
    """
    
    def print_tree(self, tree: Node_Tree) -> str:
        """
        Convert Node_Tree to .tscn text format.
        
        Args:
            tree: The Node_Tree to format
            
        Returns:
            Valid .tscn text content
        """
        lines = []
        
        # Print header
        lines.append(self._print_header(tree.header))
        lines.append("")  # Blank line after header
        
        # Print external resources
        for ext_resource in tree.ext_resources:
            lines.append(self._print_ext_resource(ext_resource))
        
        # Blank line after ext_resources (if any)
        if tree.ext_resources:
            lines.append("")
        
        # Print nodes with blank lines between them
        for i, node in enumerate(tree.nodes):
            is_first_node = (i == 0)
            lines.append(self._print_node(node, is_first_node))
            # Add blank line after each node (except the last one)
            if i < len(tree.nodes) - 1:
                lines.append("")
        
        return "\n".join(lines)
    
    def _print_header(self, header: Header) -> str:
        """
        Format scene header.
        
        Format: [gd_scene format=3 uid="uid://..."]
        
        Args:
            header: The Header to format
            
        Returns:
            Formatted header line
        """
        return f'[gd_scene format={header.format_version} uid="{header.scene_uid}"]'
    
    def _print_ext_resource(self, resource: ExtResource) -> str:
        """
        Format external resource declaration.
        
        Format: [ext_resource type="..." uid="..." path="..." id="..."]
        
        Args:
            resource: The ExtResource to format
            
        Returns:
            Formatted ext_resource line
        """
        return (
            f'[ext_resource type="{resource.resource_type}" '
            f'uid="{resource.uid}" '
            f'path="{resource.path}" '
            f'id="{resource.resource_id}"]'
        )
    
    def _print_node(self, node: Node, is_first_node: bool = False) -> str:
        """
        Format node section with properties.
        
        Formats:
        - First node (root): [node name="..." type="..." unique_id=...] (no parent attribute)
        - Child nodes with parent=".": [node name="..." type="..." parent="." unique_id=...]
        - Other child nodes: [node name="..." type="..." parent="path" unique_id=...]
        - Scene instance: [node name="..." type="..." parent="..." instance=ExtResource("...") unique_id=...]
        
        Args:
            node: The Node to format
            is_first_node: True if this is the first node in the tree (root node)
            
        Returns:
            Formatted node section (header + properties)
        """
        lines = []
        
        # Build node header attributes
        attrs = [f'name="{node.name}"']
        
        # Add type attribute
        attrs.append(f'type="{node.node_type}"')
        
        # Add parent attribute (skip only for the first node in the file)
        if not is_first_node:
            attrs.append(f'parent="{node.parent_path}"')
        
        # Add instance attribute for scene instances
        if node.is_instance and '_instance_resource_id' in node.properties:
            resource_id = node.properties['_instance_resource_id']
            attrs.append(f'instance=ExtResource("{resource_id}")')
        
        # Add unique_id attribute
        attrs.append(f'unique_id={node.unique_id}')
        
        # Format node header
        node_header = f'[node {" ".join(attrs)}]'
        lines.append(node_header)
        
        # Format properties (excluding internal metadata)
        for key, value in node.properties.items():
            # Skip internal metadata properties
            if key.startswith('_'):
                continue
            
            property_line = self._print_property(key, value)
            lines.append(property_line)
        
        return "\n".join(lines)
    
    def _print_property(self, key: str, value: Any) -> str:
        """
        Format property as key = value.
        
        Handles:
        - Strings: "value"
        - Numbers: 123, 45.6
        - Booleans: true, false
        - Color: Color(r, g, b, a)
        - Vector2: Vector2(x, y)
        - NodePath: NodePath("path")
        - ExtResource: ExtResource("id")
        
        Args:
            key: Property key
            value: Property value (any type)
            
        Returns:
            Formatted property line
        """
        formatted_value = self._format_value(value)
        return f"{key} = {formatted_value}"
    
    def _format_value(self, value: Any) -> str:
        """
        Format a property value with correct syntax.
        
        Args:
            value: The value to format
            
        Returns:
            Formatted value string
        """
        # Handle special types with __str__ methods
        if isinstance(value, (Color, Vector2, NodePath, ExtResourceRef)):
            return str(value)
        
        # Handle strings
        if isinstance(value, str):
            return f'"{value}"'
        
        # Handle booleans
        if isinstance(value, bool):
            return "true" if value else "false"
        
        # Handle numbers (int, float)
        if isinstance(value, (int, float)):
            return str(value)
        
        # Fallback: return as-is (for complex types like PackedStringArray)
        return str(value)
