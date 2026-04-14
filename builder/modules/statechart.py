"""
StateChart Module - Appends StateChart, CompoundState, and AtomicState nodes to TscnBuilder
"""

from typing import Optional
from ..core import TscnBuilder, TscnNode


class StateChartModule:
    """StateChart component generator that operates on a TscnBuilder instance"""
    
    # Script paths and UIDs for StateChart nodes
    SCRIPTS = {
        "StateChart": ("res://addons/godot_state_charts/state_chart.gd", "uid://couw105c3bde4"),
        "ParallelState": ("res://addons/godot_state_charts/parallel_state.gd", "uid://c1vp0ojjvaby1"),
        "CompoundState": ("res://addons/godot_state_charts/compound_state.gd", "uid://jk2jm1g6q853"),
        "AtomicState": ("res://addons/godot_state_charts/atomic_state.gd", "uid://cytafq8i1y8qm"),
        "Transition": ("res://addons/godot_state_charts/transition.gd", "uid://cf1nsco3w0mf6"),
        "ExpressionGuard": ("res://addons/godot_state_charts/expression_guard.gd", "uid://b4xy2kqvvx8yx"),
    }
    
    def __init__(self, builder: TscnBuilder, parent: str = "."):
        """Initialize StateChart module
        
        Args:
            builder: TscnBuilder instance to operate on
            parent: Parent node path for the StateChart root
        """
        self.builder = builder
        self.parent = parent
        self._pending_initial_states = {}
    
    def _add_script_resource(self, node_type: str) -> str:
        """Add StateChart script as external resource"""
        if node_type not in self.SCRIPTS:
            raise ValueError(f"Unknown StateChart node type: {node_type}")
        
        script_path, script_uid = self.SCRIPTS[node_type]
        res_id = self.builder.add_ext_resource("Script", script_path, script_uid, f"script_{node_type}")
        return res_id
    
    def add_statechart(self, name: str = "StateChart") -> TscnNode:
        """Add StateChart root node"""
        res_id = self._add_script_resource("StateChart")
        
        return self.builder.add_node(
            name, "Node",
            parent=self.parent,
            script=f'ExtResource("{res_id}")'
        )
    
    def add_parallel_state(self, name: str, parent: str) -> TscnNode:
        """Add ParallelState (allows simultaneous active child states)"""
        res_id = self._add_script_resource("ParallelState")
        
        return self.builder.add_node(
            name, "Node",
            parent=parent,
            script=f'ExtResource("{res_id}")'
        )
    
    def add_compound_state(self, name: str, parent: str, 
                          initial_state: Optional[str] = None) -> TscnNode:
        """Add CompoundState (mutually exclusive child states)
        
        Args:
            initial_state: Name of the initial child state (resolved after children are added)
        """
        res_id = self._add_script_resource("CompoundState")
        
        node = self.builder.add_node(
            name, "Node",
            parent=parent,
            script=f'ExtResource("{res_id}")'
        )
        
        if initial_state:
            self._pending_initial_states[name] = initial_state
        
        return node
    
    def add_atomic_state(self, name: str, parent: str) -> TscnNode:
        """Add AtomicState (leaf state, cannot have child states)"""
        res_id = self._add_script_resource("AtomicState")
        
        return self.builder.add_node(
            name, "Node",
            parent=parent,
            script=f'ExtResource("{res_id}")'
        )
    
    def add_transition(self, name: str, from_state: str, to_state: str,
                      event: str = "", delay: float = 0.0) -> TscnNode:
        """Add Transition (state change trigger)
        
        Args:
            name: Transition name
            from_state: Source state node name
            to_state: Target state node name
            event: Event name that triggers this transition
            delay: Delay in seconds before transition executes
        """
        res_id = self._add_script_resource("Transition")
        
        from_node = self.builder.get_node(from_state)
        to_node = self.builder.get_node(to_state)
        
        if from_node is None:
            raise ValueError(f"Source state '{from_state}' not found")
        if to_node is None:
            raise ValueError(f"Target state '{to_state}' not found")
        
        relative_path = from_node.get_relative_path_to(to_node)
        
        properties = {
            "script": f'ExtResource("{res_id}")',
            "to": f'NodePath("{relative_path}")',
            "delay_in_seconds": f'"{delay}"'
        }
        
        if event:
            properties["event"] = f'&"{event}"'
        
        return self.builder.add_node(name, "Node", parent=from_state, **properties)
    
    def add_expression_guard(self, name: str, parent: str, expression: str) -> TscnNode:
        """Add ExpressionGuard (condition check for transition)
        
        Args:
            name: Guard name
            parent: Parent transition node name
            expression: GDScript expression (e.g., "player_health > 50")
        """
        res_id = self._add_script_resource("ExpressionGuard")
        
        return self.builder.add_node(
            name, "Node",
            parent=parent,
            script=f'ExtResource("{res_id}")',
            expression=f'"{expression}"'
        )
    
    def add_component(self, name: str, parent: str, 
                     script_path: str, script_uid: str) -> TscnNode:
        """Add Component node (C# script attached to state)
        
        Args:
            name: Component name
            parent: Parent state node name
            script_path: Path to C# script
            script_uid: Script UID
        """
        res_id = self.builder.add_ext_resource("Script", script_path, script_uid, f"component_{name}")
        
        return self.builder.add_node(
            name, "Node",
            parent=parent,
            script=f'ExtResource("{res_id}")'
        )
    
    def resolve_initial_states(self):
        """Resolve initial_state NodePath references after tree is built"""
        for compound_name, initial_name in self._pending_initial_states.items():
            compound_node = self.builder.get_node(compound_name)
            initial_node = self.builder.get_node(initial_name)
            
            if compound_node and initial_node:
                relative_path = compound_node.get_relative_path_to(initial_node)
                compound_node.set_property("initial_state", f'NodePath("{relative_path}")')
