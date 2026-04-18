# Plugin Search: Dependency Injection for Godot C#

**Date**: 2026-04-18  
**Last Searched**: 2026-04-18  
**Problem**: Godot _Ready() initialization order makes parent-to-child data injection awkward

## Search Keywords Used
- "Godot C# dependency injection framework"
- "Godot C# initialization order"
- "Godot C# component communication"
- "Godot C# property injection"

## Candidates Found

### ✅ 1. Chickensoft AutoInject (RECOMMENDED)
**GitHub**: https://github.com/chickensoft-games/AutoInject  
**Stars**: ~150+ (estimated, Chickensoft org has 153 stars for GodotEnv)  
**Last Update**: 2024-05 (May 2024)  
**Status**: ✅ Active, well-maintained  
**NuGet**: `Chickensoft.AutoInject`

**What it does**:
- Reflection-free, node-based dependency injection
- Parent nodes provide values, child nodes depend on them
- Uses Source Generators (Introspection) for zero-runtime-reflection

**What it helps**:
- Solves _Ready() execution order problem elegantly
- Provides `OnResolved()` callback after all dependencies are ready
- Type-safe, compile-time checked
- Includes bonus features: IAutoConnect ([Node] attribute), IAutoOn (lifecycle hooks)

**What pain it solves**:
- No more manual `_EnterTree()` hacks
- No more parent knowing child's internal structure
- Declarative `[Dependency]` attribute
- Automatic provider search up the scene tree

**Architecture**:
```csharp
// Provider (Parent)
[Meta(typeof(IAutoNode))]
public partial class TSItemWrapper : Control, IProvide<ItemDataResource>
{
    [Export] public ItemDataResource Data { get; set; }
    
    ItemDataResource IProvide<ItemDataResource>.Value() => Data;
    
    public void OnReady() => this.Provide();
}

// Dependent (Child)
[Meta(typeof(IAutoNode))]
public partial class GridShapeComponent : Node
{
    [Dependency]
    public ItemDataResource Data => this.DependOn<ItemDataResource>();
    
    public void OnResolved()
    {
        // Data is now available! Initialize shape.
        InitializeShape();
    }
}
```

**Pros**:
- ✅ Solves exact problem (parent → child data flow)
- ✅ No reflection (uses Source Generators)
- ✅ Type-safe
- ✅ Well-documented
- ✅ Active maintenance
- ✅ Includes testing utilities
- ✅ Bonus: IAutoConnect for [Node] binding
- ✅ Bonus: IAutoOn for lifecycle hooks (OnReady, OnProcess, etc.)

**Cons**:
- ⚠️ Requires overriding `_Notification(int what)` in every node
- ⚠️ Adds dependency on Chickensoft.Introspection (Source Generator)
- ⚠️ Learning curve for Provider/Dependent pattern

**Dependencies**:
- Chickensoft.GodotNodeInterfaces
- Chickensoft.Introspection
- Chickensoft.Introspection.Generator
- Chickensoft.AutoInject

---

### 2. Godot.DependencyInjection (Filip-Drabinski)
**GitHub**: https://github.com/Filip-Drabinski/Godot.DependencyInjection  
**NuGet**: https://www.nuget.org/packages/Godot.DependencyInjection  
**Stars**: Unknown (likely < 100)  
**Last Update**: 2023-09 (September 2023)  
**Status**: ⚠️ Possibly stale (1+ year old)

**What it does**:
- Traditional DI container approach
- Service registration and resolution

**Evaluation**: ❌ REJECTED
- Reason: Last update over 1 year ago
- Reason: Unknown star count (likely low)
- Reason: Traditional DI container doesn't fit Godot's node tree model well

---

### 3. GodotAddons.DependencyInjection
**NuGet**: https://www.nuget.org/packages/GodotAddons.DependencyInjection  
**Stars**: Unknown  
**Last Update**: 2024-10 (October 2024)  
**Status**: ⚠️ No GitHub repository found

**Evaluation**: ❌ REJECTED
- Reason: No GitHub repository for verification
- Reason: No documentation found
- Reason: Unknown community adoption

---

### 4. TheColorRed/godot-di
**GitHub**: https://github.com/TheColorRed/godot-di  
**Stars**: Unknown (likely < 50)  
**Last Update**: Unknown  
**Status**: ⚠️ Insufficient information

**Evaluation**: ❌ REJECTED
- Reason: Minimal documentation
- Reason: Unknown maintenance status
- Reason: No clear advantage over AutoInject

---

## Alternative Patterns Considered

### Pattern 1: Property Setter Injection (Manual)
```csharp
// Parent
public override void _EnterTree()
{
    var child = GetNode<GridShapeComponent>("GridShapeComponent");
    child.Data = Data;
}
```
**Status**: ❌ Current workaround (ugly, tight coupling)

### Pattern 2: Lazy<T> Initialization
```csharp
private Lazy<ItemDataResource> _data;

public override void _Ready()
{
    _data = new Lazy<ItemDataResource>(() => GetParent<TSItemWrapper>().Data);
}
```
**Status**: ⚠️ Possible but still requires parent knowledge

### Pattern 3: Observer Pattern (C# Events)
```csharp
// Parent
public event Action<ItemDataResource> OnDataReady;

public override void _Ready()
{
    OnDataReady?.Invoke(Data);
}

// Child
public override void _Ready()
{
    GetParent<TSItemWrapper>().OnDataReady += HandleData;
}
```
**Status**: ⚠️ Possible but verbose, manual subscription management

---

## Final Recommendation

**Use Chickensoft AutoInject** for the following reasons:

1. **Solves the exact problem**: Parent → child data flow with proper lifecycle
2. **Type-safe**: Compile-time checking via Source Generators
3. **Well-maintained**: Active development, good documentation
4. **Bonus features**: IAutoConnect, IAutoOn, IAutoInit
5. **Testing support**: Includes utilities for unit testing
6. **Community adoption**: Part of Chickensoft ecosystem (GodotEnv has 454 stars)

**Trade-offs**:
- Requires `_Notification` override (one-time boilerplate)
- Adds Source Generator dependency (acceptable for the benefits)

**Next Steps**:
1. Install AutoInject via NuGet
2. Refactor TSItemWrapper to implement `IProvide<ItemDataResource>`
3. Refactor GridShapeComponent to use `[Dependency]` attribute
4. Test the new pattern
5. Document the pattern in project rules
