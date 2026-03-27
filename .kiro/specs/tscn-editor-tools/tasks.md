# Implementation Plan: tscn-editor-tools

## Overview

This implementation plan creates a Python library for programmatically reading and modifying Godot .tscn scene files. The library provides structured, safe modifications that preserve all existing content, formatting, UIDs, and references. Implementation follows a bottom-up approach: build the parser and data structures first, then the reader API, and finally the editor API with modification capabilities.

## Tasks

- [x] 1. Set up project structure and core type definitions
  - Create directory `KiroWorkingSpace/.kiro/scripts/ui_builder/tscn_editor_tools/`
  - Create `__init__.py` to make it a Python package
  - Create `types.py` with all data classes (Header, ExtResource, Node, PropertyValue types, Error types)
  - Implement PropertyValue type classes (Color, Vector2, NodePath, ExtResourceRef) with `__str__` methods
  - Implement error classes (ParseError, EditorError)
  - _Requirements: 1.8, 9.6, 10.6_

- [x] 2. Implement Parser component for .tscn text parsing
  - [x] 2.1 Create parser.py with Parser class skeleton
    - Implement `parse()` method that orchestrates parsing workflow
    - Implement `_parse_header()` to extract format version and scene UID
    - _Requirements: 1.1_
  
  - [x] 2.2 Implement external resource parsing
    - Implement `_parse_ext_resources()` to extract type, UID, path, and ID
    - Handle multiple ext_resource sections
    - _Requirements: 1.2_
  
  - [x] 2.3 Implement node section parsing
    - Implement `_parse_nodes()` to extract node name, type, parent, unique_id
    - Parse node properties as key-value pairs
    - Identify scene instance nodes with scene_path and scene_uid
    - _Requirements: 1.3, 1.4, 1.5_
  
  - [x] 2.4 Implement property value parsing
    - Implement `_parse_property_value()` to handle strings, numbers, booleans
    - Parse Color() constructor with 4 float values
    - Parse Vector2() constructor with 2 float values
    - Parse NodePath() constructor with string path
    - Parse ExtResource() constructor with ID reference
    - _Requirements: 1.8_
  
  - [x] 2.5 Implement error handling and validation
    - Return ParseError with line number and descriptive message
    - Validate section headers ([gd_scene], [ext_resource], [node])
    - Validate property syntax (key = value)
    - Handle malformed UIDs, missing quotes, invalid constructors
    - _Requirements: 1.6, 1.7_

- [x] 3. Implement Node_Tree component for internal representation
  - [x] 3.1 Create node_tree.py with Node_Tree class
    - Implement Node_Tree dataclass with header, ext_resources, nodes
    - Build computed indices: _node_by_path, _nodes_by_type, _children_by_parent
    - _Requirements: 2.1, 2.2, 2.3_
  
  - [x] 3.2 Implement tree query methods
    - Implement `get_node_by_path()` for exact path lookup
    - Implement `get_nodes_by_type()` for type-based queries
    - Implement `get_children()` for parent-child lookup
    - Implement `get_root_nodes()` to find nodes with parent="."
    - Implement `build_full_path()` to compute full path from root
    - _Requirements: 2.4, 2.5_
  
  - [x] 3.3 Implement scene instance metadata preservation
    - Store is_instance, scene_path, scene_uid in Node dataclass
    - Preserve scene instance references during tree construction
    - _Requirements: 2.6_

- [x] 4. Checkpoint - Validate parser and tree construction
  - Test Parser with SettingsMenuV2.tscn (10,800 chars)
  - Verify all nodes, properties, and ext_resources are parsed correctly
  - Ensure all tests pass, ask the user if questions arise.

- [x] 5. Implement Pretty_Printer component for .tscn text generation
  - [x] 5.1 Create pretty_printer.py with Pretty_Printer class
    - Implement `print_tree()` method that orchestrates formatting
    - Implement `_print_header()` to format [gd_scene format=X uid="..."]
    - _Requirements: 9.1, 9.2_
  
  - [x] 5.2 Implement external resource formatting
    - Implement `_print_ext_resource()` with correct attribute order
    - Add blank lines between ext_resource sections
    - _Requirements: 9.3_
  
  - [x] 5.3 Implement node section formatting
    - Implement `_print_node()` with [node name="..." type="..." ...] format
    - Format properties with correct indentation
    - Add blank line before each node section
    - _Requirements: 9.4, 9.7_
  
  - [x] 5.4 Implement property value formatting
    - Implement `_print_property()` to format key = value pairs
    - Preserve Color(), Vector2(), NodePath(), ExtResource() constructor syntax
    - Preserve string quotes, numeric precision, boolean values
    - _Requirements: 9.5, 10.4, 10.5, 10.6_
  
  - [x] 5.5 Implement formatting consistency
    - Maintain node order from Node_Tree
    - Preserve metadata properties (e.g., metadata/_tab_index)
    - _Requirements: 9.6, 10.7_

- [ ]* 5.6 Write property test for round-trip consistency
  - **Property: Parse → Print → Parse produces equivalent Node_Tree**
  - **Validates: Requirements 10.8**
  - Test with various .tscn files including SettingsMenuV2.tscn
  - Verify all nodes, properties, UIDs, and ext_resources are preserved

- [x] 6. Implement TscnReader component for read-only queries
  - [x] 6.1 Create reader.py with TscnReader class
    - Implement `__init__()` to load and parse .tscn file using Parser
    - Implement `tree` property for read-only access to Node_Tree
    - Handle parse errors and propagate them to caller
    - _Requirements: 5.1, 5.2, 5.3, 12.1_
  
  - [x] 6.2 Implement node query methods
    - Implement `find_nodes_by_name()` for exact name matching
    - Implement `find_nodes_by_type()` using Node_Tree indices
    - Implement `find_nodes_by_property()` to filter by property value
    - Return empty list when no matches found
    - _Requirements: 4.1, 4.2, 4.3, 4.6, 4.7_
  
  - [x] 6.3 Implement property query methods
    - Implement `get_node_property()` to retrieve single property value
    - Implement `get_node_properties()` to get all properties for a node
    - Implement `node_exists()` to check path validity
    - _Requirements: 12.4, 12.5_
  
  - [x] 6.4 Implement metadata query methods
    - Implement `get_node_count_by_type()` for type statistics
    - Implement `list_ext_resources()` to enumerate external resources
    - _Requirements: 12.2, 12.3_
  
  - [x] 6.5 Implement tree visualization
    - Implement `print_tree_view()` to generate ASCII tree with indentation
    - Display node names, types, unique_ids
    - Show parent-child relationships with ├──, └──, │ characters
    - Annotate scene instances with [INSTANCE: path]
    - Show key properties inline (e.g., text values)
    - Annotate nodes with scripts using [script] marker
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

- [x] 7. Checkpoint - Validate TscnReader API
  - Test all query methods with SettingsMenuV2.tscn
  - Verify tree visualization output is readable and accurate
  - Ensure all tests pass, ask the user if questions arise.

- [x] 8. Implement TscnEditor component for modifications
  - [ ] 8.1 Create editor.py with TscnEditor class
    - Implement `__init__()` to load .tscn file using TscnReader
    - Implement `reader` property to expose read-only query interface
    - Store mutable copy of Node_Tree for modifications
    - _Requirements: 5.1, 5.4_
  
  - [ ] 8.2 Implement UID generation utility
    - Create UIDGenerator class with existing_ids tracking
    - Implement `generate()` to create unique IDs (max + 1 strategy)
    - Ensure generated IDs never collide with existing ones
    - _Requirements: 7.2_
  
  - [ ] 8.3 Implement single property update
    - Implement `update_property()` to modify one property on one node
    - Validate node path exists before updating
    - Preserve all other properties on the node
    - Preserve all other nodes in the scene
    - Add property if it doesn't exist
    - Return EditorError for non-existent nodes
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8_
  
  - [ ] 8.4 Implement batch property updates
    - Implement `update_properties_batch()` to handle multiple PropertyUpdate objects
    - Apply changes to all matching nodes
    - Preserve non-matching nodes unchanged
    - Return BatchResult with success_count and error list
    - Continue processing on individual failures
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_
  
  - [ ] 8.5 Implement add_node for regular nodes
    - Implement `add_node()` to create new nodes with name, type, parent_path
    - Generate unique unique_id using UIDGenerator
    - Set parent_path correctly
    - Support initial properties dictionary
    - Validate parent path exists
    - Return EditorError for duplicate names under same parent
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.7, 7.8_
  
  - [ ] 8.6 Implement add_scene_instance for scene instances
    - Implement `add_scene_instance()` to create scene instance nodes
    - Set is_instance=True, scene_path, scene_uid
    - Add corresponding ext_resource if not already present
    - Generate unique unique_id
    - _Requirements: 7.5, 7.6_
  
  - [ ] 8.7 Implement remove_node
    - Implement `remove_node()` to delete node by path
    - Remove all children recursively
    - Preserve all other nodes
    - Preserve all ext_resources (even if no longer referenced)
    - Return EditorError for non-existent nodes
    - Prevent removing root node
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6_
  
  - [ ] 8.8 Implement save method
    - Implement `save()` to write modifications to disk
    - Use Pretty_Printer to format Node_Tree
    - Default to original file path if output_path not specified
    - Preserve all UIDs, formatting, and references
    - _Requirements: 9.8, 10.1, 10.2, 10.3_

- [ ]* 8.9 Write unit tests for TscnEditor operations
  - Test update_property with various property types
  - Test add_node and add_scene_instance
  - Test remove_node with children
  - Test batch updates with mixed success/failure
  - Test save and reload cycle

- [ ] 9. Integration and documentation
  - [ ] 9.1 Update __init__.py with public API exports
    - Export TscnReader, TscnEditor classes
    - Export type classes (Color, Vector2, NodePath, ExtResourceRef)
    - Export error classes (ParseError, EditorError)
  
  - [ ] 9.2 Review InstructionDesignPrinciples.md
    - Read KiroWorkingSpace/.kiro/specs/tscn-editor-tools/InstructionDesignPrinciples.md if it exists
    - Ensure implementation follows any documented principles
  
  - [ ] 9.3 Update GodotUIBuilder.md documentation
    - Add section on tscn-editor-tools usage
    - Provide example: loading SettingsMenuV2.tscn, modifying properties, saving
    - Document when to use TscnEditor vs UIBuilder (modification vs generation)
    - Show tree visualization example
    - _Requirements: All_

- [ ] 10. Final validation checkpoint
  - Test complete workflow: load SettingsMenuV2.tscn → modify properties → save → reload
  - Verify Godot can load modified .tscn files without errors
  - Verify all UIDs and references are preserved
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Implementation uses Python with type hints for clarity and safety
- All file operations target `KiroWorkingSpace/.kiro/scripts/ui_builder/tscn_editor_tools/`
- SettingsMenuV2.tscn (10,800 chars) serves as primary validation test case
- Round-trip property (parse → print → parse) is critical for correctness
- Preservation of UIDs and formatting ensures Godot compatibility
