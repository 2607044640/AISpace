"""
分析 SettingsMenuV2.tscn 中的 OptionComponent 实例
找到 testfwewfa（正确的）和其他 OptionComponent（错误的），对比差异
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from tscn_editor_tools.reader import TscnReader

def main():
    # 读取 SettingsMenuV2.tscn
    script_dir = Path(__file__).parent.resolve()
    # 从 C:\Godot\KiroWorkingSpace\.kiro\scripts\ui_builder 到 C:\Godot\3d-practice
    workspace_root = script_dir.parent.parent.parent.parent
    tscn_path = workspace_root / "3d-practice" / "A1UIScenes" / "SettingsMenuV2.tscn"
    
    print(f"脚本目录: {script_dir}")
    print(f"工作区根目录: {workspace_root}")
    print(f"TSCN路径: {tscn_path}")
    print(f"文件存在: {tscn_path.exists()}")
    print()
    
    print("="*70)
    print("分析 SettingsMenuV2.tscn 中的 OptionComponent 实例")
    print("="*70)
    
    reader = TscnReader(str(tscn_path))
    
    # 打印完整树形结构
    print("\n完整场景树形结构：")
    print("="*70)
    print(reader.print_tree_view())
    
    # 查找所有 OptionComponent 实例
    print("\n"+"="*70)
    print("查找所有场景实例节点：")
    print("="*70)
    
    option_components = []
    for node in reader.tree.nodes:
        if node.is_instance:
            path = reader.tree.build_full_path(node)
            print(f"\n节点: {node.name}")
            print(f"  路径: {path}")
            print(f"  类型: {node.node_type}")
            print(f"  场景路径: {node.scene_path}")
            print(f"  场景UID: {node.scene_uid}")
            print(f"  unique_id: {node.unique_id}")
            print(f"  父节点: {node.parent_path}")
            
            # 打印所有属性
            if node.properties:
                print(f"  属性:")
                for key, value in node.properties.items():
                    if not key.startswith('_'):  # 跳过内部属性
                        print(f"    {key} = {value}")
            
            # 如果是 OptionComponent，记录下来
            if node.scene_path and "OptionComponent" in node.scene_path:
                option_components.append((node.name, path, node))
    
    # 重点对比 OptionComponent
    print("\n"+"="*70)
    print("OptionComponent 实例对比：")
    print("="*70)
    
    if option_components:
        print(f"\n找到 {len(option_components)} 个 OptionComponent 实例：")
        for name, path, node in option_components:
            print(f"\n{'='*70}")
            print(f"节点名称: {name}")
            print(f"完整路径: {path}")
            print(f"场景路径: {node.scene_path}")
            print(f"场景UID: {node.scene_uid}")
            print(f"unique_id: {node.unique_id}")
            print(f"父节点: {node.parent_path}")
            
            # 详细属性
            print(f"\n所有属性（包括内部）:")
            for key, value in sorted(node.properties.items()):
                print(f"  {key} = {value}")
            
            # 特别标注 testfwewfa
            if name == "testfwewfa":
                print("\n⭐⭐⭐ 这是正确的 OptionComponent 实例！⭐⭐⭐")
    else:
        print("未找到 OptionComponent 实例")
    
    # 查找 testfwewfa 节点
    print("\n"+"="*70)
    print("查找 testfwewfa 节点：")
    print("="*70)
    
    testfwewfa_nodes = reader.find_nodes_by_name("testfwewfa")
    if testfwewfa_nodes:
        for node in testfwewfa_nodes:
            path = reader.tree.build_full_path(node)
            print(f"\n找到 testfwewfa!")
            print(f"  完整路径: {path}")
            print(f"  类型: {node.node_type}")
            print(f"  是否为场景实例: {node.is_instance}")
            print(f"  场景路径: {node.scene_path}")
            print(f"  场景UID: {node.scene_uid}")
            print(f"  unique_id: {node.unique_id}")
            print(f"  父节点: {node.parent_path}")
            
            print(f"\n  所有属性:")
            for key, value in sorted(node.properties.items()):
                print(f"    {key} = {value}")
    else:
        print("未找到 testfwewfa 节点")
    
    # 对比分析
    print("\n"+"="*70)
    print("差异分析：")
    print("="*70)
    
    if len(option_components) >= 2:
        # 找到 testfwewfa
        correct_node = None
        wrong_nodes = []
        
        for name, path, node in option_components:
            if name == "testfwewfa":
                correct_node = (name, path, node)
            else:
                wrong_nodes.append((name, path, node))
        
        if correct_node and wrong_nodes:
            print(f"\n正确的节点: {correct_node[0]}")
            print(f"错误的节点: {[n[0] for n in wrong_nodes]}")
            
            correct_props = correct_node[2].properties
            
            print(f"\n属性对比：")
            for wrong_name, wrong_path, wrong_node in wrong_nodes:
                print(f"\n对比 {wrong_name}:")
                wrong_props = wrong_node.properties
                
                # 找出差异
                all_keys = set(correct_props.keys()) | set(wrong_props.keys())
                for key in sorted(all_keys):
                    if key.startswith('_'):
                        continue
                    
                    correct_val = correct_props.get(key, "❌ 缺失")
                    wrong_val = wrong_props.get(key, "❌ 缺失")
                    
                    if correct_val != wrong_val:
                        print(f"  ⚠️  {key}:")
                        print(f"      正确: {correct_val}")
                        print(f"      错误: {wrong_val}")

if __name__ == "__main__":
    main()
