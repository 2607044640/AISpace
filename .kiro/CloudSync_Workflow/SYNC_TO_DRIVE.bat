@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   🚀 Kiro 云端同步工具
echo ========================================
echo.

cd /d "%~dp0..\..\..\"

python "%~dp0kiro_sync_to_drive.py"

echo.
echo ========================================
pause
