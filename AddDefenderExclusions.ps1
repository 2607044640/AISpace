# ============================================
# Godot C# 编译优化 - Windows Defender 排除脚本
# ============================================
# 用途：解决 Godot 编译卡顿问题（从 30s 降至 5s）
# 执行：以管理员身份运行 PowerShell，然后执行此脚本

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Godot 编译优化 - 添加 Defender 排除项" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# 检查管理员权限
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "[错误] 此脚本需要管理员权限！" -ForegroundColor Red
    Write-Host "请右键点击 PowerShell，选择 '以管理员身份运行'，然后重新执行此脚本。`n" -ForegroundColor Yellow
    pause
    exit
}

Write-Host "[✓] 管理员权限验证通过`n" -ForegroundColor Green

# 定义排除路径
$exclusionPaths = @(
    "C:\Godot\3d-practice",                                      # Godot 项目根目录（包含 bin/obj）
    "$env:USERPROFILE\.nuget\packages",                          # NuGet 全局缓存
    "$env:APPDATA\Godot\app_userdata\Tesseract_Backpack"        # Godot 运行时数据
)

# 定义排除进程
$exclusionProcesses = @(
    "dotnet.exe",           # .NET 编译器
    "MSBuild.exe",          # MSBuild 构建工具
    "Godot_v*.exe"          # Godot 编辑器（通配符匹配所有版本）
)

# 添加路径排除
Write-Host "正在添加路径排除项..." -ForegroundColor Yellow
foreach ($path in $exclusionPaths) {
    try {
        if (Test-Path $path) {
            Add-MpPreference -ExclusionPath $path -ErrorAction Stop
            Write-Host "  [✓] 已添加: $path" -ForegroundColor Green
        } else {
            Write-Host "  [!] 路径不存在，跳过: $path" -ForegroundColor DarkYellow
        }
    } catch {
        Write-Host "  [×] 添加失败: $path" -ForegroundColor Red
        Write-Host "      错误: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# 添加进程排除
Write-Host "`n正在添加进程排除项..." -ForegroundColor Yellow
foreach ($process in $exclusionProcesses) {
    try {
        Add-MpPreference -ExclusionProcess $process -ErrorAction Stop
        Write-Host "  [✓] 已添加: $process" -ForegroundColor Green
    } catch {
        Write-Host "  [×] 添加失败: $process" -ForegroundColor Red
        Write-Host "      错误: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# 验证结果
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "验证当前排除项配置" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$currentPreferences = Get-MpPreference

Write-Host "已排除的路径:" -ForegroundColor Yellow
$currentPreferences.ExclusionPath | Where-Object { $_ -match "Godot|nuget" } | ForEach-Object {
    Write-Host "  - $_" -ForegroundColor Gray
}

Write-Host "`n已排除的进程:" -ForegroundColor Yellow
$currentPreferences.ExclusionProcess | Where-Object { $_ -match "dotnet|MSBuild|Godot" } | ForEach-Object {
    Write-Host "  - $_" -ForegroundColor Gray
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "[完成] 排除项已添加！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`n下一步操作:" -ForegroundColor Yellow
Write-Host "  1. 重启 Godot 编辑器" -ForegroundColor White
Write-Host "  2. 执行 'dotnet build' 测试编译速度" -ForegroundColor White
Write-Host "  3. 预期编译时间应从 30s 降至 5s 以内`n" -ForegroundColor White

pause
