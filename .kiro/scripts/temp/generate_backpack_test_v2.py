"""
背包系统测试场景生成器 V2
基于正确的 TscnBuilder API
生成时间：2026-04-15
"""

import sys
sys.path.append('C:/Godot/KiroWorkingSpace')

from builder.core import TscnBuilder
from builder.modules.ui import UIModule
from builder.modules.statechart import StateChartModule

# ============================================================
# 1. 初始化场景
# ============================================================
scene = TscnBuilder(root_name="BackpackTest", root_type="Control")
ui = UIModule(scene)

# 设置全屏根节点
scene.initialize_root(
    layout_mode=3,
    anchors_preset=15,
    anchor_right=1.0,
    anchor_bottom=1.0,
    grow_horizontal=2,
    grow_vertical=2
)

# ============================================================
# 2. 添加背景
# ============================================================
scene.add_node("Background", "ColorRect", parent=".",
    layout_mode=1,
    anchors_preset=15,
    anchor_right=1.0,
    anchor_bottom=1.0,
    grow_horizontal=2,
    grow_vertical=2,
    color="Color(0.1, 0.1, 0.12, 1)"
)

# ============================================================
# 3. 添加主容器
# ============================================================
scene.add_node("ScreenMargin", "MarginContainer", parent=".",
    layout_mode=1,
    anchors_preset=15,
    anchor_right=1.0,
    anchor_bottom=1.0,
    grow_horizontal=2,
    grow_vertical=2
)

# 设置边距
margin_node = scene.get_node("ScreenMargin")
margin_node.set_property("theme_override_constants/margin_left", 50)
margin_node.set_property("theme_override_constants/margin_top", 50)
margin_node.set_property("theme_override_constants/margin_right", 50)
margin_node.set_property("theme_override_constants/margin_bottom", 50)

scene.add_node("MainVBox", "VBoxContainer", parent="ScreenMargin",
    layout_mode=2
)

# 设置 VBox 间距
vbox_node = scene.get_node("MainVBox")
vbox_node.set_property("theme_override_constants/separation", 30)

# ============================================================
# 4. 添加标题
# ============================================================
scene.add_node("Title", "Label", parent="MainVBox",
    layout_mode=2,
    text="Backpack System Test",
    horizontal_alignment=1
)

# 设置标题字体大小
title_node = scene.get_node("Title")
title_node.set_property("theme_override_font_sizes/font_size", 36)

# ============================================================
# 5. 创建背包面板 (BackpackGridUIComponent)
# ============================================================
backpack_grid_ui_res = scene.add_ext_resource(
    resource_type="Script",
    path="res://addons/A1TetrisBackpack/Core/BackpackGridUIComponent.cs",
    uid="uid://dkk5driwga8ql"
)

scene.add_node("BackpackPanel", "Control", parent="MainVBox",
    layout_mode=2,
    size_flags_horizontal=4,
    size_flags_vertical=4,
    script=f'ExtResource("{backpack_grid_ui_res}")'
)

# 设置网格属性
backpack_panel = scene.get_node("BackpackPanel")
backpack_panel.set_property("Width", 10)
backpack_panel.set_property("Height", 6)
backpack_panel.set_property("DrawDebugLines", True)

# ============================================================
# 6. 添加逻辑网格组件
# ============================================================
logic_grid_res = scene.add_ext_resource(
    resource_type="Script",
    path="res://addons/A1TetrisBackpack/Core/BackpackGridComponent.cs",
    uid="uid://1rgai2oppf42"
)

scene.add_node("BackpackGridComponent", "Node", parent="BackpackPanel",
    script=f'ExtResource("{logic_grid_res}")'
)

logic_grid = scene.get_node("BackpackGridComponent")
logic_grid.set_property("Width", 10)
logic_grid.set_property("Height", 6)

# ============================================================
# 7. 添加交互控制器
# ============================================================
controller_res = scene.add_ext_resource(
    resource_type="Script",
    path="res://addons/A1TetrisBackpack/Core/BackpackInteractionController.cs",
    uid="uid://drof8dtjnyqs3"
)

scene.add_node("BackpackInteractionController", "Node", parent="BackpackPanel",
    script=f'ExtResource("{controller_res}")'
)

# ============================================================
# 8. 创建物品容器
# ============================================================
scene.add_node("ItemsContainer", "Control", parent="BackpackPanel",
    layout_mode=2
)

# ============================================================
# 9. 创建测试物品
# ============================================================
scene.add_node("TestItem", "Control", parent="ItemsContainer",
    custom_minimum_size="Vector2(64, 64)",
    layout_mode=2,
    position="Vector2(128, 128)"
)

# 添加可点击背景（用于接收鼠标输入）
scene.add_node("ClickableBackground", "ColorRect", parent="TestItem",
    layout_mode=1,
    anchors_preset=15,
    anchor_right=1.0,
    anchor_bottom=1.0,
    color="Color(0.2, 0.2, 0.2, 0.5)"
)

# ============================================================
# 10. 创建 StateChart
# ============================================================
sc = StateChartModule(scene, parent="TestItem")
sc.add_statechart("StateChart")

# Root 状态
sc.add_compound_state("Root", parent="StateChart", initial_state="Idle")

# Idle 状态
sc.add_atomic_state("Idle", parent="Root")

# Dragging 状态
sc.add_atomic_state("Dragging", parent="Root")

# Transitions
sc.add_transition("ToDragging", from_state="Idle", to_state="Dragging", event="drag_start")
sc.add_transition("ToIdle", from_state="Dragging", to_state="Idle", event="drag_end")

# ============================================================
# 11. 添加 FollowMouseUIComponent 到 Dragging 状态
# ============================================================
follow_mouse_res = scene.add_ext_resource(
    resource_type="Script",
    path="res://addons/A1TetrisBackpack/Interaction/FollowMouseUIComponent.cs",
    uid="uid://d2svbqvyq43tw"
)

scene.add_node("FollowMouseUIComponent", "Node", parent="Dragging",
    script=f'ExtResource("{follow_mouse_res}")'
)

# ============================================================
# 12. 添加 DraggableItemComponent
# ============================================================
draggable_res = scene.add_ext_resource(
    resource_type="Script",
    path="res://addons/A1TetrisBackpack/Interaction/DraggableItemComponent.cs",
    uid="uid://bdka4obxtossd"
)

scene.add_node("DraggableItemComponent", "Node", parent="TestItem",
    script=f'ExtResource("{draggable_res}")'
)

# ============================================================
# 13. 添加 GridShapeComponent
# ============================================================
shape_res = scene.add_ext_resource(
    resource_type="Script",
    path="res://addons/A1TetrisBackpack/Items/GridShapeComponent.cs",
    uid="uid://bbykh8wvhqtcj"
)

scene.add_node("GridShapeComponent", "Node", parent="TestItem",
    script=f'ExtResource("{shape_res}")'
)

# ============================================================
# 14. 创建 VisualContainer
# ============================================================
scene.add_node("VisualContainer", "Control", parent="TestItem",
    layout_mode=2,
    size_flags_horizontal=4,
    size_flags_vertical=4
)

# ============================================================
# 15. 添加物品图标 (ColorRect 占位符)
# ============================================================
scene.add_node("ItemIcon", "ColorRect", parent="VisualContainer",
    layout_mode=2,
    custom_minimum_size="Vector2(64, 64)",
    color="Color(0.3, 0.6, 0.9, 1)"
)

# ============================================================
# 16. 添加说明文本
# ============================================================
scene.add_node("Instructions", "Label", parent="MainVBox",
    layout_mode=2,
    text="Left Click: Drag | Right Click: Rotate | Drop in backpack to place",
    horizontal_alignment=1
)

instructions_node = scene.get_node("Instructions")
instructions_node.set_property("theme_override_font_sizes/font_size", 16)

# ============================================================
# 17. 绑定所有 NodePath
# ============================================================
# BackpackPanel 绑定（修复：BackpackGridUIComponent 需要 LogicGrid 引用）
scene.assign_node_path("BackpackPanel", "LogicGrid", "BackpackGridComponent")

# BackpackInteractionController 绑定
scene.assign_multiple_node_paths("BackpackInteractionController", {
    "LogicGrid": "BackpackGridComponent",
    "ViewGrid": "BackpackPanel"
})

# DraggableItemComponent 绑定
scene.assign_multiple_node_paths("DraggableItemComponent", {
    "ClickableArea": "TestItem",
    "StateChart": "StateChart"
})

# FollowMouseUIComponent 绑定
scene.assign_multiple_node_paths("FollowMouseUIComponent", {
    "TargetUI": "TestItem"
})

# ============================================================
# 18. 解析 StateChart 初始状态
# ============================================================
sc.resolve_initial_states()

# ============================================================
# 19. 生成树形视图（调试用）
# ============================================================
print("\n=== Scene Tree ===")
print(scene.generate_tree_view())

# ============================================================
# 20. 保存场景
# ============================================================
output_path = "C:/Godot/3d-practice/Scenes/BackpackTest.tscn"
scene.save(output_path)

print(f"\n✓ 测试场景已生成: {output_path}")
print("\n接下来的操作：")
print("1. 在 Godot 中打开场景: Scenes/BackpackTest.tscn")
print("2. 运行场景 (F5)")
print("3. 测试功能：")
print("   - 左键拖动物品")
print("   - 右键旋转物品")
print("   - 放置到背包网格中")
print("   - 尝试放置到边界外（应该回弹）")
print("4. 检查控制台输出查看日志")
