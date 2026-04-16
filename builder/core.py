"""
Core TSCN Builder - Manages underlying .tscn file structure
Zero hardcoded UI or StateChart logic
"""

import random
from typing import Optional, List, Dict, Any


class TscnNode:
    """Represents a generic node in the TSCN tree"""
    
    def __init__(self, name: str, node_type: str, unique_id: Optional[int] = None):
        self.name = name
        self.node_type = node_type
        self.unique_id = unique_id or random.randint(1, 2**31 - 1)
        self.parent_path = "."
        self.properties: Dict[str, Any] = {}
        self.children: List['TscnNode'] = []
        self.parent: Optional['TscnNode'] = None
    
    def get_path_from_root(self) -> List['TscnNode']:
        """Get complete node path from root to current node"""
        path = []
        current = self
        while current is not None:
            path.append(current)
            current = current.parent
        return path[::-1]
    
    def get_relative_path_to(self, target: 'TscnNode') -> str:
        """Calculate precise relative NodePath from current node to target node"""
        my_path = self.get_path_from_root()
        target_path = target.get_path_from_root()
        
        lca_index = -1
        for i in range(min(len(my_path), len(target_path))):
            if my_path[i] == target_path[i]:
                lca_index = i
            else:
                break
        
        if lca_index == -1:
            raise ValueError(f"Nodes {self.name} and {target.name} are not in the same tree!")
        
        steps_up = len(my_path) - 1 - lca_index
        down_path = [node.name for node in target_path[lca_index + 1:]]
        
        if steps_up == 0 and not down_path:
            return "."
        
        parts = [".."] * steps_up + down_path
        return "/".join(parts)
    
    def _add_child(self, child: 'TscnNode') -> 'TscnNode':
        """Internal: Add child node"""
        child.parent = self
        self.children.append(child)
        
        if self.parent is None:
            child.parent_path = "."
        else:
            if self.parent_path == ".":
                child.parent_path = self.name
            else:
                child.parent_path = f"{self.parent_path}/{self.name}"
        return child
    
    def set_property(self, key: str, value: Any) -> 'TscnNode':
        """Set property (chainable)"""
        self.properties[key] = value
        return self


class TscnBuilder:
    """Core builder managing TSCN file structure"""
    
    def __init__(self, root_name: str, root_type: str, scene_uid: Optional[str] = None):
        """Initialize TSCN builder
        
        Args:
            root_name: Root node name
            root_type: Root node type (e.g., "Control", "CharacterBody3D", "Node3D")
            scene_uid: Optional scene UID
        """
        self.root_name = root_name
        self.root_type = root_type
        self.scene_uid = scene_uid or self._generate_uid()
        self.root: Optional[TscnNode] = None
        self.ext_resources: List[Dict[str, str]] = []
        self.sub_resources: List[Dict[str, Any]] = []
        self._resource_counter = 1
        self._node_registry: Dict[str, TscnNode] = {}
    
    def _generate_uid(self) -> str:
        """Generate random UID"""
        chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        return "uid://" + "".join(random.choice(chars) for _ in range(14))
    
    def initialize_root(self, **properties) -> TscnNode:
        """Create root node with optional properties"""
        self.root = TscnNode(self.root_name, self.root_type)
        for key, value in properties.items():
            self.root.set_property(key, value)
        self._node_registry[self.root_name] = self.root
        return self.root
    
    def add_node(self, name: str, node_type: str, parent: str = ".", **properties) -> TscnNode:
        """Add a node to the tree
        
        Args:
            name: Node name
            node_type: Node type
            parent: Parent path ("." for root, or node name/path)
            **properties: Node properties
        
        Returns:
            Created TscnNode
        """
        node = TscnNode(name, node_type)
        
        # Don't auto-mark all nodes as unique - only mark nodes that need to be found
        # (StateChart states, nodes referenced by [Export] properties, etc.)
        for key, value in properties.items():
            node.set_property(key, value)
        
        # Find parent node
        if parent == ".":
            if self.root is None:
                raise ValueError("Root node not initialized. Call initialize_root() first.")
            parent_node = self.root
        else:
            parent_node = self._node_registry.get(parent)
            if parent_node is None:
                raise ValueError(f"Parent node '{parent}' not found in registry")
        
        parent_node._add_child(node)
        self._node_registry[name] = node
        return node
    
    def get_node(self, name: str) -> Optional[TscnNode]:
        """Get node by name from registry"""
        return self._node_registry.get(name)
    
    def assign_node_path(self, target_node_name: str, property_name: str, path_to_node_name: str):
        """Calculate NodePath using Scene Unique Name and assign to target node's property
        
        This is the killer feature for C# architecture: automatically bind UI nodes
        to Controller [Export] properties using robust % syntax.
        
        Args:
            target_node_name: Node that has the [Export] property (e.g., "SettingsController")
            property_name: Property name (e.g., "ApplyButton", "VolumeSlider")
            path_to_node_name: Node to assign (e.g., "ApplyButton")
        
        Example:
            # Create UI button
            ui.add_button("ApplyButton", parent="MainVBox", text="Apply")
            
            # Create C# controller
            scene.add_node("SettingsController", "Node", parent=".",
                          script=ExtResource("controller_script"))
            
            # Automatically bind button to controller's [Export] property
            scene.assign_node_path("SettingsController", "ApplyButton", "ApplyButton")
            
            # Generated TSCN will have:
            # [node name="SettingsController" ...]
            # ApplyButton = NodePath("%ApplyButton")  # Uses Scene Unique Name!
        """
        target_node = self.get_node(target_node_name)
        path_to_node = self.get_node(path_to_node_name)
        
        if target_node is None:
            raise ValueError(f"Target node '{target_node_name}' not found in registry")
        if path_to_node is None:
            raise ValueError(f"Path-to node '{path_to_node_name}' not found in registry")
        
        # Auto-mark the referenced node as unique so it can be found via %
        # This ensures only nodes that need to be found are marked as unique
        if not path_to_node.properties.get("unique_name_in_owner"):
            path_to_node.set_property("unique_name_in_owner", True)
        
        # Use Scene Unique Name syntax for robust, hierarchy-independent path resolution
        # This is much more stable than relative paths like "../../../NodeName"
        target_node.set_property(property_name, f'NodePath("%{path_to_node_name}")')
    
    def assign_multiple_node_paths(self, target_node_name: str, bindings: dict):
        """Batch assign multiple NodePaths to a target node
        
        Args:
            target_node_name: Node that has [Export] properties
            bindings: Dictionary mapping property names to node names
        
        Example:
            scene.assign_multiple_node_paths("SettingsController", {
                "ApplyButton": "ApplyButton",
                "CancelButton": "CancelButton",
                "VolumeSlider": "VolumeSlider",
                "FullscreenCheckbox": "FullscreenCheckbox"
            })
        """
        for property_name, node_name in bindings.items():
            self.assign_node_path(target_node_name, property_name, node_name)
    
    def add_ext_resource(self, resource_type: str, path: str, uid: str, resource_id: Optional[str] = None) -> str:
        """Add external resource
        
        Returns:
            Resource ID for referencing
        """
        if resource_id is None:
            resource_id = f"{self._resource_counter}_res"
            self._resource_counter += 1
        
        if not any(r["id"] == resource_id for r in self.ext_resources):
            self.ext_resources.append({
                "type": resource_type,
                "path": path,
                "uid": uid,
                "id": resource_id
            })
        
        return resource_id
    
    def add_sub_resource(self, resource_type: str, resource_id: str, **properties) -> str:
        """Add sub-resource
        
        Returns:
            Resource ID for referencing
        """
        if not any(r["id"] == resource_id for r in self.sub_resources):
            self.sub_resources.append({
                "type": resource_type,
                "id": resource_id,
                "properties": properties
            })
        
        return resource_id
    
    def generate_tree_view(self) -> str:
        """Generate tree view for inspection"""
        if not self.root:
            return "No root node"
        
        lines = []
        
        def _traverse(node: TscnNode, prefix: str = "", is_last: bool = True):
            info = f"{node.name} ({node.node_type})"
            
            extras = []
            if node.properties.get("_is_instance"):
                extras.append(f"[INSTANCE: {node.properties['_scene_path']}]")
            if "text" in node.properties:
                extras.append(node.properties["text"].strip('"'))
            if "_script_path" in node.properties:
                extras.append("[script]")
            if node == self.root:
                extras.append("[root]")
            
            if extras:
                info += f" {' '.join(extras)}"
            
            connector = "└── " if is_last else "├── "
            lines.append(prefix + connector + info)
            
            child_prefix = prefix + ("    " if is_last else "│   ")
            for i, child in enumerate(node.children):
                _traverse(child, child_prefix, i == len(node.children) - 1)
        
        lines.append(f"{self.root.name} ({self.root.node_type}) [root]")
        for i, child in enumerate(self.root.children):
            _traverse(child, "", i == len(self.root.children) - 1)
        
        return "\n".join(lines)
    
    def generate_tscn(self) -> str:
        """Generate .tscn file content"""
        if not self.root:
            raise ValueError("No root node created")
        
        lines = []
        
        # Calculate load_steps
        load_steps = len(self.ext_resources) + len(self.sub_resources)
        
        # File header
        if load_steps > 0:
            lines.append(f'[gd_scene load_steps={load_steps} format=3 uid="{self.scene_uid}"]')
        else:
            lines.append(f'[gd_scene format=3 uid="{self.scene_uid}"]')
        lines.append("")
        
        # External resources
        for res in self.ext_resources:
            lines.append(f'[ext_resource type="{res["type"]}" uid="{res["uid"]}" path="{res["path"]}" id="{res["id"]}"]')
        
        if self.ext_resources:
            lines.append("")
        
        # Sub-resources
        for res in self.sub_resources:
            lines.append(f'[sub_resource type="{res["type"]}" id="{res["id"]}"]')
            for key, value in res["properties"].items():
                if isinstance(value, str):
                    lines.append(f'{key} = "{value}"')
                else:
                    lines.append(f"{key} = {value}")
            lines.append("")
        
        # Node definitions
        def _write_node(node: TscnNode):
            # Instance node
            if node.properties.get("_is_instance"):
                scene_path = node.properties["_scene_path"]
                scene_res_id = None
                for res in self.ext_resources:
                    if res["type"] == "PackedScene" and res["path"] == scene_path:
                        scene_res_id = res["id"]
                        break
                
                if node == self.root:
                    lines.append(f'[node name="{node.name}" instance=ExtResource("{scene_res_id}")]')
                else:
                    lines.append(f'[node name="{node.name}" parent="{node.parent_path}" instance=ExtResource("{scene_res_id}")]')
            else:
                # Regular node
                if node == self.root:
                    lines.append(f'[node name="{node.name}" type="{node.node_type}"]')
                else:
                    lines.append(f'[node name="{node.name}" type="{node.node_type}" parent="{node.parent_path}"]')
            
            # Properties
            for key, value in node.properties.items():
                if key.startswith("_"):
                    continue
                
                if isinstance(value, str):
                    # Check if value is already a formatted Godot expression
                    # (NodePath, ExtResource, Color, Vector2, etc.)
                    if (value.startswith('NodePath(') or 
                        value.startswith('ExtResource(') or 
                        value.startswith('SubResource(') or
                        value.startswith('Color(') or
                        value.startswith('Vector2(') or
                        value.startswith('Vector3(') or
                        value.startswith('&"')):  # StringName
                        lines.append(f"{key} = {value}")
                    else:
                        # Regular string - needs quotes
                        lines.append(f'{key} = "{value}"')
                elif isinstance(value, bool):
                    lines.append(f"{key} = {str(value).lower()}")
                elif isinstance(value, (int, float)):
                    lines.append(f"{key} = {value}")
                else:
                    lines.append(f"{key} = {value}")
            
            lines.append("")
            
            # Children
            for child in node.children:
                _write_node(child)
        
        _write_node(self.root)
        
        return "\n".join(lines)
    
    def save(self, output_path: str):
        """Save to file"""
        content = self.generate_tscn()
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Scene saved to: {output_path}")
