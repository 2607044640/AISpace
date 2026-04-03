# R3 重构总结

## 完成时间
2026-04-03

## 成果

### 1. 安装 R3
- **包名**: R3 v1.3.0 (Cysharp)
- **替代**: System.Reactive (官方 Rx.NET)
- **原因**: 
  - 专为游戏引擎优化（Unity, Godot）
  - 性能提升 10 倍
  - 支持帧操作（EveryUpdate, DelayFrame）
  - 零内存分配

### 2. 重构 SettingsMenu.cs
- **重构前**: 380 行
- **重构后**: 343 行
- **减少**: 37 行 (9.7%)

**关键改进**:
- `_ExitTree()`: 50+ 行 → 1 行
- 零内存泄漏风险
- 自动事件清理
- 代码更清晰

### 3. 核心模式

```csharp
using R3;

private readonly CompositeDisposable _disposables = new();

private void SubscribeToEvents()
{
    // 单参数事件
    Observable.FromEvent<float>(
        h => slider.ValueChanged += h,
        h => slider.ValueChanged -= h
    )
    .Subscribe(value => Handle(value))
    .AddTo(_disposables);
    
    // 多参数事件（tuple）
    Observable.FromEvent<Action<int, string>, (int, string)>(
        conversion: h => (i, s) => h((i, s)),
        addHandler: h => dropdown.ItemSelected += h,
        removeHandler: h => dropdown.ItemSelected -= h
    )
    .Subscribe(x => {
        var (index, text) = x;
        Handle(index, text);
    })
    .AddTo(_disposables);
}

public override void _ExitTree()
{
    _disposables.Dispose(); // 一行搞定！
}
```

### 4. 文档更新

#### DesignPatterns.md
- 新增 `<ReactiveExtensions>` 章节
- 包含完整代码示例
- 游戏引擎特性说明
- 使用规则和反模式

#### PluginRecord.md
- 新增 **Arch ECS** 条目
  - 用途：1000+ 实体的性能优化
  - 适用：弹幕游戏、RTS、大规模模拟
  - 不适用：UI、玩家控制器
- 新增 **R3** 条目
  - 用途：自动事件管理
  - 特性：帧操作、零分配

## R3 vs System.Reactive

| 对比项 | System.Reactive | R3 |
|--------|-----------------|-----|
| Stars | 6.7k | 3.5k |
| 发布时间 | 2010年 | 2024年 |
| 性能 | 基准 | 10倍快 |
| 游戏引擎 | ❌ | ✅ Godot/Unity |
| 帧操作 | ❌ | ✅ EveryUpdate |
| 兼容性 | 标准 Rx | 不兼容 |

## 下一步

可选优化：
1. 将 R3 模式应用到所有 `*ComponentHelper` 基类
2. 创建辅助扩展方法简化常见模式
3. 评估游戏逻辑中使用 `EveryUpdate()` 的场景

## 参考

- R3 GitHub: https://github.com/Cysharp/R3
- 重构文件: `3d-practice/B1Scripts/UI/SettingsMenu.cs`
- 设计模式: `KiroWorkingSpace/.kiro/steering/DesignPatterns.md`
- 插件记录: `KiroWorkingSpace/.kiro/steering/PluginRecord.md`
