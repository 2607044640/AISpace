# Godot ThemeGen Rules

## Overview
ThemeGen by Inspiaaa is the official Godot plugin for programmatic theme generation using GDScript. It enables code-based theme definition with style reuse, inheritance, and live preview capabilities.

**Plugin**: [Inspiaaa/ThemeGen](https://github.com/Inspiaaa/ThemeGen)  
**Project Location**: `A1UIResources/ThemeGen/`  
**Godot Version**: 4.0+

---

## Core Architecture

### Base Class Structure
```gdscript
@tool
extends ProgrammaticTheme

const UPDATE_ON_SAVE = true
const VERBOSITY = Verbosity.QUIET  # SILENT, QUIET, NORMAL

var color_primary = Color("#...")
var color_secondary = Color("#...")
var default_font_size = 16

func setup():
    set_save_path("res://A1UIResources/ThemeGen/generated/theme_name.tres")

func define_theme():
    define_default_font_size(default_font_size)
    # Define styles here
```

### Execution Flow
```
setup_*() → Initialize variables, set save path
    ↓
define_theme() → Define all styles and variants
    ↓
Generated .tres file → Output to generated/ folder
```

---

## API Reference

### Core Methods

#### Theme Setup
- `set_save_path(path)` - Set output .tres file path
- `define_default_font(resource)` - Set project-wide font
- `define_default_font_size(size)` - Set default font size
- `set_theme_generator(function)` - Override define_theme() for specific variant

#### Style Definition
- `define_style(node_type, properties_dict)` - Style a control type
- `define_variant_style(variant_name, base_type, properties_dict)` - Create type variation

#### StyleBox Helpers
- `stylebox_flat(props)` - Create StyleBoxFlat
- `stylebox_line(props)` - Create StyleBoxLine
- `stylebox_empty(props)` - Create StyleBoxEmpty
- `stylebox_texture(props)` - Create StyleBoxTexture
- `inherit(base, overrides...)` - Inherit and override properties
- `merge(a, b, c...)` - Merge multiple StyleBoxes

#### Shortcut Functions
- `border_width(all)` or `border_width(left, top, right, bottom)`
- `corner_radius(all)` or `corner_radius(tl, tr, br, bl)`
- `expand_margins(all)` or `expand_margins(left, top, right, bottom)`
- `content_margins(all)` or `content_margins(left, top, right, bottom)`
- `texture_margins(all)` or `texture_margins(left, top, right, bottom)`

### Underscore Suffix Pattern
```gdscript
stylebox_flat({
    bg_color = Color.WHITE,
    border_ = border_width(2),        # Expands to all 4 sides
    corner_ = corner_radius(8),       # Expands to all 4 corners
    content_ = content_margins(10)    # Expands to all 4 margins
})
```

### Built-in References
- `current_theme` - Access Theme instance directly
- `styles.Button.normal` - Reference parent styles in variants

---

## Multi-Variant System

### Creating Multiple Themes
```gdscript
func setup_light_theme():
    set_save_path("res://themes/generated/light.tres")
    background_color = Color.WHITE
    text_color = Color.BLACK

func setup_dark_theme():
    set_save_path("res://themes/generated/dark.tres")
    background_color = Color.BLACK
    text_color = Color.WHITE

func define_theme():
    # Shared definition for both variants
    define_style("Label", { font_color = text_color })
```

**Output**: Generates both `light.tres` and `dark.tres` from single script.

---

## Type Variations

### Creating Variants
```gdscript
# Base button style
define_style("Button", {
    normal = stylebox_flat({ bg_color = base_color }),
    font_color = text_color
})

# Accent button variant
define_variant_style("AccentButton", "Button", {
    normal = inherit(styles.Button.normal, {
        bg_color = accent_color
    }),
    font_color = Color.WHITE
})
```

### Using Variants in Scenes
**Inspector**: Theme → Theme Type Variation → "AccentButton"  
**C#**: `button.ThemeTypeVariation = "AccentButton";`

---

## C# Integration

### Loading Generated Themes
```csharp
private Theme _lightTheme = GD.Load<Theme>("res://A1UIResources/ThemeGen/generated/light_theme.tres");
private Theme _darkTheme = GD.Load<Theme>("res://A1UIResources/ThemeGen/generated/dark_theme.tres");
```

### Global Theme Switching
```csharp
// Apply to entire UI tree
GetTree().Root.Theme = _darkTheme;

// Apply to specific subtree
uiRootControl.Theme = _lightTheme;
```

### Runtime Overrides
```csharp
// WRONG - modifies shared resource
var stylebox = button.GetThemeStylebox("normal");
stylebox.BgColor = Colors.Red; // Affects ALL buttons!

// CORRECT - duplicate first
var stylebox = button.GetThemeStylebox("normal").Duplicate() as StyleBoxFlat;
stylebox.BgColor = Colors.Red;
button.AddThemeStyleboxOverride("normal", stylebox);
```

### Common Override Methods
```csharp
control.AddThemeStyleboxOverride("normal", styleBox);
control.AddThemeColorOverride("font_color", color);
control.AddThemeFontSizeOverride("font_size", size);
control.RemoveThemeStyleboxOverride("normal");
```

---

## Workflow Rules

### Theme Generation (GDScript)
✓ **DO**:
- Define all color palettes as variables in `setup_*()`
- Use helper functions for repetitive properties
- Create type variations for reusable patterns
- Enable `UPDATE_ON_SAVE = true` for live preview
- Set `VERBOSITY = Verbosity.QUIET` for clean output
- Output to `generated/` folder to indicate auto-generated files

✗ **DON'T**:
- Manually edit generated `.tres` files (will be overwritten)
- Hardcode colors in style definitions (use variables)
- Duplicate code between theme variants (use shared `define_theme()`)

### Theme Management (C#)
✓ **DO**:
- Load themes via `GD.Load<Theme>()` at initialization
- Use global theme switching for app-wide changes
- Apply type variations for specialized controls
- Always duplicate resources before modifying

✗ **DON'T**:
- Modify shared theme resources directly
- Use excessive per-node overrides (defeats theme purpose)
- Call `AddThemeOverride()` inside `_Notification(NOTIFICATION_THEME_CHANGED)` (infinite loop)

---

## Theme Inheritance Hierarchy

**Priority (Highest → Lowest)**:
1. Node theme overrides (`AddTheme*Override()`)
2. Node's theme property (direct assignment)
3. Parent node's theme property (inherited)
4. Project settings default theme
5. Godot editor default theme

**Best Practice**: Define 90% in theme, 10% as overrides.

---

## Live Preview System

### Manual Generation
1. Open theme script in Godot editor
2. Press `Ctrl+Shift+X` to run
3. Check Output tab for generation status

### Automatic Generation
1. Enable "ThemeGen Save Sync" plugin in Project Settings → Plugins
2. Add `const UPDATE_ON_SAVE = true` to theme script
3. Save script → Auto-regenerates theme

---

## Project-Specific Patterns

### Current Themes
- `modern_game_theme.gd` → Modern game UI style
- `light_minimal_theme.gd` → Clean light theme
- `dark_elegant_theme.gd` → Professional dark theme
- `fantasy_rpg_theme.gd` → Fantasy RPG aesthetic

### Common Patterns in Project
```gdscript
# Elevation effect with shadow
var button_normal = stylebox_flat({
    bg_color = background_elevated,
    corner_ = corner_radius(6),
    content_ = content_margins(18, 10, 18, 10),
    shadow_color = Color(0, 0, 0, 0.4),
    shadow_size = 4,
    shadow_offset = Vector2(0, 2)
})

# Glow effect on focus
var lineedit_focus = inherit(lineedit_normal, {
    border_color = accent_color,
    shadow_color = accent_color.darkened(0.5),
    shadow_size = 4
})
```

---

## Performance Considerations

- Theme switching: Lightweight (single property assignment)
- Type variations: No runtime overhead
- Per-node overrides: Linear scaling with node count
- Theme loading: Use `preload()` for instant access

---

## Integration with Project Architecture

### Separation of Concerns
- **ThemeGen (GDScript)**: Theme definition and generation
- **C# Helpers**: Runtime theme management and switching
- **Component System**: Theme variations align with component-based UI

### Helper Integration
```csharp
// ThemeSwitcherComponentHelper.cs
public partial class ThemeSwitcherComponentHelper : Node
{
    [Export] public Theme LightTheme { get; set; }
    [Export] public Theme DarkTheme { get; set; }
    
    public void SwitchTheme(bool isDark)
    {
        GetTree().Root.Theme = isDark ? DarkTheme : LightTheme;
    }
}
```

---

## Common Pitfalls

| Issue | Cause | Solution |
|-------|-------|----------|
| Theme not updating | Manual edit of .tres file | Regenerate via ThemeGen script |
| All buttons change color | Modified shared resource | Always `.Duplicate()` before modifying |
| Stack overflow | Override in NOTIFICATION_THEME_CHANGED | Move override logic outside notification |
| Variant not found | Typo in variation name | Check spelling, case-sensitive |
| Changes not visible | Editor cache | Reload scene or restart editor |

---

## Quick Reference

### Generate All Themes
```bash
# Open any theme script and press Ctrl+Shift+X
# Or enable Save Sync plugin for auto-generation
```

### Preview Themes
1. Open `theme_preview.tscn`
2. Select root node
3. Inspector → Theme → Load generated theme
4. View results

### Debug Output
```gdscript
const VERBOSITY = Verbosity.NORMAL  # See detailed generation logs
```

---

## Resources

- **GitHub**: https://github.com/Inspiaaa/ThemeGen
- **Asset Library**: Search "ThemeGen" in Godot AssetLib
- **Official Docs**: https://docs.godotengine.org/en/stable/tutorials/ui/gui_theme_type_variations.html
- **Project Themes**: `A1UIResources/ThemeGen/`
