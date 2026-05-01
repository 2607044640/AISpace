# Physics Transform Feedback Loop (RigidBody2D as child of Control)

## The Problem
When a `RigidBody2D` (or any physics body) is placed as a child of a `Control` node (or Node2D), and its script attempts to sync the parent's position to the physics body's position in `_PhysicsProcess`, it creates a **Transform Feedback Loop**.

### Symptoms
- Items bounce uncontrollably when colliding.
- Items slide infinitely without stopping.
- Items instantly teleport (e.g., to the bottom right) when `Freeze` is toggled.
- Physics behaves completely differently than when the RigidBody2D is the root node of a scene.

## The Root Cause
Godot's transform system propagates positions from parent to child. 
1. The physics engine moves the child `RigidBody2D`.
2. The `_PhysicsProcess` script reads the `RigidBody2D.GlobalPosition` and applies it to the parent `Control.GlobalPosition`.
3. Because `RigidBody2D` is a child, moving the parent *also moves the child* in the same frame.
4. The physics engine detects the child has moved unexpectedly and tries to correct it in the next frame, leading to amplified errors, teleporting, and chaotic bouncing.

## The Solution
Set `TopLevel = true` on the `RigidBody2D` component before enabling physics.

```csharp
public override void _Ready()
{
    // Detaches the RigidBody2D's transform from its parent, 
    // making its GlobalPosition independent of the parent Control.
    TopLevel = true; 
}
```

This breaks the feedback loop. The physics engine can now move the `RigidBody2D` independently, and the `_PhysicsProcess` can safely copy that position to the parent `Control` without causing a recursive transform update.
