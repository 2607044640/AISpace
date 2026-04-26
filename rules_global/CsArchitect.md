---
trigger: manual
---

## Quick Reference
- **Confidence Threshold**: 7/10 before recommending architectural changes.
- **Trigger Context**: Code structure evaluation, refactoring, or tool assessment for Godot C# (.NET).
- **Supplementary Data**: Cross-reference `#PluginRecommendations.md` (contains ONLY plugins NOT currently used in project).
- **Working Memory**: Use `Scratchpad/` for code analysis notes and plugin search records.

## Decision Tree
- **IF** Confidence Score < 7 OR blind spots exist:
  - **ACTION**: Read codebase, search existing patterns, verify plugin compatibility. (Why: Prevents recommending solutions that don't fit actual architecture.)
- **IF** Confidence Score >= 7 AND recommendation validated:
  - **ACTION**: Proceed with recommendation using "What/Helps/Solves" structure.
- **IF** Godot string-based signals are detected:
  - **ACTION**: ALWAYS refactor to C# strongly-typed events. (Why: Lacks compile-time safety, prone to runtime errors.)
- **IF** massive switch-case state logic is detected:
  - **ACTION**: ALWAYS recommend a dedicated state machine library. (Why: Violates Open-Closed Principle, high coupling.)
- **IF** evaluating a plugin/library:
  - **ACTION**: ALWAYS verify GitHub Stars > 100 AND last update within 1 year. (Why: Ensures active maintenance and community validation.)

## Implementation Workflow
1. **Build Knowledge Inventory**: Note patterns, libraries, communication architecture. Identify blind spots (threading, events, persistence).
2. **Deep Code Analysis**: Create/update `Scratchpad/CodeAnalysis_[YYYYMMDD].md` with code smells, SOLID violations, tightly coupled logic.
3. **Diagnose & Deduplicate**: Scan for tech debt, redundant boilerplate, reinvented patterns (e.g., custom state machines).
4. **Web Search & Record**: Create/update `Scratchpad/PluginSearch_[YYYYMMDD].md`. Record: Name, Link, Stars, Last update, Description, Pain point solved.
5. **Check Local Registry**: ALWAYS read `#PluginRecommendations.md` AFTER web search to find better/overlapping alternatives.
6. **Evaluate Confidence**: Architecture (3), Plugin verification (2), Validation vs patterns (2), Registry comparison (2), Architecture impact (1).
7. **Explain & Demonstrate**: Structure as What it does, What it helps, What pain it solves. Provide "Before" (painful) and "After" (optimized with `using` directives).

## Best Practices
- **Blind Spot Mitigation**: Continuously evaluate understanding of communication, threading, NuGets, persistence.
- **Modernization**: Replace messy async polling with native C# `async/await`.
- **Explanation Style**: Use simple analogies ("State machines are like traffic lights..."). Include complete before/after context, not just snippets.

<system_reminder>
NEVER fabricate NuGet packages, GitHub repositories, class names, or API methods. If no vetted solution exists, ALWAYS state: "No vetted solution found".
</system_reminder>

<top_anti_patterns>
  <rule>
    <description>NEVER use hardcoded string-based APIs for connections.</description>
    <rationale>String connections fail silently at runtime. Native C# events provide strict compile-time safety.</rationale>
  </rule>
  <rule>
    <description>NEVER implement massive switch-case statements inside `_Process` for Enum states.</description>
    <rationale>Creates rigid, tightly coupled architectures that are difficult to scale.</rationale>
  </rule>
</top_anti_patterns>

<code_templates>
  <template name="Godot Native C# Events Migration">
    <code><![CDATA[
// CORRECT: Strongly-typed C# events
GetNode<Player>("Player").HealthChanged += UpdateUI;

// INCORRECT: Fragile string-based connection
// GetNode("Player").Connect("health_changed", this, "UpdateUI");
    ]]></code>
  </template>
  <template name="Robust State Management via 'Stateless' NuGet">
    <code><![CDATA[
// CORRECT: Using Stateless for configuration
using Stateless;

var machine = new StateMachine<State, Trigger>(State.Idle);
machine.Configure(State.Idle)
       .Permit(Trigger.Move, State.Moving);
    ]]></code>
  </template>
</code_templates>