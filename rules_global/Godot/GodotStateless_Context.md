---
trigger: manual
---

<layer_1_quick_start>
  <quick_reference>
    - **Installation Target**: `dotnet add package Stateless`
    - **Compatibility**: Version 5.x+ (.NET Standard 2.0, Godot 4.x compatible)
    - **Visualization Command**: `UmlDotGraph.Format(_machine.GetInfo())`
  </quick_reference>

  <decision_tree>
    - **IF** component is Control Layer (e.g., MovementComponent) **AND** has 8+ states **AND** relies on event-driven inputs -> **USE Stateless** (Why: Handles complex architectural flow and multiple component reactions securely).
    - **IF** logic uses simple threshold checks (`value > threshold`) -> **NEVER use Stateless** (Why: Over-engineers logic and adds per-frame overhead for zero benefit).
    - **IF** component is Display/Presentation Layer (e.g., AnimationConfig, UI) -> **NEVER use Stateless** (Why: View layer must react to state, not manage it).
  </decision_tree>

  <end_to_end_example>
    <code><![CDATA[
// Initialize event-driven state machine
private StateMachine<State, Trigger> _machine;

public override void OnEntityReady()
{
    _machine = new StateMachine<State, Trigger>(State.Idle);
    
    _machine.Configure(State.Idle)
        .Permit(Trigger.StartMove, State.Walking);

    // Bind strictly to events; NEVER poll in _PhysicsProcess
    _inputComponent.OnMovePressed += () => {
        if (_machine.CanFire(Trigger.StartMove)) 
            _machine.Fire(Trigger.StartMove);
    };
}
    ]]></code>
  </end_to_end_example>

  <top_anti_patterns>
    <rule>
      <description>NEVER poll values every frame to trigger state changes.</description>
      <rationale>Introduces backwards logic, destroys the benefits of event-driven architecture, and adds unnecessary per-frame overhead.</rationale>
      <example>
        <![CDATA[
// INCORRECT (Polling)
void Update() {
    if (speed > sprintThreshold) _machine.Fire(Trigger.StartSprint); 
}

// CORRECT (Event-Driven)
_inputComponent.OnSprintPressed += () => _machine.Fire(Trigger.StartSprint);
        ]]>
      </example>
    </rule>
    <rule>
      <description>NEVER implement state machines in Display Layer components (e.g., AnimationConfig).</description>
      <rationale>Violates separation of concerns. State machines belong where logic decisions are made, not where the result is drawn.</rationale>
      <example>
        <![CDATA[
// INCORRECT (In AnimationConfig)
if (speed > SprintThreshold) _machine.Fire(Trigger.StartSprint);

// CORRECT (In AnimationConfig - Simple If/Else)
if (speed > SprintThreshold) return ("Sprint", 1.0f);
        ]]>
      </example>
    </rule>
    <rule>
      <description>NEVER utilize Stateless for simple binary states or low-complexity behavior.</description>
      <rationale>Writing 80 lines of boilerplate for 3 states wastes ~200 bytes of memory and severely damages readability compared to a 10-line boolean method.</rationale>
      <example>
        <![CDATA[
// INCORRECT
_machine = new StateMachine<DoorState, DoorTrigger>(DoorState.Closed);
_machine.Configure(DoorState.Closed).Permit(DoorTrigger.Open, DoorState.Opening); // ...60 more lines

// CORRECT
_isOpen = !_isOpen;
PlayAnimation(_isOpen ? "Open" : "Close");
        ]]>
      </example>
    </rule>
  </top_anti_patterns>

  <decision_flowchart>
    <![CDATA[
    Should I Use Stateless?
    
    START
      ↓
    [Is this a Control Layer component?]
    (MovementComponent, AIController, PlayerController)
      ↓ NO  → Use simple if/else
      ↓ YES
      ↓
    [Are there 8+ states with complex transitions?]
      ↓ NO  → Use simple if/else
      ↓ YES
      ↓
    [Can state changes be triggered by discrete events?]
    (Input events, signals - NOT polling every frame)
      ↓ NO  → Use simple if/else
      ↓ YES
      ↓
    [Do multiple components need to react to state changes?]
      ↓ NO  → Consider if/else (might be simpler)
      ↓ YES
      ↓
    ✓ USE STATELESS
    
    Default Rule: When in doubt, use simple if/else.
                  You can always refactor later.
    ]]>
  </decision_flowchart>
</layer_1_quick_start>

<layer_2_detailed_guide>
  <api_reference>
    - `StateMachine<TState, TTrigger>(TState initialState)`: Instantiates a new state machine.
    - `Configure(TState state)`: Begins configuration for the specified state.
    - `OnEntry(Action action)`: Executes lambda/method upon entering the state.
    - `OnExit(Action action)`: Executes lambda/method upon exiting the state.
    - `Permit(TTrigger trigger, TState destinationState)`: Defines an unconditional transition.
    - `PermitIf(TTrigger trigger, TState destinationState, Func<bool> guard)`: Defines a conditional transition.
    - `Ignore(TTrigger trigger)`: Silently ignores the trigger in the configured state.
    - `PermitReentry(TTrigger trigger)`: Allows self-transition, triggering both OnExit and OnEntry.
    - `CanFire(TTrigger trigger)`: Returns a boolean confirming if the trigger is currently valid.
    - `Fire(TTrigger trigger)`: Executes the transition.
    - `Fire(TTrigger trigger, TParameter param)`: Executes transition with passed parameters.
    - `SubstateOf(TState parentState)`: Maps hierarchical state relationships.
    - `State`: Property returning the machine's current state.
  </api_reference>

  <implementation_guide>
    1. **Define Enums**: Create strict `State` and `Trigger` enumerations representing component behaviors.
    2. **Instantiate**: Create the `StateMachine<State, Trigger>` instance inside `InitializeStateMachine()` using a default starting state.
    3. **Configure Graph**: Map states using `.Configure()`, dictate flow with `.Permit()`, and assign isolated behavior parameters via `.OnEntry()`.
    4. **Bind System Events**: Subscribe to input or external system events during `OnEntityReady()` to act as discrete `.Fire()` triggers. Validate with `.CanFire()` before execution.
    5. **Apply Logic**: Consume the updated variables (e.g., `_currentSpeed`) directly inside `_PhysicsProcess()` without utilizing internal conditional chains.
  </implementation_guide>

  <technical_specifications>
    - **Memory Allocation**: ~200 bytes per `StateMachine` instance.
    - **Performance Overhead (Event-Driven)**: 0 per-frame comparisons (Cost is relegated strictly to trigger events).
    - **Performance Overhead (Polling Pattern)**: 8+ comparisons plus state validity checks per frame (PROHIBITED).
  </technical_specifications>

  <performance_considerations>
    | Approach | Per-Frame Cost | Memory Overhead | Maintainability | Best Use Case |
    |----------|----------------|-----------------|-----------------|---------------|
    | **Simple if/else** | 4 comparisons | 0 bytes | High (for simple logic) | Threshold checks, 2-5 states |
    | **Stateless (Event-Driven)** | 0 comparisons | ~200 bytes | High (for complex logic) | 8+ states, event-driven flow |
    | **Stateless (Polling)** ❌ | 8+ comparisons + state checks | ~200 bytes | Low (over-engineered) | NEVER use this pattern |

    **Key Insight:** Stateless should REDUCE per-frame overhead by eliminating polling, not increase it. If you're checking conditions every frame to fire triggers, you're using it wrong.

    **Example Comparison:**
    ```csharp
    // Simple if/else: 4 comparisons per frame
    if (speed > sprintThreshold) return "Sprint";
    if (speed > walkThreshold) return "Walk";
    return "Idle";

    // Stateless (Event-Driven): 0 comparisons per frame
    _inputComponent.OnSprintPressed += () => _machine.Fire(Trigger.Sprint);
    // State machine sets _currentSpeed once, _PhysicsProcess just applies it

    // Stateless (Polling) ❌: 8+ comparisons per frame
    if (speed > sprintThreshold && _machine.CanFire(Trigger.Sprint))
        _machine.Fire(Trigger.Sprint); // WRONG!
    ```
  </performance_considerations>

  <code_templates>
    <template name="ControlLayerMovementStateMachine">
      <code><![CDATA[
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
        // Zero if/else chains - rely purely on state-controlled variables
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
    
    public event Action<string> OnAnimationRequested;
    
    private void EmitAnimationCommand(string animName)
    {
        OnAnimationRequested?.Invoke(animName);
    }
}
      ]]></code>
    </template>
  </code_templates>

  <core_rules>
    <rule>
      <description>ALWAYS place state machines strictly in components that control system behavior (MovementComponent, AIController).</description>
      <rationale>Maintains pure MVC-style component separation. Decisions dictate state, rendering visually reflects state.</rationale>
      <example>
        <![CDATA[
// CORRECT 
public class PlayerController : Node { private StateMachine _machine; }

// INCORRECT
public class UIHealthBar : Node { private StateMachine _machine; }
        ]]>
      </example>
    </rule>
  </core_rules>
</layer_2_detailed_guide>

<layer_3_advanced>
  <troubleshooting>
    <error symptom="High frame-time spikes or unintended rapid state switching in _PhysicsProcess.">
      <cause>Implementation is manually checking input values or velocity variables every frame to fire triggers (Polling).</cause>
      <fix>Eradicate `_machine.Fire()` from `_PhysicsProcess()`. Bind firing events strictly to explicit state changes emitted by Input Components or external signals.</fix>
    </error>
    <error symptom="InvalidOperationException during state machine execution.">
      <cause>Attempted to fire a trigger that lacks a `.Permit()` mapping from the currently active state.</cause>
      <fix>Wrap all trigger execution calls in the guard clause: `if (_machine.CanFire(Trigger.Event)) { _machine.Fire(Trigger.Event); }`.</fix>
    </error>
  </troubleshooting>

  <best_practices>
    <rule>
      <description>ALWAYS adhere to the "Call Down, Signal Up" pattern for triggering visual outputs.</description>
      <rationale>Ensures strict decoupling. State machines emit signals mapping to their current logic; isolated animation or audio components subscribe to those signals.</rationale>
      <example>
        <![CDATA[
// SIGNAL UP
public event Action<string> OnAnimationRequested;
_machine.Configure(State.Idle).OnEntry(() => OnAnimationRequested?.Invoke("Idle"));
        ]]>
      </example>
    </rule>
    <rule>
      <description>ALWAYS export and document complex machine logic using the integrated DOT graph utility.</description>
      <rationale>Ensures precise state flow mapping is preserved for project team members and visually verified via WebGraphViz.</rationale>
      <example>
        <![CDATA[
string dotGraph = UmlDotGraph.Format(_machine.GetInfo());
System.IO.File.WriteAllText("state_diagram.dot", dotGraph);
        ]]>
      </example>
    </rule>
  </best_practices>
</layer_3_advanced>