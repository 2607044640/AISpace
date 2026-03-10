---
inclusion: always
---

# Godot Design Patterns

<context>
Detailed examples and patterns: See `addons/CoreComponents/ARCHITECTURE.md`
</context>

<GodotDesignPatterns>

<CoreArchitecture>
- ENFORCE "Composition over Inheritance". Avoid deep hierarchies.
- Break entities into single-responsibility child Nodes (Components).
- The Root node (e.g., `Player`) acts ONLY as a "Mediator" coordinating its components.
</CoreArchitecture>

<DecouplingRule>
- Call Down, Signal Up: Parents call child methods. Children emit C# `event/Action` upwards.
- Sibling Isolation: Components MUST NOT reference each other directly.
- Injection: Always use `[Export]` instead of hardcoding `GetNode<T>()`.
</DecouplingRule>

<Reusability>
- Add `[GlobalClass]` to core components for cross-project reuse.
- Hardcode ZERO specific content (e.g., animation names). Expose them via `[Export]`.
</Reusability>

<AntiPatterns_NEVER_DO_THIS>
- NEVER write monolithic `_PhysicsProcess` with endless `if-else`. Use FSMs.
- NEVER tightly couple logic (e.g., Movement should emit `OnJumped`, not call AudioPlayer directly).
</AntiPatterns_NEVER_DO_THIS>

</GodotDesignPatterns>

---

<GodotCompositionRules>

## Entity Rules
- Must be `partial class` with `[Entity]` attribute
- Call `InitializeEntity()` in `_Ready()`
- Zero business logic - container only

## Component Rules
- Must be `partial class` with `[Component(typeof(ParentType))]`
- Call `InitializeComponent()` in `_Ready()`
- Use `[ComponentDependency(typeof(OtherComponent))]` for dependencies
- Subscribe events in `OnEntityReady()`, NOT `_Ready()`
- Unsubscribe in `_ExitTree()` to prevent leaks

## Auto-Generated Variables
- `parent` - Access entity (e.g., `parent.Velocity`)
- `componentName` - Access dependencies (lowercase first letter: `InputComponent` → `inputComponent`)

## Communication
- Components emit events: `public event Action<T> OnSomething;`
- Other components subscribe in `OnEntityReady()`
- Never use `GetNode()` for components
- Never call component methods directly across siblings

## Lifecycle
```
Entity._Ready() → InitializeEntity()
  → Component._Ready() → InitializeComponent()
    → Dependencies resolved
      → Component.OnEntityReady() → Subscribe events
```

**Critical:** Dependencies are null in `_Ready()`. Always subscribe in `OnEntityReady()`.

</GodotCompositionRules>
