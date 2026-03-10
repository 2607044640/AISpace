---
inclusion: manual
---

# Godot C# 开发参考

<core_architecture>
## 核心架构

### Node 系统
Godot 使用 Node 树结构组织游戏对象。每个场景是一个 Node 树，游戏是场景树的集合。

**获取节点（类型安全）：**
```csharp
// 使用泛型获取节点
Button myButton = GetNode<Button>("ButtonName");

// 避免空引用
Button myButton = GetNodeOrNull<Button>("ButtonName");
if (myButton != null) { /* 使用 */ }

// 获取父节点
Node parent = GetParent();

// 获取子节点
Node child = GetChild(0);
```

### Node 生命周期
```csharp
public override void _EnterTree()
{
    // 节点添加到场景树时调用（从根到叶）
    // 用于：初始化不依赖子节点的内容
}

public override void _Ready()
{
    // 节点及其子节点准备就绪时调用（从叶到根）
    // 用于：获取子节点引用、初始化游戏逻辑
}

public override void _Process(double delta)
{
    // 每帧调用（帧率不固定）
    // 用于：视觉更新、UI 逻辑、非物理相关的游戏逻辑
}

public override void _PhysicsProcess(double delta)
{
    // 物理帧调用（固定时间步长，默认 60 FPS）
    // 用于：物理计算、角色移动、碰撞检测
}

public override void _ExitTree()
{
    // 节点从场景树移除时调用
    // 用于：清理资源、断开信号连接
}
```

**控制生命周期：**
```csharp
SetProcess(false);        // 停止 _Process
SetPhysicsProcess(false); // 停止 _PhysicsProcess
```
</core_architecture>

<global_management>
## 全局管理系统（Autoload/Singleton）

Godot 的 Autoload 系统类似 UE 的 Subsystem 或 Unity 的 GameManager，用于创建全局可访问的单例。

### 创建 Autoload
1. 创建 C# 脚本（如 `GameManager.cs`）
2. Project Settings > Autoload > 添加脚本
3. 设置 Node Name（如 "GameManager"）

### Autoload 脚本示例
```csharp
// Scripts/GameManager.cs
using Godot;

public partial class GameManager : Node
{
    // 单例实例（可选，用于类型安全访问）
    public static GameManager Instance { get; private set; }
    
    // 全局数据
    public int Score { get; set; }
    public int Level { get; set; }
    
    public override void _Ready()
    {
        Instance = this;
    }
    
    public void SaveGame()
    {
        // 保存逻辑
    }
}
```

### 访问 Autoload
```csharp
// 方法 1：通过单例实例（推荐）
GameManager.Instance.Score += 10;

// 方法 2：通过场景树
var gm = GetNode<GameManager>("/root/GameManager");
gm.Score += 10;
```
</global_management>

<data_management>
## 数据管理系统

### Resource（数据容器）
Resource 是 Godot 的数据容器，类似 UE 的 DataAsset。可序列化、可在编辑器中编辑。

**创建自定义 Resource：**
```csharp
// Scripts/Data/ItemData.cs
using Godot;

[GlobalClass] // 使其在编辑器中可见
public partial class ItemData : Resource
{
    [Export] public string ItemName { get; set; }
    [Export] public int ItemId { get; set; }
    [Export] public Texture2D Icon { get; set; }
    [Export] public int Price { get; set; }
}
```

**使用 Resource：**
```csharp
// 在编辑器中分配
[Export] public ItemData MyItem { get; set; }

// 代码加载
ItemData item = GD.Load<ItemData>("res://Data/Items/Sword.tres");
```

### CSV/Excel 数据导入

**方法 1：CSV 文件直接读取**
```csharp
// Scripts/Data/DataLoader.cs
using Godot;
using System.Collections.Generic;

public partial class DataLoader : Node
{
    public static Dictionary<int, ItemData> LoadItemsFromCSV(string path)
    {
        var items = new Dictionary<int, ItemData>();
        var file = FileAccess.Open(path, FileAccess.ModeFlags.Read);
        
        if (file == null)
        {
            GD.PrintErr($"无法打开文件: {path}");
            return items;
        }
        
        // 跳过标题行
        file.GetCsvLine();
        
        while (!file.EofReached())
        {
            var line = file.GetCsvLine();
            if (line.Length < 4) continue;
            
            var item = new ItemData
            {
                ItemId = line[0].ToInt(),
                ItemName = line[1],
                Price = line[2].ToInt(),
                // Icon 路径在 CSV 中，需要加载
                Icon = GD.Load<Texture2D>(line[3])
            };
            
            items[item.ItemId] = item;
        }
        
        file.Close();
        return items;
    }
}
```

**CSV 文件格式示例（res://Data/Items.csv）：**
```csv
ItemId,ItemName,Price,IconPath
1,剑,100,res://Assets/Icons/sword.png
2,盾,80,res://Assets/Icons/shield.png
3,药水,20,res://Assets/Icons/potion.png
```

**方法 2：使用 Resource 生成器（推荐）**
```csharp
// Scripts/Tools/ResourceGenerator.cs
#if TOOLS
using Godot;
using System.IO;

[Tool]
public partial class ResourceGenerator : EditorScript
{
    public override void _Run()
    {
        GenerateItemResources("res://Data/Items.csv", "res://Data/Items/");
    }
    
    private void GenerateItemResources(string csvPath, string outputDir)
    {
        var file = FileAccess.Open(csvPath, FileAccess.ModeFlags.Read);
        if (file == null) return;
        
        // 跳过标题
        file.GetCsvLine();
        
        while (!file.EofReached())
        {
            var line = file.GetCsvLine();
            if (line.Length < 4) continue;
            
            var item = new ItemData
            {
                ItemId = line[0].ToInt(),
                ItemName = line[1],
                Price = line[2].ToInt(),
                Icon = GD.Load<Texture2D>(line[3])
            };
            
            // 保存为 .tres 文件
            string savePath = $"{outputDir}{item.ItemName}.tres";
            ResourceSaver.Save(item, savePath);
            GD.Print($"生成: {savePath}");
        }
        
        file.Close();
    }
}
#endif
```

**使用方法：**
1. 创建 CSV 文件
2. 在编辑器中：File > Run Script > 选择 ResourceGenerator.cs
3. 自动生成 .tres 资源文件


### JSON 数据管理
```csharp
// 保存数据
public void SaveToJson(string path, object data)
{
    var json = Json.Stringify(data);
    var file = FileAccess.Open(path, FileAccess.ModeFlags.Write);
    file.StoreString(json);
    file.Close();
}

// 加载数据
public T LoadFromJson<T>(string path) where T : new()
{
    var file = FileAccess.Open(path, FileAccess.ModeFlags.Read);
    if (file == null) return new T();
    
    var json = file.GetAsText();
    file.Close();
    
    var result = Json.ParseString(json);
    return result.As<T>();
}
```
</data_management>

<signals>
## 信号系统（Signals）

信号是 Godot 的事件系统，用于解耦通信。

### 声明和发射信号
```csharp
public partial class Player : Node2D
{
    // 声明信号
    [Signal]
    public delegate void HealthChangedEventHandler(int newHealth);
    
    [Signal]
    public delegate void DiedEventHandler();
    
    private int _health = 100;
    
    public void TakeDamage(int damage)
    {
        _health -= damage;
        
        // 发射信号
        EmitSignal(SignalName.HealthChanged, _health);
        
        if (_health <= 0)
        {
            EmitSignal(SignalName.Died);
        }
    }
}
```

### 连接信号
```csharp
// 方法 1：使用 += 操作符（推荐）
player.HealthChanged += OnPlayerHealthChanged;
player.Died += OnPlayerDied;

private void OnPlayerHealthChanged(int newHealth)
{
    GD.Print($"玩家生命值: {newHealth}");
}

private void OnPlayerDied()
{
    GD.Print("玩家死亡");
}

// 方法 2：使用 Connect
player.Connect(Player.SignalName.HealthChanged, 
    Callable.From<int>(OnPlayerHealthChanged));

// 断开信号（避免内存泄漏）
player.HealthChanged -= OnPlayerHealthChanged;
```

### Lambda 表达式连接
```csharp
// 带参数
button.Pressed += () => OnButtonPressed(itemId);

// 注意：Lambda 无法直接断开，需要保存引用
Action callback = () => OnButtonPressed(itemId);
button.Pressed += callback;
// 断开时
button.Pressed -= callback;
```

### 信号性能考虑
```csharp
// 信号 vs 直接调用
// 信号的开销：
// - 信号查找和分发有额外开销
// - 比直接方法调用慢约 2-5 倍
// - 但提供了解耦和灵活性

// ❌ 不推荐 - 高频调用用信号
public override void _Process(double delta)
{
    EmitSignal(SignalName.PositionUpdated, Position); // 每帧发射，开销大
}

// ✅ 推荐 - 高频调用用直接调用
private Action<Vector2> _onPositionChanged;

public override void _Process(double delta)
{
    _onPositionChanged?.Invoke(Position); // 更快
}

// ✅ 推荐 - 低频事件用信号
public void TakeDamage(int amount)
{
    Health -= amount;
    EmitSignal(SignalName.HealthChanged, Health); // 偶尔触发，信号很合适
}

// 何时用信号？
// - 跨节点通信（解耦）
// - 低频事件（按钮点击、生命值变化、游戏状态改变）
// - 需要多个监听者
// - 与 GDScript 交互

// 何时用直接调用？
// - 高频更新（_Process、_PhysicsProcess）
// - 性能关键路径
// - 单一监听者
// - 紧密耦合的组件
```
</signals>

<scene_management>
## 场景管理

### 加载和实例化场景
```csharp
// 加载 PackedScene
PackedScene scene = GD.Load<PackedScene>("res://Scenes/Enemy.tscn");

// 实例化
Node instance = scene.Instantiate();

// 类型安全实例化
Enemy enemy = scene.Instantiate<Enemy>();

// 添加到场景树
AddChild(enemy);

// 设置位置（如果是 Node2D）
if (enemy is Node2D node2D)
{
    node2D.Position = new Vector2(100, 100);
}
```

### 切换场景
```csharp
// 方法 1：使用 SceneTree
GetTree().ChangeSceneToFile("res://Scenes/MainMenu.tscn");

// 方法 2：使用 PackedScene
PackedScene nextScene = GD.Load<PackedScene>("res://Scenes/Level1.tscn");
GetTree().ChangeSceneToPacked(nextScene);
```

### 场景管理器示例
```csharp
// Scripts/SceneManager.cs (Autoload)
public partial class SceneManager : Node
{
    public static SceneManager Instance { get; private set; }
    
    [Export] public PackedScene MainMenu { get; set; }
    [Export] public PackedScene GameScene { get; set; }
    
    public override void _Ready()
    {
        Instance = this;
    }
    
    public void LoadScene(string scenePath)
    {
        GetTree().ChangeSceneToFile(scenePath);
    }
    
    public void LoadMainMenu()
    {
        GetTree().ChangeSceneToPacked(MainMenu);
    }
}
```
</scene_management>

<input_handling>
## 输入处理

### Input Actions（推荐）
在 Project Settings > Input Map 中定义动作。

```csharp
public override void _Process(double delta)
{
    // 检查动作是否按下
    if (Input.IsActionPressed("move_right"))
    {
        Position += new Vector2(speed * (float)delta, 0);
    }
    
    // 检查动作是否刚按下（单次触发）
    if (Input.IsActionJustPressed("jump"))
    {
        Jump();
    }
    
    // 检查动作是否刚释放
    if (Input.IsActionJustReleased("fire"))
    {
        StopFiring();
    }
    
    // 获取动作强度（0.0 到 1.0，用于手柄）
    float strength = Input.GetActionStrength("accelerate");
}
```

### 直接输入检测
```csharp
public override void _Input(InputEvent @event)
{
    // 鼠标按钮
    if (@event is InputEventMouseButton mouseButton)
    {
        if (mouseButton.ButtonIndex == MouseButton.Left && mouseButton.Pressed)
        {
            GD.Print($"左键点击位置: {mouseButton.Position}");
        }
    }
    
    // 鼠标移动
    if (@event is InputEventMouseMotion mouseMotion)
    {
        GD.Print($"鼠标移动: {mouseMotion.Relative}");
    }
    
    // 键盘
    if (@event is InputEventKey key)
    {
        if (key.Keycode == Key.Escape && key.Pressed)
        {
            GetTree().Quit();
        }
    }
}

// 未处理的输入（UI 未消费的输入）
public override void _UnhandledInput(InputEvent @event)
{
    // 游戏逻辑输入处理
}
```

### 获取鼠标位置
```csharp
// 屏幕坐标
Vector2 mousePos = GetViewport().GetMousePosition();

// 世界坐标（2D）
Vector2 worldPos = GetGlobalMousePosition();
```
</input_handling>

<collision_detection>
## 碰撞检测

### Area2D（触发区域）
```csharp
public partial class Coin : Area2D
{
    public override void _Ready()
    {
        // 连接信号
        BodyEntered += OnBodyEntered;
        BodyExited += OnBodyExited;
    }
    
    private void OnBodyEntered(Node2D body)
    {
        if (body is Player player)
        {
            player.CollectCoin();
            QueueFree(); // 删除自己
        }
    }
    
    private void OnBodyExited(Node2D body)
    {
        GD.Print($"{body.Name} 离开区域");
    }
    
    // 检查重叠
    public bool IsPlayerInRange()
    {
        var bodies = GetOverlappingBodies();
        foreach (var body in bodies)
        {
            if (body is Player)
                return true;
        }
        return false;
    }
}
```

### CharacterBody2D（角色物理）
```csharp
public partial class Player : CharacterBody2D
{
    [Export] public float Speed = 300.0f;
    [Export] public float JumpVelocity = -400.0f;
    
    public override void _PhysicsProcess(double delta)
    {
        Vector2 velocity = Velocity;
        
        // 重力
        if (!IsOnFloor())
        {
            velocity.Y += gravity * (float)delta;
        }
        
        // 跳跃
        if (Input.IsActionJustPressed("jump") && IsOnFloor())
        {
            velocity.Y = JumpVelocity;
        }
        
        // 移动
        float direction = Input.GetAxis("move_left", "move_right");
        velocity.X = direction * Speed;
        
        Velocity = velocity;
        MoveAndSlide();
        
        // 检查碰撞
        for (int i = 0; i < GetSlideCollisionCount(); i++)
        {
            var collision = GetSlideCollision(i);
            GD.Print($"碰撞: {collision.GetCollider()}");
        }
    }
}
```

### RayCast2D（射线检测）
```csharp
public partial class RaycastExample : Node2D
{
    private RayCast2D _raycast;
    
    public override void _Ready()
    {
        _raycast = GetNode<RayCast2D>("RayCast2D");
        _raycast.Enabled = true;
    }
    
    public override void _Process(double delta)
    {
        if (_raycast.IsColliding())
        {
            var collider = _raycast.GetCollider();
            var point = _raycast.GetCollisionPoint();
            GD.Print($"射线击中: {collider} 位置: {point}");
        }
    }
}
```
</collision_detection>

<animation>
## 动画系统

### Tween（代码动画）
```csharp
public partial class TweenExample : Node2D
{
    public void AnimatePosition()
    {
        // 创建 Tween
        Tween tween = CreateTween();
        
        // 移动到目标位置（2 秒）
        tween.TweenProperty(this, "position", new Vector2(500, 300), 2.0);
        
        // 链式调用
        tween.TweenProperty(this, "rotation", Mathf.Pi, 1.0);
        tween.TweenProperty(this, "scale", Vector2.One * 2, 0.5);
    }
    
    public void ComplexAnimation()
    {
        Tween tween = CreateTween();
        
        // 设置缓动函数
        tween.SetTrans(Tween.TransitionType.Bounce);
        tween.SetEase(Tween.EaseType.Out);
        
        // 并行动画
        tween.SetParallel(true);
        tween.TweenProperty(this, "position:x", 500, 1.0);
        tween.TweenProperty(this, "position:y", 300, 1.0);
        
        // 回调
        tween.TweenCallback(Callable.From(() => GD.Print("动画完成")));
    }
    
    public void FadeOut()
    {
        Tween tween = CreateTween();
        tween.TweenProperty(this, "modulate:a", 0.0, 1.0);
        tween.TweenCallback(Callable.From(QueueFree));
    }
}
```

### AnimationPlayer
```csharp
public partial class AnimatedCharacter : Node2D
{
    private AnimationPlayer _animPlayer;
    
    public override void _Ready()
    {
        _animPlayer = GetNode<AnimationPlayer>("AnimationPlayer");
    }
    
    public void PlayAnimation(string animName)
    {
        _animPlayer.Play(animName);
    }
    
    public void OnAnimationFinished(string animName)
    {
        GD.Print($"动画完成: {animName}");
    }
}
```
</animation>

<export_attributes>
## Export 属性（Inspector 变量）

```csharp
public partial class ExportExample : Node
{
    // 基本类型
    [Export] public int Health = 100;
    [Export] public float Speed = 5.0f;
    [Export] public string PlayerName = "Player";
    [Export] public bool IsAlive = true;
    
    // 范围限制
    [Export(PropertyHint.Range, "0,100,1")] public int Percentage = 50;
    [Export(PropertyHint.Range, "0,10,0.1")] public float Volume = 1.0f;
    
    // 文件路径
    [Export(PropertyHint.File, "*.png,*.jpg")] public string TexturePath;
    [Export(PropertyHint.Dir)] public string FolderPath;
    
    // 枚举
    public enum WeaponType { Sword, Bow, Staff }
    [Export] public WeaponType CurrentWeapon = WeaponType.Sword;
    
    // 数组
    [Export] public int[] Scores = { 10, 20, 30 };
    [Export] public string[] Names = { "Alice", "Bob" };
    
    // Godot 类型
    [Export] public PackedScene EnemyScene;
    [Export] public Texture2D Icon;
    [Export] public AudioStream Sound;
    
    // Resource
    [Export] public ItemData Item;
    
    // Node 引用
    [Export] public Node2D Target;
    
    // 多行文本
    [Export(PropertyHint.MultilineText)] public string Description;
    
    // 颜色
    [Export] public Color PlayerColor = Colors.Red;
}
```
</export_attributes>

<utilities>
## 实用工具

### 定时器
```csharp
public partial class TimerExample : Node
{
    private Timer _timer;
    
    public override void _Ready()
    {
        // 创建定时器
        _timer = new Timer();
        AddChild(_timer);
        _timer.WaitTime = 2.0; // 2 秒
        _timer.OneShot = false; // 重复触发
        _timer.Timeout += OnTimerTimeout;
        _timer.Start();
    }
    
    private void OnTimerTimeout()
    {
        GD.Print("定时器触发");
    }
    
    // 一次性延迟
    public async void DelayedAction()
    {
        await ToSignal(GetTree().CreateTimer(1.0), Timer.SignalName.Timeout);
        GD.Print("1 秒后执行");
    }
}
```

### 随机数
```csharp
// 使用 GD.Randf() 和 GD.Randi()
float randomFloat = GD.Randf(); // 0.0 到 1.0
int randomInt = GD.Randi(); // 0 到 2^32-1
int randomRange = GD.RandiRange(1, 10); // 1 到 10

// 使用 RandomNumberGenerator（可设置种子）
var rng = new RandomNumberGenerator();
rng.Seed = 12345;
float value = rng.RandfRange(0.0f, 100.0f);
```

### 日志输出
```csharp
GD.Print("普通日志");
GD.PrintErr("错误日志");  // 红色
GD.PushWarning("警告");   // 黄色
GD.PrintRich("[color=green]彩色文本[/color]");
```

### 节点查找
```csharp
// 按名称查找
Node node = GetNode("NodeName");

// 按路径查找
Node node = GetNode("Parent/Child/GrandChild");

// 按类型查找所有子节点
var sprites = GetChildren().OfType<Sprite2D>();

// 按组查找
GetTree().GetNodesInGroup("enemies");
```

### 组（Groups）
```csharp
// 添加到组
AddToGroup("enemies");

// 检查是否在组中
if (IsInGroup("enemies"))
{
    // ...
}

// 调用组中所有节点的方法
GetTree().CallGroup("enemies", "TakeDamage", 10);

// 移除组
RemoveFromGroup("enemies");
```
</utilities>

<best_practices>
## 最佳实践

### 命名规范
```csharp
// 类名：PascalCase
public partial class PlayerController : Node2D

// 公共属性/方法：PascalCase
public int Health { get; set; }
public void TakeDamage(int amount) { }

// 私有字段：_camelCase
private int _currentHealth;
private Timer _cooldownTimer;

// 常量：UPPER_CASE
private const int MAX_HEALTH = 100;

// Export 变量：PascalCase（必须）
[Export] public float MoveSpeed = 5.0f;
```

### 内存管理
```csharp
// 删除节点
QueueFree(); // 安全删除（在帧结束时）
Free();      // 立即删除（危险）

// 断开信号避免内存泄漏
public override void _ExitTree()
{
    player.HealthChanged -= OnHealthChanged;
}

// 释放资源
texture?.Dispose();
```

### 性能优化
```csharp
// 缓存节点引用
private Sprite2D _sprite;
public override void _Ready()
{
    _sprite = GetNode<Sprite2D>("Sprite");
}

// 避免在 _Process 中频繁调用 GetNode
public override void _Process(double delta)
{
    // 好
    _sprite.Position += Vector2.Right;
    
    // 差
    GetNode<Sprite2D>("Sprite").Position += Vector2.Right;
}

// 使用对象池
private List<Enemy> _enemyPool = new();
```
</best_practices>

<common_patterns>
## 常用模式

### 状态机
```csharp
public partial class Player : CharacterBody2D
{
    public enum State { Idle, Running, Jumping, Falling }
    private State _currentState = State.Idle;
    
    public override void _PhysicsProcess(double delta)
    {
        switch (_currentState)
        {
            case State.Idle:
                HandleIdleState();
                break;
            case State.Running:
                HandleRunningState();
                break;
            case State.Jumping:
                HandleJumpingState();
                break;
        }
    }
    
    private void ChangeState(State newState)
    {
        _currentState = newState;
    }
}
```

### 对象池
```csharp
public partial class BulletPool : Node
{
    [Export] public PackedScene BulletScene;
    [Export] public int PoolSize = 20;
    
    private List<Bullet> _pool = new();
    
    public override void _Ready()
    {
        for (int i = 0; i < PoolSize; i++)
        {
            var bullet = BulletScene.Instantiate<Bullet>();
            bullet.Visible = false;
            AddChild(bullet);
            _pool.Add(bullet);
        }
    }
    
    public Bullet GetBullet()
    {
        foreach (var bullet in _pool)
        {
            if (!bullet.Visible)
            {
                bullet.Visible = true;
                return bullet;
            }
        }
        return null;
    }
    
    public void ReturnBullet(Bullet bullet)
    {
        bullet.Visible = false;
    }
}
```
</common_patterns>


<async_await>
## Async/Await 异步编程

### Partial Classes 要求
Godot 4 C# 要求所有继承自 GodotObject 的类使用 `partial` 关键字。

```csharp
// 正确
public partial class Player : CharacterBody2D

// 错误 - 会导致编译错误
public class Player : CharacterBody2D
```

### ToSignal 等待信号
```csharp
public async Task DelayAsync(float seconds)
{
    await ToSignal(GetTree().CreateTimer(seconds), Timer.SignalName.Timeout);
    GD.Print("延迟完成");
}

// 等待 Tween 完成
public async Task AnimateAsync()
{
    Tween tween = CreateTween();
    tween.TweenProperty(this, "position", new Vector2(500, 300), 2.0);
    await ToSignal(tween, Tween.SignalName.Finished);
    GD.Print("动画完成");
}
```

### 线程安全 - Task.Delay 问题
Godot 的 Scene Tree API 不是线程安全的。使用 Task.Delay 后操作节点会导致崩溃。

```csharp
// 错误 - 可能崩溃
public async Task LoadDataWrong()
{
    await Task.Delay(1000);
    AddChild(node); // 可能在非主线程执行
}

// 正确 - 使用 CallDeferred
public async Task LoadDataCorrect()
{
    await Task.Delay(1000);
    CallDeferred(MethodName.AddChild, node);
}
```

### Async 方法返回类型
```csharp
// 推荐 - 返回 Task
public async Task LoadDataAsync()
{
    await ToSignal(GetTree().CreateTimer(1.0), Timer.SignalName.Timeout);
}

// 推荐 - 返回 Task<T>
public async Task<int> CalculateAsync()
{
    await Task.Delay(100);
    return 42;
}

// 避免 - 只用于事件处理器
public async void OnButtonPressed()
{
    await LoadDataAsync();
}
```

### 后台加载资源
```csharp
public async Task<PackedScene> LoadSceneAsync(string path)
{
    ResourceLoader.LoadThreadedRequest(path);
    
    while (true)
    {
        var progress = new Godot.Collections.Array();
        var status = ResourceLoader.LoadThreadedGetStatus(path, progress);
        
        if (status == ResourceLoader.ThreadLoadStatus.Loaded)
        {
            return ResourceLoader.LoadThreadedGet(path) as PackedScene;
        }
        else if (status == ResourceLoader.ThreadLoadStatus.Failed)
        {
            GD.PrintErr($"加载失败: {path}");
            return null;
        }
        
        // 显示进度
        float percent = progress.Count > 0 ? (float)progress[0] : 0;
        GD.Print($"加载进度: {percent * 100}%");
        
        await ToSignal(GetTree(), SceneTree.SignalName.ProcessFrame);
    }
}
```
</async_await>

<threading>
## 线程安全和 CallDeferred

### CallDeferred 基础
确保方法在主线程的空闲时间执行，用于从后台线程安全地操作场景树。

```csharp
// 方法 1：使用 MethodName（推荐）
CallDeferred(MethodName.UpdateUI, data);

// 方法 2：使用 Callable.From
CallDeferred(Callable.From(() => UpdateUI(data)));

// 方法 3：使用字符串（不推荐）
CallDeferred("UpdateUI", data);
```

### 后台线程操作场景树
```csharp
public async Task LoadDataAsync()
{
    // 在后台线程加载数据
    var data = await Task.Run(() => LoadHeavyData());
    
    // 回到主线程更新 UI
    CallDeferred(MethodName.UpdateUI, data);
}

private void UpdateUI(object data)
{
    // 这里可以安全地操作节点
    label.Text = data.ToString();
}
```

### 线程安全的信号连接
```csharp
// 使用 CONNECT_DEFERRED 标志
player.Connect(Player.SignalName.HealthChanged, 
    Callable.From<int>(OnHealthChanged), 
    (uint)ConnectFlags.Deferred);
```
</threading>

<math_utilities>
## 数学工具

### Vector2 常用操作
```csharp
Vector2 a = new Vector2(1, 2);
Vector2 b = new Vector2(3, 4);

// 长度
float length = a.Length();
float lengthSquared = a.LengthSquared(); // 更快，避免开方

// 归一化
Vector2 normalized = a.Normalized();

// 距离
float distance = a.DistanceTo(b);

// 点积
float dot = a.Dot(b);

// 角度
float angle = a.AngleTo(b);
float angleToPoint = a.AngleToPoint(b);

// 方向向量
Vector2 direction = a.DirectionTo(b);

// 插值
Vector2 lerp = a.Lerp(b, 0.5f);

// 反射
Vector2 normal = new Vector2(0, 1);
Vector2 reflected = a.Reflect(normal);

// 旋转
Vector2 rotated = a.Rotated(Mathf.Pi / 4); // 旋转 45 度
```

### Vector2 常量
```csharp
Vector2.Zero      // (0, 0)
Vector2.One       // (1, 1)
Vector2.Up        // (0, -1)
Vector2.Down      // (0, 1)
Vector2.Left      // (-1, 0)
Vector2.Right     // (1, 0)
```

### Transform2D 操作
```csharp
// 创建变换
Transform2D transform = Transform2D.Identity;

// 平移
transform = transform.Translated(new Vector2(10, 20));

// 旋转
transform = transform.Rotated(Mathf.Pi / 4);

// 缩放
transform = transform.Scaled(new Vector2(2, 2));

// 应用变换到点
Vector2 point = new Vector2(5, 5);
Vector2 transformed = transform * point;

// 逆变换
Transform2D inverse = transform.Inverse();

// 获取位置、旋转、缩放
Vector2 origin = transform.Origin;
float rotation = transform.Rotation;
Vector2 scale = transform.Scale;
```
</math_utilities>

<camera_coordinates>
## Camera2D 和坐标转换

### 屏幕坐标 vs 世界坐标
```csharp
public override void _Input(InputEvent @event)
{
    if (@event is InputEventMouseButton mouseButton)
    {
        // 屏幕坐标（相对于窗口）
        Vector2 screenPos = mouseButton.Position;
        
        // 世界坐标（考虑相机变换）
        Vector2 worldPos = GetGlobalMousePosition();
        
        GD.Print($"屏幕: {screenPos}, 世界: {worldPos}");
    }
}
```

### Camera2D 坐标转换
```csharp
public partial class CameraHelper : Camera2D
{
    // 屏幕坐标转世界坐标
    public Vector2 ScreenToWorld(Vector2 screenPos)
    {
        var canvasTransform = GetCanvasTransform();
        return canvasTransform.AffineInverse() * screenPos;
    }
    
    // 世界坐标转屏幕坐标
    public Vector2 WorldToScreen(Vector2 worldPos)
    {
        var canvasTransform = GetCanvasTransform();
        return canvasTransform * worldPos;
    }
    
    // 获取相机可见区域（世界坐标）
    public Rect2 GetVisibleRect()
    {
        var viewportSize = GetViewportRect().Size;
        var zoom = Zoom;
        
        var size = viewportSize / zoom;
        var position = GlobalPosition - size / 2;
        
        return new Rect2(position, size);
    }
    
    // 检查点是否在相机视野内
    public bool IsPointVisible(Vector2 worldPos)
    {
        return GetVisibleRect().HasPoint(worldPos);
    }
}
```

### Camera2D 平滑跟随
```csharp
public partial class FollowCamera : Camera2D
{
    [Export] public Node2D Target;
    [Export] public float SmoothSpeed = 5.0f;
    [Export] public Vector2 Offset = Vector2.Zero;
    
    public override void _Process(double delta)
    {
        if (Target == null) return;
        
        var targetPos = Target.GlobalPosition + Offset;
        GlobalPosition = GlobalPosition.Lerp(targetPos, SmoothSpeed * (float)delta);
    }
}
```

### Camera2D 限制区域
```csharp
public partial class BoundedCamera : Camera2D
{
    public override void _Ready()
    {
        // 设置相机边界
        LimitLeft = 0;
        LimitTop = 0;
        LimitRight = 2000;
        LimitBottom = 1500;
        
        // 启用平滑
        PositionSmoothingEnabled = true;
        PositionSmoothingSpeed = 5.0f;
    }
}
```

### Camera2D Zoom 详解
```csharp
// Zoom 是 Vector2，不是 float
// 默认值是 (1, 1)
// 值越大，看到的范围越小（放大）
// 值越小，看到的范围越大（缩小）

public partial class ZoomCamera : Camera2D
{
    public void ZoomIn()
    {
        // 放大 - 增加 Zoom 值
        Zoom = new Vector2(2, 2); // 2x 放大
    }
    
    public void ZoomOut()
    {
        // 缩小 - 减小 Zoom 值
        Zoom = new Vector2(0.5f, 0.5f); // 看到 2x 范围
    }
    
    public void SmoothZoom(float targetZoom, float speed)
    {
        var target = new Vector2(targetZoom, targetZoom);
        Zoom = Zoom.Lerp(target, speed * (float)GetProcessDeltaTime());
    }
}
```

### Godot 坐标系说明
```csharp
// ⚠️ 重要：Godot 的 Y 轴向下
// 这与数学坐标系不同！

// Vector2 常量的实际方向：
Vector2.Up    // (0, -1)  - Y 轴负方向
Vector2.Down  // (0, 1)   - Y 轴正方向
Vector2.Left  // (-1, 0)  - X 轴负方向
Vector2.Right // (1, 0)   - X 轴正方向

// 角度也受影响：
// 0 度 = 向右
// 90 度 = 向下（不是向上！）
// 180 度 = 向左
// 270 度 = 向上
```
</camera_coordinates>


<save_system>
## 存档系统

### JSON 存档（游戏数据）
```csharp
public partial class SaveSystem : Node
{
    private const string SavePath = "user://savegame.json";
    
    public class SaveData
    {
        public int Level { get; set; }
        public int Score { get; set; }
        public float[] PlayerPosition { get; set; } // Vector2 需要转换
        public Dictionary<string, bool> UnlockedItems { get; set; }
    }
    
    public void SaveGame(SaveData data)
    {
        var json = Json.Stringify(data);
        var file = FileAccess.Open(SavePath, FileAccess.ModeFlags.Write);
        
        if (file == null)
        {
            GD.PrintErr($"无法创建存档: {FileAccess.GetOpenError()}");
            return;
        }
        
        file.StoreString(json);
        file.Close();
    }
    
    public SaveData LoadGame()
    {
        if (!FileAccess.FileExists(SavePath))
            return new SaveData();
        
        var file = FileAccess.Open(SavePath, FileAccess.ModeFlags.Read);
        if (file == null) return new SaveData();
        
        var json = file.GetAsText();
        file.Close();
        
        var result = Json.ParseString(json);
        // 手动解析 Dictionary...
        return new SaveData();
    }
}
```

### ConfigFile 存档（设置）
ConfigFile 使用 INI 格式，通过 section（章节）组织数据，适合保存游戏设置。

```csharp
public partial class SettingsManager : Node
{
    private const string ConfigPath = "user://settings.cfg";
    private ConfigFile _config = new();
    
    public void SaveSettings()
    {
        // section 用于分组相关设置
        // 格式：[section]
        //       key=value
        _config.SetValue("audio", "master_volume", 0.8f);
        _config.SetValue("audio", "music_volume", 0.6f);
        _config.SetValue("video", "fullscreen", true);
        _config.SetValue("video", "resolution_x", 1920);
        _config.SetValue("video", "resolution_y", 1080);
        
        _config.Save(ConfigPath);
    }
    
    public void LoadSettings()
    {
        if (_config.Load(ConfigPath) != Error.Ok)
        {
            GD.Print("使用默认设置");
            return;
        }
        
        // GetValue(section, key, default)
        float masterVolume = (float)_config.GetValue("audio", "master_volume", 1.0f);
        AudioServer.SetBusVolumeDb(0, Mathf.LinearToDb(masterVolume));
        
        bool fullscreen = (bool)_config.GetValue("video", "fullscreen", false);
        DisplayServer.WindowSetMode(fullscreen ? 
            DisplayServer.WindowMode.Fullscreen : 
            DisplayServer.WindowMode.Windowed);
    }
    
    // 获取所有 section
    public void ListAllSections()
    {
        var sections = _config.GetSections();
        foreach (var section in sections)
        {
            GD.Print($"Section: {section}");
            var keys = _config.GetSectionKeys(section);
            foreach (var key in keys)
            {
                var value = _config.GetValue(section, key);
                GD.Print($"  {key} = {value}");
            }
        }
    }
}
```

**生成的 settings.cfg 文件格式：**
```ini
[audio]
master_volume=0.8
music_volume=0.6

[video]
fullscreen=true
resolution_x=1920
resolution_y=1080
```

### 二进制存档
```csharp
public void SaveBinary(SaveData data)
{
    var file = FileAccess.Open("user://savegame.dat", FileAccess.ModeFlags.Write);
    
    file.Store32((uint)data.Level);
    file.Store32((uint)data.Score);
    file.StoreFloat(data.PlayerPosition.X);
    file.StoreFloat(data.PlayerPosition.Y);
    
    file.Close();
}
```

### 加密存档
```csharp
public void SaveEncrypted(SaveData data, string password)
{
    var json = Json.Stringify(data);
    var file = FileAccess.OpenEncrypted("user://savegame.enc", 
        FileAccess.ModeFlags.Write, password.ToUtf8Buffer());
    
    file.StoreString(json);
    file.Close();
}
```
</save_system>

<audio_system>
## 音频系统

### AudioStreamPlayer 类型
- AudioStreamPlayer - 全局音频（UI、BGM）
- AudioStreamPlayer2D - 2D 位置音频
- AudioStreamPlayer3D - 3D 位置音频

### 音频管理器
```csharp
public partial class AudioManager : Node
{
    [Export] public AudioStream BackgroundMusic;
    
    private AudioStreamPlayer _musicPlayer;
    private AudioStreamPlayer _sfxPlayer;
    
    public override void _Ready()
    {
        // BGM 播放器
        _musicPlayer = new AudioStreamPlayer();
        _musicPlayer.Stream = BackgroundMusic;
        _musicPlayer.Autoplay = true;
        _musicPlayer.Bus = "Music";
        AddChild(_musicPlayer);
        
        // SFX 播放器
        _sfxPlayer = new AudioStreamPlayer();
        _sfxPlayer.Bus = "SFX";
        AddChild(_sfxPlayer);
    }
    
    public void PlaySound(AudioStream sound)
    {
        _sfxPlayer.Stream = sound;
        _sfxPlayer.Play();
    }
    
    public void SetMasterVolume(float volume)
    {
        int busIndex = AudioServer.GetBusIndex("Master");
        AudioServer.SetBusVolumeDb(busIndex, Mathf.LinearToDb(volume));
    }
    
    public void SetMute(bool muted)
    {
        int busIndex = AudioServer.GetBusIndex("Master");
        AudioServer.SetBusMute(busIndex, muted);
    }
}
```

### 音频池（避免重复创建）
```csharp
public partial class AudioPool : Node
{
    [Export] public int PoolSize = 10;
    private List<AudioStreamPlayer> _pool = new();
    
    public override void _Ready()
    {
        for (int i = 0; i < PoolSize; i++)
        {
            var player = new AudioStreamPlayer();
            AddChild(player);
            _pool.Add(player);
        }
    }
    
    public void PlaySound(AudioStream sound)
    {
        foreach (var player in _pool)
        {
            if (!player.Playing)
            {
                player.Stream = sound;
                player.Play();
                return;
            }
        }
    }
}
```
</audio_system>

<shader_material>
## Shader 和材质

### ShaderMaterial 基础
```csharp
// 创建 ShaderMaterial
var material = new ShaderMaterial();
material.Shader = GD.Load<Shader>("res://Shaders/MyShader.gdshader");

// 应用到 Sprite
sprite.Material = material;

// 设置 Shader 参数
material.SetShaderParameter("my_color", Colors.Red);
material.SetShaderParameter("intensity", 1.5f);
```

### Modulate 属性
```csharp
// 修改节点颜色（乘法混合）
sprite.Modulate = new Color(1, 0, 0, 0.5f); // 红色半透明

// Self Modulate（不影响子节点）
sprite.SelfModulate = Colors.Blue;

// CanvasModulate（影响整个画布）
var canvasModulate = new CanvasModulate();
canvasModulate.Color = new Color(0.8f, 0.8f, 1.0f);
AddChild(canvasModulate);
```

### 闪光效果示例
```csharp
public partial class FlashEffect : Sprite2D
{
    private ShaderMaterial _material;
    
    public override void _Ready()
    {
        _material = (ShaderMaterial)Material;
    }
    
    public async void Flash()
    {
        _material.SetShaderParameter("flash_intensity", 1.0f);
        await ToSignal(GetTree().CreateTimer(0.1), Timer.SignalName.Timeout);
        _material.SetShaderParameter("flash_intensity", 0.0f);
    }
}
```

**对应的 Shader（res://Shaders/Flash.gdshader）：**
```gdshader
shader_type canvas_item;

uniform vec4 flash_color : source_color = vec4(1.0, 1.0, 1.0, 1.0);
uniform float flash_intensity : hint_range(0.0, 1.0) = 0.0;

void fragment() {
    vec4 tex_color = texture(TEXTURE, UV);
    COLOR = mix(tex_color, flash_color, flash_intensity);
    COLOR.a = tex_color.a;
}
```

### Shader Uniform Hints
```gdshader
// 颜色（带 Alpha）
uniform vec4 color : source_color = vec4(1.0);

// 颜色（无 Alpha）
uniform vec3 color_no_alpha : source_color = vec3(1.0);

// 范围滑块
uniform float value : hint_range(0.0, 1.0) = 0.5;
uniform float value_step : hint_range(0.0, 10.0, 0.1) = 5.0;

// 纹理
uniform sampler2D texture : source_color;
uniform sampler2D normal_map : hint_normal;

// 整数
uniform int count : hint_range(0, 10) = 5;

// 布尔值（显示为复选框）
uniform bool enabled = true;
```
</shader_material>

<networking>
## 网络多人游戏

### RPC（远程过程调用）
```csharp
public partial class Player : CharacterBody2D
{
    [Rpc(MultiplayerApi.RpcMode.AnyPeer)]
    public void TakeDamage(int amount)
    {
        Health -= amount;
    }
    
    public void Attack()
    {
        // 调用所有客户端的方法
        Rpc(MethodName.TakeDamage, 10);
    }
}
```

### MultiplayerSynchronizer
```csharp
public partial class NetworkedPlayer : CharacterBody2D
{
    [Export] public int Health { get; set; } = 100;
    
    public override void _Ready()
    {
        var sync = new MultiplayerSynchronizer();
        sync.RootPath = GetPath();
        AddChild(sync);
        
        // 配置同步属性
        sync.ReplicationConfig = new SceneReplicationConfig();
        sync.ReplicationConfig.AddProperty(".:Health");
        sync.ReplicationConfig.AddProperty(".:Position");
    }
}
```
</networking>

<performance>
## 性能优化

### 使用 Profiler
- Debugger > Profiler 查看性能瓶颈
- C# 脚本需要 JetBrains Rider + dotTrace

### 缓存节点引用
```csharp
// 差
public override void _Process(double delta)
{
    GetNode<Sprite2D>("Sprite").Position += Vector2.Right;
}

// 好
private Sprite2D _sprite;
public override void _Ready()
{
    _sprite = GetNode<Sprite2D>("Sprite");
}
public override void _Process(double delta)
{
    _sprite.Position += Vector2.Right;
}
```

### 减少 Marshalling 开销
C# 和 Godot 之间的调用需要 marshalling，频繁调用会影响性能。

```csharp
// 差 - 每次循环都调用 Godot API
for (int i = 0; i < 1000; i++)
{
    Position += Vector2.Right;
}

// 好 - 缓存到本地变量
Vector2 pos = Position;
for (int i = 0; i < 1000; i++)
{
    pos += Vector2.Right;
}
Position = pos;
```

### 对象池模式
避免频繁创建和销毁对象。

```csharp
public partial class BulletPool : Node
{
    [Export] public PackedScene BulletScene;
    [Export] public int PoolSize = 20;
    
    private List<Bullet> _pool = new();
    
    public override void _Ready()
    {
        for (int i = 0; i < PoolSize; i++)
        {
            var bullet = BulletScene.Instantiate<Bullet>();
            bullet.Visible = false;
            AddChild(bullet);
            _pool.Add(bullet);
        }
    }
    
    public Bullet GetBullet()
    {
        foreach (var bullet in _pool)
        {
            if (!bullet.Visible)
            {
                bullet.Visible = true;
                return bullet;
            }
        }
        return null;
    }
}
```
</performance>


<editor_plugins>
## 编辑器插件

### #if TOOLS 预处理指令
```csharp
// ⚠️ 重要：编辑器代码必须用 #if TOOLS 包裹
#if TOOLS
using Godot;

[Tool]
public partial class MyEditorPlugin : EditorPlugin
{
    public override void _EnterTree()
    {
        GD.Print("插件已加载");
    }
    
    public override void _ExitTree()
    {
        GD.Print("插件已卸载");
    }
}
#endif

// 为什么必须用 #if TOOLS？
// 1. EditorPlugin 等类型只在编辑器中存在
// 2. 导出游戏时不包含编辑器代码，减小体积
// 3. 不用会导致导出的游戏崩溃（找不到 EditorPlugin 类型）
// 4. 编译错误：在非编辑器构建中引用编辑器类型
```

### 创建编辑器插件
```csharp
#if TOOLS
using Godot;

[Tool]
public partial class MyEditorPlugin : EditorPlugin
{
    private Control _dockPanel;
    
    public override void _EnterTree()
    {
        // 插件被启用时调用
        // 时机：
        // - 首次启用插件
        // - 编辑器启动时（如果插件已启用）
        // - 重新加载项目
        
        GD.Print("插件已加载");
        
        // 添加自定义 Dock
        _dockPanel = new Control();
        AddControlToDock(DockSlot.LeftUl, _dockPanel);
    }
    
    public override void _ExitTree()
    {
        // 插件被禁用时调用
        // 时机：
        // - 禁用插件
        // - 编辑器关闭
        // - 重新加载项目
        
        GD.Print("插件已卸载");
        
        // 清理资源
        if (_dockPanel != null)
        {
            RemoveControlFromDocks(_dockPanel);
            _dockPanel.QueueFree();
        }
    }
}
#endif
```

### 自定义 Inspector
```csharp
#if TOOLS
public partial class CustomInspectorPlugin : EditorInspectorPlugin
{
    public override bool _CanHandle(GodotObject @object)
    {
        return @object is MyCustomNode;
    }
    
    public override void _ParseBegin(GodotObject @object)
    {
        var button = new Button();
        button.Text = "自定义按钮";
        AddCustomControl(button);
    }
}
#endif
```

### Tool 脚本和 Engine.IsEditorHint()
```csharp
// [Tool] 使脚本在编辑器中运行
[Tool]
public partial class EditorScript : Node2D
{
    [Export] public int Count = 5;
    
    public override void _Process(double delta)
    {
        // Engine.IsEditorHint() 检查是否在编辑器中
        if (Engine.IsEditorHint())
        {
            // 仅在编辑器中执行
            // 用于：实时预览、编辑器工具
            UpdateEditorPreview();
        }
        else
        {
            // 仅在游戏运行时执行
            UpdateGameLogic();
        }
    }
    
    private void UpdateEditorPreview()
    {
        // 编辑器预览逻辑
        // 例如：显示调试信息、实时更新可视化
    }
    
    private void UpdateGameLogic()
    {
        // 游戏逻辑
    }
}

// Engine.IsEditorHint() 常见使用场景：
// 1. 编辑器预览效果（如程序化生成的网格）
// 2. 避免在编辑器中执行游戏逻辑
// 3. 编辑器专用的可视化辅助
// 4. 防止编辑器中的性能问题

// 示例：程序化生成网格
[Tool]
public partial class ProceduralMesh : MeshInstance2D
{
    [Export] public int GridSize = 10;
    
    public override void _Process(double delta)
    {
        if (Engine.IsEditorHint())
        {
            // 在编辑器中实时更新网格
            GenerateMesh();
        }
    }
    
    private void GenerateMesh()
    {
        // 生成网格逻辑
    }
}
```
</editor_plugins>

<advanced_topics>
## 高级主题

### 抽象类和接口
```csharp
// 抽象类
public abstract partial class Entity : Node2D
{
    public abstract void TakeDamage(int amount);
    public abstract void Die();
}

public partial class Player : Entity
{
    public override void TakeDamage(int amount)
    {
        Health -= amount;
    }
    
    public override void Die()
    {
        QueueFree();
    }
}

// 接口
public interface IDamageable
{
    void TakeDamage(int amount);
}

public partial class Enemy : CharacterBody2D, IDamageable
{
    public void TakeDamage(int amount)
    {
        Health -= amount;
    }
}
```

### 自定义属性和反射
```csharp
[AttributeUsage(AttributeTargets.Property)]
public class SaveableAttribute : Attribute
{
    public string Key { get; set; }
    
    public SaveableAttribute(string key = "")
    {
        Key = key;
    }
}

public partial class Player : Node
{
    [Saveable("player_health")]
    public int Health { get; set; } = 100;
}

// 使用反射读取
public Dictionary<string, object> GetSaveableData(object obj)
{
    var data = new Dictionary<string, object>();
    var type = obj.GetType();
    
    foreach (var prop in type.GetProperties())
    {
        var attr = prop.GetCustomAttribute<SaveableAttribute>();
        if (attr != null)
        {
            string key = string.IsNullOrEmpty(attr.Key) ? prop.Name : attr.Key;
            data[key] = prop.GetValue(obj);
        }
    }
    
    return data;
}
```

**⚠️ 反射性能警告：**
```csharp
// ❌ 差 - 在热路径使用反射
public override void _Process(double delta)
{
    var data = GetSaveableData(this); // 每帧都反射，非常慢！
}

// ✅ 好 - 缓存反射结果
private Dictionary<string, PropertyInfo> _saveableProps;

public override void _Ready()
{
    // 只反射一次
    _saveableProps = new Dictionary<string, PropertyInfo>();
    var type = GetType();
    
    foreach (var prop in type.GetProperties())
    {
        var attr = prop.GetCustomAttribute<SaveableAttribute>();
        if (attr != null)
        {
            string key = string.IsNullOrEmpty(attr.Key) ? prop.Name : attr.Key;
            _saveableProps[key] = prop;
        }
    }
}

public Dictionary<string, object> GetSaveableDataFast()
{
    var data = new Dictionary<string, object>();
    foreach (var kvp in _saveableProps)
    {
        data[kvp.Key] = kvp.Value.GetValue(this);
    }
    return data;
}

// 反射的性能影响：
// - 反射比直接访问慢 10-100 倍
// - 不要在 _Process、_PhysicsProcess 中使用
// - 适合在初始化时使用（_Ready、_EnterTree）
// - 缓存反射结果可以大幅提升性能
```

### 服务定位器模式
```csharp
public partial class ServiceLocator : Node
{
    public static ServiceLocator Instance { get; private set; }
    
    private Dictionary<Type, object> _services = new();
    
    public override void _Ready()
    {
        Instance = this;
    }
    
    public void Register<T>(T service)
    {
        _services[typeof(T)] = service;
    }
    
    public T Get<T>()
    {
        if (_services.TryGetValue(typeof(T), out var service))
        {
            return (T)service;
        }
        throw new Exception($"服务 {typeof(T)} 未注册");
    }
}

// 使用
ServiceLocator.Instance.Register<IAudioManager>(new AudioManager());
var audio = ServiceLocator.Instance.Get<IAudioManager>();
```

### 单元测试（GdUnit4Net）
```csharp
using GdUnit4;

[TestSuite]
public class PlayerTests
{
    [TestCase]
    public void TestHealthDecrease()
    {
        var player = new Player();
        player.Health = 100;
        
        player.TakeDamage(30);
        
        Assertions.AssertThat(player.Health).IsEqual(70);
    }
    
    [TestCase]
    public async Task TestPlayerSpawn()
    {
        var runner = ISceneRunner.Load("res://Scenes/Game.tscn");
        await runner.SimulateFrames(10);
        
        var player = runner.FindChild<Player>("Player");
        Assertions.AssertThat(player).IsNotNull();
    }
}
```
</advanced_topics>

<resource_loading>
## 资源加载优化

### preload vs GD.Load
```csharp
// ⚠️ 注意：preload 是 GDScript 特有的编译时加载
// preload("res://icon.png")  # GDScript only

// C# 中没有 preload，只能用 GD.Load
var texture = GD.Load<Texture2D>("res://icon.png");

// 区别：
// - preload: 编译时加载，游戏启动时已在内存中（GDScript only）
// - GD.Load: 运行时加载，首次调用时加载到内存
// - 性能影响：GD.Load 首次调用稍慢，但后续调用会使用缓存

// C# 的替代方案：在 _Ready 中预加载
[Export] public Texture2D PreloadedTexture; // 在编辑器中分配
// 或
private Texture2D _texture;
public override void _Ready()
{
    _texture = GD.Load<Texture2D>("res://icon.png"); // 启动时加载
}
```

### GD.Load vs ResourceLoader
```csharp
// 推荐 - 简洁
var texture = GD.Load<Texture2D>("res://icon.png");

// 等价
var texture = ResourceLoader.Load<Texture2D>("res://icon.png");
```

### 资源缓存
Godot 自动缓存已加载的资源，多次 Load 同一路径不会重复加载。

```csharp
// 这两次调用返回同一个实例
var tex1 = GD.Load<Texture2D>("res://icon.png");
var tex2 = GD.Load<Texture2D>("res://icon.png");
// tex1 == tex2 为 true

// 缓存机制：
// - 资源按路径缓存
// - 只要有引用存在，资源就不会被卸载
// - 场景切换时，未被引用的资源会被自动清理
// - 无法手动清除单个资源缓存
```

### 后台加载大资源
```csharp
public async Task<PackedScene> LoadSceneAsync(string path)
{
    // 请求后台加载
    ResourceLoader.LoadThreadedRequest(path);
    
    while (true)
    {
        var progress = new Godot.Collections.Array();
        var status = ResourceLoader.LoadThreadedGetStatus(path, progress);
        
        // 所有可能的状态：
        switch (status)
        {
            case ResourceLoader.ThreadLoadStatus.InvalidResource:
                GD.PrintErr($"无效资源: {path}");
                return null;
                
            case ResourceLoader.ThreadLoadStatus.InProgress:
                // 继续等待
                float percent = progress.Count > 0 ? (float)progress[0] : 0;
                GD.Print($"加载进度: {percent * 100}%");
                break;
                
            case ResourceLoader.ThreadLoadStatus.Failed:
                GD.PrintErr($"加载失败: {path}");
                return null;
                
            case ResourceLoader.ThreadLoadStatus.Loaded:
                // 加载完成，获取资源
                return ResourceLoader.LoadThreadedGet(path) as PackedScene;
        }
        
        // 等待下一帧
        await ToSignal(GetTree(), SceneTree.SignalName.ProcessFrame);
    }
}
```
</resource_loading>

<common_issues>
## 常见问题

### Partial Classes 编译错误
错误：`CS0260: Missing partial modifier`

解决：所有继承自 GodotObject 的类必须使用 `partial` 关键字。

```csharp
// 错误
public class Player : Node2D

// 正确
public partial class Player : Node2D
```

### Export 变量不显示
问题：[Export] 变量在 Inspector 中不显示。

解决方案：
1. 变量必须是 public
2. 变量名必须首字母大写（PascalCase）
3. 重新编译项目（Build 按钮）

```csharp
// 错误 - 不会显示
[Export] private int health;
[Export] public int health; // 小写

// 正确
[Export] public int Health { get; set; }
```

### 线程崩溃
错误：在非主线程操作节点导致崩溃。

解决：使用 CallDeferred。

```csharp
// 错误
await Task.Delay(1000);
AddChild(node);

// 正确
await Task.Delay(1000);
CallDeferred(MethodName.AddChild, node);
```

### 信号内存泄漏
问题：未断开信号连接导致内存泄漏。

解决：在 _ExitTree 中断开信号。

```csharp
public override void _Ready()
{
    player.HealthChanged += OnHealthChanged;
}

public override void _ExitTree()
{
    player.HealthChanged -= OnHealthChanged;
}
```
</common_issues>

<quick_reference>
## 快速参考

### 常用快捷键
- F5 - 运行项目
- F6 - 运行当前场景
- Ctrl+B - 编译 C# 项目
- Ctrl+Shift+A - 添加子节点
- Ctrl+D - 复制节点

### 常用路径
- `res://` - 项目根目录
- `user://` - 用户数据目录（Windows: %APPDATA%/Godot/app_userdata/[项目名]）

### 常用节点类型
- Node2D - 2D 基础节点
- Sprite2D - 2D 精灵
- CharacterBody2D - 2D 角色物理
- Area2D - 2D 触发区域
- Timer - 定时器
- AudioStreamPlayer - 音频播放器

### 常用方法
```csharp
GetNode<T>("path")           // 获取节点
QueueFree()                  // 删除节点
AddChild(node)               // 添加子节点
GetTree()                    // 获取场景树
EmitSignal(name, args)       // 发射信号
CallDeferred(method, args)   // 延迟调用
```
</quick_reference>


<viewport_system>
## Viewport 坐标系统

### Viewport 基础
```csharp
// 获取 Viewport 大小
Vector2 viewportSize = GetViewportRect().Size;

// 获取鼠标在 Viewport 中的位置
Vector2 mousePos = GetViewport().GetMousePosition();

// 获取 Viewport 变换
Transform2D viewportTransform = GetViewport().GetCanvasTransform();

// 获取 Viewport 的全局变换
Transform2D globalTransform = GetViewport().GetGlobalCanvasTransform();
```

### 多 Viewport 使用
```csharp
public partial class MiniMap : SubViewport
{
    private Camera2D _minimapCamera;
    
    public override void _Ready()
    {
        _minimapCamera = new Camera2D();
        AddChild(_minimapCamera);
        
        // 设置 Viewport 大小
        Size = new Vector2I(200, 200);
    }
    
    public void UpdateCamera(Vector2 playerPos)
    {
        _minimapCamera.GlobalPosition = playerPos;
    }
}
```
</viewport_system>

<advanced_input>
## 高级输入处理

### Input.GetVector() 简化方向输入
```csharp
public override void _PhysicsProcess(double delta)
{
    // 自动处理四个方向输入，返回归一化向量
    Vector2 direction = Input.GetVector("move_left", "move_right", "move_up", "move_down");
    
    Velocity = direction * Speed;
    MoveAndSlide();
}
```

### 手柄输入
```csharp
public override void _Process(double delta)
{
    // 检测手柄连接
    var joypads = Input.GetConnectedJoypads();
    if (joypads.Count == 0) return;
    
    // 获取摇杆输入
    float leftStickX = Input.GetJoyAxis(0, JoyAxis.LeftX);
    float leftStickY = Input.GetJoyAxis(0, JoyAxis.LeftY);
    
    // 获取按钮输入
    if (Input.IsJoyButtonPressed(0, JoyButton.A))
    {
        Jump();
    }
    
    // 获取扳机输入（0.0 到 1.0）
    float rightTrigger = Input.GetJoyAxis(0, JoyAxis.TriggerRight);
}
```

### 触摸输入
```csharp
public override void _Input(InputEvent @event)
{
    if (@event is InputEventScreenTouch touch)
    {
        if (touch.Pressed)
        {
            GD.Print($"触摸位置: {touch.Position}");
        }
    }
    
    if (@event is InputEventScreenDrag drag)
    {
        GD.Print($"拖动: {drag.Relative}");
    }
}
```
</advanced_input>

<advanced_export>
## 高级 Export 属性

### 枚举和标志
```csharp
public partial class AdvancedExport : Node
{
    // 枚举下拉菜单
    public enum Difficulty { Easy, Normal, Hard, Extreme }
    [Export] public Difficulty GameDifficulty = Difficulty.Normal;
    
    // 标志（多选）
    [Flags]
    public enum Abilities { None = 0, Jump = 1, Dash = 2, Fly = 4, Swim = 8 }
    [Export(PropertyHint.Flags, "Jump,Dash,Fly,Swim")]
    public Abilities PlayerAbilities = Abilities.Jump | Abilities.Dash;
    
    // 物理层
    [Export(PropertyHint.Layers2DPhysics)]
    public uint CollisionLayer = 1;
    
    [Export(PropertyHint.Layers2DPhysics)]
    public uint CollisionMask = 1;
    
    // 颜色（无 Alpha）
    [Export(PropertyHint.ColorNoAlpha)]
    public Color BackgroundColor = Colors.White;
    
    // 指数范围
    [Export(PropertyHint.ExpRange, "0.01,100,0.01")]
    public float ZoomLevel = 1.0f;
}
```

### 自定义导出组
```csharp
public partial class GroupedExport : Node
{
    [ExportGroup("Movement")]
    [Export] public float Speed = 300.0f;
    [Export] public float JumpForce = 400.0f;
    [Export] public float Gravity = 980.0f;
    
    [ExportGroup("Combat")]
    [Export] public int MaxHealth = 100;
    [Export] public int AttackDamage = 10;
    [Export] public float AttackCooldown = 1.0f;
    
    [ExportGroup("Visual")]
    [Export] public Color PlayerColor = Colors.Blue;
    [Export] public Texture2D PlayerTexture;
}
```
</advanced_export>

<audio_2d>
## 2D 位置音频

### AudioStreamPlayer2D 使用
```csharp
public partial class SoundEmitter : Node2D
{
    [Export] public AudioStream Sound;
    private AudioStreamPlayer2D _player;
    
    public override void _Ready()
    {
        _player = new AudioStreamPlayer2D();
        _player.Stream = Sound;
        _player.MaxDistance = 1000; // 最大听到距离
        _player.Attenuation = 2.0f; // 衰减系数
        AddChild(_player);
    }
    
    public void PlaySound()
    {
        _player.Play();
    }
}
```

### 音频管理器（支持 2D 音效）
```csharp
public partial class AudioManager2D : Node
{
    [Export] public PackedScene AudioPlayer2DScene;
    
    public void PlaySoundAt(AudioStream sound, Vector2 position)
    {
        var player = new AudioStreamPlayer2D();
        player.Stream = sound;
        player.GlobalPosition = position;
        player.Autoplay = true;
        
        // 播放完自动删除
        player.Finished += () => player.QueueFree();
        
        GetTree().Root.AddChild(player);
    }
}
```
</audio_2d>

<shader_examples>
## 更多 Shader 示例

### 溶解效果
```gdshader
shader_type canvas_item;

uniform sampler2D noise_texture;
uniform float dissolve_amount : hint_range(0.0, 1.0) = 0.0;

void fragment() {
    vec4 tex = texture(TEXTURE, UV);
    float noise = texture(noise_texture, UV).r;
    
    if (noise < dissolve_amount) {
        discard;
    }
    
    COLOR = tex;
}
```

### 描边效果
```gdshader
shader_type canvas_item;

uniform vec4 outline_color : source_color = vec4(1.0, 1.0, 1.0, 1.0);
uniform float outline_width : hint_range(0.0, 10.0) = 1.0;

void fragment() {
    vec4 tex = texture(TEXTURE, UV);
    
    if (tex.a < 0.5) {
        // 检查周围像素
        float alpha = 0.0;
        for (float x = -outline_width; x <= outline_width; x++) {
            for (float y = -outline_width; y <= outline_width; y++) {
                vec2 offset = vec2(x, y) * TEXTURE_PIXEL_SIZE;
                alpha = max(alpha, texture(TEXTURE, UV + offset).a);
            }
        }
        
        if (alpha > 0.5) {
            COLOR = outline_color;
        } else {
            COLOR = tex;
        }
    } else {
        COLOR = tex;
    }
}
```

### 波浪效果
```gdshader
shader_type canvas_item;

uniform float wave_speed = 2.0;
uniform float wave_amplitude = 10.0;
uniform float wave_frequency = 5.0;

void vertex() {
    float wave = sin(TIME * wave_speed + VERTEX.x * wave_frequency) * wave_amplitude;
    VERTEX.y += wave;
}
```
</shader_examples>

<testing_advanced>
## 高级测试

### 场景测试（Scene Runner）
```csharp
using GdUnit4;

[TestSuite]
public class GameSceneTests
{
    [TestCase]
    public async Task TestPlayerMovement()
    {
        // 加载场景
        var runner = ISceneRunner.Load("res://Scenes/Game.tscn");
        
        // 模拟输入
        runner.SimulateKeyPress(Key.Right);
        
        // 模拟多帧
        await runner.SimulateFrames(60);
        
        // 验证结果
        var player = runner.FindChild<Player>("Player");
        Assertions.AssertThat(player.Position.X).IsGreater(0);
    }
    
    [TestCase]
    public async Task TestEnemySpawn()
    {
        var runner = ISceneRunner.Load("res://Scenes/Game.tscn");
        
        // 等待 5 秒
        await runner.SimulateFrames(300);
        
        // 验证敌人生成
        var enemies = runner.FindChildren<Enemy>();
        Assertions.AssertThat(enemies.Count).IsGreater(0);
    }
}
```

### Mocking 示例
```csharp
using GdUnit4;

[TestSuite]
public class PlayerWithMockTests
{
    [TestCase]
    public void TestPlayerWithMockAudio()
    {
        // 创建 Mock
        var mockAudio = Mock.Create<IAudioManager>();
        
        // 创建玩家并注入 Mock
        var player = new Player();
        player.AudioManager = mockAudio;
        
        // 执行操作
        player.Jump();
        
        // 验证 Mock 被调用
        Mock.Verify(mockAudio, 1, "PlaySound", "jump");
    }
    
    [TestCase]
    public void TestPlayerWithMockInput()
    {
        var mockInput = Mock.Create<IInputHandler>();
        Mock.Setup(mockInput, "GetMoveDirection").Returns(Vector2.Right);
        
        var player = new Player();
        player.InputHandler = mockInput;
        
        player.ProcessMovement(0.016f);
        
        Assertions.AssertThat(player.Velocity.X).IsGreater(0);
    }
}
```
</testing_advanced>

<performance_advanced>
## 高级性能优化

### 避免 LINQ 在热路径
```csharp
// 差 - LINQ 在 _Process 中
public override void _Process(double delta)
{
    var activeEnemies = enemies.Where(e => e.IsActive).ToList();
}

// 好 - 使用传统循环
public override void _Process(double delta)
{
    activeEnemies.Clear();
    foreach (var enemy in enemies)
    {
        if (enemy.IsActive)
            activeEnemies.Add(enemy);
    }
}
```

### 使用 Struct 优化内存
```csharp
// 值类型 - 栈分配，更快
public struct DamageInfo
{
    public int Amount;
    public Vector2 Position;
    public DamageType Type;
}

// 引用类型 - 堆分配，有 GC 压力
public class DamageInfo
{
    public int Amount { get; set; }
    public Vector2 Position { get; set; }
    public DamageType Type { get; set; }
}
```

### 避免装箱拆箱
```csharp
// 差 - 装箱
object value = 42; // int 装箱为 object
int number = (int)value; // 拆箱

// 好 - 使用泛型
public void ProcessValue<T>(T value) where T : struct
{
    // 无装箱
}
```

### 使用 ArrayPool 减少分配
```csharp
using System.Buffers;

public void ProcessLargeArray()
{
    // 从池中租用数组
    int[] buffer = ArrayPool<int>.Shared.Rent(1000);
    
    try
    {
        // 使用数组
        for (int i = 0; i < 1000; i++)
        {
            buffer[i] = i * 2;
        }
    }
    finally
    {
        // 归还数组到池
        ArrayPool<int>.Shared.Return(buffer);
    }
}
```
</performance_advanced>

<godot_concepts>
## Godot 特有概念

### NodePath 和路径语法
```csharp
// 相对路径
GetNode("Child");              // 直接子节点
GetNode("Child/GrandChild");   // 嵌套路径
GetNode("../Sibling");         // 父节点的子节点

// 绝对路径
GetNode("/root/GameManager");  // 从根节点开始

// NodePath 类型（性能优化）
private NodePath _playerPath = "Player";
var player = GetNode<Player>(_playerPath);
```

### StringName（性能优化）
StringName 是 Godot 的优化字符串类型，用于频繁比较的字符串。

```csharp
// 信号名使用 StringName
EmitSignal(SignalName.HealthChanged, 100);

// 方法名使用 StringName
CallDeferred(MethodName.UpdateUI, data);

// 为什么用 StringName？
// - 内部使用哈希，比较速度快
// - 避免字符串拼写错误
// - 编译时检查
```

### Variant 类型
Godot 的动态类型系统，用于与 GDScript 互操作。

```csharp
// Variant 可以存储任何 Godot 类型
Variant value = 42;
value = "Hello";
value = new Vector2(1, 2);

// 类型检查
if (value.VariantType == Variant.Type.Int)
{
    int number = value.AsInt32();
}

// 从 Dictionary 获取值
var dict = new Godot.Collections.Dictionary();
dict["health"] = 100;
Variant health = dict["health"];
int healthValue = health.AsInt32();
```

### Godot.Collections vs System.Collections
```csharp
// ❌ 错误 - 不能 Export System.Collections
[Export] public List<int> Numbers; // 不会显示在 Inspector

// ✅ 正确 - 使用 Godot.Collections
[Export] public Godot.Collections.Array<int> Numbers;

// 何时用哪个？
// - Export 变量：必须用 Godot.Collections
// - 内部逻辑：推荐用 System.Collections（性能更好）
// - 与 GDScript 交互：必须用 Godot.Collections

// 转换
var godotArray = new Godot.Collections.Array<int> { 1, 2, 3 };
var systemList = new List<int>(godotArray); // Godot → System
```

### Callable 详细用法
```csharp
// 无参数方法
Callable.From(MyMethod);

// 带参数方法
Callable.From(() => MyMethod(arg1, arg2));

// 泛型参数
Callable.From<int>(OnHealthChanged);
Callable.From<int, string>(OnDamage);

// 为什么需要 Callable？
// - Godot 的信号系统需要
// - 跨语言调用（C# ↔ GDScript）
// - 延迟调用（CallDeferred）
```
</godot_concepts>

<memory_management_details>
## 内存管理详解

### QueueFree() vs Free()
```csharp
// QueueFree() - 安全（推荐）
// - 在当前帧结束时删除
// - 允许当前帧的其他代码继续访问节点
// - 不会导致空引用异常
QueueFree();

// Free() - 危险
// - 立即删除节点
// - 如果其他代码还在使用会崩溃
// - 只在确定没有其他引用时使用
Free();

// 示例：为什么 QueueFree 更安全
public void OnAreaEntered(Node2D body)
{
    if (body is Player)
    {
        QueueFree(); // 安全 - 信号处理完成后才删除
        // Free();   // 危险 - 可能还有其他信号处理器
    }
}
```

### Node 引用计数和 C# GC
```csharp
// Godot 使用引用计数管理 Node
// C# 的 GC 与 Godot 的引用计数配合工作

// 场景中的节点：由 Godot 管理
var sprite = GetNode<Sprite2D>("Sprite");
// sprite 变量只是引用，不影响生命周期

// 动态创建的节点：需要添加到树中
var newSprite = new Sprite2D();
// 此时 newSprite 只有 C# 引用
AddChild(newSprite);
// 现在 Godot 也持有引用，即使 C# 变量超出作用域也不会被删除

// 从树中移除但不删除
RemoveChild(newSprite);
// newSprite 仍然存在，可以重新添加
AddChild(newSprite);
```

### 资源的生命周期
```csharp
// 资源（Resource）的缓存
var tex1 = GD.Load<Texture2D>("res://icon.png");
var tex2 = GD.Load<Texture2D>("res://icon.png");
// tex1 == tex2 为 true（同一个实例）

// 手动清除缓存（很少需要）
ResourceLoader.LoadThreadedRequest("res://large_texture.png");
// ... 使用资源 ...
// 无法手动清除单个资源缓存
// 只能通过场景切换时自动清理未使用的资源
```
</memory_management_details>

<common_pitfalls>
## 常见陷阱

### _Ready() 调用顺序
```csharp
// ⚠️ 陷阱：_Ready() 从子节点到父节点调用
public partial class Parent : Node
{
    private Child _child;
    
    public override void _Ready()
    {
        // 此时 Child._Ready() 已经执行完毕
        _child = GetNode<Child>("Child");
        _child.DoSomething(); // 安全
    }
}

public partial class Child : Node
{
    public override void _Ready()
    {
        // 此时 Parent._Ready() 还没执行
        var parent = GetParent<Parent>();
        // parent.SomeField 可能还是 null！
    }
}

// ✅ 解决方案：使用 _EnterTree() 或延迟初始化
public partial class Child : Node
{
    public override void _Ready()
    {
        // 延迟到下一帧
        CallDeferred(MethodName.Initialize);
    }
    
    private void Initialize()
    {
        // 现在 Parent._Ready() 已经执行
        var parent = GetParent<Parent>();
        parent.SomeField.DoSomething(); // 安全
    }
}
```

### 场景实例化时机
```csharp
// ⚠️ 陷阱：Instantiate() 后节点还不在树中
var enemy = enemyScene.Instantiate<Enemy>();
// enemy.GetNode("Sprite"); // ❌ 错误 - 节点还不在树中
// enemy._Ready() 还没被调用

AddChild(enemy);
// 现在 enemy 在树中，_Ready() 已被调用
enemy.GetNode<Sprite2D>("Sprite"); // ✅ 正确
```

### Autoload 初始化顺序
```csharp
// ⚠️ 陷阱：Autoload 按 Project Settings 中的顺序初始化

// 如果 AudioManager 在 GameManager 之前
public partial class AudioManager : Node
{
    public override void _Ready()
    {
        // GameManager 还没初始化！
        // GameManager.Instance 是 null
    }
}

// ✅ 解决方案：延迟访问或调整顺序
public partial class AudioManager : Node
{
    public override void _Ready()
    {
        // 不在 _Ready 中访问其他 Autoload
    }
    
    public void Initialize()
    {
        // 由 GameManager 在其 _Ready 中调用
        var gm = GameManager.Instance; // 安全
    }
}
```

### Export 类型限制
```csharp
// ❌ 不能 Export 的类型
[Export] public List<int> Numbers;           // System.Collections
[Export] public Dictionary<string, int> Map; // System.Collections
[Export] public MyCustomClass Data;          // 非 Resource 类

// ✅ 可以 Export 的类型
[Export] public Godot.Collections.Array<int> Numbers;
[Export] public Godot.Collections.Dictionary<string, int> Map;
[Export] public MyCustomResource Data; // 继承 Resource

// 自定义 Resource
[GlobalClass]
public partial class MyCustomResource : Resource
{
    [Export] public string Name { get; set; }
    [Export] public int Value { get; set; }
}
```

### 信号参数类型限制
```csharp
// ❌ 不能用自定义 class 作为信号参数
public class DamageInfo
{
    public int Amount;
    public Vector2 Position;
}

[Signal]
public delegate void DamagedEventHandler(DamageInfo info); // ❌ 错误

// ✅ 解决方案 1：使用多个参数
[Signal]
public delegate void DamagedEventHandler(int amount, Vector2 position);

// ✅ 解决方案 2：使用 Resource
[GlobalClass]
public partial class DamageInfo : Resource
{
    [Export] public int Amount { get; set; }
    [Export] public Vector2 Position { get; set; }
}

[Signal]
public delegate void DamagedEventHandler(DamageInfo info); // ✅ 正确
```

### GetNode 性能陷阱
```csharp
// ❌ 性能差 - 每帧遍历树
public override void _Process(double delta)
{
    var sprite = GetNode<Sprite2D>("Sprite");
    sprite.Position += Vector2.Right;
}

// ✅ 性能好 - 缓存引用
private Sprite2D _sprite;

public override void _Ready()
{
    _sprite = GetNode<Sprite2D>("Sprite");
}

public override void _Process(double delta)
{
    _sprite.Position += Vector2.Right;
}

// GetNode 的开销：
// - 字符串解析
// - 树遍历
// - 类型转换
// 在热路径（_Process）中避免使用
```
</common_pitfalls>

<file_paths>
## 文件路径系统

### res:// 和 user:// 路径
```csharp
// res:// - 项目资源路径（只读）
var texture = GD.Load<Texture2D>("res://Assets/icon.png");
var scene = GD.Load<PackedScene>("res://Scenes/Player.tscn");

// user:// - 用户数据路径（可读写）
var savePath = "user://savegame.json";
var file = FileAccess.Open(savePath, FileAccess.ModeFlags.Write);

// user:// 的实际位置：
// Windows: %APPDATA%\Godot\app_userdata\[项目名]\
// Linux: ~/.local/share/godot/app_userdata/[项目名]/
// macOS: ~/Library/Application Support/Godot/app_userdata/[项目名]/

// 获取实际路径
string userPath = ProjectSettings.GlobalizePath("user://");
GD.Print($"用户数据路径: {userPath}");
```

### FileAccess 错误处理
```csharp
var file = FileAccess.Open("user://savegame.json", FileAccess.ModeFlags.Read);

if (file == null)
{
    var error = FileAccess.GetOpenError();
    
    switch (error)
    {
        case Error.FileNotFound:
            GD.Print("文件不存在");
            break;
        case Error.FileNoPermission:
            GD.Print("没有权限");
            break;
        case Error.FileCantOpen:
            GD.Print("无法打开文件");
            break;
        default:
            GD.PrintErr($"未知错误: {error}");
            break;
    }
    
    return;
}

// 使用文件...
file.Close();
```
</file_paths>
