# Godot Object Pool Research

## Repositories Studied

### 1. [Chickensoft - LogicBlocks / Collections] (C#)
- **Status**: High-quality C# ecosystem for Godot.
- **Approach**: Likely uses standard C# `ObjectPool<T>` or a custom wrapper for Godot Nodes.
- **Pros**: Type-safe (Generics), clean architecture.
- **Cons**: Might be overly complex for simple bullet pooling.

### 2. [BulletUpHell] (GDScript/Plugin)
- **Stars**: ~500+
- **Context**: A specialized bullet hell plugin.
- **Approach**: Uses highly optimized custom pooling for thousands of bullets.
- **Structure**: Uses a dedicated `BulletManager` (Autoload) and `PackedScene` arrays.

### 3. [Godot-Object-Pool] (Various)
- **Pattern**: `PoolManager` Autoload.
- **Logic**: Dictionary mapping `String` (ID or path) to `Array` (available objects).
- **Functions**: `get_obj(scene_path)`, `return_obj(instance)`.

## Structural Patterns Analysis

### A. The "Singleton Manager" (Autoload)
- **Pros**: Accessible from anywhere (`PoolManager.spawn(...)`).
- **Cons**: Global state management can get messy if not handled correctly.

### B. The "Node-Parent" Pool
- **Pros**: Logical grouping in the scene tree. Good for local scene reuse.
- **Cons**: Need to pass references to the pooler everywhere.

### C. The "Resource-Based" Pool
- **Pros**: Can be shared across different scenes as a `.tres`.
- **Cons**: Harder to manage `Node` lifecycles (which are not resources).

## Next Steps
- Find the specific C# implementation details for Chickensoft or similar "Premium" C# Godot libs.
- Compare "Pre-instantiation" vs "On-demand growth".
- Analyze "Signal vs Interface" for resetting object state.
