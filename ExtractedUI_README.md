# 提取的UI资源说明

## 概述
从OpenSourceGames文件夹中的两个开源Godot游戏项目提取了UI相关资源，已排除所有脚本文件(.gd)。

## 提取的项目

### 1. ExtractedUI_99Managers (足球经理游戏)
来源: `OpenSourceGames/99managers/game`

#### 包含内容:
- **screens/** - 各种游戏界面场景
  - about/ - 关于页面
  - dashboard/ - 仪表板
  - datapack_screen/ - 数据包界面
  - editor/ - 编辑器界面
  - main/ - 主界面 (包含loading_screen)
  - match_screen/ - 比赛界面
  - menu/ - 菜单
  - save_games_screen/ - 存档界面
  - settings/ - 设置界面
  - setup/ - 设置向导
  - splash/ - 启动画面

- **ui_components/** - 可复用UI组件
  - backgrounds/ - 背景组件
  - base/ - 基础组件
  - competitions_tree/ - 比赛树形视图
  - email/ - 邮件组件
  - graphs/ - 图表组件
  - info/ - 信息显示组件
  - morality_indicator/ - 士气指示器
  - overview/ - 概览组件
  - player_list/ - 球员列表
  - profiles/ - 个人资料
  - visual_calendar/ - 可视化日历
  - visual_competitions/ - 可视化比赛
  - visual_contract_negotiation/ - 合同谈判界面
  - visual_finances/ - 财务可视化
  - visual_formation/ - 阵型编辑器
  - visual_global_offer_list/ - 全局报价列表
  - visual_offer_list/ - 报价列表
  - visual_stadium/ - 体育场可视化

- **assets/** - 游戏资源
  - audio/ - 音效文件
  - backgrounds/ - 背景图片
  - fonts/ - 字体文件 (Inter, NotoSansSC, DSEG7, Prompt)
  - icons/ - 图标集合
  - joypad_glyphs/ - 手柄按钮图标
  - player/ - 球员头像资源
  - player_face/ - 球员面部生成资源
  - team_logos/ - 队徽资源

- **themes/** - 主题文件
  - theme_dark.tres - 深色主题
  - theme_light.tres - 浅色主题
  - theme_solarized_dark.tres - Solarized深色
  - theme_solarized_light.tres - Solarized浅色

- **theme_base/** - 主题基础资源
  - button_groups/ - 按钮组
  - label/ - 标签样式和字体设置
  - style_boxes/ - 样式框资源

### 2. ExtractedUI_Librerama (迷你游戏合集)
来源: `OpenSourceGames/librerama`

#### 包含内容:
- **modals/** - 模态对话框
  - modal/ - 基础模态框
  - settings_modal/ - 设置对话框
  - tab_modal/ - 标签页对话框

- **places/** - 游戏场景
  - _assets/ - 场景资源
  - arcade_machine/ - 街机机器
  - intro/ - 介绍场景
  - lobby/ - 大厅场景

- **themes/** - 主题资源
  - _assets/ - 主题资源
  - _resources/ - 主题资源文件
  - arcade/ - 街机风格主题
  - theme_lobby.tres - 大厅主题

- **fonts/** - 字体文件
  - noto_sans_regular.ttf
  - noto_sans_bold.ttf
  - noto_sans_italic.ttf

## 文件类型
提取的文件包括:
- `.tscn` - Godot场景文件
- `.tres` - Godot资源文件 (主题、样式等)
- `.png` / `.svg` - 图像文件
- `.ttf` / `.otf` - 字体文件
- `.ogg` / `.wav` / `.mp3` - 音频文件
- `.import` - Godot导入配置文件

## 使用说明
这些UI资源可以直接在Godot项目中使用:
1. 将需要的文件夹复制到你的Godot项目中
2. 场景文件(.tscn)可以直接在Godot编辑器中打开
3. 主题文件(.tres)可以应用到Control节点
4. 注意: 由于排除了脚本文件，某些场景可能需要重新编写逻辑代码

## 注意事项
- 所有GDScript脚本文件(.gd)已被排除
- 某些场景可能依赖于原项目的脚本逻辑
- 建议参考原项目了解完整的实现方式
- 资源路径可能需要根据你的项目结构进行调整

### 3. ExtractedUI_GameTemplate (Godot游戏模板)
来源: `C:\Users\26070\Downloads\Godot-Game-Template-main`

#### 包含内容:
- **scenes/** - 完整的游戏场景系统
  - credits/ - 制作人员名单 (可滚动版本)
  - end_credits/ - 结束制作人员名单
  - game_scene/ - 游戏场景 (包含关卡和教程系统)
  - loading_screen/ - 加载界面 (包含shader缓存版本)
  - menus/ - 菜单系统
    - level_select_menu/ - 关卡选择菜单
    - main_menu/ - 主菜单 (包含动画版本)
    - options_menu/ - 选项菜单 (音频/游戏/输入/视频设置)
  - opening/ - 开场动画
  - windows/ - 弹窗系统
    - game_won_window/ - 游戏胜利窗口
    - level_lost_window/ - 关卡失败窗口
    - level_won_window/ - 关卡胜利窗口
    - main_menu_credits_window/ - 主菜单制作人员窗口
    - main_menu_options_window/ - 主菜单选项窗口
    - pause_menu_layer/ - 暂停菜单层
    - pause_menu/ - 暂停菜单
    - pause_menu_options_window/ - 暂停菜单选项窗口

- **assets/** - 资源文件
  - git_logo/ - Git标志
  - godot_engine_logo/ - Godot引擎标志
  - plugin_logo/ - 插件标志

- **resources/** - 资源配置
  - themes/ - 主题资源文件

## 原项目链接
- 99 Managers: https://github.com/dulvui/99managers
- Librerama: https://codeberg.org/Yeldham/librerama
- Godot Game Template: https://github.com/crystal-bit/godot-game-template
