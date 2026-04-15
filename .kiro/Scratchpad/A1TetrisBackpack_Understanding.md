# A1TetrisBackpack Addon 理解文档

**生成时间：** 2026-04-15  
**目的：** 临时记录对 A1TetrisBackpack 插件的理解，用于生成测试场景

---

## 文件结构

```
3d-practice/addons/A1TetrisBackpack/
├── Core/                    # 核心层（MVC架构）
│   ├── BackpackGridComponent.cs          # Model：1D数组网格逻辑
│   ├── BackpackGridUIComponent.cs        # View：坐标转换 + 可视化
│   └── BackpackInteractionController.cs  # Controller：拖拽状态管理
├── Items/                   # 物品层
│   ├── ItemDataResource.cs               # 物品静态配置（Resource）
│   └── GridShapeComponent.cs             # 运行时形状 + 旋转
├── Interaction/             # 交互层
│   ├── DraggableItemComponent.cs         # GUI输入 → StateChart桥接
│   └── FollowMouseUIComponent.cs         # 鼠标跟随（Power Switch）
├── Synergies/               # 羁绊层
│   ├── SynergyDataResource.cs            # 羁绊配置（Resource）
│   └── SynergyComponent.cs               # 运行时羁绊检测
└── MicroUI/                 # 微交互层
    └── UITweenInteractComponent.cs       # 悬停/按下动画
```

---

## UID 映射表

| 组件 | UID | 路径 |
|------|-----|------|
| BackpackGridComponent | `uid://1rgai2oppf42` | Core/ |
| BackpackGridUIComponent | `uid://dkk5driwga8ql` | Core/ |
| BackpackInteractionController | `uid://drof8dtjnyqs3` | Core/ |
| ItemDataResource | `uid://lelpt5ux6h0d` | Items/ |
| GridShapeComponent | `uid://bbykh8wvhqtcj` | Items/ |
| DraggableItemComponent | `uid://bdka4obxtossd` | Interaction/ |
| FollowMouseUIComponent | `uid://d2svbqvyq43tw` | Interaction/ |
| SynergyComponent | `uid://d2044al4njiin` | Synergies/ |
| SynergyDataResource | `uid://crdecb4pdhdt2` | Synergies/ |
| UITweenInteractComponent | `uid://bp3kxm28rswm` | MicroUI/ |

---

## 依赖关系

### 数据流
```
ItemDataResource (静态) → GridShapeComponent (运行时)
                              ↓
BackpackGridComponent ← BackpackInteractionController → BackpackGridUIComponent
      (Model)                 (Controller)                    (View)
                              ↓
                    DraggableItemComponent → StateChart → FollowMouseUIComponent
```

### 关键引用需求

**BackpackInteractionController:**
- `[Export] BackpackGridComponent LogicGrid`
- `[Export] BackpackGridUIComponent ViewGrid`

**DraggableItemComponent:**
- `[Export] Control ClickableArea`
- `[Export] Node StateChart`

**FollowMouseUIComponent:**
- `[Export] Control TargetUI`
- `[Export] Vector2 GrabOffset`

**GridShapeComponent:**
- `[Export] ItemDataResource Data`

**SynergyComponent:**
- `[Export] SynergyDataResource SynergyData`
- `[Export] GridShapeComponent Shape`

**UITweenInteractComponent:**
- `[Export] Control InteractionArea`
- `[Export] Control VisualTarget`

---

## 测试场景需求

### 最小化场景结构
```
BackpackTest (Control, fullscreen)
└── BackpackPanel (BackpackGridUIComponent)
    ├── LogicGrid (BackpackGridComponent)
    ├── Controller (BackpackInteractionController)
    └── ItemsContainer
        └── TestItem (Control) ← InteractionArea
            ├── StateChart
            │   └── Root (CompoundState, initial="Idle")
            │       ├── Idle (AtomicState)
            │       └── Dragging (AtomicState)
            │           └── FollowMouseUI
            ├── Draggable
            ├── Shape
            ├── Synergy
            ├── TweenInteract
            └── VisualContainer ← VisualTarget
                └── ItemIcon (ColorRect占位符)
```

### 测试目标
1. ✅ 拖拽：左键拖动物品
2. ✅ 旋转：右键旋转物品
3. ✅ 吸附：放置成功时对齐网格
4. ✅ 回弹：放置失败时回到原位
5. ✅ 动画：悬停/按下缩放效果

### 暂不测试
- ❌ 羁绊系统（需要 ItemData→Node 映射）
- ❌ 实际纹理（使用 ColorRect）
- ❌ 星星视觉（暂时隐藏）

---

## 已知问题

1. **SynergyComponent.CheckItemHasTag() 未实现**
   - 需要 BackpackInteractionController 维护 `Dictionary<Vector2I, Node>`
   - 当前返回 false（占位实现）

2. **缺少 ItemDataResource 实例**
   - 需要创建 .tres 文件或在代码中初始化

3. **StateChart 依赖**
   - 需要 godot_state_charts addon
   - 需要正确的 UID 引用

---

## 下一步

1. 读取 UI 和 StateChart 模块文档
2. 生成测试场景 Python 脚本
3. 执行脚本生成 .tscn 文件
4. 编译 C# 代码
5. 运行测试场景
6. 根据错误调整
