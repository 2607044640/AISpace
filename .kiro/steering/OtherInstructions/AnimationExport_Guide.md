---
inclusion: manual
---

# Godot动画自动导出完整指南

## 概述
本指南介绍如何使用EditorScenePostImport脚本自动将GLB/FBX文件中的所有动画批量导出为独立的`.res`资源文件，并通过C# Export变量实现可视化管理。

**适用场景：**
- 从Mixamo等平台下载的角色模型（包含多个动画）
- 需要在多个场景中复用动画
- 希望通过Inspector可视化管理动画路径

---

## 核心问题：Import Script UID加载失败

### 问题表现
创建EditorScenePostImport脚本后，Godot报错：
```
Couldn't load post-import script: uid://xxxxx
```

### 根本原因
Godot 4.x的import系统在某些情况下无法通过UID正确加载EditorScenePostImport脚本，特别是：
- 脚本刚创建时
- UID缓存未同步时
- 使用外部工具（如AI、文本编辑器）创建脚本时

### 解决方案
**将import script路径从UID改为直接文件路径**

修改`.glb.import`或`.fbx.import`文件：
```diff
- import_script/path="uid://ct2g8eln8f3in"
+ import_script/path="res://your_import_script.gd"
```

**为什么文件路径更可靠？**
1. 不依赖UID缓存同步
2. 不受`.godot/uid_cache.bin`影响
3. 对于import scripts，Godot优先支持直接路径

---

## 实现步骤

### 步骤1：创建批量导出脚本

创建`sophia_import.gd`（或其他名称）：

```gdscript
@tool
extends EditorScenePostImport

func _post_import(scene: Node) -> Object:
	print("=== Post-Import: Starting ===")
	
	# 查找AnimationPlayer
	var anim_player = find_animation_player(scene)
	if anim_player == null:
		push_warning("No AnimationPlayer found in scene")
		return scene
	
	print("Found AnimationPlayer with ", anim_player.get_animation_list().size(), " animations")
	
	# 设置保存目录
	var save_dir = "res://animations/"  # 修改为你的目标路径
	
	# 确保目录存在
	if not DirAccess.dir_exists_absolute(save_dir):
		DirAccess.make_dir_recursive_absolute(save_dir)
		print("Created directory: ", save_dir)
	
	# 保存每个动画
	var saved_count = 0
	for anim_name in anim_player.get_animation_list():
		var anim = anim_player.get_animation(anim_name)
		var save_path = save_dir + anim_name + ".res"
		
		var err = ResourceSaver.save(anim, save_path)
		if err == OK:
			print("✓ Saved animation: ", anim_name, " -> ", save_path)
			saved_count += 1
		else:
			push_error("✗ Failed to save animation: ", anim_name, " (Error: ", err, ")")
	
	print("=== Post-Import: Complete (", saved_count, "/", anim_player.get_animation_list().size(), " saved) ===")
	
	return scene

func find_animation_player(node: Node) -> AnimationPlayer:
	if node is AnimationPlayer:
		return node
	
	for child in node.get_children():
		var result = find_animation_player(child)
		if result != null:
			return result
	
	return null
```

### 步骤2：修复Import配置

**方法A：手动编辑.import文件（推荐）**

1. 找到目标文件的`.import`文件（如`sophia.glb.import`）
2. 找到`import_script/path`行
3. 修改为：
   ```ini
   import_script/path="res://sophia_import.gd"
   ```

**方法B：通过编辑器配置（可能遇到UID问题）**

1. 选中GLB/FBX文件
2. 在Import面板 → Advanced → Import Script
3. 选择你的脚本文件
4. 如果遇到UID错误，使用方法A

### 步骤3：触发导入

1. 在FileSystem中右键点击GLB/FBX文件
2. 选择"Reimport"
3. 查看Output面板，应该看到：
   ```
   === Post-Import: Starting ===
   Found AnimationPlayer with 8 animations
   ✓ Saved animation: Run -> res://animations/Run.res
   ✓ Saved animation: Idle -> res://animations/Idle.res
   ...
   === Post-Import: Complete (8/8 saved) ===
   ```

### 步骤4：在C#中使用Export变量管理

修改你的角色控制器脚本：

```csharp
using Godot;

public partial class Player3D : CharacterBody3D
{
	// Export变量 - 可在Inspector中拖拽
	[Export] public Animation FastRunAnimation;
	[Export] public Animation IdleAnimation;
	[Export] public Animation RunAnimation;
	
	private AnimationPlayer _animPlayer;
	private string _currentAnimation = "";

	public override void _Ready()
	{
		_animPlayer = GetNode<AnimationPlayer>("SophiaSkin/AnimationPlayer");
		LoadExportedAnimations();
	}

	private void LoadExportedAnimations()
	{
		// 获取或创建AnimationLibrary
		AnimationLibrary library;
		if (_animPlayer.HasAnimationLibrary(""))
		{
			library = _animPlayer.GetAnimationLibrary("");
		}
		else
		{
			library = new AnimationLibrary();
			_animPlayer.AddAnimationLibrary("", library);
		}
		
		// 添加Export的动画
		if (FastRunAnimation != null && !library.HasAnimation("FastRun"))
		{
			library.AddAnimation("FastRun", FastRunAnimation);
			GD.Print("✓ Loaded FastRun animation");
		}
		
		if (IdleAnimation != null && !library.HasAnimation("Idle"))
		{
			library.AddAnimation("Idle", IdleAnimation);
			GD.Print("✓ Loaded Idle animation");
		}
		
		if (RunAnimation != null && !library.HasAnimation("Run"))
		{
			library.AddAnimation("Run", RunAnimation);
			GD.Print("✓ Loaded Run animation");
		}
	}

	private void PlayAnimation(string animName)
	{
		if (_currentAnimation != animName && _animPlayer.HasAnimation(animName))
		{
			_animPlayer.Play(animName);
			_currentAnimation = animName;
		}
	}

	public override void _PhysicsProcess(double delta)
	{
		// 示例：根据移动状态播放动画
		Vector2 inputDir = Input.GetVector("move_left", "move_right", "move_forward", "move_backward");
		
		if (inputDir != Vector2.Zero)
		{
			if (Input.IsActionPressed("sprint"))
			{
				PlayAnimation("FastRun");
			}
			else
			{
				PlayAnimation("Run");
			}
		}
		else
		{
			PlayAnimation("Idle");
		}
		
		// ... 其他移动逻辑
	}
}
```

### 步骤5：在编辑器中配置

1. 编译C#代码：
   ```cmd
   dotnet build "YourProject.sln"
   ```

2. 在Godot编辑器中：
   - 选中Player3D节点
   - 在Inspector中找到Export变量
   - 从FileSystem拖拽对应的`.res`文件到槽位

3. 保存场景（Ctrl+S）

4. 测试（F5）

---

## 技术说明

### UID vs 文件路径对比

| 特性 | UID路径 | 文件路径 |
|------|---------|----------|
| 格式 | `uid://ct2g8eln8f3in` | `res://script.gd` |
| 依赖 | UID缓存系统 | 文件系统 |
| 可靠性 | 可能失败 | 稳定 |
| 适用场景 | 普通资源引用 | Import scripts |

### Export变量的优势

**类似UE的蓝图变量：**
- 可视化管理
- 拖拽操作
- 不需要硬编码路径
- 易于调整和测试

**代码示例对比：**

```csharp
// ❌ 硬编码路径
var anim = GD.Load<Animation>("res://animations/Run.res");

// ✅ Export变量
[Export] public Animation RunAnimation;  // 在Inspector中拖拽
```

### AnimationLibrary管理

Godot 4.x使用AnimationLibrary管理动画：
- 默认库名为空字符串`""`
- 可以创建多个命名库
- 动画名在库内必须唯一

---

## 常见问题

### Q1: Import脚本没有执行
**检查：**
1. `.import`文件中的路径是否正确
2. 脚本是否继承自`EditorScenePostImport`
3. 脚本开头是否有`@tool`标记
4. Output面板是否有错误信息

**解决：**
- 确保使用文件路径而非UID
- 重新Reimport文件
- 检查脚本语法

### Q2: 找不到AnimationPlayer
**错误信息：**
```
No AnimationPlayer found in scene
```

**解决：**
- 检查GLB/FBX文件是否包含动画
- 在Advanced Import Settings中查看场景结构
- 确认AnimationPlayer节点存在

### Q3: 动画不播放
**检查：**
1. Inspector中的Export变量是否已填充
2. Output面板是否显示"✓ Loaded XXX animation"
3. AnimationPlayer路径是否正确
4. 动画名是否匹配

### Q4: 编译错误
**常见错误：**
```
CS0246: The type or namespace name 'Animation' could not be found
```

**解决：**
- 确保使用`using Godot;`
- 检查Godot版本（需要4.0+）
- 重新生成C#项目

---

## 备用方案：手动导出

如果自动导出失败，可以手动配置：

1. 双击GLB/FBX文件打开Advanced Import Settings
2. 选中左侧的`AnimationPlayer`节点
3. 在右侧滚动到`Animation`标签
4. 对每个动画：
   - 展开动画名称
   - 勾选`save_to_file/enabled`
   - 设置路径：`res://animations/[AnimationName].res`
5. 点击`Reimport`

---

## 最佳实践

1. **目录结构：**
   ```
   project/
   ├── characters/
   │   └── sophia/
   │       ├── model/
   │       │   └── sophia.glb
   │       ├── animations/      # 导出的动画
   │       │   ├── Run.res
   │       │   ├── Idle.res
   │       │   └── Jump.res
   │       └── import_script.gd
   ```

2. **命名规范：**
   - 动画名使用PascalCase：`FastRun`, `Idle`, `Jump`
   - 文件名与动画名一致
   - Export变量名清晰：`FastRunAnimation`, `IdleAnimation`

3. **版本控制：**
   - 提交`.import`文件
   - 提交导出的`.res`文件
   - 提交import脚本

4. **性能优化：**
   - 只导出需要的动画
   - 使用AnimationLibrary分组管理
   - 避免重复加载

---

## 相关资源

- [Godot C# Export Hints](https://readmedium.com/the-power-of-godot-c-export-hints-godot-4-c-ba4504150804)
- [EditorScenePostImport文档](https://docs.godotengine.org/en/stable/classes/class_editorscenepostimport.html)
- [AnimationLibrary文档](https://docs.godotengine.org/en/stable/classes/class_animationlibrary.html)

---

## 总结

通过EditorScenePostImport脚本 + C# Export变量的组合：
1. 自动批量导出所有动画
2. 可视化管理动画引用
3. 避免硬编码路径
4. 类似UE的工作流程

**关键要点：**
- Import script使用文件路径而非UID
- Export变量提供可视化管理
- AnimationLibrary统一管理动画资源
