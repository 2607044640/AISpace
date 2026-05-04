---
trigger: manual
---

## Quick Reference
- **Core Rule**: 3-Strike Rule (Max 3 failed fix attempts before escalation)

## Decision Tree
- IF Confidence < 7 OR blind spots: ALWAYS trigger web/doc search. (Why: NEVER guess missing facts)
- IF Confidence >= 7 AND search complete: Proceed with execution.
- IF 3 consecutive fails for same issue: Check `AISpace/hardbugs/` directory for historical solutions. If no solution is found, HALT and escalate. (Why: Prevents infinite loops while leveraging past fixes)
- IF deadlocks, timing issues, Godot/OS bugs: Check `hardbugs/`, then HALT and escalate.

## Implementation Workflow
1. Pinpoint blind spots and assign Confidence Score (1-10).
2. Trigger search if Confidence < 7.
3. Read error logs completely; add targeted debug logging.
4. Apply EXACTLY ONE change per iteration and verify compilation.

## Best Practices
- Implement and verify functionality incrementally.

</template>
