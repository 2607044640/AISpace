# Component Design: GridShapeVisualComponent

**Date**: 2026-04-18  
**Project**: Tesseract Backpack (TS)  
**Component Type**: Visual + Interaction (Control-based)  
**Status**: ✅ IMPLEMENTED (Upgraded to Control with _HasPoint override)  
**Renamed From**: ItemShapeBlocksComponent → GridShapeVisualComponent  
**Architecture Upgrade**: Node → Control (to override _HasPoint)

## Design Overview

### Purpose

Generate precise 1x1 visual blocks for irregular tetris shapes AND implement pixel-perfect hit-testing by overriding Godot's `_HasPoint()` method.

### Critical Architecture Shift

**Problem**: MouseFilter routing is insufficient against Godot's native Rect2 AABB hit-testing for GuiInput.

**Solution**: GridShapeVisualComponent now **inherits from Control** and **acts as the InteractionArea itself**, overriding `_HasPoint()` for grid-based collision detection.

**Before (Node-based, FAILED)**:
```
InteractionArea (Control)
├── GridShapeVisualComponent (Node) - Sibling observer
└── ColorRect[] - Generated blocks
```

**After (Control-based, SUCCESS)**:
```
GridShapeVisualComponent (Control) - IS the interaction area
└── ColorRect[] - Generated blocks (MouseFilter.Ignore)
```

## Design Overview

### Purpose

Generate precise 1x1 visual/collision blocks for irregular tetris shapes, solving AABB bounding box limitations. Acts as the visual presentation layer for GridShapeComponent.

### Naming Philosophy: Logic-Visual Pairing

**CRITICAL NAMING CONVENTION**: Components with strong "data/logic" and "visual/presentation" binding MUST use prefix-aligned naming to establish immediate cognitive links.

**Pattern**: `[Domain][Aspect]Component`

**Example Pair**:
- `GridShapeComponent` - Logic/Data layer (manages shape state, rotation, normalization)
- `GridShapeVisualComponent` - Visual/Presentation layer (generates UI blocks, handles feedback)

**Why This Matters**:
- **Instant Recognition**: Developers immediately understand they're a matched pair
- **Scalability**: Pattern extends to other aspects (GridShapeSynergyComponent, GridShapeAudioComponent)
- **Maintainability**: Prevents "arbitrary naming hell" as project grows
- **Cognitive Efficiency**: No mental overhead mapping unrelated names

**Bad Naming (❌)**:
- `ItemShapeBlocksComponent` - Sounds like independent data entity
- No clear relationship to `GridShapeComponent`
- Arbitrary naming increases cognitive load

**Good Naming (✅)**:
- `GridShapeVisualComponent` - Clearly paired with `GridShapeComponent`
- Prefix alignment (`GridShape-`) makes relationship explicit
- Suffix (`Visual`) clarifies responsibility

### Responsibilities

1. **Visual Block Generation**: Create individual `ColorRect` nodes for each cell
2. **Reactive Synchronization**: Rebuild blocks when GridShapeComponent shape changes
3. **Validation Feedback**: Provide visual feedback for drag-and-drop states
4. **Precise Mouse Filtering**: Configure pixel-perfect mouse interaction per cell

## Critical Naming Rule

### Enforcement: Type-to-Variable Matching

**RULE**: Variables representing injected components or interfaces MUST strictly match their Type names (camelCase or PascalCase). Absolutely NO arbitrary aliases.

**Rationale**:
- Reduces cognitive load (no mental mapping)
- Improves code readability
- Ensures refactoring safety
- Maintains consistency across codebase

**Examples**:
```csharp
// ❌ BAD: Arbitrary aliases
[Export] public GridShapeComponent ShapeData { get; set; }
[Export] public Control VisualContainer { get; set; }

// ✅ GOOD: Type names
[Export] public GridShapeComponent GridShapeComponent { get; set; }
[Export] public Control InteractionArea { get; set; }
```

## Mounting Architecture

### Component Hierarchy

```
TSItem (Control) - implements IItemDataProvider
├── GridShapeComponent (Node) - Logic/Data
├── GridShapeVisualComponent (Node) - Visual/Presentation [SIBLING]
│   ├── References: GridShapeComponent
│   └── Targets: InteractionArea
└── InteractionArea (Control)
    └── [Generated ColorRect blocks]
```

### Mounting Strategy

**GridShapeVisualComponent mounts as a sibling to GridShapeComponent**:
- Both are child nodes of the ItemEntity (TSItem)
- GridShapeVisualComponent subscribes to GridShapeComponent's reactive streams
- Directly targets InteractionArea Control node for block placement
- Pure presentation layer - no data ownership

### Data Flow

```
IItemDataProvider (TSItemWrapper)
    ↓ event DataInitialized(ItemDataResource)
GridShapeComponent (Logic/Data)
    ↓ Receives Data via event subscription
    ↓ Initializes CurrentLocalCells from Data.BaseShape
    ↓ Emits OnShapeChangedAsObservable on rotation
GridShapeVisualComponent (Visual/Presentation)
    ↓ Subscribes to OnShapeChangedAsObservable
    ↓ Calls RebuildVisualBlocks()
    ↓ Iterates CurrentLocalCells
InteractionArea (MouseFilter.Ignore)
    └── ColorRect[] (MouseFilter.Pass for each cell)
```

### Key Integration Points

1. **IItemDataProvider**: Ultimate source of truth for static item data (BaseShape)
2. **GridShapeComponent**: Manages runtime shape state (rotation, normalization)
3. **GridShapeVisualComponent**: Generates visual/interaction blocks reactively
4. **InteractionArea**: Container with `MouseFilter.Ignore` for precise child interaction

## Architecture

### Component Dependencies

```
GridShapeVisualComponent
├── Depends on: GridShapeComponent (shape data + events)
├── Depends on: Control InteractionArea (block container)
└── Provides: Validation feedback API
```

### Reactive Listener Pattern

GridShapeVisualComponent is a **pure reactive listener**:
- Does NOT own data
- Subscribes to GridShapeComponent.OnShapeChangedAsObservable
- Rebuilds visual representation when logical state changes
- Follows Observer Pattern strictly

## Key Design Decisions

### 1. Parent Container Mouse Filtering

**Decision**: Set `InteractionArea.MouseFilter = Ignore`

**Rationale**:
- Parent container should not intercept mouse events
- Only child blocks (actual cells) should receive clicks
- Prevents AABB bounding box from capturing clicks

### 2. Individual Block Generation

**Decision**: Create separate `ColorRect` for each cell

**Rationale**:
- Pixel-perfect mouse interaction
- Each block can have independent mouse filtering
- Supports irregular shapes without empty space clicks

### 3. Reactive Rebuild

**Decision**: Subscribe to `OnShapeChangedAsObservable` via R3

**Rationale**:
- Automatic synchronization with shape changes
- No manual update calls needed
- Follows reactive programming patterns from DesignPatterns.md

### 4. Validation Feedback API

**Decision**: Expose `SetValidationFeedback(bool)` and `ResetFeedback()`

**Rationale**:
- Controller can provide visual feedback during drag
- Decoupled: Component doesn't know about drag logic
- Simple boolean interface (valid/invalid)

### 5. Logic-Visual Naming Pair

**Decision**: Rename from ItemShapeBlocksComponent to GridShapeVisualComponent

**Rationale**:
- Establishes clear relationship with GridShapeComponent
- Prefix alignment (GridShape-) makes pairing explicit
- Prevents "arbitrary naming hell" as project scales
- Reduces cognitive load for developers

## Export Properties

| Property | Type | Default | Purpose | Naming Rule |
|----------|------|---------|---------|-------------|
| GridShapeComponent | GridShapeComponent | null | Logic data source | ✅ Matches type |
| InteractionArea | Control | null | Block container | ✅ Specific name |
| CellSize | float | 64f | Block size in pixels | N/A |
| NormalColor | Color | White 20% | Default state | N/A |
| ValidColor | Color | Green 60% | Valid placement | N/A |
| InvalidColor | Color | Red 60% | Invalid placement | N/A |

## Public API

### Methods

```csharp
// Set validation feedback (called by Controller during drag)
void SetValidationFeedback(bool isValid)

// Reset to normal state (called when drag ends)
void ResetFeedback()
```

### Internal Methods

```csharp
// Rebuild all visual blocks based on current shape
private void RebuildVisualBlocks()
```

## Integration Example

### TSItem Scene Structure

```
TSItem (Control) - implements IItemDataProvider
├── GridShapeComponent (Node) - Logic/Data
├── GridShapeVisualComponent (Node) - Visual/Presentation
│   ├── GridShapeComponent -> GridShapeComponent
│   └── InteractionArea -> InteractionArea
└── InteractionArea (Control)
    └── [Generated ColorRect blocks]
```

### Controller Integration

```csharp
// In BackpackInteractionController
var visualComponent = item.GetNode<GridShapeVisualComponent>("GridShapeVisualComponent");

// During drag hover
bool isValidPlacement = LogicGrid.CanPlaceItem(...);
visualComponent.SetValidationFeedback(isValidPlacement);

// On drag end
visualComponent.ResetFeedback();
```

## Performance Considerations

### Block Count

- Typical tetris shapes: 3-5 blocks
- Maximum expected: ~10 blocks
- ColorRect is lightweight (minimal overhead)

### Rebuild Frequency

- Only on shape rotation (infrequent)
- Not called during drag movement
- Efficient: O(n) where n = cell count

### Memory Management

- Old blocks properly freed via `QueueFree()`
- R3 subscription disposed via `.AddTo(this)`
- No memory leaks

## Testing Checklist

- [ ] L-shape: Verify empty corner not clickable
- [ ] T-shape: Verify top empty cells not clickable
- [ ] Rotation: Verify blocks rebuild correctly
- [ ] Validation: Verify green/red feedback works
- [ ] Performance: Verify no frame drops with multiple items
- [ ] Naming: Verify all exports follow strict naming rule
- [ ] Pairing: Verify GridShapeComponent + GridShapeVisualComponent relationship is clear

## Compliance

✅ Follows `DesignPatterns.md` Component-Based architecture  
✅ Uses R3 reactive streams for event handling  
✅ Proper memory management with `.AddTo(this)`  
✅ Documented with 3-part structure (目的/示例/算法)  
✅ Single Responsibility Principle (only handles visual generation)  
✅ **Strict naming rule enforced (Type-to-Variable matching)**  
✅ **Logic-Visual naming pair established (GridShape prefix alignment)**  
✅ **Mounting architecture clearly defined (sibling to GridShapeComponent)**  
✅ **Pure reactive listener pattern (no data ownership)**

## Design Overview

### Purpose

Generate precise 1x1 visual/collision blocks for irregular tetris shapes, solving AABB bounding box limitations.

### Responsibilities

1. **Block Generation**: Create individual `ColorRect` nodes for each cell
2. **Shape Synchronization**: Rebuild blocks when shape changes (rotation)
3. **Validation Feedback**: Provide visual feedback for drag-and-drop states
4. **Mouse Filtering**: Configure precise mouse interaction per cell

## Critical Naming Rule

### Enforcement: Type-to-Variable Matching

**RULE**: Variables representing injected components or interfaces MUST strictly match their Type names (camelCase or PascalCase). Absolutely NO arbitrary aliases.

**Rationale**:
- Reduces cognitive load (no mental mapping)
- Improves code readability
- Ensures refactoring safety
- Maintains consistency across codebase

**Examples**:
```csharp
// ❌ BAD: Arbitrary aliases
[Export] public GridShapeComponent ShapeData { get; set; }
[Export] public Control VisualContainer { get; set; }

// ✅ GOOD: Type names
[Export] public GridShapeComponent GridShapeComponent { get; set; }
[Export] public Control InteractionArea { get; set; }
```

## Mounting Architecture

### Component Hierarchy

```
TSItem (Control) - implements IItemDataProvider
├── GridShapeComponent (Node)
│   └── Data source: IItemDataProvider.DataInitialized event
├── ItemShapeBlocksComponent (Node) [SIBLING to GridShapeComponent]
│   ├── References: GridShapeComponent
│   └── Targets: InteractionArea
└── InteractionArea (Control)
    └── [Generated ColorRect blocks]
```

### Mounting Strategy

**ItemShapeBlocksComponent mounts as a sibling to GridShapeComponent**:
- Both are child nodes of the ItemEntity (TSItem)
- ItemShapeBlocksComponent subscribes to GridShapeComponent's reactive streams
- Directly targets InteractionArea Control node for block placement

### Data Flow

```
IItemDataProvider (TSItemWrapper)
    ↓ event DataInitialized(ItemDataResource)
GridShapeComponent
    ↓ Receives Data via event subscription
    ↓ Initializes CurrentLocalCells from Data.BaseShape
    ↓ Emits OnShapeChangedAsObservable on rotation
ItemShapeBlocksComponent
    ↓ Subscribes to OnShapeChangedAsObservable
    ↓ Calls RebuildBlocks()
    ↓ Iterates CurrentLocalCells
InteractionArea (MouseFilter.Ignore)
    └── ColorRect[] (MouseFilter.Pass for each cell)
```

### Key Integration Points

1. **IItemDataProvider**: Ultimate source of truth for static item data (BaseShape)
2. **GridShapeComponent**: Manages runtime shape state (rotation, normalization)
3. **ItemShapeBlocksComponent**: Generates visual/interaction blocks reactively
4. **InteractionArea**: Container with `MouseFilter.Ignore` for precise child interaction

## Architecture

### Component Dependencies

```
ItemShapeBlocksComponent
├── Depends on: GridShapeComponent (shape data)
├── Depends on: Control InteractionArea (block container)
└── Provides: Validation feedback API
```

### Data Flow (Detailed)

```
GridShapeComponent.OnShapeChangedAsObservable
    ↓
ItemShapeBlocksComponent.RebuildBlocks()
    ↓
Clear existing blocks from InteractionArea
    ↓
Iterate GridShapeComponent.CurrentLocalCells
    ↓
For each cellPos:
    Create ColorRect
    Position = cellPos * CellSize
    MouseFilter = Pass
    Add to InteractionArea
    ↓
BackpackInteractionController.SetValidationFeedback()
    ↓
Update block colors (green/red)
```

## Key Design Decisions

### 1. Parent Container Mouse Filtering

**Decision**: Set `InteractionArea.MouseFilter = Ignore`

**Rationale**:
- Parent container should not intercept mouse events
- Only child blocks (actual cells) should receive clicks
- Prevents AABB bounding box from capturing clicks

### 2. Individual Block Generation

**Decision**: Create separate `ColorRect` for each cell

**Rationale**:
- Pixel-perfect mouse interaction
- Each block can have independent mouse filtering
- Supports irregular shapes without empty space clicks

### 3. Reactive Rebuild

**Decision**: Subscribe to `OnShapeChangedAsObservable` via R3

**Rationale**:
- Automatic synchronization with shape changes
- No manual update calls needed
- Follows reactive programming patterns from DesignPatterns.md

### 4. Validation Feedback API

**Decision**: Expose `SetValidationFeedback(bool)` and `ResetFeedback()`

**Rationale**:
- Controller can provide visual feedback during drag
- Decoupled: Component doesn't know about drag logic
- Simple boolean interface (valid/invalid)

### 5. Strict Naming Convention

**Decision**: Variable names MUST match Type names

**Rationale**:
- Eliminates cognitive overhead of arbitrary aliases
- Self-documenting code (`GridShapeComponent.CurrentLocalCells`)
- Refactoring safety (type changes propagate to variable names)

## Export Properties

| Property | Type | Default | Purpose | Naming Rule |
|----------|------|---------|---------|-------------|
| GridShapeComponent | GridShapeComponent | null | Shape data source | ✅ Matches type |
| InteractionArea | Control | null | Block container | ✅ Specific name |
| CellSize | float | 64f | Block size in pixels | N/A |
| NormalColor | Color | White 20% | Default state | N/A |
| ValidColor | Color | Green 60% | Valid placement | N/A |
| InvalidColor | Color | Red 60% | Invalid placement | N/A |

## Public API

### Methods

```csharp
// Set validation feedback (called by Controller during drag)
void SetValidationFeedback(bool isValid)

// Reset to normal state (called when drag ends)
void ResetFeedback()
```

### Internal Methods

```csharp
// Rebuild all blocks based on current shape
private void RebuildBlocks()
```

## Integration Example

### TSItem Scene Structure

```
TSItem (Control) - implements IItemDataProvider
├── GridShapeComponent (Node)
├── ItemShapeBlocksComponent (Node)
│   ├── GridShapeComponent -> GridShapeComponent
│   └── InteractionArea -> InteractionArea
└── InteractionArea (Control)
    └── [Generated ColorRect blocks]
```

### Controller Integration

```csharp
// In BackpackInteractionController
var blocksComponent = item.GetNode<ItemShapeBlocksComponent>("ItemShapeBlocksComponent");

// During drag hover
bool isValidPlacement = LogicGrid.CanPlaceItem(...);
blocksComponent.SetValidationFeedback(isValidPlacement);

// On drag end
blocksComponent.ResetFeedback();
```

## Performance Considerations

### Block Count

- Typical tetris shapes: 3-5 blocks
- Maximum expected: ~10 blocks
- ColorRect is lightweight (minimal overhead)

### Rebuild Frequency

- Only on shape rotation (infrequent)
- Not called during drag movement
- Efficient: O(n) where n = cell count

### Memory Management

- Old blocks properly freed via `QueueFree()`
- R3 subscription disposed via `.AddTo(this)`
- No memory leaks

## Testing Checklist

- [ ] L-shape: Verify empty corner not clickable
- [ ] T-shape: Verify top empty cells not clickable
- [ ] Rotation: Verify blocks rebuild correctly
- [ ] Validation: Verify green/red feedback works
- [ ] Performance: Verify no frame drops with multiple items
- [ ] Naming: Verify all exports follow strict naming rule

## Compliance

✅ Follows `DesignPatterns.md` Component-Based architecture  
✅ Uses R3 reactive streams for event handling  
✅ Proper memory management with `.AddTo(this)`  
✅ Documented with 3-part structure (目的/示例/算法)  
✅ Single Responsibility Principle (only handles block generation)  
✅ **Strict naming rule enforced (Type-to-Variable matching)**  
✅ **Mounting architecture clearly defined (sibling to GridShapeComponent)**
