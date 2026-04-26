---
trigger: manual
---

## Quick Reference
- **Tool**: `mcp_sequential_thinking_sequentialthinking`
- **Log Path**: `$env:APPDATA/Godot/app_userdata/Tesseract_Backpack/logs/godot.log`
- **Profiler Path**: Godot Editor → Debug → Profiler
- **Target Confidence Threshold**: 8/10 (Minimum required before execution)

## Decision Tree
- **IF** no profiling data available: Request profiling data or add logs. (Why: Prevent premature optimization.)
- **IF** Confidence Score < 8 OR bottleneck unknown: Add targeted logs, check Profiler.
- **IF** optimization breaks tests/behavior: REVERT immediately. (Why: Correctness > Performance.)
- **IF** Confidence Score >= 8 AND bottleneck confirmed: Apply targeted optimization to THAT bottleneck ONLY.

## Implementation Workflow
1. **Execute** `mcp_sequential_thinking_sequentialthinking` to establish analytical context.
2. **Build Knowledge Inventory**: Map FPS/frame time, identify `_Process` inhabitants, locate memory/GC spikes.
3. **Assign Confidence Score**: If < 8, mandate Godot Profiler usage, inject timestamps, isolate suspected systems.
4. **Validate Bottleneck**: Confirm exact file/method. Measure baseline metrics (FPS, frame time).
5. **Apply Targeted Optimization**: Refactor isolated bottleneck. Run `dotnet build`. Validate performance improved AND behavior is identical.

## Best Practices
- **Profile First**: Always run Godot Profiler before assuming bottlenecks.
- **Measure Impact**: Record FPS/frame time before and after optimization.
- **One Change at a Time**: Optimize one system, measure, then move to the next.
- **Documentation**: Comment non-standard code structures resulting from an optimization.

<top_anti_patterns>
  <rule>
    <description>NEVER optimize without profiling data.</description>
    <rationale>Wastes time on non-bottlenecks and degrades maintainability.</rationale>
  </rule>
  <rule>
    <description>NEVER use anonymous objects in `Observable.EveryUpdate()`.</description>
    <rationale>Triggers severe GC allocations every frame.</rationale>
    <example>
      // CORRECT (Zero allocation)
      Observable.EveryUpdate().Select(_ => (Position, Velocity)).Subscribe(d => Process(d.Item1, d.Item2));
    </example>
  </rule>
  <rule>
    <description>NEVER use `ReactiveProperty<T>` for high-frequency physics data like Velocity.</description>
    <rationale>Induces extreme allocation overhead.</rationale>
    <example>
      // CORRECT
      public Vector3 Velocity { get; set; }
      Observable.EveryPhysicsUpdate().Select(_ => Velocity).Subscribe(v => ProcessVelocity(v));
    </example>
  </rule>
</top_anti_patterns>

<system_reminder>
If multiple bottlenecks are identified, prioritize by impact and optimize ONE at a time. If an engine/OS bug is suspected, document and escalate to the user. Do NOT hack around core engine bugs with micro-optimizations.
</system_reminder>