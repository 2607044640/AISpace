---
inclusion: manual
---
<feature_implementation_rules>
  <layer_1_quick_start>
    <quick_reference>
      - Tool: `mcp_sequential_thinking_sequentialthinking`
      - Confidence Threshold: 7/10 before implementation
      - Core Rule: Read existing systems BEFORE creating new ones
    </quick_reference>
    
    <decision_tree>
      - IF Confidence Score < 7 OR blind spots exist:
        - ACTION: Read relevant existing code, search for similar systems. (Why: Prevents duplicate implementations and architectural drift.)
      - IF existing system found that provides 80%+ of requested functionality:
        - ACTION: Propose extending existing system instead of creating new one. (Why: Maintains architectural consistency and reduces code duplication.)
      - IF Confidence Score >= 7 AND no conflicts detected:
        - ACTION: Proceed with implementation. (Why: High confidence threshold met with validated approach.)
      - IF implementation breaks existing tests or compilation:
        - ACTION: Halt and re-evaluate approach. (Why: New feature should not break existing functionality.)
    </decision_tree>
    
    <top_anti_patterns>
      <rule>
        <description>NEVER implement a feature without reading existing related systems first.</description>
        <rationale>Creates duplicate systems, violates DRY principle, and causes architectural fragmentation.</rationale>
      </rule>
      <rule>
        <description>NEVER assume communication patterns without verifying existing architecture.</description>
        <rationale>Violates established patterns (e.g., Mediator), creates tight coupling, breaks maintainability.</rationale>
      </rule>
      <rule>
        <description>NEVER add features that require new dependencies without checking existing packages.</description>
        <rationale>Introduces dependency bloat when existing packages may already provide the functionality.</rationale>
      </rule>
    </top_anti_patterns>
  </layer_1_quick_start>

  <layer_2_detailed_guide>
    <api_reference>
      - Tool: `mcp_sequential_thinking_sequentialthinking`
      - Purpose: Enforces mandatory analysis before feature implementation.
    </api_reference>

    <implementation_guide>
      <step>Execute `mcp_sequential_thinking_sequentialthinking` to establish context.</step>
      <step>Build Knowledge Inventory:
        - What existing systems handle similar functionality?
        - What design patterns are used in related features?
        - What communication mechanisms exist (events, signals, reactive streams)?
        - How does save/load system work?
        - What UI patterns are established?
      </step>
      <step>Identify Blind Spots:
        - Are there existing reward/progression systems?
        - How do other features integrate with UI?
        - What's the data persistence pattern?
        - Are there existing event buses or message systems?
        - What threading model is used for async operations?
      </step>
      <step>Assign Confidence Score (1-10). If < 7, fill blind spots by:
        - Reading related component files
        - Searching for similar patterns in codebase
        - Checking existing NuGet packages
        - Reviewing architecture documentation
      </step>
      <step>Validate approach:
        - Does this extend existing systems or create new ones?
        - Does this follow established patterns (Entity/Component, Mediator)?
        - Does this integrate cleanly with existing UI/data layers?
      </step>
      <step>Implement incrementally:
        - Create minimal skeleton first
        - Verify compilation after each component
        - Test integration points immediately
        - Run `dotnet build` after each C# modification
      </step>
    </implementation_guide>

    <technical_specifications>
      - Engine Target: Godot 4.6.1 stable mono
      - Language Target: C#
      - Architecture: Entity-Component with Mediator pattern
      - Reactive Framework: R3 + R3.Godot
    </technical_specifications>

    <core_rules>
      <rule>
        <description>ALWAYS read existing related systems before implementing new features.</description>
        <rationale>Prevents architectural drift, maintains consistency, identifies reusable components.</rationale>
      </rule>
      <rule>
        <description>ALWAYS verify Confidence Score >= 7 before starting implementation.</description>
        <rationale>Ensures sufficient understanding of existing architecture and integration points.</rationale>
      </rule>
      <rule>
        <description>ALWAYS follow established patterns (Entity/Component, Mediator, R3 reactive streams).</description>
        <rationale>Maintains architectural consistency and code maintainability.</rationale>
      </rule>
      <rule>
        <description>ALWAYS use [Export] NodePath with Scene Unique Names (%) for node references.</description>
        <rationale>Prevents hardcoded coupling and enables flexible scene composition.</rationale>
      </rule>
      <rule>
        <description>ALWAYS implement features incrementally with compilation verification at each step.</description>
        <rationale>Catches errors early and maintains working state throughout development.</rationale>
      </rule>
    </core_rules>

    <knowledge_inventory_checklist>
      <category name="Existing Systems">
        - [ ] Similar features already implemented?
        - [ ] Existing data structures that could be reused?
        - [ ] Related components in the same domain?
      </category>
      <category name="Architecture Patterns">
        - [ ] How do similar features communicate (events, signals, reactive)?
        - [ ] What's the established component hierarchy?
        - [ ] Is there a Mediator pattern in use?
      </category>
      <category name="Integration Points">
        - [ ] How does UI update mechanism work?
        - [ ] What's the save/load pattern?
        - [ ] Are there existing event buses or message systems?
      </category>
      <category name="Dependencies">
        - [ ] What NuGet packages are already installed?
        - [ ] Are there existing utilities for this functionality?
        - [ ] What's the threading model for async operations?
      </category>
    </knowledge_inventory_checklist>

    <blind_spots_checklist>
      <question>Do I know if a similar system already exists?</question>
      <action>Search codebase for related class names and functionality</action>
      
      <question>Do I know the established communication patterns?</question>
      <action>Read existing component interactions and event flows</action>
      
      <question>Do I know how this integrates with save/load?</question>
      <action>Check existing persistence implementations</action>
      
      <question>Do I know the UI update mechanism?</question>
      <action>Review existing UI components and reactive bindings</action>
      
      <question>Do I know what dependencies are available?</question>
      <action>Check .csproj file and existing using statements</action>
    </blind_spots_checklist>
  </layer_2_detailed_guide>

  <layer_3_advanced>
    <escalation_triggers>
      <trigger>
        <condition>Existing system found that provides 80%+ of requested functionality</condition>
        <action>Propose extending existing system instead of creating new one</action>
        <rationale>Prevents code duplication and maintains architectural consistency</rationale>
      </trigger>
      <trigger>
        <condition>Implementation requires breaking established patterns</condition>
        <action>Discuss architectural tradeoffs with user before proceeding</action>
        <rationale>Ensures user understands impact of deviating from established architecture</rationale>
      </trigger>
      <trigger>
        <condition>Feature requires new dependencies not aligned with existing stack</condition>
        <action>Propose alternatives using existing packages or discuss necessity</action>
        <rationale>Prevents dependency bloat and maintains stack consistency</rationale>
      </trigger>
    </escalation_triggers>

    <best_practices>
      - **Extend Before Create:** Always check if existing systems can be extended before creating new ones.
      - **Pattern Consistency:** Match the architectural patterns used in similar features.
      - **Incremental Integration:** Integrate with one system at a time (UI, then data, then events).
      - **Validation Points:** Verify compilation and basic functionality after each integration point.
      - **Documentation:** Update relevant documentation when adding new systems or patterns.
    </best_practices>

    <example_workflow>
      <scenario>User requests: "Add a quest system with rewards"</scenario>
      <execution>
        <step>1. Execute mcp_sequential_thinking_sequentialthinking</step>
        <step>2. Knowledge Inventory:
          - Search for existing "reward" or "progression" systems
          - Check how achievements/unlocks are currently handled
          - Review existing UI notification patterns
          - Identify save/load mechanism
        </step>
        <step>3. Blind Spots Identified:
          - Does a reward system already exist?
          - How are game state changes currently tracked?
          - What's the pattern for persistent data?
        </step>
        <step>4. Fill Blind Spots:
          - Read existing progression-related components
          - Check for event systems or message buses
          - Review save/load implementation
        </step>
        <step>5. Confidence Score: 8/10 (sufficient to proceed)</step>
        <step>6. Implementation Decision:
          - Found existing RewardComponent → extend it for quest rewards
          - Found event bus → use it for quest completion notifications
          - Found save system → integrate quest state into existing pattern
        </step>
        <step>7. Incremental Implementation:
          - Create QuestComponent following Entity/Component pattern
          - Integrate with existing RewardComponent
          - Add UI using established reactive binding patterns
          - Integrate with save system
          - Verify compilation after each step
        </step>
      </execution>
    </example_workflow>
  </layer_3_advanced>
</feature_implementation_rules>
