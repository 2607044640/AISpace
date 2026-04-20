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
      <description>Use TypeName_Purpose format for all fields/properties. Both parts PascalCase.</description>
      <rationale>Enables bidirectional search (by type or purpose) and eliminates cognitive overhead.</rationale>
      <examples>
        ✅ CORRECT: OptionButton_Theme, PopupMenu_MenuOption, Button_Option
        ❌ FORBIDDEN: _themeDropdown, optionButton, menuPopup (arbitrary names)
      </examples>
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