---
inclusion: manual
---

<context>
Meta-rules for creating, formatting, summarizing, and storing AI instruction files and project documentation.
</context>

<instructions>

<critical_constraints>
- **Zero Hallucination:** NEVER fabricate APIs, classes, methods, UIDs, or file paths not explicitly in the source material.
- **Technical Fidelity:** NEVER alter code blocks, function signatures, or parameter lists when condensing text.
- **Preserve Guardrails:** ALWAYS retain explicit boundary conditions (e.g., "Use ONLY on root-level").
- **Compression:** Achieve brevity via strict Markdown and removing conversational filler. NEVER discard technical specifications.
- **No Examples:** NEVER use "good vs bad" examples or `<example>` tags. Describe constraints using pure, concise, imperative text.
</critical_constraints>

<file_management>
- Store ALL rules, steering files, and instructions exclusively in `KiroWorkingSpace/.kiro/`.
- NEVER store rule files in individual project folders.
</file_management>

<writing_style>
- Place the most critical information at the top.
- Write in the imperative mood ("Validate input").
- State explicitly what to do; keep sentences extremely short and concise.
- Use prohibitions ONLY to block dangerous APIs or pinpoint concrete bad practices.
</writing_style>

<formatting>
- Structure content using consistent, descriptive XML tags.
- Nest tags logically for hierarchical data (`<outer><inner></inner></outer>`).
- Reference tags directly in text.
</formatting>

<anti_noise_checklist>
Delete ruthlessly before saving:
- Generic AI advice, textbook principles, and common sense.
- Contradictions and duplicated information.
- Role-playing fluff.
- Vague directives.
- Over-engineering.
</anti_noise_checklist>

</instructions>