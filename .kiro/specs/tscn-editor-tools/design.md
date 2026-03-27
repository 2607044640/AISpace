# Design Document: tscn-editor-tools

## Overview

The tscn-editor-tools feature provides a Python library for programmatically reading and modifying Godot .tscn scene files. This addresses the fragility of text-based editing (strReplace) and the destructiveness of full regeneration (UIBuilder) by offering structured, safe modifications that preserve all existing content, formatting, UIDs, and references.

The library consists of two main components:
- **TscnReader**: A read-only parser and query interface for analyzing .tscn files
- **TscnEditor**: A modification interface that loads, edits, and saves .tscn files while preserving all metadata

This design enables safe batch updates to large .tscn files (10,800+ characters) without manual text manipulation or losing carefully configured properties.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Client Code                             │
│  (Python scripts, automation tools, batch processors)        │
└───────────────┬─────────────────────────────┬───────────────┘
                │                             │
                ▼                             ▼
    ┌───────────────────────┐   ┌───────────────────────┐
    │    TscnReader         │   │    TscnEditor         │
    │  (Read-only API)      │   │  (Modification API)   │
    └───────────┬───────────┘   └───────────┬───────────┘
                │                           │
                │                           │ uses
                │                           ▼
                │               ┌───────────────────────┐
                └──────────────►│      TscnReader       │
                                └───────────┬───────────┘
                                            │
                                            ▼
                        ┌───────────────────────────────────┐
                        │         Parser                    │
                        │  (Text → Node_Tree)               │
                        └───────────┬───────────────────────┘
                                    │
                                    ▼
                        ┌───────────────────────────────────┐
                        │       Node_Tree                   │
                        │  (Internal representation)        │
                        └───────────┬───────────────────────┘
                                    │
                                    ▼
                        ┌───────────────────────────────────┐
                        │      Pretty_Printer               │
                        │  (Node_Tree → Text)               │
                        └───────────────────────────────────┘
```

### Design Principles

1. **Immutability for Safety**: TscnReader provides read-only access; TscnEditor creates modified copies
2. **Preservation First**: All modifications preserve UIDs, formatting, and unreferenced content
3. **Structured Representation**: Internal tree structure enables reliable queries and modifications
4. **Round-Trip Fidelity**: Parse → Print → Parse produces equivalent structures
5. **Error Isolation**: Invalid operations return errors without modifying state

### Module Structure

```
tscn_editor_tools/
├── __init__.py
├── parser.py           # Text → Node_Tree conversion
├── node_tree.py        # Internal tree representation
├── pretty_printer.py   # Node_Tree → Text conversion
├── reader.py           # TscnReader (read-only API)
├── editor.py           # TscnEditor (modification API)
└── types.py            # Data classes and type definitions
```

## Components and Interfaces

### 1. Parser Component

**Responsibility**: Convert .tscn text format into structured Node_Tree representation

**Key Methods**:
```python
class Parser:
    def parse(self, tscn_text: str) -> Result[Node_Tree, ParseError]:
        """Parse .tscn text into Node_Tree structure"""
        
    def _parse_header(self, lines: List[str]) -> Result[Header, ParseError]:
        """Extract format version and scene UID"""
        
    def _parse_ext_resources(self, lines: List[str]) -> Result[List[ExtResource], ParseError]:
        """Parse [ext_resource] sections"""
        
    def _parse_nodes(self, lines: List[str]) -> Result[List[Node], ParseError]:
        """Parse [node] sections with properties"""
        
    def _parse_property_value(self, value: str) -> PropertyValue:
        """Parse property values (strings, numbers, Color(), Vector2(), etc.)"""
```

**Input Format** (INI-like structure):
```
[gd_scene format=3 uid="uid://bs256ppml668y"]

[ext_resource type="PackedScene" uid="uid://dbaix0lcy10v2" path="res://..." id="1_scene"]

[node name="NodeName" type="Control" unique_id=480540166]
property_key = "value"
color = Color(0.12, 0.12, 0.12, 1)
```

**Error Handling**:
- Returns `ParseError` with line number and description
- Validates section headers, property syntax, and value formats
- Handles malformed UIDs, missing quotes, and invalid constructors

### 2. Node_Tree Component

**Responsibility**: Internal representation of scene hierarchy with efficient queries

**Data Structure**:
```python
@dataclass
class Header:
    format_version: int
    scene_uid: str

@dataclass
class ExtResource:
    type: str
    uid: str
    path: str
    id: str

@dataclass
class Node:
    name: str
    type: str
    unique_id: int
    parent_path: str  # "." for root, "ParentName" for children
    properties: Dict[str, PropertyValue]
    is_instance: bool
    scene_path: Optional[str]  # For scene instances
    scene_uid: Optional[str]   # For scene instances

@dataclass
class Node_Tree:
    header: Header
    ext_resources: List[ExtResource]
    nodes: List[Node]  # Ordered as in file
    
    # Computed indices for fast lookup
    _node_by_path: Dict[str, Node]
    _nodes_by_type: Dict[str, List[Node]]
    _children_by_parent: Dict[str, List[Node]]
```

**Key Methods**:
```python
class Node_Tree:
    def get_node_by_path(self, path: str) -> Optional[Node]:
        """Get node by full path (e.g., 'Parent/Child')"""
        
    def get_nodes_by_type(self, node_type: str) -> List[Node]:
        """Get all nodes of specific type"""
        
    def get_children(self, parent_path: str) -> List[Node]:
        """Get direct children of a node"""
        
    def get_root_nodes(self) -> List[Node]:
        """Get all root nodes (parent='.')"""
        
    def build_full_path(self, node: Node) -> str:
        """Compute full path from root to node"""
```

### 3. Pretty_Printer Component

**Responsibility**: Convert Node_Tree back to valid .tscn text format

**Key Methods**:
```python
class Pretty_Printer:
    def print_tree(self, tree: Node_Tree) -> str:
        """Convert Node_Tree to .tscn text format"""
        
    def _print_header(self, header: Header) -> str:
        """Format: [gd_scene format=3 uid="..."]"""
        
    def _print_ext_resource(self, resource: ExtResource) -> str:
        """Format: [ext_resource type="..." uid="..." path="..." id="..."]"""
        
    def _print_node(self, node: Node) -> str:
        """Format node section with properties"""
        
    def _print_property(self, key: str, value: PropertyValue) -> str:
        """Format property with correct type syntax"""
```

**Formatting Rules**:
- Blank line after header
- Blank line between ext_resource sections
- Blank line before each node section
- Properties indented consistently
- Preserve original property value formatting (Color(), Vector2(), etc.)

### 4. TscnReader Component

**Responsibility**: Read-only API for querying .tscn files

**Public Interface**:
```python
class TscnReader:
    def __init__(self, tscn_path: str):
        """Load and parse .tscn file"""
        
    @property
    def tree(self) -> Node_Tree:
        """Access internal tree (read-only)"""
        
    def find_nodes_by_name(self, name: str) -> List[Node]:
        """Find nodes with exact name match"""
        
    def find_nodes_by_type(self, node_type: str) -> List[Node]:
        """Find all nodes of specific type"""
        
    def find_nodes_by_property(self, key: str, value: Any) -> List[Node]:
        """Find nodes where property matches value"""
        
    def get_node_property(self, node_path: str, key: str) -> Optional[PropertyValue]:
        """Get property value for specific node"""
        
    def get_node_properties(self, node_path: str) -> Dict[str, PropertyValue]:
        """Get all properties for specific node"""
        
    def node_exists(self, node_path: str) -> bool:
        """Check if node path exists"""
        
    def get_node_count_by_type(self, node_type: str) -> int:
        """Count nodes of specific type"""
        
    def list_ext_resources(self) -> List[ExtResource]:
        """Get all external resources"""
        
    def print_tree_view(self) -> str:
        """Generate human-readable tree visualization"""
```

**Tree View Format**:
```
SettingsMenuV2_Control (Control) [unique_id=480540166]
├── Background_ColorRect (ColorRect) [unique_id=1633307466]
│   └── color: Color(0.12, 0.12, 0.12, 1)
├── MainMargin_MarginContainer (MarginContainer) [unique_id=179320186]
│   └── MainVBox_VBoxContainer (VBoxContainer) [unique_id=1960884345]
│       ├── Tabs_TabContainer (TabContainer) [unique_id=1140248651]
│       │   ├── Audio (MarginContainer) [unique_id=1614754775]
│       │   │   └── MasterVolume [INSTANCE: res://A1UIScenes/UIComponents/SliderComponent.tscn]
│       │   └── Video (MarginContainer) [unique_id=1215484890]
│       └── ButtonsMargin_MarginContainer (MarginContainer) [unique_id=184188394]
```

### 5. TscnEditor Component

**Responsibility**: Modification API for editing .tscn files

**Public Interface**:
```python
class TscnEditor:
    def __init__(self, tscn_path: str):
        """Load .tscn file for editing"""
        
    @property
    def reader(self) -> TscnReader:
        """Access read-only query interface"""
        
    def update_property(self, node_path: str, key: str, value: PropertyValue) -> Result[None, EditorError]:
        """Update single property on specific node"""
        
    def update_properties_batch(self, updates: List[PropertyUpdate]) -> BatchResult:
        """Update multiple properties across multiple nodes"""
        
    def add_node(self, name: str, node_type: str, parent_path: str, 
                 properties: Dict[str, PropertyValue] = None) -> Result[Node, EditorError]:
        """Add new regular node"""
        
    def add_scene_instance(self, name: str, scene_path: str, parent_path: str,
                          properties: Dict[str, PropertyValue] = None) -> Result[Node, EditorError]:
        """Add scene instance node"""
        
    def remove_node(self, node_path: str) -> Result[None, EditorError]:
        """Remove node and all children"""
        
    def save(self, output_path: str = None) -> Result[None, EditorError]:
        """Save modifications to file (defaults to original path)"""
```

**Data Classes**:
```python
@dataclass
class PropertyUpdate:
    node_path: str
    key: str
    value: PropertyValue

@dataclass
class BatchResult:
    success_count: int
    errors: List[Tuple[PropertyUpdate, EditorError]]
```

**Modification Rules**:
1. All modifications create new Node_Tree (immutable updates)
2. Generate unique `unique_id` for new nodes (max existing + 1)
3. Preserve all UIDs for existing nodes
4. Add ext_resource entries for new scene instances
5. Validate parent paths before adding nodes
6. Prevent duplicate names under same parent
7. Prevent removing root nodes

## Data Models

### Property Value Types

```python
from typing import Union, List
from dataclasses import dataclass

# Simple types
PropertyValue = Union[str, int, float, bool, PropertyConstructor]

# Complex types (parsed from constructors)
@dataclass
class Color:
    r: float
    g: float
    b: float
    a: float
    
    def __str__(self) -> str:
        return f"Color({self.r}, {self.g}, {self.b}, {self.a})"

@dataclass
class Vector2:
    x: float
    y: float
    
    def __str__(self) -> str:
        return f"Vector2({self.x}, {self.y})"

@dataclass
class NodePath:
    path: str
    
    def __str__(self) -> str:
        return f'NodePath("{self.path}")'

@dataclass
class ExtResourceRef:
    id: str
    
    def __str__(self) -> str:
        return f'ExtResource("{self.id}")'

PropertyConstructor = Union[Color, Vector2, NodePath, ExtResourceRef]
```

### Error Types

```python
@dataclass
class ParseError:
    line_number: int
    message: str
    context: str  # Surrounding lines for debugging

@dataclass
class EditorError:
    error_type: str  # "NodeNotFound", "DuplicateName", "InvalidParent", etc.
    message: str
    node_path: Optional[str]

# Result type for error handling
Result = Union[Ok[T], Err[E]]
```

### UID Generation

```python
class UIDGenerator:
    def __init__(self, existing_ids: Set[int]):
        self.used_ids = existing_ids
        self.next_id = max(existing_ids) + 1 if existing_ids else 1
        
    def generate(self) -> int:
        """Generate unique ID not in existing set"""
        while self.next_id in self.used_ids:
            self.next_id += 1
        self.used_ids.add(self.next_id)
        return self.next_id
```

