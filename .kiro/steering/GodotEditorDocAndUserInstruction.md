---
inclusion: manual
---

# Godot Editor Mode Development

<instructions>
## Enable Editor Execution
Add `[Tool]` attribute to run scripts in Godot editor:
```csharp
[Tool]
[GlobalClass]
public partial class MyEditorScript : Node
{
    // Code runs in editor AND runtime
}
```

## Property Ordering
Properties display in declaration order. Put important parameters first:
```csharp
[ExportCategory("Main Settings")]
[Export] public Mode CurrentMode { get; set; }  // Shows first

[Export] public int DetailSetting { get; set; }  // Shows second
```

Use `[ExportCategory("Name")]` to group related properties.
</instructions>

<property_hiding>
## Hide Properties Dynamically
Override `_ValidateProperty()` to hide properties based on state:

```csharp
public override void _ValidateProperty(Godot.Collections.Dictionary property)
{
    string name = property["name"].AsStringName();
    
    if (name == "PropertyToHide")
    {
        property["usage"] = (int)PropertyUsageFlags.NoEditor;
    }
}
```

**Key flags:**
- `PropertyUsageFlags.NoEditor` - Hide from inspector, keep data
- `PropertyUsageFlags.Storage` - Save to file but don't show
</property_hiding>

<dynamic_updates>
## Trigger Property List Refresh
Call `NotifyPropertyListChanged()` when property visibility changes:

```csharp
private Mode _mode;

[Export]
public Mode CurrentMode
{
    get => _mode;
    set
    {
        _mode = value;
        NotifyPropertyListChanged();  // Refresh inspector
        UpdateBehavior();
    }
}
```

**When to call:**
- After changing enum that controls visibility
- After loading data that affects property display
- When toggling features on/off
</dynamic_updates>

<examples>
## Complete Example: Mode-Based Property Display

```csharp
[Tool]
[GlobalClass]
public partial class MarginHelper : MarginContainer
{
    public enum Mode { Uniform, TwoAxis, Individual }
    
    private Mode _mode = Mode.Uniform;
    
    [ExportCategory("Settings")]
    [Export]
    public Mode CurrentMode
    {
        get => _mode;
        set
        {
            _mode = value;
            NotifyPropertyListChanged();
            ApplyMargins();
        }
    }
    
    private int _uniform = 10;
    [Export] public int Uniform { get => _uniform; set { _uniform = value; ApplyMargins(); } }
    
    private int _horizontal = 10;
    [Export] public int Horizontal { get => _horizontal; set { _horizontal = value; ApplyMargins(); } }
    
    private int _vertical = 10;
    [Export] public int Vertical { get => _vertical; set { _vertical = value; ApplyMargins(); } }
    
    public override void _ValidateProperty(Godot.Collections.Dictionary property)
    {
        string name = property["name"].AsStringName();
        
        switch (CurrentMode)
        {
            case Mode.Uniform:
                if (name == "Horizontal" || name == "Vertical")
                    property["usage"] = (int)PropertyUsageFlags.NoEditor;
                break;
                
            case Mode.TwoAxis:
                if (name == "Uniform")
                    property["usage"] = (int)PropertyUsageFlags.NoEditor;
                break;
        }
    }
    
    private void ApplyMargins()
    {
        // [Tool] allows this to run in editor
        switch (CurrentMode)
        {
            case Mode.Uniform:
                AddThemeConstantOverride("margin_left", Uniform);
                AddThemeConstantOverride("margin_top", Uniform);
                break;
            case Mode.TwoAxis:
                AddThemeConstantOverride("margin_left", Horizontal);
                AddThemeConstantOverride("margin_top", Vertical);
                break;
        }
    }
}
```
</examples>

<common_issues>
## Troubleshooting

**Properties not hiding:**
- Restart Godot editor after code changes
- Verify `NotifyPropertyListChanged()` is called in setter
- Check property name matches exactly (case-sensitive)

**Changes not visible in editor:**
- Missing `[Tool]` attribute
- Method not called during property change
- Node not in scene tree when method runs

**Property order wrong:**
- Reorder `[Export]` declarations in code
- Group with `[ExportCategory("Name")]`
- Backing fields must be declared before properties
</common_issues>
