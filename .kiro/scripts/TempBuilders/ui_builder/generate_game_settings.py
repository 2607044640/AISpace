"""
生成游戏设置界面 - 基于截图设计
包含：基础设置、游戏设置两个标签页
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from godot_ui_builder import UIBuilder


def create_game_settings_ui():
    """创建游戏设置UI"""
    
    ui = UIBuilder("GameSettings")
    
    # 1. 根节点（全屏）
    root = ui.create_control("Control", fullscreen=True)
    
    # 2. 添加背景（使用锚点填充）
    root.add_color_rect("Background", use_anchors=True)
    
    # 3. 主边距容器（使用MarginContainerHelper，锚点模式）
    margin = root.add_margin_container(
        "MainMargin",
        uniform=30,
        use_anchors=True,
        vertical_margin=70,
        horizontal_margin=128
    )
    margin.set_property("anchors_preset", 15)
    margin.set_property("anchor_right", 1.0)
    margin.set_property("anchor_bottom", 1.0)
    margin.set_property("offset_top", -1.0)
    margin.set_property("offset_bottom", -1.0)
    margin.set_property("grow_horizontal", 2)
    margin.set_property("grow_vertical", 2)
    
    # 4. 主面板
    panel = margin.add_panel_container("MainPanel")
    inner_margin = panel.add_margin_container("InnerMargin", uniform=33)
    
    # 5. 主垂直布局
    main_vbox = inner_margin.add_vbox("MainVBox", separation=20)
    
    # === 顶部标签栏 ===
    tab_bar = main_vbox.add_hbox("TabBar", separation=10)
    tab_bar.add_button("BasicSettingsTab", text="基础设置", size_flags_h=3)
    tab_bar.add_button("GameSettingsTab", text="游戏设置", size_flags_h=3)
    tab_bar.add_button("ExitGameTab", text="退出游戏", size_flags_h=3)
    
    # === 基础设置区域 ===
    basic_section = main_vbox.add_vbox("BasicSettingsSection", separation=15)
    
    # 标题
    basic_section.add_label("BasicSettingsTitle", text="基础设置", font_size=24)
    
    # 分辨率行
    resolution_row = basic_section.add_hbox("ResolutionRow", separation=20)
    resolution_row.add_label("ResolutionLabel", text="分辨率:", min_size=(80, 0), size_flags_h=6)
    resolution_dropdown = resolution_row.add_button("ResolutionDropdown", text="1920x1080:59", size_flags_h=3)
    
    resolution_row.add_label("DisplayModeLabel", text="显示模式:", min_size=(80, 0), size_flags_h=6)
    display_dropdown = resolution_row.add_button("DisplayModeDropdown", text="全屏幕显示", size_flags_h=3)
    
    resolution_row.add_label("LanguageLabel", text="语言:", min_size=(80, 0), size_flags_h=6)
    language_dropdown = resolution_row.add_button("LanguageDropdown", text="中文", size_flags_h=3)
    
    # 音乐音量行
    music_row = basic_section.add_hbox("MusicVolumeRow", separation=20)
    music_row.add_label("MusicVolumeLabel", text="音乐音量:", min_size=(100, 0), size_flags_h=6)
    music_slider = music_row.add_progress_bar("MusicVolumeSlider", value=50, 
                                              size_flags_h=3, size_flags_v=4,
                                              show_percentage=True)
    music_row.add_button("MusicMuteCheckbox", text="静音", size_flags_h=4)
    
    # 音效音量行
    sound_row = basic_section.add_hbox("SoundVolumeRow", separation=20)
    sound_row.add_label("SoundVolumeLabel", text="音效音量:", min_size=(100, 0), size_flags_h=6)
    sound_slider = sound_row.add_progress_bar("SoundVolumeSlider", value=50,
                                              size_flags_h=3, size_flags_v=4,
                                              show_percentage=True)
    sound_row.add_button("SoundMuteCheckbox", text="静音", size_flags_h=4)
    
    # === 游戏设置区域 ===
    game_section = main_vbox.add_vbox("GameSettingsSection", separation=15)
    
    # 标题
    game_section.add_label("GameSettingsTitle", text="游戏设置", font_size=24)
    
    # 第一行：3个预览框
    preview_row1 = game_section.add_hbox("PreviewRow1", separation=15)
    
    # 预览框1
    preview1_vbox = preview_row1.add_vbox("Preview1VBox", separation=5)
    preview1_vbox.set_property("size_flags_horizontal", 3)
    preview1_vbox.add_button("Preview1Checkbox", text="播放背景场景动画", size_flags_h=0)
    preview1_panel = preview1_vbox.add_panel_container("Preview1Panel")
    preview1_panel.set_property("custom_minimum_size", "Vector2(250, 150)")
    preview1_margin = preview1_panel.add_margin_container("Preview1Margin", uniform=5)
    preview1_margin.add_label("Preview1Text", text="预览区域", align="center")
    
    # 预览框2
    preview2_vbox = preview_row1.add_vbox("Preview2VBox", separation=5)
    preview2_vbox.set_property("size_flags_horizontal", 3)
    preview2_vbox.add_button("Preview2Checkbox", text="显示操作提示", size_flags_h=0)
    preview2_panel = preview2_vbox.add_panel_container("Preview2Panel")
    preview2_panel.set_property("custom_minimum_size", "Vector2(250, 150)")
    preview2_margin = preview2_panel.add_margin_container("Preview2Margin", uniform=5)
    preview2_margin.add_label("Preview2Text", text="预览区域", align="center")
    
    # 预览框3
    preview3_vbox = preview_row1.add_vbox("Preview3VBox", separation=5)
    preview3_vbox.set_property("size_flags_horizontal", 3)
    preview3_vbox.add_button("Preview3Checkbox", text="显示警示信息", size_flags_h=0)
    preview3_panel = preview3_vbox.add_panel_container("Preview3Panel")
    preview3_panel.set_property("custom_minimum_size", "Vector2(250, 150)")
    preview3_margin = preview3_panel.add_margin_container("Preview3Margin", uniform=5)
    preview3_margin.add_label("Preview3Text", text="预览区域", align="center")
    
    # 第二行：3个预览框
    preview_row2 = game_section.add_hbox("PreviewRow2", separation=15)
    
    # 预览框4
    preview4_vbox = preview_row2.add_vbox("Preview4VBox", separation=5)
    preview4_vbox.set_property("size_flags_horizontal", 3)
    preview4_vbox.add_button("Preview4Checkbox", text="合成后自动关闭合成页面", size_flags_h=0)
    preview4_panel = preview4_vbox.add_panel_container("Preview4Panel")
    preview4_panel.set_property("custom_minimum_size", "Vector2(250, 150)")
    preview4_margin = preview4_panel.add_margin_container("Preview4Margin", uniform=5)
    preview4_margin.add_label("Preview4Text", text="预览区域", align="center")
    
    # 预览框5
    preview5_vbox = preview_row2.add_vbox("Preview5VBox", separation=5)
    preview5_vbox.set_property("size_flags_horizontal", 3)
    preview5_vbox.add_button("Preview5Checkbox", text="显示防御塔HUD", size_flags_h=0)
    preview5_panel = preview5_vbox.add_panel_container("Preview5Panel")
    preview5_panel.set_property("custom_minimum_size", "Vector2(250, 150)")
    preview5_margin = preview5_panel.add_margin_container("Preview5Margin", uniform=5)
    preview5_margin.add_label("Preview5Text", text="预览区域", align="center")
    
    # 预览框6
    preview6_vbox = preview_row2.add_vbox("Preview6VBox", separation=5)
    preview6_vbox.set_property("size_flags_horizontal", 3)
    preview6_vbox.add_button("Preview6Checkbox", text="显示按钮名称", size_flags_h=0)
    preview6_panel = preview6_vbox.add_panel_container("Preview6Panel")
    preview6_panel.set_property("custom_minimum_size", "Vector2(250, 150)")
    preview6_margin = preview6_panel.add_margin_container("Preview6Margin", uniform=5)
    preview6_margin.add_label("Preview6Text", text="预览区域", align="center")
    
    # === 底部按钮栏 ===
    bottom_bar = main_vbox.add_hbox("BottomBar", separation=20)
    bottom_bar.add_button("ConfigButton", text="配置", size_flags_h=3)
    bottom_bar.add_button("DrawButton", text="抽奖", size_flags_h=3)
    bottom_bar.add_button("EncyclopediaButton", text="图鉴", size_flags_h=3)
    bottom_bar.add_button("SettingsButton", text="设置", size_flags_h=3)
    bottom_bar.add_button("StartGameButton", text="开始游戏", size_flags_h=3)
    
    # 生成树状图
    print("=" * 80)
    print("Game Settings UI Structure:")
    print("=" * 80)
    print(ui.generate_tree_view())
    print("=" * 80)
    
    # 保存到3d-practice项目（使用绝对路径）
    output_path = "C:/Godot/3d-practice/A1UIScenes/GameSettings.tscn"
    ui.save(output_path)
    
    return ui


if __name__ == "__main__":
    create_game_settings_ui()
