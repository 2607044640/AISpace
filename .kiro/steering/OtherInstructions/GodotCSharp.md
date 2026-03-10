---
inclusion: manual
---

# Godot C# 精简参考

<critical_rules>
## 必须遵守的规则

```csharp
// 所有 Godot 类必须用 partial
public partial class Player : Node2D  // ✓
public class Player : Node2D          // ✗ 编译错误
```

**删除节点：**
```csharp
QueueFree();  // ✓ 帧结束时删除，安全
Free();       // ✗ 立即删除，可能崩溃
```

**线程安全：**
```csharp
// ✗ 错误 - Task.Delay 后操作节点会崩溃
await Task.Delay(1000);
AddChild(node);

// ✓ 正确 - 使用 CallDeferred
await Task.Delay(1000);
CallDeferred(MethodName.AddChild, node);
```

**缓存节点引用：**
```csharp
// ✗ 每帧遍历树，慢 10-100 倍
public override void _Process(double delta)
{
    GetNode<Sprite2D>("Sprite").Position += Vector2.Right;
}

// ✓ 在 _Ready 中缓存
private Sprite2D _sprite;
public override void _Ready() { _sprite = GetNode<Sprite2D>("Sprite"); }
public override void _Process(double delta) { _sprite.Position += Vector2.Right; }
```
</critical_rules>

<when_to_use>
## 何时使用什么

### Autoload（全局单例）
**使用场景：**
- 游戏管理器（分数、关卡、状态）
- 音频管理器
- 存档系统
- 场景管理器
- 输入管理器

**创建步骤：**
1. Project Settings > Autoload
2. 添加脚本，设置名称
3. 代码访问：`GameManager.Instance.Score`

```csharp
public partial class GameManager : Node
{
    public static GameManager Instance { get; private set; }
    public int Score { get; set; }
    
    public override void _Ready() { Instance = this; }
}
```

### 抽象类 vs 接口
**抽象类 - 用于共享实现：**
```csharp
public abstract partial class Entity : Node2D
{
    [Export] public int Health { get; set; } = 100;
    public abstract void TakeDamage(int amount);
    
    // 共享方法
    public void Die() { QueueFree(); }
}
```

**接口 - 用于多重继承：**
```csharp
public interface IDamageable { void TakeDamage(int amount); }
public interface IInteractable { void Interact(); }

public partial class Chest : StaticBody2D, IDamageable, IInteractable
{
    public void TakeDamage(int amount) { }
    public void Interact() { }
}
```

### 信号 vs 直接调用
**信号 - 低频事件：**
- 按钮点击
- 生命值变化
- 游戏状态改变
- 跨节点通信

**直接调用 - 高频更新：**
- _Process / _PhysicsProcess 中的逻辑
- 性能关键路径
- 信号比直接调用慢 2-5 倍

```csharp
// ✗ 高频用信号，性能差
public override void _Process(double delta)
{
    EmitSignal(SignalName.PositionUpdated, Position);
}

// ✓ 高频用直接调用
private Action<Vector2> _onPositionChanged;
public override void _Process(double delta)
{
    _onPositionChanged?.Invoke(Position);
}
```

### _Process vs _PhysicsProcess
**_Process - 视觉和 UI：**
- 动画更新
- UI 逻辑
- 粒子效果
- 相机跟随

**_PhysicsProcess - 物理和移动：**
- 角色移动
- 碰撞检测
- 物理计算
- 固定时间步长（60 FPS）

### Area2D vs CharacterBody2D
**Area2D - 触发区域：**
- 拾取物品
- 触发器
- 检测范围
- 不需要物理响应

**CharacterBody2D - 角色物理：**
- 玩家控制
- 敌人移动
- 需要碰撞响应
- MoveAndSlide()

### Resource vs JSON
**Resource - 游戏数据：**
- 物品数据
- 敌人配置
- 关卡设置
- 可在编辑器中编辑
- 类型安全

**JSON - 存档数据：**
- 玩家进度
- 设置选项
- 运行时数据
- 跨平台兼容

**ConfigFile - 配置文件：**
- 游戏设置
- INI 格式
- Section 分组
- 简单键值对

### Tween vs AnimationPlayer
**Tween - 代码动画：**
- 简单属性动画
- UI 动画
- 程序化动画
- 运行时创建

**AnimationPlayer - 复杂动画：**
- 角色动画
- 多属性同步
- 关键帧动画
- 在编辑器中设计

### Struct vs Class
**Struct - 小数据：**
- 数据容器（< 16 字节）
- 频繁创建的临时对象
- 栈分配，无 GC 压力

```csharp
public struct DamageInfo
{
    public int Amount;
    public Vector2 Position;
}
```

**Class - 复杂对象：**
- 大对象
- 需要继承
- 需要引用语义
</when_to_use>

<data_import>
## CSV/Excel 数据导入

**直接读取 CSV：**
```csharp
public static Dictionary<int, ItemData> LoadCSV(string path)
{
    var items = new Dictionary<int, ItemData>();
    var file = FileAccess.Open(path, FileAccess.ModeFlags.Read);
    if (file == null) return items;
    
    file.GetCsvLine(); // 跳过标题
    while (!file.EofReached())
    {
        var line = file.GetCsvLine();
        if (line.Length < 3) continue;
        
        items[line[0].ToInt()] = new ItemData
        {
            ItemId = line[0].ToInt(),
            ItemName = line[1],
            Price = line[2].ToInt()
        };
    }
    file.Close();
    return items;
}
```

**CSV 格式：**
```csv
ItemId,ItemName,Price
1,剑,100
2,盾,80
```
</data_import>

<performance>
## 性能关键点

**避免 Marshalling 开销：**
```csharp
// ✗ 每次循环都调用 Godot API
for (int i = 0; i < 1000; i++)
    Position += Vector2.Right;

// ✓ 缓存到本地变量
Vector2 pos = Position;
for (int i = 0; i < 1000; i++)
    pos += Vector2.Right;
Position = pos;
```

**避免 LINQ 在热路径：**
```csharp
// ✗ _Process 中用 LINQ
public override void _Process(double delta)
{
    var active = enemies.Where(e => e.IsActive).ToList();
}

// ✓ 传统循环
public override void _Process(double delta)
{
    activeEnemies.Clear();
    foreach (var e in enemies)
        if (e.IsActive) activeEnemies.Add(e);
}
```

**反射性能：**
- 反射比直接访问慢 10-100 倍
- 只在 _Ready 中使用
- 缓存反射结果

**对象池：**
```csharp
public partial class BulletPool : Node
{
    private List<Bullet> _pool = new();
    
    public override void _Ready()
    {
        for (int i = 0; i < 20; i++)
        {
            var bullet = BulletScene.Instantiate<Bullet>();
            bullet.Visible = false;
            AddChild(bullet);
            _pool.Add(bullet);
        }
    }
    
    public Bullet Get()
    {
        foreach (var b in _pool)
            if (!b.Visible) { b.Visible = true; return b; }
        return null;
    }
}
```
</performance>

<common_patterns>
## 常用模式

### 状态机
```csharp
public enum State { Idle, Running, Jumping }
private State _state = State.Idle;

public override void _PhysicsProcess(double delta)
{
    switch (_state)
    {
        case State.Idle: HandleIdle(); break;
        case State.Running: HandleRunning(); break;
        case State.Jumping: HandleJumping(); break;
    }
}
```

### 服务定位器
```csharp
public partial class ServiceLocator : Node
{
    public static ServiceLocator Instance { get; private set; }
    private Dictionary<Type, object> _services = new();
    
    public void Register<T>(T service) { _services[typeof(T)] = service; }
    public T Get<T>() { return (T)_services[typeof(T)]; }
}

// 使用
ServiceLocator.Instance.Register<IAudioManager>(audioManager);
var audio = ServiceLocator.Instance.Get<IAudioManager>();
```
</common_patterns>

<input>
## 输入处理

**Input.GetVector - 简化方向输入：**
```csharp
// 自动归一化，处理四个方向
Vector2 dir = Input.GetVector("left", "right", "up", "down");
Velocity = dir * Speed;
```

**Input Actions vs 直接检测：**
- Input Actions：推荐，可重新绑定
- 直接检测：特殊情况（鼠标位置、手柄摇杆）

```csharp
// Input Actions
if (Input.IsActionJustPressed("jump")) Jump();

// 直接检测
if (@event is InputEventMouseButton mb && mb.Pressed)
    OnClick(mb.Position);
```
</input>

<export>
## Export 属性

**基本类型：**
```csharp
[Export] public int Health = 100;
[Export(PropertyHint.Range, "0,100")] public int Percentage = 50;
[Export(PropertyHint.File, "*.png")] public string TexturePath;
```

**类型限制：**
```csharp
// ✗ 不能 Export
[Export] public List<int> Numbers;  // System.Collections

// ✓ 可以 Export
[Export] public Godot.Collections.Array<int> Numbers;
[Export] public ItemData Item;  // Resource
```

**导出组：**
```csharp
[ExportGroup("Movement")]
[Export] public float Speed = 300;
[Export] public float JumpForce = 400;

[ExportGroup("Combat")]
[Export] public int MaxHealth = 100;
```
</export>

<async>
## 异步编程

**ToSignal - 等待信号：**
```csharp
await ToSignal(GetTree().CreateTimer(1.0), Timer.SignalName.Timeout);

Tween tween = CreateTween();
tween.TweenProperty(this, "position", target, 2.0);
await ToSignal(tween, Tween.SignalName.Finished);
```

**后台加载：**
```csharp
public async Task<PackedScene> LoadAsync(string path)
{
    ResourceLoader.LoadThreadedRequest(path);
    
    while (true)
    {
        var progress = new Godot.Collections.Array();
        var status = ResourceLoader.LoadThreadedGetStatus(path, progress);
        
        if (status == ResourceLoader.ThreadLoadStatus.Loaded)
            return ResourceLoader.LoadThreadedGet(path) as PackedScene;
        
        await ToSignal(GetTree(), SceneTree.SignalName.ProcessFrame);
    }
}
```
</async>

<common_pitfalls>
## 常见陷阱

**_Ready() 调用顺序：**
- 子节点先于父节点
- 父节点的 _Ready 中可以安全访问子节点
- 子节点的 _Ready 中父节点可能未初始化

**场景实例化时机：**
```csharp
var enemy = scene.Instantiate<Enemy>();
// enemy._Ready() 还没调用
AddChild(enemy);
// 现在 _Ready() 已调用
```

**Autoload 初始化顺序：**
- 按 Project Settings 中的顺序
- 不要在 _Ready 中访问其他 Autoload

**Export 变量不显示：**
- 必须 public
- 必须 PascalCase
- 重新编译（Build 按钮）

**信号内存泄漏：**
```csharp
public override void _Ready()
{
    player.HealthChanged += OnHealthChanged;
}

public override void _ExitTree()
{
    player.HealthChanged -= OnHealthChanged;  // 必须断开
}
```
</common_pitfalls>

<paths>
## 文件路径

```csharp
// res:// - 项目资源（只读）
var tex = GD.Load<Texture2D>("res://icon.png");

// user:// - 用户数据（可读写）
var file = FileAccess.Open("user://save.json", FileAccess.ModeFlags.Write);

// user:// 实际位置：
// Windows: %APPDATA%\Godot\app_userdata\[项目名]\
// Linux: ~/.local/share/godot/app_userdata/[项目名]/
// macOS: ~/Library/Application Support/Godot/app_userdata/[项目名]/
```
</paths>

<godot_types>
## Godot 特有类型

**NodePath - 节点路径：**
```csharp
GetNode("Child");              // 子节点
GetNode("Child/GrandChild");   // 嵌套
GetNode("../Sibling");         // 兄弟节点
GetNode("/root/GameManager");  // 绝对路径
```

**StringName - 性能优化：**
```csharp
EmitSignal(SignalName.HealthChanged, 100);  // 使用 StringName
CallDeferred(MethodName.UpdateUI, data);    // 编译时检查
```

**Godot.Collections vs System.Collections：**
- Export 变量：必须用 Godot.Collections
- 内部逻辑：推荐用 System.Collections（性能更好）
- 与 GDScript 交互：必须用 Godot.Collections
</godot_types>

<quick_ref>
## 快速参考

**生命周期顺序：**
1. _EnterTree()（根→叶）
2. _Ready()（叶→根）
3. _Process() / _PhysicsProcess()
4. _ExitTree()

**常用方法：**
```csharp
GetNode<T>("path")           // 获取节点
QueueFree()                  // 删除节点
AddChild(node)               // 添加子节点
EmitSignal(name, args)       // 发射信号
CallDeferred(method, args)   // 延迟调用
```

**坐标系：**
- Y 轴向下（不是向上！）
- Vector2.Up = (0, -1)
- Vector2.Down = (0, 1)

**快捷键：**
- F5 - 运行项目
- F6 - 运行当前场景
- Ctrl+B - 编译 C#
</quick_ref>
