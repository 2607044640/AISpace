# 快速测试指南 - 点击检测调试

## 🎯 测试目标
验证 DraggableItemComponent 是否能正确接收鼠标点击事件

## ⚡ 快速步骤

### 1. 确保场景已重新生成
```bash
cd KiroWorkingSpace
python .kiro/scripts/temp/generate_backpack_test_v2.py
```

### 2. ⚠️ 在 Godot 中重新加载场景（关键步骤！）
- 如果 Godot 已打开 `BackpackTest.tscn`
- **必须点击编辑器顶部的 "Reload" 按钮**
- 或者关闭场景标签页后重新打开
- **不重新加载会看到旧版本的场景！**

### 3. 运行场景
- 按 F5 或点击 "Run Project"
- 场景会自动在 5 秒后停止

### 4. 疯狂点击蓝色方块
- 在 5 秒倒计时内
- 用鼠标左键疯狂点击蓝色方块（TestItem）
- 位置大约在屏幕中央偏左

### 5. 查看控制台输出

## ✅ 成功的标志

如果点击检测**正常工作**，你会看到：

```
═══════════════════════════════════════════════════════
DraggableItemComponent: _Ready() 被调用
═══════════════════════════════════════════════════════
✓ DraggableItemComponent: 自动使用父节点 'TestItem' 作为 ClickableArea
✓ DraggableItemComponent: ClickableArea 尺寸 = (64, 64), 位置 = (128, 128)
✓ DraggableItemComponent: ClickableArea.MouseFilter = Stop
✓ DraggableItemComponent: 已订阅 TestItem 的 GuiInput 事件
✓ DraggableItemComponent: 请在 (128, 128) 到 (192, 192) 区域内点击测试
[心跳] DraggableItemComponent 存活中... ClickableArea=TestItem
⏱️  倒计时: 4.0 秒后自动停止...

╔═══════════════════════════════════════════════════════╗
║ 🎯 GUI INPUT 事件触发！
║ 事件类型: InputEventMouseButton
║ 时间戳: 12345678
╚═══════════════════════════════════════════════════════╝
╔═══════════════════════════════════════════════════════╗
║ 🖱️  鼠标按键事件详情
║ 按键: Left
║ 按下状态: True
║ 位置: (32, 32)
║ 全局位置: (160, 160)
╚═══════════════════════════════════════════════════════╝
→ 检测到左键按下，调用 HandleDragStart()
DraggableItemComponent: 发送状态事件 'drag_start'
DraggableItemComponent: 拖拽开始
```

## ❌ 失败的标志

如果点击检测**仍然不工作**，你只会看到：

```
[心跳] DraggableItemComponent 存活中... ClickableArea=TestItem
⏱️  倒计时: 4.0 秒后自动停止...
⏱️  倒计时: 3.0 秒后自动停止...
⏱️  倒计时: 2.0 秒后自动停止...
```

**没有** `🎯 GUI INPUT 事件触发！` 消息

## 🔍 故障排查

### 问题 1: 没有看到心跳消息
- **原因**: 场景没有正确加载或 DraggableItemComponent 没有初始化
- **解决**: 检查编译是否成功，确认场景中有 TestItem 节点

### 问题 2: 有心跳但没有点击事件
- **原因**: MouseFilter 设置错误，或者点击位置不对
- **解决**: 
  - 检查心跳日志中的 `MouseFilter` 是否为 `Stop`
  - 确认点击在 `(128, 128)` 到 `(192, 192)` 区域内
  - 检查 ClickableBackground 的 MouseFilter 是否为 `Ignore`

### 问题 3: 场景行为没有改变
- **原因**: 忘记在 Godot 中重新加载场景
- **解决**: 点击 Godot 编辑器的 "Reload" 按钮

## 📊 调试信息说明

| 日志类型 | 含义 |
|---------|------|
| `═══` 边框 | 重要的初始化或事件边界 |
| `✓` 绿色勾 | 成功的操作 |
| `✗` 红色叉 | 失败的操作 |
| `[心跳]` | 组件存活证明（每 0.5 秒） |
| `⏱️` | 倒计时提示 |
| `🎯` | GUI 输入事件触发 |
| `🖱️` | 鼠标按键详情 |

## 🎓 关键知识点

### MouseFilter 值的含义
- `0` = **Stop**: 接收并消费输入事件
- `1` = **Pass**: 接收事件但传递给父节点
- `2` = **Ignore**: 完全忽略，让事件穿透

### 正确的层级设置
```
TestItem (Control)           MouseFilter = Stop   ← 接收事件
├── ClickableBackground      MouseFilter = Ignore ← 穿透
├── VisualContainer          MouseFilter = Ignore ← 穿透
│   └── ItemIcon             MouseFilter = Ignore ← 穿透
└── DraggableItemComponent   订阅 TestItem.GuiInput
```

### 为什么需要 Ignore？
- 子节点默认 MouseFilter = Stop
- 子节点会拦截所有点击，父节点收不到
- 设置为 Ignore 让点击"穿透"到父节点

## 📝 测试检查清单

- [ ] 运行了场景生成器脚本
- [ ] 在 Godot 中点击了 Reload 按钮
- [ ] 编译了 C# 代码（`dotnet build`）
- [ ] 运行了场景（F5）
- [ ] 看到了倒计时消息
- [ ] 看到了心跳消息
- [ ] 疯狂点击了蓝色方块
- [ ] 检查了控制台输出

## 🚀 下一步

如果测试成功：
- 移除或禁用心跳日志（太吵了）
- 简化 GUI 输入日志
- 继续实现拖拽功能

如果测试失败：
- 截图控制台输出
- 检查 Godot 场景树中 TestItem 的属性
- 使用 Godot 的 Remote 标签页查看运行时节点状态
