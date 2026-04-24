---
trigger: manual
---

<layer_1_quick_start>
  <quick_reference>
    - **Run Analysis:** `dotnet build` (from `3d-practice/`)
    - **Auto-Fix:** `dotnet roslynator fix --severity warning`
    - **Strict Mode:** `dotnet build /p:TreatWarningsAsErrors=true`
    - **Installed Analyzers:** Roslynator 4.12.11, StyleCop 1.2.0-beta.556, SonarAnalyzer 10.6.0
  </quick_reference>

  <decision_tree>
    - Before commit: Run `dotnet build /p:TreatWarningsAsErrors=true` (Why: catches all issues)
    - After C# file edit: Run `dotnet build` (Why: MainRules.md mandates immediate verification)
    - Too many warnings: Run `dotnet roslynator fix` first, then review remaining issues
    - Single file check: Open in IDE for real-time feedback (Why: dotnet build is project-level only)
    - CI/CD pipeline: Use `/p:TreatWarningsAsErrors=true` to fail builds on warnings
  </decision_tree>

  <top_anti_patterns>
    - **Ignoring CA1050:** Types in global namespace pollute scope and cause collisions
    - **Using `#pragma warning disable`:** Masks real issues. Fix root cause or suppress in .editorconfig
    - **Skipping build after changes:** Violates MainRules.md verification requirement
    - **Committing with warnings:** Technical debt accumulates. Fix or explicitly suppress
  </top_anti_patterns>
</layer_1_quick_start>

<layer_2_detailed_guide>
  <api_reference>
    | Command | Purpose | Key Parameters |
    |---------|---------|----------------|
    | `dotnet build` | Run all analyzers | `/p:TreatWarningsAsErrors=true`, `/v:detailed` |
    | `dotnet roslynator fix` | Auto-fix issues | `--severity [error\|warning\|info]`, `--diagnostic-id CA1050` |
    | `dotnet roslynator analyze` | Analyze only | `--include "**/*.cs"` |
    | `dotnet clean` | Reset build cache | Use before `dotnet build` if analyzers not running |
  </api_reference>

  <configuration_files>
    <file name=".editorconfig" location="3d-practice/">
      <purpose>Define naming conventions and rule severities</purpose>
      <critical_sections>
        - **Naming Rules:** `dotnet_naming_rule.*` enforces TypeName_Purpose pattern (ERROR level)
        - **Diagnostic Severity:** `dotnet_diagnostic.CA1050.severity = warning`
        - **Code Style:** `csharp_style_var_when_type_is_apparent = true`
      </critical_sections>
      <syntax>
        ```ini
        # Custom naming: TypeName_Purpose
        dotnet_naming_rule.private_fields_typename_purpose.severity = error
        dotnet_naming_rule.private_fields_typename_purpose.symbols = private_fields
        dotnet_naming_rule.private_fields_typename_purpose.style = typename_purpose_style
        
        dotnet_naming_symbols.private_fields.applicable_kinds = field
        dotnet_naming_symbols.private_fields.applicable_accessibilities = private
        
        dotnet_naming_style.typename_purpose_style.capitalization = pascal_case
        dotnet_naming_style.typename_purpose_style.word_separator = _
        ```
      </syntax>
    </file>

    <file name="Directory.Build.props" location="3d-practice/">
      <purpose>Global analyzer enforcement across all projects</purpose>
      <critical_properties>
        - `EnforceCodeStyleInBuild=true`: Run analyzers during build
        - `EnableNETAnalyzers=true`: Enable Microsoft analyzers
        - `AnalysisLevel=latest`: Use newest rule set
        - `TreatWarningsAsErrors`: Set per configuration
      </critical_properties>
      <mechanism>MSBuild auto-loads this file before compiling any .csproj</mechanism>
    </file>

    <file name="stylecop.json" location="3d-practice/">
      <purpose>StyleCop-specific configuration</purpose>
      <critical_settings>
        - `documentExposedElements=true`: Public APIs require XML docs
        - `documentPrivateElements=false`: Skip private member docs
        - `usingDirectivesPlacement=outsideNamespace`: System usings first
      </critical_settings>
      <reference>Linked via `<AdditionalFiles>` in Directory.Build.props</reference>
    </file>
  </configuration_files>

  <core_rules>
    <rule>
      <description>ALWAYS run `dotnet build` immediately after ANY C# code modification</description>
      <rationale>MainRules.md mandates compilation verification. Catches errors before commit.</rationale>
    </rule>
    <rule>
      <description>NEVER use `#pragma warning disable` without explicit justification comment</description>
      <rationale>Masks technical debt. Prefer .editorconfig suppression for legitimate framework constraints.</rationale>
    </rule>
    <rule>
      <description>ALWAYS fix CA1050 violations (types not in namespaces) immediately</description>
      <rationale>Global namespace pollution causes naming collisions and violates C# standards.</rationale>
      <example>
        // BEFORE (CA1050 violation)
        public class ItemDataResource : Resource { }
        
        // AFTER
        namespace A1TetrisBackpack.Items
        {
            public class ItemDataResource : Resource { }
        }
      </example>
    </rule>
    <rule>
      <description>ALWAYS convert public fields to properties with [Export] for Godot classes</description>
      <rationale>CA1051 violation. Fields break encapsulation. Properties support validation.</rationale>
      <example>
        // BEFORE (CA1051 violation)
        [Export] public string CharacterName = "Default";
        
        // AFTER
        [Export] public string CharacterName { get; set; } = "Default";
      </example>
    </rule>
    <rule>
      <description>Suppress CA1051 globally for Godot [Export] fields if property conversion breaks serialization</description>
      <rationale>Godot 4.x may require fields for certain export types (Animation, Resource). Framework constraint.</rationale>
      <configuration>
        ```ini
        # In .editorconfig
        dotnet_diagnostic.CA1051.severity = none
        ```
      </configuration>
    </rule>
    <rule>
      <description>Use `dotnet roslynator fix` for bulk cleanup, then manually review changes</description>
      <rationale>Auto-fix may alter semantics. Always verify with `dotnet build` and test run.</rationale>
    </rule>
  </core_rules>

  <critical_rule_ids>
    | Rule ID | Description | Severity | Action |
    |---------|-------------|----------|--------|
    | CA1050 | Types must be in namespaces | ERROR | Wrap in namespace matching folder structure |
    | CA1051 | No public instance fields | WARNING | Convert to property or suppress for Godot [Export] |
    | CA1819 | Properties should not return arrays | WARNING | Use IReadOnlyList&lt;T&gt; or convert to method |
    | CA1062 | Validate public method arguments | WARNING | Add null checks with ArgumentNullException |
    | SA1208 | System usings before others | WARNING | Reorder using directives |
    | SA1633 | File header required | NONE | Disabled (not required for this project) |
    | S3776 | Cognitive complexity too high | WARNING | Refactor method into smaller functions |
    | RCS1163 | Unused parameter | WARNING | Remove or prefix with underscore |
  </critical_rule_ids>
</layer_2_detailed_guide>

<layer_3_advanced>
  <troubleshooting>
    <error symptom="Analyzers not running, no warnings shown">
      <cause>Build cache stale or NuGet packages not restored</cause>
      <fix>
        ```bash
        dotnet clean
        dotnet restore
        dotnet build
        ```
      </fix>
    </error>
    <error symptom=".editorconfig rules not enforced">
      <cause>Syntax error in .editorconfig or rule severity set to 'none'</cause>
      <fix>
        ```bash
        # Validate syntax
        dotnet format --verify-no-changes --verbosity diagnostic
        
        # Check if file is loaded
        dotnet build /v:diagnostic | Select-String -Pattern ".editorconfig"
        ```
      </fix>
    </error>
    <error symptom="Too many warnings, build output unreadable">
      <cause>Initial scan on legacy codebase</cause>
      <fix>
        ```bash
        # Filter by severity
        dotnet build 2>&1 | Select-String -Pattern "error CA|error CS"
        
        # Or suppress low-priority rules temporarily
        # In .editorconfig:
        dotnet_diagnostic.SA1600.severity = none  # Disable doc comments
        ```
      </fix>
    </error>
    <error symptom="CA1051 warnings on Godot [Export] fields">
      <cause>Analyzer doesn't recognize Godot framework pattern</cause>
      <fix>Already suppressed in .editorconfig. If reappears, verify `dotnet_diagnostic.CA1051.severity = none`</fix>
    </error>
  </troubleshooting>

  <best_practices>
    - **Pre-commit Hook:** Add `dotnet build /p:TreatWarningsAsErrors=true` to git pre-commit hook
    - **IDE Integration:** Use Ctrl+. (VS Code), Alt+Enter (Rider) for quick fixes instead of manual edits
    - **Incremental Cleanup:** Fix 10-20 warnings per session. Avoid massive refactors that break functionality
    - **Rule Customization:** Adjust severity in .editorconfig, not via `#pragma`. Centralized control prevents drift
    - **CI/CD Enforcement:** Fail builds on warnings in Release configuration only. Allow warnings in Debug for rapid iteration
  </best_practices>

  <ci_cd_integration>
    <github_actions>
      ```yaml
      - name: Static Analysis
        run: |
          cd 3d-practice
          dotnet build /p:TreatWarningsAsErrors=true
      ```
    </github_actions>
    <gitlab_ci>
      ```yaml
      static-analysis:
        script:
          - cd 3d-practice
          - dotnet build /p:TreatWarningsAsErrors=true
      ```
    </gitlab_ci>
  </ci_cd_integration>
</layer_3_advanced>
