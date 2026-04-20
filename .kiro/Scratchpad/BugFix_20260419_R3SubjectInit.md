# Bug Fix: R3 Subject 初始化缺失

## 日期
2026-04-19

## Bug 描述
`GridShapeComponent.OnShapeChangedAsObservable` Subject 从未被初始化，导致 `GridShapeVisualComponent` 订阅时抛出 `NullReferenceException`。

## 根本原因
```csharp
// 错误：仅声明属性，未实例化
public Subject<Unit> OnShapeChangedAsObservable { get; private set; }
```

Subject 在 `_Ready()` 中未被初始化为 `new Subject<Unit>()`，导致属性值为 `null`。

## 修复方案

### 1. 初始化 Subject
```csharp
public override void _Ready()
{
    // 【BUG FIX】初始化 R3 Subject（必须在任何订阅之前完成）
    OnShapeChangedAsObservable = new Subject<Unit>();
    GD.Print($"[{Name}] OnShapeChangedAsObservable 已初始化");
    
    // ... 其余逻辑
}
```

### 2. 触发事件
```csharp
public void SetData(ItemDataResource data)
{
    _data = data;
    InitializeShape();
    
    // 【关键】触发形状变化事件
    OnShapeChangedAsObservable?.OnNext(Unit.Default);
}
```

### 3. 条件构建
```csharp
// GridShapeVisualComponent._Ready()
if (GridShapeComponent.CurrentLocalCells != null)
{
    RebuildVisualBlocks();
}
else
{
    // 等待 OnShapeChangedAsObservable 事件
}
```

## 次要问题：数据注入时序

**问题**: GridShapeVisualComponent 在 `_Ready()` 中立即调用 `RebuildVisualBlocks()`，但此时 `CurrentLocalCells` 为 `null`（数据通过 `IItemDataProvider` 接口异步注入）。

**解决**: 添加 null 检查，仅在数据已存在时立即构建，否则等待 `OnShapeChangedAsObservable` 事件。

## 验证

### 编译
```bash
dotnet build
# 结果: 成功，无错误
```

### 运行
```bash
# 场景: Scenes/BackpackTest.tscn
# 结果: 正常加载，无 NullReferenceException
```

### Debug 日志
```
[GridShapeComponent] GridShapeComponent._Ready() 开始
[GridShapeComponent] OnShapeChangedAsObservable 已初始化
[GridShapeComponent] GridShapeComponent._Ready() 完成
[GridShapeVisualComponent] GridShapeVisualComponent._Ready() 开始
[GridShapeVisualComponent] 已订阅 GridShapeComponent.OnShapeChangedAsObservable
[GridShapeVisualComponent] 数据尚未注入，等待 OnShapeChangedAsObservable 事件
[GridShapeComponent] GridShapeComponent.SetData: 收到 Data = item_default
GridShapeComponent 初始化完成：3 个格子
[GridShapeVisualComponent] 收到形状变化事件，重建视觉方块
[GridShapeVisualComponent] RebuildVisualBlocks() 开始
```

## 教训

### R3 Subject 初始化规则
**MUST**: 所有 R3 Subject 必须在 `_Ready()` 中显式初始化
```csharp
// 正确模式
public override void _Ready()
{
    MySubject = new Subject<T>();
    // ... 其余逻辑
}
```

### 异步数据注入处理
当组件依赖异步注入的数据时：
1. 订阅数据变化事件（如 `OnShapeChangedAsObservable`）
2. 在 `_Ready()` 中检查数据是否已存在
3. 如果存在，立即处理；否则等待事件

### Debug 日志策略
在修复 Bug 时添加详细的 debug 日志：
- 标记关键初始化点
- 记录事件触发时机
- 验证执行顺序
- 稳定后移除或条件编译

## 状态
✅ **已修复**  
✅ **已验证**  
⏳ **待清理 Debug 日志**
