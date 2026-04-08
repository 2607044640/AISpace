---
inclusion: always
---
<instructions>
  <initialization>
    Read `#KiroWorkingSpace/ConversationReset.md` for protocol.
    Read project's `docLastConversationState.md` and `ProjectRules.md` to restore context.
  </initialization>

  <execution_protocol>
    <epistemic_validation>
      Call `mcp_sequential_thinking_sequentialthinking` on EVERY request (multiple times if user explicitly asks to "think").
      During sequential thinking, strictly execute these steps before any action:
      1. Knowledge Inventory: List explicit, known facts regarding the request.
      2. Blind Spot Identification: Pinpoint missing, unfamiliar, or uncertain concepts.
      3. Confidence Scoring: Assign a score (1-10).
      4. Search Trigger: If Confidence < 7 OR core concepts are identified as blind spots, NEVER guess. You MUST use web search or documentation lookup tools to retrieve missing facts before proceeding.
      5. Execution: If Confidence >= 7 (or after successful search), proceed with actions.
    </epistemic_validation>
    
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
    <mandatory_compilation>
      ALWAYS compile after writing ANY C# code.
      ALWAYS compile when verification is needed during development.
      NEVER skip compilation checks - catch errors immediately.
      
      Command: `dotnet build` (run in 3d-practice directory)
      Note: dotnet build auto-detects .sln file in current directory.
    </mandatory_compilation>
    
    Logs: Check Godot Output tab or `$env:APPDATA\Godot\app_userdata\ProjectName\logs\godot.log`
  </development_workflow>
  
  <documentation_standards>
    - **Trivial Functions** (e.g., Godot lifecycle hooks like `_ExitTree`, `_PhysicsProcess`, simple getters/setters): Omit documentation entirely. DO NOT waste lines explaining the obvious.
    - **Simple Functions**: Highly flexible. Write a single-sentence `<summary>`, use inline comments inside the function, or write nothing at all if self-evident. DO NOT force the 3-part structure.
    - **Complex/Logic-Heavy Functions**: MUST follow this strict 3-part structure (Order: Purpose -> Example -> Algorithm):
      1. **目的 (Purpose):** State WHAT the function does in the exact context of this project/game.
      2. **示例 (Example):** Provide a concrete scenario (Input -> Output or State Change).
      3. **算法 (Algorithm):** List the logical execution steps that map strictly 1:1 to the code blocks below it.
    
    <anti_noise_constraints>
      - NEVER include textbook math proofs, API tutorials, or general programming concepts.
      - Delete ruthlessly: if an explanation applies to programming in general rather than this specific feature, REMOVE it.
    </anti_noise_constraints>

    <examples>
      <example>
        <description>Complex logic function (Standard abstract 3-part template).</description>
        <good>
        /// <summary>
        /// 功能名称
        /// 目的：解决XX问题，确保XX
        /// 示例：输入 A 得到 B
        /// 算法：1. 获取X -> 2. 计算Y -> 3. 返回Z
        /// </summary>
        </good>
      </example>
      
      <example>
        <description>Simple or trivial functions (Flexible formatting or completely omitted).</description>
        <good>
        // Options: Omit entirely, write a simple inline comment, or use a 1-line summary.
        /// <summary>单句描述即可，或者完全不写。</summary>
        </good>
      </example>
    </examples>
  </documentation_standards>

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