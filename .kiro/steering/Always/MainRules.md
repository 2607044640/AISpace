---
inclusion: always
---
<layer_1_quick_start>
  <quick_reference>
    - Compilation Command: `dotnet build` (Execution directory: `3d-practice/`)
    - Godot Log Path: `$env:APPDATA/Godot/app_userdata/Tesseract_Backpack/logs/godot.log`
    - Architecture & Steering Path: `KiroWorkingSpace/.kiro/`
    - Project Code Path: `3d-practice/`
    - Internal State Tracking: `KiroWorkingSpace/.kiro/Scratchpad/`
  </quick_reference>

  <quickstart_workflow>
    1. Read `ConversationReset.md`, `docLastConversationState.md`, and `ProjectRules.md` to establish context.
    2. Execute `mcp_sequential_thinking_sequentialthinking` on every request.
    3. Verify assumptions and existing code state.
    4. Execute implementation incrementally (read files, run commands, make changes).
    5. Run `dotnet build` immediately after any C# modifications.
    6. Update internal state, checklists, and bug logs in `.kiro/Scratchpad/` silently.
  </quickstart_workflow>

  <decision_tree>
    * Is the function trivial (lifecycle hooks, simple getters)? -> Omit documentation entirely. (Why: Prevents noise and wasted lines explaining self-evident code.)
    * Is the function simple? -> Use single-sentence summary or inline comments. (Why: Maintains flexibility without forcing rigid structures.)
    * Is the function complex or logic-heavy? -> Apply mandatory 3-part structure (目的/Purpose, 示例/Example, 算法/Algorithm). (Why: Ensures logic execution steps map strictly 1:1 to code.)
    * Does analysis show a significantly better architectural approach? -> Propose approach but wait for user approval before pivoting. (Why: Prevents unauthorized deviations from explicitly requested architecture.)
  </decision_tree>

  <top_anti_patterns>
    * Skipping `dotnet build` after C# edits. (Why: Fails to catch errors immediately during development.)
    * Summarizing or narrating `.kiro/Scratchpad/` updates to the user. (Why: Pollutes conversation output with internal tracking data.)
    * Documenting general programming concepts or textbook math. (Why: Violates strict anti-noise constraints; documentation must strictly apply to the specific project/game.)
    * Renaming properties/fields with arbitrary alternative names. (Why: Creates cognitive overhead and breaks code searchability.)
  </top_anti_patterns>
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
    <rule>
      <description>Enforce the 3-part documentation structure (目的, 示例, 算法) exclusively on complex/logic-heavy functions.</description>
      <rationale>Standardizes complex logic explanation while preventing documentation bloat on simple or trivial functions.</rationale>
    </rule>
    <rule>
      <description>NEVER rename properties/fields with arbitrary names. Use exact type name, camelCase, abbreviations, or lowercase only.</description>
      <rationale>Maintains 1:1 type-to-variable mapping for instant searchability.</rationale>
    </rule>
  </core_rules>
</layer_2_detailed_guide>

<layer_3_advanced>
  <troubleshooting>
    <error symptom="Unexpected Godot runtime behavior or unhandled exceptions during execution.">
      <cause>Silenced runtime errors or logic bugs not caught by dotnet build compilation.</cause>
      <fix>Check Godot Output tab or parse $env:APPDATA/Godot/app_userdata/Tesseract_Backpack/logs/godot.log for raw engine logs.</fix>
    </error>
    <error symptom="Implementation fails to integrate properly with existing systems or violates user architecture.">
      <cause>Blindly accepting assumptions or pivoting architecture without explicit user approval.</cause>
      <fix>Re-read docLastConversationState.md, execute sequential thinking, and request authorization before altering architecture.</fix>
    </error>
    <error symptom="mcp_godot_export_mesh_library execution failure.">
      <cause>Missing required node type in the target scene.</cause>
      <fix>Ensure the target node is specifically a MeshInstance3D before invoking the export tool.</fix>
    </error>
  </troubleshooting>

  <best_practices>
    - Delete documentation ruthlessly if the explanation applies to programming in general rather than the specific feature.
    - Implement functionality incrementally and verify each individual step.
    - Save permanent documentation, steering files, and specifications strictly outside of the Scratchpad directory.
  </best_practices>
</layer_3_advanced>