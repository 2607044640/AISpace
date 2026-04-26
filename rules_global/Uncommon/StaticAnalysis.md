---
trigger: manual
---

## Quick Reference
- **Run Analysis**: `dotnet build` (from `TetrisBackpack/`)
- **Auto-Fix**: `dotnet roslynator fix --severity warning`
- **Strict Mode**: `dotnet build /p:TreatWarningsAsErrors=true`
- **Analyzers**: Roslynator 4.12.11, StyleCop 1.2.0-beta.556, SonarAnalyzer 10.6.0

## Decision Tree
- **Before commit**: Run `dotnet build /p:TreatWarningsAsErrors=true`. (Why: Catches all issues.)
- **After C# file edit**: Run `dotnet build`. (Why: Verifies compilation immediately.)
- **Too many warnings**: Run `dotnet roslynator fix` first, then review remaining issues.
- **Single file check**: Open in IDE for real-time feedback. (Why: `dotnet build` is project-level.)

## Configuration Files
1. **`.editorconfig`**: Defines naming conventions (`TypeName_Purpose`) and rule severities (`dotnet_diagnostic.CA1050.severity = warning`).
2. **`Directory.Build.props`**: Enforces analyzers globally (`EnforceCodeStyleInBuild=true`, `EnableNETAnalyzers=true`).
3. **`stylecop.json`**: StyleCop rules (`documentExposedElements=true`).

## Best Practices
- **Pre-commit Hook**: Add `dotnet build /p:TreatWarningsAsErrors=true` to git pre-commit hook.
- **Incremental Cleanup**: Fix 10-20 warnings per session. Avoid massive refactors.
- **Rule Customization**: Adjust severity in `.editorconfig`, NOT via `#pragma`.

<top_anti_patterns>
  <rule>
    <description>NEVER ignore CA1050 (Types not in namespaces).</description>
    <rationale>Global namespace pollution causes collisions. Always wrap in a namespace matching the folder structure.</rationale>
  </rule>
  <rule>
    <description>NEVER use `#pragma warning disable` without an explicit justification comment.</description>
    <rationale>Masks real issues. Fix the root cause or suppress via `.editorconfig`.</rationale>
  </rule>
</top_anti_patterns>

<complex_pattern>
  <description>Godot `[Export]` Fields vs CA1051</description>
  <rationale>CA1051 warns against public fields. However, Godot sometimes requires them for serialization. We suppress CA1051 globally in `.editorconfig` for `[Export]`, but prefer Properties `[Export] public string Name { get; set; }` where possible.</rationale>
</complex_pattern>

<system_reminder>
If analyzers aren't running, the build cache may be stale. Run `dotnet clean`, `dotnet restore`, and `dotnet build`.
</system_reminder>
