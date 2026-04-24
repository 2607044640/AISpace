"""
TscnEditor: Modification API for editing .tscn files
"""

import copy
from typing import Optional, Dict, Any, List, Set
from pathlib import Path
from .reader import TscnReader
from .pretty_printer import Pretty_Printer
from .node_tree import Node_Tree
from .types import Node, ExtResource, PropertyUpdate, BatchResult, EditorError


class UIDGenerator:
    """
    Generates unique IDs for new nodes.
    
    Ensures generated IDs don't conflict with existing unique_id values
    in the scene.
    """
    
    def __init__(self, existing_ids: Set[int]):
        """
        Initialize generator with existing IDs.
        
        Args:
            existing_ids: Set of unique_id values already in use
        """
        self.used_ids = existing_ids.copy()
        self.next_id = max(existing_ids) + 1 if existing_ids else 1
    
    def generate(self) -> int:
        """
        Generate a unique ID not in the existing set.
        
        Returns:
            New unique_id value
        """
        while self.next_id in self.used_ids:
            self.next_id += 1
        self.used_ids.add(self.next_id)
        return self.next_id


class TscnEditor:
    """
    Modification interface for editing .tscn scene files.
    
    Provides methods to:
    - Update node properties (single and batch)
    - Add new nodes (regular and scene instances)
    - Remove nodes with recursive child removal
    - Save modifications back to .tscn format
    
    All modifications preserve UIDs, formatting, and references.
    """
    
    def __init__(self, tscn_path: str):
        """
        Load .tscn file for editing.
        
        Args:
            tscn_path: Path to .tscn file
            
        Raises:
            ParseError: If file cannot be parsed
            FileNotFoundError: If file does not exist
        """
        self.tscn_path = Path(tscn_path)
        
        # Load using TscnReader
        self._reader = TscnReader(str(self.tscn_path))
        
        # Create mutable copy of tree for modifications
        self._tree = copy.deepcopy(self._reader.tree)
        
        # Initialize UID generator with existing IDs
        existing_ids = {node.unique_id for node in self._tree.nodes}
        self._uid_generator = UIDGenerator(existing_ids)
    
    @property
    def reader(self) -> TscnReader:
        """
        Access read-only query interface.
        
        Returns:
            TscnReader instance with current tree state
        """
        # Update reader's tree to reflect current modifications
        self._reader._tree = self._tree
        return self._reader
    
    def update_property(self, node_path: str, key: str, value: Any) -> None:
        """
        Update single property on specific node.
        
        Args:
            node_path: Full path to node (e.g., "Parent/Child")
            key: Property key to update
            value: New property value
            
        Raises:
            EditorError: If node path does not exist
        """
        node = self._tree.get_node_by_path(node_path)
        if node is None:
            raise EditorError(f"Node not found: {node_path}")
        
        # Update property
        node.properties[key] = value
        
        # Rebuild indices to reflect changes
        self._tree._build_indices()
    
    def update_properties_batch(self, updates: List[PropertyUpdate]) -> BatchResult:
        """
        Update multiple properties across multiple nodes.
        
        Args:
            updates: List of PropertyUpdate operations
            
        Returns:
            BatchResult with success count and error messages
        """
        success_count = 0
        errors = []
        
        for update in updates:
            try:
                self.update_property(
                    update.node_path,
                    update.property_key,
                    update.property_value
                )
                success_count += 1
            except EditorError as e:
                errors.append(f"{update.node_path}: {str(e)}")
        
        return BatchResult(success_count=success_count, errors=errors)
    
    def add_node(
        self,
        name: str,
        node_type: str,
        parent_path: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> Node:
        """
        Add new regular node to the scene.
        
        Args:
            name: Node name
            node_type: Node type (e.g., "Button", "Label")
            parent_path: Full path to parent node, or "." for root
            properties: Optional initial properties
            
        Returns:
            The newly created Node
            
        Raises:
            EditorError: If parent doesn't exist or duplicate name
        """
        # Validate parent exists (unless adding root node)
        if parent_path != ".":
            parent_node = self._tree.get_node_by_path(parent_path)
            if parent_node is None:
                raise EditorError(f"Parent node not found: {parent_path}")
        
        # Check for duplicate name under same parent
        existing_children = self._tree.get_children(parent_path)
        if any(child.name == name for child in existing_children):
            raise EditorError(
                f"Node with name '{name}' already exists under parent '{parent_path}'"
            )
        
        # Generate unique ID
        unique_id = self._uid_generator.generate()
        
        # Create new node
        new_node = Node(
            name=name,
            node_type=node_type,
            unique_id=unique_id,
            parent_path=parent_path,
            properties=properties.copy() if properties else {},
            is_instance=False
        )
        
        # Add to tree
        self._tree.nodes.append(new_node)
        
        # Rebuild indices
        self._tree._build_indices()
        
        return new_node
    
    def add_scene_instance(
        self,
        name: str,
        scene_path: str,
        parent_path: str,
        scene_uid: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> Node:
        """
        Add scene instance node to the scene.
        
        Args:
            name: Node name
            scene_path: Path to scene file (e.g., "res://scenes/Player.tscn")
            parent_path: Full path to parent node, or "." for root
            scene_uid: Optional scene UID (if known)
            properties: Optional initial properties
            
        Returns:
            The newly created Node
            
        Raises:
            EditorError: If parent doesn't exist or duplicate name
        """
        # Validate parent exists (unless adding root node)
        if parent_path != ".":
            parent_node = self._tree.get_node_by_path(parent_path)
            if parent_node is None:
                raise EditorError(f"Parent node not found: {parent_path}")
        
        # Check for duplicate name under same parent
        existing_children = self._tree.get_children(parent_path)
        if any(child.name == name for child in existing_children):
            raise EditorError(
                f"Node with name '{name}' already exists under parent '{parent_path}'"
            )
        
        # Check if ext_resource already exists for this scene
        resource_id = None
        for ext_res in self._tree.ext_resources:
            if ext_res.path == scene_path:
                resource_id = ext_res.resource_id
                break
        
        # If not found, create new ext_resource
        if resource_id is None:
            resource_id = self._generate_resource_id("scene")
            
            # Use provided scene_uid or generate placeholder
            if scene_uid is None:
                scene_uid = "uid://placeholder"
            
            new_ext_resource = ExtResource(
                resource_type="PackedScene",
                uid=scene_uid,
                path=scene_path,
                resource_id=resource_id
            )
            self._tree.ext_resources.append(new_ext_resource)
        
        # Generate unique ID for node
        unique_id = self._uid_generator.generate()
        
        # Create properties dict with instance metadata
        node_properties = properties.copy() if properties else {}
        node_properties['_instance_resource_id'] = resource_id
        
        # Create new scene instance node
        new_node = Node(
            name=name,
            node_type="Node",  # Scene instances typically use base type
            unique_id=unique_id,
            parent_path=parent_path,
            properties=node_properties,
            is_instance=True,
            scene_path=scene_path,
            scene_uid=scene_uid
        )
        
        # Add to tree
        self._tree.nodes.append(new_node)
        
        # Rebuild indices
        self._tree._build_indices()
        
        return new_node
    
    def remove_node(self, node_path: str) -> None:
        """
        Remove node and all its children from the scene.
        
        Args:
            node_path: Full path to node to remove
            
        Raises:
            EditorError: If node doesn't exist or is root node
        """
        node = self._tree.get_node_by_path(node_path)
        if node is None:
            raise EditorError(f"Node not found: {node_path}")
        
        # Prevent removing root nodes
        if node.parent_path == ".":
            raise EditorError("Cannot remove root node")
        
        # Collect all nodes to remove (node + all descendants)
        nodes_to_remove = self._collect_descendants(node_path)
        nodes_to_remove.append(node)
        
        # Remove from tree
        for node_to_remove in nodes_to_remove:
            self._tree.nodes.remove(node_to_remove)
        
        # Rebuild indices
        self._tree._build_indices()
    
    def save(self, output_path: Optional[str] = None) -> None:
        """
        Save modifications to .tscn file.
        
        Args:
            output_path: Optional output path (defaults to original path)
            
        Raises:
            EditorError: If save operation fails
        """
        # Use original path if not specified
        if output_path is None:
            output_path = str(self.tscn_path)
        
        # Format tree using Pretty_Printer
        printer = Pretty_Printer()
        tscn_content = printer.print_tree(self._tree)
        
        # Write to file
        try:
            output_file = Path(output_path)
            output_file.write_text(tscn_content, encoding='utf-8')
        except Exception as e:
            raise EditorError(f"Failed to save file: {str(e)}")
    
    # ===== Helper Methods =====
    
    def _collect_descendants(self, node_path: str) -> List[Node]:
        """
        Recursively collect all descendant nodes.
        
        Args:
            node_path: Full path to parent node
            
        Returns:
            List of all descendant nodes
        """
        descendants = []
        children = self._tree.get_children(node_path)
        
        for child in children:
            child_path = self._tree.build_full_path(child)
            descendants.append(child)
            # Recursively collect child's descendants
            descendants.extend(self._collect_descendants(child_path))
        
        return descendants
    
    def _generate_resource_id(self, resource_type: str) -> str:
        """
        Generate unique resource ID for ext_resource.
        
        Args:
            resource_type: Type hint for ID (e.g., "scene", "script")
            
        Returns:
            Resource ID string (e.g., "1_scene", "2_script")
        """
        # Find highest numeric prefix in existing resource IDs
        max_id = 0
        for ext_res in self._tree.ext_resources:
            # Extract numeric prefix (e.g., "1" from "1_scene")
            parts = ext_res.resource_id.split('_')
            if parts[0].isdigit():
                max_id = max(max_id, int(parts[0]))
        
        # Generate new ID
        new_id = max_id + 1
        return f"{new_id}_{resource_type}"
