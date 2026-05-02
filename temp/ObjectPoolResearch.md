# 对象池(Object Pool) 架构研究报告

## 1. 为什么在项目初期引入对象池？
在游戏引擎（尤其是Godot）中，在战斗高潮时动态实例化(Instantiate)和释放(QueueFree)大量节点（如子弹、伤害飘字、特效）会引起明显的内存分配和垃圾回收(GC)开销，甚至导致主线程卡顿（帧率骤降）。初期引入不仅能从根本上避免性能瓶颈，还能强制规范代码结构，让所有实体生成与销毁逻辑收敛到一处，极大提高项目的可维护性。

## 2. 泛型 Autoload 架构可行性
你提出的 **“全局 Autoload + 泛型 T + 统一容器管理”** 方案是非常标准且先进的架构。
具体结构通常是：
1. **全局管理器 (PoolManager Autoload)**: 存储一个以类型或唯一ID为Key的字典 `Dictionary<string, IPool>`。
2. **泛型池 (ObjectPool<T>)**: 针对具体的类型 `T`（需继承自 Node）进行实例化、回收、激活管理。
3. **调用方式**: 
   - 比如子弹系统：`PoolManager.Get<Bullet>(bulletScenePath)`
   - 返回一个已经从树中激活的 `T` 实例。使用完毕后调用 `PoolManager.Release(bullet)`。
这种方案的代码确实十分干净，做下一个项目时可以直接把 `PoolManager` 的脚本迁移过去。

## 3. GitHub 现有项目调研
经过在 GitHub 上的搜索，Godot 专用的大于 100 stars 的 C# 对象池插件比较少（大多为 GDScript 且实现简单），最相关的库如下：

- **Godot 相关库**:
  - `godot-addons/godot-object-pool` (48 stars) - 偏基础实现。
  - `blue-mug-orange-cup/easyPool` (11 stars) - C# 实现的基础对象池。
- **Unity / 泛型 C# 相关高星库**（更值得借鉴架构）:
  - `UnityPatterns/ObjectPool` (422 stars) - Unity经典对象池。
  - `microsoft/Microsoft.IO.RecyclableMemoryStream` (2132 stars) - 微软官方的流对象池，展示了最高级别的C#池化思想。
  - `thefuntastic/unity-object-pool` (283 stars) - 基于泛型和委托的高级对象池。

### 方案优缺点总结

#### 方案A: 纯 Godot 节点池 (基于 `PackedScene`)
- **思路**: 使用 `Dictionary<PackedScene, Array<Node>>`。每次需要时克隆 `PackedScene`。
- **优点**: 非常直观，跟 Godot 结合紧密。
- **缺点**: 缺乏类型安全，获取后需要强制转换 `as T`。不使用泛型，代码有些啰嗦。

#### 方案B: 泛型委托池 (类似于 .NET 原生 `ObjectPool<T>`)
- **思路**: 池子本身只关心 `T`。创建时传入 `Func<T> createFunc`, `Action<T> onGet`, `Action<T> onRelease`。
- **优点**: 极度解耦，不依赖具体的引擎 Node。不仅可以池化节点，甚至可以池化普通的 C# 类（比如某个计算用的大数组、数据结构）。
- **缺点**: Node 节点必须配合 `PackedScene` 的实例化，所以在Godot中需要包装一层。

#### 方案C: 混合型组件池 (推荐方案)
- **思路**: 构建一个单例 `PoolManager`。内部维护 `Dictionary<string, Queue<Node>>` (使用场景路径或资源ID做Key)。暴露泛型方法 `public T Spawn<T>(PackedScene prefab, Vector2 position)`。同时为所有可池化对象定义接口 `IPoolable`，包含 `OnSpawn()` 和 `OnDespawn()` 方法。
- **优点**: 
  1. 完美契合 Godot 的场景系统（基于 PackedScene）。
  2. 满足了题主的“通过 T 放入和取出”的强类型需求。
  3. 通过 `IPoolable` 接口处理激活/休眠的重置逻辑，各司其职（子弹自己负责重置速度，特效自己负责重置动画）。
- **缺点**: 需要严格遵守接口规范，如果不小心手动调用了 `QueueFree()` 会破坏池子状态。

## 4. 架构设计总结与选择

在Godot中进行C#开发，最好的做法是**借鉴Unity的泛型对象池思想，结合Godot的场景实例化机制**。推荐采用 **“方案C (混合型组件池)”**。

它能完美实现你所想的：
```csharp
// 调用干净利落
Bullet bullet = ObjectPool.Spawn<Bullet>(bulletPrefab);
bullet.Shoot();

// 子弹内部销毁时
ObjectPool.Despawn(this);
```
