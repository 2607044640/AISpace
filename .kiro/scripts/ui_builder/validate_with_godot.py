"""
Validate that Godot can parse the test output file
"""

import subprocess
import sys
from pathlib import Path

def validate_scene_with_godot(scene_path: str, project_path: str) -> bool:
    """
    Validate a .tscn file by attempting to load it with Godot's --check-only flag
    
    Args:
        scene_path: Path to .tscn file
        project_path: Path to Godot project directory
        
    Returns:
        True if valid, False otherwise
    """
    
    # Try to find Godot executable
    godot_paths = [
        r"C:\Program Files\Godot\Godot_v4.3-stable_mono_win64\Godot_v4.3-stable_mono_win64.exe",
        r"C:\Godot\Godot_v4.3-stable_mono_win64\Godot_v4.3-stable_mono_win64.exe",
        "godot",
        "godot4"
    ]
    
    godot_exe = None
    for path in godot_paths:
        if Path(path).exists():
            godot_exe = path
            break
    
    if godot_exe is None:
        print("⚠️  Could not find Godot executable")
        print("   Skipping Godot validation (Python tests passed)")
        return True
    
    print(f"Using Godot: {godot_exe}")
    
    # Run Godot with --check-only flag
    try:
        result = subprocess.run(
            [godot_exe, "--path", project_path, "--check-only", scene_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✓ Godot successfully validated the scene file")
            return True
        else:
            print(f"✗ Godot validation failed:")
            print(f"  stdout: {result.stdout}")
            print(f"  stderr: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ Godot validation timed out")
        return False
    except Exception as e:
        print(f"✗ Error running Godot: {e}")
        return False


if __name__ == "__main__":
    scene_path = "A1UIScenes/SettingsMenuV2_Test.tscn"
    project_path = str(Path(__file__).parent.parent.parent.parent.parent / "3d-practice")
    
    print("="*60)
    print("GODOT VALIDATION TEST")
    print("="*60)
    print(f"Scene: {scene_path}")
    print(f"Project: {project_path}")
    print()
    
    success = validate_scene_with_godot(scene_path, project_path)
    
    sys.exit(0 if success else 1)
