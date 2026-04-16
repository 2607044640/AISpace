# Item Templates Creation - COMPLETED

## 任务完成时间
2026-04-16

## 创建的文件

### 1. Python 生成器脚本
- `KiroWorkingSpace/builder/generate_basic_item.py` - 生成 BasicItem.tscn
- `KiroWorkingSpace/builder/generate_draggable_item.py` - 生成 TetrisDraggableItem.tscn

### 2. 场景模板
- `3d-practice/addons/A1TetrisBackpack/Items/BasicItem.tscn` - 最小化模板
- `3d-practice/addons/A1TetrisBackpack/Items/TetrisDraggableItem.tscn` - 完整拖拽模板

### 3. 文档
- `3d-practice/addons/A1TetrisBackpack/Items/README.md` - 完整使用文档

## 模板对比

| 特性 | BasicItem | TetrisDraggableItem |
|------|-----------|---------------------|
| 用途 | 最小化模板，快速扩展 | 完整拖拽功能 |
| StateChart | ✅ Idle/Clicked | ✅ Idle/Dragging |
| 拖拽 | ❌ | ✅ |
| 旋转 | ❌ | ✅ |
| 网格形状 | ❌ | ✅ |
| 跟随鼠标 | ❌ | ✅ |
| 适用场景 | 消耗品、装备、任务物品 | Tetris 背包、网格背包 |

## BasicItem.tscn 结构

```
BasicItem (Control)
├── ClickableBackground (ColorRect) [%]
└── StateChart [%]
    └── Root [%]
        ├── Idle [%]
        │   └── ToDragging (Transition)
        └── Clicked [%]
```

**状态流转**：
- Idle → `clicked` 事件 → Clicked
- Clicked → 0.5秒后自动 → Idle

**扩展方向**：
- 添加 C# 脚本监听状态变化
- 添加更多状态（Equipped, Consumed, Destroyed）
- 添加自定义组件（Tooltip, Animation, Sound）

## TetrisDraggableItem.tscn 结构

```
TetrisDraggableItem (Control)
├── ClickableBackground (ColorRect) [%]
├── VisualContainer (Control)
│   └── ItemIcon (TextureRect)
├── StateChart [%]
│   └── Root [%]
│       ├── Idle [%]
│       │   └── ToDragging (Transition)
│       └── Dragging [%]
│           ├── ToIdle (Transition)
│           └── FollowMouseUIComponent
│               - TargetUIPath = "%TetrisDraggableItem"
├── DraggableItemComponent
│   - ClickableAreaPath = "%ClickableBackground"
│   - StateChartPath = "%StateChart"
└── GridShapeComponent
```

**状态流转**：
- Idle → `drag_start` 事件 → Dragging
- Dragging → `drag_end` 事件 → Idle

**组件功能**：
- `DraggableItemComponent`: 监听鼠标输入，发送状态机事件
- `GridShapeComponent`: 管理物品形状，支持旋转
- `FollowMouseUIComponent`: 在 Dragging 状态下跟随鼠标

## 使用示例

### 创建消耗品（BasicItem）
```csharp
// 1. 加载场景
var basicItemScene = GD.Load<PackedScene>("res://addons/A1TetrisBackpack/Items/BasicItem.tscn");
var potion = basicItemScene.Instantiate<Control>();
AddChild(potion);

// 2. 添加点击逻辑
var background = potion.GetNode<ColorRect>("%ClickableBackground");
background.GuiInput += (InputEvent @event) => {
    if (@event is InputEventMouseButton mouseEvent && 
        mouseEvent.Pressed && 
        mouseEvent.ButtonIndex == MouseButton.Left)
    {
        potion.GetNode("%StateChart").Call("send_event", "clicked");
        UsePotion();  // 使用药水
    }
};

// 3. 监听状态变化
var clickedState = potion.GetNode("%Clicked");
clickedState.Connect("state_entered", Callable.From(() => {
    GD.Print("药水被使用了！");
    // 播放音效、显示特效
}));
```

### 创建可拖拽物品（TetrisDraggableItem）
```csharp
// 1. 加载场景
var draggableScene = GD.Load<PackedScene>("res://addons/A1TetrisBackpack/Items/TetrisDraggableItem.tscn");
var sword = draggableScene.Instantiate<Control>();
backpackUI.AddChild(sword);

// 2. 配置物品数据
var itemData = new ItemDataResource {
    ItemID = "sword_001",
    ItemName = "铁剑",
    BaseShape = new Array<Vector2I> {
        new Vector2I(0, 0),
        new Vector2I(0, 1),
        new Vector2I(0, 2)  // 1x3 竖条
    }
};

var shapeComponent = sword.GetNode<GridShapeComponent>("%GridShapeComponent");
shapeComponent.Data = itemData;

// 3. 设置图标
var icon = sword.GetNode<TextureRect>("VisualContainer/ItemIcon");
icon.Texture = GD.Load<Texture2D>("res://icons/sword.png");

// 4. 注册到控制器
var controller = GetNode<BackpackInteractionController>("%BackpackInteractionController");
controller.RegisterItem(sword);
```

## 技术亮点

### 1. Scene Unique Names (%)
所有需要查找的节点都标记为 `unique_name_in_owner = true`，使用 `%NodeName` 语法查找：
- ✅ 层级无关：不受节点树结构变化影响
- ✅ 重构安全：移动节点不会破坏引用
- ✅ 易于维护：路径清晰直观

### 2. StateChart 驱动
使用 GodotStateCharts 管理物品状态：
- ✅ 可视化：在编辑器中直观看到状态流转
- ✅ 解耦：状态逻辑与业务逻辑分离
- ✅ 扩展性：轻松添加新状态和转换

### 3. 组件化设计
每个功能独立封装为组件：
- `DraggableItemComponent`: 拖拽输入
- `GridShapeComponent`: 形状管理
- `FollowMouseUIComponent`: 鼠标跟随
- ✅ 可复用：组件可用于其他场景
- ✅ 可测试：每个组件独立测试
- ✅ 可维护：修改一个组件不影响其他

### 4. R3 响应式编程
使用 R3 Subject 发布事件：
```csharp
draggable.OnDragStartedAsObservable
    .Subscribe(_ => {
        GD.Print("开始拖拽");
    })
    .AddTo(disposables);
```
- ✅ 解耦：发布者和订阅者解耦
- ✅ 组合：多个事件流可以组合
- ✅ 内存安全：自动管理订阅生命周期

## 架构决策

### 为什么不提取 Core 系统？
**决策**：保持现有结构，只添加 Items 文件夹

**理由**：
1. **YAGNI 原则**：目前只有 TetrisBackpack 一个实现
2. **降低风险**：避免大规模重构导致的 bug
3. **快速交付**：用户需要的是模板，不是架构重构
4. **易于回滚**：如果模板不满意，容易调整

**未来扩展**：
- 如果需要其他背包类型（如 ListBackpack），再考虑提取 Core 系统
- 当前架构已经足够清晰，不影响未来重构

### 为什么使用 Python 生成器？
**优势**：
1. **一致性**：所有场景使用相同的生成逻辑
2. **可维护性**：修改模板只需修改 Python 脚本
3. **可复用性**：生成器可用于其他场景
4. **版本控制**：Python 脚本易于版本控制和 diff

## 下一步

### 立即可用
- ✅ 两个模板已生成并可用
- ✅ 文档完整，包含使用示例
- ✅ 符合项目架构规范

### 可选扩展
1. **创建示例场景**：
   - 创建一个完整的背包 UI 示例
   - 包含多个物品实例
   - 演示拖拽、旋转、放置

2. **添加更多模板**：
   - `EquippableItem.tscn` - 可装备物品
   - `ConsumableItem.tscn` - 消耗品
   - `QuestItem.tscn` - 任务物品

3. **创建物品数据库**：
   - 使用 ItemDataResource 创建物品库
   - 包含常见物品（剑、盾、药水等）
   - 提供预设的形状和图标

## 总结

✅ **任务完成**：成功创建两个物品模板
✅ **文档完整**：包含使用说明、示例代码、常见问题
✅ **架构合理**：保持现有结构，避免过度设计
✅ **易于扩展**：模板设计灵活，支持多种扩展方向

用户现在可以：
1. 使用 BasicItem 快速创建简单物品
2. 使用 TetrisDraggableItem 创建完整的拖拽物品
3. 根据需求扩展模板，添加自定义功能
