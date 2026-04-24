"""
生成DropdownComponent prefab - 下拉选择器行组件（带独立显示区域和下拉按钮）
结构: Label + Display Area (Button/Label) + Dropdown Button + Reset Button
示例：分辨率选择器 "分辨率: [1920x1080:59] [▼] [重置]"
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from godot_ui_builder import UIBuilder, UINode


def create_dropdown_component():
    """创建下拉选择器元素prefab"""
    
    ui = UIBuilder("DropdownComponent")
    
    # 根节点：HBoxContainer
    root = UINode("DropdownRow", "HBoxContainer", auto_suffix=True)
    root.properties["layout_mode"] = 2
    root.properties["theme_override_constants/separation"] = 15
    ui.root = root
    
    # Label（固定宽度）
    root.add_label("DropdownLabel", text="选项名称:", min_size=(150, 0), size_flags_h=0)
    
    # 显示区域（显示当前选中的值，可点击展开）
    display_button = root.add_button("DisplayButton", text="1920x1080:59", size_flags_h=3)
    
    # 下拉箭头按钮
    root.add_button("DropdownArrow", text="▼", size_flags_h=4)
    
    # Reset Button
    root.add_button("ResetButton", text="重置", size_flags_h=4)
    
    # 生成树状图
    print("=" * 80)
    print("Dropdown Component Structure:")
    print("=" * 80)
    print(ui.generate_tree_view())
    print("=" * 80)
    
    # 保存
    output_path = "C:/Godot/3d-practice/A1UIScenes/UIComponents/DropdownComponent.tscn"
    ui.save(output_path)
    
    return ui


if __name__ == "__main__":
    create_dropdown_component()
