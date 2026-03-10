# 深度分析：遗漏的细节

## Round 1 深度检查

### ✅ 已添加
- ToSignal 基础用法
- Task.Delay 线程安全问题
- async Task vs async void
- Partial classes 要求
- [GlobalClass] 属性
- 资源缓存机制
- 后台加载资源

### ❌ 遗漏细节

1. **preload 在 C# 中不可用的详细说明**
   - 原文："preload 是 GDScript 特有的编译时加载"
   - 需要补充：C# 的替代方案和性能影响

2. **ResourceLoader.LoadThreadedGetStatus 的所有状态**
   - 原文只提到 Loaded 和 Failed
   - 缺少：InProgress, InvalidResource

3. **GD.Load 自动缓存的具体机制**
   - 原文："Godot 自动缓存已加载的资源"
   - 需要补充：如何手动清除缓存

## Round 2 深度检查

### ✅ 已添加
- EditorPlugin 基础
- 自定义 Inspector
- Tool 属性
- CallDeferred 三种方式
- 信号线程安全
- Vector2 所有操作
- Transform2D 操作

### ❌ 遗漏细节

1. **EditorPlugin 的 _EnterTree 和 _ExitTree 调用时机**
   - 原文只说"启用时"和"禁用时"
   - 需要补充：具体什么时候调用

2. **#if TOOLS 预处理指令的重要性**
   - 原文使用了但没有解释为什么必须用
   - 需要补充：不用会导致什么问题

3. **Engine.IsEditorHint() 的详细用法**
   - 原文只有简单示例
   - 需要补充：常见使用场景

4. **Vector2 常量的坐标系说明**
   - Vector2.Up 是 (0, -1) 而不是 (0, 1)
   - 需要解释：Godot 的 Y 轴向下

5. **Transform2D 的矩阵表示**
   - 原文没有说明内部结构
   - 需要补充：X、Y、Origin 的含义

## Round 3 深度检查

### ✅ 已添加
- ShaderMaterial 基础
- Modulate 三种类型
- 闪光效果 Shader
- JSON/ConfigFile/Binary/Encrypted 存档
- Camera2D 坐标转换
- 相机跟随和边界

### ❌ 遗漏细节

1. **Shader uniform 的类型提示**
   - 原文：`uniform float flash_intensity : hint_range(0.0, 1.0)`
   - 需要补充：其他 hint 类型（source_color 等）

2. **user:// 路径的具体位置**
   - 原文提到但没有说明不同平台的路径
   - 需要补充：Windows/Linux/Mac 的实际路径

3. **FileAccess.GetOpenError() 的错误码**
   - 原文使用了但没有列出常见错误
   - 需要补充：Error 枚举的常见值

4. **ConfigFile 的 section 概念**
   - 原文使用了 "audio"、"video" section
   - 需要补充：section 的作用和最佳实践

5. **Camera2D.GetCanvasTransform() vs GetGlobalCanvasTransform()**
   - 原文只用了 GetCanvasTransform()
   - 需要补充：两者的区别

6. **Camera2D 的 Zoom 属性**
   - 原文在 GetVisibleRect() 中使用
   - 需要补充：Zoom 的工作原理（Vector2，不是 float）

## Round 5 深度检查

### ✅ 已添加
- 自定义属性
- 反射读取属性
- 服务定位器
- GdUnit4Net 基础
- 场景测试
- Mocking

### ❌ 遗漏细节

1. **AttributeUsage 的参数说明**
   - 原文：`[AttributeUsage(AttributeTargets.Property)]`
   - 需要补充：其他 Targets 和 AllowMultiple、Inherited

2. **反射的性能影响**
   - 原文使用了反射但没有警告
   - 需要补充：反射很慢，不要在热路径使用

3. **服务定位器 vs 依赖注入的对比**
   - 原文只实现了服务定位器
   - 需要补充：何时用哪个

4. **GdUnit4Net 的安装方法**
   - 原文直接使用但没有说明如何安装
   - 需要补充：NuGet 包安装

5. **[TestSuite] 和 [TestCase] 的生命周期**
   - 原文没有说明测试的执行顺序
   - 需要补充：每个测试是独立的

## 新发现的重要遗漏

### 1. Godot 特有的概念没有解释

- **Node Path 语法**：`"Parent/Child/GrandChild"` 的规则
- **NodePath 类型**：什么时候用 string vs NodePath
- **StringName**：性能优化的字符串类型
- **Variant**：Godot 的动态类型系统

### 2. C# 和 Godot 的互操作

- **Godot.Collections vs System.Collections**
  - 何时用 Godot.Collections.Array
  - 何时用 List<T>
  
- **Callable 的详细用法**
  - Callable.From() 的各种重载
  - 为什么需要 Callable

### 3. 内存管理的细节

- **QueueFree() vs Free() 的具体区别**
  - 原文只说"安全"和"危险"
  - 需要补充：QueueFree 在帧结束时删除

- **Node 的引用计数**
  - Godot 使用引用计数
  - C# 的 GC 如何与之配合

### 4. 信号的高级用法

- **信号参数的类型限制**
  - 只能用 Godot 支持的类型
  - 不能用自定义 class（除非继承 GodotObject）

- **SignalName 的作用**
  - 为什么用 SignalName.HealthChanged 而不是字符串

### 5. Export 的限制

- **不能 Export 的类型**
  - 不能 Export System.Collections.Generic.List<T>
  - 必须用 Godot.Collections.Array<T>

- **Export 和序列化的关系**
  - Export 的变量会被序列化到 .tscn 文件

### 6. 性能相关的重要细节

- **GetNode 的性能**
  - 每次调用都要遍历树
  - 为什么必须缓存

- **信号的性能开销**
  - 信号比直接调用慢
  - 何时值得用信号

### 7. 常见陷阱

- **_Ready() 的调用顺序**
  - 子节点先于父节点
  - 可能导致空引用

- **场景实例化的时机**
  - Instantiate() 后节点还不在树中
  - 必须 AddChild() 后才能用 GetNode()

- **Autoload 的初始化顺序**
  - 按照 Project Settings 中的顺序
  - 可能导致依赖问题

## 优先级排序

### 高优先级（必须补充）
1. Godot 特有概念（NodePath、StringName、Variant）
2. Godot.Collections vs System.Collections
3. QueueFree vs Free 详细说明
4. _Ready() 调用顺序陷阱
5. Export 类型限制
6. user:// 路径说明
7. Callable 详细用法

### 中优先级（建议补充）
8. Shader uniform hints
9. Error 枚举常见值
10. Camera2D Zoom 工作原理
11. 反射性能警告
12. 信号参数类型限制
13. GetNode 性能说明

### 低优先级（可选）
14. AttributeUsage 详细参数
15. 服务定位器 vs 依赖注入
16. GdUnit4Net 安装
17. Transform2D 矩阵结构
