---
inclusion: always
---
<instructions>
  <initialization>
    Read `#KiroWorkingSpace/.kiro/steering/ConversationReset.md` for protocol.
    Read project's `docLastConversationState.md` and `ProjectRules.md` to restore context.
  </initialization>

  <execution_protocol>
    Call `mcp_sequential_thinking_sequentialthinking` on EVERY request (multiple times if user explicitly asks to "think").
     
    Execute actions immediately: read files, run commands, make changes.
    Implement incrementally and verify each step.
    
    Never blindly accept assumptions. Apply critical thinking throughout: Verify assumptions before implementing. Check existing code. Question initial solutions. If analysis shows a significantly better approach, briefly explain why and PROPOSE it, but DO NOT pivot away from my explicitly requested architecture/method unless I approve.
  </execution_protocol>

  <workspace_management>
    Use `.kiro/Scratchpad/` exclusively for your internal state tracking, complex task checklists, and cross-session bug logs.
    DO NOT summarize, narrate, or explain these file updates to the user unless explicitly asked.
    Save permanent docs, steering files, and specs outside the Scratchpad.
    
    Project structure:
    - Architecture rules, scripts, and steering files: `KiroWorkingSpace/.kiro/`
    - Godot project code: `3d-practice/`
  </workspace_management>

  <development_workflow>
    <mandatory_compilation>
      ALWAYS compile after writing ANY C# code.
      ALWAYS compile when verification is needed during development.
      NEVER skip compilation checks - catch errors immediately.
      
      Command: `dotnet build` (run in 3d-practice directory)
      Note: dotnet build auto-detects .sln file in current directory.
    </mandatory_compilation>
    
    Logs: Check Godot Output tab or `$env:APPDATA/Godot/app_userdata/Tesseract_Backpack/logs/godot.log`
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
  </documentation_standards>

  <mcp_tools>
    Project tools: `mcp_godot_get_godot_version`, `mcp_godot_list_projects`, `mcp_godot_get_project_info`, `mcp_godot_launch_editor`, `mcp_godot_run_project`, `mcp_godot_stop_project`, `mcp_godot_get_debug_output`
    Scene tools: `mcp_godot_create_scene`, `mcp_godot_add_node`, `mcp_godot_save_scene`, `mcp_godot_load_sprite`
    Advanced tools: `mcp_godot_export_mesh_library` (requires MeshInstance3D), `mcp_godot_get_uid`, `mcp_godot_update_project_uids`
  </mcp_tools>
</instructions>