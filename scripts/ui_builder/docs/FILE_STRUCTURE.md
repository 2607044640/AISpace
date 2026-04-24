# UI Builder 文件结构说明

## 目录结构

```
ui_builder/
├── generators/                  # 场景生成器
│   └── godot_ui_builder.py
├── tscn_editor_tools/           # TscnEditor核心库
│   ├── __init__.py
│   ├── parser.py
│   ├── node_tree.py
│   ├── pretty_printer.py
│   ├── reader.py
│   ├── editor.py
│   └── types.py
├── docs/                        # 文档
│   ├── README.md
│   ├── EDITOR_USAGE.md
│   ├── FILE_STRUCTURE.md
│   ├── IMPORTANT_PARAMETERS.md
│   └── TEST_RESULTS.md
├── tests/                       # 测试脚本
│   ├── test_runner.py
│   ├── test_parser.py
│   ├── test_pretty_printer.py
│   ├── test_reader.py
│   ├── test_editor.py
│   └── ...
├── tools/                       # 分析和验证工具
│   ├── analyze_option_components.py
│   ├── example_reader_usage.py
│   ├── validate_settings_menu.py
│   └── validate_with_godot.py
└── test_data/                   # 测试数据
    ├── simple_scene.tscn
    ├── nested_test.tscn
    └── batch_test.tscn
```

## 核心文件分类

### 1. 场景生成器 (Scene Generator)
**位置:** `generators/`
- `godot_ui_builder.py` - UI场景生成器，从零创建.tscn文件

### 2. TscnEditor 核心库 (Core Library)
**位置:** `tscn_editor_tools/`

**用途:** 读取和修改现有.tscn文件

**文件:**
- `parser.py` - 解析.tscn文本格式为结构化数据
- `node_tree.py` - 内部树表示，带高效索引
- `pretty_printer.py` - 将Node_Tree格式化回.tscn文本
- `reader.py` - 只读查询API (TscnReader类)
- `editor.py` - 修改API (TscnEditor类)
- `types.py` - 类型定义 (Node, Color, Vector2, ExtResource等)
- `__init__.py` - 包初始化

**关键特性:**
- 直接修改原文件 (`editor.save()` 覆盖原文件)
- 保留所有元数据 (unique_id, UID, 格式)
- 自动转换Python list为PackedStringArray
- Round-trip保证 (Parse → Modify → Save → Parse)

### 3. 文档 (Documentation)
**位置:** `docs/`
- `README.md` - 基本使用说明
- `EDITOR_USAGE.md` - TscnEditor详细用法
- `FILE_STRUCTURE.md` - 本文件
- `IMPORTANT_PARAMETERS.md` - 重要参数说明
- `TEST_RESULTS.md` - 测试结果记录

### 4. 测试脚本 (Test Scripts)
**位置:** `tests/`
**保留原因:** 验证库功能，回归测试

- `test_runner.py` - 测试运行器
- `test_parser.py` - Parser测试
- `test_pretty_printer.py` - Pretty_Printer测试
- `test_reader.py` - Reader基础测试
- `test_editor.py` - Editor基础测试
- 其他test_*.py文件

### 5. 分析和验证工具 (Analysis & Validation Tools)
**位置:** `tools/`
**保留原因:** 调试和验证工具

- `analyze_option_components.py` - 分析OptionComponent结构
- `example_reader_usage.py` - Reader使用示例
- `validate_settings_menu.py` - 验证SettingsMenu结构
- `validate_with_godot.py` - Godot验证工具

### 6. 测试数据 (Test Data)
**位置:** `test_data/`
- `simple_scene.tscn` - 简单测试场景
- `nested_test.tscn` - 嵌套结构测试
- `batch_test.tscn` - 批量操作测试

## 使用指南

### 生成新场景
```python
from godot_ui_builder import UIBuilder
ui = UIBuilder("MyScene")
# ... 构建场景
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

### 读取场景结构
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from tscn_editor_tools import TscnReader

reader = TscnReader("path/to/scene.tscn")
print(reader.print_tree_view())
```

## 导入路径说明

**从根目录脚本导入:**
```python
from tscn_editor_tools import TscnReader, TscnEditor
```

**从子文件夹脚本导入 (tests/, tools/):**
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))  # 返回上级目录

from tscn_editor_tools import TscnReader, TscnEditor
```

## 文件清理规则

### 应该删除的文件类型:
- 一次性修改脚本 (如 `fix_*.py`, `modify_*.py`)
- 临时测试输出 (如 `*_Test.tscn`)
- 临时读取脚本 (如 `read_*.py`)

### 应该保留的文件类型:
- 核心库文件 (`tscn_editor_tools/`)
- 生成器 (`godot_ui_builder.py`)
- 文档 (`docs/*.md`)
- 测试脚本 (`tests/test_*.py`)
- 测试数据 (`test_data/*.tscn`)
- 分析工具 (`tools/*.py`)

## 关键概念

### TscnEditor vs UIBuilder
- **UIBuilder:** 从零生成新场景，适合创建完整UI
- **TscnEditor:** 修改现有场景，适合调整属性、添加节点

### 直接修改 vs 生成新文件
- **默认行为:** `editor.save()` 直接覆盖原文件
- **生成新文件:** `editor.save("new_path.tscn")` 仅在需要时使用

### 数组格式自动转换
- Python: `["item1", "item2"]`
- Godot: `PackedStringArray("item1", "item2")`
- TscnEditor自动处理转换
