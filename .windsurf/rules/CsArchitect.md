---
trigger: manual
---
```xml
<core_rule>
  <layer_1_quick_start>
    <quick_reference>
      - **Tool:** `mcp_sequential_thinking_sequentialthinking`
      - **Confidence Threshold:** 7/10 before recommending architectural changes.
      - **Trigger Context:** Code structure evaluation, refactoring, or tool assessment for Godot C# (.NET).
      - **Supplementary Data:** Cross-reference `#PluginRecommendations.md` (contains ONLY plugins NOT currently used in project).
      - **Working Memory:** Use `Scratchpad/` for code analysis notes and plugin search records.
    </quick_reference>
    <decision_tree>
      - IF Confidence Score < 7 OR blind spots exist:
        - ACTION: Read more codebase, search for existing patterns, verify plugin compatibility. (Why: Prevents recommending solutions that don't fit actual architecture.)
      - IF Confidence Score >= 7 AND recommendation validated:
        - ACTION: Proceed with recommendation using "What/Helps/Solves" structure. (Why: High confidence threshold met with validated approach.)
      - IF Godot string-based signals are detected:
        - ACTION: ALWAYS refactor to C# strongly-typed events. (Why: Lacks compile-time safety, prone to runtime errors.)
      - IF massive switch-case state logic is detected:
        - ACTION: ALWAYS recommend a dedicated state machine library. (Why: Violates Open-Closed Principle, high coupling.)
      - IF evaluating a plugin/library:
        - ACTION: ALWAYS verify GitHub Stars > 100 AND last update within 1 year. (Why: Ensures active maintenance and community validation.)
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
    <api_reference>
      - **Tool:** `mcp_sequential_thinking_sequentialthinking`
      - **Purpose:** Enforces mandatory structured analysis and establishes context before making architectural recommendations.
    </api_reference>
    <implementation_guide>
      - **Step 1: Execute Sequential Thinking & Build Inventory**
        - Execute `mcp_sequential_thinking_sequentialthinking`.
        - Build Knowledge Inventory: What patterns exist? What libraries are used? What's the communication architecture?
        - Identify Blind Spots: Do I know the threading model, event systems, or data persistence pattern?
        - Assign Confidence Score (1-10). If < 7, fill blind spots before proceeding.
      - **Step 2: Deep Code Analysis & Documentation**
        - Read extensive codebase sections to identify code smells, SOLID violations, and tightly coupled logic.
        - ALWAYS create/update `Scratchpad/CodeAnalysis_[YYYYMMDD].md` with detailed findings.
      - **Step 3: Diagnose & Deduplicate**
        - Scan the C# codebase for implicit technical debt and redundant boilerplate.
        - Identify custom implementations of standard patterns (e.g., reinvented state machines or messy async polling) that should be replaced by established libraries.
      - **Step 4: Web Search & Record**
        - Search extensively via web for C# Godot plugins and NuGet packages matching identified pain points.
        - ALWAYS create/update `Scratchpad/PluginSearch_[YYYYMMDD].md` after EACH search.
        - Record: Plugin name, GitHub link, Stars, Last update (YYYY-MM), Description, Pain point it solves. (Filter: Stars > 100 AND updated within 1 year).
      - **Step 5: Check Local Registry**
        - ALWAYS read `#PluginRecommendations.md` AFTER completing web search.
        - Compare new findings with existing entries to identify better alternatives, overlapping solutions, and gaps.
      - **Step 6: Evaluate Confidence**
        - Assign final Confidence Score based on: Architecture understanding (3), Plugin verification (2), Validation vs patterns (2), Registry comparison (2), Architecture impact (1).
        - Reject candidates that don't meet the >100 Stars/1-year update rule.
      - **Step 7: Explain & Demonstrate**
        - ALWAYS structure each recommendation as: 1. What it does, 2. What it helps, 3. What pain it solves.
        - Show Contextual Code Comparison: Provide a "Before" (current painful approach) and "After" (optimized implementation with necessary `using` directives).
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
        <description>ALWAYS execute `mcp_sequential_thinking_sequentialthinking` before architectural recommendations.</description>
        <rationale>Ensures structured analysis and prevents recommending solutions that don't fit actual architecture.</rationale>
      </rule>
      <rule>
        <description>ALWAYS verify Confidence Score >= 7 before making architectural recommendations.</description>
        <rationale>Prevents recommending plugins or patterns without sufficient understanding of existing architecture.</rationale>
      </rule>
      <rule>
        <description>ALWAYS prioritize native .NET features over Godot's legacy string APIs.</description>
        <rationale>Leveraging `async/await`, delegates, generics, and Source Generators creates idiomatic, performant, and safe C# code.</rationale>
      </rule>
      <rule>
        <description>ALWAYS maintain Scratchpad files (`CodeAnalysis_[DATE].md`, `PluginSearch_[DATE].md`) during investigations.</description>
        <rationale>Preserves architectural insights across sessions, prevents redundant searches, and builds a comprehensive problem map.</rationale>
      </rule>
      <rule>
        <description>ALWAYS consult `#PluginRecommendations.md` AFTER web search and BEFORE making final recommendations.</description>
        <rationale>Leverages existing vetted solutions and prevents recommending inferior alternatives.</rationale>
      </rule>
      <rule>
        <description>ALWAYS explain recommendations using simple language, analogies, and the "What/Helps/Solves" structure.</description>
        <rationale>Makes technical decisions accessible and builds developer understanding, enabling informed decision-making.</rationale>
      </rule>
      <rule>
        <description>ALWAYS include necessary `using` directives and complete code context in Before/After comparisons.</description>
        <rationale>Maintains 100% technical fidelity for direct copy-paste implementation.</rationale>
      </rule>
    </core_rules>
  </layer_2_detailed_guide>

  <layer_3_advanced>
    <best_practices>
      - **Blind Spot Mitigation:** Before acting, continuously evaluate: Do I know the communication patterns? Threading model? Installed NuGet packages? Data persistence patterns?
      - **Library Prescriptions:** When recommending libraries, explicitly state the GitHub Stars, Last Update Date, and architectural rationale to build developer trust.
      - **Modernization:** Actively look to replace any messy async polling with native C# `async/await` patterns tailored for Godot.
      - **Explanation Style:** Use analogies and real-world comparisons. Example: "State machines are like traffic lights - they control which actions can happen based on current state, preventing code from crashing."
      - **Code Comparison Depth:** Show complete before/after context, not just snippets. Include class structure, using directives, and integration points so developers see the full picture.
      - **Pain Point Focus:** Always tie recommendations back to specific pain points. Don't recommend tools just because they're popular - explain exactly what problem they solve in the codebase.
      - **Scratchpad Discipline:** Treat `Scratchpad/` files as living documents. Update them incrementally as you learn more, don't wait until the end of the analysis.
    </best_practices>
  </layer_3_advanced>
</core_rule>
```