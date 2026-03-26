"""
快速部署Enemy场景到3d-practice项目
"""

import os
import shutil

def deploy_enemy():
    # 源路径（KiroWorkingSpace）
    source_base = os.path.join(os.path.dirname(__file__), "../..")
    
    # 目标路径（3d-practice）
    target_base = os.path.join(source_base, "../3d-practice")
    
    if not os.path.exists(target_base):
        print(f"❌ 3d-practice项目不存在: {target_base}")
        return
    
    # 文件映射
    files_to_copy = [
        ("Scenes/Enemy.tscn", "Scenes/Enemy.tscn"),
        ("B1Scripts/Enemy.cs", "B1Scripts/Enemy.cs"),
        ("Scenes/EnemyTest.tscn", "Scenes/EnemyTest.tscn"),
        ("B1Scripts/EnemyTestScene.cs", "B1Scripts/EnemyTestScene.cs"),
    ]
    
    print("=== 部署Enemy场景到3d-practice ===\n")
    
    for src_rel, dst_rel in files_to_copy:
        src = os.path.join(source_base, src_rel)
        dst = os.path.join(target_base, dst_rel)
        
        if not os.path.exists(src):
            print(f"⚠️  源文件不存在: {src_rel}")
            continue
        
        # 创建目标目录
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        
        # 复制文件
        shutil.copy2(src, dst)
        print(f"✓ {src_rel} → 3d-practice/{dst_rel}")
    
    print("\n=== 部署完成 ===")
    print("\n下一步:")
    print("1. 在Godot中打开3d-practice项目")
    print("2. 运行 Scenes/EnemyTest.tscn")
    print("3. 按空格键测试敌人被击中效果")

if __name__ == "__main__":
    deploy_enemy()
