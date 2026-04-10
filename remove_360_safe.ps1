# Script to remove 360 Safe and related files
# Run as Administrator if needed

Write-Host "=== 360 Safe Removal Script ===" -ForegroundColor Yellow
Write-Host ""

# Main 360 Safe folder
$360SafeFolder = "$env:APPDATA\360safe"

if (Test-Path $360SafeFolder) {
    Write-Host "Found 360 Safe folder: $360SafeFolder" -ForegroundColor Red
    Write-Host "Attempting to remove..." -ForegroundColor Yellow
    
    try {
        Remove-Item -Path $360SafeFolder -Recurse -Force -ErrorAction Stop
        Write-Host "Successfully removed 360 Safe folder!" -ForegroundColor Green
    }
    catch {
        Write-Host "Error removing folder: $_" -ForegroundColor Red
        Write-Host "You may need to run this script as Administrator" -ForegroundColor Yellow
    }
}
else {
    Write-Host "360 Safe folder not found at: $360SafeFolder" -ForegroundColor Green
}

# Check for 360 in browser settings
Write-Host "`nChecking browser homepage settings..." -ForegroundColor Yellow

# Check IE homepage
$ieHomepage = Get-ItemProperty -Path "HKCU:\Software\Microsoft\Internet Explorer\Main" -Name "Start Page" -ErrorAction SilentlyContinue
if ($ieHomepage -and $ieHomepage.'Start Page' -like "*360*") {
    Write-Host "Found 360 in IE homepage: $($ieHomepage.'Start Page')" -ForegroundColor Red
    Write-Host "To reset, run: Set-ItemProperty -Path 'HKCU:\Software\Microsoft\Internet Explorer\Main' -Name 'Start Page' -Value 'about:blank'" -ForegroundColor Cyan
}

# Check for 360 in startup programs
Write-Host "`nChecking startup programs..." -ForegroundColor Yellow
$startupItems = Get-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -ErrorAction SilentlyContinue
if ($startupItems) {
    $startupItems.PSObject.Properties | Where-Object { $_.Value -like "*360*" } | ForEach-Object {
        Write-Host "Found 360 in startup: $($_.Name) = $($_.Value)" -ForegroundColor Red
        Write-Host "To remove, run: Remove-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run' -Name '$($_.Name)'" -ForegroundColor Cyan
    }
}

# Check for 360 browser extensions/plugins
Write-Host "`nChecking for 360-related browser extensions..." -ForegroundColor Yellow
$chromeExtensions = "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Extensions"
if (Test-Path $chromeExtensions) {
    Get-ChildItem -Path $chromeExtensions -Directory | ForEach-Object {
        $manifestPath = Join-Path $_.FullName "*\manifest.json"
        $manifests = Get-ChildItem -Path $manifestPath -ErrorAction SilentlyContinue
        foreach ($manifest in $manifests) {
            $content = Get-Content $manifest.FullName -Raw -ErrorAction SilentlyContinue
            if ($content -like "*360*") {
                Write-Host "Found potential 360 extension: $($_.Name)" -ForegroundColor Red
                Write-Host "  Path: $($_.FullName)" -ForegroundColor Gray
            }
        }
    }
}

Write-Host "`n=== Cleanup Complete ===" -ForegroundColor Green
Write-Host "Please restart your computer for changes to take full effect." -ForegroundColor Yellow
Write-Host "`nIf 360 still appears, check your CapsLock+ plugin settings for custom search engines." -ForegroundColor Cyan
