# A1ObjectPool Architecture Rules (Godot Object Pool)

For nodes that are spawned and destroyed at a high frequency (e.g., bullets, floating damage text, death effects), the use of dynamic `Instantiate()` and `QueueFree()` is strictly forbidden to prevent runtime GC spikes and frame drops.
You MUST uniformly use the project's built-in `A1ObjectPool` addon architecture.

## Two Mandatory Requirements

### 1. Implementation & Reset Contract
All node components that need to enter the object pool (like a `Bullet` class) MUST implement the `IPoolable` interface:
- Provide a `PoolScene` property returning its associated `PackedScene`.
- Reset all physical states (like zeroing out velocity) in `OnRent()`.
- Terminate pending logic (like stopping timers or Tweens) in `OnReturn()`.

When spawning objects, retrieve them via the singleton: `PoolManager.Instance.Rent<T>(scene)`.

### 2. Destruction & Recycling — MUST Use Despawn()
For any object implementing `IPoolable`, it is **ABSOLUTELY FORBIDDEN** to call `QueueFree()` or `Free()`.
(The project includes a custom Roslyn Analyzer; any attempt to call `QueueFree()` on a pooled object will trigger an immediate compiler error).

**You MUST uniformly call the extension method:**
```csharp
this.Despawn(); 
```
`.Despawn()` will automatically determine if the object supports pooling and safely recycle it back into the hidden queue, or safely fallback to a standard `QueueFree()` for non-pooled objects.
