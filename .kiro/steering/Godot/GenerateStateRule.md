---
inclusion: manual
---

<context>
Meta-rule to synthesize the current session's work into a highly compressed, reusable domain-specific rule file for future AI context.
</context>

<instructions>

<critical_constraints>
- Output file path MUST strictly be: C:\Godot\KiroWorkingSpace\.kiro\steering\Godot\
- Target filename format: `<DomainName>_Context.md` (e.g., `SettingUI_Context.md`).
- Ensure zero hallucination of APIs, paths, or UIDs.
- Preserve all explicit boundary conditions and technical specifications.
- Format output using concise, imperative language and nested XML tags.
- Strip all conversational filler, generic advice, and examples.
</critical_constraints>

<workflow>

<step_1_temp_reflection>
Analyze all completed tasks, code modifications, and logic changes in the current session. Draft an exhaustive internal temporary list of these items. Do not limit the quantity during this raw extraction phase.
</step_1_temp_reflection>

<step_2_compliance_and_compression>
Read and apply constraints from `#InstructionDesignPrinciples.md` (or the core principles embedded in this file). 
Apply the anti-noise checklist to the temporary list:
- Delete generic AI advice, textbook principles, and common sense.
- Delete contradictions and duplicated information.
- Delete role-playing fluff and vague directives.
- Compress the remaining technical specifications into strict Markdown and concise imperative sentences.
</step_2_compliance_and_compression>

<step_3_file_generation>
Generate the final rule file. Prepend the file with `--- inclusion: manual ---`. Use the highly compressed data to populate the required XML structure.
</step_3_file_generation>

</workflow>

<output_template>
Structure the generated file using the following tags exclusively:

<context>Brief summary of the domain/system functionality.</context>
<architecture>Core technical structure, class relationships, and critical file paths.</architecture>
<modifications>Precise list of established logic, fixed bugs, or recent architectural decisions.</modifications>
<directives>Imperative rules and boundary conditions for future modifications in this domain.</directives>
</output_template>

</instructions>