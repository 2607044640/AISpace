# 静态分析常用命令速查表

## 基础命令

### 1. 分析整个解决方案
```bash
cd 3d-practice
dotnet build
```

### 2. 分析单个项目
```bash
cd 3d-practice
dotnet build 3dPractice.csproj
```

### 3. 分析时显示详细信息
```bash
dotnet build /v:detailed
```

### 4. 只运行分析器（不编译）
```bash
dotnet build /p:RunAnalyzersDuringBuild=true /p:RunAnalyzers=true /t:Rebuild
```

---

## 高级命令

### 5. 将警告视为错误（CI/CD 模式）
```bash
dotnet build /p:TreatWarningsAsErrors=true
```

### 6. 只显示特定严重级别的问题
```bash
# 只显示错误
dotnet build /p:WarningLevel=0

# 显示错误和警告
dotnet build /p:WarningLevel=4
```

### 7. 生成分析报告到文件
```bash
dotnet build > analysis_report.txt 2>&1
```

### 8. 只分析特定文件（通过 MSBuild 过滤）
```bash
# 注意：dotnet build 不支持直接指定单个 .cs 文件
# 但可以通过 Roslynator CLI 实现：
dotnet roslynator analyze --include "**/*CharacterAnimationConfig.cs"
```

---

## Roslynator 专用命令

### 9. 自动修复所有可修复的问题
```bash
dotnet roslynator fix
```

### 10. 只修复特定严重级别
```bash
dotnet roslynator fix --severity warning
```

### 11. 只修复特定规则
```bash
dotnet roslynator fix --diagnostic-id CA1050
```

### 12. 预览修复（不实际修改文件）
```bash
dotnet roslynator fix --dry-run
```

### 13. 分析特定文件夹
```bash
dotnet roslynator analyze --include "addons/A1TetrisBackpack/**/*.cs"
```

---

## 过滤和搜索

### 14. 只显示特定规则的警告
```bash
dotnet build 2>&1 | Select-String -Pattern "CA1050"
```

### 15. 统计警告数量
```bash
dotnet build 2>&1 | Select-String -Pattern "warning" | Measure-Object
```

### 16. 按文件分组显示警告
```bash
dotnet build 2>&1 | Select-String -Pattern "\.cs\(\d+,\d+\): warning" | Group-Object { $_ -replace '\.cs\(.*', '.cs' }
```

### 17. 只显示前 N 个警告
```bash
dotnet build 2>&1 | Select-String -Pattern "warning" | Select-Object -First 20
```

---

## IDE 集成

### Visual Studio
- **实时分析：** 自动启用，错误列表窗口显示
- **快速修复：** `Ctrl + .` 或点击灯泡图标
- **批量修复：** 右键项目 → Analyze and Code Cleanup

### VS Code
- **安装扩展：** C# (ms-dotnettools.csharp)
- **查看问题：** `Ctrl + Shift + M` 打开 Problems 面板
- **快速修复：** `Ctrl + .`

### Rider
- **实时分析：** 自动启用
- **查看问题：** Alt + 6 打开 Problems 工具窗口
- **快速修复：** `Alt + Enter`
- **批量修复：** Code → Code Cleanup

---

## CI/CD 集成示例

### GitHub Actions
```yaml
- name: Run Static Analysis
  run: |
    cd 3d-practice
    dotnet build /p:TreatWarningsAsErrors=true
```

### GitLab CI
```yaml
static-analysis:
  script:
    - cd 3d-practice
    - dotnet build /p:TreatWarningsAsErrors=true
```

---

## 性能优化

### 18. 禁用特定分析器（加速编译）
在 `.csproj` 中添加：
```xml
<PropertyGroup>
  <!-- 禁用 StyleCop -->
  <NoWarn>$(NoWarn);SA1633;SA1600</NoWarn>
</PropertyGroup>
```

### 19. 只在 Release 模式运行分析
在 `Directory.Build.props` 中：
```xml
<PropertyGroup Condition="'$(Configuration)' == 'Release'">
  <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
</PropertyGroup>
```

---

## 常见问题排查

### 问题：分析器没有运行
```bash
# 检查分析器是否已安装
dotnet list package | Select-String -Pattern "Analyzer"

# 强制重新加载分析器
dotnet clean
dotnet restore
dotnet build
```

### 问题：规则没有生效
```bash
# 验证 .editorconfig 语法
dotnet format --verify-no-changes --verbosity diagnostic

# 检查 Directory.Build.props 是否被加载
dotnet build /v:diagnostic | Select-String -Pattern "Directory.Build.props"
```

### 问题：警告太多，无法阅读
```bash
# 按严重级别过滤
dotnet build 2>&1 | Select-String -Pattern "error CS|error CA"

# 或者临时降低警告级别
dotnet build /p:AnalysisLevel=5
```

---

## 推荐工作流

### 日常开发
```bash
# 1. 编码前：检查当前状态
dotnet build | Select-String -Pattern "warning" | Measure-Object

# 2. 编码中：IDE 实时反馈（无需手动命令）

# 3. 提交前：全量检查
dotnet build /p:TreatWarningsAsErrors=true

# 4. 自动修复简单问题
dotnet roslynator fix --severity info
```

### 代码审查
```bash
# 生成完整报告
dotnet build > code_review_$(Get-Date -Format "yyyyMMdd_HHmmss").txt 2>&1

# 统计各类问题数量
dotnet build 2>&1 | Select-String -Pattern "warning (CA|SA|S|RCS)" | Group-Object { $_ -replace '.*warning ([A-Z]+\d+).*', '$1' } | Sort-Object Count -Descending
```

---

**提示：** 所有命令都假设你在 `3d-practice/` 目录下执行。如果在其他目录，需要调整路径。
