---
trigger: manual
---

<layer_1_quick_start>
  <quick_reference>
    - **Target Path:** `C:\Godot\AISpace\.windsurf\rules\Godot\`
    - **Target Filename:** `Godot<DomainName>_Context.md` (e.g., `GodotInputMap_Context.md`)
    - **Required Front Matter:** `--- inclusion: manual ---`
  </quick_reference>

  <decision_tree>
    - If establishing domain name -> **ALWAYS** use PascalCase. (Why: Enforces consistent naming conventions across the Kiro workspace.)
    - If extracting session data -> **ALWAYS** perform exhaustive raw extraction before filtering. (Why: Prevents accidental loss of critical architectural decisions or bug fixes.)
    - If finalizing data -> **MUST** apply the anti-noise checklist. (Why: Guarantees high-density, easily scannable context for future AI consumption.)
  </decision_tree>

  <minimal_workflow>
    1. Extract an exhaustive internal temporary list of all completed tasks, logic changes, and code modifications from the current session.
    2. Filter the temporary list ruthlessly using the anti-noise checklist (remove fluff, contradictions, and generic advice).
    3. Compress the remaining technical specifications into strict Markdown and concise imperative sentences.
    4. Generate the final file at the designated path using the required YAML header and mandatory XML structure.
  </minimal_workflow>

  <top_anti_patterns>
    - Retaining generic AI advice, textbook principles, or common sense. (Why: Dilutes domain-specific instructions and wastes token context.)
    - Keeping contradictions or duplicated information. (Why: Causes conflicting instructions and AI paralysis in future sessions.)
    - Including role-playing fluff or vague directives. (Why: Destroys the scannability and structural integrity of the rule file.)
  </top_anti_patterns>
</layer_1_quick_start>

<layer_2_detailed_guide>
  <api_reference>
    | Component | Value/Tag | Constraint |
    | :--- | :--- | :--- |
    | **Output Path** | `C:\Godot\AISpace\.windsurf\rules\Godot\` | **MUST** be exact absolute path. |
    | **Filename Format** | `Godot<DomainName>_Context.md` | **MUST** use PascalCase for domain name. |
    | **YAML Header** | `---` `<newline>` `inclusion: manual` `<newline>` `---` | **MUST** be prepended to every generated file. |
    | **Tag: Context** | `<context>` | **MUST** contain a brief summary of the domain/system functionality. |
    | **Tag: Architecture**| `<architecture>` | **MUST** contain core technical structure, class relationships, and critical file paths. |
    | **Tag: Modifications**| `<modifications>` | **MUST** contain a precise list of established logic, fixed bugs, or architectural decisions. |
    | **Tag: Directives** | `<directives>` | **MUST** contain imperative rules and boundary conditions for future modifications. |
  </api_reference>

  <core_rules>
    <rule>
      <description>**NEVER** hallucinate APIs, file paths, or UIDs.</description>
      <rationale>Fabricated data corrupts the AI context repository and guarantees runtime failures in subsequent Godot development sessions.</rationale>
    </rule>
    <rule>
      <description>**ALWAYS** use the precise four output XML tags (`<context>`, `<architecture>`, `<modifications>`, `<directives>`) exclusively.</description>
      <rationale>Maintains a strict, predictable parsing schema for context ingestion across all Kiro domains.</rationale>
    </rule>
    <rule>
      <description>**MUST** format all output using concise, imperative language and nested XML tags.</description>
      <rationale>Ensures maximum instructional density and eliminates parsing ambiguity.</rationale>
    </rule>
  </core_rules>
</layer_2_detailed_guide>

<layer_3_advanced>
  <troubleshooting>
    <error symptom="Generated context file is ignored by Kiro workspace or fails to parse">
      <cause>Missing or malformed YAML front matter, or incorrect directory path.</cause>
      <fix>Verify the file is saved exactly in `C:\Godot\AISpace\.windsurf\rules\Godot\` and the first lines are strictly `--- \n inclusion: manual \n ---`.</fix>
    </error>
    <error symptom="Domain rule file contains excessively long paragraphs and low density">
      <cause>Failure to apply the anti-noise checklist during Step 2 (Compliance and Compression).</cause>
      <fix>Re-process the file text. Delete all textbook principles, generic advice, and role-play fluff. Compress remaining text into imperative bullet points or tables.</fix>
    </error>
  </troubleshooting>

  <best_practices>
    <rule>
      <description>**ALWAYS** separate the raw extraction phase (Step 1) from the compression phase (Step 2).</description>
      <rationale>Attempting to filter while extracting often leads to the accidental omission of nuanced boundary conditions or critical bug-fix rationales.</rationale>
    </rule>
    <rule>
      <description>**MUST** preserve all explicit boundary conditions and technical specifications during the compression phase.</description>
      <rationale>While fluff must be deleted, the exact limitations, allowed parameters, and edge cases are the most vital data for future AI sessions.</rationale>
    </rule>
  </best_practices>
</layer_3_advanced>