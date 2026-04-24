"""
修复Godot缓存问题
删除.godot文件夹强制重新导入
"""

import os
import shutil

def fix_godot_cache(project_path):
    godot_cache = os.path.join(project_path, ".godot")
    
    if os.path.exists(godot_cache):
        print(f"删除Godot缓存: {godot_cache}")
        try:
            shutil.rmtree(godot_cache)
            print("✓ 缓存已删除")
            print("\n下一步:")
            print("1. 在Godot中重新打开项目")
            print("2. 等待重新导入完成")
            print("3. 尝试打开Enemy.tscn")
        except Exception as e:
            print(f"❌ 删除失败: {e}")
    else:
        print("⚠️  .godot文件夹不存在")

if __name__ == "__main__":
    # 修复3d-practice项目
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    project_path = os.path.join(base_dir, "../3d-practice")
    
    if os.path.exists(project_path):
        fix_godot_cache(project_path)
    else:
        print(f"❌ 项目不存在: {project_path}")
