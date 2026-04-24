import sys
sys.path.append('C:/Godot/AISpace/.kiro/scripts/ui_builder/generators')
from godot_ui_builder import UIBuilder

# 创建背包测试场景
ui = UIBuilder("BackpackTest")
root = ui.create_control("BackpackTest", fullscreen=True)

# 背景
root.add_color_rect("Background", color=(0.1, 0.1, 0.12, 1), use_anchors=True)

# 全屏边距
margin = root.add_margin_container("ScreenMargin", uniform=50, use_anchors=True, script=None)
margin.set_property("anchors_preset", 15)
margin.set_property("anchor_right", 1.0)
margin.set_property("anchor_bottom", 1.0)
margin.set_property("grow_horizontal", 2)
margin.set_property("grow_vertical", 2)

# 主容器
vbox = margin.add_vbox("MainContent", separation=30)

# 标题
vbox.add_label("Title", text="Backpack System Test", align="center", font_size=36)

# 背包面板容器
backpack_panel = vbox.add_panel_container("BackpackPanel")
backpack_inner = backpack_panel.add_margin_container("PanelMargin", uniform=20, script=None)

# 背包网格 UI (BackpackGridUIComponent)
backpack_grid = backpack_inner.add_control("BackpackGridUI")
backpack_grid.set_property("layout_mode", 2)
backpack_grid.set_property("size_flags_horizontal", 4)  # Shrink center
backpack_grid.set_property("size_flags_vertical", 4)
backpack_grid.set_property("script", 'ExtResource("1_backpack_grid_ui")')

# 逻辑网格组件 (BackpackGridComponent)
logic_grid = backpack_grid.add_node("LogicGrid", "Node")
logic_grid.set_property("script", 'ExtResource("2_backpack_grid")')

# 控制器 (BackpackInteractionController)
controller = backpack_grid.add_node("Controller", "Node")
controller.set_property("script", 'ExtResource("3_controller")')

# 物品容器
items_container = backpack_grid.add_control("ItemsContainer")
items_container.set_property("layout_mode", 2)

# 测试物品实体
test_item = items_container.add_control("TestItem")
test_item.set_property("custom_minimum_size", "Vector2(64, 64)")
test_item.set_property("layout_mode", 2)

# StateChart
statechart = test_item.add_node("StateChart", "Node")
statechart.set_property("script", 'ExtResource("4_statechart")')

root_state = statechart.add_node("Root", "Node")
root_state.set_property("script", 'ExtResource("5_compound_state")')
root_state.set_property("initial_state", 'NodePath("Idle")')

idle_state = root_state.add_node("Idle", "Node")
idle_state.set_property("script", 'ExtResource("6_atomic_state")')

dragging_state = root_state.add_node("Dragging", "Node")
dragging_state.set_property("script", 'ExtResource("6_atomic_state")')

# FollowMouseUIComponent (挂载在 Dragging 下)
follow_mouse = dragging_state.add_node("FollowMouseUI", "Node")
follow_mouse.set_property("script", 'ExtResource("7_follow_mouse")')

# Transitions
idle_to_drag = idle_state.add_node("ToDragging", "Node")
idle_to_drag.set_property("script", 'ExtResource("8_transition")')
idle_to_drag.set_property("to", f'NodePath("{idle_to_drag.get_relative_path_to(dragging_state)}")')
idle_to_drag.set_property("event", '&"drag_start"')

drag_to_idle = dragging_state.add_node("ToIdle", "Node")
drag_to_idle.set_property("script", 'ExtResource("8_transition")')
drag_to_idle.set_property("to", f'NodePath("{drag_to_idle.get_relative_path_to(idle_state)}")')
drag_to_idle.set_property("event", '&"drag_end"')

# DraggableItemComponent
draggable = test_item.add_node("Draggable", "Node")
draggable.set_property("script", 'ExtResource("9_draggable")')

# GridShapeComponent
shape = test_item.add_node("Shape", "Node")
shape.set_property("script", 'ExtResource("10_shape")')

# SynergyComponent
synergy = test_item.add_node("Synergy", "Node")
synergy.set_property("script", 'ExtResource("11_synergy")')

# UITweenInteractComponent
tween_interact = test_item.add_node("TweenInteract", "Node")
tween_interact.set_property("script", 'ExtResource("12_tween")')

# VisualContainer (视觉目标)
visual_container = test_item.add_control("VisualContainer")
visual_container.set_property("layout_mode", 2)
visual_container.set_property("size_flags_horizontal", 4)
visual_container.set_property("size_flags_vertical", 4)

# 物品图标
item_icon = visual_container.add_texture_rect("ItemIcon")
item_icon.set_property("layout_mode", 2)
item_icon.set_property("custom_minimum_size", "Vector2(64, 64)")
item_icon.set_property("texture", 'ExtResource("13_icon")')
item_icon.set_property("expand_mode", 1)
item_icon.set_property("stretch_mode", 5)

# 星星容器
star_container = visual_container.add_control("StarContainer")
star_container.set_property("layout_mode", 2)

star1 = star_container.add_texture_rect("Star1")
star1.set_property("layout_mode", 2)
star1.set_property("custom_minimum_size", "Vector2(16, 16)")
star1.set_property("modulate", "Color(0.5, 0.5, 0.5, 1)")  # 灰色

star2 = star_container.add_texture_rect("Star2")
star2.set_property("layout_mode", 2)
star2.set_property("custom_minimum_size", "Vector2(16, 16)")
star2.set_property("modulate", "Color(0.5, 0.5, 0.5, 1)")  # 灰色

# 说明文本
vbox.add_label("Instructions", 
               text="Left Click: Drag | Right Click: Rotate | Test the backpack system", 
               align="center", 
               font_size=16)

# 保存场景
ui.save("3d-practice/Scenes/BackpackTest.tscn")
print("✓ 背包测试场景已生成: 3d-practice/Scenes/BackpackTest.tscn")
