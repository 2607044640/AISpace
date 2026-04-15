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

| Plugin | Stars | Last Update | Core Features | Solves |
| :--- | :---: | :---: | :--- | :--- |
| **Terrain3D** | 1.8k+ | 2026-03 | High-performance 3D terrain with LOD, brush editing for Godot 4. | Large outdoor terrains with multi-material blending. Native Godot lacks efficient terrain system. |
| **cyclopsLevelBuilder** | 500+ | 2025-12 | In-engine CSG level builder for rapid prototyping. | Greyboxing without switching to Blender. Fast iteration on level geometry. |
| **func_godot** | 800+ | 2025-11 | Quake MAP/VMF importer with auto-generated brush geometry and collision. | Retro FPS workflow using TrenchBroom or similar BSP editors. |
| **Godot Asset Placer** | 600+ | 2025-10 | 3D asset placement with grid snapping, ground alignment, random transforms. | Manual placement of trees/props is tedious. Need batch/brush-based scene decoration. |

### Architecture & Core Systems

| Plugin | Stars | Last Update | Core Features | Solves |
| :--- | :---: | :---: | :--- | :--- |
| **Arch ECS** | 2.8k+ | 2026-02 | High-performance C# ECS with archetype-based storage, optional multithreading. NuGet: `Arch`. | Massive entity counts (1000+ bullets, particles, enemies). 10x faster than traditional OOP. Use for bullet hell, RTS, large-scale simulations. NOT for UI, player controllers, or small entity counts. |
| **Friflo.Engine.ECS** | 400+ | 2026-01 | High-performance C# ECS with zero-allocation, cache-friendly design. | OOP performance bottlenecks with massive entity counts (RTS, bullet hell, survivor-likes). |
| **Nodot** | 300+ | 2025-12 | Pre-built node library for rapid prototyping across multiple genres. | Need quick gameplay loop assembly without writing boilerplate from scratch. |
| **CommunityToolkit.Mvvm** | 3.6k+ | 2026-03 | Microsoft's official MVVM library. NuGet: `CommunityToolkit.Mvvm`. Source generators for `ObservableProperty`, `RelayCommand`. Platform-agnostic. | Boilerplate MVVM code (INotifyPropertyChanged, commands). Alternative to R3 for traditional MVVM pattern. Use for WPF/Avalonia-style data binding. NOT needed if using R3 reactive approach. |

### 2D Pipeline & Animation

| Plugin | Stars | Last Update | Core Features | Solves |
| :--- | :---: | :---: | :--- | :--- |
| **godot-4-importality** | 200+ | 2025-11 | Auto-import Aseprite files and spritesheets with live sync. | Pixel art iteration requires constant manual export/configuration. |

### Game Feel & VFX

| Plugin | Stars | Last Update | Core Features | Solves |
| :--- | :---: | :---: | :--- | :--- |
| **Shaker** (various implementations) | 150+ | 2025-09 | Modular camera shake and hit-stop effects. | Native camera shake code is rigid and hard to tune. Need rich impact feedback. |

### Backend & Online Services

| Plugin | Stars | Last Update | Core Features | Solves |
| :--- | :---: | :---: | :--- | :--- |
| **Talo Godot** | 250+ | 2026-01 | Open-source backend for analytics, leaderboards, events. | Lightweight online features without heavy BaaS lock-in. |

### Physics & Platform Integration

| Plugin | Stars | Last Update | Core Features | Solves |
| :--- | :---: | :---: | :--- | :--- |
| **Godot Jolt** | 2.1k+ | 2026-03 | Jolt physics engine replacement for native 3D physics. | Native 3D physics has poor performance, tunneling, ragdoll instability with complex scenes. |
| **GodotSteam** | 2.7k+ | 2025-08 | Steamworks API bindings for achievements, cloud saves, P2P. | Steam integration for PC releases. **WARNING: Main repo archived Aug 2025. Verify active fork before use.** |

### Systems Management & Input

| Plugin | Stars | Last Update | Core Features | Solves |
| :--- | :---: | :---: | :--- | :--- |
| **Scene Manager** (glass-brick) | 400+ | 2025-10 | Async scene loading with transition animations. | Manual scene loading causes stutters and lacks smooth transitions. |
| **Input Helper** (nathanhoad) | 500+ | 2025-12 | Auto-detect input device, dynamic button prompts. | Cross-platform controller UI (keyboard/Xbox/PS) requires manual device tracking. |

### Audio Pipeline

| Plugin | Stars | Last Update | Core Features | Solves |
| :--- | :---: | :---: | :--- | :--- |
| **Sound Manager** (nathanhoad) | 350+ | 2025-11 | Global audio pool, music crossfade, priority scheduling. | Node destruction cuts audio abruptly. No global volume/priority management. |

### Editor Workflow & Data

| Plugin | Stars | Last Update | Core Features | Solves |
| :--- | :---: | :---: | :--- | :--- |
| **CSV Data Importer** (timothyqiu) | 180+ | 2025-09 | Import CSV/TSV as typed Godot resources. | Game config tables (item stats, dialogue) need efficient parsing into engine-native data. |

---

**Registry Last Updated:** 2026-04-15

</plugin_registry>
