---
inclusion: always
---
<layer_1_quick_start>
  <quick_reference>
    - Compilation Command: `dotnet build` (Execution directory: `3d-practice/`)
    - Godot Log Path: `$env:APPDATA/Godot/app_userdata/Tesseract_Backpack/logs/godot.log`
    - Recent Changes: `Get-Content "C:\Users\26070\My Drive\Kiro_Godot_Brain\AI_Context_Changes.md" -Head <lines>`
    - Architecture & Steering Path: `KiroWorkingSpace/.kiro/`
    - Project Code Path: `3d-practice/`
    - Internal State Tracking: `KiroWorkingSpace/.kiro/Scratchpad/`
    
    **Steering File Purposes:**
    - `DesignPatterns.md`: Architectural patterns, R3 reactive rules, naming conventions, component communication, troubleshooting. (Why: Daily development reference - patterns + problem solving)
    - `BugInvestigation.md`: Systematic debugging protocol, 3-Strike Rule, Confidence Score evaluation, escalation procedures. (Why: Structured investigation for complex/rare bugs)
  </quick_reference>

  <quickstart_workflow>
    1. Read `ConversationReset.md`, `docLastConversationState.md`, and `ProjectRules.md` to establish context.
    2. Execute `mcp_sequential_thinking_sequentialthinking` on every request.
    3. Verify assumptions and existing code state.
    4. Execute implementation incrementally (read files, run commands, make changes).
    5. Run `dotnet build` immediately after any C# modifications.
    6. Update internal state, checklists, and bug logs in `.kiro/Scratchpad/` silently.
  </quickstart_workflow>

  <error_escalation>
    **IF 3 consecutive fix attempts fail for the same issue:**
    - HALT execution immediately
    - Read and follow instructions in `C:\Godot\KiroWorkingSpace\.kiro\steering\StableOrOther\BugInvestigation.md`
    - Use the Escalation Template to request human intervention
  </error_escalation>
</layer_1_quick_start>

<layer_2_detailed_guide>
  <api_reference>
    - `mcp_sequential_thinking_sequentialthinking`
    - `mcp_godot_get_godot_version`
    - `mcp_godot_list_projects`
    - `mcp_godot_get_project_info`
    - `mcp_godot_launch_editor`
    - `mcp_godot_run_project`
    - `mcp_godot_stop_project`
    - `mcp_godot_get_debug_output`
    - `mcp_godot_create_scene`
    - `mcp_godot_add_node`
    - `mcp_godot_save_scene`
    - `mcp_godot_load_sprite`
    - `mcp_godot_export_mesh_library` (Requires: MeshInstance3D)
    - `mcp_godot_get_uid`
    - `mcp_godot_update_project_uids`
  </api_reference>

  <core_rules>
    <rule>
      <description>Call mcp_sequential_thinking_sequentialthinking on EVERY request.</description>
      <rationale>Ensures structured analysis prior to any action execution, verifying assumptions before implementation.</rationale>
    </rule>
    <rule>
      <description>Store ALL rules, steering files, and architecture documents exclusively in KiroWorkingSpace/.kiro/.</description>
      <rationale>Maintains strict separation between system/instruction files and the Godot project source code.</rationale>
    </rule>
    <rule>
      <description>Execute dotnet build from the 3d-practice/ directory after writing ANY C# code or when verification is needed.</description>
      <rationale>Catches C# compilation errors immediately; relies on auto-detection of the .sln file in the directory.</rationale>
    </rule>
    <rule>
      <description>Use .kiro/Scratchpad/ exclusively for internal state tracking, complex task checklists, and cross-session bug logs.</description>
      <rationale>Isolates working memory from permanent documentation and prevents conversational bloat.</rationale>
    </rule>
  </core_rules>
</layer_2_detailed_guide>

<layer_3_advanced>
  <best_practices>
    - Delete documentation ruthlessly if the explanation applies to programming in general rather than the specific feature.
    - Implement functionality incrementally and verify each individual step.
    - Save permanent documentation, steering files, and specifications strictly outside of the Scratchpad directory.
  </best_practices>
</layer_3_advanced>
