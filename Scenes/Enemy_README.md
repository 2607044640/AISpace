# 敌人场景设计文档

## 概述
基于StateChart的敌人实体，支持飞行和地面两种移动模式。飞行时可被打断，强制进入地面模式3秒后自动恢复飞行。

**组件复用：** 完全复用A1MyAddon的核心组件，无需编写自定义移动逻辑。

## 场景结构

```
Enemy (CharacterBody3D) [Entity]
└── StateChart
    └── Movement (CompoundState, initial=Fly)
        ├── Fly (AtomicState)
        │   ├── FlyMovement (FlyMovementComponent from A1MyAddon)
        │   └── OnInterrupted (Transition) → Ground
        └── Ground (AtomicState)
            ├── GroundMovement (GroundMovementComponent from A1MyAddon)
            └── AutoRecover (Transition, 3s delay) → Fly
```

## 状态转换

### 1. Fly → Ground (被打断)
- **触发事件**: `on_interrupted`
- **触发方式**: `enemy.OnHit()`
- **效果**: 立即切换到地面模式，FlyMovement组件停止，GroundMovement组件激活

### 2. Ground → Fly (自动恢复)
- **触发条件**: 自动触发（空事件）
- **延迟**: 3秒
- **效果**: 3秒后自动恢复飞行，GroundMovement组件停止，FlyMovement组件激活

## 组件说明

### FlyMovementComponent (复用)
**来源:** `3d-practice/addons/A1MyAddon/CoreComponents/FlyMovementComponent.cs`

**特性:**
- 3D全向飞行，无重力
- 平滑加速/减速
- 支持相机相对移动
- 只在Fly状态激活时运行

**导出参数:**
- `FlySpeed`: 飞行速度 (默认: 8.0)
- `FlyAcceleration`: 加速度 (默认: 20.0)
- `FlyDeceleration`: 减速度 (默认: 15.0)
- `PhantomCameraPath`: 相机路径 (默认: "PhantomCamera3D")

### GroundMovementComponent (复用)
**来源:** `3d-practice/addons/A1MyAddon/CoreComponents/GroundMovementComponent.cs`

**特性:**
- 应用重力
- 地面碰撞检测
- 支持跳跃（可选）
- 只在Ground状态激活时运行

**导出参数:**
- `Speed`: 移动速度 (默认: 5.0)
- `JumpVelocity`: 跳跃速度 (默认: 4.5)
- `Gravity`: 重力加速度 (默认: 9.8)
- `PhantomCameraPath`: 相机路径 (默认: "PhantomCamera3D")

## 使用方法

### 在代码中触发打断
```csharp
// 获取敌人引用
var enemy = GetNode<Enemy>("Enemy");

// 触发打断（例如：被玩家攻击）
enemy.OnHit();
```

### 测试场景
运行 `EnemyTest.tscn` 进行测试：
- 敌人初始处于飞行模式
- 按空格键模拟击中敌人
- 敌人被打断并进入地面模式
- 3秒后自动恢复飞行

## 设计模式

### Power Switch Pattern
组件生命周期由StateChart控制：
- 状态激活 → 组件激活（`_PhysicsProcess`开始运行）
- 状态停用 → 组件停用（`_PhysicsProcess`停止运行）

### 组件复用
通过复用A1MyAddon的核心组件：
- 零自定义移动代码
- 自动获得所有组件功能（相机相对移动、平滑加速等）
- 与Player使用相同的移动逻辑，保证一致性
- 易于维护和更新

## 扩展建议

### 添加输入控制
如果需要AI或玩家控制敌人移动：

```python
# 在generate_enemy_scene.py中添加
fly.add_component("Input", "res://addons/A1MyAddon/CoreComponents/PlayerInputComponent.cs")
ground.add_component("Input", "res://addons/A1MyAddon/CoreComponents/PlayerInputComponent.cs")
```

或创建自定义AIInputComponent继承BaseInputComponent。

### 添加更多状态
```python
# 添加攻击状态
attacked = movement.add_atomic_state("Attacked")
attacked.add_component("AttackedBehavior", "res://Components/AttackedBehavior.cs")

# 添加转换
fly.add_transition("OnAttacked", to_state=attacked, event="on_attacked")
attacked.add_transition("Recover", to_state=fly, event="", delay=1.0)
```

### 添加并行维度
```python
# 创建并行根状态
root = statechart.add_parallel_state("Root")

# Movement维度
movement = root.add_compound_state("Movement", initial_state="Fly")
# ... (现有的Fly和Ground状态)

# Action维度（独立运行）
action = root.add_compound_state("Action", initial_state="Idle")
idle = action.add_atomic_state("Idle")
attacking = action.add_atomic_state("Attacking")
```

## 注意事项

1. **组件自动绑定:** FlyMovementComponent和GroundMovementComponent会自动调用`AutoBindToParentState()`
2. **无需输入组件:** 当前实现不需要输入，敌人静止悬浮。如需移动，添加InputComponent
3. **相机路径:** 如果场景中没有PhantomCamera3D，组件会使用实体本地坐标系
4. **延迟转换可被取消:** 如果在3秒内再次触发打断，延迟会重置

## 与Player的对比

| 特性 | Player | Enemy |
|------|--------|-------|
| 移动组件 | FlyMovementComponent + GroundMovementComponent | 相同 |
| 输入组件 | PlayerInputComponent | 无（可选添加AIInputComponent） |
| 状态切换 | 按F键手动切换 | 被击中自动切换 |
| 恢复机制 | 无 | 3秒后自动恢复飞行 |

## 生成脚本

使用 `.kiro/scripts/statechart_builder/generate_enemy_scene.py` 生成场景：

```bash
python .kiro/scripts/statechart_builder/generate_enemy_scene.py
```

生成的场景文件：`Scenes/Enemy.tscn`
