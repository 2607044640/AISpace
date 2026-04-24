"""
Core type definitions for .tscn file representation
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


# ===== Property Value Types =====

@dataclass
class Color:
    """Godot Color(r, g, b, a) property value"""
    r: float
    g: float
    b: float
    a: float
    
    def __str__(self) -> str:
        return f"Color({self.r}, {self.g}, {self.b}, {self.a})"


@dataclass
class Vector2:
    """Godot Vector2(x, y) property value"""
    x: float
    y: float
    
    def __str__(self) -> str:
        return f"Vector2({self.x}, {self.y})"


@dataclass
class NodePath:
    """Godot NodePath("path") property value"""
    path: str
    
    def __str__(self) -> str:
        return f'NodePath("{self.path}")'


@dataclass
class ExtResourceRef:
    """Godot ExtResource("id") property value"""
    resource_id: str
    
    def __str__(self) -> str:
        return f'ExtResource("{self.resource_id}")'


# ===== Core Data Structures =====

@dataclass
class Header:
    """Scene file header [gd_scene format=X uid="..."]"""
    format_version: int
    scene_uid: str


@dataclass
class ExtResource:
    """External resource declaration"""
    resource_type: str  # "Script", "PackedScene", "Texture2D", etc.
    uid: str           # "uid://..."
    path: str          # "res://..."
    resource_id: str   # "1_script", "2_scene", etc.


@dataclass
class Node:
    """Scene node with properties"""
    name: str
    node_type: str
    unique_id: int
    parent_path: str  # "." for root, "Parent/Child" for nested
    properties: Dict[str, Any] = field(default_factory=dict)
    
    # Scene instance metadata
    is_instance: bool = False
    scene_path: Optional[str] = None
    scene_uid: Optional[str] = None


# ===== Error Types =====

class ParseError(Exception):
    """Error during .tscn file parsing"""
    def __init__(self, message: str, line_number: Optional[int] = None):
        self.message = message
        self.line_number = line_number
        super().__init__(
            f"Parse error at line {line_number}: {message}" 
            if line_number else f"Parse error: {message}"
        )


class EditorError(Exception):
    """Error during .tscn file modification"""
    pass


# ===== Batch Operation Types =====

@dataclass
class PropertyUpdate:
    """Single property update operation"""
    node_path: str
    property_key: str
    property_value: Any


@dataclass
class BatchResult:
    """Result of batch property update operation"""
    success_count: int
    errors: List[str] = field(default_factory=list)
