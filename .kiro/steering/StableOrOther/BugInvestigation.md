---
inclusion: manual
---

<bug_investigation_rules>

  <layer_1_quick_start>
  
    <quick_reference>
      - Tool: `mcp_sequential_thinking_sequentialthinking`
      - Core Rule: 3-Strike Rule (Max 3 failed fix attempts before escalation)
    </quick_reference>
    
    <decision_tree>
      - IF Confidence < 7 OR blind spots: ALWAYS trigger web/doc search (Why: NEVER guess missing facts)
      - IF Confidence >= 7 AND search complete: Proceed with execution
      - IF 3 consecutive fails for same issue: Halt and escalate (Why: Prevents infinite loops)
      - IF deadlocks, timing issues, or Godot/OS bugs: Halt and escalate
    </decision_tree>
    
  </layer_1_quick_start>

  <layer_2_detailed_guide>
  
    <api_reference>
      - Tool: `mcp_sequential_thinking_sequentialthinking`
      - Purpose: Enforces mandatory logic sequence before fixes
    </api_reference>

    <implementation_guide>
      <step>Execute mcp_sequential_thinking_sequentialthinking to catalog Knowledge Inventory.</step>
      <step>Pinpoint Blind Spots and assign Confidence Score (1-10).</step>
      <step>Trigger search if Confidence < 7.</step>
      <step>Read error logs completely and add targeted debug logging.</step>
      <step>Apply EXACTLY ONE change per iteration and verify compilation.</step>
    </implementation_guide>

    <technical_specifications>
      - Engine: Godot 4.6.1 stable mono
      - Language: C#
      - OS: Windows
    </technical_specifications>

    <core_rules>
      <rule>
        <description>ALWAYS halt execution and output the Escalation Template upon meeting any escalation trigger.</description>
        <rationale>Escalation triggers indicate system-level issues or unsolvable state loops requiring human intervention.</rationale>
      </rule>
    </core_rules>

    <code_templates>
      <template name="escalation_query_template">
        <code><![CDATA[
# Bug Report for Gemini

## Environment
- Engine: Godot 4.6.1 stable mono
- Language: C#
- OS: Windows

## Problem
[Provide a precise, one-sentence description of the issue]

## What I Tried
1. [First attempt methodology and exact result]
2. [Second attempt methodology and exact result]
3. [Third attempt methodology and exact result]

## Current Code
```csharp
[Insert the specific, relevant C# code block causing the issue]
```

## Error Logs
[Paste complete error output from Godot console or dotnet build]

## Question
[What specific aspect needs clarification or alternative approach?]
        ]]></code>
      </template>
    </code_templates>
    
  </layer_2_detailed_guide>

  <layer_3_advanced>
  
    <troubleshooting>
      <error symptom="Unexpected runtime behavior or unhandled exceptions">
        <cause>Silenced runtime errors or logic bugs not caught by dotnet build.</cause>
        <fix>Parse $env:APPDATA/Godot/app_userdata/Tesseract_Backpack/logs/godot.log for raw engine logs.</fix>
      </error>
      
      <error symptom="Implementation violates user architecture">
        <cause>Blindly accepting assumptions or pivoting architecture without user approval.</cause>
        <fix>Re-read docLastConversationState.md and request authorization before altering architecture.</fix>
      </error>
      
      <error symptom="mcp_godot_export_mesh_library execution failure">
        <cause>Missing required node type in target scene.</cause>
        <fix>Ensure target node is strictly a MeshInstance3D before invoking export tool.</fix>
      </error>
      
      <error symptom="Infinite UI loops or massive CPU spikes">
        <cause>Two-way binding echo without termination condition.</cause>
        <fix>Insert .DistinctUntilChanged() into subscription chain to drop duplicate payloads.</fix>
        <example>
          // ❌ Problem: Infinite loop
          slider.OnValueChangedAsObservable().Subscribe(value => _volume.Value = value);
          _volume.Subscribe(value => slider.Value = value);  // Triggers slider change again!
          
          // ✅ Solution: Block duplicates
          slider.OnValueChangedAsObservable().DistinctUntilChanged().Subscribe(value => _volume.Value = value);
          _volume.DistinctUntilChanged().Subscribe(value => slider.Value = value);
        </example>
      </error>
      
      <error symptom="Cross-thread crash or UI freezing">
        <cause>Async task manipulating Node property from background thread.</cause>
        <fix>Append .ObserveOn(GodotProvider.MainThread) immediately before .Subscribe().</fix>
        <example>
          Observable.Timer(TimeSpan.FromSeconds(2))
              .ObserveOn(GodotProvider.MainThread)  // Force UI thread
              .Subscribe(_ => label.Text = "Done!");
        </example>
      </error>
      
      <error symptom="Micro-stutters or frame drops (GC Spikes)">
        <cause>Heap allocation using anonymous objects in EveryUpdate/EveryPhysicsUpdate loops.</cause>
        <fix>Use struct-based ValueTuples instead of anonymous objects.</fix>
        <example>
          // ❌ Problem: Allocates memory every frame
          Observable.EveryUpdate()
              .Select(_ => new { PlayerPos = player.Position, EnemyPos = enemy.Position })
              .Subscribe(data => { var distance = data.PlayerPos.DistanceTo(data.EnemyPos); });
          
          // ✅ Solution: ValueTuple on stack
          Observable.EveryUpdate()
              .Select(_ => (PlayerPos: player.Position, EnemyPos: enemy.Position))
              .Subscribe(tuple => { var distance = tuple.PlayerPos.DistanceTo(tuple.EnemyPos); });
        </example>
      </error>
    </troubleshooting>

    <best_practices>
      - Delete documentation ruthlessly if it applies to generic programming instead of specific features.
      - Implement and verify functionality incrementally.
      - Save permanent docs, steering files, and specs strictly outside the Scratchpad directory.
    </best_practices>
    
  </layer_3_advanced>

</bug_investigation_rules>
