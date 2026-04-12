---
inclusion: manual
---
```xml
<kiro_rule>
  <layer_1_quick_start>
    <quick_reference>
      - **Trigger Context:** Code structure evaluation, refactoring, or tool assessment for Godot C# (.NET).
      - **Supplementary Data:** Cross-reference `#PluginRecord.md` (Do NOT use as the primary source).
    </quick_reference>
    <decision_tree>
      - If Godot string-based signals are detected: ALWAYS refactor to C# strongly-typed events. (Why: Lacks compile-time safety, prone to runtime errors).
      - If massive switch-case state logic is detected: ALWAYS recommend a dedicated state machine library. (Why: Violates Open-Closed Principle, high coupling).
      - If evaluating a plugin/library: ALWAYS verify GitHub Stars > 100 AND last update within 1 year. (Why: Ensures active maintenance and community validation).
    </decision_tree>
    <top_anti_patterns>
      <rule>
        <description>NEVER use hardcoded string-based APIs for connections.</description>
        <rationale>String connections fail silently at runtime. Native C# events provide strict compile-time safety.</rationale>
      </rule>
      <rule>
        <description>NEVER implement massive switch-case statements inside `_Process(double delta)` for Enum states.</description>
        <rationale>Creates rigid, tightly coupled architectures that are difficult to scale.</rationale>
      </rule>
      <rule>
        <description>NEVER fabricate NuGet packages, GitHub repositories, class names, or API methods.</description>
        <rationale>Breaks trust and codebase integrity. If no verified tool exists, ALWAYS state: "No vetted solution found".</rationale>
      </rule>
    </top_anti_patterns>
  </layer_1_quick_start>

  <layer_2_detailed_guide>
    <implementation_guide>
      - **Step 1: Diagnose:** Scan the provided C# codebase for tight coupling, SOLID violations, redundant boilerplate, and implicit technical debt.
      - **Step 2: Deduplicate:** Identify custom implementations of standard patterns (e.g., reinvented state machines, messy async polling) that should be replaced by established libraries.
      - **Step 3: Discover:** Search extensively via web for C# Godot plugins and NuGet packages. Cross-reference candidates with `#PluginRecord.md`.
      - **Step 4: Filter:** Reject candidates unless they have >100 GitHub Stars AND an update within the last year (unless deemed feature-complete).
      - **Step 5: Prescribe & Demonstrate:** Recommend 1-3 verified tools (including links, star counts, update dates, and rationale). Output 100% accurate C# code blocks showing the refactored integration.
    </implementation_guide>
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

// INCORRECT: Massive switch-case statements inside _Process handling Enum states
        ]]></code>
      </template>
    </code_templates>
    <core_rules>
      <rule>
        <description>ALWAYS prioritize native .NET features over Godot's legacy string APIs.</description>
        <rationale>Leveraging `async/await`, delegates, generics, and Source Generators creates idiomatic, performant, and safe C# code.</rationale>
      </rule>
      <rule>
        <description>ALWAYS recommend lightweight, single-purpose libraries.</description>
        <rationale>Monolithic frameworks introduce unnecessary complexity and dependency bloat.</rationale>
      </rule>
      <rule>
        <description>ALWAYS format detected issues and library comparisons using strict Markdown tables or concise lists.</description>
        <rationale>Ensures maximum readability and eliminates conversational fluff.</rationale>
      </rule>
      <rule>
        <description>ALWAYS include necessary `using` directives and exact type casting in refactored C# code blocks.</description>
        <rationale>Maintains 100% technical fidelity for direct copy-paste implementation.</rationale>
      </rule>
    </core_rules>
  </layer_2_detailed_guide>

  <layer_3_advanced>
    <best_practices>
      - **Library Prescriptions:** When recommending libraries, explicitly state the GitHub Stars, Last Update Date, and architectural rationale to build developer trust.
      - **Modernization:** Actively look to replace any messy async polling with native C# `async/await` patterns tailored for Godot.
    </best_practices>
  </layer_3_advanced>
</kiro_rule>
```