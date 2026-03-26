"""
生成SliderElement prefab - 滑块行组件
结构: Label + ProgressBar + Reset Button
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from godot_ui_builder import UIBuilder, UINode


def create_slider_element():
    """创建滑块元素prefab"""
    
    ui = UIBuilder("SliderElement")
    
    # 根节点：HBoxContainer
    root = UINode("SliderRow", "HBoxContainer", auto_suffix=True)
    root.properties["layout_mode"] = 2
    root.properties["theme_override_constants/separation"] = 20
    ui.root = root
    
    # Label
    root.add_label("SliderLabel", text="滑块名称:", min_size=(150, 0), size_flags_h=0)
    
    # ProgressBar (作为滑块)
    root.add_progress_bar("SliderBar", value=50, 
                         size_flags_h=3, size_flags_v=4,
                         show_percentage=True)
    
    # Reset Button
    root.add_button("ResetButton", text="重置", size_flags_h=4)
    
    # 生成树状图
    print("=" * 80)
    print("Slider Element Structure:")
    print("=" * 80)
    print(ui.generate_tree_view())
    print("=" * 80)
    
    # 保存
    output_path = "C:/Godot/3d-practice/A1UIScenes/UIComponents/SliderComponent.tscn"
    ui.save(output_path)
    
    return ui


if __name__ == "__main__":
    create_slider_element()
