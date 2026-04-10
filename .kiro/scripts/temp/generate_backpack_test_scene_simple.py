#!/usr/bin/env python3
"""
背包系统测试场景生成器 - 简化版
直接使用UIBuilder，不包含StateChart（在编辑器中手动添加）
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ui_builder', 'generators'))

from godot_ui_builder import UIBuilder, UINode

def generate_backpack_test_scene():
    """生成背包测试场景"""
    
    # 创建场景
    ui = UIBuilder("BackpackTestScene", scene_uid="uid://c8qvxqxqxqxqx")
    
    # 根节点
    root = ui.create_control("Root", fullscreen=True)
    root.properties["layout_mode"] = 3
    root.properties["anchors_preset"] = 15
    root.properties["anchor_right"] = 1.0
    root.properties["anchor_bottom"] = 1.0
    root.properties["grow_horizontal"] = 2
    root.properties["grow_vertical"] = 2
    
    # 背景
    bg = root.add_color_rect("Background", color=(0.1, 0.1, 0.1, 1), use_anchors=True)
    
    # 中心容器
    center = root.add_margin_container("CenterMargin", uniform=50, use_anchors=True, script=None)
    center.properties["anchors_preset"] = 15
    center.properties["anchor_right"] = 1.0
    center.properties["anchor_bottom"] = 1.0
    center.properties["grow_horizontal"] = 2
    center.properties["grow_vertical"] = 2
    
    # 主布局
    vbox = center.add_vbox("MainLayout", separation=20)
    
    # 标题
    title = vbox.add_label("Title", text="Backpack System Test", align="center", font_size=32)
    title.properties["size_flags_horizontal"] = 4
    
    # 背包面板容器
    backpack_container = vbox.add_panel_container("BackpackContainer")
    backpack_container.properties["size_flags_vertical"] = 3
    
    # 背包面板
    backpack_panel = UINode("BackpackPanel", "BackpackGridUIComponent", auto_suffix=False)
    backpack_panel.properties["layout_mode"] = 2
    backpack_panel.properties["size_flags_horizontal"] = 4
    backpack_panel.properties["size_flags_vertical"] = 4
    backpack_panel.properties["CellSize"] = "Vector2(64, 64)"
    backpack_panel.properties["DrawDebugLines"] = "true"
    backpack_panel.properties["GridColor"] = "Color(1, 1, 1, 0.3)"
    backpack_panel.properties["LogicGrid"] = 'NodePath("LogicGrid")'
    backpack_container._add_child(backpack_panel)
    
    # 逻辑网格
    logic_grid = UINode("LogicGrid", "BackpackGridComponent", auto_suffix=False)
    logic_grid.properties["Width"] = 8
    logic_grid.properties["Height"] = 6
    backpack_panel._add_child(logic_grid)
    
    # 交互控制器
    controller = UINode("Controller", "BackpackInteractionController", auto_suffix=False)
    controller.properties["LogicGrid"] = 'NodePath("../LogicGrid")'
    controller.properties["ViewGrid"] = 'NodePath("..")'
    backpack_panel._add_child(controller)
    
    # 物品容器
    items_container = UINode("ItemsContainer", "Control", auto_suffix=False)
    items_container.properties["layout_mode"] = 2
    items_container.properties["anchors_preset"] = 15
    items_container.properties["anchor_right"] = 1.0
    items_container.properties["anchor_bottom"] = 1.0
    backpack_panel._add_child(items_container)
    
    # 说明文本
    info_label = vbox.add_label(
        "InfoLabel",
        text="Note: StateChart nodes need to be added manually in Godot Editor",
        align="center",
        font_size=14
    )
    info_label.properties["size_flags_horizontal"] = 4
    info_label.properties["modulate"] = "Color(1, 1, 0, 1)"
    
    # 底部按钮栏
    button_row = vbox.add_hbox("ButtonRow", separation=15)
    button_row.properties["size_flags_horizontal"] = 4
    
    clear_btn = button_row.add_button("ClearButton", text="Clear Grid")
    clear_btn.properties["custom_minimum_size"] = "Vector2(120, 40)"
    
    reset_btn = button_row.add_button("ResetButton", text="Reset Items")
    reset_btn.properties["custom_minimum_size"] = "Vector2(120, 40)"
    
    # 保存场景
    output_path = "c:/Godot/3d-practice/Scenes/BackpackTestScene.tscn"
    ui.save(output_path)
    print(f"✓ 背包测试场景已生成: {output_path}")
    
    return output_path


if __name__ == "__main__":
    scene_path = generate_backpack_test_scene()
    print(f"\n测试场景生成完成！")
    print(f"路径: {scene_path}")
    print(f"\n下一步:")
    print(f"1. 在 Godot 编辑器中打开场景")
    print(f"2. 在 ItemsContainer 下手动添加测试物品（带StateChart）")
    print(f"3. 为每个测试物品配置组件和属性")
    print(f"4. 运行场景测试拖拽功能")
