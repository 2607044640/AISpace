"""
生成敌人场景 - 飞行模式可被打断，强制进入地面模式3秒

状态设计：
- Movement维度：Ground(地面) 和 Fly(飞行) 互斥
- 飞行时可被打断(on_interrupted事件) -> 进入地面模式
- 地面模式3秒后自动恢复飞行

组件复用：
- FlyMovementComponent (from 3d-practice/addons/A1MyAddon/CoreComponents)
- GroundMovementComponent (from 3d-practice/addons/A1MyAddon/CoreComponents)
"""

import sys
import os

# 添加builder路径
sys.path.insert(0, os.path.dirname(__file__))
from godot_statechart_builder import StateChartBuilder

def generate_enemy_scene():
    # 创建敌人实体
    builder = StateChartBuilder(
        entity_name="Enemy",
        entity_type="CharacterBody3D",
        entity_script_path="res://B1Scripts/Enemy.cs"
    )
    
    # 创建StateChart
    statechart = builder.create_entity_with_statechart()
    
    # Movement维度 - 初始状态为飞行
    movement = statechart.add_compound_state("Movement", initial_state="Fly")
    
    # 飞行状态 - 使用A1MyAddon的FlyMovementComponent
    fly = movement.add_atomic_state("Fly")
    fly.add_component(
        "FlyMovement", 
        "res://addons/A1MyAddon/CoreComponents/FlyMovementComponent.cs"
    )
    
    # 地面状态 - 使用A1MyAddon的GroundMovementComponent
    ground = movement.add_atomic_state("Ground")
    ground.add_component(
        "GroundMovement", 
        "res://addons/A1MyAddon/CoreComponents/GroundMovementComponent.cs"
    )
    
    # 转换：飞行 -> 地面 (被打断)
    fly.add_transition(
        name="OnInterrupted",
        to_state=ground,
        event="on_interrupted"
    )
    
    # 转换：地面 -> 飞行 (3秒后自动恢复)
    ground.add_transition(
        name="AutoRecover",
        to_state=fly,
        event="",  # 空事件表示自动转换
        delay=3.0  # 3秒延迟
    )
    
    # 打印结构验证
    print("=== Enemy StateChart Structure ===")
    builder.generate_tree_view()
    print("\n=== Transitions ===")
    print("Fly --[on_interrupted]--> Ground")
    print("Ground --[auto, 3s delay]--> Fly")
    print("\n=== Components (Reused from A1MyAddon) ===")
    print("- FlyMovementComponent")
    print("- GroundMovementComponent")
    
    # 保存场景
    output_path = os.path.join(os.path.dirname(__file__), "../../../Scenes/Enemy.tscn")
    builder.save(output_path)
    print(f"\n✓ Scene saved to: res://Scenes/Enemy.tscn")
    
    return builder

if __name__ == "__main__":
    generate_enemy_scene()
