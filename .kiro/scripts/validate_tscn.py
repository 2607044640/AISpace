"""
验证.tscn文件格式
"""

import sys
import re

def validate_tscn(file_path):
    print(f"=== 验证 {file_path} ===\n")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        # 检查第一行
        first_line = lines[0]
        print(f"第一行: {first_line}")
        
        if not first_line.startswith('[gd_scene'):
            print("❌ 错误: 第一行必须以 [gd_scene 开头")
            return False
        
        # 检查UID格式
        uid_match = re.search(r'uid://[a-z0-9]+', first_line)
        if uid_match:
            print(f"✓ UID: {uid_match.group()}")
        else:
            print("❌ 错误: UID格式不正确")
            return False
        
        # 检查load_steps
        load_steps_match = re.search(r'load_steps=(\d+)', first_line)
        if load_steps_match:
            load_steps = int(load_steps_match.group(1))
            print(f"✓ load_steps: {load_steps}")
        else:
            print("❌ 错误: 缺少load_steps")
            return False
        
        # 统计资源
        ext_resources = len([l for l in lines if l.startswith('[ext_resource')])
        sub_resources = len([l for l in lines if l.startswith('[sub_resource')])
        total_resources = ext_resources + sub_resources
        
        print(f"✓ ext_resource: {ext_resources}")
        print(f"✓ sub_resource: {sub_resources}")
        print(f"✓ 总资源数: {total_resources}")
        
        if total_resources != load_steps:
            print(f"⚠️  警告: load_steps({load_steps}) != 实际资源数({total_resources})")
        
        # 检查节点定义
        nodes = len([l for l in lines if l.startswith('[node name=')])
        print(f"✓ 节点数: {nodes}")
        
        # 检查文件编码
        print(f"✓ 文件编码: UTF-8")
        print(f"✓ 文件大小: {len(content)} 字节")
        
        print("\n✅ 文件格式验证通过")
        return True
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        validate_tscn(sys.argv[1])
    else:
        # 默认验证Enemy.tscn
        import os
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        validate_tscn(os.path.join(base_dir, "Scenes", "Enemy.tscn"))
