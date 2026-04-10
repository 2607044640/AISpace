# Script to find all 360-related files and folders
Write-Host "Searching for 360-related files..." -ForegroundColor Yellow

$results = @()

# Search locations
$searchPaths = @(
    "$env:APPDATA",
    "$env:LOCALAPPDATA",
    "C:\Program Files",
    "C:\Program Files (x86)",
    "$env:USERPROFILE\Desktop",
    "$env:USERPROFILE\Downloads",
    "C:\ProgramData"
)

foreach ($path in $searchPaths) {
    if (Test-Path $path) {
        Write-Host "Searching in: $path" -ForegroundColor Cyan
        $items = Get-ChildItem -Path $path -Filter "*360*" -Recurse -ErrorAction SilentlyContinue
        $results += $items
    }
}

# Display results
Write-Host "`nFound $($results.Count) items containing '360':" -ForegroundColor Green
$results | Select-Object FullName, @{Name="Type";Expression={if($_.PSIsContainer){"Folder"}else{"File"}}}, Length, LastWriteTime | Format-Table -AutoSize

# Save to file
$results | Select-Object FullName, @{Name="Type";Expression={if($_.PSIsContainer){"Folder"}else{"File"}}} | Export-Csv -Path "360_files_found.csv" -NoTypeInformation -Encoding UTF8
Write-Host "`nResults saved to: 360_files_found.csv" -ForegroundColor Green

# Check for 360 in browser shortcuts
Write-Host "`nChecking browser shortcuts..." -ForegroundColor Yellow
$shortcuts = Get-ChildItem -Path "$env:APPDATA\Microsoft\Internet Explorer\Quick Launch" -Filter "*.lnk" -ErrorAction SilentlyContinue
$shortcuts += Get-ChildItem -Path "$env:USERPROFILE\Desktop" -Filter "*.lnk" -ErrorAction SilentlyContinue

foreach ($shortcut in $shortcuts) {
    $shell = New-Object -ComObject WScript.Shell
    $link = $shell.CreateShortcut($shortcut.FullName)
    if ($link.TargetPath -like "*360*" -or $link.Arguments -like "*360*") {
        Write-Host "Found 360 reference in shortcut: $($shortcut.FullName)" -ForegroundColor Red
        Write-Host "  Target: $($link.TargetPath)" -ForegroundColor Gray
        Write-Host "  Arguments: $($link.Arguments)" -ForegroundColor Gray
    }
}
