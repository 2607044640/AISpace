"""
Godot StateChart Builder - Programmatically generate Godot StateChart .tscn files
Enables AI to manipulate StateCharts without dealing with verbose .tscn text
"""

import random
from typing import Optional, List, Dict, Any


class StateChartNode:
    """Represents a StateChart node (StateChart, State, Transition, Guard, Component)"""
    
    # Script paths for different node types
    SCRIPTS = {
        "StateChart": "res://addons/godot_state_charts/state_chart.gd",
        "ParallelState": "res://addons/godot_state_charts/parallel_state.gd",
        "CompoundState": "res://addons/godot_state_charts/compound_state.gd",
        "AtomicState": "res://addons/godot_state_charts/atomic_state.gd",
        "Transition": "res://addons/godot_state_charts/transition.gd",
        "ExpressionGuard": "res://addons/godot_state_charts/expression_guard.gd",
    }
    
    # UIDs for StateChart scripts
    SCRIPT_UIDS = {
        "StateChart": "uid://couw105c3bde4",
        "ParallelState": "uid://c1vp0ojjvaby1",
        "CompoundState": "uid://jk2jm1g6q853",
        "AtomicState": "uid://cytafq8i1y8qm",
        "Transition": "uid://cf1nsco3w0mf6",
        "ExpressionGuard": "uid://b4xy2kqvvx8yx",
    }
    
    def __init__(self, name: str, node_type: str, unique_id: Optional[int] = None):
        self.name = name
        self.node_type = node_type
        self.unique_id = unique_id or random.randint(1, 2**31 - 1)
        self.parent_path = "."
        self.properties: Dict[str, Any] = {}
        self.children: List['StateChartNode'] = []
        self.parent: Optional['StateChartNode'] = None
        
        # Auto-assign script for state chart nodes
        if node_type in self.SCRIPTS:
            self.properties["script"] = f'ExtResource("script_{node_type}")'
            self.properties["_script_path"] = self.SCRIPTS[node_type]
            self.properties["_script_uid"] = self.SCRIPT_UIDS[node_type]
    
    def get_path_from_root(self) -> List['StateChartNode']:
        """Get complete node path from root to current node"""
        path = []
        current = self
        while current is not None:
            path.append(current)
            current = current.parent
        return path[::-1]  # Reverse to get [Root, Child, GrandChild, Self]
    
    def get_relative_path_to(self, target: 'StateChartNode') -> str:
        """Calculate precise relative NodePath from current node to target node.
        
        Example: Automatically calculates "../../FlyMode" for transitions
        
        Args:
            target: Target node
            
        Returns:
            Relative path string like "../../FlyMode" or "." (same node)
            
        Raises:
            ValueError: If nodes are not in the same tree
        """
        my_path = self.get_path_from_root()
        target_path = target.get_path_from_root()
        
        # 1. Find Lowest Common Ancestor (LCA)
        lca_index = -1
        for i in range(min(len(my_path), len(target_path))):
            if my_path[i] == target_path[i]:
                lca_index = i
            else:
                break
        
        if lca_index == -1:
            raise ValueError(f"Nodes {self.name} and {target.name} are not in the same tree!")
        
        # 2. Calculate steps up (how many ".." needed)
        steps_up = len(my_path) - 1 - lca_index
        
        # 3. Calculate down path from LCA
        down_path = [node.name for node in target_path[lca_index + 1:]]
        
        # 4. Combine path
        if steps_up == 0 and not down_path:
            return "."  # Same node
        
        parts = [".."] * steps_up + down_path
        return "/".join(parts)
    
    def _add_child(self, child: 'StateChartNode') -> 'StateChartNode':
        """Internal method: Add child node"""
        child.parent = self
        self.children.append(child)
        # Calculate parent_path
        if self.parent is None:
            # Root node's children
            child.parent_path = "."
        else:
            # Non-root node's children
            if self.parent_path == ".":
                child.parent_path = self.name
            else:
                child.parent_path = f"{self.parent_path}/{self.name}"
        return child
    
    def set_property(self, key: str, value: Any) -> 'StateChartNode':
        """Set property (chainable)"""
        self.properties[key] = value
        return self
    
    # === State Node Methods ===
    
    def add_parallel_state(self, name: str) -> 'StateChartNode':
        """Add ParallelState (allows simultaneous active child states)"""
        node = StateChartNode(name, "ParallelState")
        return self._add_child(node)
    
    def add_compound_state(self, name: str, initial_state: Optional[str] = None) -> 'StateChartNode':
        """Add CompoundState (mutually exclusive child states)
        
        Args:
            initial_state: Name of the initial child state (will be set after children are added)
        """
        node = StateChartNode(name, "CompoundState")
        if initial_state:
            node.properties["_initial_state_name"] = initial_state  # Store for later resolution
        return self._add_child(node)
    
    def add_atomic_state(self, name: str) -> 'StateChartNode':
        """Add AtomicState (leaf state, cannot have child states)"""
        node = StateChartNode(name, "AtomicState")
        return self._add_child(node)
    
    # === Transition Methods ===
    
    def add_transition(self, name: str, to_state: 'StateChartNode', 
                      event: str = "", delay: float = 0.0) -> 'StateChartNode':
        """Add Transition (state change trigger)
        
        Args:
            name: Transition name
            to_state: Target state node
            event: Event name that triggers this transition (empty for automatic)
            delay: Delay in seconds before transition executes
        """
        node = StateChartNode(name, "Transition")
        
        # Calculate relative path to target state
        relative_path = self.get_relative_path_to(to_state)
        node.properties["to"] = f'NodePath("{relative_path}")'
        
        if event:
            node.properties["event"] = f'&"{event}"'
        
        if delay > 0:
            node.properties["delay_in_seconds"] = f'"{delay}"'
        else:
            node.properties["delay_in_seconds"] = '"0.0"'
        
        return self._add_child(node)
    
    # === Guard Methods ===
    
    def add_expression_guard(self, name: str, expression: str) -> 'StateChartNode':
        """Add ExpressionGuard (condition check for transition)
        
        Args:
            name: Guard name
            expression: GDScript expression (e.g., "player_health > 50")
        """
        node = StateChartNode(name, "ExpressionGuard")
        node.properties["expression"] = f'"{expression}"'
        return self._add_child(node)
    
    # === Component Methods ===
    
    def add_component(self, name: str, script_path: str, script_uid: Optional[str] = None) -> 'StateChartNode':
        """Add Component node (C# script attached to state)
        
        Args:
            name: Component name
            script_path: Path to C# script (e.g., "res://addons/A1MyAddon/CoreComponents/GroundMovementComponent.cs")
            script_uid: Script UID (optional)
        """
        node = StateChartNode(name, "Node")
        node.properties["script"] = f'ExtResource("component_{name}")'
        node.properties["_component_script_path"] = script_path
        node.properties["_component_script_uid"] = script_uid or "uid://placeholder"
        return self._add_child(node)


class StateChartBuilder:
    """StateChart builder"""
    
    def __init__(self, entity_name: str, entity_type: str = "CharacterBody3D", 
                 entity_script_path: Optional[str] = None, entity_script_uid: Optional[str] = None):
        """Initialize StateChart builder
        
        Args:
            entity_name: Entity node name (e.g., "Player3D")
            entity_type: Entity node type (e.g., "CharacterBody3D", "Node3D")
            entity_script_path: Path to entity C# script
            entity_script_uid: Entity script UID
        """
        self.entity_name = entity_name
        self.entity_type = entity_type
        self.entity_script_path = entity_script_path
        self.entity_script_uid = entity_script_uid or self._generate_uid()
        self.root: Optional[StateChartNode] = None
        self.statechart: Optional[StateChartNode] = None
        self.ext_resources: List[Dict[str, str]] = []
        self._resource_counter = 1
    
    def _generate_uid(self) -> str:
        """Generate random UID"""
        chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        return "uid://" + "".join(random.choice(chars) for _ in range(14))
    
    def create_entity_with_statechart(self) -> StateChartNode:
        """Create entity root node with StateChart child"""
        # Create entity root
        self.root = StateChartNode(self.entity_name, self.entity_type)
        
        if self.entity_script_path:
            self.root.properties["script"] = f'ExtResource("entity_script")'
            self.root.properties["_entity_script_path"] = self.entity_script_path
            self.root.properties["_entity_script_uid"] = self.entity_script_uid
        
        # Create StateChart node
        self.statechart = StateChartNode("StateChart", "StateChart")
        self.root._add_child(self.statechart)
        
        return self.statechart
    
    def _resolve_initial_states(self, node: StateChartNode):
        """Resolve initial_state NodePath references after tree is built"""
        if node.node_type == "CompoundState" and "_initial_state_name" in node.properties:
            initial_name = node.properties["_initial_state_name"]
            # Find child with matching name
            for child in node.children:
                if child.name == initial_name:
                    relative_path = node.get_relative_path_to(child)
                    node.properties["initial_state"] = f'NodePath("{relative_path}")'
                    del node.properties["_initial_state_name"]
                    break
        
        # Recurse
        for child in node.children:
            self._resolve_initial_states(child)
    
    def _collect_ext_resources(self, node: StateChartNode):
        """Collect all external resource references"""
        # Entity script
        if "_entity_script_path" in node.properties:
            script_path = node.properties["_entity_script_path"]
            if not any(r["path"] == script_path for r in self.ext_resources):
                self.ext_resources.append({
                    "type": "Script",
                    "path": script_path,
                    "id": "entity_script",
                    "uid": node.properties.get("_entity_script_uid", "uid://placeholder")
                })
        
        # StateChart scripts
        if "_script_path" in node.properties:
            script_path = node.properties["_script_path"]
            script_uid = node.properties.get("_script_uid", "uid://placeholder")
            resource_id = f"script_{node.node_type}"
            
            if not any(r["id"] == resource_id for r in self.ext_resources):
                self.ext_resources.append({
                    "type": "Script",
                    "path": script_path,
                    "id": resource_id,
                    "uid": script_uid
                })
        
        # Component scripts
        if "_component_script_path" in node.properties:
            script_path = node.properties["_component_script_path"]
            script_uid = node.properties.get("_component_script_uid", "uid://placeholder")
            resource_id = f"component_{node.name}"
            
            if not any(r["path"] == script_path for r in self.ext_resources):
                self.ext_resources.append({
                    "type": "Script",
                    "path": script_path,
                    "id": resource_id,
                    "uid": script_uid
                })
        
        # Recurse
        for child in node.children:
            self._collect_ext_resources(child)
    
    def generate_tree_view(self) -> str:
        """Generate tree view (for AI inspection)"""
        if not self.root:
            return "No root node"
        
        lines = []
        
        def _traverse(node: StateChartNode, prefix: str = "", is_last: bool = True):
            # Node info
            info = f"{node.name} ({node.node_type})"
            
            # Add key properties
            extras = []
            if "event" in node.properties:
                event_str = node.properties["event"].strip('&"')
                extras.append(f"event={event_str}")
            if "to" in node.properties:
                to_str = node.properties["to"].strip('NodePath("').strip('")')
                extras.append(f"to={to_str}")
            if "_component_script_path" in node.properties:
                extras.append("[component]")
            if node == self.root:
                extras.append("[root]")
            
            if extras:
                info += f" {' '.join(extras)}"
            
            # Draw tree structure
            connector = "└── " if is_last else "├── "
            lines.append(prefix + connector + info)
            
            # Recurse children
            child_prefix = prefix + ("    " if is_last else "│   ")
            for i, child in enumerate(node.children):
                _traverse(child, child_prefix, i == len(node.children) - 1)
        
        # Root node special handling
        lines.append(f"{self.root.name} ({self.root.node_type}) [root]")
        for i, child in enumerate(self.root.children):
            _traverse(child, "", i == len(self.root.children) - 1)
        
        return "\n".join(lines)
    
    def generate_tscn(self) -> str:
        """Generate .tscn text"""
        if not self.root:
            raise ValueError("No root node created")
        
        # Resolve initial_state references
        self._resolve_initial_states(self.root)
        
        # Collect external resources
        self._collect_ext_resources(self.root)
        
        lines = []
        
        # Generate unique scene UID (different from entity script UID)
        scene_uid = f"uid://c{random.randint(100000000, 999999999):09x}"
        
        # Calculate load_steps: ext_resources + sub_resources
        load_steps = len(self.ext_resources)
        if self.root.node_type == "CharacterBody3D":
            load_steps += 1  # Add 1 for CapsuleShape3D sub_resource
        
        # File header
        lines.append(f'[gd_scene load_steps={load_steps} format=3 {scene_uid}]')
        lines.append("")
        
        # External resources (use simple numeric IDs)
        for idx, res in enumerate(self.ext_resources, start=1):
            lines.append(f'[ext_resource type="{res["type"]}" path="{res["path"]}" id="{idx}"]')
        
        if self.ext_resources:
            lines.append("")
        
        # SubResources (if any, like CollisionShape)
        if self.root.node_type == "CharacterBody3D":
            lines.append('[sub_resource type="CapsuleShape3D" id="CapsuleShape3D_1"]')
            lines.append('radius = 0.5')
            lines.append('height = 2.0')
            lines.append("")
        
        # Node definitions
        def _write_node(node: StateChartNode, ext_resource_map: dict):
            # Node header
            if node == self.root:
                lines.append(f'[node name="{node.name}" type="{node.node_type}"]')
            else:
                lines.append(f'[node name="{node.name}" type="{node.node_type}" parent="{node.parent_path}"]')
            
            # Properties
            for key, value in node.properties.items():
                # Skip internal properties
                if key.startswith("_"):
                    continue
                
                # Handle script references
                if key == "script":
                    if "_entity_script_path" in node.properties:
                        script_path = node.properties["_entity_script_path"]
                        res_id = ext_resource_map.get(script_path, "1")
                        lines.append(f'script = ExtResource("{res_id}")')
                    elif "_script_path" in node.properties:
                        script_path = node.properties["_script_path"]
                        res_id = ext_resource_map.get(script_path, "2")
                        lines.append(f'script = ExtResource("{res_id}")')
                    elif "_component_script_path" in node.properties:
                        script_path = node.properties["_component_script_path"]
                        res_id = ext_resource_map.get(script_path, "5")
                        lines.append(f'script = ExtResource("{res_id}")')
                    continue
                
                # Write other properties
                if isinstance(value, str):
                    lines.append(f"{key} = {value}")
                elif isinstance(value, (int, float)):
                    lines.append(f"{key} = {value}")
                else:
                    lines.append(f"{key} = {value}")
            
            lines.append("")
            
            # Recurse children
            for child in node.children:
                _write_node(child, ext_resource_map)
        
        # Create resource path to ID mapping
        ext_resource_map = {res["path"]: str(idx) for idx, res in enumerate(self.ext_resources, start=1)}
        
        # Write root node first
        _write_node(self.root, ext_resource_map)
        
        # Add CollisionShape3D after root entity (if CharacterBody3D)
        if self.root.node_type == "CharacterBody3D":
            lines.append(f'[node name="CollisionShape3D" type="CollisionShape3D" parent="."]')
            lines.append('transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0)')
            lines.append('shape = SubResource("CapsuleShape3D_1")')
            lines.append("")
        
        return "\n".join(lines)
    
    def save(self, output_path: str):
        """Save to file"""
        content = self.generate_tscn()
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ StateChart saved to: {output_path}")
