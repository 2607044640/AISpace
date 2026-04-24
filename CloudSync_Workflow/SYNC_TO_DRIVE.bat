@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   🚀 Agent 云端同步工具
echo ========================================
echo.

cd /d "%~dp0..\..\..\"

python "%~dp0agent_sync_to_drive.py"

echo.
echo ========================================
pause
