"""
生成OptionElement prefab - 下拉选项行组件
结构: Label + Button(dropdown) + Reset Button
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from godot_ui_builder import UIBuilder


def create_option_element():
    """创建选项元素prefab"""
    
    ui = UIBuilder("OptionElement")
    
    # 根节点：HBoxContainer
    root = ui.root = ui.root or type('obj', (object,), {
        'name': 'OptionRow_HBoxContainer',
        'node_type': 'HBoxContainer',
        'unique_id': 100000001,
        'parent_path': '.',
        'properties': {
            'layout_mode': 2,
            'theme_override_constants/separation': 20
        },
        'children': [],
        'parent': None
    })()
    
    from godot_ui_builder import UINode
    root = UINode("OptionRow", "HBoxContainer", auto_suffix=True)
    root.properties["layout_mode"] = 2
    root.properties["theme_override_constants/separation"] = 20
    ui.root = root
    
    # Label
    root.add_label("OptionLabel", text="选项名称:", min_size=(150, 0), size_flags_h=0)
    
    # Dropdown Button
    root.add_button("OptionDropdown", text="选项值", size_flags_h=3)
    
    # Reset Button
    root.add_button("ResetButton", text="重置", size_flags_h=4)
    
    # 生成树状图
    print("=" * 80)
    print("Option Element Structure:")
    print("=" * 80)
    print(ui.generate_tree_view())
    print("=" * 80)
    
    # 保存
    output_path = "C:/Godot/3d-practice/A1UIScenes/UIComponents/OptionComponent.tscn"
    ui.save(output_path)
    
    return ui


if __name__ == "__main__":
    create_option_element()
