# 上次对话状态

## 元数据
- **更新日期**: 2026-04-18
- **引擎**: Godot 4.6.1 stable mono
- **语言**: C# only
- **项目**: Tesseract Backpack (TS) - 完整网格背包系统（带协同效果）
- **阶段**: 核心架构完成，数据注入问题已解决

## 项目命名规范

### TS 前缀标准
- **项目名称**: Tesseract Backpack (TS)
- **旧代码库**: `3d-practice/addons/A1TetrisBackpack/` (C# 组件)
- **新项目目录**: `3d-practice/A1TesseractBackpack/` (场景和资源)
- **场景文件命名**: 使用 `TS` 前缀
  - 示例: `TSItem.tscn`
  - 位置: `3d-practice/A1TesseractBackpack/TSItem.tscn`
- **文档命名**: `GodotBackpackTesseractSys_Context.md`

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
