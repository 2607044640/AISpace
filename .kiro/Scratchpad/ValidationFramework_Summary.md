# Unified Validation Framework

**Created:** 2026-04-19  
**Purpose:** Document the complete "Knowledge Inventory + Blind Spots + Confidence Score" validation framework applied across all high-risk operations.

---

## Core Concept

**Problem:** AI can hallucinate or make assumptions when information is missing, leading to:
- Incorrect implementations based on assumed architecture
- Breaking existing systems by not understanding dependencies
- Proposing solutions that don't fit the actual codebase structure
- Optimizing wrong bottlenecks without profiling data

**Solution:** Mandatory validation protocol before high-risk operations:
1. Execute `mcp_sequential_thinking_sequentialthinking`
2. Build **Knowledge Inventory** (explicit known facts)
3. Identify **Blind Spots** (missing/uncertain information)
4. Assign **Confidence Score** (1-10)
5. If Confidence < Threshold: Fill blind spots before proceeding
6. If Confidence >= Threshold: Execute with validation

---

## Protocols Implemented

### 1. BugInvestigation.md ✅ (ALREADY EXISTED)
- **Confidence Threshold:** 7/10
- **Knowledge Inventory:** Error logs, stack traces, reproduction steps
- **Blind Spots:** Root cause location, timing issues, dependency state
- **Escalation:** Three-Strike Rule (3 failed attempts → escalate)
- **Location:** `KiroWorkingSpace/.kiro/steering/StableOrOther/BugInvestigation.md`

### 2. FeatureImplementation.md ✅ (NEWLY CREATED)
- **Confidence Threshold:** 7/10
- **Knowledge Inventory:** Existing systems, patterns, dependencies, communication mechanisms
- **Blind Spots:** Duplicate systems? Integration points? Save/load impact? UI patterns?
- **Escalation:** If existing system provides 80%+ of functionality → extend instead of create
- **Location:** `KiroWorkingSpace/.kiro/steering/StableOrOther/FeatureImplementation.md`

### 3. PerformanceOptimization.md ✅ (NEWLY CREATED)
- **Confidence Threshold:** 8/10 (higher due to risk)
- **Knowledge Inventory:** Profiling data, FPS metrics, bottleneck location, frame time breakdown
- **Blind Spots:** CPU vs GPU? Memory leaks? GC spikes? Specific bottleneck location?
- **Escalation:** No profiling data available OR optimization breaks tests
- **Location:** `KiroWorkingSpace/.kiro/steering/StableOrOther/PerformanceOptimization.md`

### 4. CsArchitect.md ✅ (ENHANCED)
- **Confidence Threshold:** 7/10
- **Knowledge Inventory:** Existing patterns, installed packages, communication architecture
- **Blind Spots:** Threading model? Event systems? Data persistence? Similar functionality?
- **Confidence Calculation:** 
  - Understanding of existing architecture (3 points)
  - Verification of plugin compatibility (2 points)
  - Validation against existing patterns (2 points)
  - Comparison with registry entries (2 points)
  - Architectural impact assessment (1 point)
- **Location:** `KiroWorkingSpace/.kiro/steering/CsArchitect.md`

### 5. ConversationReset.md ✅ (ENHANCED)
- **Confidence Threshold:** 7/10
- **Knowledge Inventory:** Completed tasks, current phase, pending tasks, architectural decisions, known bugs
- **Blind Spots:** Unrecorded decisions? Scratchpad analysis? Temporary workarounds? Technical debt?
- **Escalation:** Important info but unsure how to summarize → ask user
- **Location:** `KiroWorkingSpace/.kiro/steering/ConversationReset.md`

---

## Common Structure (All Protocols)

```xml
<layer_1_quick_start>
  <quick_reference>
    - Tool: mcp_sequential_thinking_sequentialthinking
    - Confidence Threshold: [X]/10
    - Escalation Trigger: [Condition]
  </quick_reference>
  
  <decision_tree>
    - IF Confidence < [X]: ACTION + WHY
    - IF Blind Spot detected: ACTION + WHY
    - IF [Failure Condition]: ESCALATE + WHY
  </decision_tree>
  
  <top_anti_patterns>
    - NEVER [action] (Why: [consequence])
  </top_anti_patterns>
</layer_1_quick_start>

<layer_2_detailed_guide>
  <implementation_guide>
    <step>Execute mcp_sequential_thinking_sequentialthinking</step>
    <step>Build Knowledge Inventory (known facts)</step>
    <step>Identify Blind Spots (missing information)</step>
    <step>Assign Confidence Score (1-10)</step>
    <step>IF Confidence < threshold: Fill blind spots</step>
    <step>Execute with validation</step>
  </implementation_guide>
  
  <knowledge_inventory_checklist>
    [Domain-specific known facts to verify]
  </knowledge_inventory_checklist>
  
  <blind_spots_checklist>
    [Domain-specific missing information to identify]
  </blind_spots_checklist>
</layer_2_detailed_guide>

<layer_3_advanced>
  <escalation_triggers>
    [Conditions that require user intervention]
  </escalation_triggers>
</layer_3_advanced>
```

---

## When to Apply Each Protocol

| Scenario | Protocol | Trigger Keywords |
|----------|----------|------------------|
| Bug reports, crashes, errors | BugInvestigation.md | "bug", "error", "crash", "not working", "exception" |
| New features, systems, mechanics | FeatureImplementation.md | "add", "create", "implement", "new feature", "system" |
| Performance issues, lag, optimization | PerformanceOptimization.md | "slow", "lag", "optimize", "performance", "FPS" |
| Architecture review, refactoring, plugins | CsArchitect.md | "refactor", "architecture", "plugin", "library", "pattern" |
| Context reset, state preservation | ConversationReset.md | "reset", "context limit", "save state", "new session" |

---

## Integration with Existing Rules

### MainRules.md
- Workflow: Calls sequential thinking on EVERY request
- Compilation: `dotnet build` after C# changes
- State Tracking: `.kiro/Scratchpad/` for internal state

### DesignPatterns.md
- Architecture: Entity-Component with Mediator pattern
- Reactive: R3 + R3.Godot patterns
- Anti-patterns: Hardcoded GetNode, direct sibling access

### Validation Framework (NEW)
- Pre-execution: Knowledge Inventory + Blind Spots + Confidence Score
- Threshold: 7-8/10 before high-risk operations
- Escalation: Clear triggers for user intervention

---

## Success Metrics

**Before Framework:**
- ❌ Blind guessing at bug causes
- ❌ Creating duplicate systems
- ❌ Optimizing wrong bottlenecks
- ❌ Recommending incompatible plugins

**After Framework:**
- ✅ Structured analysis before action
- ✅ Explicit identification of missing information
- ✅ Confidence-based decision making
- ✅ Clear escalation paths

---

## Example: Bug Investigation Success

**Scenario:** GridShapeVisualComponent NullReferenceException

**Execution:**
1. ✅ Sequential thinking (Thoughts 1-7)
2. ✅ Knowledge Inventory: _Ready() order, R3 Subject initialization
3. ✅ Blind Spots: Actual code implementation, initialization order
4. ✅ Confidence Score: 4/10 → too low, read files first
5. ✅ Fill blind spots: Read component files, add debug logging
6. ✅ Root cause identified: OnShapeChangedAsObservable not initialized
7. ✅ Fix applied: Initialize Subject in _Ready()
8. ✅ Verification: dotnet build passed

**Result:** Bug fixed in 2 iterations with clear reasoning at each step.

---

## Future Enhancements

**Potential Additional Protocols:**
- CrossSystemIntegration.md (can be merged into FeatureImplementation.md)
- DatabaseMigration.md (if database work becomes common)
- SecurityAudit.md (for security-sensitive changes)

**Confidence Score Refinement:**
- Track historical accuracy of confidence scores
- Adjust thresholds based on success rates
- Add domain-specific scoring criteria

---

## Key Takeaway

**The framework prevents the "AI doesn't know what it doesn't know" problem by:**
1. Forcing explicit enumeration of known facts
2. Forcing explicit identification of missing information
3. Requiring confidence threshold before high-risk operations
4. Providing clear escalation paths when confidence is insufficient

This creates a **unified validation framework** that ensures AI operates with verified knowledge rather than assumptions.
