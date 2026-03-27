---
inclusion: manual
---

<context>
Meta-rules for creating, formatting, summarizing, and storing AI instruction files and project documentation.
</context>

<instructions>
<critical_constraints>
- **Zero Hallucination:** NEVER fabricate, guess, or inject APIs, classes, methods, UIDs, or file paths not explicitly present in the source material. If a source example is incomplete, leave it incomplete.
- **100% Technical Fidelity:** NEVER delete or alter code blocks, function signatures, or parameter lists (e.g., `vertical_margin`) when condensing text. 
- **Preserve Guardrails:** Always retain "Wrong vs. Correct" examples and explicit boundary conditions (e.g., "Use ONLY on root-level"). These are core mechanics, not noise.
- **Format-Driven Compression:** Achieve brevity by leveraging strict Markdown (tables, concise lists) and removing conversational filler, NEVER by discarding technical specifications.
</critical_constraints>

<file_management>
- Store ALL rules, steering files, and instructions exclusively in `KiroWorkingSpace/.kiro/`.
- NEVER store rule files in individual project folders.
</file_management>

<writing_style>
- Place the most critical, must-know information at the top.
- Write in the imperative mood ("Validate input", not "Don't forget to validate").
- State explicitly what to do rather than relying on long lists of what not to do.
- Keep sentences short and concise without losing any critical content.
- Use prohibitions ONLY to block dangerous APIs (e.g., "Never use gets()") or pinpoint concrete bad practices.
</writing_style>

<formatting>
- Structure content using consistent, descriptive XML tags.
- Nest tags logically for hierarchical data (`<outer><inner></inner></outer>`).
- Reference tags directly in text (e.g., "Follow the steps in `<instructions>`").
- Ground abstractions with concrete examples using `<example>` tags.
</formatting>

<anti_noise_checklist>
Delete ruthlessly before saving (without violating <critical_constraints>):
- Generic AI advice, textbook principles, and common sense.
- Contradictions and duplicated information across files.
- Excessive role-playing ("You are the world's best...").
- Vague directives ("Handle errors properly").
- Over-engineering (longer is not better).
</anti_noise_checklist>
</instructions>

<examples>
<example>
<description>Transforming vague advice into actionable, imperative instructions.</description>
<bad>Be careful with pointers and remember to handle errors properly.</bad>
<good>Validate pointers before dereferencing: `if (!ptr) return;`. On invalid login, return 401, log the attempt, and increment the fail counter.</good>
</example>
</examples>