"""
修复 SettingsMenuV2.tscn 中所有错误的 DropdownComponent 实例
删除 script = null 属性，添加正确的 LabelText 属性
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from tscn_editor_tools.editor import TscnEditor
from tscn_editor_tools.types import PropertyUpdate

def main():
    script_dir = Path(__file__).parent.resolve()
    workspace_root = script_dir.parent.parent.parent.parent
    tscn_path = workspace_root / "3d-practice" / "A1UIScenes" / "SettingsMenuV2.tscn"
    
    print("="*70)
    print("修复 SettingsMenuV2.tscn 中的 DropdownComponent 实例")
    print("="*70)
    print(f"\n文件路径: {tscn_path}\n")
    
    # 加载编辑器
    editor = TscnEditor(str(tscn_path))
    
    # 查找所有 DropdownComponent 实例
    dropdown_nodes = []
    for node in editor._tree.nodes:
        if node.is_instance and node.scene_path == "res://A1UIScenes/UIComponents/DropdownComponent.tscn":
            dropdown_nodes.append(node)
    
    print(f"找到 {len(dropdown_nodes)} 个 DropdownComponent 实例\n")
    
    # 定义正确的 LabelText 映射
    label_text_map = {
        "DisplayMode": "Display Mode",
        "WindowResolution": "Window Resolution",
        "VSync": "VSync",
        "FPSLimit": "FPS Limit",
        "AntiAlias": "Anti-Alias",
        "NumberFormat": "Number Format",
        "Language": "Language",
        "GameMode": "Game Mode",
        "testfwewfa": "testfwewfa"  # 保持不变
    }
    
    # 批量更新
    updates = []
    
    for node in dropdown_nodes:
        node_path = editor._tree.build_full_path(node)
        
        print(f"处理节点: {node.name}")
        print(f"  路径: {node_path}")
        
        # 检查是否有 script 属性
        if "script" in node.properties:
            print(f"  ❌ 发现错误的 script 属性: {node.properties['script']}")
            # 删除 script 属性（通过设置为 None 然后手动删除）
            del node.properties["script"]
            print(f"  ✅ 已删除 script 属性")
        
        # 检查是否缺少 LabelText
        if "LabelText" not in node.properties:
            label_text = label_text_map.get(node.name, node.name)
            print(f"  ❌ 缺少 LabelText 属性")
            print(f"  ✅ 添加 LabelText = \"{label_text}\"")
            node.properties["LabelText"] = label_text
        else:
            print(f"  ✓ 已有 LabelText = \"{node.properties['LabelText']}\"")
        
        print()
    
    # 重建索引
    editor._tree._build_indices()
    
    # 保存
    output_path = tscn_path.parent / "SettingsMenuV2_Fixed.tscn"
    print(f"保存到: {output_path}")
    editor.save(str(output_path))
    
    print("\n" + "="*70)
    print("✅ 修复完成！")
    print("="*70)
    print(f"\n修复后的文件: {output_path}")
    print("请在 Godot 中打开验证")

if __name__ == "__main__":
    main()
