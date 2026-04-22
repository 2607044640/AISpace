# TSItem.tscn 场景重构指南
## 架构升级：GridShapeVisualComponent → ItemCellGroupController

---

## 📋 重构检查清单

### ✅ Phase 1: 清理旧节点

- [ ] **删除 GridShapeVisualComponent 节点**
  - 路径：`TetrisDraggableItem/GridShapeVisualComponent`
  - 原因：已被 ItemCellGroupController 替代
  
- [ ] **删除 ClickableBackground 节点**
  - 路径：`TetrisDraggableItem/InteractionArea/ClickableBackground`
  - 原因：GridCellUI 将动态生成视觉方块，不再需要占位符

---

### ✅ Phase 2: 添加新节点

- [ ] **添加 ItemCellGroupController 节点**
  - **父节点**：`TetrisDraggableItem`（根节点）
  - **节点类型**：`Node`
  - **节点名称**：`ItemCellGroupController`
  - **Unique Name**：✅ 启用（勾选 "Access as Unique Name"）
  - **脚本**：`res://addons/A1TetrisBackpack/Items/ItemCellGroupController.cs`

---

### ✅ Phase 3: 配置节点层级结构

**目标层级结构**：
```
TetrisDraggableItem (Control) ← ROOT
├── StateChart (Node)
│   └── Root (CompoundState)
│       ├── Idle (AtomicState)
│       │   └── ToDragging (Transition)
│       └── Dragging (AtomicState)
│           ├── ToIdle (Transition)
│           └── FollowMouseUIComponent (Node)
├── GridShapeComponent (Node)
├── ItemCellGroupController (Node) ← 新增
├── DraggableItemComponent (Node)
├── InteractionArea (Control)
│   └── ItemIcon (TextureRect)
└── (GridCellUI 将由 ItemCellGroupController 动态生成)
```

**节点顺序建议**：
1. StateChart
2. GridShapeComponent
3. ItemCellGroupController
4. DraggableItemComponent
5. InteractionArea

---

### ✅ Phase 4: 关键 Inspector 属性配置

#### 🔴 **CRITICAL: MouseFilter 设置（必须正确，否则AABB bug复现）**

**TetrisDraggableItem (根节点)**
- **Mouse Filter**: `Ignore` ⚠️ **必须设置为 Ignore**
- **Custom Minimum Size**: `(64, 64)`
- **Layout Mode**: `Anchors`
- **Script**: `TSItemWrapper.cs`

**InteractionArea**
- **Mouse Filter**: `Ignore` ⚠️ **必须设置为 Ignore**
- **Layout Mode**: `Full Rect`
- **Anchors**: `(0, 0, 1, 1)` - 填满父节点
- **Grow Horizontal**: `Both`
- **Grow Vertical**: `Both`

**ItemIcon (TextureRect)**
- **Mouse Filter**: `Ignore`
- **Expand Mode**: `Ignore Size`
- **Stretch Mode**: `Keep Aspect Centered`

---

#### 📌 **ItemCellGroupController 配置**

**Export 属性**：
| 属性名 | 类型 | 值 | 说明 |
|--------|------|-----|------|
| `GridShapeComp_Path` | NodePath | `%GridShapeComponent` | 指向逻辑数据源 |
| `InteractionArea_Path` | NodePath | `%InteractionArea` | 指向容器节点 |
| `CellSize` | float | `64.0` | 单个格子像素尺寸 |

**设置步骤**：
1. 选中 `ItemCellGroupController` 节点
2. 在 Inspector 中找到 "Script Variables" 部分
3. 点击 `GridShapeComp_Path` 右侧的 "Assign" 按钮
4. 选择 `%GridShapeComponent` 节点
5. 点击 `InteractionArea_Path` 右侧的 "Assign" 按钮
6. 选择 `%InteractionArea` 节点
7. 设置 `CellSize` 为 `64.0`

---

#### 📌 **DraggableItemComponent 配置**

**Export 属性**：
| 属性名 | 类型 | 值 | 说明 |
|--------|------|-----|------|
| `ItemCellGroupController_Path` | NodePath | `%ItemCellGroupController` | 指向新的控制器 |
| `StateChartPath` | NodePath | `%StateChart` | 指向状态机 |
| `DragStartEventName` | String | `"drag_start"` | 拖拽开始事件名 |
| `DragEndEventName` | String | `"drag_end"` | 拖拽结束事件名 |

**设置步骤**：
1. 选中 `DraggableItemComponent` 节点
2. 在 Inspector 中找到 "Script Variables" 部分
3. **删除旧的 `GridShapeVisualComponentPath` 属性**（如果存在）
4. 点击 `ItemCellGroupController_Path` 右侧的 "Assign" 按钮
5. 选择 `%ItemCellGroupController` 节点
6. 验证 `StateChartPath` 指向 `%StateChart`

---

#### 📌 **GridShapeComponent 配置**

**Export 属性**：
| 属性名 | 类型 | 值 | 说明 |
|--------|------|-----|------|
| `CellSize` | Vector2 | `(64, 64)` | 单个格子尺寸 |
| `AutoResizeParent` | bool | `false` | 不自动调整父节点尺寸 |
| `VisualContainerPath` | NodePath | `%InteractionArea` | 视觉容器路径 |

---

### ✅ Phase 5: 验证配置

**检查清单**：
- [ ] `TetrisDraggableItem` 的 MouseFilter = `Ignore`
- [ ] `InteractionArea` 的 MouseFilter = `Ignore`
- [ ] `ItemCellGroupController` 的 `GridShapeComp_Path` 指向 `%GridShapeComponent`
- [ ] `ItemCellGroupController` 的 `InteractionArea_Path` 指向 `%InteractionArea`
- [ ] `DraggableItemComponent` 的 `ItemCellGroupController_Path` 指向 `%ItemCellGroupController`
- [ ] 所有 NodePath 使用 `%` 前缀（Scene Unique Name）
- [ ] 旧的 `GridShapeVisualComponent` 节点已删除
- [ ] 旧的 `ClickableBackground` 节点已删除

---

### ✅ Phase 6: 运行时验证

**预期行为**：
1. ✅ 场景加载时，`ItemCellGroupController` 自动生成 GridCellUI 方块
2. ✅ L 形物品的空角区域不响应鼠标点击
3. ✅ 实际占用的格子显示"透明体+发光边框"效果
4. ✅ 鼠标悬停时边框高亮
5. ✅ 拖拽时显示绿色（有效）或红色（无效）反馈

**调试日志检查**：
```
[ItemCellGroupController] ItemCellGroupController._Ready() 开始
[ItemCellGroupController] GridShapeComponent引用有效: GridShapeComponent
[ItemCellGroupController] InteractionArea引用有效: InteractionArea
[ItemCellGroupController] InteractionArea.MouseFilter已设置为Ignore
[ItemCellGroupController] 已订阅GridShapeComponent.OnShapeChangedAsObservable
[ItemCellGroupController] 数据已存在，立即构建单元格
[ItemCellGroupController] RebuildCells() 开始
[ItemCellGroupController] 生成单元格 0: cellPos=(0, 0)
[ItemCellGroupController] 生成单元格 1: cellPos=(0, 1)
[ItemCellGroupController] 生成单元格 2: cellPos=(1, 1)
[ItemCellGroupController] RebuildCells() 完成，生成 3 个单元格
```

---

## 🚨 常见错误排查

### 错误 1: L 形空角仍然响应点击
**原因**：MouseFilter 未设置为 Ignore
**解决方案**：
1. 检查 `TetrisDraggableItem` 的 MouseFilter
2. 检查 `InteractionArea` 的 MouseFilter
3. 两者都必须设置为 `Ignore`

### 错误 2: NullReferenceException
**原因**：NodePath 配置错误
**解决方案**：
1. 确保所有 NodePath 使用 `%` 前缀
2. 确保目标节点启用了 "Access as Unique Name"
3. 重新分配 NodePath

### 错误 3: 没有视觉方块生成
**原因**：数据未注入或事件未触发
**解决方案**：
1. 检查 `TSItemWrapper` 是否正确触发 `DataInitialized` 事件
2. 检查 `GridShapeComponent` 是否正确初始化 `OnShapeChangedAsObservable`
3. 查看 Godot Output 日志

### 错误 4: 编译错误
**原因**：旧的引用未清理
**解决方案**：
1. 删除场景中的 `GridShapeVisualComponent` 节点
2. 运行 `dotnet build` 验证编译
3. 重新打开场景

---

## 📝 场景文件修改摘要

**删除的节点**：
- `GridShapeVisualComponent`
- `ClickableBackground`

**新增的节点**：
- `ItemCellGroupController`

**修改的属性**：
- `TetrisDraggableItem.MouseFilter`: `Pass` → `Ignore`
- `InteractionArea.MouseFilter`: `Pass` → `Ignore`
- `DraggableItemComponent.ItemCellGroupController_Path`: 新增

**保持不变的节点**：
- `StateChart` 及其子节点
- `GridShapeComponent`
- `InteractionArea`
- `ItemIcon`

---

## ✅ 完成标志

当你看到以下现象时，说明重构成功：
1. ✅ 场景加载无错误
2. ✅ L 形物品显示 3 个独立的发光边框方块
3. ✅ 点击 L 形空角无响应
4. ✅ 点击实际方块可以拖拽
5. ✅ 右键点击可以旋转
6. ✅ 拖拽时显示红绿反馈

---

## 🎯 下一步工作

完成 TSItem.tscn 重构后：
1. 测试 BackpackTest.tscn 场景
2. 应用 GridCellUI 到 BackpackGridUIComponent
3. 移除旧的 GridShapeVisualComponent.cs 文件
4. 更新其他使用该 Prefab 的场景
