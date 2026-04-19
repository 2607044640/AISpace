# Event → R3 迁移日志

## 📅 迁移时间
2026-04-18

## 🎯 迁移目标
将 BaseInputComponent 的 C# event 迁移到 R3 Subject，提升输入系统的响应式编程能力。

---

## ✅ 已完成迁移

### 1. **BaseInputComponent** (核心输入抽象类)
**文件：** `3d-practice/addons/A1MyAddon/CoreComponents/BaseInputComponent.cs`

**迁移前：**
```csharp
public event Action<Vector2> OnMovementInput;
public event Action OnJumpJustPressed;
```

**迁移后：**
```csharp
public Subject<Vector2> MovementInput { get; } = new();
public Subject<Unit> JumpPressed { get; } = new();
```

**变更：**
- ✅ 添加 `using R3;`
- ✅ 替换 event 为 Subject
- ✅ 添加 `_ExitTree()` 清理资源
- ✅ 更新触发方法：`Invoke()` → `OnNext()`

---

### 2. **GroundMovementComponent** (地面移动组件)
**文件：** `3d-practice/addons/A1MyAddon/CoreComponents/GroundMovementComponent.cs`

**迁移前：**
```csharp
_inputComponent.OnMovementInput += HandleMovementInput;
_inputComponent.OnJumpJustPressed += HandleJumpInput;
```

**迁移后：**
```csharp
_inputComponent.MovementInput
    .Subscribe(direction => _currentInputDirection = direction)
    .AddTo(_disposables);

_inputComponent.JumpPressed
    .Subscribe(_ => _jumpRequested = true)
    .AddTo(_disposables);
```

**变更：**
- ✅ 添加 `using R3;`
- ✅ 添加 `CompositeDisposable _disposables`
- ✅ 替换 `+=` 订阅为 `.Subscribe().AddTo()`
- ✅ 删除 `HandleMovementInput()` 和 `HandleJumpInput()` 方法
- ✅ 更新 `_ExitTree()` 为 `_disposables.Dispose()`

---

### 3. **FlyMovementComponent** (飞行移动组件)
**文件：** `3d-practice/addons/A1MyAddon/CoreComponents/FlyMovementComponent.cs`

**迁移前：**
```csharp
_inputComponent.OnMovementInput += HandleMovementInput;
```

**迁移后：**
```csharp
_inputComponent.MovementInput
    .Subscribe(direction => _currentInputDirection = direction)
    .AddTo(_disposables);
```

**变更：**
- ✅ 添加 `using R3;`
- ✅ 添加 `CompositeDisposable _disposables`
- ✅ 替换订阅方式
- ✅ 删除 `HandleMovementInput()` 方法

---

### 4. **CharacterRotationComponent** (角色旋转组件)
**文件：** `3d-practice/addons/A1MyAddon/CoreComponents/CharacterRotationComponent.cs`

**迁移前：**
```csharp
_inputComponent.OnMovementInput += HandleMovementInput;
```

**迁移后：**
```csharp
_inputComponent.MovementInput
    .Subscribe(direction => _currentInputDir = direction)
    .AddTo(_disposables);
```

**变更：**
- ✅ 添加 `using R3;`
- ✅ 添加 `CompositeDisposable _disposables`
- ✅ 替换订阅方式
- ✅ 删除 `HandleMovementInput()` 方法

---

### 5. **InputToStateOperator** (输入到状态转换器)
**文件：** `3d-practice/addons/A1MyAddon/CoreComponents/Examples/InputToStateOperator.cs`

**迁移前：**
```csharp
_inputComponent.OnJumpJustPressed += HandleJumpInput;
_inputComponent.OnMovementInput += HandleMovementInput;
```

**迁移后：**
```csharp
_inputComponent.JumpPressed
    .Subscribe(_ => HandleJumpInput())
    .AddTo(_disposables);

_inputComponent.MovementInput
    .Subscribe(direction => HandleMovementInput(direction))
    .AddTo(_disposables);
```

**变更：**
- ✅ 添加 `using R3;`
- ✅ 添加 `CompositeDisposable _disposables`
- ✅ 替换订阅方式（保留原有方法调用）

---

## ❌ 未迁移（保持现状）

### 1. **Helper 类** (UI 组件)
- `ToggleComponentHelper.cs`
- `SliderComponentHelper.cs`
- `DropdownComponentHelper.cs`
- `OptionComponentHelper.cs`
- `ThemeSwitcherComponentHelper.cs`

**原因：** 已实现 `event + ReactiveProperty` 混合模式，完美兼容新旧代码。

---

### 2. **HealthComponent** (生命值组件)
**文件：** `3d-practice/addons/A1MyAddon/CoreComponents/Examples/Enemy_Example.cs`

**保留的 event：**
```csharp
public event Action<float> OnDamaged;
public event Action<float> OnHealed;
public event Action OnDied;
```

**原因：**
- 订阅者仅1个（Box_Example）
- 功能简单，event 已经足够
- 迁移收益不大

---

### 3. **第三方库 Event**
- `StateChart.cs`
- `Transition.cs`
- `R3.Godot` 插件

**原因：** 外部库 API，禁止修改。

---

## 📊 迁移统计

| 类别 | 数量 | 状态 |
|------|------|------|
| 迁移的核心组件 | 5 | ✅ 完成 |
| 保持现状的 Helper 类 | 5 | ✅ 无需修改 |
| 保留 event 的组件 | 1 | ✅ 评估后保留 |
| 编译警告 | 5 | ⚠️ 第三方库警告 |
| 编译错误 | 0 | ✅ 无错误 |

---

## 🎁 迁移收益

### 1. **自动内存管理**
- 旧方式：手动 `+=` 和 `-=`，容易遗漏导致内存泄漏
- 新方式：`.AddTo(_disposables)` + `_disposables.Dispose()`，自动清理

### 2. **支持 R3 操作符**
现在可以轻松添加高级功能：
```csharp
// 输入防抖（防止误触）
_inputComponent.JumpPressed
    .ThrottleFirst(TimeSpan.FromMilliseconds(200))
    .Subscribe(_ => HandleJump())
    .AddTo(_disposables);

// 输入组合（同时按下多个键）
Observable.CombineLatest(
    _inputComponent.MovementInput,
    _inputComponent.JumpPressed
).Subscribe(...)
.AddTo(_disposables);
```

### 3. **线程安全**
```csharp
// 异步操作后更新 UI
someAsyncStream
    .ObserveOn(GodotProvider.MainThread)
    .Subscribe(...)
    .AddTo(_disposables);
```

---

## 🚀 未来优化建议

### 1. **输入防抖**
在 `PlayerInputComponent` 中添加防抖，防止双击跳跃：
```csharp
JumpPressed
    .ThrottleFirst(TimeSpan.FromMilliseconds(200))
    .Subscribe(_ => TriggerJumpInput())
    .AddTo(_disposables);
```

### 2. **输入录制与回放**
使用 R3 的 `Replay()` 操作符实现输入录制：
```csharp
var recordedInput = MovementInput.Replay();
recordedInput.Connect(); // 开始录制
```

### 3. **输入统计**
使用 R3 的 `Scan()` 操作符统计输入频率：
```csharp
MovementInput
    .Scan(0, (count, _) => count + 1)
    .Subscribe(count => GD.Print($"移动输入次数: {count}"))
    .AddTo(_disposables);
```

---

## ✅ 验证结果

- ✅ 编译成功（0 错误）
- ✅ 所有订阅者已更新
- ✅ 内存管理已优化
- ✅ 代码风格统一

---

## 📝 注意事项

1. **备份文件夹未修改**
   - `.backup_old_components/` 中的旧代码未迁移
   - 这些是历史代码，不影响当前项目

2. **第三方库警告**
   - PhantomCamera 插件有 5 个警告
   - 这些是第三方库的问题，不影响本次迁移

3. **新代码规范**
   - 新组件应优先使用 `Subject<T>` 而不是 `event Action<T>`
   - 所有订阅必须调用 `.AddTo(_disposables)`
   - 所有组件必须在 `_ExitTree()` 中调用 `_disposables.Dispose()`
