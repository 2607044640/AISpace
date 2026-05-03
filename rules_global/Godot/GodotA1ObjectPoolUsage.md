# A1ObjectPool Usage Guide

Use this pool for high-frequency objects (Bullets, Damage UI, Effects) to prevent GC spikes and frame drops. 
**Do not use dynamic `Instantiate()` or `QueueFree()` for these objects.**

## 1. Setup Your Object (The Contract)
Make your node script implement `IPoolable`.

```csharp
public partial class Bullet : Node2D, IPoolable
{
    // 1. Specify the scene this object comes from
    public PackedScene PoolScene => GD.Load<PackedScene>("res://Scenes/Bullet.tscn");

    // 2. Reset state when pulled from the pool (e.g., zero out velocity)
    public void OnRent() { 
        Velocity = Vector2.Zero; 
    }

    // 3. Stop logic when returned to the pool (e.g., stop timers)
    public void OnReturn() { 
        // Logic to halt active processes
    }
}
```

## 2. Prewarm the Pool (Initialization)
Before combat or heavy usage starts, pre-allocate the objects so they are ready in memory.

```csharp
// Prewarm 100 bullets into the hidden pool
PoolManager.Instance.Register(BulletScene, 100);
```

## 3. Spawn (Rent)
When you need the object (e.g., player fires a weapon), rent it from the pool instead of instantiating it.

```csharp
// The manager activates a bullet from the hidden shelf and hands it to you
var b = PoolManager.Instance.Rent<Bullet>(BulletScene);
AddChild(b);
b.GlobalPosition = spawnPosition;
```

## 4. Destroy (Despawn)
When the object finishes its job (e.g., hits a target or goes off-screen), **NEVER call `QueueFree()`**.

```csharp
b.Despawn(); 
```
*Note: The project enforces this. Calling `QueueFree()` on an `IPoolable` object will trigger a strict compiler error (A1POOL001).*
