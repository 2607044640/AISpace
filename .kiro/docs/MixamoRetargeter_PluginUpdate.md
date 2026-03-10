---
inclusion: manual
---

# Mixamo Animation Retargeter 插件修复与改进

## 插件信息
- **位置**: `addons/mixamo_animation_retargeter/`
- **版本**: Godot 4.6.1 stable mono
- **来源**: [GitHub](https://github.com/RaidTheory/Godot-Mixamo-Animation-Retargeter)

---

## 修复: Godot 4.6 兼容性

**问题**: 右键菜单无反应，报错 `Cannot call method 'get_root' on a null value`

**原因**: Godot 4.6改变了FileSystemDock内部结构

**解决**: 添加递归查找Tree节点的fallback：

```gdscript
static func find_tree_recursive(node: Node) -> Tree:
    if node is Tree:
        return node
    for child in node.get_children():
        var result = find_tree_recursive(child)
        if result != null:
            return result
    return null
```

---

## 新增: 默认导出路径

**实现**:

```gdscript
const DEFAULT_EXPORT_PATH = "res://Animations/AnimationRes/"

func _ensure_export_directory_exists() -> void:
    var dir = DirAccess.open("res://")
    if dir and not dir.dir_exists(DEFAULT_EXPORT_PATH):
        dir.make_dir_recursive(DEFAULT_EXPORT_PATH)

func _show_save_dialog(fbx_paths: Array) -> void:
    var file_dialog = EditorFileDialog.new()
    file_dialog.current_dir = DEFAULT_EXPORT_PATH
    file_dialog.current_path = DEFAULT_EXPORT_PATH
    # ...
```

**效果**:
- 自动创建 `Animations/AnimationRes/` 目录
- 对话框默认打开到该目录
- 直接点击"选择当前文件夹"即可

---

## 使用流程

1. 右键FBX文件 → "Retarget Mixamo Animation(s)"
2. 对话框自动打开到默认路径
3. 点击"选择当前文件夹"或选择其他路径
4. 动画导出为 `.res` 文件（自动转snake_case）

**示例**: `Fast Run.fbx` → `fast_run.res`

---

## 与动画系统集成

```csharp
// Quick Test模式
[Export] public Animation IdleAnimation;   // 拖入 idle.res
[Export] public Animation RunAnimation;    // 拖入 run.res
[Export] public Animation SprintAnimation; // 拖入 fast_run.res
```

AnimationSet自动设置循环：
- 移动动画（Idle/Run/Sprint）→ Linear循环
- 一次性动画（Jump/Attack）→ 不循环

---

## 故障排除

**右键菜单无选项**:
- 项目 → 项目设置 → 插件 → 确认已启用
- 重启Godot编辑器

**动画无法播放**:
- 检查Skeleton名称（插件默认"Skeleton"）
- 确认骨骼结构与Mixamo标准一致

**导出路径错误**:
- 修改 `DEFAULT_EXPORT_PATH` 常量
- 手动选择正确路径

---

## 插件配置的导入设置

```gdscript
# 骨骼重定向
subresources["nodes"]["PATH:Skeleton3D"]["retarget/bone_map"] = 
    load("res://addons/mixamo_animation_retargeter/mixamo_bone_map.tres")
subresources["nodes"]["PATH:Skeleton3D"]["retarget/bone_renamer/unique_node/skeleton_name"] = "Skeleton"

# 动画导出
subresources["animations"]["mixamo_com"]["save_to_file/enabled"] = true
subresources["animations"]["mixamo_com"]["save_to_file/path"] = "res://Animations/AnimationRes/animation_name.res"
subresources["animations"]["mixamo_com"]["settings/loop_mode"] = 0
```

---

## 修改记录

**2026-03-07**:
- 修复Godot 4.6兼容性（find_tree_recursive fallback）
- 新增默认导出路径功能
- 自动创建导出目录
