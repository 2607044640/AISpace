# Code Analysis: Godot _Ready() Initialization Order Problem

**Date**: 2026-04-18  
**Project**: Tesseract Backpack (TS)  
**Problem Domain**: Component initialization and dependency injection

## Problem Statement

### Current Pain Point
TSItemWrapper needs to pass `ItemDataResource Data` to its child `GridShapeComponent`, but Godot's lifecycle makes this awkward:

```
Godot Lifecycle Order:
1. _EnterTree() - Parent → Child (top-down)
2. _Ready()      - Child → Parent (bottom-up)
```

### Current Workaround (Ugly)
```csharp
// TSItemWrapper.cs
public override void _EnterTree()
{
    _shapeComponent = GetNodeOrNull<GridShapeComponent>("GridShapeComponent");
    _shapeComponent.Data = Data;  // Manually inject before child's _Ready()
}
```

### Why This Is Bad
1. **Tight Coupling**: Parent knows child's internal structure (`GridShapeComponent` name)
2. **Violates SRP**: Parent shouldn't manage child's initialization
3. **Fragile**: Breaks if child node is renamed or moved
4. **Not Scalable**: Imagine 10 properties to inject - nightmare!
5. **Violates Design Patterns**: Should use `[Export] NodePath` but that doesn't help with data injection

## Root Cause Analysis

### The Fundamental Problem
**Godot's _Ready() executes bottom-up (child first), but we need top-down data flow (parent data → child).**

This is a classic **Dependency Injection** problem:
- Parent has data (`ItemDataResource`)
- Child needs data to initialize properly
- But child's `_Ready()` runs before parent can inject

### Why _EnterTree Workaround Is Suboptimal
- Forces parent to know child's implementation details
- Requires manual `GetNode()` calls (violates `[Export] NodePath` pattern)
- No compile-time safety
- Hard to maintain as complexity grows

## Architectural Smell Detected

This pattern appears in multiple places:
- TSItemWrapper → GridShapeComponent
- Potentially other wrapper → component relationships

**Code Smell**: "Parent Knows Too Much About Children"

## Desired Solution Characteristics

1. **Declarative**: Use attributes like `[Inject]` or `[FromParent]`
2. **Type-Safe**: Compile-time checking
3. **Automatic**: No manual `GetNode()` calls
4. **Scalable**: Works for 1 property or 100 properties
5. **Godot-Native**: Integrates with Godot's lifecycle naturally

## Search Directions

1. **Dependency Injection Frameworks** for Godot C#
2. **Property Injection Patterns** (attribute-based)
3. **Service Locator Pattern** implementations
4. **Lazy Initialization** patterns
5. **Observer Pattern** for parent-child communication
6. **Source Generators** for automatic injection code

## Next Steps

1. Search for Godot C# DI frameworks
2. Evaluate attribute-based injection solutions
3. Consider building custom `[FromParent]` attribute with Source Generator
4. Document findings in PluginSearch file
