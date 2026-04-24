import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
GODOT_EXE = r"C:\Program Files\Godot\Godot_v4.3-stable_mono_win64.exe"

print(f"Starting Godot...")
print(f"Executable: {GODOT_EXE}")
print(f"Project: {PROJECT_ROOT}")

subprocess.Popen([GODOT_EXE, "--path", str(PROJECT_ROOT)])
print("Game started!")
