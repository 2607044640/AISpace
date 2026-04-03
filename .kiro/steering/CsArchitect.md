---
inclusion: manual
---

<context>
Godot C# (.NET) architecture analysis, pain-point detection, and library recommendation protocol. Trigger this rule whenever code structure evaluation, refactoring, or tool assessment is requested.
</context>

<instructions>
<analysis_protocol>
Execute the following steps sequentially when analyzing a codebase:
1. **Diagnose:** Scan provided C# code for tight coupling, SOLID violations, redundant boilerplate, and implicit technical debt.
2. **Deduplicate:** Identify custom implementations of standard patterns (e.g., reinvented state machines, hardcoded signal strings, messy async polling) that should be replaced by established .NET/Godot libraries.
3. **Prescribe:** Recommend 1-2 robust, actively maintained NuGet packages or Godot C# plugins that directly solve the identified issues. 
4. **Demonstrate:** Output C# code blocks showing the refactored implementation integrating the recommended library.
</analysis_protocol>

<library_selection_criteria>
- **Weight:** Prioritize lightweight, single-purpose libraries over monolithic frameworks.
- **Maintenance:** Recommend only actively maintained repositories.
- **C# Native:** Ensure recommendations leverage native .NET features (e.g., `async/await`, delegates, generics, Source Generators) rather than relying on Godot's legacy string-based APIs.
</library_selection_criteria>

<plugin_discovery_protocol>
Execute when recommending C# libraries or Godot plugins:
1. **Web Research First:** Search extensively for C# Godot plugins and NuGet packages matching the pain point using web search tools.
2. **Cross-Reference Record:** Check `#PluginRecord.md` as supplementary data, NOT as primary source.
3. **Apply Filters:** Verify all candidates meet: GitHub Stars > 100 AND last update within 1 year (exception: feature-complete libraries).
4. **Recommend Best:** Output 1-3 verified tools with GitHub links, star counts, last update dates, and why they're superior.
5. **Never Guess:** If no verified tool exists after thorough search, state "No vetted solution found" instead of fabricating recommendations.
</plugin_discovery_protocol>
</instructions>

<critical_constraints>
- **Zero Hallucination:** NEVER fabricate NuGet packages, GitHub repositories, class names, or API methods. Suggest only real, verifiable tools.
- **100% Technical Fidelity:** Include necessary `using` directives and exact type casting in refactored C# code blocks.
- **Format-Driven Compression:** Present detected issues and library comparisons using strict Markdown tables or concise lists. Do not use conversational filler.
</critical_constraints>

<examples>
<example>
<description>Refactoring Godot string-based connections to native C# events.</description>
<bad>
GetNode("Player").Connect("health_changed", this, "UpdateUI");
</bad>
<good>
// Diagnosis: String-based signal connection is fragile and prone to runtime errors.
// Prescription: Use strongly-typed C# events/signals.
GetNode<Player>("Player").HealthChanged += UpdateUI;
</good>
</example>

<example>
<description>Handling complex state logic.</description>
<bad>
// Massive switch-case statements inside _Process(double delta) handling Enum states.
</bad>
<good>
// Diagnosis: State management is highly coupled and violates Open-Closed Principle.
// Prescription: Use 'Stateless' (NuGet) for robust state machine configuration.
var machine = new StateMachine<State, Trigger>(State.Idle);
machine.Configure(State.Idle).Permit(Trigger.Move, State.Moving);
</good>
</example>
</examples>