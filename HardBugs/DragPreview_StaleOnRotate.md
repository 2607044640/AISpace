# Hard Bug: Drag Preview — 旋转后预览冻结 & Ghost Glow

---

## Bug A：旋转期间预览不刷新（DistinctUntilChanged 阻塞）

### 症状
玩家在拖拽状态下按右键旋转物品，背景格子的绿/红高亮**不会立即更新**，
直到鼠标跨越一个网格边界才重新计算。期间显示的是旧形状的预览结果。

### 根因（已确认）
预览 R3 流的过滤节点：
```csharp
.Select(mousePos => (inBounds: ..., gridPos: GlobalToGridPosition(mousePos)))
.DistinctUntilChanged()   // ← 问题出在这里
```
`DistinctUntilChanged` 比较的是 `(bool inBounds, Vector2I gridPos)` 元组。
旋转只改变了物品形状（`shapeComponent.CurrentLocalCells`），**不改变鼠标坐标**，
所以元组值不变 → 数据被过滤 → `ShowPreview` 不会被调用 → 预览冻结。

### 修复方案（推荐）
合并两条流：鼠标位置流 + 形状变化流。形状一旦变化，强制发射一次无视 `DistinctUntilChanged` 的更新。

```csharp
// 当前：只监听鼠标位置
Observable.EveryUpdate()
    .Select(_ => ViewGrid.GetGlobalMousePosition())
    .Select(mousePos => (inBounds: ..., gridPos: ...))
    .DistinctUntilChanged()
    .TakeUntil(draggable.OnDragEndedAsObservable)

// 修复：shapeStream 必须与 posStream 吐出相同的元组类型，Merge 才能工作
// 关键：不把形状数组放进 DistinctUntilChanged 比较键（引用比较会失效，且有额外开销）
var posStream = Observable.EveryUpdate()
    .Select(_ => ViewGrid.GetGlobalMousePosition())
    .Select(mousePos => (
        inBounds: ViewGrid.GetGlobalRect().HasPoint(mousePos),
        gridPos:  ViewGrid.GlobalToGridPosition(mousePos)
    ))
    .DistinctUntilChanged(); // 只比较 (bool, Vector2I) 元组

// shapeStream：旋转时"伪装"成相同元组，实时反查当前鼠标坐标，绕过 DistinctUntilChanged
var shapeStream = shapeComponent.OnShapeChangedAsObservable
    .Select(_ => {
        var mp = ViewGrid.GetGlobalMousePosition();
        return (
            inBounds: ViewGrid.GetGlobalRect().HasPoint(mp),
            gridPos:  ViewGrid.GlobalToGridPosition(mp)
        );
    });

Observable.Merge(posStream, shapeStream)
    .TakeUntil(draggable.OnDragEndedAsObservable)
    .Subscribe(state => {
        if (!state.inBounds) ViewGrid.ClearPreview();
        else ViewGrid.ShowPreview(Logic.EvaluatePlacementPreview(
            shapeComponent.CurrentLocalCells, state.gridPos));
    })
    .AddTo(itemEntity);
```

### 关键落地细节（Gotcha）
- **类型一致性**：`shapeStream` 必须将 `Unit` 转换为与 `posStream` 完全相同的 `(bool inBounds, Vector2I gridPos)` 元组，`Merge` 才能编译通过。
- **为什么不把形状放进 Distinct 键**：`Vector2I[]` 数组在 C# 中是引用类型，`DistinctUntilChanged` 默认用引用相等，同一数组旋转后内容变了但引用不变会导致过滤失效；且每帧做数组内容比较有额外 GC 开销。

### 状态
- [x] 已修复（`Observable.Merge(posStream, shapeStream)`）

---

## Bug B：Ghost Glow（幽灵高亮）—— 使用 mouse_entered/exited 的必然后果

### 症状
格子高亮（绿/红发光）在拖拽结束后**仍然残留**，鼠标移走后某些格子永久卡在发光状态。

### 根因
使用 Godot 信号 `mouse_entered` / `mouse_exited` 驱动高亮的方案，在以下场景必然失败：

| 场景 | 失败原因 |
|---|---|
| 快速拖拽（> 一格/帧） | `mouse_exited` 从未触发，格子永久高亮 |
| 帧边界跨越 | `entered` 和 `exited` 乱序，状态机撕裂 |
| 管理几十格的订阅 | 每格一个订阅，内存开销 & 难以统一 `ClearPreview` |
| 物品被删除时 | 若 `mouse_exited` 未在 `_ExitTree` 前触发，泄漏订阅 |

### 正确方案（当前实现）
**"天花板摄像头"模型**：不给地板每块瓷砖装压力传感器，而是在天花板装一个广角摄像头，
用数学坐标直接计算"鼠标踩在哪格"。

```csharp
Observable.EveryUpdate()
    .Select(_ => ViewGrid.GetGlobalMousePosition())
    .Select(mousePos => (
        inBounds: ViewGrid.GetGlobalRect().HasPoint(mousePos),
        gridPos:  ViewGrid.GlobalToGridPosition(mousePos)   // 纯数学，不依赖任何事件
    ))
    .DistinctUntilChanged()                          // 过滤亚格子抖动
    .TakeUntil(draggable.OnDragEndedAsObservable)    // 自动终止，零手动清理
    .Subscribe(state =>
    {
        if (!state.inBounds) ViewGrid.ClearPreview();
        else ViewGrid.ShowPreview(BackpackGridComp.EvaluatePlacementPreview(...));
    })
    .AddTo(itemEntity);
```

优势：
- `TakeUntil` 保证无论何种结束方式（正常松手、节点销毁、异常），高亮状态都被清除
- `DistinctUntilChanged` 让性能开销仅发生在跨格瞬间，而非每帧
- 无信号订阅 = 无乱序 = 无幽灵

### 状态
- [x] 已通过 R3 流架构规避，不会在当前代码库复现

---

## 相关约束（见 GodotBackpackTesseractSys_Context.md）
- `top_anti_patterns`: NEVER use `mouse_entered`/`mouse_exited` for grid highlight
- `implementation_anchors`: R3 Placement Preview Stream Pattern
