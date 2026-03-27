"""
TscnReader: Read-only API for querying .tscn files
"""

from typing import List, Optional, Dict, Any
from pathlib import Path
from .parser import Parser
from .node_tree import Node_Tree
from .types import Node, ExtResource


class TscnReader:
    """
    Read-only interface for querying .tscn scene files.
    
    Provides methods to:
    - Query nodes by name, type, or property
    - Access node properties
    - Get metadata and statistics
    - Visualize scene hierarchy
    """
    
    def __init__(self, tscn_path: str):
        """
        Load and parse .tscn file.
        
        Args:
            tscn_path: Path to .tscn file
            
        Raises:
            ParseError: If file cannot be parsed
            FileNotFoundError: If file does not exist
        """
        self.tscn_path = Path(tscn_path)
        
        if not self.tscn_path.exists():
            raise FileNotFoundError(f"File not found: {tscn_path}")
        
        # Read file content
        content = self.tscn_path.read_text(encoding='utf-8')
        
        # Parse using Parser
        parser = Parser(content)
        header, ext_resources, nodes = parser.parse()
        
        # Build Node_Tree
        self._tree = Node_Tree(
            header=header,
            ext_resources=ext_resources,
            nodes=nodes
        )
    
    @property
    def tree(self) -> Node_Tree:
        """Access internal tree (read-only)"""
        return self._tree
    
    # ===== Node Query Methods =====
    
    def find_nodes_by_name(self, name: str) -> List[Node]:
        """
        Find nodes with exact name match.
        
        Args:
            name: Node name to search for
            
        Returns:
            List of nodes with matching name (empty if none found)
        """
        return [node for node in self._tree.nodes if node.name == name]
    
    def find_nodes_by_type(self, node_type: str) -> List[Node]:
        """
        Find all nodes of specific type.
        
        Args:
            node_type: Node type to search for (e.g., "Button", "Label")
            
        Returns:
            List of nodes with matching type (empty if none found)
        """
        return self._tree.get_nodes_by_type(node_type)
    
    def find_nodes_by_property(self, key: str, value: Any) -> List[Node]:
        """
        Find nodes where property matches value.
        
        Args:
            key: Property key to check
            value: Property value to match
            
        Returns:
            List of nodes with matching property (empty if none found)
        """
        matching_nodes = []
        for node in self._tree.nodes:
            if key in node.properties and node.properties[key] == value:
                matching_nodes.append(node)
        return matching_nodes
    
    # ===== Property Query Methods =====
    
    def get_node_property(self, node_path: str, key: str) -> Optional[Any]:
        """
        Get property value for specific node.
        
        Args:
            node_path: Full path to node (e.g., "Parent/Child")
            key: Property key
            
        Returns:
            Property value if found, None otherwise
        """
        node = self._tree.get_node_by_path(node_path)
        if node is None:
            return None
        return node.properties.get(key)
    
    def get_node_properties(self, node_path: str) -> Dict[str, Any]:
        """
        Get all properties for specific node.
        
        Args:
            node_path: Full path to node (e.g., "Parent/Child")
            
        Returns:
            Dictionary of properties (empty if node not found)
        """
        node = self._tree.get_node_by_path(node_path)
        if node is None:
            return {}
        return node.properties.copy()
    
    def node_exists(self, node_path: str) -> bool:
        """
        Check if node path exists.
        
        Args:
            node_path: Full path to node (e.g., "Parent/Child")
            
        Returns:
            True if node exists, False otherwise
        """
        return self._tree.get_node_by_path(node_path) is not None
    
    # ===== Metadata Query Methods =====
    
    def get_node_count_by_type(self, node_type: str) -> int:
        """
        Count nodes of specific type.
        
        Args:
            node_type: Node type to count
            
        Returns:
            Number of nodes with matching type
        """
        return len(self._tree.get_nodes_by_type(node_type))
    
    def list_ext_resources(self) -> List[ExtResource]:
        """
        Get all external resources.
        
        Returns:
            List of external resource declarations
        """
        return self._tree.ext_resources.copy()
    
    # ===== Tree Visualization =====
    
    def print_tree_view(self) -> str:
        """
        Generate human-readable tree visualization.
        
        Returns:
            ASCII tree showing hierarchy with:
            - Node names, types, unique_ids
            - Parent-child relationships (├──, └──, │)
            - Scene instances [INSTANCE: path]
            - Key properties inline
            - Script markers [script]
        """
        lines = []
        root_nodes = self._tree.get_root_nodes()
        
        for i, root_node in enumerate(root_nodes):
            is_last_root = (i == len(root_nodes) - 1)
            self._print_node_recursive(root_node, "", is_last_root, lines)
        
        return "\n".join(lines)
    
    def _print_node_recursive(self, node: Node, prefix: str, is_last: bool, lines: List[str]):
        """
        Recursively print node and its children with ASCII tree formatting.
        
        Args:
            node: Node to print
            prefix: Current indentation prefix
            is_last: Whether this is the last child of its parent
            lines: Output lines list to append to
        """
        # Build node line
        connector = "└── " if is_last else "├── "
        node_line = f"{prefix}{connector}{node.name} ({node.node_type})"
        
        # Add unique_id
        node_line += f" [unique_id={node.unique_id}]"
        
        # Add scene instance annotation
        if node.is_instance and node.scene_path:
            node_line += f" [INSTANCE: {node.scene_path}]"
        
        # Add script marker
        if 'script' in node.properties:
            node_line += " [script]"
        
        lines.append(node_line)
        
        # Show key properties inline
        key_properties = self._get_key_properties(node)
        if key_properties:
            child_prefix = prefix + ("    " if is_last else "│   ")
            for prop_key, prop_value in key_properties.items():
                lines.append(f"{child_prefix}└── {prop_key}: {prop_value}")
        
        # Print children
        node_path = self._tree.build_full_path(node)
        children = self._tree.get_children(node_path)
        
        for i, child in enumerate(children):
            is_last_child = (i == len(children) - 1)
            child_prefix = prefix + ("    " if is_last else "│   ")
            self._print_node_recursive(child, child_prefix, is_last_child, lines)
    
    def _get_key_properties(self, node: Node) -> Dict[str, Any]:
        """
        Extract key properties to display inline.
        
        Args:
            node: Node to extract properties from
            
        Returns:
            Dictionary of key properties (text, color, etc.)
        """
        key_props = {}
        
        # Common properties to show
        display_keys = ['text', 'color', 'position', 'size', 'value', 'placeholder_text']
        
        for key in display_keys:
            if key in node.properties:
                key_props[key] = node.properties[key]
        
        return key_props
