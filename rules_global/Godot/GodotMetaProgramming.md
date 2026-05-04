# A1GodotMetaProgramming 架构指南 (Godot MetaProgramming Guidelines)

## 概述
A1GodotMetaProgramming 是我们为了减少 Godot C# 开发中的样板代码（Boilerplate）并提高与 R3（Reactive Extensions）结合时的健壮性而创建的源代码生成器（Source Generators）集合。

本指南旨在向之后的 AI 提供关于各个标签（Attributes）的设计意图、使用场景及历史变更，确保在使用该框架时能够采用最高效和正确的模式。

---

## 1. `[R3Event]` - 响应式事件生成
**目的**：替代容易在 `_Ready` 中由于 Godot 生命周期问题（子节点先于父节点 Ready）导致 `Subject` 尚未初始化便被订阅或调用的情况。

**使用方式**：
```csharp
[R3Event] private partial void OnMyEvent(string msg);
```
**生成物**：
- `OnMyEvent(msg)`: 用于触发事件的方法。
- `OnMyEventObservable`: 暴露出来的可订阅流（`Observable<string>`）。
- **核心机制**：内部 `Subject` 使用**懒加载 (Lazy Initialization)** 模式，只在第一次 `get` 时才 `new Subject()`。同时生成了针对该 `Subject` 的自动销毁生命周期。

**参数规则**：
- 0 参数 -> 自动对应 `Unit`。
- 1 参数 -> `T`。
- 2+ 参数 -> 生成元组 `(T1 a, T2 b, ...)`。

---

## 2. `[GodotNode]` - 节点自动绑定
**目的**：替代大量在 `_Ready` 里的手动 `GetNodeOrNull<T>("%Name")` 和空值检查错误输出。

**使用方式**：
```csharp
[GodotNode] private GridShapeComponent _shape; 
// 等同于 [GodotNode("%GridShapeComponent")]

[GodotNode("../Path")] private Control _uiRoot;
```

**生成物**：
- `[Export] NodePath _shape_Path`。
- `_InitNodeGridShapeComponent()`：封装了获取节点并 `PushError` 检查的逻辑。
- `_InitAllNodes()`：统一调用所有生成的 `_InitNode*()` 方法。

**注意事项**：
- **手动触发**：必须在类的 `_Ready()` 中手动调用 `_InitAllNodes();`。
- **Godot Inspector 兼容性缺陷**：Godot 的 C# 解析器**无法读取** Source Generator 生成的 `[Export]` 属性，因此无法在编辑器面板中直接修改绑定的路径。如果该变量必须在 Godot Inspector 中手动指定，**绝对不要使用 `[GodotNode]`**，而应回归老办法：`[Export] public NodePath MyPath;`。

---

## 3. 生命周期的订阅清理：`.AddTo(this)` vs `[GenerateCompositeDisposable]`

**现状与结论：`[GenerateCompositeDisposable]` 在本项目中已废弃/非必要，全面推荐使用 `.AddTo(this)`。**

### 背景
过去我们为了管理 R3 订阅的释放，编写了 `[GenerateCompositeDisposable]` 以自动注入一个 `CompositeDisposable _disposables` 并在 `_ExitTree` 时 `Dispose()`。

### 为什么被替代？
Godot 环境下 R3 的 `.AddTo(this)` 拓展方法内部直接为每个订阅挂载了 `TreeExiting` 的处理逻辑。这完美满足了我们在销毁时清理订阅的需求。

```csharp
// 【推荐模式】完全等价且更简洁
someObs.Subscribe(...).AddTo(this);
```

### 什么时候才必须使用 `CompositeDisposable`？
只有在**节点还活着，但需要提前清空所有旧订阅并重新订阅新状态**时（即状态切换、中途重置），才必须使用 `CompositeDisposable`（因为 `.AddTo(this)` 只能等 `TreeExiting`，不能提前手动清理）。
**但在当前项目架构中，极少出现这种中途重置订阅的场景（绝大部分是在节点整个生命周期内订阅一次）**。

因此，在诸如常规组件开发以及 `Godot.Composition` 框架下的 `OnEntityReady()` 方法中，请**统一使用 `.AddTo(this)`**，不再需要生成和管理 `_disposables`。
