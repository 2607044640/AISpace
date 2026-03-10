# Godot C# AI Implementation Guide

## Overview

This guide covers implementing AI systems in Godot using pure C#, focusing on Behavior Trees and State Machines without external plugins.

**Philosophy:** Maximum flexibility and control through code-first approach.

---

## Core Architecture

### 1. Component Structure

```
Scripts/AI/
├── Core/
│   ├── BTNode.cs           # Base behavior tree node
│   ├── BehaviorTree.cs     # Tree executor
│   ├── Blackboard.cs       # Shared data storage
│   └── AIController.cs     # Main AI controller
├── Composites/
│   ├── BTSequence.cs       # Execute children in order (AND logic)
│   ├── BTSelector.cs       # Try children until success (OR logic)
│   ├── BTParallel.cs       # Execute all children simultaneously
│   └── BTRandomSelector.cs # Random child selection
├── Decorators/
│   ├── BTInverter.cs       # Invert child result
│   ├── BTRepeater.cs       # Repeat child N times
│   ├── BTCooldown.cs       # Add cooldown to child
│   └── BTUntilFail.cs      # Repeat until failure
├── Conditions/
│   ├── BTCheckDistance.cs  # Check distance to target
│   ├── BTCheckHealth.cs    # Check health threshold
│   └── BTCheckLineOfSight.cs # Raycast visibility check
└── Actions/
    ├── BTMoveToTarget.cs   # Navigate to position
    ├── BTAttack.cs         # Perform attack
    ├── BTPatrol.cs         # Patrol waypoints
    └── BTPlayAnimation.cs  # Trigger animation
```

---

## UE Comparison

| Godot C# | Unreal Engine | Purpose |
|----------|---------------|---------|
| `AIController` | `AAIController` | Main AI brain |
| `Blackboard` | `UBlackboardComponent` | Shared data |
| `BehaviorTree` | `UBehaviorTree` | Tree structure |
| `BTNode` | `UBTNode` | Base task class |
| `BTSequence` | `UBTComposite_Sequence` | Sequential execution |
| `BTSelector` | `UBTComposite_Selector` | Priority selection |

---

## Implementation

### 1. BTNode Base Class

```csharp
using Godot;

namespace Game.AI
{
    public abstract partial class BTNode : Node
    {
        public enum Status
        {
            Success,  // Task completed successfully
            Failure,  // Task failed
            Running   // Task still executing
        }

        protected CharacterBody3D Agent;
        protected Blackboard Blackboard;

        public virtual void Initialize(CharacterBody3D agent, Blackboard blackboard)
        {
            Agent = agent;
            Blackboard = blackboard;
        }

        // Called when node starts executing
        public virtual void OnEnter() { }

        // Called every frame while running
        public abstract Status Execute(double delta);

        // Called when node stops executing
        public virtual void OnExit() { }
    }
}
```

### 2. Blackboard (Shared Data)

```csharp
using Godot;
using System.Collections.Generic;

namespace Game.AI
{
    public partial class Blackboard : Node
    {
        private Dictionary<string, Variant> _data = new();

        public void SetValue(string key, Variant value)
        {
            _data[key] = value;
        }

        public T GetValue<T>(string key, T defaultValue = default)
        {
            if (_data.TryGetValue(key, out var value))
                return value.As<T>();
            return defaultValue;
        }

        public bool HasValue(string key) => _data.ContainsKey(key);

        public void Clear() => _data.Clear();
    }
}
```

### 3. BehaviorTree Executor

```csharp
using Godot;

namespace Game.AI
{
    public partial class BehaviorTree : Node
    {
        [Export] public CharacterBody3D Agent;
        [Export] public bool AutoStart = true;

        private BTNode _rootNode;
        private Blackboard _blackboard;
        private bool _isRunning;

        public override void _Ready()
        {
            _blackboard = new Blackboard();
            _rootNode = BuildTree();
            InitializeTree(_rootNode);

            if (AutoStart)
                Start();
        }

        public override void _Process(double delta)
        {
            if (!_isRunning) return;

            var status = _rootNode.Execute(delta);

            // Restart tree if completed
            if (status != BTNode.Status.Running)
            {
                _rootNode.OnExit();
                _rootNode.OnEnter();
            }
        }

        private void InitializeTree(BTNode node)
        {
            node.Initialize(Agent, _blackboard);
            foreach (var child in node.GetChildren())
            {
                if (child is BTNode btChild)
                    InitializeTree(btChild);
            }
        }

        public void Start()
        {
            _isRunning = true;
            _rootNode.OnEnter();
        }

        public void Stop()
        {
            _isRunning = false;
            _rootNode.OnExit();
        }

        // Override this to build your tree structure
        protected virtual BTNode BuildTree()
        {
            // Example: Simple patrol and attack behavior
            var root = new BTSelector();
            
            var attackSequence = new BTSequence();
            attackSequence.AddChild(new BTCheckDistance { MaxDistance = 5.0f });
            attackSequence.AddChild(new BTAttack());
            
            root.AddChild(attackSequence);
            root.AddChild(new BTPatrol());
            
            return root;
        }

        public Blackboard GetBlackboard() => _blackboard;
    }
}
```

### 4. Composite Nodes

#### BTSequence (AND logic)

```csharp
namespace Game.AI
{
    public partial class BTSequence : BTNode
    {
        private int _currentChildIndex = 0;

        public override void OnEnter()
        {
            _currentChildIndex = 0;
        }

        public override Status Execute(double delta)
        {
            while (_currentChildIndex < GetChildCount())
            {
                var child = GetChild<BTNode>(_currentChildIndex);
                var status = child.Execute(delta);

                if (status == Status.Failure)
                    return Status.Failure;

                if (status == Status.Running)
                    return Status.Running;

                // Success, move to next child
                _currentChildIndex++;
            }

            // All children succeeded
            return Status.Success;
        }
    }
}
```

#### BTSelector (OR logic)

```csharp
namespace Game.AI
{
    public partial class BTSelector : BTNode
    {
        private int _currentChildIndex = 0;

        public override void OnEnter()
        {
            _currentChildIndex = 0;
        }

        public override Status Execute(double delta)
        {
            while (_currentChildIndex < GetChildCount())
            {
                var child = GetChild<BTNode>(_currentChildIndex);
                var status = child.Execute(delta);

                if (status == Status.Success)
                    return Status.Success;

                if (status == Status.Running)
                    return Status.Running;

                // Failure, try next child
                _currentChildIndex++;
            }

            // All children failed
            return Status.Failure;
        }
    }
}
```

### 5. Example Action Nodes

#### BTMoveToTarget

```csharp
using Godot;

namespace Game.AI
{
    public partial class BTMoveToTarget : BTNode
    {
        [Export] public float Speed = 5.0f;
        [Export] public float StoppingDistance = 0.5f;
        [Export] public string TargetKey = "target_position";

        public override Status Execute(double delta)
        {
            if (!Blackboard.HasValue(TargetKey))
                return Status.Failure;

            var target = Blackboard.GetValue<Vector3>(TargetKey);
            var distance = Agent.GlobalPosition.DistanceTo(target);

            if (distance <= StoppingDistance)
                return Status.Success;

            var direction = (target - Agent.GlobalPosition).Normalized();
            Agent.Velocity = direction * Speed;
            Agent.MoveAndSlide();

            return Status.Running;
        }
    }
}
```

#### BTCheckDistance

```csharp
using Godot;

namespace Game.AI
{
    public partial class BTCheckDistance : BTNode
    {
        [Export] public float MaxDistance = 10.0f;
        [Export] public string TargetKey = "player";

        public override Status Execute(double delta)
        {
            if (!Blackboard.HasValue(TargetKey))
                return Status.Failure;

            var target = Blackboard.GetValue<Node3D>(TargetKey);
            if (target == null)
                return Status.Failure;

            var distance = Agent.GlobalPosition.DistanceTo(target.GlobalPosition);
            return distance <= MaxDistance ? Status.Success : Status.Failure;
        }
    }
}
```

---

## Usage Example

### Enemy AI Controller

```csharp
using Godot;

namespace Game.AI
{
    public partial class EnemyAI : BehaviorTree
    {
        [Export] public Node3D Player;
        [Export] public float DetectionRange = 15.0f;
        [Export] public float AttackRange = 3.0f;

        protected override BTNode BuildTree()
        {
            // Root selector: try behaviors in priority order
            var root = new BTSelector();

            // High priority: Attack if player is close
            var attackBehavior = new BTSequence();
            attackBehavior.AddChild(new BTCheckDistance 
            { 
                MaxDistance = AttackRange,
                TargetKey = "player"
            });
            attackBehavior.AddChild(new BTAttack());

            // Medium priority: Chase if player detected
            var chaseBehavior = new BTSequence();
            chaseBehavior.AddChild(new BTCheckDistance 
            { 
                MaxDistance = DetectionRange,
                TargetKey = "player"
            });
            chaseBehavior.AddChild(new BTMoveToTarget 
            { 
                TargetKey = "player_position",
                Speed = 6.0f
            });

            // Low priority: Patrol when idle
            var patrolBehavior = new BTPatrol();

            root.AddChild(attackBehavior);
            root.AddChild(chaseBehavior);
            root.AddChild(patrolBehavior);

            return root;
        }

        public override void _Process(double delta)
        {
            // Update blackboard with player info
            if (Player != null)
            {
                GetBlackboard().SetValue("player", Player);
                GetBlackboard().SetValue("player_position", Player.GlobalPosition);
            }

            base._Process(delta);
        }
    }
}
```

---

## Advanced Patterns

### 1. Utility AI Integration

```csharp
public partial class BTUtilitySelector : BTNode
{
    public override Status Execute(double delta)
    {
        BTNode bestChild = null;
        float bestScore = float.MinValue;

        foreach (var child in GetChildren())
        {
            if (child is IUtilityNode utilityNode)
            {
                float score = utilityNode.CalculateUtility(Blackboard);
                if (score > bestScore)
                {
                    bestScore = score;
                    bestChild = child as BTNode;
                }
            }
        }

        return bestChild?.Execute(delta) ?? Status.Failure;
    }
}
```

### 2. State Machine Hybrid

```csharp
public partial class BTStateMachine : BTNode
{
    private BTNode _currentState;

    public void ChangeState(BTNode newState)
    {
        _currentState?.OnExit();
        _currentState = newState;
        _currentState?.OnEnter();
    }

    public override Status Execute(double delta)
    {
        return _currentState?.Execute(delta) ?? Status.Failure;
    }
}
```

---

## Best Practices

1. **Keep nodes small and focused** - Each node should do one thing well
2. **Use Blackboard for communication** - Avoid direct references between nodes
3. **Leverage C# features** - Use LINQ, async/await, generics where appropriate
4. **Profile performance** - Use `GD.Print()` to debug tree execution
5. **Reuse subtrees** - Create common behavior patterns as reusable trees

---

## Debugging Tips

```csharp
public abstract partial class BTNode : Node
{
    [Export] public bool DebugMode = false;

    public override Status Execute(double delta)
    {
        if (DebugMode)
            GD.Print($"[{Name}] Executing...");

        var status = ExecuteInternal(delta);

        if (DebugMode)
            GD.Print($"[{Name}] Status: {status}");

        return status;
    }

    protected abstract Status ExecuteInternal(double delta);
}
```

---

## Resources

- [Behavior Trees Explained](https://www.gamedeveloper.com/programming/behavior-trees-for-ai-how-they-work)
- [godot-behavior-tree-csharp](https://github.com/MadFlyFish/godot-behavior-tree-csharp)
- UE Behavior Tree documentation (for concept reference)

---

**Next Steps:**
1. Implement core classes (BTNode, BehaviorTree, Blackboard)
2. Create basic composite nodes (Sequence, Selector)
3. Build action nodes for your specific game
4. Test with simple AI behaviors
5. Iterate and expand
