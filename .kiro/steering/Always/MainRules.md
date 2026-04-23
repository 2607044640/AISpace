---
inclusion: always
---
<layer_1_quick_start>
  <quick_reference>
    - Compilation Command: `dotnet build` (Execution directory: `3d-practice/`)
    - Godot Log Path: `$env:APPDATA/Godot/app_userdata/Tesseract_Backpack/logs/godot.log`
    - Recent Changes: `Get-Content "C:\Users\26070\My Drive\Kiro_Godot_Brain\AI_Context_Changes.md" -Head <lines>` (XML 格式测试)
    - Architecture & Steering Path: `KiroWorkingSpace/.kiro/`
    - Project Code Path: `3d-practice/`
    - Internal State Tracking: `KiroWorkingSpace/.kiro/Scratchpad/`
    
    **Steering File Purposes:**
    - `ProjectRules.md`: Architectural patterns, R3 rules, naming conventions, component communication.
    - `BugInvestigation.md`: Systematic debugging protocol, 3-Strike Rule, escalation procedures.
  </quick_reference>

  <quickstart_workflow>
    1. Read `ConversationReset.md`, `docLastConversationState.md`, and `ProjectRules.md` to establish context.
    2. Execute `mcp_sequential_thinking_sequentialthinking` on EVERY request.
    3. Verify assumptions and existing code state.
    4. Execute implementation incrementally (read files, run commands, make changes).
    5. Run `dotnet build` immediately after ANY C# modifications.
    6. Update internal state, checklists, and bug logs in `.kiro/Scratchpad/` silently.
  </quickstart_workflow>

  <error_escalation>
    **IF 3 consecutive fix attempts fail for the same issue:**
    - HALT execution immediately.
    - Read and follow instructions in `C:\Godot\KiroWorkingSpace\.kiro\steering\StableOrOther\BugInvestigation.md`.
    - Use the Escalation Template to request human intervention.
  </error_escalation>
</layer_1_quick_start>

<layer_2_detailed_guide>
  <api_reference>
    - Core MCPs: `mcp_sequential_thinking_sequentialthinking`, `mcp_godot_launch_editor`, `mcp_godot_run_project`, `mcp_godot_get_debug_output`
    - Scene MCPs: `mcp_godot_create_scene`, `mcp_godot_add_node`, `mcp_godot_save_scene`
    - Asset MCPs: `mcp_godot_load_sprite`, `mcp_godot_export_mesh_library` (Req: MeshInstance3D)
    - UID MCPs: `mcp_godot_get_uid`, `mcp_godot_update_project_uids`
  </api_reference>

  <scene_management>
    - Edit existing `.tscn` files directly to add nodes, modify properties, connect signals, and set Export variables.
    - Execute file edits yourself; do not ask the user to edit manually.
    - **CRITICAL SYNC:** Any renaming of `[Export]` variables or node paths in C# MUST trigger an immediate, corresponding text edit in the associated `.tscn` file.
  </scene_management>

  <error_recovery_protocol>
    - **NO BLIND FIXES:** If `dotnet build` fails or runtime errors occur, guessing or blind code modification is STRICTLY FORBIDDEN.
    - **LOGS FIRST:** Run the specific scene (F6) to generate logs, wait 2 seconds or prompt the user to interact, then fetch via `mcp_godot_get_debug_output` or read `godot.log`.
    - **MANDATORY ANALYSIS:** Force the use of `mcp_sequential_thinking_sequentialthinking` to analyze the root cause from the logs before executing any code changes.
  </error_recovery_protocol>

  <csharp_scene_sync_constraint>
    - **STRICT SYNC:** If you modify an `[Export]` variable name or a `GetNode<Type>("Path")` string in a `.cs` script, you MUST synchronously open and modify the corresponding `.tscn` file. (Failure to do this causes immediate `NullReferenceException` at runtime).
  </csharp_scene_sync_constraint>

  <core_rules>
    <rule>
      <description>Call mcp_sequential_thinking_sequentialthinking on EVERY request.</description>
      <rationale>Ensures structured analysis prior to any action execution, verifying assumptions before implementation.</rationale>
    </rule>
    <rule>
      <description>Design all code and architecture with extensibility and generality as core principles.</description>
      <rationale>Future-proof design prevents technical debt. Use generic abstractions and parameterized logic. (Exception: Scratchpad files).</rationale>
    </rule>
    <rule>
      <description>Store ALL rules, steering files, and architecture documents EXCLUSIVELY in KiroWorkingSpace/.kiro/.</description>
      <rationale>Maintains strict separation between system instructions and Godot project source code.</rationale>
    </rule>
    <rule>
      <description>Execute dotnet build from 3d-practice/ after writing ANY C# code.</description>
      <rationale>Catches C# compilation errors immediately via the .sln file.</rationale>
    </rule>
    <rule>
      <description>Use .kiro/Scratchpad/ EXCLUSIVELY for internal state tracking, checklists, and cross-session bug logs.</description>
      <rationale>Isolates working memory from permanent documentation and prevents conversational bloat.</rationale>
    </rule>
    <rule>
      <description>Delete documentation ruthlessly if the explanation applies to programming in general rather than the specific feature.</description>
      <rationale>Keeps context windows highly concentrated on Godot/Project specific logic rather than generic coding tutorials.</rationale>
    </rule>
  </core_rules>
</layer_2_detailed_guide>