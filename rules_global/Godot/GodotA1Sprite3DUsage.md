---
inclusion: manual
---

# Godot A1Sprite3D Usage — 二渲三动画系统

2D 纸片人在 3D 世界中渲染的完整解决方案。支持 8 方向（或 4 方向）精灵动画、Montage 打断机制、帧事件回调。

## 核心设计

**完全不使用 AnimationPlayer。** 通过纯代码驱动 `Sprite3D.FrameCoords`：
- **X 轴（列）** = 动画帧，由内部计时器按 FPS 驱动
- **Y 轴（行）** = 方向，由摄像机角度实时计算

用户只需要"填表"（在 Inspector 中填写帧范围和 FPS），无需手动 K 关键帧。

## 文件结构

| 文件 | 类型 | 职责 |
|---|---|---|
| `BillboardDirection.cs` | 静态工具类 | 纯数学：摄像机角度 → 0~7 方向索引 |
| `BillboardAnimEntry.cs` | Resource 子资源 | 单条动画定义（名称、帧范围、FPS、Montage 标记） |
| `BillboardAnimConfig.cs` | Resource 资源 | 角色配置集合（图集、行列数、所有动画条目） |
| `BillboardAnimator.cs` | Node 组件 | 核心控制器（挂在 Entity 上，驱动 Sprite3D） |

## 快速开始

### 1. 准备 SpriteSheet

美术出图格式：横向 = 动画帧，纵向 = 方向。

```
         列0    列1    列2    列3
行0(S)  [walk0] [walk1] [walk2] [walk3]
行1(SW) [walk0] [walk1] [walk2] [walk3]
行2(W)  [walk0] [walk1] [walk2] [walk3]
...
行7(SE) [walk0] [walk1] [walk2] [walk3]
```

### 2. 创建 BillboardAnimConfig 资源

在 FileSystem 中右键 → New Resource → `BillboardAnimConfig`：
- 拖入你的 SpriteSheet 图片
- 设置 Columns（列数）和 Rows（行数）
- 在 Animations 数组中添加条目

### 3. 搭建场景

```
Enemy (CharacterBody3D) [Entity]
├── BillboardAnimator        ← 拖入 AnimConfig 资源
├── Sprite3D                 ← Billboard = Y-Billboard
└── AIInputComponent         ← 或 PlayerInputComponent
```

### 4. 代码使用

```csharp
using R3;

// 播放持续性动画（会被 AutoSelect 覆盖）
billboardAnimator.PlayAnimation("Walk");

// 播放打断型动画（不会被 AutoSelect 覆盖）
billboardAnimator.PlayMontage("Attack");

// 监听帧事件（如攻击第2帧生成伤害框）
billboardAnimator.AnimationFrameEvent
    .Where(e => e.animName == "Attack" && e.frameOffset == 2)
    .Subscribe(_ => SpawnHitbox())
    .AddTo(_disposables);

// 监听 Montage 结束
billboardAnimator.MontageFinished
    .Subscribe(animName => GD.Print($"{animName} 播放完毕"))
    .AddTo(_disposables);
```

## 与现有 3D 动画系统的关系

| 系统 | 适用场景 |
|---|---|
| `AnimationControllerComponent` + `CharacterAnimationConfig` | 3D 骨骼模型（如玩家角色） |
| `BillboardAnimator` + `BillboardAnimConfig` | 2.5D 纸片人（如怪物、NPC） |

**一个角色只挂其中一套，永远不会同时挂两套。**
