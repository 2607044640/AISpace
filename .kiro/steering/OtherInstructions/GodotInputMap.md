---
inclusion: manual
---
# Godot Input Map 配置指南

<instructions>
## 编辑器配置流程

### 添加新动作
1. 打开 Project > Project Settings > Input Map
2. 在顶部输入框输入动作名（如 `jump`）
3. 点击 "Add" 按钮
4. 点击动作右侧的 "+" 按钮添加输入：
   - **键盘**：选择 "Key"，按下目标键
   - **鼠标**：选择 "Mouse Button"，选择按钮编号
   - **手柄按钮**：选择 "Joypad Buttons"，选择按钮编号
   - **手柄摇杆**：选择 "Joypad Axes"，选择轴和方向

### 修改现有动作
1. 找到目标动作
2. 点击 "+" 添加新输入，或点击输入右侧的 "x" 删除
3. 调整 Deadzone（死区）：点击动作展开，修改数值（默认 0.5）

### 删除动作
点击动作右侧的垃圾桶图标

## 何时需要重启

**不需要重启：**
- 在编辑器中修改 Input Map
- 添加/删除/修改动作
- 修改 Deadzone

**需要重新运行游戏：**
- 修改后测试新输入（F5 运行游戏）

**需要重启编辑器：**
- 手动编辑 `project.godot` 文件后
- Input Map 配置损坏时
</instructions>

<code_usage>
## 代码中使用 Input Map

### 检测按键状态
```csharp
// 按住检测（每帧）
if (Input.IsActionPressed("jump"))
{
    // 持续执行
}

// 按下瞬间检测（仅触发一次）
if (Input.IsActionJustPressed("jump"))
{
    velocity.Y = JumpVelocity;
}

// 释放瞬间检测
if (Input.IsActionJustReleased("jump"))
{
    // 跳跃结束
}
```

### 获取轴向输入
```csharp
// 单轴（-1.0 到 1.0）
float horizontal = Input.GetAxis("move_left", "move_right");
float vertical = Input.GetAxis("move_forward", "move_backward");

// 组合为 Vector2
Vector2 inputDir = Input.GetVector("move_left", "move_right", "move_forward", "move_backward");
```

### 获取输入强度
```csharp
// 返回 0.0 到 1.0（支持模拟输入）
float strength = Input.GetActionStrength("accelerate");
```

### 3D 移动示例
```csharp
public override void _PhysicsProcess(double delta)
{
    Vector2 inputDir = Input.GetVector("move_left", "move_right", "move_forward", "move_backward");
    Vector3 direction = (Transform.Basis * new Vector3(inputDir.X, 0, inputDir.Y)).Normalized();
    
    if (direction != Vector3.Zero)
    {
        velocity.X = direction.X * Speed;
        velocity.Z = direction.Z * Speed;
    }
    
    if (Input.IsActionJustPressed("jump") && IsOnFloor())
    {
        velocity.Y = JumpVelocity;
    }
    
    MoveAndSlide();
}
```
</code_usage>

<reference>
## 手柄按钮映射参考

### Xbox/PlayStation 按钮编号
| 编号 | Xbox      | PlayStation | 常用于     |
|------|-----------|-------------|------------|
| 0    | A         | Cross (×)   | 跳跃/确认  |
| 1    | B         | Circle (○)  | 取消/互动  |
| 2    | X         | Square (□)  | 重装/使用  |
| 3    | Y         | Triangle (△)| 切换视角   |
| 4    | LB        | L1          | 技能1      |
| 5    | RB        | R1          | 技能2      |
| 6    | LT        | L2          | 瞄准       |
| 7    | RT        | R2          | 攻击       |
| 8    | Back/View | Share       | 地图       |
| 9    | Start     | Options     | 菜单       |
| 10   | L3        | L3          | 冲刺       |
| 11   | R3        | R3          | 锁定       |

### 摇杆轴编号
| 轴 | 控制           | axis_value |
|----|----------------|------------|
| 0  | 左摇杆 X 轴    | -1.0 左, 1.0 右 |
| 1  | 左摇杆 Y 轴    | -1.0 上, 1.0 下 |
| 2  | 右摇杆 X 轴    | -1.0 左, 1.0 右 |
| 3  | 右摇杆 Y 轴    | -1.0 上, 1.0 下 |

### D-Pad（十字键）
使用 Joypad Buttons：
- 上：Button 12
- 下：Button 13
- 左：Button 14
- 右：Button 15
</reference>

<storage>
## 配置存储位置

Input Map 存储在 `project.godot` 文件的 `[input]` 部分：

```ini
[input]

jump={
"deadzone": 0.2,
"events": [Object(InputEventKey,"physical_keycode":32,...), Object(InputEventJoypadButton,"button_index":0,...)]
}
```

**直接编辑 project.godot：**
- 关闭 Godot 编辑器
- 编辑 `project.godot` 文件
- 重新打开编辑器（配置会自动加载）
</storage>

<common_patterns>
## 常用输入模式

### 第一人称移动
```csharp
move_forward    = W, Up, 左摇杆上
move_backward   = S, Down, 左摇杆下
move_left       = A, Left, 左摇杆左
move_right      = D, Right, 左摇杆右
jump            = Space, 手柄 A
crouch          = Ctrl, C, 手柄 B
sprint          = Shift, 手柄 L3
```

### 第三人称动作
```csharp
attack          = 左键, 手柄 RT
dodge           = Space, 手柄 B
lock_target     = 中键, 手柄 R3
interact        = E, 手柄 A
```

### 载具控制
```csharp
accelerate      = W, 手柄 RT
brake           = S, 手柄 LT
steer_left      = A, 左摇杆左
steer_right     = D, 左摇杆右
handbrake       = Space, 手柄 A
```
</common_patterns>

<troubleshooting>
## 常见问题

### 输入无响应
检查动作名拼写：`Input.IsActionPressed("jum")` ❌ → `"jump"` ✅

### 手柄不工作
1. 确认手柄已连接（运行前插入）
2. 检查 device 设置：`-1` = 所有设备，`0` = 第一个设备
3. 测试手柄：Project Settings > Input Map > 点击 "+" > 按手柄按钮查看识别

### 摇杆漂移
增加 Deadzone：展开动作 > 修改 deadzone 值（0.2 → 0.3）

### 输入延迟
使用 `_PhysicsProcess()` 而非 `_Process()`：
```csharp
public override void _PhysicsProcess(double delta) // ✅ 固定时间步
{
    if (Input.IsActionPressed("move")) { }
}
```
</troubleshooting>
