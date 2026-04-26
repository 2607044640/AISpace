---
trigger: manual
---

## Objective
Recommended plugins and libraries for Godot C# projects. NOT currently used in this project. Use as reference AFTER conducting fresh web research.

## Critical Rules
- Recommend ONLY plugins meeting: GitHub Stars > 100 AND last update within 1 year.
- Exception: "Feature-complete" plugins (pure math, isolated tools) may bypass the 1-year rule.
- Filter recommendations by user's ACTUAL pain point. (e.g., Never suggest BaaS for offline games).
- This list is NOT exhaustive. ALWAYS conduct fresh web search for better alternatives.

## Filtering Protocol
1. Conduct extensive web search for plugins matching user's pain point.
2. Cross-reference findings with this document.
3. Verify all candidates meet quality thresholds.
4. Output: Plugin name + GitHub link + stars + last update + solved pain point.

## Registry (Updated: 2026-04-15)

### Core Systems & Architecture
- **Arch ECS** (2.8k+, 2026-02): High-performance C# ECS. For massive entity counts.
- **Friflo.Engine.ECS** (400+, 2026-01): Zero-allocation C# ECS.
- **CommunityToolkit.Mvvm** (3.6k+, 2026-03): Microsoft's official MVVM library (alternative to R3).

### Level Design
- **Terrain3D** (1.8k+, 2026-03): High-performance 3D terrain with LOD.
- **cyclopsLevelBuilder** (500+, 2025-12): In-engine CSG level builder for rapid greyboxing.
- **func_godot** (800+, 2025-11): Quake MAP/VMF importer.

### Physics & Input
- **Godot Jolt** (2.1k+, 2026-03): Jolt physics engine replacement for native 3D physics.
- **Input Helper** (500+, 2025-12): Auto-detect input device, dynamic button prompts.

### Online & Systems
- **Talo Godot** (250+, 2026-01): Open-source backend for analytics, leaderboards.
- **GodotSteam** (2.7k+, 2025-08): Steamworks API bindings. (WARNING: Main repo archived Aug 2025).
- **Scene Manager** (400+, 2025-10): Async scene loading with transitions.
- **Sound Manager** (350+, 2025-11): Global audio pool and priority scheduling.

<system_reminder>
Never guess plugin names or NuGet packages. If a verified tool does not exist, clearly state so.
</system_reminder>
