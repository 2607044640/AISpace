---
description: Manually sync project context to Google Drive for Gemini (runs CloudSync_Workflow silently in background)
---

# Sync to Gemini

This workflow replaces the Kiro `agentStop` auto-sync hook. It triggers the CloudSync pipeline that
scans `AISpace/.windsurf/rules/` + `3d-practice/` and writes the AI context bundle to
`C:\Users\26070\My Drive\Kiro_Godot_Brain\`.

## Steps

1. Run the sync in a hidden background window:
// turbo
```powershell
Start-Process powershell -WindowStyle Hidden -ArgumentList '-Command', "& 'C:\Godot\3d-practice\SYNC_TO_GEMINI_SILENT.bat'"
```

2. (Optional) Tail the latest log to verify success:
// turbo
```powershell
Get-ChildItem 'C:\Godot\AISpace\CloudSync_Workflow\logs' -Filter 'sync_*.log' |
    Sort-Object LastWriteTime -Descending | Select-Object -First 1 |
    ForEach-Object { Get-Content $_.FullName -Tail 20 }
```

3. (Optional) Inspect the most recent changes Gemini will see:
// turbo
```powershell
Get-Content "C:\Users\26070\My Drive\Kiro_Godot_Brain\AI_Context_Changes.md" -Head 30
```
