# Migration Guide: Legacy Builders → Component-Based Architecture

This guide helps you migrate from the old isolated builders to the new modular system.

## Key Architectural Changes

### Before (Isolated Systems)
- `godot_ui_builder.py` - Standalone UI generator
- `godot_statechart_builder.py` - Standalone StateChart generator
- **Problem**: Cannot combine UI + StateChart in a single scene

### After (Component-Based)
- `builder/core.py` - Core TSCN structure manager
- `builder/modules/ui.py` - UI plugin module
- `builder/modules/statechart.py` - StateChart plugin module
- **Solution**: True composition - mix and match freely

## Migration Patterns

### Pattern 1: UI Scene Migration

#### Old Code (godot_ui_builder.py)
```python
from godot_ui_builder import UIBuilder

builder = UIBuilder("SettingsMenu")
root = builder.create_control()

margin = root.add_margin_container("MainMargin", uniform=20)
vbox = margin.add_vbox("MainVBox", separation=10)
vbox.add_label("Title", text="Settings", font_size=32)
vbox.add_button("ApplyButton", text="Apply")

builder.save("SettingsMenu.tscn")
```

#### New Code (Component-Based)
```python
from builder.core import TscnBuilder
from builder.modules.ui import UIModule

scene = TscnBuilder(root_name="SettingsMenu", root_type="Control")
ui = UIModule(scene)
ui.setup_fullscreen_control()

ui.add_margin_container("MainMargin", parent=".", uniform=20)
ui.add_vbox("MainVBox", parent="MainMargin", separation=10)
ui.add_label("Title", parent="MainVBox", text="Settings", font_size=32)
ui.add_button("ApplyButton", parent="MainVBox", text="Apply")

scene.save("SettingsMenu.tscn")
```

**Key Changes**:
1. Import from `builder.core` and `builder.modules.ui`
2. Create `TscnBuilder` instead of `UIBuilder`
3. Instantiate `UIModule(scene)`
4. Use `parent="NodeName"` instead of chaining methods
5. Call `scene.save()` instead of `builder.save()`

### Pattern 2: StateChart Scene Migration

#### Old Code (godot_statechart_builder.py)
```python
from godot_statechart_builder import StateChartBuilder

builder = StateChartBuilder("Player", "CharacterBody3D")
statechart = builder.create_entity_with_statechart()

root = statechart.add_compound_state("Root")
idle = root.add_atomic_state("Idle")
walking = root.add_atomic_state("Walking")

idle.add_transition("ToWalking", walking, event="move_start")

builder.save("Player.tscn")
```

#### New Code (Component-Based)
```python
from builder.core import TscnBuilder
from builder.modules.statechart import StateChartModule

scene = TscnBuilder(root_name="Player", root_type="CharacterBody3D")
scene.initialize_root()

sc = StateChartModule(scene, parent=".")
sc.add_statechart("StateChart")

sc.add_compound_state("Root", parent="StateChart", initial_state="Idle")
sc.add_atomic_state("Idle", parent="Root")
sc.add_atomic_state("Walking", parent="Root")

sc.add_transition("ToWalking", from_state="Idle", to_state="Walking", event="move_start")
sc.resolve_initial_states()

scene.save("Player.tscn")
```

**Key Changes**:
1. Import from `builder.core` and `builder.modules.statechart`
2. Create `TscnBuilder` instead of `StateChartBuilder`
3. Call `scene.initialize_root()` explicitly
4. Instantiate `StateChartModule(scene, parent=".")`
5. Use `parent="NodeName"` instead of chaining methods
6. Use `from_state` and `to_state` parameters for transitions
7. Call `sc.resolve_initial_states()` before saving

### Pattern 3: Combined Scene (NEW CAPABILITY)

This was **impossible** with the old architecture:

```python
from builder.core import TscnBuilder
from builder.modules.ui import UIModule
from builder.modules.statechart import StateChartModule

# Initialize scene
scene = TscnBuilder(root_name="ItemEntity", root_type="Control")

# Add UI components
ui = UIModule(scene)
ui.setup_fullscreen_control()
ui.add_texture_rect("ItemIcon", parent=".")
ui.add_label("ItemName", parent=".", text="Sword")

# Add StateChart components
sc = StateChartModule(scene, parent=".")
sc.add_statechart("StateChart")
root = sc.add_compound_state("Root", parent="StateChart", initial_state="Idle")
sc.add_atomic_state("Idle", parent="Root")
sc.add_atomic_state("Dragging", parent="Root")
sc.add_transition("ToDragging", from_state="Idle", to_state="Dragging", event="drag_start")
sc.resolve_initial_states()

# Export unified scene
scene.save("ItemEntity.tscn")
```

## API Mapping Reference

### UIBuilder → UIModule

| Old Method | New Method | Notes |
|------------|------------|-------|
| `UIBuilder(name)` | `TscnBuilder(root_name=name, root_type="Control")` + `UIModule(scene)` | Split into core + module |
| `builder.create_control()` | `ui.setup_fullscreen_control()` | Returns root node |
| `node.add_margin_container(...)` | `ui.add_margin_container(..., parent="NodeName")` | Explicit parent parameter |
| `node.add_vbox(...)` | `ui.add_vbox(..., parent="NodeName")` | Explicit parent parameter |
| `node.add_label(...)` | `ui.add_label(..., parent="NodeName")` | Explicit parent parameter |
| `node.add_button(...)` | `ui.add_button(..., parent="NodeName")` | Explicit parent parameter |
| `builder.save(path)` | `scene.save(path)` | Called on TscnBuilder |

### StateChartBuilder → StateChartModule

| Old Method | New Method | Notes |
|------------|------------|-------|
| `StateChartBuilder(name, type)` | `TscnBuilder(root_name=name, root_type=type)` + `StateChartModule(scene)` | Split into core + module |
| `builder.create_entity_with_statechart()` | `scene.initialize_root()` + `sc.add_statechart("StateChart")` | Explicit steps |
| `node.add_compound_state(name)` | `sc.add_compound_state(name, parent="ParentName")` | Explicit parent parameter |
| `node.add_atomic_state(name)` | `sc.add_atomic_state(name, parent="ParentName")` | Explicit parent parameter |
| `node.add_transition(name, target, event)` | `sc.add_transition(name, from_state="Source", to_state="Target", event=event)` | Explicit from/to parameters |
| `builder.save(path)` | `sc.resolve_initial_states()` + `scene.save(path)` | Must resolve states first |

## Common Migration Issues

### Issue 1: Chained Method Calls

**Old (Chaining)**:
```python
root = builder.create_control()
margin = root.add_margin_container("Margin")
vbox = margin.add_vbox("VBox")
vbox.add_label("Label", text="Hello")
```

**New (Explicit Parents)**:
```python
ui.setup_fullscreen_control()
ui.add_margin_container("Margin", parent=".")
ui.add_vbox("VBox", parent="Margin")
ui.add_label("Label", parent="VBox", text="Hello")
```

**Why**: The new architecture uses a flat node registry instead of nested object references.

### Issue 2: Transition Target References

**Old (Object References)**:
```python
idle = root.add_atomic_state("Idle")
walking = root.add_atomic_state("Walking")
idle.add_transition("ToWalking", walking, event="move")
```

**New (String Names)**:
```python
sc.add_atomic_state("Idle", parent="Root")
sc.add_atomic_state("Walking", parent="Root")
sc.add_transition("ToWalking", from_state="Idle", to_state="Walking", event="move")
```

**Why**: The module uses the node registry to resolve references by name.

### Issue 3: Initial State Resolution

**Old (Automatic)**:
```python
root = statechart.add_compound_state("Root")
idle = root.add_atomic_state("Idle")
# Initial state automatically set
```

**New (Explicit)**:
```python
sc.add_compound_state("Root", parent="StateChart", initial_state="Idle")
sc.add_atomic_state("Idle", parent="Root")
sc.resolve_initial_states()  # MUST call this
```

**Why**: Deferred resolution allows flexible state tree construction.

## Step-by-Step Migration Checklist

1. **Update imports**:
   - Replace `from godot_ui_builder import UIBuilder` with `from builder.core import TscnBuilder` and `from builder.modules.ui import UIModule`
   - Replace `from godot_statechart_builder import StateChartBuilder` with `from builder.core import TscnBuilder` and `from builder.modules.statechart import StateChartModule`

2. **Replace builder initialization**:
   - UI: `UIBuilder(name)` → `TscnBuilder(root_name=name, root_type="Control")` + `UIModule(scene)`
   - StateChart: `StateChartBuilder(name, type)` → `TscnBuilder(root_name=name, root_type=type)` + `StateChartModule(scene)`

3. **Convert chained calls to explicit parents**:
   - Change `parent_node.add_child(...)` to `module.add_child(..., parent="ParentName")`

4. **Update transition syntax**:
   - Change `source.add_transition(name, target, event)` to `sc.add_transition(name, from_state="Source", to_state="Target", event=event)`

5. **Add state resolution**:
   - Call `sc.resolve_initial_states()` before `scene.save()`

6. **Test generation**:
   - Run your script and verify the tree view with `print(scene.generate_tree_view())`
   - Open the generated `.tscn` file in Godot to confirm structure

## Benefits of Migration

1. **Composition**: Combine UI + StateChart in a single scene
2. **Modularity**: Add custom modules without modifying core
3. **Clarity**: Explicit parent references instead of nested objects
4. **Flexibility**: Mix and match modules as needed
5. **Maintainability**: Separation of concerns between core and modules

## Need Help?

- See `builder/examples/` for complete working examples
- Read `builder/README.md` for full API documentation
- Check generated tree views with `scene.generate_tree_view()`
