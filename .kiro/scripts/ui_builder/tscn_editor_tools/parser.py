"""
Parser for Godot .tscn file format
"""

import re
from typing import Tuple, List, Any, Optional
from .types import Header, ExtResource, Node, ParseError, Color, Vector2, NodePath, ExtResourceRef


class Parser:
    """Parses .tscn text format into structured data"""
    
    def __init__(self, content: str):
        self.lines = content.split('\n')
        self.current_line = 0
    
    def parse(self) -> Tuple[Header, List[ExtResource], List[Node]]:
        """Parse entire .tscn file and return structured data"""
        try:
            header = self._parse_header()
            ext_resources = self._parse_ext_resources()
            nodes = self._parse_nodes()
            return header, ext_resources, nodes
        except Exception as e:
            if isinstance(e, ParseError):
                raise
            raise ParseError(str(e), self.current_line + 1)
    
    def _parse_header(self) -> Header:
        """Parse [gd_scene format=X uid="..."] header"""
        if self.current_line >= len(self.lines):
            raise ParseError("Empty file", 1)
        
        line = self.lines[self.current_line].strip()
        self.current_line += 1
        
        # Match: [gd_scene format=3 uid="uid://..."]
        match = re.match(r'\[gd_scene\s+format=(\d+)\s+uid="([^"]+)"\]', line)
        if not match:
            raise ParseError(f"Invalid header format: {line}", self.current_line)
        
        format_version = int(match.group(1))
        scene_uid = match.group(2)
        
        return Header(format_version=format_version, scene_uid=scene_uid)
    
    def _parse_ext_resources(self) -> List[ExtResource]:
        """Parse all [ext_resource ...] sections"""
        ext_resources = []
        
        while self.current_line < len(self.lines):
            line = self.lines[self.current_line].strip()
            
            # Skip empty lines
            if not line:
                self.current_line += 1
                continue
            
            # Stop if we hit a node section
            if line.startswith('[node'):
                break
            
            # Parse ext_resource line
            if line.startswith('[ext_resource'):
                ext_resource = self._parse_ext_resource_line(line)
                ext_resources.append(ext_resource)
                self.current_line += 1
            else:
                self.current_line += 1
        
        return ext_resources
    
    def _parse_ext_resource_line(self, line: str) -> ExtResource:
        """Parse single [ext_resource type="..." uid="..." path="..." id="..."] line"""
        # Extract attributes using regex
        # Note: Use \s before id= to avoid matching "id" within "uid"
        type_match = re.search(r'type="([^"]+)"', line)
        uid_match = re.search(r'uid="([^"]+)"', line)
        path_match = re.search(r'path="([^"]+)"', line)
        id_match = re.search(r'\sid="([^"]+)"', line)
        
        if not (type_match and uid_match and path_match and id_match):
            raise ParseError(f"Invalid ext_resource format: {line}", self.current_line + 1)
        
        return ExtResource(
            resource_type=type_match.group(1),
            uid=uid_match.group(1),
            path=path_match.group(1),
            resource_id=id_match.group(1)
        )
    
    def _parse_nodes(self) -> List[Node]:
        """Parse all [node ...] sections with their properties"""
        nodes = []
        
        while self.current_line < len(self.lines):
            line = self.lines[self.current_line].strip()
            
            # Skip empty lines
            if not line:
                self.current_line += 1
                continue
            
            # Parse node section
            if line.startswith('[node'):
                node = self._parse_node_section(line)
                nodes.append(node)
            else:
                self.current_line += 1
        
        return nodes
    
    def _parse_node_section(self, header_line: str) -> Node:
        """Parse [node name="..." type="..." ...] and following properties"""
        # Extract node attributes
        name_match = re.search(r'name="([^"]+)"', header_line)
        type_match = re.search(r'type="([^"]+)"', header_line)
        parent_match = re.search(r'parent="([^"]+)"', header_line)
        unique_id_match = re.search(r'unique_id=(\d+)', header_line)
        instance_match = re.search(r'instance=ExtResource\("([^"]+)"\)', header_line)
        
        if not name_match:
            raise ParseError(f"Node missing name attribute: {header_line}", self.current_line + 1)
        
        name = name_match.group(1)
        node_type = type_match.group(1) if type_match else "Node"
        parent_path = parent_match.group(1) if parent_match else "."
        unique_id = int(unique_id_match.group(1)) if unique_id_match else 0
        
        # Check if this is a scene instance
        is_instance = instance_match is not None
        instance_resource_id = instance_match.group(1) if instance_match else None
        
        self.current_line += 1
        
        # Parse properties until next section or empty line
        properties = {}
        while self.current_line < len(self.lines):
            line = self.lines[self.current_line].strip()
            
            # Stop at next section or empty line followed by section
            if not line or line.startswith('['):
                break
            
            # Parse property line
            if '=' in line:
                key, value = self._parse_property_line(line)
                properties[key] = value
            
            self.current_line += 1
        
        node = Node(
            name=name,
            node_type=node_type,
            unique_id=unique_id,
            parent_path=parent_path,
            properties=properties,
            is_instance=is_instance
        )
        
        # Store instance metadata if applicable
        if is_instance and instance_resource_id:
            properties['_instance_resource_id'] = instance_resource_id
        
        return node
    
    def _parse_property_line(self, line: str) -> Tuple[str, Any]:
        """Parse property line: key = value"""
        if '=' not in line:
            raise ParseError(f"Invalid property syntax: {line}", self.current_line + 1)
        
        key, value_str = line.split('=', 1)
        key = key.strip()
        value_str = value_str.strip()
        
        value = self._parse_property_value(value_str)
        return key, value
    
    def _parse_property_value(self, value_str: str) -> Any:
        """Parse property value (string, number, Color(), Vector2(), etc.)"""
        value_str = value_str.strip()
        
        # Color(r, g, b, a)
        color_match = re.match(r'Color\(([\d.]+),\s*([\d.]+),\s*([\d.]+),\s*([\d.]+)\)', value_str)
        if color_match:
            return Color(
                r=float(color_match.group(1)),
                g=float(color_match.group(2)),
                b=float(color_match.group(3)),
                a=float(color_match.group(4))
            )
        
        # Vector2(x, y)
        vector2_match = re.match(r'Vector2\(([\d.]+),\s*([\d.]+)\)', value_str)
        if vector2_match:
            return Vector2(
                x=float(vector2_match.group(1)),
                y=float(vector2_match.group(2))
            )
        
        # NodePath("path")
        nodepath_match = re.match(r'NodePath\("([^"]+)"\)', value_str)
        if nodepath_match:
            return NodePath(path=nodepath_match.group(1))
        
        # ExtResource("id")
        extresource_match = re.match(r'ExtResource\("([^"]+)"\)', value_str)
        if extresource_match:
            return ExtResourceRef(resource_id=extresource_match.group(1))
        
        # String with quotes
        if value_str.startswith('"') and value_str.endswith('"'):
            return value_str[1:-1]  # Remove quotes
        
        # Boolean
        if value_str.lower() == 'true':
            return True
        if value_str.lower() == 'false':
            return False
        
        # Number (int or float)
        try:
            if '.' in value_str:
                return float(value_str)
            else:
                return int(value_str)
        except ValueError:
            pass
        
        # Return as-is if no pattern matches (e.g., PackedStringArray, etc.)
        return value_str
