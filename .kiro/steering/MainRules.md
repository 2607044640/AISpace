---
inclusion: always
---

<instructions>
# Godot C# Development Rules

## Session Start
1. Read `#KiroWorkingSpace/ConversationReset.md` for protocol
2. Read project's `docLastConversationState.md` to restore context

## Execution Protocol
- Call `mcp_sequential_thinking_sequentialthinking` on EVERY request
- Take action immediately: read files, run commands, make changes
- Implement incrementally, verify each step(important)

## C# Compilation
After editing `.cs` file:
```cmd
dotnet build "New Game Project Test Godot.sln"
```

## Testing Game State
Test game state capture:
```cmd
python .kiro/scripts/testing/detailed_game_state.py
```

View comprehensive test results:
```cmd
python .kiro/scripts/testing/comprehensive_test.py
```

## Logging

Editor Output: Godot editor → Output tab (not saved)

Runtime logs:
```powershell
Get-Content "$env:APPDATA\Godot\app_userdata\<ProjectName>\logs\godot.log" -Tail 50
```

In code:
```csharp
GD.Print("message");        // Normal
GD.PrintErr("error");       // Red
GD.PushWarning("warning");  // Yellow
```

## Scene Files
- Edit `.tscn`files(text-based scene definitions) directly to add nodes (lights, cameras, collision shapes)
- Changes apply on next editor reload or game run

## TempFolder
Location: `.kiro/TempFolder/`

Use for: Task checklists, analysis notes, bug tracking
Format: `FeatureName_Purpose.md` with `[ ]`/`[x]` checkboxes
Delete when complete.

Never use for: Permanent docs, steering files, specs

## Godot MCP Tools (14 available)

Project: `get_godot_version`, `list_projects`, `get_project_info`, `launch_editor`, `run_project`, `stop_project`, `get_debug_output`

Scene: `create_scene`, `add_node`, `save_scene`, `load_sprite`

Advanced: `export_mesh_library` (需要MeshInstance3D), `get_uid`, `update_project_uids` (Godot 4.4+)

Example:
```javascript
mcp_godot_create_scene({
  projectPath: "C:\\Godot\\project",
  scenePath: "new_scene.tscn",
  rootNodeType: "Node2D"
})
```
</instructions>
