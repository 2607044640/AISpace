"""
生成完整的游戏设置UI - 基于用户提供的截图
包含：基础设置区域和游戏设置区域，使用所有component prefabs
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from godot_ui_builder import UIBuilder


def create_complete_settings_ui():
    """创建完整的游戏设置UI"""
    
    ui = UIBuilder("CompleteGameSettings")
    
    # 1. 根节点（全屏）
    root = ui.create_control("Control", fullscreen=True)
    
    # 2. 背景
    root.add_color_rect("Background", color=(0.1, 0.15, 0.1, 1), use_anchors=True)
    
    # 3. 主边距容器
    margin = root.add_margin_container("MainMargin", uniform=30, use_anchors=True,
                                       vertical_margin=50, horizontal_margin=100)
    margin.set_property("anchors_preset", 15)
    margin.set_property("anchor_right", 1.0)
    margin.set_property("anchor_bottom", 1.0)
    margin.set_property("grow_horizontal", 2)
    margin.set_property("grow_vertical", 2)
    
    # 4. 滚动容器（支持鼠标滚轮滚动）
    scroll = margin.add_scroll_container("ScrollContainer", 
                                         horizontal_scroll=0,  # 禁用水平滚动
                                         vertical_scroll=2,    # 总是显示垂直滚动条
                                         follow_focus=True)
    
    # 5. 主面板
    panel = scroll.add_panel_container("MainPanel")
    inner_margin = panel.add_margin_container("InnerMargin", uniform=40)
    
    # 6. 主垂直布局
    main_vbox = inner_margin.add_vbox("MainVBox", separation=30)
    
    # === 顶部标题栏 ===
    title_hbox = main_vbox.add_hbox("TitleBar", separation=20)
    title_hbox.add_button("BackButton", text="返回", size_flags_h=4)
    title_hbox.add_label("TitleSpacer", text="", size_flags_h=3)  # 占位符
    title_hbox.add_button("SaveButton", text="保存设置", size_flags_h=4)
    title_hbox.add_button("ResetAllButton", text="重置全部", size_flags_h=4)
    
    main_vbox.add_separator("TitleSep", separation=20)
    
    # === 基础设置区域 ===
    basic_section = main_vbox.add_vbox("BasicSettingsSection", separation=15)
    basic_section.add_label("BasicSettingsTitle", text="基础设置", font_size=28)
    
    # 使用DropdownComponent - 分辨率
    basic_section.add_instance("ResolutionSetting",
                              scene_path="res://A1UIScenes/UIComponents/DropdownComponent.tscn")
    
    # 使用OptionComponent - 显示模式
    basic_section.add_instance("DisplayModeSetting",
                              scene_path="res://A1UIScenes/UIComponents/OptionComponent.tscn")
    
    # 使用OptionComponent - 语言
    basic_section.add_instance("LanguageSetting",
                              scene_path="res://A1UIScenes/UIComponents/OptionComponent.tscn")
    
    # 使用SliderComponent - 音乐音量
    basic_section.add_instance("MusicVolumeSetting",
                              scene_path="res://A1UIScenes/UIComponents/SliderComponent.tscn")
    
    # 使用SliderComponent - 音效音量
    basic_section.add_instance("SoundVolumeSetting",
                              scene_path="res://A1UIScenes/UIComponents/SliderComponent.tscn")
    
    main_vbox.add_separator("SectionSep", separation=30)
    
    # === 游戏设置区域 ===
    game_section = main_vbox.add_vbox("GameSettingsSection", separation=15)
    game_section.add_label("GameSettingsTitle", text="游戏设置", font_size=28)
    
    # 第一行：3个预览框
    preview_row1 = game_section.add_hbox("PreviewRow1", separation=20)
    
    # 预览框1
    preview1_vbox = preview_row1.add_vbox("Preview1VBox", separation=10)
    preview1_vbox.set_property("size_flags_horizontal", 3)
    preview1_vbox.add_instance("Preview1Toggle",
                              scene_path="res://A1UIScenes/UIComponents/ToggleComponent.tscn")
    preview1_panel = preview1_vbox.add_panel_container("Preview1Panel")
    preview1_panel.set_property("custom_minimum_size", "Vector2(280, 180)")
    
    # 预览框2
    preview2_vbox = preview_row1.add_vbox("Preview2VBox", separation=10)
    preview2_vbox.set_property("size_flags_horizontal", 3)
    preview2_vbox.add_instance("Preview2Toggle",
                              scene_path="res://A1UIScenes/UIComponents/ToggleComponent.tscn")
    preview2_panel = preview2_vbox.add_panel_container("Preview2Panel")
    preview2_panel.set_property("custom_minimum_size", "Vector2(280, 180)")
    
    # 预览框3
    preview3_vbox = preview_row1.add_vbox("Preview3VBox", separation=10)
    preview3_vbox.set_property("size_flags_horizontal", 3)
    preview3_vbox.add_instance("Preview3Toggle",
                              scene_path="res://A1UIScenes/UIComponents/ToggleComponent.tscn")
    preview3_panel = preview3_vbox.add_panel_container("Preview3Panel")
    preview3_panel.set_property("custom_minimum_size", "Vector2(280, 180)")
    
    # 第二行：3个预览框
    preview_row2 = game_section.add_hbox("PreviewRow2", separation=20)
    
    # 预览框4
    preview4_vbox = preview_row2.add_vbox("Preview4VBox", separation=10)
    preview4_vbox.set_property("size_flags_horizontal", 3)
    preview4_vbox.add_instance("Preview4Toggle",
                              scene_path="res://A1UIScenes/UIComponents/ToggleComponent.tscn")
    preview4_panel = preview4_vbox.add_panel_container("Preview4Panel")
    preview4_panel.set_property("custom_minimum_size", "Vector2(280, 180)")
    
    # 预览框5
    preview5_vbox = preview_row2.add_vbox("Preview5VBox", separation=10)
    preview5_vbox.set_property("size_flags_horizontal", 3)
    preview5_vbox.add_instance("Preview5Toggle",
                              scene_path="res://A1UIScenes/UIComponents/ToggleComponent.tscn")
    preview5_panel = preview5_vbox.add_panel_container("Preview5Panel")
    preview5_panel.set_property("custom_minimum_size", "Vector2(280, 180)")
    
    # 预览框6
    preview6_vbox = preview_row2.add_vbox("Preview6VBox", separation=10)
    preview6_vbox.set_property("size_flags_horizontal", 3)
    preview6_vbox.add_instance("Preview6Toggle",
                              scene_path="res://A1UIScenes/UIComponents/ToggleComponent.tscn")
    preview6_panel = preview6_vbox.add_panel_container("Preview6Panel")
    preview6_panel.set_property("custom_minimum_size", "Vector2(280, 180)")
    
    # === 底部按钮栏 ===
    bottom_bar = main_vbox.add_hbox("BottomBar", separation=20)
    bottom_bar.add_button("ConfigButton", text="配置", size_flags_h=3)
    bottom_bar.add_button("DrawButton", text="抽奖", size_flags_h=3)
    bottom_bar.add_button("EncyclopediaButton", text="图鉴", size_flags_h=3)
    bottom_bar.add_button("SettingsButton", text="设置", size_flags_h=3)
    bottom_bar.add_button("StartGameButton", text="开始游戏", size_flags_h=3)
    
    # 生成树状图
    print("=" * 80)
    print("Complete Game Settings UI Structure:")
    print("=" * 80)
    print(ui.generate_tree_view())
    print("=" * 80)
    
    # 保存
    output_path = "C:/Godot/3d-practice/A1UIScenes/CompleteGameSettings.tscn"
    ui.save(output_path)
    
    return ui


if __name__ == "__main__":
    create_complete_settings_ui()
