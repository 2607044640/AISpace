# 背包系统测试说明 V2

**生成时间：** 2026-04-15  
**场景路径：** `3d-practice/Scenes/BackpackTest.tscn`  
**基于：** 正确的 TscnBuilder API

---

## ✅ 已完成

1. **重新阅读核心文档** - GodotTscnBuilder, GodotUIBuilder, GodotStateChartBuilder
2. **场景生成成功** - BackpackTest.tscn 已使用正确的 API 创建
3. **C# 编译成功** - 所有组件编译通过
4. **场景结构完整** - 包含所有必需的组件和 StateChart

---

## 📋 接下来的操作

### 1. 在 Godot 中打开场景
```
文件 → 打开场景 → Scenes/BackpackTest.tscn
```

### 2. 运行场景测试
按 `F5` 或点击"运行当前场景"按钮

### 3. 测试功能清单

#### ✅ 基础拖拽测试
- [ ] **左键拖动物品** - 物品应该跟随鼠标移动
- [ ] **ZIndex 提升** - 拖动时物品应该显示在最上层
- [ ] **鼠标跟随** - 物品中心应该跟随鼠标位置

#### ✅ 旋转测试
- [ ] **右键旋转** - 右键点击物品应该旋转 90°
- [ ] **形状变换** - 旋转后形状应该正确变换（当前是 1x1，看不出效果）
- [ ] **旋转计数** - 控制台应该输出旋转次数

#### ✅ 放置测试
- [ ] **吸附到网格** - 放置到背包内应该自动对齐到网格
- [ ] **位置计算** - 物品应该精确对齐到格子
- [ ] **逻辑网格更新** - 控制台应该输出"物品已放置"

#### ✅ 回弹测试
- [ ] **边界外回弹** - 放置到背包外应该回到原位
- [ ] **碰撞回弹** - 放置到已占用格子应该回到原位（需要多个物品）
- [ ] **原位恢复** - 回弹后物品应该回到拾取前的位置

#### ✅ UI 微交互测试
- [ ] **悬停放大** - 鼠标悬停时物品应该放大到 1.05
- [ ] **按下缩小** - 按下时物品应该缩小到 0.95
- [ ] **平滑动画** - 缩放应该有平滑的过渡效果
- [ ] **快速打断** - 快速移动鼠标时动画应该平滑打断

---

## 🐛 预期问题与解决方案

### 问题 1：物品不响应鼠标事件
**原因：** Control 节点的 `mouse_filter` 可能设置为 `IGNORE`  
**解决：** 在 Godot 编辑器中选中 TestItem，设置 `Mouse Filter = Stop`

### 问题 2：StateChart 事件不触发
**原因：** godot_state_charts addon 未启用  
**解决：** 项目 → 项目设置 → 插件 → 启用 "Godot State Charts"

### 问题 3：物品初始位置不在网格内
**原因：** 初始 position 设置可能不正确  
**解决：** 在编辑器中手动调整 TestItem 的 Position 到 (128, 128)

### 问题 4：拖拽时物品不跟随鼠标
**原因：** FollowMouseUIComponent 的 TargetUI 引用可能不正确  
**解决：** 检查 FollowMouseUI 节点的 TargetUI 属性是否指向 TestItem

### 问题 5：放置时坐标计算错误
**原因：** BackpackPanel 的 GlobalPosition 可能不是 (0, 0)  
**解决：** 这是正常的，坐标转换会自动处理

---

## 📊 控制台输出示例

### 正常启动输出
```
BackpackGridComponent 初始化完成：10x6 = 60 格子
BackpackGridUIComponent: 初始化完成
SynergyComponent: 初始化完成
DraggableItemComponent: 初始化完成
FollowMouseUIComponent: 初始化完成
UITweenInteractComponent: 初始化完成
BackpackInteractionController: 初始化完成
```

### 拖拽操作输出
```
物品 TestItem 拾取：原位置 (128, 128)，网格坐标 (2, 2)
物品 test_item 已从网格 (2, 2) 移除
物品 test_item 已放置在 (3, 3)
物品 TestItem 吸附到网格 (3, 3)，全局位置 (192, 192)
```

### 旋转操作输出
```
物品 TestItem 已旋转 90°
SynergyComponent: 物品已旋转，当前旋转次数 = 1 (90°)
```

---

## 🔧 调试技巧

### 1. 查看网格线
- BackpackPanel 的 `DrawDebugLines` 已设置为 `true`
- 应该能看到 10x6 的网格线
- 如果看不到，检查 `_Draw()` 方法是否被调用

### 2. 检查 NodePath 绑定
在 Godot 编辑器中：
1. 选中 Controller 节点
2. 查看 Inspector 中的 `LogicGrid` 和 `ViewGrid` 属性
3. 确保它们正确指向对应的节点

### 3. 监控 StateChart 状态
1. 运行场景
2. 在远程场景树中选中 StateChart
3. 查看当前激活的状态（应该是 Idle）
4. 拖动物品时应该切换到 Dragging

### 4. 使用断点调试
在以下位置设置断点：
- `DraggableItemComponent.HandleGuiInput()` - 检查输入事件
- `BackpackInteractionController.HandleItemPickedUp()` - 检查拾取逻辑
- `BackpackInteractionController.HandleItemDropped()` - 检查放置逻辑

---

## 🚀 下一步开发

### 短期目标（测试通过后）
1. **创建 ItemDataResource.tres** - 定义 2x2 或 L 形物品
2. **添加多个测试物品** - 测试碰撞检测
3. **实现 ItemData → Node 映射** - 完成羁绊系统
4. **添加星星视觉效果** - 显示羁绊激活状态

### 中期目标
1. **创建物品预制件** - 标准化物品结构
2. **实现拖拽预览** - 显示绿色/红色高亮
3. **添加音效** - 拾取/放置/旋转/羁绊激活
4. **实现羁绊效果应用** - 实际的游戏效果

### 长期目标
1. **物品数据库** - 管理所有物品配置
2. **背包保存/加载** - 序列化系统
3. **物品拖拽动画** - 平滑的吸附动画
4. **自动整理功能** - 智能排列物品

---

## 📝 已知限制

1. **单物品测试** - 当前只有一个物品，无法测试碰撞
2. **无实际纹理** - 使用 ColorRect 占位符
3. **羁绊系统未完成** - CheckItemHasTag() 返回 false
4. **无拖拽预览** - 不显示放置是否合法
5. **形状固定** - ItemDataResource 未配置，使用默认 1x1

---

## ✅ 测试完成标准

当以下所有功能正常工作时，基础系统测试通过：

- [x] 场景生成成功
- [x] C# 编译成功
- [ ] 物品可以拖拽
- [ ] 物品可以旋转
- [ ] 放置到背包内自动吸附
- [ ] 放置到背包外自动回弹
- [ ] 悬停/按下动画正常
- [ ] 控制台输出正确

测试通过后，可以开始实现高级功能（羁绊系统、多物品、视觉效果等）。
