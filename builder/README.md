# TSCN Builder - Component-Based Architecture

A modular Python framework for programmatically generating Godot `.tscn` scene files using Composition over Inheritance.

## Architecture Overview

```
builder/
├── core.py              # TscnBuilder - Core scene structure manager
├── modules/
│   ├── ui.py           # UIModule - Control nodes, layouts, anchors
│   └── statechart.py   # StateChartModule - StateChart components
└── examples/           # Usage demonstrations
```

## Design Pattern: Builder + Plugin

- **Core Builder (`TscnBuilder`)**: Manages underlying `.tscn` file structure (ext_resource, sub_resource, node tree)
- **Component Modules**: Independent plugins that append specialized nodes to a TscnBuilder instance
- **True Composition**: Mix and match modules freely - UI only, StateChart only, or both

## Quick Start

### 1. UI Only Scene

```python
from builder.core import TscnBuilder
from builder.modules.ui import UIModule

scene = TscnBuilder(root_name="SettingsMenu", root_type="Control")
ui = UIModule(scene)
ui.setup_fullscreen_control()

margin = ui.add_margin_container("MainMargin", uniform=20)
ui.add_label("Title", parent="MainMargin", text="Settings", font_size=32)
ui.add_button("ApplyButton", parent="MainMargin", text="Apply")

scene.save("SettingsMenu.tscn")
```

### 2. StateChart Only Scene

```python
from builder.core import TscnBuilder
from builder.modules.statechart import StateChartModule

scene = TscnBuilder(root_name="Player", root_type="CharacterBody3D")
scene.initialize_root()

sc = StateChartModule(scene, parent=".")
sc.add_statechart("StateChart")

root = sc.add_compound_state("Root", parent="StateChart", initial_state="Idle")
sc.add_atomic_state("Idle", parent="Root")
sc.add_atomic_state("Walking", parent="Root")

sc.add_transition("ToWalking", from_state="Idle", to_state="Walking", event="move_start")
sc.resolve_initial_states()

scene.save("PlayerStateChart.tscn")
```

### 3. Combined Scene (UI + StateChart)

```python
from builder.core import TscnBuilder
from builder.modules.ui import UIModule
from builder.modules.statechart import StateChartModule

scene = TscnBuilder(root_name="ItemEntity", root_type="Control")

# Add UI
ui = UIModule(scene)
ui.setup_fullscreen_control()
ui.add_texture_rect("ItemIcon", parent=".")
ui.add_label("ItemName", parent=".", text="Sword")

# Add StateChart
sc = StateChartModule(scene, parent=".")
sc.add_statechart("StateChart")
root = sc.add_compound_state("Root", parent="StateChart", initial_state="Idle")
sc.add_atomic_state("Idle", parent="Root")
sc.add_atomic_state("Dragging", parent="Root")
sc.add_transition("ToDragging", from_state="Idle", to_state="Dragging", event="drag_start")
sc.resolve_initial_states()

scene.save("ItemEntity.tscn")
```

## Core API Reference

### TscnBuilder

```python
TscnBuilder(root_name: str, root_type: str, scene_uid: Optional[str] = None)
```

Core methods:
- `initialize_root(**properties)` - Create root node with properties
- `add_node(name, node_type, parent=".", **properties)` - Add generic node
- `get_node(name)` - Retrieve node by name
- `add_ext_resource(type, path, uid, id=None)` - Register external resource
- `add_sub_resource(type, id, **properties)` - Register sub-resource
- `assign_node_path(target_node_name, property_name, path_to_node_name)` - Bind UI node to C# [Export] property
- `assign_multiple_node_paths(target_node_name, bindings)` - Batch bind multiple UI nodes
- `generate_tree_view()` - Generate ASCII tree for inspection
- `save(output_path)` - Export to .tscn file

### UIModule

```python
UIModule(builder: TscnBuilder)
```

Container methods:
- `add_margin_container(name, parent=".", uniform=None, ...)`
- `add_panel_container(name, parent=".")`
- `add_scroll_container(name, parent=".", ...)`
- `add_vbox(name, parent=".", separation=None)`
- `add_hbox(name, parent=".", separation=None)`

Control methods:
- `add_label(name, parent=".", text="", align="left", ...)`
- `add_button(name, parent=".", text="", ...)`
- `add_checkbox(name, parent=".", text="", ...)`
- `add_progress_bar(name, parent=".", value=0, ...)`
- `add_color_rect(name, parent=".", color=(0.15, 0.15, 0.15, 1), ...)`
- `add_texture_rect(name, parent=".", texture_path=None, ...)`
- `add_instance(name, parent=".", scene_path="", scene_uid="")`
- `add_separator(name, parent=".", ...)`

### StateChartModule

```python
StateChartModule(builder: TscnBuilder, parent: str = ".")
```

State methods:
- `add_statechart(name="StateChart")` - Add StateChart root
- `add_parallel_state(name, parent)` - Simultaneous active states
- `add_compound_state(name, parent, initial_state=None)` - Mutually exclusive states
- `add_atomic_state(name, parent)` - Leaf state

Transition methods:
- `add_transition(name, from_state, to_state, event="", delay=0.0)`
- `add_expression_guard(name, parent, expression)`

Component methods:
- `add_component(name, parent, script_path, script_uid)`
- `resolve_initial_states()` - Call after building state tree

## Key Features

### 1. Automatic NodePath Resolution

Modules automatically calculate relative NodePaths (e.g., `../../FlyMode`) - no manual path calculation needed.

### 2. C# Export Property Binding (Killer Feature)

Automatically bind UI nodes to C# Controller [Export] properties without manual NodePath calculation:

```python
# Create UI
ui.add_button("ApplyButton", parent="MainVBox", text="Apply")

# Create C# Controller
scene.add_node("SettingsController", "Node", parent=".",
              script=ExtResource("controller_script"))

# Automatically bind button to controller's [Export] property
scene.assign_node_path("SettingsController", "ApplyButton", "ApplyButton")

# Or batch bind multiple controls
scene.assign_multiple_node_paths("SettingsController", {
    "ApplyButton": "ApplyButton",
    "CancelButton": "CancelButton",
    "VolumeSlider": "VolumeSlider"
})
```

Generated TSCN:
```gdscript
[node name="SettingsController" type="Node" parent="."]
script = ExtResource("1_res")
ApplyButton = NodePath("../MainVBox/ApplyButton")
CancelButton = NodePath("../MainVBox/CancelButton")
VolumeSlider = NodePath("../MainVBox/VolumeSlider")
```

In your C# Controller:
```csharp
[Export] public NodePath ApplyButton { get; set; }
[Export] public NodePath CancelButton { get; set; }
[Export] public NodePath VolumeSlider { get; set; }

public override void _Ready()
{
    InitializeComponent();
    
    // Pure C# events with R3 reactive extensions
    GetNode<Button>(ApplyButton).OnPressedAsObservable()
        .Subscribe(_ => ApplySettings())
        .AddTo(_disposables);
}
```

### 3. Node Registry

All nodes are registered by name for easy cross-referencing:

```python
ui.add_vbox("MainVBox", parent=".")
ui.add_label("Title", parent="MainVBox")  # Reference by name
```

### 4. Resource Management

External resources (scripts, textures, scenes) are automatically deduplicated and assigned IDs.

### 5. Tree Visualization

```python
print(scene.generate_tree_view())
```

Output:
```
ItemEntity (Control) [root]
└── ItemIcon (TextureRect)
└── StateChart (Node) [script]
    └── Root (Node) [script]
        ├── Idle (Node) [script]
        └── Dragging (Node) [script]
```

## Migration from Legacy Builders

### Old (godot_ui_builder.py)
```python
builder = UIBuilder("SettingsMenu")
root = builder.create_control()
margin = root.add_margin_container("MainMargin", uniform=20)
```

### New (Component-Based)
```python
scene = TscnBuilder(root_name="SettingsMenu", root_type="Control")
ui = UIModule(scene)
ui.setup_fullscreen_control()
margin = ui.add_margin_container("MainMargin", uniform=20)
```

### Old (godot_statechart_builder.py)
```python
builder = StateChartBuilder("Player", "CharacterBody3D")
statechart = builder.create_entity_with_statechart()
root = statechart.add_compound_state("Root")
```

### New (Component-Based)
```python
scene = TscnBuilder(root_name="Player", root_type="CharacterBody3D")
scene.initialize_root()
sc = StateChartModule(scene, parent=".")
sc.add_statechart("StateChart")
root = sc.add_compound_state("Root", parent="StateChart")
```

## Extending with Custom Modules

Create new modules following the same pattern:

```python
class PhysicsModule:
    def __init__(self, builder: TscnBuilder):
        self.builder = builder
    
    def add_collision_shape(self, name: str, parent: str = ".", shape_type: str = "CapsuleShape3D"):
        # Add sub-resource
        shape_id = self.builder.add_sub_resource(shape_type, f"{shape_type}_1")
        
        # Add node
        return self.builder.add_node(
            name, "CollisionShape3D",
            parent=parent,
            shape=f'SubResource("{shape_id}")'
        )
```

Usage:
```python
scene = TscnBuilder(root_name="Player", root_type="CharacterBody3D")
scene.initialize_root()

physics = PhysicsModule(scene)
physics.add_collision_shape("Collider", parent=".")

scene.save("Player.tscn")
```

## Best Practices

1. **Always initialize root first**: Call `initialize_root()` or use a module's setup method
2. **Use parent names, not paths**: Reference nodes by name, not full paths
3. **Resolve StateChart initial states**: Call `sc.resolve_initial_states()` after building state tree
4. **Inspect before saving**: Use `generate_tree_view()` to verify structure
5. **Obtain UIDs correctly**: Use `mcp_godot_get_uid` for scene instances and resources

## Examples

See `builder/examples/` for complete working examples:
- `example_ui_only.py` - Settings menu with UI components
- `example_statechart_only.py` - Player with state machine
- `example_combined.py` - Draggable item with UI + StateChart
- `example_csharp_export_binding.py` - C# MVC pattern with automatic [Export] property binding
