"""
Generate TetrisDraggableItem.tscn - Complete draggable item with rotation
用途：完整的可拖拽物品模板，包含 StateChart、拖拽、旋转、网格形状
"""

import sys
import os

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Direct imports to avoid circular dependency
import core
import modules.statechart as statechart_module

TscnBuilder = core.TscnBuilder
StateChartBuilder = statechart_module.StateChartModule  # 正确的类名


def generate_draggable_item():
    """生成完整的可拖拽物品模板"""
    
    # 创建场景
    scene = TscnBuilder("TetrisDraggableItem", "Control")
    root = scene.initialize_root(
        custom_minimum_size="Vector2(64, 64)",
        layout_mode=3,
        anchors_preset=0
    )
    
    # 添加可点击背景（用于接收鼠标输入）
    scene.add_node(
        "ClickableBackground",
        "ColorRect",
        parent=".",
        layout_mode=1,
        anchors_preset=15,
        anchor_right=1.0,
        anchor_bottom=1.0,
        grow_horizontal=2,
        grow_vertical=2,
        color="Color(0.3, 0.7, 0.3, 0.8)",  # 半透明绿色
        mouse_filter=0,  # Stop - 接收鼠标输入
        unique_name_in_owner=True
    )
    
    # 添加 VisualContainer（用于显示物品图标）
    scene.add_node(
        "VisualContainer",
        "Control",
        parent=".",
        layout_mode=1,
        anchors_preset=15,
        anchor_right=1.0,
        anchor_bottom=1.0,
        grow_horizontal=2,
        grow_vertical=2,
        mouse_filter=2  # Ignore - 不接收鼠标输入
    )
    
    # 添加物品图标
    scene.add_node(
        "ItemIcon",
        "TextureRect",
        parent="VisualContainer",
        layout_mode=1,
        anchors_preset=15,
        anchor_right=1.0,
        anchor_bottom=1.0,
        grow_horizontal=2,
        grow_vertical=2,
        expand_mode=1,  # ExpandMode.IGNORE_SIZE
        stretch_mode=5,  # StretchMode.KEEP_ASPECT_CENTERED
        mouse_filter=2  # Ignore
    )
    
    # 添加 StateChart
    statechart = StateChartBuilder(scene, parent=".")
    statechart.add_statechart("StateChart")
    
    # 创建 Idle/Dragging 状态机
    statechart.add_compound_state("Root", parent="StateChart", initial_state="Idle")
    statechart.add_atomic_state("Idle", parent="Root")
    statechart.add_atomic_state("Dragging", parent="Root")
    
    # 添加转换
    statechart.add_transition(
        "ToDragging",
        from_state="Idle",
        to_state="Dragging",
        event="drag_start",
        delay=0.0
    )
    
    statechart.add_transition(
        "ToIdle",
        from_state="Dragging",
        to_state="Idle",
        event="drag_end",
        delay=0.0
    )
    
    # 在 Dragging 状态下添加 FollowMouseUIComponent
    follow_mouse_script_id = scene.add_ext_resource(
        "Script",
        "res://addons/A1TetrisBackpack/Interaction/FollowMouseUIComponent.cs",
        "uid://placeholder",
        "follow_mouse_script"
    )
    
    scene.add_node(
        "FollowMouseUIComponent",
        "Node",
        parent="Dragging",
        script=f'ExtResource("{follow_mouse_script_id}")'
    )
    
    # 绑定 FollowMouseUIComponent 的 TargetUIPath
    scene.assign_node_path("FollowMouseUIComponent", "TargetUIPath", "TetrisDraggableItem")
    
    # 解析初始状态
    statechart.resolve_initial_states()
    
    # 添加 DraggableItemComponent
    draggable_script_id = scene.add_ext_resource(
        "Script",
        "res://addons/A1TetrisBackpack/Interaction/DraggableItemComponent.cs",
        "uid://placeholder",
        "draggable_script"
    )
    
    scene.add_node(
        "DraggableItemComponent",
        "Node",
        parent=".",
        script=f'ExtResource("{draggable_script_id}")'
    )
    
    # 绑定 DraggableItemComponent 的路径
    scene.assign_node_path("DraggableItemComponent", "ClickableAreaPath", "ClickableBackground")
    scene.assign_node_path("DraggableItemComponent", "StateChartPath", "StateChart")
    
    # 添加 GridShapeComponent
    shape_script_id = scene.add_ext_resource(
        "Script",
        "res://addons/A1TetrisBackpack/Items/GridShapeComponent.cs",
        "uid://placeholder",
        "shape_script"
    )
    
    scene.add_node(
        "GridShapeComponent",
        "Node",
        parent=".",
        script=f'ExtResource("{shape_script_id}")'
    )
    
    # 生成场景
    workspace_root = os.path.dirname(os.path.dirname(current_dir))
    output_path = os.path.join(workspace_root, "3d-practice", "addons", "A1TetrisBackpack", "Items", "TetrisDraggableItem.tscn")
    scene.save(output_path)
    
    print("\n=== TetrisDraggableItem.tscn 生成完成 ===")
    print("用途：完整的可拖拽物品模板")
    print("功能：")
    print("  - 拖拽：左键拖动物品")
    print("  - 旋转：右键旋转物品（需要在 Controller 中订阅）")
    print("  - 网格形状：支持 Tetris 形状定义")
    print("  - StateChart：Idle/Dragging 状态管理")
    print("\n使用方法：")
    print("  1. 实例化此场景")
    print("  2. 设置 GridShapeComponent.Data 为 ItemDataResource")
    print("  3. 设置 ItemIcon.texture 为物品图标")
    print("  4. 在 BackpackInteractionController 中注册物品")
    print("\n节点树：")
    print(scene.generate_tree_view())


if __name__ == "__main__":
    generate_draggable_item()
