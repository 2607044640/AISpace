---
trigger: always_on
---

<!-- SINGLE SOURCE OF TRUTH — Edit this file. All IDEs read it via hardlink. -->

## 1. Quick Start & Workflow
- **Build**: `dotnet build` (Dir: `TetrisBackpack/`)
- **Logs**: `$env:APPDATA/Godot/app_userdata/Tesseract_Backpack/logs/godot.log`
- **Context**: `C:\Users\26070\My Drive\Agent_Godot_Brain\AI_Context_Changes.md`
- **Master Sync**: `AISpace\SyncMasterCopy\AI_Context_Master_Latest.txt` (full AI-ready bundle of useful project files, rules, and recent changes)
- **Paths**: Code=`TetrisBackpack/`, Rules/Arch=`AISpace/` (Single source: `AGENTS.md`)
- **Steering**: `BugInvestigation.md` (Escalation), `_RulesSystem.md` (Infrastructure)

<workflow>
1. Verify assumptions from `ConversationReset.md`, `docLastConversationState.md`, `AGENTS.md`.
2. Execute incrementally.
3. IMPORTANT: `dotnet build` from `TetrisBackpack/` immediately after ANY `.cs` edit.
</workflow>

## 2. API & Workspace
- **Docs MCP**: `context7` (Lookup `R3`, `NuGet`)
- **MCPs**: `mcp_godot_launch_editor`, `run_project`, `get_debug_output`, `create_scene`, `add_node`, `save_scene`, `load_sprite`, `export_mesh_library`, `get_uid`, `update_project_uids`
- **Temp Files**: `AISpace\temp\` (analysis), `TetrisBackpack\temp\` (test scripts). Strictly disposable. NEVER scatter `test_*` or `*.bak` in main dirs.

## 3. Operations & Error Handling
- **Scene**: Edit `.tscn` directly.
- **Docs**: Delete generic programming docs. Keep Godot/Project-specific logic.

<system_reminder>
- CRITICAL SYNC: Renaming `[Export]` or `%NodePath` in C# MUST trigger immediate `.tscn` sync. (Why: NullReferenceException)
- NO BLIND FIXES: F6 -> fetch `godot.log` via MCP. Analyze before changing code.
- 3-STRIKE ESCALATION: 3 failed fixes = HALT. Consult `BugInvestigation.md`.
- RUN SCENE: ALWAYS specify the exact scene (e.g., `A1TesseractBackpack/TSBackpack.tscn`) when using `mcp_godot_run_project`. DO NOT blindly run the default scene.
</system_reminder>

## 4. Architecture & R3 Strictness

<prime_directive>
  <description>CRITICAL: Clean Architecture, Cross-Project Generality & Pragmatic KISS</description>
  <rationale>Core systems (like Object Pools) must be designed as pristine, decoupled, and generic frameworks ready for drop-in reuse in future projects. However, this generality must NOT infect simple, domain-specific logic. Do not over-engineer what should be a simple script.</rationale>
  <rules>
    1. CORE FRAMEWORK GENERALITY: Global systems, managers, and architectural foundations MUST use generic (`T`), type-safe, and highly decoupled code to ensure 100% cross-project reusability. Keep the core perfectly clean.
    2. PRAGMATIC SIMPLICITY (KISS): For everyday game logic and simple requirements, the most effective and direct code is the best. Do not invent abstractions or premature generalizations (like unnecessary `[Export]` vars) unless specifically commanded.
    3. COMPONENT STRICTNESS: Composition > Inheritance. Components do EXACTLY ONE thing. Entities are just mediators.
    4. NAMING ENFORCEMENT: Injected component variables MUST match their Type names (e.g., `NodePath_InitPoint`).
    5. EXACT BLUEPRINT OBEDIENCE: Execute bug fixes and hotfixes EXACTLY as diagnosed. Do not silently refactor or "generalize" unrelated code during a fix.
  </rules>
</prime_directive>

<complex_pattern>
  <description>CRITICAL: Godot Lifecycle & R3 Initialization</description>
  <rationale>Godot executes _EnterTree Top-Down but _Ready Bottom-Up. Previously this caused strict initialization orders, but metaprogramming solves this via Lazy Initialization.</rationale>
  <rules>
    1. R3 EVENTS: Use `[R3Event]` instead of manual `Subject<T>`. It lazy-initializes on first access, making it safe and ensuring correct initialization order for children to subscribe during their `_Ready()`.
    2. CORE DATA: Instantiate `ReactiveProperty<T>` or simple collections inline (e.g., `= new()`) rather than inside lifecycle methods.
    3. TIMING: Use `await ToSignal(GetTree(), SceneTree.SignalName.ProcessFrame);` instead of `CallDeferred`.
  </rules>
</complex_pattern>

<object_pool>
  <description>CRITICAL: High-Frequency Object Management</description>
  <rationale>For fast-spawning/destroying entities (e.g., Bullets, Damage UI, Effects), avoid runtime instantiation overhead to prevent GC spikes and FPS drops.</rationale>
  <rules>
    1. USE THE POOL: Always refer to `AISpace\rules_global\Godot\GodotA1ObjectPoolUsage.md` when designing object pools.
  </rules>
</object_pool>

### Component & R3 Cheat Sheet
- **Structure**: Entities = Mediators (NO logic). NO sibling cross-referencing.
- **Events**: NEVER use Godot Signals (`[Signal]`). ALWAYS use `[R3Event] private partial void OnEventName(...)` to auto-generate Observables.
- **Memory**: `CompositeDisposable _disposables` -> Dispose in `_ExitTree()`.
- **Perf**: `ValueTuples (a, b)` in `EveryUpdate` to prevent GC.
- **Streams**:
  - Physics (Velocity): `Observable.EveryPhysicsUpdate()`
  - UI Updates: Append `.ObserveOn(GodotProvider.MainThread)`
  - Button Clicks: `.ThrottleFirst(TimeSpan)` (NEVER `.Throttle()`)
  - Continuous I/O (Sliders): `.Debounce(TimeSpan)`
  - State Flags: Use `ReactiveProperty<T>`
  - Discard Payload: Chain `.AsUnitObservable()`

## 5. Metaprogramming (Source Generators)

### A1GodotMetaProgramming (`using A1GodotMetaProgramming;`)
> Folder layout: `R3Events/` · `Lifecycle/` · `NodeBinding/`

- **[R3Event]**: Usage: `[R3Event] private partial void OnMyEvent(string msg);`
  - **Auto-Generates**:
    1. A trigger method (`OnMyEvent(msg)`) that internally calls `OnNext`.
    2. A public `Observable<T> OnMyEventObservable { get; }`.
    3. Internal `Subject<T>` with lazy-initialization and automatic `_ExitTree` disposal.
  - **Type Variations**:
    - **0 Args**: Generates `Observable<Unit>`.
    - **1 Arg**: Generates `Observable<T>`.
    - **2+ Args**: Generates Tuple `Observable<(T1 name1, T2 name2)>`.

- **[GenerateCompositeDisposable]**: Add to class. Auto-generates `_disposables` field + `TreeExiting` auto-dispose hook.
  - Usage: `[GenerateCompositeDisposable] public partial class MyComp : Node { ... }`
  - Replaces: manual `private readonly CompositeDisposable _disposables = new();` + `_ExitTree()` dispose.

- **[GodotNode]**: Add to a `private` field. Auto-generates `[Export] NodePath` + `GetNodeOrNull` binding method.
  - Usage: `[GodotNode] private GridShapeComponent _gridShapeComp;`
  - Auto-Generates:
    1. `[Export] public NodePath _gridShapeComp_Path { get; set; } = "%GridShapeComponent";`
    2. `private void _InitNodeGridShapeComponent()` — calls `GetNodeOrNull` + `GD.PushError` on null.
  - Override default path: `[GodotNode("../OtherPath")] private GridShapeComponent _gridShapeComp;`
  - Call generated init in `_Ready()`: `_InitNodeGridShapeComponent();`

### Godot.Composition (Architecture)
- **Entities**: Add `[Entity]` to root. Call `InitializeEntity()` in `_Ready()`.
- **Components**: Add `[Component(typeof(Parent))]` to children. Call `InitializeComponent()` in `_Ready()`.
- **Dependencies**: Request via `[ComponentDependency(typeof(T))]`. Access via auto-generated `parent` and `camelCase` properties.
- **Lifecycle**: Override `OnEntityReady()` for R3 subscriptions. Append `.AddTo(_disposables)`.

## 6. Coding Standards

### Naming
- **Strict Node-to-Variable Matching (Anti-Alias Rule)**: 
  Variables that reference Nodes MUST contain the exact Node name string.
  1. **No Synonyms or Abbreviations**: If a node is named `InitPoint`, the variable MUST contain `InitPoint`. Changing it to `spawnPlace` or `init` is STRICTLY FORBIDDEN.
  2. **Format (`TypeName_NodeName`)**: Variables must follow the type prefix format. Example: `[Export] NodePath NodePath_InitPoint;` or `Control control_InitPoint;`.
  3. **Domain Explicit Names**: Node names must be unambiguous. Use `InsideBackpackItems` instead of a generic `ItemsContainer`.
- **Private Variables**: `_camelCase` for internal state.

### Component & Node Access
- **Nodes Lookup**: Use `%Name` -> `GetNodeOrNull<T>("%Name")` + `GD.PushError`.

### Documentation Rules
- **FORBIDDEN (NO BOILERPLATE)**: 
  1. **STRICTLY FORBIDDEN**: XML comments (`/// <summary>`), class/method headers, or any "Summary" blocks.
  2. **STRICTLY FORBIDDEN**: Redundant comments for standard Godot lifecycle methods (`_Ready`, `_Process`, etc.).
  3. **STRICTLY FORBIDDEN**: Any AI-style preamble or file-level "This script handles..." summaries.
- **MANDATORY**: Inline `//` comments (in Chinese) explaining WHY for custom Rx streams, math formulas, and complex logic. NO "how" or "what" comments unless logic is extremely non-obvious.
