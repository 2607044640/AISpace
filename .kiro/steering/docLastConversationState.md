---
inclusion: manual
---

<!-- WARNING: Keep inclusion as 'manual' - do not change to 'always' to save tokens -->

# Last Conversation State
*Updated: 2026-03-11*

## Project Status
- **Engine:** Godot 4.6.1 stable mono
- **Language:** C# only
- **Project Type:** 消消乐+扫雷混合游戏（3D角色控制器）
- **Phase:** 架构重构完成，组件化开发中

## Active Goals
**Next Tasks:**
1. 测试游戏，确保角色移动、跳跃、动画正常
2. 根据需要创建更多实体（Enemy、Box 等）
3. 扩展动画系统或添加新功能

**Reason:** 基础架构已完成，现在可以专注于游戏功能开发

## Critical Context

### 核心架构模式
**Godot.Composition 组件化架构：**
- Entity（实体）：纯容器，只调用 `InitializeEntity()`
- Component（组件）：单一职责，通过事件通信
- 依赖查找：使用 `ComponentExtensions` 手动查找组件（支持多态）
- 事件驱动：组件通过 `event Action` 解耦

**依赖倒置实现：**
```
BaseInputComponent (抽象基类)
    ↑ 依赖抽象
MovementComponent
CharacterRotationComponent
AnimationControllerComponent
    ↑ 实现
PlayerInputComponent (玩家输入)
AIInputComponent (AI输入 - 未来)
```

### Key Files

**核心组件：**
- `addons/CoreComponents/BaseInputComponent.cs` - 输入抽象基类
- `addons/CoreComponents/PlayerInputComponent.cs` - 玩家输入实现
- `addons/CoreComponents/MovementComponent.cs` - 移动组件
- `addons/CoreComponents/CharacterRotationComponent.cs` - 旋转组件
- `addons/CoreComponents/AnimationControllerComponent.cs` - 动画控制
- `addons/CoreComponents/CameraControlComponent.cs` - 相机控制
- `addons/CoreComponents/ComponentExtensions.cs` - 组件查找扩展方法

**动画系统：**
- `addons/CoreComponents/Animation/AnimationNames.cs` - 动画名称常量
- `addons/CoreComponents/Animation/AnimationSet.cs` - 动画集合
- `addons/CoreComponents/Animation/CharacterAnimationConfig.cs` - 动画配置

**实体：**
- `Scripts/Player3D.cs` - 玩家实体（10行代码）
- `Scenes/Player3D.tscn` - 玩家场景

**文档：**
- `addons/CoreComponents/INDEX.md` - 导航索引
- `addons/CoreComponents/README.md` - 完整文档
- `addons/CoreComponents/QUICK_START.md` - 快速开始
- `addons/CoreComponents/ARCHITECTURE.md` - 架构模式
- `addons/CoreComponents/HOW_IT_WORKS.md` - Godot.Composition 原理
- `addons/CoreComponents/MIGRATION_GUIDE.md` - 项目搬运指南
- `addons/CoreComponents/REFACTORING_GUIDE.md` - 重构指南
- `addons/CoreComponents/ARCHITECTURE_NOTES.md` - 架构说明

### Breaking Changes
**依赖查找方式：**
- Godot.Composition 不支持基类的 `[ComponentDependency]`
- 必须使用 `ComponentExtensions` 手动查找
- 示例：
```csharp
public void OnEntityReady()
{
    _inputComponent = parent.FindAndSubscribeInput(
        HandleMovementInput,
        HandleJumpInput
    );
}
```

## Recent Conversation Summary

### 1. 问题发现
用户发现 Godot.Composition 插件的 `ComponentContainer.cs` 只注册具体类型和接口，不注册基类，导致 `[ComponentDependency(typeof(BaseInputComponent))]` 无法工作。

### 2. 尝试的解决方案
**方案 A：创建接口（IEntityInput）**
- 创建了完整的 spec（requirements, design, tasks）
- 用户决定不采用此方案

**方案 B：修改插件源码**
- 从 GitHub 克隆了插件源码
- 修改了 `ComponentContainer.cs` 的 `Add` 方法，添加基类注册
- 遇到问题：Source Generator 冲突，编译失败

**方案 C：运行时补丁（GodotCompositionBasePatch）**
- 创建了运行时反射补丁
- 在 Entity 初始化后通过反射注册基类
- 结果：`baseInputComponent` 依然为 null，依赖注入失败

### 3. 最终方案
**回退到 ComponentExtensions 方案：**
- 使用 `parent.FindAndSubscribeInput()` 手动查找组件
- 简单、可靠、无副作用
- 一行代码解决问题

### 4. 清理工作
删除了所有失败的尝试：
- ✅ 删除 `.kiro/specs/interface-based-input-system/`
- ✅ 删除 `addons/Godot.Composition.Modified/`
- ✅ 删除 `GodotCompositionBasePatch.cs`
- ✅ 删除 `BASE_CLASS_DEPENDENCY_PATCH.md`
- ✅ 删除 `CHANGELOG.md`
- ✅ 恢复 MovementComponent 使用 ComponentExtensions
- ✅ 恢复 Player3D.cs 移除补丁调用

## Documentation Updated
- ✅ `addons/CoreComponents/ARCHITECTURE_NOTES.md` - 新建，说明依赖查找方案
- ✅ `.kiro/steering/docLastConversationState.md` - 本文件，完整重写

## 关键经验教训

### 问题根源
Godot.Composition 插件的设计决策：
- 只注册具体类型和接口
- 不遍历基类链
- Source Generator 生成的代码依赖插件的注册机制

### 为什么补丁失败
1. **反射时机问题**：补丁在 `InitializeEntity()` 之后执行，但 Source Generator 生成的代码在编译时已经确定了依赖查找逻辑
2. **Source Generator 限制**：生成的 `baseInputComponent` 变量的赋值逻辑在编译时固化，运行时修改字典无法影响已生成的代码
3. **插件内部机制**：ComponentContainer 的查找逻辑可能有缓存或其他机制，单纯修改字典不够

### 正确的解决方案
**ComponentExtensions 是最佳方案：**
- 简单：一行代码
- 可靠：不依赖插件内部机制
- 灵活：支持任何类型的多态查找
- 无副作用：不修改插件，不使用反射

## 下次对话开始时
1. 读取本文件恢复上下文
2. 确认角色移动功能是否正常
3. 根据用户需求继续开发新功能
