"""
Godot .tscn File Editor Tools

Provides programmatic reading and modification of Godot .tscn scene files.
"""

from .parser import Parser
from .node_tree import Node_Tree
from .pretty_printer import Pretty_Printer
from .TscnReader import TscnReader
from .TscnEditor import TscnEditor, UIDGenerator
from .types import (
    Color,
    Vector2,
    NodePath,
    ExtResourceRef,
    Header,
    ExtResource,
    Node,
    ParseError,
    EditorError,
    PropertyUpdate,
    BatchResult,
)

__all__ = [
    "Parser",
    "Node_Tree",
    "Pretty_Printer",
    "TscnReader",
    "TscnEditor",
    "UIDGenerator",
    "Color",
    "Vector2",
    "NodePath",
    "ExtResourceRef",
    "Header",
    "ExtResource",
    "Node",
    "ParseError",
    "EditorError",
    "PropertyUpdate",
    "BatchResult",
]
