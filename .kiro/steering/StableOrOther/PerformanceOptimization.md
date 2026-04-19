---
inclusion: manual
---
<performance_optimization_rules>
  <layer_1_quick_start>
    <quick_reference>
      - Tool: `mcp_sequential_thinking_sequentialthinking`
      - Confidence Threshold: 8/10 before optimization (higher due to risk)
      - Core Rule: Profile BEFORE optimizing (never guess bottlenecks)
    </quick_reference>
    
    <decision_tree>
      - IF no profiling data available:
        - ACTION: Request profiling data or add performance logging. (Why: Optimizing without data is premature optimization that breaks working code.)
      - IF Confidence Score < 8 OR bottleneck location unknown:
        - ACTION: Add targeted performance logging, check Godot profiler, analyze frame times. (Why: Must identify actual bottleneck before optimizing.)
      - IF optimization breaks tests or changes behavior:
        - ACTION: Revert immediately and re-evaluate approach. (Why: Performance gains are worthless if functionality breaks.)
      - IF Confidence Score >= 8 AND bottleneck confirmed:
        - ACTION: Apply targeted optimization to confirmed bottleneck only. (Why: High confidence threshold met with validated target.)
    </decision_tree>
    
    <top_anti_patterns>
      <rule>
        <description>NEVER optimize without profiling data or performance metrics.</description>
        <rationale>Premature optimization wastes time on non-bottlenecks and often makes code worse.</rationale>
      </rule>
      <rule>
        <description>NEVER apply generic optimizations without understanding the specific bottleneck.</description>
        <rationale>Generic advice (e.g., "use object pooling") may not address the actual problem and adds complexity.</rationale>
      </rule>
      <rule>
        <description>NEVER optimize multiple systems simultaneously.</description>
        <rationale>Makes it impossible to measure which change actually improved performance.</rationale>
      </rule>
      <rule>
        <description>NEVER sacrifice code readability for micro-optimizations without proven need.</description>
        <rationale>Maintainability loss is not worth negligible performance gains.</rationale>
      </rule>
    </top_anti_patterns>
  </layer_1_quick_start>

  <layer_2_detailed_guide>
    <api_reference>
      - Tool: `mcp_sequential_thinking_sequentialthinking`
      - Purpose: Enforces mandatory profiling and analysis before optimization.
      - Godot Profiler: Access via Debug → Profiler in Godot Editor
      - Performance Log: `$env:APPDATA/Godot/app_userdata/Tesseract_Backpack/logs/godot.log`
    </api_reference>

    <implementation_guide>
      <step>Execute `mcp_sequential_thinking_sequentialthinking` to establish context.</step>
      <step>Build Knowledge Inventory:
        - What is the actual FPS / frame time?
        - Which systems run in _Process vs _PhysicsProcess?
        - Are there visible frame drops or consistent low FPS?
        - What operations happen every frame?
        - Are there any obvious infinite loops or recursive calls?
      </step>
      <step>Identify Blind Spots:
        - Is the bottleneck CPU-bound or GPU-bound?
        - Which specific script/node is causing the slowdown?
        - Are there memory leaks or GC spikes?
        - Is the issue in game logic, rendering, or physics?
        - Are there profiling metrics available?
      </step>
      <step>Assign Confidence Score (1-10). If < 8, fill blind spots by:
        - Running Godot Profiler during lag scenario
        - Adding targeted performance logging (GD.Print with timestamps)
        - Checking frame time breakdown (process vs physics vs rendering)
        - Monitoring memory usage and GC collections
        - Isolating suspected systems by temporarily disabling them
      </step>
      <step>Validate bottleneck:
        - Confirm specific file/method causing slowdown
        - Measure baseline performance (FPS, frame time, memory)
        - Verify the bottleneck is actually significant (>10% frame time)
      </step>
      <step>Apply targeted optimization:
        - Optimize ONLY the confirmed bottleneck
        - Measure performance after change
        - Verify functionality remains correct
        - Run `dotnet build` and tests after C# modifications
      </step>
    </implementation_guide>

    <technical_specifications>
      - Engine Target: Godot 4.6.1 stable mono
      - Language Target: C#
      - Performance Target: 60 FPS (16.67ms frame time)
      - Profiling Tools: Godot Profiler, custom performance logging
    </technical_specifications>

    <core_rules>
      <rule>
        <description>ALWAYS obtain profiling data before attempting any optimization.</description>
        <rationale>Prevents premature optimization and ensures effort targets actual bottlenecks.</rationale>
      </rule>
      <rule>
        <description>ALWAYS verify Confidence Score >= 8 before optimizing.</description>
        <rationale>Higher threshold than other protocols due to risk of breaking working code.</rationale>
      </rule>
      <rule>
        <description>ALWAYS measure performance before and after optimization.</description>
        <rationale>Validates that optimization actually improved performance and by how much.</rationale>
      </rule>
      <rule>
        <description>ALWAYS optimize one system at a time.</description>
        <rationale>Enables accurate measurement of each optimization's impact.</rationale>
      </rule>
      <rule>
        <description>ALWAYS verify functionality remains correct after optimization.</description>
        <rationale>Performance gains are worthless if behavior changes or breaks.</rationale>
      </rule>
      <rule>
        <description>NEVER use anonymous objects in Observable.EveryUpdate() or Observable.EveryPhysicsUpdate().</description>
        <rationale>Causes GC allocations every frame. Use ValueTuples instead.</rationale>
      </rule>
      <rule>
        <description>NEVER use ReactiveProperty&lt;T&gt; for high-frequency physics data (e.g., Velocity).</description>
        <rationale>Severe allocation overhead. Use standard properties and poll via Observable.EveryPhysicsUpdate().</rationale>
      </rule>
    </core_rules>

    <knowledge_inventory_checklist>
      <category name="Performance Metrics">
        - [ ] Current FPS / frame time measured?
        - [ ] Frame time breakdown available (process/physics/render)?
        - [ ] Memory usage and GC spike data?
        - [ ] Profiler data captured during lag scenario?
      </category>
      <category name="System Analysis">
        - [ ] Which systems run every frame?
        - [ ] Are there nested loops or recursive calls?
        - [ ] How many nodes are in the scene tree?
        - [ ] Are there expensive operations in _Process/_PhysicsProcess?
      </category>
      <category name="Bottleneck Location">
        - [ ] Specific file/method identified?
        - [ ] CPU-bound or GPU-bound confirmed?
        - [ ] Game logic, rendering, or physics issue?
        - [ ] Single bottleneck or multiple issues?
      </category>
    </knowledge_inventory_checklist>

    <blind_spots_checklist>
      <question>Do I have actual profiling data?</question>
      <action>Run Godot Profiler or add performance logging</action>
      
      <question>Do I know which specific code is causing the bottleneck?</question>
      <action>Add targeted logging with timestamps to narrow down location</action>
      
      <question>Do I know if it's CPU or GPU bound?</question>
      <action>Check Godot Profiler's CPU vs GPU time breakdown</action>
      
      <question>Do I know the baseline performance metrics?</question>
      <action>Measure FPS and frame time before any changes</action>
      
      <question>Do I know if there are memory leaks or GC spikes?</question>
      <action>Monitor memory usage over time and check for GC collections</action>
    </blind_spots_checklist>
  </layer_2_detailed_guide>

  <layer_3_advanced>
    <escalation_triggers>
      <trigger>
        <condition>No profiling data available and user cannot provide it</condition>
        <action>Add performance logging infrastructure first, then re-evaluate</action>
        <rationale>Cannot optimize without knowing the bottleneck</rationale>
      </trigger>
      <trigger>
        <condition>Optimization breaks tests or changes behavior</condition>
        <action>Revert immediately and analyze why behavior changed</action>
        <rationale>Correctness always takes precedence over performance</rationale>
      </trigger>
      <trigger>
        <condition>Multiple unrelated bottlenecks identified</condition>
        <action>Prioritize by impact and optimize one at a time</action>
        <rationale>Prevents confusion about which change improved performance</rationale>
      </trigger>
      <trigger>
        <condition>Suspected engine bug or OS-level issue</condition>
        <action>Document findings and escalate to user for external investigation</action>
        <rationale>Engine/OS bugs are outside scope of code optimization</rationale>
      </trigger>
    </escalation_triggers>

    <common_godot_performance_patterns>
      <pattern name="GC Allocation in Update Loops">
        <symptom>Frame drops every few seconds, GC spikes in profiler</symptom>
        <cause>Anonymous objects or string concatenation in _Process/_PhysicsProcess</cause>
        <fix>Use ValueTuples instead of anonymous objects, cache strings, use StringBuilder</fix>
        <example><![CDATA[
// BAD: Allocates every frame
Observable.EveryUpdate()
    .Select(_ => new { pos = Position, vel = Velocity })
    .Subscribe(data => Process(data.pos, data.vel));

// GOOD: Zero allocation
Observable.EveryUpdate()
    .Select(_ => (Position, Velocity))
    .Subscribe(data => Process(data.Item1, data.Item2));
        ]]></example>
      </pattern>

      <pattern name="ReactiveProperty Overhead">
        <symptom>Consistent frame drops, high CPU usage in property setters</symptom>
        <cause>ReactiveProperty&lt;T&gt; used for high-frequency data like Velocity</cause>
        <fix>Use standard properties and poll via Observable.EveryPhysicsUpdate()</fix>
        <example><![CDATA[
// BAD: Allocation overhead every physics frame
public ReactiveProperty<Vector3> Velocity { get; } = new();

// GOOD: Standard property, poll when needed
public Vector3 Velocity { get; set; }

Observable.EveryPhysicsUpdate()
    .Select(_ => Velocity)
    .Subscribe(vel => ProcessVelocity(vel));
        ]]></example>
      </pattern>

      <pattern name="Excessive GetNode Calls">
        <symptom>High CPU usage in _Process, many GetNode calls in profiler</symptom>
        <cause>GetNode called every frame instead of cached in _Ready</cause>
        <fix>Cache node references in _Ready using [Export] NodePath</fix>
        <example><![CDATA[
// BAD: GetNode every frame
public override void _Process(double delta)
{
    var player = GetNode<Player>("%Player"); // Expensive!
    player.Update();
}

// GOOD: Cache in _Ready
[Export] public NodePath PlayerPath { get; set; } = "%Player";
private Player _player;

public override void _Ready()
{
    _player = GetNodeOrNull<Player>(PlayerPath);
}

public override void _Process(double delta)
{
    _player?.Update();
}
        ]]></example>
      </pattern>

      <pattern name="Unoptimized LINQ in Update Loops">
        <symptom>High CPU usage, many allocations in LINQ operations</symptom>
        <cause>LINQ queries (Where, Select, etc.) executed every frame</cause>
        <fix>Cache results, use for loops, or move logic outside update loop</fix>
        <example><![CDATA[
// BAD: LINQ every frame
public override void _Process(double delta)
{
    var activeEnemies = enemies.Where(e => e.IsActive).ToList(); // Allocates!
    ProcessEnemies(activeEnemies);
}

// GOOD: Cache or use for loop
private List<Enemy> _activeEnemies = new();

public override void _Process(double delta)
{
    _activeEnemies.Clear();
    foreach (var enemy in enemies)
    {
        if (enemy.IsActive) _activeEnemies.Add(enemy);
    }
    ProcessEnemies(_activeEnemies);
}
        ]]></example>
      </pattern>
    </common_godot_performance_patterns>

    <best_practices>
      - **Profile First:** Always run Godot Profiler before making assumptions about bottlenecks.
      - **Measure Impact:** Record FPS/frame time before and after each optimization.
      - **One Change at a Time:** Optimize one system, measure, then move to next bottleneck.
      - **Preserve Readability:** Only sacrifice code clarity for proven, significant performance gains.
      - **Document Optimizations:** Add comments explaining why code is written in a specific way for performance.
      - **Regression Testing:** Verify functionality remains correct after each optimization.
    </best_practices>

    <example_workflow>
      <scenario>User reports: "The game is lagging during combat"</scenario>
      <execution>
        <step>1. Execute mcp_sequential_thinking_sequentialthinking</step>
        <step>2. Knowledge Inventory:
          - User reports lag during combat (not constant)
          - No profiling data provided yet
          - Combat involves multiple enemies and particle effects
        </step>
        <step>3. Blind Spots Identified:
          - What's the actual FPS during lag?
          - Is it CPU or GPU bound?
          - Which specific system is the bottleneck?
          - Are there GC spikes?
        </step>
        <step>4. Confidence Score: 3/10 (too low - need data)</step>
        <step>5. Fill Blind Spots:
          - Request user run Godot Profiler during combat
          - Add performance logging to combat systems
          - Measure FPS and frame time during lag scenario
        </step>
        <step>6. Profiler Results:
          - FPS drops from 60 to 30 during combat
          - CPU time spike in EnemyAI._Process
          - GC collections every 2 seconds
        </step>
        <step>7. Updated Confidence Score: 8/10 (sufficient to proceed)</step>
        <step>8. Targeted Optimization:
          - Found: LINQ query in EnemyAI._Process running every frame
          - Baseline: 30 FPS during combat
          - Fix: Cache enemy list, use for loop instead of LINQ
          - Result: 55 FPS during combat (83% improvement)
          - Verification: Combat behavior unchanged, tests pass
        </step>
      </execution>
    </example_workflow>
  </layer_3_advanced>
</performance_optimization_rules>
