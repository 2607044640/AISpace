# Godot UI Builder

快速开始指南和文件结构说明。

## 快速开始

### 生成新UI场景
```python
from godot_ui_builder import UIBuilder

ui = UIBuilder("MyMenu", scene_uid="uid://...")
root = ui.create_control("Control", fullscreen=True)
# ... 构建UI
ui.save("output.tscn")
```

### 修改现有场景
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from tscn_editor_tools import TscnEditor

editor = TscnEditor("path/to/scene.tscn")
editor.update_property("NodeName", "property", value)
editor.save()  # 直接覆盖原文件
```

## 文件结构

```
ui_builder/
 godot_ui_builder.py       # UI场景生成器
 tscn_editor_tools/         # 核心库（读取/修改.tscn）
 docs/                      # 完整文档
 tests/                     # 测试脚本
 tools/                     # 分析和验证工具
 test_data/                 # 测试数据
```

## 文档

- **docs/README.md** - 基本使用说明
- **docs/FILE_STRUCTURE.md** - 详细文件结构
- **docs/EDITOR_USAGE.md** - TscnEditor详细用法
- **AISpace/.kiro/steering/GodotUIBuilder.md** - 完整API参考

## 核心概念

- **UIBuilder**: 从零生成新场景
- **TscnEditor**: 修改现有场景（直接覆盖原文件）
- **TscnReader**: 只读查询场景结构

## 验证流程

生成或修改场景后，必须验证：
```python
mcp_godot_launch_editor(projectPath="c:/Godot/3d-practice")
# 在Godot中打开场景文件检查错误
```
