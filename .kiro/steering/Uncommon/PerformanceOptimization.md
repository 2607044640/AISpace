---
inclusion: manual
---

<performance_optimization_rules>
  <layer_1_quick_start>
    <quick_reference>
      - Tool: `mcp_sequential_thinking_sequentialthinking`
      - Log Path: `$env:APPDATA/Godot/app_userdata/Tesseract_Backpack/logs/godot.log`
      - Profiler Path: Godot Editor → Debug → Profiler
      - Target Confidence Threshold: 8/10 (Minimum required before optimization execution)
    </quick_reference>

    <decision_tree>
      - IF no profiling data available:
        - ACTION: Request profiling data or add performance logging. (Why: Optimizing without data is premature optimization that breaks working code.)
      - IF Confidence Score < 8 OR bottleneck location unknown:
        - ACTION: Add targeted performance logging, check Godot profiler, analyze frame times. (Why: Must identify actual bottleneck before optimizing.)
      - IF optimization breaks tests or changes behavior:
        - ACTION: Revert immediately and re-evaluate approach. (Why: Correctness ALWAYS takes precedence; performance gains are worthless if functionality breaks.)
      - IF Confidence Score >= 8 AND bottleneck confirmed:
        - ACTION: Apply targeted optimization to confirmed bottleneck ONLY. (Why: High confidence threshold met with validated target.)
    </decision_tree>

    <top_anti_patterns>
      <rule>
        <description>**NEVER** optimize without profiling data or performance metrics.</description>
        <rationale>Premature optimization wastes time on non-bottlenecks and often degrades codebase maintainability.</rationale>
      </rule>
      <rule>
        <description>**NEVER** apply generic optimizations without understanding the specific bottleneck.</description>
        <rationale>Generic advice (e.g., "use object pooling") may fail to address the actual problem while adding unnecessary complexity.</rationale>
      </rule>
      <rule>
        <description>**NEVER** optimize multiple systems simultaneously.</description>
        <rationale>It becomes mathematically impossible to isolate and measure which specific change yielded the performance improvement.</rationale>
      </rule>
      <rule>
        <description>**NEVER** sacrifice code readability for micro-optimizations without a proven need.</description>
        <rationale>The severe loss in maintainability is not justified by negligible or theoretical performance gains.</rationale>
      </rule>
    </top_anti_patterns>
  </layer_1_quick_start>

  <layer_2_detailed_guide>
    <api_reference>
      - `mcp_sequential_thinking_sequentialthinking`: Core tool for enforcing mandatory profiling and analytical context establishment.
      - `Godot Profiler`: Engine-native metric capture (Debug → Profiler).
      - `Observable.EveryUpdate()` / `Observable.EveryPhysicsUpdate()`: High-frequency loop hooks.
    </api_reference>

    <implementation_guide>
      <step>Execute `mcp_sequential_thinking_sequentialthinking` to establish analytical context and prevent premature action.</step>
      <step>Build Knowledge Inventory: Map FPS/frame time, identify `_Process`/`_PhysicsProcess` inhabitants, monitor frame drops, flag every-frame operations, and spot infinite/recursive loops.</step>
      <step>Identify Blind Spots: Determine if bounds are CPU or GPU, pinpoint the exact script/node, monitor memory leaks/GC spikes, and locate profiling metrics.</step>
      <step>Assign Confidence Score (1-10): If < 8, mandate Godot Profiler usage, inject targeted `GD.Print` timestamps, check process/physics/rendering breakdowns, and isolate suspected systems via toggling.</step>
      <step>Validate Bottleneck: Confirm the exact file/method responsible, measure baseline metrics (FPS, frame time > 10% total execution), and document the delta.</step>
      <step>Apply Targeted Optimization: Refactor the isolated bottleneck ONLY. Run `dotnet build` and test suites. Validate that performance improved AND behavior remained completely identical.</step>
    </implementation_guide>

    <technical_specifications>
      - Engine Target: Godot 4.6.1 stable mono
      - Language Target: C#
      - Performance Target: 60 FPS (16.67ms maximum frame time)
    </technical_specifications>

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

    <core_rules>
      <rule>
        <description>**ALWAYS** obtain profiling data before attempting any optimization.</description>
        <rationale>Prevents premature optimization and ensures effort directly targets empirical bottlenecks.</rationale>
      </rule>
      <rule>
        <description>**ALWAYS** verify a Confidence Score >= 8 before authorizing optimization.</description>
        <rationale>Enforces a higher-than-normal threshold due to the severe risk of introducing regressions into functional code.</rationale>
      </rule>
      <rule>
        <description>**ALWAYS** measure and log performance explicitly before and after an optimization pass.</description>
        <rationale>Validates the exact statistical improvement and justifies the change.</rationale>
      </rule>
      <rule>
        <description>**ALWAYS** execute optimization on exactly one system at a time.</description>
        <rationale>Guarantees variable isolation for accurate performance measurement.</rationale>
      </rule>
      <rule>
        <description>**NEVER** use anonymous objects in `Observable.EveryUpdate()` or `Observable.EveryPhysicsUpdate()`.</description>
        <rationale>Triggers severe Garbage Collection (GC) allocations every single frame.</rationale>
        <example>
          <![CDATA[
          // INCORRECT (Allocates every frame)
          Observable.EveryUpdate()
              .Select(_ => new { pos = Position, vel = Velocity })
              .Subscribe(data => Process(data.pos, data.vel));

          // CORRECT (Zero allocation using ValueTuples)
          Observable.EveryUpdate()
              .Select(_ => (Position, Velocity))
              .Subscribe(data => Process(data.Item1, data.Item2));
          ]]>
        </example>
      </rule>
      <rule>
        <description>**NEVER** use `ReactiveProperty<T>` for high-frequency physics data (e.g., Velocity).</description>
        <rationale>Induces extreme allocation overhead during high-frequency polling.</rationale>
        <example>
          <![CDATA[
          // INCORRECT (Allocation overhead every physics frame)
          public ReactiveProperty<Vector3> Velocity { get; } = new();

          // CORRECT (Standard property polled on demand)
          public Vector3 Velocity { get; set; }
          Observable.EveryPhysicsUpdate()
              .Select(_ => Velocity)
              .Subscribe(vel => ProcessVelocity(vel));
          ]]>
        </example>
      </rule>
    </core_rules>
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

    <troubleshooting>
      <error symptom="Frame drops every few seconds, GC spikes visible in Godot Profiler.">
        <cause>Anonymous objects or string concatenations executing within `_Process` or `_PhysicsProcess` update loops.</cause>
        <fix><![CDATA[Replace anonymous objects with `ValueTuples`. Cache static strings and implement `StringBuilder` for dynamic string mutations inside loops.]]></fix>
      </error>

      <error symptom="High CPU usage in _Process, multiple GetNode calls registering in profiler.">
        <cause>`GetNode` or `GetNodeOrNull` is being invoked dynamically every frame instead of being cached during initialization.</cause>
        <fix>
          <![CDATA[
          // FIX: Cache node references in _Ready using [Export] NodePath
          [Export] public NodePath PlayerPath { get; set; } = "%Player";
          private Player _player;

          public override void _Ready() {
              _player = GetNodeOrNull<Player>(PlayerPath);
          }

          public override void _Process(double delta) {
              _player?.Update();
          }
          ]]>
        </fix>
      </error>

      <error symptom="High CPU usage, severe heap allocations originating from LINQ operations.">
        <cause>LINQ queries (`Where`, `Select`, `ToList`) executing continuously inside frame loops.</cause>
        <fix>
          <![CDATA[
          // FIX: Pre-allocate collections, clear them, and use standard `for/foreach` loops.
          private List<Enemy> _activeEnemies = new();

          public override void _Process(double delta) {
              _activeEnemies.Clear();
              foreach (var enemy in enemies) {
                  if (enemy.IsActive) _activeEnemies.Add(enemy);
              }
              ProcessEnemies(_activeEnemies);
          }
          ]]>
        </fix>
      </error>

      <error symptom="Suspected engine bug or OS-level rendering issue degrading performance.">
        <cause>Bottleneck occurs below the C# script execution layer (e.g., Godot core, drivers).</cause>
        <fix>Document all findings, capture profiler dumps, and immediately escalate to the user for external investigation. Do NOT attempt to hack around core engine bugs with script-level micro-optimizations.</fix>
      </error>
    </troubleshooting>

    <best_practices>
      - **Profile First:** Always run Godot Profiler before making assumptions about bottlenecks.
      - **Measure Impact:** Record FPS/frame time before and after each optimization.
      - **One Change at a Time:** Optimize one system, measure, then move to next bottleneck.
      - **Preserve Readability:** Only sacrifice code clarity for proven, significant performance gains.
      - **Documentation Mandate:** Comment all non-standard code structures resulting from an optimization to prevent future developers from refactoring it back to a slower, more idiomatic pattern.
      - **Regression Safeguards:** Ensure robust unit testing occurs locally before committing optimized paths. Correctness > Performance.
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