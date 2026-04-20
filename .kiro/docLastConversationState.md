# 上次对话状态

## 元数据
- **更新日期**: 2026-04-19
- **引擎**: Godot 4.6.1 stable mono
- **语言**: C# only
- **项目**: Tesseract Backpack (TS) - 完整网格背包系统（带协同效果）
- **阶段**: Event Aggregator 架构完成并验证，R3 Subject 初始化 Bug 已修复

## 项目命名规范

### TS 前缀标准
- **项目名称**: Tesseract Backpack (TS)
- **旧代码库**: `3d-practice/addons/A1TetrisBackpack/` (C# 组件)
- **新项目目录**: `3d-practice/A1TesseractBackpack/` (场景和资源)
- **场景文件命名**: 使用 `TS` 前缀
  - 示例: `TSItem.tscn`
  - 位置: `3d-practice/A1TesseractBackpack/TSItem.tscn`
- **文档命名**: `GodotBackpackTesseractSys_Context.md`

## 最新完成：R3 Subject 初始化 Bug 修复 ✅

### 问题诊断
在实现 Event Aggregator 架构后，运行时出现 `NullReferenceException`：
- **症状**: GridShapeVisualComponent 尝试订阅 `GridShapeComponent.OnShapeChangedAsObservable` 时崩溃
- **根本原因**: `OnShapeChangedAsObservable` Subject 从未被初始化（仅声明为属性，未实例化）
- **次要问题**: GridShapeVisualComponent 在 `_Ready()` 中过早尝试构建视觉方块，此时数据尚未通过 `IItemDataProvider` 接口注入

### 修复方案

**1. GridShapeComponent.cs - Subject 初始化**
```csharp
public override void _Ready()
{
    GD.Print($"[{Name}] GridShapeComponent._Ready() 开始");
    
    // 【BUG FIX】初始化 R3 Subject（必须在任何订阅之前完成）
    OnShapeChangedAsObservable = new Subject<Unit>();
    GD.Print($"[{Name}] OnShapeChangedAsObservable 已初始化");
    
    // ... 其余初始化逻辑
}
```

**2. GridShapeComponent.SetData() - 触发事件**
```csharp
public void SetData(ItemDataResource data)
{
    _data = data;
    InitializeShape();
    
    if (AutoResizeParent)
    {
        CallDeferred(MethodName.UpdateParentSize);
    }
    
    // 【关键】触发形状变化事件，通知 GridShapeVisualComponent 构建视觉方块
    OnShapeChangedAsObservable?.OnNext(Unit.Default);
    
    GD.Print($"GridShapeComponent 初始化完成：{CurrentLocalCells?.Length ?? 0} 个格子");
}
```

**3. GridShapeVisualComponent.cs - 条件构建**
```csharp
public override void _Ready()
{
    // ... 引用解析和订阅逻辑
    
    GridShapeComponent.OnShapeChangedAsObservable
        .Subscribe(_ => 
        {
            GD.Print($"[{Name}] 收到形状变化事件，重建视觉方块");
            RebuildVisualBlocks();
        })
        .AddTo(this);
    
    // 【架构修正】不在 _Ready() 中立即构建方块
    // 原因：数据通过 IItemDataProvider 接口异步注入，此时 CurrentLocalCells 可能为 null
    // 解决方案：仅通过 OnShapeChangedAsObservable 事件触发构建（数据注入后会自动触发）
    if (GridShapeComponent.CurrentLocalCells != null)
    {
        GD.Print($"[{Name}] 数据已存在，立即构建视觉方块");
        RebuildVisualBlocks();
    }
    else
    {
        GD.Print($"[{Name}] 数据尚未注入，等待 OnShapeChangedAsObservable 事件");
    }
}
```

### 初始化时序

正确的初始化顺序（通过 debug 日志验证）：
```
1. GridShapeComponent._Ready()
   └─ OnShapeChangedAsObservable = new Subject<Unit>()

2. GridShapeVisualComponent._Ready()
   └─ 订阅 OnShapeChangedAsObservable
   └─ 检查 CurrentLocalCells (此时为 null，跳过构建)

3. TSItemWrapper._Ready()
   └─ 触发 DataInitialized 事件

4. GridShapeComponent.OnDataReceived()
   └─ SetData(data)
   └─ InitializeShape()
   └─ OnShapeChangedAsObservable.OnNext(Unit.Default)

5. GridShapeVisualComponent 订阅者接收事件
   └─ RebuildVisualBlocks()
   └─ 生成 ColorRect 方块
```

### 验证结果

✅ **编译成功**: `dotnet build` 无错误  
✅ **运行成功**: Scenes/BackpackTest.tscn 正常加载  
✅ **初始化正确**: Debug 日志显示完整的事件流  
✅ **无 NullReferenceException**: Subject 在订阅前已初始化  
✅ **数据注入正确**: IItemDataProvider 接口模式工作正常  

### 测试场景
- **测试文件**: `3d-practice/Scenes/BackpackTest.tscn`
- **测试项**: TSItem 实例（L 形物品）
- **验证点**: 
  1. 场景加载无崩溃
  2. 视觉方块正确生成
  3. 事件流正确触发

### 下一步测试
1. **鼠标交互测试**: 点击 L 形的实际方块 vs 空白角落
2. **旋转功能测试**: 拖拽中右键旋转
3. **验证反馈测试**: 红绿光颜色切换
4. **清理 Debug 日志**: 移除或减少生产环境的调试输出

---

## 最新完成：事件聚合架构 - 离散方块 + R3 流汇聚 ✅

### 架构转变：放弃 _HasPoint，采用事件聚合

**问题**: _HasPoint 重写虽然可行，但与 Godot 的 AABB 系统对抗，不够优雅。

**用户提出的更优方案**: 
- 不与 AABB 对抗，让每个 1x1 ColorRect 独立接收 GuiInput
- 通过 R3 Subject 将所有方块的事件汇聚成单一流
- DraggableItemComponent 订阅这个流，而不是监听单一父容器

### 核心架构：Event Aggregator Pattern

```csharp
// GridShapeVisualComponent - 事件聚合器
private readonly Subject<InputEvent> _onBlockInputSubject = new();
public Observable<InputEvent> OnBlockInputAsObservable => _onBlockInputSubject;

// 生成方块时绑定事件
visualBlock.GuiInput += (inputEvent) =>
{
    _onBlockInputSubject.OnNext(inputEvent);
};

// DraggableItemComponent - 订阅聚合流
GridShapeVisualComponent.OnBlockInputAsObservable
    .Subscribe(HandleGuiInput)
    .AddTo(this);
```

### 数据流

```
用户点击 L 形的任意方块
    ↓
ColorRect[n].GuiInput 事件触发
    ↓
_onBlockInputSubject.OnNext(inputEvent)
    ↓
OnBlockInputAsObservable 流发射事件
    ↓
DraggableItemComponent 订阅者接收
    ↓
HandleGuiInput() 处理（左键拖拽/右键旋转）
    ↓
StateChart 状态切换
```

### 架构优势

✅ **完全绕过 AABB**: 每个方块独立响应，无需对抗 Godot 系统  
✅ **纯组件化**: GridShapeVisualComponent 是 Node（纯逻辑控制器）  
✅ **事件统一**: R3 Subject 汇聚所有 GuiInput 到单一流  
✅ **高度解耦**: DraggableItemComponent 只订阅流，不关心实现细节  
✅ **易于扩展**: 可以轻松添加事件过滤、转换、合并等 R3 操作  
✅ **内存安全**: Subject 在 _ExitTree 中 Dispose  

### 关键实现

**GridShapeVisualComponent (Node)**:
- 生成独立的 ColorRect 方块（MouseFilter.Pass）
- 绑定每个方块的 GuiInput 到 R3 Subject
- 暴露 `OnBlockInputAsObservable` 供外部订阅
- InteractionArea 设置 MouseFilter.Ignore（父容器不拦截）

**DraggableItemComponent**:
- Export 从 `NodePath ClickableAreaPath` 改为 `GridShapeVisualComponent GridShapeVisualComponent`
- 订阅 `GridShapeVisualComponent.OnBlockInputAsObservable`
- 逻辑保持不变（左键拖拽，右键旋转）

### TSItem 场景结构

```
TetrisDraggableItem (TSItemWrapper) - MouseFilter.Ignore
├── InteractionArea (Control) - MouseFilter.Ignore
│   ├── ClickableBackground (ColorRect)
│   ├── ItemIcon (TextureRect)
│   └── [运行时生成的 ColorRect 方块 - MouseFilter.Pass]
├── StateChart
├── GridShapeComponent - 逻辑/数据层
├── GridShapeVisualComponent - 事件聚合器
└── DraggableItemComponent - 订阅聚合流
```

### 文件修改

- ✅ `GridShapeVisualComponent.cs` - 从 Control 回归 Node，添加 R3 Subject 事件聚合
- ✅ `DraggableItemComponent.cs` - 订阅 GridShapeVisualComponent 的事件流
- ✅ `TSItem.tscn` - 更新 DraggableItemComponent 的 Export 引用

### 验证

✅ `dotnet build` 成功  
✅ 事件聚合架构实现  
✅ R3 流订阅正确配置  
✅ 场景文件更新完成  

### 测试指南

**当前状态**: Event Aggregator 架构已实现并通过初始化验证

**待测试功能**:
1. ✅ 场景加载和初始化（已验证）
2. ⏳ L 形物品鼠标交互精度
   - 点击实际方块 → 应触发拖拽
   - 点击空白角落 (1,0) → 不应响应
3. ⏳ 拖拽中右键旋转
4. ⏳ 验证反馈（红绿光）
5. ⏳ 方块自动重建（旋转后）

**测试步骤**:
1. 在 Godot 编辑器中打开 `Scenes/BackpackTest.tscn`
2. 运行场景（F5）
3. 尝试点击 TSItem 的不同区域
4. 拖拽物品并测试旋转
5. 观察控制台输出和视觉反馈

**Debug 日志清理**:
- 当前代码包含大量 `GD.Print()` 用于调试
- 验证稳定后应移除或改为条件编译（`#if DEBUG`）

### 关键教训

**在 Godot 中处理不规则形状的鼠标交互，最优雅的方案是：**
1. 让每个 1x1 方块独立接收事件（MouseFilter.Pass）
2. 通过 R3 Subject 将多个事件源汇聚成单一流
3. 组件订阅这个流，而不是依赖父容器的 AABB

这是纯粹的**事件驱动 + 响应式编程**架构，完全符合 DesignPatterns.md 的组件化原则！

---

## 最新完成：TSItem 场景集成 GridShapeVisualComponent ✅

### 场景结构更新

**TSItem.tscn 新架构**:
```
TetrisDraggableItem (Control) - TSItemWrapper
├── InteractionArea (Control) [重命名自 VisualContainer]
│   ├── ClickableBackground (ColorRect)
│   ├── ItemIcon (TextureRect)
│   └── [GridShapeVisualComponent 生成的 ColorRect 方块]
├── StateChart (Node)
├── DraggableItemComponent (Node)
├── GridShapeComponent (Node) - 逻辑/数据层
└── GridShapeVisualComponent (Node) - 视觉/表现层 [新增]
```

### 关键配置

**GridShapeComponent**:
- `AutoResizeParent = true` - 自动调整父节点尺寸
- `VisualContainerPath = NodePath("../InteractionArea")`

**GridShapeVisualComponent** (新增):
- `GridShapeComponent = NodePath("../GridShapeComponent")` - 引用逻辑组件
- `InteractionArea = NodePath("../InteractionArea")` - 目标容器
- `CellSize = 64.0` - 方块尺寸

**InteractionArea**:
- 添加 `unique_name_in_owner = true` - 支持 % 引用
- `mouse_filter = 2` (Ignore) - 由 GridShapeVisualComponent 在运行时设置

### 数据流

```
TSItemWrapper (IItemDataProvider)
    ↓ DataInitialized event
GridShapeComponent
    ↓ Initializes CurrentLocalCells
    ↓ OnShapeChangedAsObservable
GridShapeVisualComponent
    ↓ RebuildVisualBlocks()
InteractionArea
    └── ColorRect[] (1x1 精确交互方块)
```

### 验证

✅ `dotnet build` 成功  
✅ 场景结构正确配置  
✅ NodePath 引用正确  
✅ Logic-Visual 组件成对集成  

### 下一步

- 在 Godot 编辑器中打开场景验证
- 测试物品拖拽和精确鼠标交互
- 验证旋转时方块自动重建
- 测试红绿光验证反馈

---

## 最新完成：GridShapeVisualComponent - 逻辑视觉配对命名 ✅

### 命名规范升级：Logic-Visual Pairing

**问题**: `ItemShapeBlocksComponent` 命名不清晰，无法体现与 `GridShapeComponent` 的强绑定关系。

**解决方案**: 采用**前缀一致 + 职能后缀**命名法

```
GridShapeComponent (逻辑/数据层)
    ↕ 强绑定关系
GridShapeVisualComponent (视觉/表现层)
```

**命名模式**: `[Domain][Aspect]Component`
- **Domain**: GridShape (共享前缀，建立认知链接)
- **Aspect**: Component (逻辑) vs Visual (视觉)

**优势**:
- ✅ **即时识别**: 开发者瞬间理解它们是成对出现的
- ✅ **可扩展**: 模式可延伸 (GridShapeSynergyComponent, GridShapeAudioComponent)
- ✅ **可维护**: 防止项目扩大后的"任意命名地狱"
- ✅ **认知效率**: 消除无关名称的心理映射开销

### 核心架构

**GridShapeVisualComponent 是纯响应式监听器**:
```csharp
// 订阅逻辑组件的变化事件
GridShapeComponent.OnShapeChangedAsObservable
    .Subscribe(_ => RebuildVisualBlocks())
    .AddTo(this);
```

**职责分离**:
- `GridShapeComponent`: 拥有数据，管理状态（旋转、归一化）
- `GridShapeVisualComponent`: 不拥有数据，订阅事件，生成视觉方块

**MouseFilter 架构**:
- `InteractionArea.MouseFilter = Ignore` - 父容器不拦截
- 每个 `ColorRect.MouseFilter = Pass` - 精确的 1x1 交互

### 文件变更

- ✅ 创建: `GridShapeVisualComponent.cs`
- ✅ 更新: `ComponentDesign_20260418_ShapeBlocks.md` (添加命名哲学章节)

### 验证

✅ `dotnet build` 成功  
✅ 逻辑-视觉命名配对建立  
✅ 严格命名规则执行 (Type-to-Variable)  
✅ 纯响应式监听器模式  

---

## 最新完成：ItemShapeBlocksComponent - 精确方块生成组件 ✅

### 问题背景
AABB (Axis-Aligned Bounding Box) 包围盒对不规则形状（如 L 形）创建矩形碰撞区域，导致空白区域也能被点击，鼠标交互不精确。

### 解决方案：1x1 方块生成

**核心设计**:
```csharp
// 父容器忽略鼠标，让子块精准接收事件
VisualContainer.MouseFilter = Control.MouseFilterEnum.Ignore;

// 为每个格子生成独立的 ColorRect
foreach (Vector2I cellPos in ShapeData.CurrentLocalCells)
{
    var cellBlock = new ColorRect
    {
        Size = new Vector2(CellSize, CellSize),
        Position = new Vector2(cellPos.X * CellSize, cellPos.Y * CellSize),
        MouseFilter = Control.MouseFilterEnum.Pass  // 精确交互
    };
}
```

**架构优势**:
- ✅ **像素级精确**: 只有实际格子可点击，空白区域不响应
- ✅ **视觉准确**: 交互区域与视觉表现完全匹配
- ✅ **响应式**: 订阅 OnShapeChangedAsObservable，旋转时自动重建
- ✅ **验证反馈**: 提供 SetValidationFeedback() API 用于拖拽时的红绿光反馈
- ✅ **轻量级**: ColorRect 性能开销极小

**新增文件**:
- `3d-practice/addons/A1TetrisBackpack/Items/ItemShapeBlocksComponent.cs`
- `KiroWorkingSpace/.kiro/Scratchpad/CodeAnalysis_20260418_AABBProblem.md`
- `KiroWorkingSpace/.kiro/Scratchpad/ComponentDesign_20260418_ShapeBlocks.md`

**下一步**:
- 集成到 TSItem 场景
- 更新 BackpackInteractionController 调用验证反馈方法
- 测试不规则形状的鼠标交互精度

---

## 最新完成：接口解耦的数据注入架构 ✅

### 问题背景
TSItemWrapper 需要向子节点 GridShapeComponent 传递 `ItemDataResource`，但 Godot 的 `_Ready()` 生命周期是子节点先执行，导致父节点无法在子节点初始化前注入数据。

### 初始方案的问题
使用 C# 事件模式虽然解决了生命周期问题，但引入了**强依赖**：
- GridShapeComponent 必须知道父节点是 `TSItemWrapper` 类型
- 违反了组件的通用性和可复用性原则

### 最终解决方案：Interface Segregation + Observer Pattern

**实现架构**:
```csharp
// 1. 定义接口（解耦关键）
public interface IItemDataProvider
{
    event Action<ItemDataResource> DataInitialized;
}

// 2. TSItemWrapper 实现接口
public partial class TSItemWrapper : Control, IItemDataProvider
{
    public event Action<ItemDataResource> DataInitialized;
    
    public override void _Ready()
    {
        DataInitialized?.Invoke(Data);
    }
}

// 3. GridShapeComponent 依赖接口而非具体类型
public override void _Ready()
{
    var parent = GetParent();
    if (parent is IItemDataProvider provider)  // 依赖接口
    {
        provider.DataInitialized += OnDataReceived;
    }
}
```

**优势**:
- ✅ 完全解耦：GridShapeComponent 不依赖具体的 TSItemWrapper 类型
- ✅ 高度可复用：任何实现 IItemDataProvider 的父节点都能工作
- ✅ 符合 SOLID 原则：依赖倒置原则（DIP）和接口隔离原则（ISP）
- ✅ 类型安全：编译时检查
- ✅ 易于扩展：新的 Wrapper 类只需实现接口即可
- ✅ 正确处理 Godot 生命周期顺序
- ✅ 内存安全：_ExitTree 中取消订阅

**修改文件**:
- `3d-practice/addons/A1TetrisBackpack/Items/IItemDataProvider.cs` (新增)
- `3d-practice/A1TesseractBackpack/TSItemWrapper.cs`
- `3d-practice/addons/A1TetrisBackpack/Items/GridShapeComponent.cs`

**文档更新**:
- `KiroWorkingSpace/.kiro/Scratchpad/CodeAnalysis_20260418_ReadyOrder.md` (标记为已解决)

## 当前任务：功能扩展与测试

### 已完成 ✅
1. **核心 MVC 架构**:
   - BackpackGridComponent (Model - 1D 数组网格逻辑)
   - BackpackGridUIComponent (View - 坐标转换)
   - BackpackInteractionController (Controller - 拖拽控制)

2. **基础拖拽系统**:
   - DraggableItemComponent (输入处理)
   - FollowMouseUIComponent (Power Switch 模式)
   - StateChart 集成 (Idle ↔ Dragging)
   - 吸附与回弹机制

3. **Bug 修复**:
   - Bug #1: NodePath 绑定问题
   - Bug #2: GuiInput 事件不触发 (mouse_filter 设置)
   - 防自我占用机制

4. **项目重命名**:
   - 文档重命名: GodotBackpackSystem_Context.md → GodotBackpackTesseractSys_Context.md
   - 统一 TS 命名规范

### 待测试功能 ⏳

#### 1. 旋转功能 (Rotation)
**组件**: `GridShapeComponent.Rotate90()`
**测试点**:
- [ ] 右键旋转触发
- [ ] 旋转矩阵应用: `(x,y) -> (-y,x)`
- [ ] NormalizeShape() 执行
- [ ] 旋转后放置检测
- [ ] 旋转后边界检查
- [ ] OnShapeChangedAsObservable 事件触发

**测试场景**:
```
1. 拖拽 L 形物品
2. 拖拽中按右键旋转
3. 验证形状视觉更新
4. 尝试放置到不同位置
5. 验证碰撞检测正确性
```

#### 2. 星星/协同系统 (Synergy System)
**组件**: `SynergyComponent`, `SynergyDataResource`
**测试点**:
- [ ] SynergyDataResource 创建 (.tres 资源)
- [ ] StarOffsets 配置
- [ ] ProvidedTags / RequiredTag 设置
- [ ] CheckSynergies() 逻辑
- [ ] 旋转后星星位置更新
- [ ] OnSynergyChangedAsObservable 事件
- [ ] UI 星星显示切换 (灰色 ↔ 亮色)

**测试场景**:
```
1. 创建两个物品资源 (A 提供 "Fire", B 需要 "Fire")
2. 配置物品 A 的 StarOffsets
3. 放置物品 A 到背包
4. 放置物品 B 到星星位置
5. 验证星星激活
6. 旋转物品 A，验证星星位置跟随
```

#### 3. UI 微交互 (Micro-Interactions)
**组件**: `UITweenInteractComponent`
**测试点**:
- [ ] 悬停缩放 (HoverScale: 1.05)
- [ ] 按下缩放 (PressScale: 0.95)
- [ ] Tween 平滑过渡
- [ ] PivotOffset 中心缩放
- [ ] 逻辑/视觉分离验证

**测试场景**:
```
1. 鼠标悬停物品 → 验证放大效果
2. 点击物品 → 验证缩小效果
3. 拖拽物品 → 验证 InteractionArea 不缩放
4. 验证坐标计算不受影响
```

#### 4. 多物品交互测试
**测试点**:
- [ ] 多个物品同时存在
- [ ] 物品间碰撞检测
- [ ] 物品重叠放置阻止
- [ ] 物品移除后空间释放
- [ ] 批量注册物品

**测试场景**:
```
1. 创建 3-5 个不同形状物品
2. 依次放置到背包
3. 尝试重叠放置 (应失败)
4. 移除中间物品
5. 在空出的位置放置新物品
```

### 下一步计划 📋

#### 短期任务 (本周)
1. **完成旋转功能测试**
   - 创建测试场景
   - 验证所有旋转边界情况
   - 修复发现的 bug

2. **实现星星系统 UI**
   - 创建 StarContainer 节点结构
   - 实现星星显示切换逻辑
   - 订阅 OnSynergyChangedAsObservable

3. **添加 UITweenInteractComponent**
   - 集成到物品场景
   - 测试所有交互状态
   - 验证性能影响

#### 中期任务 (下周)
1. **完善协同系统**
   - 实现 ItemData → Node 映射
   - 完成 CheckItemHasTag() 实现
   - 测试复杂协同链

2. **添加更多组件**
   - AutoShapeBuilderComponent (自动形状生成)
   - ItemTooltipComponent (物品提示)
   - BackpackSoundComponent (音效系统)

3. **性能优化**
   - 大量物品压力测试
   - R3 订阅优化
   - 内存泄漏检测

#### 长期目标
1. **高级功能**
   - 物品堆叠系统
   - 背包扩展机制
   - 物品过滤/搜索
   - 保存/加载系统

2. **编辑器工具**
   - 物品形状可视化编辑器
   - 协同配置工具
   - 背包布局预览

## 关键文件位置

### 核心代码
- **Core**: `3d-practice/addons/A1TetrisBackpack/Core/`
  - BackpackGridComponent.cs
  - BackpackGridUIComponent.cs
  - BackpackInteractionController.cs

- **Interaction**: `3d-practice/addons/A1TetrisBackpack/Interaction/`
  - DraggableItemComponent.cs
  - FollowMouseUIComponent.cs

- **Items**: `3d-practice/addons/A1TetrisBackpack/Items/`
  - GridShapeComponent.cs
  - ItemDataResource.cs

- **Synergies**: `3d-practice/addons/A1TetrisBackpack/Synergies/`
  - SynergyComponent.cs
  - SynergyDataResource.cs

- **MicroUI**: `3d-practice/addons/A1TetrisBackpack/MicroUI/`
  - UITweenInteractComponent.cs

### 场景和资源
- **TS 场景目录**: `3d-practice/A1TesseractBackpack/`
  - TSItem.tscn (物品场景模板)

### 测试场景
- **BackpackTest**: `3d-practice/Scenes/BackpackTest.tscn`
- **Test Controller**: `3d-practice/Tests/BackpackTestController.cs`

### 文档
- **系统文档**: `KiroWorkingSpace/.kiro/steering/Godot/GodotBackpackTesseractSys_Context.md`
- **设计模式**: `KiroWorkingSpace/.kiro/steering/Always/DesignPatterns.md`
- **主规则**: `KiroWorkingSpace/.kiro/steering/Always/MainRules.md`
- **项目规则**: `KiroWorkingSpace/.kiro/ProjectRules.md`

## 重要教训

### 技术教训
1. **mouse_filter 设置**: 纯视觉子节点必须设置为 Ignore (2)
2. **StateChart 事件**: 使用 `StateChart.Call("send_event", "event_name")`
3. **防自我占用**: 拾取时立即从网格移除
4. **坐标系统**: 使用 `ViewGrid.GetGlobalMousePosition()`
5. **Power Switch**: `AutoBindToParentState()` 自动管理生命周期

### 架构教训
1. **逻辑/视觉分离**: InteractionArea (Scale=1,1) + VisualTarget (可缩放)
2. **R3 内存管理**: 所有 Subject 必须在 `_ExitTree()` 中 Dispose
3. **MVC 解耦**: Controller 不直接操作 UI，通过 R3 事件通知
4. **1D 数组网格**: `index = y * Width + x`

## 启动下一个对话的步骤
1. 读取 `KiroWorkingSpace/.kiro/docLastConversationState.md`（本文件）
2. 读取 `KiroWorkingSpace/.kiro/ProjectRules.md`
3. 读取 `KiroWorkingSpace/.kiro/steering/Godot/GodotBackpackTesseractSys_Context.md`
4. 继续功能扩展和测试工作
