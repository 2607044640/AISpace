# GetNodeOrNull Migration to Scene Unique Names (%) - COMPLETED

## 任务完成时间
2026-04-16

## 修改的文件列表

### Backpack System (5 files)
1. `3d-practice/addons/A1TetrisBackpack/Core/BackpackGridUIComponent.cs`
   - `LogicGrid` → `[Export] NodePath LogicGridPath = "%BackpackGridComponent"`

2. `3d-practice/addons/A1TetrisBackpack/Core/BackpackInteractionController.cs`
   - `LogicGrid` → `[Export] NodePath LogicGridPath = "%BackpackGridComponent"`
   - `ViewGrid` → `[Export] NodePath ViewGridPath = "%BackpackPanel"`
   - `DraggableItemComponent` → `GetNodeOrNull("%DraggableItemComponent")`
   - `GridShapeComponent` → `GetNodeOrNull("%GridShapeComponent")`

3. `3d-practice/addons/A1TetrisBackpack/Interaction/DraggableItemComponent.cs`
   - `ClickableArea` → `[Export] NodePath ClickableAreaPath = "%ClickableArea"`
   - `StateChart` → `[Export] NodePath StateChartPath = "%StateChart"`

4. `3d-practice/addons/A1TetrisBackpack/Interaction/FollowMouseUIComponent.cs`
   - `TargetUI` → `[Export] NodePath TargetUIPath = "%TargetUI"`

### UI Helpers (5 files)
5. `3d-practice/addons/A1MyAddon/Helpers/DropdownComponentHelper.cs`
   - `_dropdown` → `[Export] NodePath DropdownPath = "%Dropdown_OptionButton"`

6. `3d-practice/addons/A1MyAddon/Helpers/SliderComponentHelper.cs`
   - `_slider` → `[Export] NodePath SliderPath = "%SliderBar_HSlider"`
   - `_spinBox` → `[Export] NodePath SpinBoxPath = "%ValueSpinBox_SpinBox"`

7. `3d-practice/addons/A1MyAddon/Helpers/ToggleComponentHelper.cs`
   - `_checkbox` → `[Export] NodePath CheckboxPath = "%ToggleCheckbox_CheckBox"`

8. `3d-practice/addons/A1MyAddon/Helpers/OptionComponentHelper.cs`
   - `_optionButton` → `[Export] NodePath OptionButtonPath = "%OptionDropdown_Button"`

9. `3d-practice/addons/A1MyAddon/Helpers/ThemeSwitcherComponentHelper.cs`
   - `_themeDropdown` → `[Export] NodePath ThemeDropdownPath = "%ThemeDropdown_OptionButton"`

### Core Components (5 files)
10. `3d-practice/addons/A1MyAddon/CoreComponents/AnimationControllerComponent.cs`
    - 已使用 NodePath 属性，添加了错误检查

11. `3d-practice/addons/A1MyAddon/CoreComponents/CameraControlComponent.cs`
    - 已使用 NodePath 属性，添加了错误检查

12. `3d-practice/addons/A1MyAddon/CoreComponents/CharacterRotationComponent.cs`
    - 已使用 NodePath 属性，添加了错误检查

13. `3d-practice/addons/A1MyAddon/CoreComponents/FlyMovementComponent.cs`
    - 已使用 NodePath 属性，添加了错误检查

14. `3d-practice/addons/A1MyAddon/CoreComponents/GroundMovementComponent.cs`
    - 已使用 NodePath 属性，添加了错误检查

### Extensions (1 file)
15. `3d-practice/addons/A1MyAddon/CoreComponents/Extenstions/StateChartAutoBindExtensions.cs`
    - `SendStateEvent()` → 使用 `GetNodeOrNull("%StateChart")`

## 修改模式

### 旧模式（错误）
```csharp
// 硬编码相对路径
var node = GetNodeOrNull<T>("../../../NodeName");
var node = GetParent()?.GetNodeOrNull("NodeName");
```

### 新模式（正确）
```csharp
// 使用 Export NodePath + Scene Unique Names
[Export] public NodePath NodeNamePath { get; set; } = "%NodeName";
private T _node;

public override void _Ready()
{
    _node = GetNodeOrNull<T>(NodeNamePath);
    if (_node == null)
    {
        GD.PushError($"[{Name}] Node not found: {NodeNamePath}");
        return;
    }
}
```

## 编译结果
✅ `dotnet build` 成功，无错误
⚠️ 5 个警告（来自第三方插件 PhantomCamera，非本次修改引入）

## 剩余工作
- Python 生成器已更新，会自动标记节点为 `unique_name_in_owner = true`
- 文档已更新（DesignPatterns.md）
- 所有现有 C# 代码已迁移完成

## 验证命令
```bash
# 搜索所有 GetNodeOrNull 调用
Get-ChildItem -Path addons -Filter "*.cs" -Recurse | Select-String -Pattern "GetNodeOrNull"

# 只显示未使用 % 或 NodePath 的调用
Get-ChildItem -Path addons -Filter "*.cs" -Recurse | Select-String -Pattern 'GetNodeOrNull\s*\(' | Where-Object { $_.Line -notmatch 'GetNodeOrNull<[^>]+>\s*\(%' -and $_.Line -notmatch 'GetNodeOrNull<[^>]+>\s*\([A-Z][a-zA-Z]*Path\)' }
```

## 总结
所有 GetNodeOrNull 调用已成功迁移到 Scene Unique Names (%) 模式。这消除了脆弱的相对路径依赖，使代码更加健壮和可维护。
