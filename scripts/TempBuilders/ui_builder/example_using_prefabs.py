"""
示例：使用prefab组件构建设置界面
展示如何实例化可重用的UI组件
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from godot_ui_builder import UIBuilder


def create_settings_with_prefabs():
    """使用prefab创建设置界面"""
    
    ui = UIBuilder("SettingsWithPrefabs")
    
    # 1. 根节点
    root = ui.create_control("Control", fullscreen=True)
    
    # 2. 背景
    root.add_color_rect("Background", use_anchors=True)
    
    # 3. 主边距
    margin = root.add_margin_container("MainMargin", uniform=30, use_anchors=True,
                                       vertical_margin=70, horizontal_margin=128)
    margin.set_property("anchors_preset", 15)
    margin.set_property("anchor_right", 1.0)
    margin.set_property("anchor_bottom", 1.0)
    margin.set_property("grow_horizontal", 2)
    margin.set_property("grow_vertical", 2)
    
    # 4. 面板
    panel = margin.add_panel_container("MainPanel")
    inner_margin = panel.add_margin_container("InnerMargin", uniform=33)
    
    # 5. 主布局
    vbox = inner_margin.add_vbox("MainVBox", separation=20)
    
    # 标题
    vbox.add_label("Title", text="游戏设置", align="center", font_size=32)
    vbox.add_separator("TitleSep", separation=30)
    
    # === 使用prefab实例 ===
    
    # 分辨率选项（使用OptionComponent prefab）
    vbox.add_instance("ResolutionOption", 
                     scene_path="res://A1UIScenes/UIComponents/OptionComponent.tscn")
    
    # 音乐音量滑块（使用SliderComponent prefab）
    vbox.add_instance("MusicVolumeSlider",
                     scene_path="res://A1UIScenes/UIComponents/SliderComponent.tscn")
    
    # 音效音量滑块
    vbox.add_instance("SoundVolumeSlider",
                     scene_path="res://A1UIScenes/UIComponents/SliderComponent.tscn")
    
    # 全屏开关（使用ToggleComponent prefab）
    vbox.add_instance("FullscreenToggle",
                     scene_path="res://A1UIScenes/UIComponents/ToggleComponent.tscn")
    
    # VSync开关
    vbox.add_instance("VSyncToggle",
                     scene_path="res://A1UIScenes/UIComponents/ToggleComponent.tscn")
    
    # 生成树状图
    print("=" * 80)
    print("Settings With Prefabs Structure:")
    print("=" * 80)
    print(ui.generate_tree_view())
    print("=" * 80)
    
    # 保存
    output_path = "C:/Godot/3d-practice/A1UIScenes/SettingsWithPrefabs.tscn"
    ui.save(output_path)
    
    return ui


if __name__ == "__main__":
    create_settings_with_prefabs()
