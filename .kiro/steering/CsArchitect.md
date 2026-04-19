---
inclusion: manual
---
```xml
<kiro_rule>
  <layer_1_quick_start>
    <quick_reference>
      - **Tool:** `mcp_sequential_thinking_sequentialthinking`
      - **Confidence Threshold:** 7/10 before recommending architectural changes
      - **Trigger Context:** Code structure evaluation, refactoring, or tool assessment for Godot C# (.NET).
      - **Supplementary Data:** Cross-reference `#PluginRecommendations.md` - contains ONLY plugins NOT currently used in project.
      - **Working Memory:** Use `.kiro/Scratchpad/` for code analysis notes and plugin search records.
    </quick_reference>
    <decision_tree>
      - IF Confidence Score < 7 OR blind spots exist:
        - ACTION: Read more codebase, search for existing patterns, verify plugin compatibility. (Why: Prevents recommending solutions that don't fit actual architecture.)
      - IF Confidence Score >= 7 AND recommendation validated:
        - ACTION: Proceed with recommendation using "What/Helps/Solves" structure. (Why: High confidence threshold met with validated approach.)
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
    <api_reference>
      - Tool: `mcp_sequential_thinking_sequentialthinking`
      - Purpose: Enforces mandatory analysis before architectural recommendations.
    </api_reference>

    <implementation_guide>
      - **Step 0: Execute Sequential Thinking:**
        - Execute `mcp_sequential_thinking_sequentialthinking` to establish context.
        - Build Knowledge Inventory: What patterns exist? What libraries are used? What's the communication architecture?
        - Identify Blind Spots: Do I know the threading model? Do I know existing event systems? Do I know the data persistence pattern?
        - Assign Confidence Score (1-10). If < 7, fill blind spots before recommending.
      
      - **Step 1: Deep Analysis & Record:**
        - Read extensive codebase sections to identify optimization opportunities, code smells, and architectural issues.
        - ALWAYS create or update `.kiro/Scratchpad/CodeAnalysis_[YYYYMMDD].md` with detailed findings.
        - Record: Tight coupling locations, SOLID violations, redundant patterns, performance bottlenecks, reinvented wheels.
        - Update this file continuously as you discover more issues during code reading.
        - (Why: Like a detective's notebook - prevents forgetting insights across sessions and builds a comprehensive problem map.)
      
      - **Step 2: Diagnose:**
        - Scan the provided C# codebase for tight coupling, SOLID violations, redundant boilerplate, and implicit technical debt.
        - Prioritize findings from Step 1 analysis file.
      
      - **Step 2: Deduplicate:**
        - Identify custom implementations of standard patterns (e.g., reinvented state machines, messy async polling) that should be replaced by established libraries.
      
      - **Step 3: Web Search & Record:**
        - Search extensively via web for C# Godot plugins and NuGet packages matching identified pain points.
        - ALWAYS create or update `.kiro/Scratchpad/PluginSearch_[YYYYMMDD].md` after EACH search or fetch operation.
        - Record for each candidate: Plugin name, GitHub link, Stars count, Last update date (YYYY-MM), Brief description, Pain point it solves.
        - Filter during recording: Only document if Stars > 100 AND updated within 1 year (unless deemed feature-complete).
        - Update search timestamp in the file: "Last searched: YYYY-MM-DD".
        - (Why: Like a shopping research log - prevents re-searching same things, builds institutional knowledge, tracks evaluation history.)
      
      - **Step 4: Check Local Registry:**
        - ALWAYS read `#PluginRecommendations.md` AFTER completing web search.
        - IMPORTANT: This registry contains ONLY plugins NOT currently used in the project - it's a "wishlist" of vetted alternatives.
        - Compare new findings with existing registry entries.
        - Identify: Better alternatives, overlapping solutions, gaps in current registry, outdated entries.
        - Cross-check: Ensure you're not recommending something inferior to what's already documented.
        - (Why: Like checking your pantry before grocery shopping - avoids duplication, discovers hidden gems already vetted, prevents recommending inferior alternatives.)
      
      - **Step 5: Evaluate Confidence:**
        - Assign Confidence Score (1-10) based on:
          - Understanding of existing architecture (3 points)
          - Verification of plugin compatibility (2 points)
          - Validation against existing patterns (2 points)
          - Comparison with registry entries (2 points)
          - Architectural impact assessment (1 point)
        - If Confidence < 7: Read more code, verify integration points, check threading model.
        - If Confidence >= 7: Proceed to recommendation.
      
      - **Step 6: Filter & Evaluate:**
        - Reject candidates unless they have >100 GitHub Stars AND an update within the last year (unless deemed feature-complete).
        - Prioritize plugins that directly solve user's stated pain point.
        - Avoid recommending 2D tools for 3D projects or online services for offline games.
      
      - **Step 7: Explain & Demonstrate:**
        - Use simple, intuitive language with real-world analogies when explaining concepts.
        - ALWAYS structure each recommendation explanation as:
          1. **What it does:** One-sentence summary of core functionality.
          2. **What it helps:** Concrete benefit (extensibility, maintainability, performance, safety).
          3. **What pain it solves:** Specific problem it eliminates from the codebase.
        - ALWAYS show code comparison with complete context:
          - **Before:** Current painful approach (include full method/class if needed for clarity).
          - **After:** Optimized implementation using recommended library (include necessary `using` directives).
          - **Highlight:** Point out specific improvements - lines reduced, type safety added, extensibility gained, boilerplate eliminated.
        - Recommend 1-3 verified tools with links, star counts, update dates, and architectural rationale.
        - (Why: Like showing before/after renovation photos - makes value immediately obvious and builds confidence in the recommendation.)
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
        <description>ALWAYS create or update `.kiro/Scratchpad/CodeAnalysis_[YYYYMMDD].md` during deep code analysis.</description>
        <rationale>Preserves architectural insights across sessions. Prevents re-discovering same issues. Builds comprehensive problem documentation.</rationale>
      </rule>
      <rule>
        <description>ALWAYS create or update `.kiro/Scratchpad/PluginSearch_[YYYYMMDD].md` after web searches or fetches.</description>
        <rationale>Tracks evaluation history. Prevents redundant searches. Documents why certain plugins were rejected or accepted.</rationale>
      </rule>
      <rule>
        <description>ALWAYS consult `#PluginRecommendations.md` AFTER web search and BEFORE making final recommendations.</description>
        <rationale>Leverages existing vetted solutions. Prevents recommending inferior alternatives. Identifies gaps in current registry.</rationale>
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
      <rule>
        <description>ALWAYS explain recommendations using simple language, analogies, and "What/Helps/Solves" structure.</description>
        <rationale>Makes technical decisions accessible. Builds understanding, not just compliance. Enables informed decision-making.</rationale>
      </rule>
    </core_rules>
  </layer_2_detailed_guide>

  <layer_3_advanced>
    <blind_spots_checklist>
      <question>Do I know the existing communication patterns (events, signals, reactive)?</question>
      <action>Read existing component interactions and event flows</action>
      
      <question>Do I know the threading model for async operations?</question>
      <action>Check for GodotProvider.MainThread usage and async patterns</action>
      
      <question>Do I know what NuGet packages are already installed?</question>
      <action>Read .csproj file and check existing using statements</action>
      
      <question>Do I know if similar functionality already exists?</question>
      <action>Search codebase for related patterns and implementations</action>
      
      <question>Do I know the data persistence pattern?</question>
      <action>Check existing save/load implementations</action>
    </blind_spots_checklist>

    <best_practices>
      - **Library Prescriptions:** When recommending libraries, explicitly state the GitHub Stars, Last Update Date, and architectural rationale to build developer trust.
      - **Modernization:** Actively look to replace any messy async polling with native C# `async/await` patterns tailored for Godot.
      - **Explanation Style:** Use analogies and real-world comparisons. Example: "State machines are like traffic lights - they control which actions can happen based on current state, preventing cars (code) from crashing into each other."
      - **Code Comparison Depth:** Show complete before/after context, not just snippets. Include class structure, using directives, and integration points so developers see the full picture.
      - **Pain Point Focus:** Always tie recommendations back to specific pain points. Don't recommend tools just because they're popular - explain exactly what problem they solve in the user's context.
      - **Scratchpad Discipline:** Treat `.kiro/Scratchpad/` files as living documents. Update them incrementally as you learn more, don't wait until the end of analysis.
    </best_practices>
  </layer_3_advanced>
</kiro_rule>
```