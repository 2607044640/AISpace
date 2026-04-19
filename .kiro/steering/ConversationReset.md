---
inclusion: manual
---
<conversation_reset_rules>
  <layer_1_quick_start>
    <quick_reference>
      - Tool: `mcp_sequential_thinking_sequentialthinking`
      - Confidence Threshold: 7/10 before resetting
      - Core Rule: Capture ALL critical information before clearing
    </quick_reference>
    
    <decision_tree>
      - IF Confidence Score < 7 OR blind spots exist:
        - ACTION: Read more context, check Scratchpad files, verify critical decisions captured. (Why: Prevents losing important project state.)
      - IF important information found but unsure how to summarize:
        - ACTION: Ask user for clarification before resetting. (Why: User may have context AI doesn't.)
      - IF Confidence Score >= 7 AND all information captured:
        - ACTION: Proceed with reset. (Why: High confidence threshold met with validated state capture.)
    </decision_tree>
    
    <top_anti_patterns>
      <rule>
        <description>NEVER reset without reading ALL target files and Scratchpad directory.</description>
        <rationale>Critical information may be scattered across multiple files and temporary notes.</rationale>
      </rule>
      <rule>
        <description>NEVER assume current conversation contains all important context.</description>
        <rationale>Previous sessions may have made decisions or discoveries not visible in current context.</rationale>
      </rule>
      <rule>
        <description>NEVER discard Scratchpad analysis files without reviewing them.</description>
        <rationale>Scratchpad may contain important architectural insights or bug investigation notes.</rationale>
      </rule>
    </top_anti_patterns>
  </layer_1_quick_start>

  <layer_2_detailed_guide>
    <api_reference>
      - Tool: `mcp_sequential_thinking_sequentialthinking`
      - Purpose: Enforces mandatory state capture validation before reset.
    </api_reference>

    <target_files>
      Read these files to understand the state upon starting a fresh session. Update these exact files when resetting:
      1. `KiroWorkingSpace/.kiro/docLastConversationState.md`
      2. `KiroWorkingSpace/.kiro/ProjectRules.md`
    </target_files>

    <implementation_guide>
      <step>Execute `mcp_sequential_thinking_sequentialthinking` to establish context.</step>
      <step>Build Knowledge Inventory:
        - What tasks were completed in recent sessions?
        - What is the current project phase?
        - What are the pending tasks or blockers?
        - What architectural decisions were made?
        - What bugs or issues are known?
      </step>
      <step>Identify Blind Spots:
        - Are there unrecorded decisions or workarounds?
        - Are there Scratchpad files with important analysis?
        - Are there performance issues or technical debt?
        - Are there user requests not yet implemented?
        - Are there temporary solutions that need documentation?
      </step>
      <step>Read ALL target files:
        - `docLastConversationState.md` - Current project state
        - `ProjectRules.md` - Project-specific rules and architecture
      </step>
      <step>Read Scratchpad directory:
        - Check for CodeAnalysis_*.md files
        - Check for PluginSearch_*.md files
        - Check for ComponentDesign_*.md files
        - Check for any other analysis or investigation notes
      </step>
      <step>Assign Confidence Score (1-10). If < 7, fill blind spots by:
        - Reading more context files
        - Checking recent conversation history
        - Verifying all critical decisions are captured
        - Asking user for clarification if needed
      </step>
      <step>Validate state capture:
        - All completed tasks documented?
        - All pending tasks listed?
        - All architectural decisions recorded?
        - All known issues documented?
        - All important Scratchpad insights preserved?
      </step>
      <step>Clear and rewrite target files:
        - Clear existing contents completely
        - Rewrite with up-to-date, concise summaries
        - Preserve all critical information
        - Remove outdated or irrelevant details
      </step>
    </implementation_guide>

    <core_rules>
      <rule>
        <description>ALWAYS execute `mcp_sequential_thinking_sequentialthinking` before resetting.</description>
        <rationale>Ensures structured analysis and prevents losing critical project state.</rationale>
      </rule>
      <rule>
        <description>ALWAYS verify Confidence Score >= 7 before clearing files.</description>
        <rationale>Ensures sufficient understanding of project state and all critical information captured.</rationale>
      </rule>
      <rule>
        <description>ALWAYS read Scratchpad directory before resetting.</description>
        <rationale>Scratchpad may contain important analysis or investigation notes not yet integrated into main documentation.</rationale>
      </rule>
      <rule>
        <description>ALWAYS preserve architectural decisions and key lessons learned.</description>
        <rationale>These are the most valuable information for future sessions and hardest to reconstruct.</rationale>
      </rule>
      <rule>
        <description>ALWAYS maintain concise but complete summaries.</description>
        <rationale>Balance between context window efficiency and information preservation.</rationale>
      </rule>
    </core_rules>

    <knowledge_inventory_checklist>
      <category name="Project State">
        - [ ] Current project phase identified?
        - [ ] Recent completed tasks documented?
        - [ ] Pending tasks and blockers listed?
        - [ ] Known bugs or issues recorded?
      </category>
      <category name="Architecture">
        - [ ] Key architectural decisions captured?
        - [ ] Design patterns in use documented?
        - [ ] Component structure understood?
        - [ ] Integration points identified?
      </category>
      <category name="Technical Debt">
        - [ ] Temporary workarounds documented?
        - [ ] Performance issues noted?
        - [ ] Refactoring needs identified?
        - [ ] Technical debt tracked?
      </category>
      <category name="Scratchpad Content">
        - [ ] CodeAnalysis files reviewed?
        - [ ] PluginSearch files reviewed?
        - [ ] ComponentDesign files reviewed?
        - [ ] Investigation notes reviewed?
      </category>
    </knowledge_inventory_checklist>

    <blind_spots_checklist>
      <question>Are there unrecorded architectural decisions?</question>
      <action>Review recent conversation for design choices and rationale</action>
      
      <question>Are there Scratchpad files with important insights?</question>
      <action>List and read all files in .kiro/Scratchpad/</action>
      
      <question>Are there temporary solutions that need documentation?</question>
      <action>Check for workarounds or "TODO" comments in recent discussions</action>
      
      <question>Are there user requests not yet implemented?</question>
      <action>Review conversation for feature requests or enhancement ideas</action>
      
      <question>Are there performance issues or technical debt?</question>
      <action>Check for optimization discussions or known limitations</action>
    </blind_spots_checklist>
  </layer_2_detailed_guide>

  <layer_3_advanced>
    <escalation_triggers>
      <trigger>
        <condition>Important information found but unsure how to summarize</condition>
        <action>Ask user for clarification or priority guidance</action>
        <rationale>User may have context or priorities AI doesn't understand</rationale>
      </trigger>
      <trigger>
        <condition>Scratchpad contains extensive analysis not yet integrated</condition>
        <action>Notify user and ask if analysis should be preserved separately</action>
        <rationale>Extensive analysis may be valuable for future reference</rationale>
      </trigger>
      <trigger>
        <condition>Multiple conflicting architectural approaches discussed</condition>
        <action>Ask user which approach was ultimately chosen</action>
        <rationale>Prevents documenting abandoned approaches as current state</rationale>
      </trigger>
    </escalation_triggers>

    <best_practices>
      - **Preserve Decisions Over Details:** Focus on "what was decided and why" rather than implementation minutiae.
      - **Document Lessons Learned:** Capture key insights that would be expensive to rediscover.
      - **Maintain Continuity:** Ensure next session can pick up exactly where this one left off.
      - **Scratchpad Integration:** Review Scratchpad files and integrate important insights into main documentation.
      - **Concise Summaries:** Balance completeness with brevity - aim for essential information only.
    </best_practices>

    <example_workflow>
      <scenario>Conversation context approaching limit, need to reset</scenario>
      <execution>
        <step>1. Execute mcp_sequential_thinking_sequentialthinking</step>
        <step>2. Knowledge Inventory:
          - Recent tasks: Implemented GridShapeVisualComponent, fixed NullReferenceException
          - Current phase: Core architecture complete, testing phase
          - Pending: Rotation testing, synergy system implementation
          - Architecture: Entity-Component with Mediator, R3 reactive streams
        </step>
        <step>3. Blind Spots Identified:
          - Are there Scratchpad analysis files?
          - Were there any temporary workarounds?
          - Are there performance concerns?
        </step>
        <step>4. Read target files:
          - docLastConversationState.md - Contains detailed project history
          - ProjectRules.md - Contains architecture rules
        </step>
        <step>5. Read Scratchpad:
          - Found: CodeAnalysis_20260418_AABBProblem.md
          - Found: ComponentDesign_20260418_ShapeBlocks.md
          - Found: ValidationFramework_Summary.md
        </step>
        <step>6. Confidence Score: 8/10 (sufficient to proceed)</step>
        <step>7. Clear and rewrite:
          - docLastConversationState.md: Update with latest completed tasks, preserve architectural decisions
          - ProjectRules.md: Update with any new rules or patterns discovered
          - Integrate key Scratchpad insights into main documentation
        </step>
      </execution>
    </example_workflow>
  </layer_3_advanced>
</conversation_reset_rules>