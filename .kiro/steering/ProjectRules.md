---
inclusion: always
---

<context>
**Project:** 消消乐+扫雷混合游戏 (Match-3 + Minesweeper hybrid)
**Engine:** Godot 4.6.1 stable mono
**Language:** C# only

**Key Files:**
- Main Scene: `My2DMap.tscn`
- MCP Server: `Scripts/MCP/MCPServer.cs` (port 8765)
- Game State: `Scripts/MCP/GameStateCapture.cs`
- Test Scripts: `.kiro/scripts/testing/`
</context>

<completed_guides>
文档位于 `KiroWorkingSpace/.kiro/steering/OtherInstructions/`：

- **AnimationExport_Guide.md** - 动画自动导出指南
- **GodotInputMap.md** - Input Map配置指南
- **MixamoRetargeter_PluginUpdate.md** - Mixamo插件修复与改进
</completed_guides>

<class_references>
## Animation System
- **AnimationSet.cs** (`Scripts/Animation/`)
  - Resource类，集中管理角色所有动画
  - 包含Idle/Walk/Run/Sprint/Jump等动画
  - `SetupLoopModes()` - 自动设置动画循环模式

- **CharacterAnimationConfig.cs** (`Scripts/Animation/`)
  - Resource类，角色动画配置（类似UE Data Asset）
  - 引用AnimationSet
  - `ApplyToAnimationPlayer()` - 应用配置到AnimationPlayer

## Player
- **Player3D.cs** (`Scripts/`)
  - CharacterBody3D，3D角色控制器
  - Export变量：Speed, RunSpeed, JumpVelocity, AnimationBlendTime
  - Export变量：IdleAnimation, RunAnimation, SprintAnimation, JumpAnimation
  - Export变量：IdleAnimSpeed, RunAnimSpeed, SprintAnimSpeed, JumpAnimSpeed
  - 支持Quick Test模式（直接设置动画）或AnimConfig模式

</class_references>
