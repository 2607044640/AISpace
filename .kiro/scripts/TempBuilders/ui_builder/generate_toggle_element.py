"""
生成ToggleElement prefab - 开关行组件
结构: Label + CheckBox + Reset Button
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from godot_ui_builder import UIBuilder, UINode


def create_toggle_element():
    """创建开关元素prefab"""
    
    ui = UIBuilder("ToggleElement")
    
    # 根节点：HBoxContainer
    root = UINode("ToggleRow", "HBoxContainer", auto_suffix=True)
    root.properties["layout_mode"] = 2
    root.properties["theme_override_constants/separation"] = 20
    ui.root = root
    
    # Label
    root.add_label("ToggleLabel", text="开关名称:", min_size=(150, 0), size_flags_h=0)
    
    # CheckBox
    root.add_checkbox("ToggleCheckbox", text="启用", size_flags_h=3)
    
    # Reset Button
    root.add_button("ResetButton", text="重置", size_flags_h=4)
    
    # 生成树状图
    print("=" * 80)
    print("Toggle Element Structure:")
    print("=" * 80)
    print(ui.generate_tree_view())
    print("=" * 80)
    
    # 保存
    output_path = "C:/Godot/3d-practice/A1UIScenes/UIComponents/ToggleComponent.tscn"
    ui.save(output_path)
    
    return ui


if __name__ == "__main__":
    create_toggle_element()
