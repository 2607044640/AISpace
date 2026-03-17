---
inclusion: always
---

<context>
**Project:** 3D + UI, base template project
**Engine:** Godot 4.6.1 stable mono
**Language:** C# only

**Key Files:**
- Main Scene: `My2DMap.tscn`
- MCP Server: `Scripts/MCP/MCPServer.cs` (port 8765)
- Game State: `Scripts/MCP/GameStateCapture.cs`
- Test Scripts: `.kiro/scripts/testing/`
</context>

<completed_guides>
文档位于 `KiroWorkingSpace/.kiro/steering/OtherInstructions/`：

- **AnimationExport_Guide.md** - 动画自动导出指南
- **GodotInputMap.md** - Input Map配置指南
- **MixamoRetargeter_PluginUpdate.md** - Mixamo插件修复与改进
</completed_guides>

<class_references>
## Godot.Composition 架构

### 输入系统
- **BaseInputComponent.cs** (`addons/CoreComponents/`)
  - 抽象基类，定义输入事件接口
  - Events: `OnMovementInput`, `OnJumpJustPressed`
  - 方法: `TriggerMovementInput()`, `TriggerJumpInput()`

- **PlayerInputComponent.cs** (`addons/CoreComponents/`)
  - 继承 BaseInputComponent
  - 读取玩家键盘/手柄输入

- **AIInputComponent.cs** (`addons/CoreComponents/Examples/`)
  - 继承 BaseInputComponent
  - AI 决策输入（巡逻、追击）

### 核心组件
- **MovementComponent.cs** (`addons/CoreComponents/`)
  - 物理移动计算
  - Export: Speed, JumpVelocity, Gravity, Camera
  - 依赖: BaseInputComponent

- **CharacterRotationComponent.cs** (`addons/CoreComponents/`)
  - 角色朝向控制
  - Export: CharacterModelPath, Camera, RotationSpeed
  - 依赖: BaseInputComponent

- **AnimationControllerComponent.cs** (`addons/CoreComponents/`)
  - 动画状态机
  - Export: CharacterModelPath, AnimationPlayerPath, AnimationBlendTime, AnimConfig
  - 使用 AnimationNames 常量

- **CameraControlComponent.cs** (`addons/CoreComponents/`)
  - 第三人称相机控制（使用 PhantomCamera3D）
  - Export: PCamPath, MouseSensitivity, MinPitch, MaxPitch
  - API: `GetThirdPersonRotation()`, `SetThirdPersonRotation(Vector3)`

### 动画系统
- **AnimationNames.cs** (`addons/CoreComponents/Animation/`)
  - 静态常量类，消除魔法字符串
  - 常量: Idle, Run, Sprint, JumpStart, JumpLoop, etc.

- **AnimationSet.cs** (`addons/CoreComponents/Animation/`)
  - Resource类，集中管理角色所有动画
  - 包含Idle/Walk/Run/Sprint/Jump等动画
  - `SetupLoopModes()` - 自动设置动画循环模式
  - `GetAnimationSpeed()` - 获取动画速度

- **CharacterAnimationConfig.cs** (`addons/CoreComponents/Animation/`)
  - Resource类，角色动画配置（类似UE Data Asset）
  - 引用AnimationSet
  - `ApplyToAnimationPlayer()` - 应用配置到AnimationPlayer

### 工具类
- **ComponentExtensions.cs** (`addons/CoreComponents/`)
  - 扩展方法，简化组件查找
  - `GetComponentInChildren<T>()` - 查找组件（支持多态）
  - `FindAndSubscribeInput()` - 查找并订阅输入组件
  - `UnsubscribeInput()` - 取消订阅输入组件

### 实体
- **Player3D.cs** (`Scripts/`)
  - [Entity] 纯容器（10行代码）
  - 只调用 `InitializeEntity()`
  - 所有逻辑在组件中

## 第三方插件

### PhantomCamera (`addons/phantom_camera/`)
第三人称相机插件，GDScript 实现，提供 C# 包装类。

**场景配置：**

主场景（必需）：
```
Scene Root
└── Camera3D
    └── PhantomCameraHost (script: phantom_camera_host.gd)
```

Player 场景：
```
Player3D
└── PhantomCamera3D (script: phantom_camera_3d.gd)
    - follow_mode = 6 (ThirdPerson)
    - follow_target = NodePath("..")
    - follow_offset = Vector3(0, 0.6, 0)  # 防止相机贴地穿模
    - follow_distance = 4.0
    - spring_length = 4.0
    - priority = 10
    - collision_mask = 1  # 启用碰撞检测
    - shape = SphereShape3D (radius: 0.5)
    - margin = 0.5
```

**C# 使用：**
```csharp
using PhantomCamera;

// 获取并转换
Node3D pcamNode = parent.GetNode<Node3D>("PhantomCamera3D");
PhantomCamera3D pCam = pcamNode.AsPhantomCamera3D();

// 控制旋转
Vector3 rot = pCam.GetThirdPersonRotation();
rot.Y -= mouseX * sensitivity;  // Yaw
rot.X += mouseY * sensitivity;  // Pitch
pCam.SetThirdPersonRotation(rot);

// 可选：动态设置跟随偏移
pCam.FollowOffset = new Vector3(0, 0.6f, 0);
```

**关键 API：**
- `AsPhantomCamera3D()` - 转换为包装类
- `GetThirdPersonRotation()` / `SetThirdPersonRotation(Vector3)` - 欧拉角（弧度）
- `GetThirdPersonRotationDegrees()` / `SetThirdPersonRotationDegrees(Vector3)` - 欧拉角（角度）
- `FollowOffset` - 相机跟随偏移（Vector3）

**防穿模配置：**
1. **场景文件**：设置 `follow_offset.y = 0.6` 避免相机贴地
2. **碰撞检测**：配置 `collision_mask = 1`，`shape = SphereShape3D`，`margin = 0.5`
3. **CSG 物体**：确保设置 `collision_layer = 1` 和 `use_collision = true`

</class_references>
