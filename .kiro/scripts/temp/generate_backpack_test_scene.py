#!/usr/bin/env python3
"""
背包系统测试场景生成器
生成一个完整的背包测试场景，包含所有必需组件和配置
"""

import sys
import os

# 添加路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ui_builder', 'generators'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'statechart_builder'))

from godot_ui_builder import UIBuilder, UINode
from godot_statechart_builder import StateChartBuilder

def generate_item_entity(name, position, size, color, item_id):
    """生成单个物品实体场景（带StateChart）"""
    
    # 创建物品实体的StateChart
    builder = StateChartBuilder(
        entity_name=name,
        entity_type="Control",
        entity_script_path=None,  # 物品实体不需要脚本
        entity_script_uid=None
    )
    
    # 创建实体和StateChart，返回的是StateChart节点
    statechart = builder.create_entity_with_statechart()
    
    # 获取实体根节点
    entity = builder.root
    
    # 设置实体属性
    entity.properties["layout_mode"] = 0
    entity.properties["anchors_preset"] = 0
    entity.properties["offset_left"] = position[0]
    entity.properties["offset_top"] = position[1]
    entity.properties["offset_right"] = position[0] + size[0]
    entity.properties["offset_bottom"] = position[1] + size[1]
    entity.properties["mouse_filter"] = 0  # Stop
    
    # 创建状态结构
    root = statechart.add_compound_state("Root", initial_state="Idle")
    
    # Idle 状态
    idle = root.add_atomic_state("Idle")
    
    # Dragging 状态
    dragging = root.add_atomic_state("Dragging")
    
    # 添加 FollowMouseUIComponent 到 Dragging 状态
    dragging.add_component(
        "FollowMouseUIComponent",
        "res://B1Scripts/Components/FollowMouseUIComponent.cs"
    )
    # 设置 FollowMouseUIComponent 的属性
    follow_mouse = dragging.children[-1]  # 刚添加的组件
    follow_mouse.properties["TargetUI"] = 'NodePath("../../..")'
    follow_mouse.properties["GrabOffset"] = "Vector2(0, 0)"
    
    # 添加转换
    idle.add_transition("ToDragging", to_state=dragging, event="drag_start")
    dragging.add_transition("ToIdle", to_state=idle, event="drag_end")
    
    # 添加其他组件（作为实体的直接子节点）
    draggable = StateChartNode("DraggableItemComponent", "DraggableItemComponent")
    draggable.properties["ClickableArea"] = 'NodePath("..")'
    draggable.properties["StateChart"] = 'NodePath("../StateChart")'
    draggable.properties["DragStartEventName"] = '"drag_start"'
    draggable.properties["DragEndEventName"] = '"drag_end"'
    entity._add_child(draggable)
    
    shape = StateChartNode("GridShapeComponent", "GridShapeComponent")
    shape.properties["Data"] = "null"
    entity._add_child(shape)
    
    tween = StateChartNode("UITweenInteractComponent", "UITweenInteractComponent")
    tween.properties["InteractionArea"] = 'NodePath("..")'
    tween.properties["VisualTarget"] = 'NodePath("../VisualContainer")'
    tween.properties["HoverScale"] = "Vector2(1.05, 1.05)"
    tween.properties["PressScale"] = "Vector2(0.95, 0.95)"
    tween.properties["TweenDuration"] = 0.15
    entity._add_child(tween)
    
    # VisualContainer
    visual = StateChartNode("VisualContainer", "Control")
    visual.properties["layout_mode"] = 1
    visual.properties["anchors_preset"] = 15
    visual.properties["anchor_right"] = 1.0
    visual.properties["anchor_bottom"] = 1.0
    visual.properties["mouse_filter"] = 2
    entity._add_child(visual)
    
    # ItemIcon
    icon = StateChartNode("ItemIcon", "ColorRect")
    icon.properties["layout_mode"] = 1
    icon.properties["anchors_preset"] = 15
    icon.properties["anchor_right"] = 1.0
    icon.properties["anchor_bottom"] = 1.0
    icon.properties["color"] = f"Color{color}"
    icon.properties["mouse_filter"] = 2
    visual._add_child(icon)
    
    # ItemLabel
    label = StateChartNode("ItemLabel", "Label")
    label.properties["layout_mode"] = 1
    label.properties["anchors_preset"] = 8
    label.properties["anchor_left"] = 0.5
    label.properties["anchor_top"] = 0.5
    label.properties["anchor_right"] = 0.5
    label.properties["anchor_bottom"] = 0.5
    label.properties["grow_horizontal"] = 2
    label.properties["grow_vertical"] = 2
    label.properties["text"] = f'"{item_id}"'
    label.properties["horizontal_alignment"] = 1
    label.properties["vertical_alignment"] = 1
    visual._add_child(label)
    
    return entity


def generate_backpack_test_scene():
    """生成背包测试场景"""
    
    # 创建场景
    ui = UIBuilder("BackpackTestScene", scene_uid="uid://c8qvxqxqxqxqx")
    
    # 根节点 - 全屏 Control
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
    
    # 背包面板 - BackpackGridUIComponent
    backpack_panel = UINode("BackpackPanel", "BackpackGridUIComponent", auto_suffix=False)
    backpack_panel.properties["layout_mode"] = 2
    backpack_panel.properties["size_flags_horizontal"] = 4
    backpack_panel.properties["size_flags_vertical"] = 4
    backpack_panel.properties["CellSize"] = "Vector2(64, 64)"
    backpack_panel.properties["DrawDebugLines"] = "true"
    backpack_panel.properties["GridColor"] = "Color(1, 1, 1, 0.3)"
    backpack_panel.properties["LogicGrid"] = 'NodePath("LogicGrid")'
    backpack_container._add_child(backpack_panel)
    
    # 逻辑网格组件
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
    
    # 测试物品 1
    test_item1 = generate_item_entity(
        "TestItem_LShaped",
        position=(128, 128),
        size=(128, 128),
        color=(0.8, 0.3, 0.3, 1),
        item_id="item_l_shaped"
    )
    items_container._add_child(test_item1)
    
    # 测试物品 2
    test_item2 = generate_item_entity(
        "TestItem_Square",
        position=(320, 192),
        size=(64, 64),
        color=(0.3, 0.8, 0.3, 1),
        item_id="item_square"
    )
    items_container._add_child(test_item2)
    
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
    print(f"2. 为每个测试物品的 GridShapeComponent 设置 ItemDataResource")
    print(f"3. 运行场景测试拖拽功能")
