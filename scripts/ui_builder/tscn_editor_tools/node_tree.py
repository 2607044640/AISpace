"""
Node_Tree: Internal representation of .tscn scene hierarchy
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from .types import Header, ExtResource, Node


@dataclass
class Node_Tree:
    """
    Internal tree representation of a .tscn scene file.
    
    Provides efficient queries via computed indices:
    - _node_by_path: Fast lookup by full path
    - _nodes_by_type: Fast lookup by node type
    - _children_by_parent: Fast lookup of children by parent path
    """
    
    header: Header
    ext_resources: List[ExtResource]
    nodes: List[Node]
    
    # Computed indices (built in __post_init__)
    _node_by_path: Dict[str, Node] = field(default_factory=dict, init=False, repr=False)
    _nodes_by_type: Dict[str, List[Node]] = field(default_factory=dict, init=False, repr=False)
    _children_by_parent: Dict[str, List[Node]] = field(default_factory=dict, init=False, repr=False)
    _ext_resource_by_id: Dict[str, ExtResource] = field(default_factory=dict, init=False, repr=False)
    
    def __post_init__(self):
        """Build computed indices and resolve scene instance metadata"""
        # Build ext_resource lookup index by resource_id (e.g., "1_scene", "2_script")
        self._ext_resource_by_id = {res.resource_id: res for res in self.ext_resources}
        
        # Resolve scene instance metadata
        self._resolve_scene_instances()
        
        # Build node indices
        self._build_indices()
    
    def _resolve_scene_instances(self):
        """
        Populate scene_path and scene_uid for scene instance nodes.
        
        Scene instances have is_instance=True and store the resource_id in
        properties['_instance_resource_id']. We look up the ExtResource to
        get the actual scene_path and scene_uid.
        """
        for node in self.nodes:
            if node.is_instance and '_instance_resource_id' in node.properties:
                resource_id = node.properties['_instance_resource_id']
                ext_resource = self._ext_resource_by_id.get(resource_id)
                
                if ext_resource:
                    node.scene_path = ext_resource.path
                    node.scene_uid = ext_resource.uid
    
    def _build_indices(self):
        """Build computed indices for fast queries"""
        # Build _nodes_by_type
        self._nodes_by_type.clear()
        for node in self.nodes:
            if node.node_type not in self._nodes_by_type:
                self._nodes_by_type[node.node_type] = []
            self._nodes_by_type[node.node_type].append(node)
        
        # Build _children_by_parent
        self._children_by_parent.clear()
        for node in self.nodes:
            parent_path = node.parent_path
            if parent_path not in self._children_by_parent:
                self._children_by_parent[parent_path] = []
            self._children_by_parent[parent_path].append(node)
        
        # Build _node_by_path (requires computing full paths)
        self._node_by_path.clear()
        for node in self.nodes:
            full_path = self.build_full_path(node)
            self._node_by_path[full_path] = node
    
    def build_full_path(self, node: Node) -> str:
        """
        Compute the full path from root to the given node.
        
        Args:
            node: The node to compute the path for
            
        Returns:
            Full path string (e.g., "Parent/Child/GrandChild")
            
        Examples:
            - Root node with parent="." returns just the node name
            - Child node with parent="Root" returns "Root/Child"
            - Nested node with parent="Root/Child" returns "Root/Child/GrandChild"
        """
        if node.parent_path == ".":
            # Root node
            return node.name
        else:
            # Child node - parent_path is already the full path to parent
            return f"{node.parent_path}/{node.name}"
    
    def get_node_by_path(self, path: str) -> Optional[Node]:
        """
        Get node by exact full path.
        
        Args:
            path: Full path from root (e.g., "Parent/Child")
            
        Returns:
            Node if found, None otherwise
        """
        return self._node_by_path.get(path)
    
    def get_nodes_by_type(self, node_type: str) -> List[Node]:
        """
        Get all nodes of a specific type.
        
        Args:
            node_type: The node type to search for (e.g., "Button", "Label")
            
        Returns:
            List of nodes with matching type (empty list if none found)
        """
        return self._nodes_by_type.get(node_type, [])
    
    def get_children(self, parent_path: str) -> List[Node]:
        """
        Get direct children of a node.
        
        Args:
            parent_path: Full path of the parent node, or "." for root children
            
        Returns:
            List of child nodes (empty list if none found)
        """
        return self._children_by_parent.get(parent_path, [])
    
    def get_root_nodes(self) -> List[Node]:
        """
        Get all root nodes (nodes with parent=".").
        
        Returns:
            List of root nodes
        """
        return self.get_children(".")
