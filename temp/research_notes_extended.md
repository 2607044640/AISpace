# Godot Object Pool Research (Continued)

## Pattern Comparison

| 方案 | 核心结构 | 优点 | 缺点 | 适用场景 |
| :--- | :--- | :--- | :--- | :--- |
| **Interface-Based (Chickensoft)** | `IPooled` 接口 + `Stack<T>` | 状态清理强制化，代码极其整洁，类型安全。 | 需要修改每一个池化对象的类。 | 核心系统，对代码质量要求极高。 |
| **Scene-Based Dictionary** | `Dictionary<PackedScene, Queue<Node>>` | 灵活性高，不需要修改对象代码，支持任何 Scene。 | 状态清理容易遗漏（手动重置），字典查寻开销。 | 弹幕、特效、多变的动态物体。 |
| **Static Singleton (User's Idea)** | `Autoload` + `static` 泛型方法 | 调用极其方便 `Pool.Spawn<Bullet>(...)`。 | 缺乏局部控制，可能导致全局状态污染。 | 快速原型，小型项目。 |

## 深入研究：GodotUtilities (AhmedGD1) 方案
- **逻辑**: 通过 `NodePool` 管理器。每个池是一个独立的 Node。
- **扩展性**: 支持 `Prefill()` 预生成，防止战斗瞬间卡顿。
- **自动回收**: 使用 `TreeExiting` 信号或自定义 `Recycle()` 方法。

## 深入研究：Chickensoft 方案
- **逻辑**: 强调 **生命周期管理**。
- **关键点**: 对象被取出时调用 `OnActivate()`，存入时调用 `OnDeactivate()`。
- **性能**: 极简的容器封装，几乎没有额外开销。
