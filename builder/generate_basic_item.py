"""
Generate BasicItem.tscn - Minimal clickable item template
用途：最小化模板，只有 StateChart 和点击反应，用于快速扩展
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


def generate_basic_item():
    """生成最小化的可点击物品模板"""
    
    # 创建场景
    scene = TscnBuilder("BasicItem", "Control")
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
        color="Color(0.2, 0.5, 0.8, 0.5)",  # 半透明蓝色
        mouse_filter=0,  # Stop - 接收鼠标输入
        unique_name_in_owner=True
    )
    
    # 添加 StateChart
    statechart = StateChartBuilder(scene, parent=".")
    statechart.add_statechart("StateChart")
    
    # 创建简单的 Idle/Clicked 状态机
    statechart.add_compound_state("Root", parent="StateChart", initial_state="Idle")
    statechart.add_atomic_state("Idle", parent="Root")
    statechart.add_atomic_state("Clicked", parent="Root")
    
    # 添加转换
    statechart.add_transition(
        "ToDragging",
        from_state="Idle",
        to_state="Clicked",
        event="clicked",
        delay=0.0
    )
    
    statechart.add_transition(
        "ToIdle",
        from_state="Clicked",
        to_state="Idle",
        event="reset",
        delay=0.5  # 0.5秒后自动回到 Idle
    )
    
    # 解析初始状态
    statechart.resolve_initial_states()
    
    # 生成场景
    # 从 AISpace/builder 到 TetrisBackpack
    workspace_root = os.path.dirname(os.path.dirname(current_dir))
    output_path = os.path.join(workspace_root, "TetrisBackpack", "addons", "A1TetrisBackpack", "Items", "BasicItem.tscn")
    scene.save(output_path)
    
    print("\n=== BasicItem.tscn 生成完成 ===")
    print("用途：最小化模板，只有点击状态切换")
    print("扩展示例：")
    print("  - 添加 C# 脚本监听 StateChart 信号")
    print("  - Clicked 状态下改变颜色/播放动画")
    print("  - 添加更多状态（如 Equipped, Consumed）")
    print("\n节点树：")
    print(scene.generate_tree_view())


if __name__ == "__main__":
    generate_basic_item()
