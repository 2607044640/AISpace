---
inclusion: manual
---

# Godot Stateless State Machine Guide

<critical_decision_criteria>

## When to Use Stateless

Use Stateless ONLY when ALL conditions are met:
- Complex state flow (8+ states with intricate transitions)
- Event-driven architecture (input events, not continuous polling)
- Need state flow visualization or compile-time safety
- Multiple components react to state changes

## When NOT to Use Stateless

Do NOT use Stateless for:
- Simple threshold checks (velocity > sprintSpeed)
- Animation selection based on current values
- Display/presentation layers (AnimationConfig, UI)
- Any logic that polls values every frame

**Rule:** If your logic checks `if (value > threshold)` every frame, use simple if/else instead.

</critical_decision_criteria>

<architectural_placement>

## Correct Location: Control Layer

Place state machines in components that CONTROL behavior:
- MovementComponent (controls speed, physics)
- PlayerController (handles input, coordinates actions)
- AIController (decides enemy behavior)

## Incorrect Location: Display Layer

NEVER place state machines in components that DISPLAY state:
- AnimationConfig (selects animations based on velocity)
- UI components (show current state)
- Audio components (play sounds based on events)

**Principle:** State machines belong where decisions are made, not where results are shown.

</architectural_placement>

<core_concepts>

## Event-Driven vs Polling

### Event-Driven (Correct)

```csharp
// Input event triggers state change
_inputComponent.OnSprintPressed += () => _stateMachine.Fire(Trigger.StartSprint);

// State change directly controls behavior
_stateMachine.Configure(State.Sprinting)
    .OnEntry(() => {
        Speed = 10.0f;              // Set speed
        PlayAnimation("Sprint");     // Command animation
    });
```

**Flow:** Input Event → State Change → Behavior Changes

### Polling (Incorrect)

```csharp
// ❌ WRONG: Checking value every frame
void Update() {
    if (speed > sprintThreshold) {
        _stateMachine.Fire(Trigger.StartSprint);  // Backwards logic
    }
}
```

**Problem:** This is just if/else with extra steps. No benefit over simple conditionals.

</core_concepts>

<integration_with_component_architecture>

## Component-Based Implementation

Stateless integrates with the project's component architecture:

```csharp
[GlobalClass]
[Component(typeof(CharacterBody3D))]
public partial class GroundMovementComponent : Node
{
    private enum State { Idle, Walking, Sprinting, Jumping }
    private enum Trigger { StartMove, StartSprint, StopSprint, Jump, Land, Stop }
    
    private StateMachine<State, Trigger> _machine;
    
    [ComponentDependency(typeof(BaseInputComponent))]
    private BaseInputComponent _inputComponent;
    
    [Export] public float WalkSpeed { get; set; } = 5.0f;
    [Export] public float SprintSpeed { get; set; } = 10.0f;
    
    private float _currentSpeed = 0f;
    
    public override void _Ready()
    {
        InitializeComponent();
    }
    
    public override void OnEntityReady()
    {
        InitializeStateMachine();
        
        // Subscribe to input events
        _inputComponent.OnSprintPressed += HandleSprintPressed;
        _inputComponent.OnSprintReleased += HandleSprintReleased;
    }
    
    private void InitializeStateMachine()
    {
        _machine = new StateMachine<State, Trigger>(State.Idle);
        
        _machine.Configure(State.Idle)
            .OnEntry(() => {
                _currentSpeed = 0f;
                EmitAnimationCommand("Idle");
            })
            .Permit(Trigger.StartMove, State.Walking)
            .Permit(Trigger.Jump, State.Jumping);
        
        _machine.Configure(State.Walking)
            .OnEntry(() => {
                _currentSpeed = WalkSpeed;
                EmitAnimationCommand("Walk");
            })
            .Permit(Trigger.StartSprint, State.Sprinting)
            .Permit(Trigger.Stop, State.Idle);
        
        _machine.Configure(State.Sprinting)
            .OnEntry(() => {
                _currentSpeed = SprintSpeed;
                EmitAnimationCommand("Sprint");
            })
            .Permit(Trigger.StopSprint, State.Walking)
            .Permit(Trigger.Stop, State.Idle);
    }
    
    private void HandleSprintPressed()
    {
        if (_machine.CanFire(Trigger.StartSprint))
            _machine.Fire(Trigger.StartSprint);
    }
    
    private void HandleSprintReleased()
    {
        if (_machine.CanFire(Trigger.StopSprint))
            _machine.Fire(Trigger.StopSprint);
    }
    
    public override void _PhysicsProcess(double delta)
    {
        // No if/else chains - just apply state-controlled speed
        Vector3 velocity = parent.Velocity;
        Vector3 direction = CalculateDirection();
        
        velocity.X = direction.X * _currentSpeed;
        velocity.Z = direction.Z * _currentSpeed;
        
        parent.Velocity = velocity;
        parent.MoveAndSlide();
    }
    
    public override void _ExitTree()
    {
        _inputComponent.OnSprintPressed -= HandleSprintPressed;
        _inputComponent.OnSprintReleased -= HandleSprintReleased;
    }
    
    // Event for animation component to subscribe
    public event Action<string> OnAnimationRequested;
    
    private void EmitAnimationCommand(string animName)
    {
        OnAnimationRequested?.Invoke(animName);
    }
}
```

**Key Points:**
- State machine in MovementComponent (control layer)
- Triggered by input events, not velocity checks
- Directly controls speed via `_currentSpeed`
- Emits events for AnimationComponent to subscribe
- Follows "Call Down, Signal Up" pattern

</integration_with_component_architecture>

<api_reference>

## StateMachine Configuration

```csharp
var machine = new StateMachine<TState, TTrigger>(initialState);

machine.Configure(State.Idle)
    .OnEntry(() => { /* Execute on enter */ })
    .OnExit(() => { /* Execute on exit */ })
    .Permit(Trigger.Start, State.Running)           // Allow transition
    .PermitIf(Trigger.Jump, State.Jumping, () => isGrounded)  // Conditional
    .Ignore(Trigger.Attack)                         // Ignore trigger
    .PermitReentry(Trigger.Reset);                  // Allow self-transition
```

## Firing Triggers

```csharp
// Check if trigger is valid
if (machine.CanFire(Trigger.Start))
    machine.Fire(Trigger.Start);

// Fire with parameter
machine.Fire(triggerWithParam, paramValue);

// Get current state
var currentState = machine.State;
```

## Hierarchical States

```csharp
machine.Configure(State.Alive)
    .SubstateOf(State.Playing)
    .Permit(Trigger.Die, State.Dead);

machine.Configure(State.Dead)
    .SubstateOf(State.Playing)
    .OnEntry(() => PlayDeathAnimation());
```

</api_reference>

<anti_patterns>

## Anti-Pattern 1: Polling in Display Layer

❌ **Wrong:**
```csharp
// In AnimationConfig
private (string, float) GetGroundAnimation(Vector3 velocity)
{
    float speed = velocity.Length();
    
    // Polling velocity every frame
    if (speed > SprintThreshold)
        _machine.Fire(Trigger.StartSprint);  // Backwards!
    
    return _machine.State switch {
        State.Sprinting => ("Sprint", 1.0f),
        State.Running => ("Run", 1.0f),
        _ => ("Idle", 1.0f)
    };
}
```

**Problems:**
- Checks velocity every frame (polling)
- State machine in wrong layer (display, not control)
- More complex than simple if/else
- No benefit over original code

✅ **Correct:**
```csharp
// In AnimationConfig - Simple if/else
private (string, float) GetGroundAnimation(Vector3 velocity)
{
    float speed = velocity.Length();
    
    if (speed > SprintThreshold) return ("Sprint", 1.0f);
    if (speed > MoveThreshold) return ("Run", 1.0f);
    return ("Idle", 1.0f);
}
```

**Benefits:**
- Clear and concise
- No unnecessary abstraction
- Appropriate for simple threshold checks

## Anti-Pattern 2: State Machine Without Events

❌ **Wrong:**
```csharp
public override void _PhysicsProcess(double delta)
{
    // Checking conditions every frame
    if (Input.IsActionPressed("sprint") && _machine.CanFire(Trigger.Sprint))
        _machine.Fire(Trigger.Sprint);
    
    if (!Input.IsActionPressed("sprint") && _machine.CanFire(Trigger.Walk))
        _machine.Fire(Trigger.Walk);
}
```

**Problem:** Polling input every frame defeats the purpose of event-driven state machine.

✅ **Correct:**
```csharp
public override void OnEntityReady()
{
    // Subscribe to input events
    _inputComponent.OnSprintPressed += () => {
        if (_machine.CanFire(Trigger.Sprint))
            _machine.Fire(Trigger.Sprint);
    };
    
    _inputComponent.OnSprintReleased += () => {
        if (_machine.CanFire(Trigger.Walk))
            _machine.Fire(Trigger.Walk);
    };
}
```

**Benefits:**
- Event-driven (fires only when input changes)
- No per-frame overhead
- Clear separation of concerns

## Anti-Pattern 3: Over-Engineering Simple Logic

❌ **Wrong:**
```csharp
// 80 lines of state machine for 3 states
private enum DoorState { Closed, Opening, Open, Closing }
private enum DoorTrigger { Open, Close, FinishAnimation }

private void InitializeDoorStateMachine() {
    _machine = new StateMachine<DoorState, DoorTrigger>(DoorState.Closed);
    _machine.Configure(DoorState.Closed)
        .Permit(DoorTrigger.Open, DoorState.Opening);
    // ... 60 more lines
}
```

✅ **Correct:**
```csharp
// 10 lines of simple logic
private bool _isOpen = false;

private void ToggleDoor() {
    _isOpen = !_isOpen;
    PlayAnimation(_isOpen ? "Open" : "Close");
}
```

**Rule:** Use the simplest solution that works. State machines are not always better.

</anti_patterns>

<decision_flowchart>

## Should I Use Stateless?

```
Start
  ↓
Is this a control layer component? (MovementComponent, Controller)
  ↓ No → Use simple if/else
  ↓ Yes
  ↓
Are there 8+ states with complex transitions?
  ↓ No → Use simple if/else
  ↓ Yes
  ↓
Can state changes be triggered by discrete events? (not polling)
  ↓ No → Use simple if/else
  ↓ Yes
  ↓
Do multiple components need to react to state changes?
  ↓ No → Consider if/else (might be simpler)
  ↓ Yes
  ↓
Use Stateless ✓
```

**Default Answer:** When in doubt, use simple if/else. You can always refactor later.

</decision_flowchart>

<performance_considerations>

## Overhead Comparison

| Approach | Per-Frame Cost | Memory | Maintainability |
|----------|----------------|--------|-----------------|
| Simple if/else | 4 comparisons | 0 bytes | High (for simple logic) |
| Stateless (correct) | 0 (event-driven) | ~200 bytes | High (for complex logic) |
| Stateless (polling) | 8+ comparisons + state checks | ~200 bytes | Low (over-engineered) |

**Guideline:** Stateless should REDUCE per-frame overhead by eliminating polling, not increase it.

</performance_considerations>

<visualization>

## State Diagram Generation

Stateless can generate DOT graphs for visualization:

```csharp
string dotGraph = UmlDotGraph.Format(_machine.GetInfo());
System.IO.File.WriteAllText("state_diagram.dot", dotGraph);
```

Convert to image: http://www.webgraphviz.com

**Use Case:** Document complex state flows for team understanding.

</visualization>

<nuget_package>

## Installation

```bash
dotnet add package Stateless
```

**Version:** 5.x+ (supports .NET Standard 2.0, compatible with Godot 4.x)

**Repository:** https://github.com/dotnet-state-machine/stateless

</nuget_package>

<summary>

## Quick Reference

**Use Stateless when:**
- Complex state flow (8+ states)
- Event-driven transitions
- In control layer components
- Need visualization/compile-time safety

**Use simple if/else when:**
- Simple threshold checks
- Display/presentation layers
- Polling-based logic
- Fewer than 5 states

**Golden Rule:** Stateless should make code SIMPLER, not more complex. If it adds 200 lines for no benefit, you're using it wrong.

</summary>
