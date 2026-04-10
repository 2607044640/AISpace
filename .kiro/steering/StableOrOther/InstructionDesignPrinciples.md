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
- **Smart Compression:** Achieve brevity by removing conversational filler and redundant adjectives. NEVER discard technical specifications, rationales (the "why"), or reference tables.
- **Preserve Examples (CRITICAL):** ALWAYS retain "Correct vs Incorrect" code comparisons, anti-patterns, and step-by-step usage guides. Wrap them neatly in `<example>` tags. Code is not noise.
- **Preserve Tables:** ALWAYS retain lookup tables (e.g., Size Flags, UIDs). Format them cleanly using standard Markdown tables.
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
- Briefly explain *why* a constraint exists if the source material provides the rationale.
</writing_style>

<formatting>
- Structure content using consistent, descriptive XML tags.
- Nest tags logically for hierarchical data (`<outer><inner></inner></outer>`).
- Use `<rule>`, `<rationale>`, and `<example>` structures to keep constraints tightly coupled with their context and code.
- Reference tags directly in text.
</formatting>

<anti_noise_checklist>
Delete ruthlessly before saving:
- Generic AI advice, textbook principles, and common sense.
- Contradictions and duplicated information.
- Role-playing fluff (e.g., "Here is the optimized file").
- Vague directives.
- Over-engineering.
*WARNING: Do NOT mistakenly delete exact code paths, UIDs, or technical explanations under the guise of "noise".*
</anti_noise_checklist>

</instructions>