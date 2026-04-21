# GridCellUI架构升级 - 2026-04-21

## 架构决策记录

### 问题背景
原始的ColorRect方案虽然解决了L形AABB问题，但存在以下缺陷：
1. 视觉效果原始，缺乏专业感
2. 无法复用到背包网格UI
3. 状态管理分散，难以维护
4. 缺乏统一的视觉规范

### 解决方案：GridCellUI组件化架构

#### 核心组件

**1. GridCellUI.cs** - 统一的网格单元格UI组件
- **基类**：Panel（而非Node或ColorRect）
- **渲染技术**：StyleBoxFlat（Godot内置，高性能）
- **视觉效果**："透明体+发光边框"专业风格
- **状态管理**：枚举驱动（Normal, Valid, Invalid, Hover）
- **事件系统**：R3 Subject聚合输入事件

**关键设计决策**：
```csharp
// 使用StyleBoxFlat而非自定义shader
_styleBox = new StyleBoxFlat();
_styleBox.DrawCenter = true;  // 透明背景
_styleBox.BorderColor = ...;  // 发光边框
AddThemeStyleboxOverride("panel", _styleBox);
```

**2. ItemCellGroupController.cs** - 单元格集合控制器
- **职责**：管理GridCellUI实例集合，聚合事件流
- **替代**：GridShapeVisualComponent（旧组件）
- **架构模式**：Event Aggregator + Controller
- **关键突破**：完全绕过AABB问题，每个GridCellUI独立响应

**事件聚合实现**：
```csharp
gridCellUI.OnCellInputAsObservable
    .Subscribe(inputEvent => _aggregatedInputSubject.OnNext(inputEvent))
    .AddTo(gridCellUI);  // 生命周期绑定
```

**3. DraggableItemComponent.cs** - 更新订阅目标
- **旧引用**：GridShapeVisualComponent.OnBlockInputAsObservable
- **新引用**：ItemCellGroupController.OnGroupInputAsObservable
- **变更最小化**：仅修改引用路径，逻辑保持不变

### 架构优势

1. **可复用性**：GridCellUI可用于物品和背包网格
2. **性能优化**：StyleBoxFlat性能优于自定义shader
3. **组件解耦**：事件聚合模式保持组件独立性
4. **状态集中化**：枚举驱动的颜色管理
5. **视觉统一**：全局统一的"透明体+发光边框"风格

### 技术细节

#### StyleBoxFlat配置
```csharp
BorderWidth = 2f
NormalColor_Border = (1, 1, 1, 0.3)      // 半透明白边框
NormalColor_Background = (1, 1, 1, 0.05) // 几乎透明背景
ValidColor_Border = (0.2, 1, 0.2, 0.8)   // 绿色发光
InvalidColor_Border = (1, 0.2, 0.2, 0.8) // 红色发光
```

#### 鼠标事件处理
```csharp
// GridCellUI独立接收输入
MouseFilter = MouseFilterEnum.Pass

// 父容器忽略鼠标
InteractionArea.MouseFilter = MouseFilterEnum.Ignore
```

### 文件清单

**新增文件**：
- `3d-practice/addons/A1TetrisBackpack/UI/GridCellUI.cs`
- `3d-practice/addons/A1TetrisBackpack/Items/ItemCellGroupController.cs`

**修改文件**：
- `3d-practice/addons/A1TetrisBackpack/Interaction/DraggableItemComponent.cs`

**待废弃文件**：
- `3d-practice/addons/A1TetrisBackpack/Items/GridShapeVisualComponent.cs`（保留以供参考）

### 下一步工作

1. ✅ 编译验证通过
2. ⏳ 更新TSItem.tscn场景结构
3. ⏳ 运行测试验证视觉效果
4. ⏳ 应用GridCellUI到BackpackGridUIComponent
5. ⏳ 移除旧的GridShapeVisualComponent

### 架构模式总结

**Event Aggregator Pattern**：
- 多个离散事件源（GridCellUI实例）
- 单一聚合流（ItemCellGroupController.OnGroupInputAsObservable）
- 订阅者无需关心事件来源细节

**Controller Pattern**：
- ItemCellGroupController管理GridCellUI生命周期
- 提供统一的公共API（SetGroupState, ResetGroupState）
- 封装内部实现细节

**Component-Based Architecture**：
- GridCellUI：可复用的原子组件
- ItemCellGroupController：组合控制器
- DraggableItemComponent：行为组件
- 完全解耦，职责单一
