"""
测试 TscnReader 和 TscnEditor 工具
1. 读取 SettingsMenuV2_Fixed.tscn 结构
2. 在 Game 菜单添加 PlayerCount (DropdownComponent)
3. 修改 NumberFormat 的选项
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from tscn_editor_tools.reader import TscnReader
from tscn_editor_tools.editor import TscnEditor

def main():
    script_dir = Path(__file__).parent.resolve()
    workspace_root = script_dir.parent.parent.parent.parent
    tscn_path = workspace_root / "3d-practice" / "A1UIScenes" / "SettingsMenuV2_Fixed.tscn"
    
    print("="*70)
    print("步骤 1: 使用 TscnReader 读取场景结构")
    print("="*70)
    
    # 读取场景
    reader = TscnReader(str(tscn_path))
    
    # 显示树形结构
    print("\n完整场景树形结构：")
    print(reader.print_tree_view())
    
    # 查找 Game 菜单内容
    print("\n" + "="*70)
    print("Game 菜单当前内容：")
    print("="*70)
    
    game_content_path = "MainMargin_MarginContainer/MainVBox_VBoxContainer/Tabs_TabContainer/Game/GameMargin_MarginContainer/GameContent_VBoxContainer"
    game_children = reader.tree.get_children(game_content_path)
    
    for child in game_children:
        child_path = reader.tree.build_full_path(child)
        print(f"\n节点: {child.name}")
        print(f"  类型: {child.node_type}")
        print(f"  是否为实例: {child.is_instance}")
        if child.is_instance:
            print(f"  场景路径: {child.scene_path}")
        print(f"  属性:")
        for key, value in child.properties.items():
            if not key.startswith('_'):
                print(f"    {key} = {value}")
    
    # 查看 NumberFormat 节点
    print("\n" + "="*70)
    print("NumberFormat 节点详情：")
    print("="*70)
    
    number_format_path = f"{game_content_path}/NumberFormat"
    number_format = reader.tree.get_node_by_path(number_format_path)
    if number_format:
        print(f"节点名: {number_format.name}")
        print(f"类型: {number_format.node_type}")
        print(f"场景路径: {number_format.scene_path}")
        print(f"属性:")
        for key, value in number_format.properties.items():
            if not key.startswith('_'):
                print(f"  {key} = {value}")
    
    # ===== 步骤 2: 使用 TscnEditor 进行修改 =====
    print("\n" + "="*70)
    print("步骤 2: 使用 TscnEditor 进行修改")
    print("="*70)
    
    editor = TscnEditor(str(tscn_path))
    
    # 2.1 添加 PlayerCount DropdownComponent
    print("\n2.1 添加 PlayerCount (玩家数量) DropdownComponent")
    
    try:
        new_node = editor.add_scene_instance(
            name="PlayerCount",
            scene_path="res://A1UIScenes/UIComponents/DropdownComponent.tscn",
            parent_path=game_content_path,
            scene_uid="uid://0st2knyluaer",
            properties={
                "layout_mode": 2,
                "LabelText": "Player Count",
                "Items": ["1", "2", "3", "4"],
                "DefaultIndex": 0
            }
        )
        print(f"✅ 成功添加 PlayerCount 节点")
        print(f"   unique_id: {new_node.unique_id}")
        print(f"   属性: {[k for k in new_node.properties.keys() if not k.startswith('_')]}")
    except Exception as e:
        print(f"❌ 添加失败: {e}")
    
    # 2.2 修改 NumberFormat 的选项
    print("\n2.2 修改 NumberFormat 的选项")
    
    try:
        # 更新 Items 属性
        editor.update_property(number_format_path, "Items", ["23", "43", "08293"])
        print(f"✅ 成功修改 NumberFormat 的 Items 为: ['23', '43', '08293']")
        
        # 更新 DefaultIndex
        editor.update_property(number_format_path, "DefaultIndex", 0)
        print(f"✅ 成功设置 DefaultIndex 为: 0")
    except Exception as e:
        print(f"❌ 修改失败: {e}")
    
    # ===== 步骤 3: 保存并验证 =====
    print("\n" + "="*70)
    print("步骤 3: 保存并验证")
    print("="*70)
    
    output_path = tscn_path.parent / "SettingsMenuV2_Test.tscn"
    editor.save(str(output_path))
    print(f"\n✅ 已保存到: {output_path}")
    
    # 重新读取验证
    print("\n验证修改结果：")
    reader2 = TscnReader(str(output_path))
    
    # 验证 PlayerCount
    player_count = reader2.tree.get_node_by_path(f"{game_content_path}/PlayerCount")
    if player_count:
        print(f"\n✅ PlayerCount 节点存在")
        print(f"   LabelText: {player_count.properties.get('LabelText')}")
        print(f"   Items: {player_count.properties.get('Items')}")
        print(f"   DefaultIndex: {player_count.properties.get('DefaultIndex')}")
    else:
        print(f"\n❌ PlayerCount 节点未找到")
    
    # 验证 NumberFormat
    number_format2 = reader2.tree.get_node_by_path(number_format_path)
    if number_format2:
        print(f"\n✅ NumberFormat 节点存在")
        print(f"   Items: {number_format2.properties.get('Items')}")
        print(f"   DefaultIndex: {number_format2.properties.get('DefaultIndex')}")
    else:
        print(f"\n❌ NumberFormat 节点未找到")
    
    # 显示 Game 菜单更新后的内容
    print("\n" + "="*70)
    print("Game 菜单更新后的内容：")
    print("="*70)
    
    game_children2 = reader2.tree.get_children(game_content_path)
    for child in game_children2:
        print(f"  - {child.name} ({child.node_type})")
        if child.is_instance:
            label_text = child.properties.get('LabelText', 'N/A')
            print(f"      LabelText: {label_text}")
    
    print("\n" + "="*70)
    print("✅ 测试完成！")
    print("="*70)
    print(f"\n测试文件: {output_path}")
    print("请在 Godot 中打开验证")

if __name__ == "__main__":
    main()
