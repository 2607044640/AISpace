# Requirements Document

## Introduction

The tscn-editor-tools feature provides programmatic tools for reading and modifying Godot .tscn files without losing existing content. This addresses the current pain point where strReplace is fragile (requires exact text matching) and UIBuilder regenerates entire files (losing manual configurations). The tools enable safe, targeted modifications to large .tscn files (10,800+ characters) while preserving all formatting, UIDs, and references.

## Glossary

- **TscnReader**: A parser that reads .tscn files and builds an internal tree representation
- **TscnEditor**: A modification tool that loads, edits, and saves .tscn files programmatically
- **Node_Tree**: The hierarchical structure of nodes within a .tscn scene
- **Property**: A key-value pair defining node attributes (e.g., text, color, position)
- **Scene_Instance**: A reference to an external .tscn file embedded as a node (prefab)
- **UID**: Unique identifier for nodes and external resources in Godot format
- **External_Resource**: Referenced files like scripts, textures, or scene instances
- **Parser**: The component that converts .tscn text format into structured data
- **Pretty_Printer**: The component that formats structured data back into valid .tscn text

## Requirements

### Requirement 1: Parse .tscn File Format

**User Story:** As a developer, I want to parse .tscn files into structured data, so that I can programmatically analyze and modify scene content.

#### Acceptance Criteria

1. WHEN a valid .tscn file is provided, THE Parser SHALL parse the file header including format version and scene UID
2. WHEN a valid .tscn file is provided, THE Parser SHALL extract all external resource declarations with type, UID, path, and ID
3. WHEN a valid .tscn file is provided, THE Parser SHALL parse all node sections including name, type, parent path, and unique_id
4. WHEN a valid .tscn file is provided, THE Parser SHALL extract all node properties as key-value pairs
5. WHEN a valid .tscn file is provided, THE Parser SHALL identify scene instance nodes with their referenced scene path and UID
6. WHEN an invalid .tscn file is provided, THE Parser SHALL return a descriptive error indicating the line number and issue
7. THE Parser SHALL handle INI-like section format with [node] and [ext_resource] headers
8. THE Parser SHALL preserve property value types including strings, numbers, Color(), Vector2(), NodePath(), and ExtResource() references

### Requirement 2: Build Internal Node Tree Representation

**User Story:** As a developer, I want an internal tree structure of the parsed scene, so that I can navigate and query the node hierarchy.

#### Acceptance Criteria

1. WHEN parsing completes, THE TscnReader SHALL construct a Node_Tree with parent-child relationships
2. THE Node_Tree SHALL store each node with its name, type, unique_id, parent reference, and properties dictionary
3. THE Node_Tree SHALL maintain the original node order as defined in the .tscn file
4. THE Node_Tree SHALL support root node identification (nodes with parent=".")
5. THE Node_Tree SHALL support child node lookup by parent path
6. THE Node_Tree SHALL preserve scene instance metadata including scene_path and scene_uid

### Requirement 3: Generate Human-Readable Tree View

**User Story:** As a developer, I want to visualize the scene hierarchy, so that I can understand the structure before making modifications.

#### Acceptance Criteria

1. THE TscnReader SHALL generate a tree view showing node hierarchy with indentation
2. THE Tree_View SHALL display node names, types, and parent-child relationships
3. THE Tree_View SHALL indicate scene instances with [INSTANCE: path] annotation
4. THE Tree_View SHALL show key properties like text values inline for quick reference
5. THE Tree_View SHALL use ASCII tree characters (├──, └──, │) for visual clarity
6. WHEN a node has a script attached, THE Tree_View SHALL display [script] annotation

### Requirement 4: Query API for Node and Property Lookup

**User Story:** As a developer, I want to query nodes by name or type, so that I can find specific elements to modify.

#### Acceptance Criteria

1. THE TscnReader SHALL provide a method to find nodes by exact name match
2. THE TscnReader SHALL provide a method to find nodes by type (e.g., all Button nodes)
3. THE TscnReader SHALL provide a method to find nodes by property value (e.g., text="Settings")
4. THE TscnReader SHALL provide a method to get all children of a specific node
5. THE TscnReader SHALL provide a method to get a node's full path from root
6. WHEN a query matches multiple nodes, THE TscnReader SHALL return all matches as a list
7. WHEN a query matches no nodes, THE TscnReader SHALL return an empty list

### Requirement 5: Load Existing .tscn Files

**User Story:** As a developer, I want to load existing .tscn files into TscnEditor, so that I can modify them without starting from scratch.

#### Acceptance Criteria

1. THE TscnEditor SHALL use TscnReader to parse the input .tscn file
2. WHEN loading succeeds, THE TscnEditor SHALL provide access to the Node_Tree
3. WHEN loading fails, THE TscnEditor SHALL return the Parser error without modifying any files
4. THE TscnEditor SHALL preserve all external resource declarations from the original file
5. THE TscnEditor SHALL maintain the original scene UID unless explicitly changed

### Requirement 6: Update Node Properties

**User Story:** As a developer, I want to modify node properties programmatically, so that I can batch update values like text or colors.

#### Acceptance Criteria

1. THE TscnEditor SHALL provide a method to update a single property on a specific node by node path
2. WHEN updating a property, THE TscnEditor SHALL preserve all other properties on that node
3. WHEN updating a property, THE TscnEditor SHALL preserve all other nodes in the scene
4. THE TscnEditor SHALL support updating string properties (e.g., text, name)
5. THE TscnEditor SHALL support updating numeric properties (e.g., value, font_size)
6. THE TscnEditor SHALL support updating complex properties (e.g., Color, Vector2, NodePath)
7. WHEN updating a non-existent property, THE TscnEditor SHALL add the property to the node
8. WHEN updating a property on a non-existent node, THE TscnEditor SHALL return an error without modifying the scene

### Requirement 7: Add New Nodes

**User Story:** As a developer, I want to add new nodes to existing scenes, so that I can extend UI layouts programmatically.

#### Acceptance Criteria

1. THE TscnEditor SHALL provide a method to add a new node with specified name, type, and parent path
2. WHEN adding a node, THE TscnEditor SHALL generate a unique unique_id value
3. WHEN adding a node, THE TscnEditor SHALL set the parent path correctly
4. THE TscnEditor SHALL support adding regular nodes (e.g., Button, Label)
5. THE TscnEditor SHALL support adding scene instances with scene_path and scene_uid
6. WHEN adding a scene instance, THE TscnEditor SHALL add the corresponding external resource if not already present
7. WHEN adding a node with duplicate name under same parent, THE TscnEditor SHALL return an error
8. THE TscnEditor SHALL allow setting initial properties when adding a node

### Requirement 8: Remove Nodes

**User Story:** As a developer, I want to remove nodes from scenes, so that I can clean up unused elements.

#### Acceptance Criteria

1. THE TscnEditor SHALL provide a method to remove a node by node path
2. WHEN removing a node, THE TscnEditor SHALL also remove all its children
3. WHEN removing a node, THE TscnEditor SHALL preserve all other nodes in the scene
4. WHEN removing a node, THE TscnEditor SHALL preserve all external resources (even if no longer referenced)
5. WHEN removing a non-existent node, THE TscnEditor SHALL return an error without modifying the scene
6. THE TscnEditor SHALL not allow removing the root node

### Requirement 9: Save Modifications to .tscn Format

**User Story:** As a developer, I want to save modified scenes back to .tscn format, so that Godot can load them correctly.

#### Acceptance Criteria

1. THE Pretty_Printer SHALL format the Node_Tree back into valid .tscn text format
2. THE Pretty_Printer SHALL preserve the original file header format
3. THE Pretty_Printer SHALL output external resources in the same format as the original
4. THE Pretty_Printer SHALL output node sections with correct INI-like formatting
5. THE Pretty_Printer SHALL preserve property formatting including quotes, parentheses, and type constructors
6. THE Pretty_Printer SHALL maintain node order from the Node_Tree
7. THE Pretty_Printer SHALL add blank lines between sections for readability
8. WHEN saving to a file path, THE TscnEditor SHALL write the Pretty_Printer output to disk

### Requirement 10: Preserve Formatting and References

**User Story:** As a developer, I want modifications to preserve all UIDs and formatting, so that Godot recognizes the file as unchanged except for my edits.

#### Acceptance Criteria

1. THE TscnEditor SHALL preserve all node unique_id values unless adding new nodes
2. THE TscnEditor SHALL preserve the scene UID in the file header
3. THE TscnEditor SHALL preserve all external resource UIDs
4. THE TscnEditor SHALL preserve ExtResource() references in properties
5. THE TscnEditor SHALL preserve NodePath() references in properties
6. THE TscnEditor SHALL preserve property value formatting (e.g., Color(0.12, 0.12, 0.12, 1))
7. THE TscnEditor SHALL preserve metadata properties (e.g., metadata/_tab_index)
8. FOR ALL valid .tscn files, parsing then printing then parsing SHALL produce an equivalent Node_Tree (round-trip property)

### Requirement 11: Batch Property Updates

**User Story:** As a developer, I want to update multiple properties across multiple nodes in one operation, so that I can efficiently modify scenes.

#### Acceptance Criteria

1. THE TscnEditor SHALL provide a method to update properties on multiple nodes matching a query
2. WHEN batch updating, THE TscnEditor SHALL apply changes to all matching nodes
3. WHEN batch updating, THE TscnEditor SHALL preserve all non-matching nodes unchanged
4. THE TscnEditor SHALL return the count of nodes modified by a batch operation
5. WHEN a batch operation fails on one node, THE TscnEditor SHALL continue processing remaining nodes and report all errors

### Requirement 12: Query Scene Structure Before Modifications

**User Story:** As a developer, I want to inspect scene structure before making changes, so that I can verify my modifications target the correct nodes.

#### Acceptance Criteria

1. THE TscnReader SHALL provide read-only access to the Node_Tree
2. THE TscnReader SHALL provide a method to get node count by type
3. THE TscnReader SHALL provide a method to list all external resources
4. THE TscnReader SHALL provide a method to check if a node path exists
5. THE TscnReader SHALL provide a method to get all property keys for a specific node
6. THE TscnReader SHALL provide a method to get a property value for a specific node

