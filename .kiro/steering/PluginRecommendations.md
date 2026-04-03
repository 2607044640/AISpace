---
inclusion: manual
---

<context>
Recommended plugins and libraries for Godot C# projects. NOT currently used in this project. Use as reference AFTER conducting fresh web research.
</context>

<instructions>
<critical_rules>
- This registry contains plugins NOT currently used in the project
- Recommend ONLY plugins meeting: GitHub Stars > 100 AND last update within 1 year
- Exception: "Feature-complete" plugins (pure math libraries, isolated editor tools) may bypass the 1-year rule
- Filter recommendations by user's actual pain point. Never suggest 2D tools for 3D projects or BaaS for offline games
- This record is NOT exhaustive. Always conduct fresh web research for latest/better alternatives
</critical_rules>

<filtering_protocol>
- Conduct extensive web search for plugins matching user's pain point.
- Cross-reference findings with this record as supplementary data.
- Verify all candidates meet quality thresholds (stars, activity, maintenance).
- Output: Plugin name + GitHub link + stars + last update + solved pain point.
</filtering_protocol>
</instructions>

<plugin_registry>

### Level Design & World Building

| Plugin | Core Features | Solves |
| :--- | :--- | :--- |
| **Terrain3D** | High-performance 3D terrain with LOD, brush editing for Godot 4. | Large outdoor terrains with multi-material blending. Native Godot lacks efficient terrain system. |
| **cyclopsLevelBuilder** | In-engine CSG level builder for rapid prototyping. | Greyboxing without switching to Blender. Fast iteration on level geometry. |
| **func_godot** | Quake MAP/VMF importer with auto-generated brush geometry and collision. | Retro FPS workflow using TrenchBroom or similar BSP editors. |
| **Godot Asset Placer** | 3D asset placement with grid snapping, ground alignment, random transforms. | Manual placement of trees/props is tedious. Need batch/brush-based scene decoration. |

### Architecture & Core Systems

| Plugin | Core Features | Solves |
| :--- | :--- | :--- |
| **Arch ECS** | High-performance C# ECS with archetype-based storage, optional multithreading. NuGet: `Arch`. 2.8k+ stars. | Massive entity counts (1000+ bullets, particles, enemies). 10x faster than traditional OOP. Use for bullet hell, RTS, large-scale simulations. NOT for UI, player controllers, or small entity counts. |
| **Friflo.Engine.ECS** | High-performance C# ECS with zero-allocation, cache-friendly design. | OOP performance bottlenecks with massive entity counts (RTS, bullet hell, survivor-likes). |
| **Nodot** | Pre-built node library for rapid prototyping across multiple genres. | Need quick gameplay loop assembly without writing boilerplate from scratch. |
| **CommunityToolkit.Mvvm** | Microsoft's official MVVM library. NuGet: `CommunityToolkit.Mvvm`. 3.6k+ stars. Source generators for `ObservableProperty`, `RelayCommand`. Platform-agnostic. | Boilerplate MVVM code (INotifyPropertyChanged, commands). Alternative to R3 for traditional MVVM pattern. Use for WPF/Avalonia-style data binding. NOT needed if using R3 reactive approach. |

### 2D Pipeline & Animation

| Plugin | Core Features | Solves |
| :--- | :--- | :--- |
| **godot-4-importality** | Auto-import Aseprite files and spritesheets with live sync. | Pixel art iteration requires constant manual export/configuration. |

### Game Feel & VFX

| Plugin | Core Features | Solves |
| :--- | :--- | :--- |
| **Shaker** (various implementations) | Modular camera shake and hit-stop effects. | Native camera shake code is rigid and hard to tune. Need rich impact feedback. |

### Backend & Online Services

| Plugin | Core Features | Solves |
| :--- | :--- | :--- |
| **Talo Godot** | Open-source backend for analytics, leaderboards, events. | Lightweight online features without heavy BaaS lock-in. |

### Physics & Platform Integration

| Plugin | Core Features | Solves |
| :--- | :--- | :--- |
| **Godot Jolt** | Jolt physics engine replacement for native 3D physics. | Native 3D physics has poor performance, tunneling, ragdoll instability with complex scenes. |
| **GodotSteam** | Steamworks API bindings for achievements, cloud saves, P2P. | Steam integration for PC releases. **WARNING: Main repo archived Aug 2025. Verify active fork before use.** |

### Systems Management & Input

| Plugin | Core Features | Solves |
| :--- | :--- | :--- |
| **Scene Manager** (glass-brick) | Async scene loading with transition animations. | Manual scene loading causes stutters and lacks smooth transitions. |
| **Input Helper** (nathanhoad) | Auto-detect input device, dynamic button prompts. | Cross-platform controller UI (keyboard/Xbox/PS) requires manual device tracking. |

### Audio Pipeline

| Plugin | Core Features | Solves |
| :--- | :--- | :--- |
| **Sound Manager** (nathanhoad) | Global audio pool, music crossfade, priority scheduling. | Node destruction cuts audio abruptly. No global volume/priority management. |

### Editor Workflow & Data

| Plugin | Core Features | Solves |
| :--- | :--- | :--- |
| **CSV Data Importer** (timothyqiu) | Import CSV/TSV as typed Godot resources. | Game config tables (item stats, dialogue) need efficient parsing into engine-native data. |

</plugin_registry>
