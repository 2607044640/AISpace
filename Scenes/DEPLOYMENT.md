# Enemy场景部署说明

## 重要提示

Enemy场景使用了A1MyAddon的核心组件，这些组件位于 `3d-practice` 项目中。

## 部署步骤

### 方案1：移动到3d-practice项目（推荐）

将以下文件复制到 `3d-practice` 项目：

```
KiroWorkingSpace/Scenes/Enemy.tscn 
  → 3d-practice/Scenes/Enemy.tscn

KiroWorkingSpace/B1Scripts/Enemy.cs 
  → 3d-practice/B1Scripts/Enemy.cs

KiroWorkingSpace/Scenes/EnemyTest.tscn 
  → 3d-practice/Scenes/EnemyTest.tscn

KiroWorkingSpace/B1Scripts/EnemyTestScene.cs 
  → 3d-practice/B1Scripts/EnemyTestScene.cs
```

### 方案2：复制A1MyAddon到KiroWorkingSpace

如果需要在KiroWorkingSpace中运行，复制整个A1MyAddon：

```
3d-practice/addons/A1MyAddon 
  → KiroWorkingSpace/addons/A1MyAddon
```

同时需要复制依赖：
- `3d-practice/addons/godot_state_charts` → `KiroWorkingSpace/addons/godot_state_charts`
- Godot.Composition插件

## 组件依赖

Enemy场景依赖以下A1MyAddon组件：

1. **FlyMovementComponent**
   - 路径: `res://addons/A1MyAddon/CoreComponents/FlyMovementComponent.cs`
   - 功能: 3D飞行移动

2. **GroundMovementComponent**
   - 路径: `res://addons/A1MyAddon/CoreComponents/GroundMovementComponent.cs`
   - 功能: 地面移动+重力

3. **StateChartAutoBindExtensions**
   - 路径: `res://addons/A1MyAddon/CoreComponents/Extenstions/StateChartAutoBindExtensions.cs`
   - 功能: Power Switch模式支持

## 测试

在3d-practice项目中：

1. 打开 `Scenes/EnemyTest.tscn`
2. 运行场景（F6）
3. 按空格键触发敌人被击中
4. 观察敌人从飞行模式切换到地面模式
5. 3秒后自动恢复飞行

## 生成脚本

如需重新生成场景：

```bash
cd KiroWorkingSpace
python .kiro/scripts/statechart_builder/generate_enemy_scene.py
```

生成的场景会自动引用A1MyAddon的组件路径。
