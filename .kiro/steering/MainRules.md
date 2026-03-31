---
inclusion: always
---
<instructions>
  <initialization>
    Read `#KiroWorkingSpace/ConversationReset.md` for protocol.
    Read project's `docLastConversationState.md` and `ProjectRules.md` to restore context.
  </initialization>

  <execution_protocol>
    Call `mcp_sequential_thinking_sequentialthinking` on EVERY request(at least once).特别用户提到思考时！多调用思考！
    Execute actions immediately: read files, run commands, make changes.
    Implement incrementally and verify each step.
    
    Never blindly accept assumptions. Apply critical thinking throughout: Verify assumptions before implementing. Check existing code. Question initial solutions. If analysis shows a significantly better approach, briefly explain why and PROPOSE it, but DO NOT pivot away from my explicitly requested architecture/method unless I approve.
  </execution_protocol>

  <workspace_management>
    Use `.kiro/Scratchpad/` exclusively for your internal state tracking, complex task checklists, and cross-session bug logs.
    DO NOT summarize, narrate, or explain these file updates to the user unless explicitly asked.
    Save permanent docs, steering files, and specs outside the Scratchpad.
    Store ALL architecture rules, steering files, and instructions exclusively in `KiroWorkingSpace/.kiro/`.
  </workspace_management>

  <scene_management>
    <ui_workflow_best_practices>
      ✓ Use AI to build entire initial UI layout (UIBuilder generator)
      ✕ Use AI to modify small details (wastes time, inaccurate)
      ✓ User manually modifies small details in Godot editor
      ✓ Use AI to batch-modify multiple properties (TscnEditor)
    </ui_workflow_best_practices>
    
    Generate UI scenes: Use `.kiro/scripts/ui_builder/generators/godot_ui_builder.py` (see `#GodotUIBuilder.md`).
    Generate StateChart scenes: Use `.kiro/scripts/statechart_builder/godot_statechart_builder.py` (see `#GodotStateChartBuilder.md`).
    
    Batch-modify existing scenes: Use TscnEditor (`.kiro/scripts/ui_builder/tscn_editor_tools/`).
    NEVER use AI for single-property tweaks - user edits directly in Godot.
  </scene_management>

  <development_workflow>
    C# build: Auto-triggered by hook on .cs file save.
    Logs: Check Godot Output tab or `$env:APPDATA\Godot\app_userdata\ProjectName\logs\godot.log`
  </development_workflow>

  <testing>
    Capture detailed game state: 
    `python .kiro/scripts/testing/detailed_game_state.py`
    
    Run comprehensive tests: 
    `python .kiro/scripts/testing/comprehensive_test.py`
  </testing>

  <mcp_tools>
    Project tools: `get_godot_version`, `list_projects`, `get_project_info`, `launch_editor`, `run_project`, `stop_project`, `get_debug_output`
    Scene tools: `create_scene`, `add_node`, `save_scene`, `load_sprite`
    Advanced tools: `export_mesh_library` (requires MeshInstance3D), `get_uid`, `update_project_uids`
  </mcp_tools>
</instructions>