---
 inclusion: manual
---
<layer_1_quick_start>
  <quick_reference>
    - **Plugin Directory:** `A1UIResources/ThemeGen/`
    - **Output Directory:** `A1UIResources/ThemeGen/generated/*.tres`
    - **Base Class:** `@tool extends ProgrammaticTheme`
    - **Manual Generation:** Open script in editor -> Press `Ctrl+Shift+X`
  </quick_reference>

  <decision_tree>
    - **IF** styling a base Godot Control node globally -> **THEN** use `define_style(node_type, props)`. (Why: Establishes project-wide baseline).
    - **IF** creating a specialized component style (e.g., "AccentButton") -> **THEN** use `define_variant_style(variant_name, base_type, props)`. (Why: Keeps inspector clean and utilizes Godot's Theme Type Variations).
    - **IF** needing a runtime, instance-specific state change -> **THEN** use C# `AddTheme*Override()` AFTER calling `.Duplicate()`. (Why: Prevents accidental modification of the shared global `.tres` resource).
  </decision_tree>

  <end_to_end_example>
    <![CDATA[
    // 1. GDScript: Define the Theme (A1UIResources/ThemeGen/my_theme.gd)
    @tool
    extends ProgrammaticTheme

    const UPDATE_ON_SAVE = true
    const VERBOSITY = Verbosity.QUIET

    func setup():
        set_save_path("res://A1UIResources/ThemeGen/generated/my_theme.tres")

    func define_theme():
        define_default_font_size(16)
        define_style("Button", {
            normal = stylebox_flat({
                bg_color = Color.BLACK,
                corner_ = corner_radius(6), # expands to all 4 corners
                content_ = content_margins(10) # expands to all 4 margins
            }),
            font_color = Color.WHITE
        })
        
        define_variant_style("AccentButton", "Button", {
            normal = inherit(styles.Button.normal, { bg_color = Color.RED })
        })

    // 2. C#: Apply the Theme Globally or Locally
    private Theme _appTheme = GD.Load<Theme>("res://A1UIResources/ThemeGen/generated/my_theme.tres");

    public override void _Ready()
    {
        // Global
        GetTree().Root.Theme = _appTheme;
        
        // Local Variant Assignment
        Button myButton = GetNode<Button>("MyButton");
        myButton.ThemeTypeVariation = "AccentButton";
    }
    ]]>
  </end_to_end_example>

  <top_anti_patterns>
    <rule>
      <description>NEVER manually edit generated `.tres` files.</description>
      <rationale>ThemeGen overwrites `.tres` outputs automatically upon save. Manual edits will be permanently lost.</rationale>
    </rule>
    <rule>
      <description>NEVER modify shared C# theme resources directly without duplicating them first.</description>
      <rationale>Modifying a `StyleBox` from `GetThemeStylebox()` modifies the global resource, applying the change to ALL nodes sharing that style.</rationale>
      <example>
        # INCORRECT
        var stylebox = button.GetThemeStylebox("normal");
        stylebox.BgColor = Colors.Red; 
        
        # CORRECT
        var stylebox = button.GetThemeStylebox("normal").Duplicate() as StyleBoxFlat;
        stylebox.BgColor = Colors.Red;
        button.AddThemeStyleboxOverride("normal", stylebox);
      </example>
    </rule>
    <rule>
      <description>NEVER call `AddThemeOverride()` inside Godot's `_Notification(NOTIFICATION_THEME_CHANGED)`.</description>
      <rationale>Applying an override triggers a theme changed notification, creating an infinite recursive loop (Stack Overflow).</rationale>
    </rule>
  </top_anti_patterns>
</layer_1_quick_start>

<layer_2_detailed_guide>
  <api_reference>
    - **GDScript Core Methods:**
      - `set_save_path(path)`: String path for `.tres` output.
      - `define_default_font(resource)`: Sets project-wide default font.
      - `define_default_font_size(size)`: Sets integer base font size.
      - `set_theme_generator(function)`: Override standard generation for complex multi-variants.
      - `define_style(node_type, properties_dict)`: Base UI definition.
      - `define_variant_style(variant_name, base_type, properties_dict)`: Creates Godot Theme Type Variation.
    - **GDScript StyleBox Helpers:**
      - `stylebox_flat(props)`, `stylebox_line(props)`, `stylebox_empty(props)`, `stylebox_texture(props)`
      - `inherit(base, overrides...)`: Clones and overrides properties.
      - `merge(a, b, c...)`: Merges multiple property dictionaries.
    - **GDScript Margin/Radius Shortcuts:**
      - `border_width(all)` or `border_width(l, t, r, b)` mapped via `border_`
      - `corner_radius(all)` or `corner_radius(tl, tr, br, bl)` mapped via `corner_`
      - `expand_margins(all)` or `expand_margins(l, t, r, b)` mapped via `expand_`
      - `content_margins(all)` or `content_margins(l, t, r, b)` mapped via `content_`
      - `texture_margins(all)` or `texture_margins(l, t, r, b)` mapped via `texture_`
    - **C# Control Overrides:**
      - `AddThemeStyleboxOverride(name, styleBox)`
      - `AddThemeColorOverride(name, color)`
      - `AddThemeFontSizeOverride(name, size)`
      - `RemoveThemeStyleboxOverride(name)`
  </api_reference>

  <implementation_guide>
    1. **Initialize Theme Script:** Create a `.gd` file extending `ProgrammaticTheme` in `A1UIResources/ThemeGen/`. Enable `UPDATE_ON_SAVE = true`.
    2. **Define Setup/Palettes:** Implement `setup()` (or custom `setup_*()` for variants). Assign color constants to variables and call `set_save_path()`.
    3. **Build Base Styles:** Implement `define_theme()`. Use `define_style()` for base nodes like `Button`, `Label`, `PanelContainer`.
    4. **Generate Variants:** Use `define_variant_style()` for sub-types inheriting base configurations. Save the file to trigger auto-generation (or `Ctrl+Shift+X`).
    5. **Apply via C#:** Use `GD.Load<Theme>()` to load the `.tres` files in C# singletons or view components.
  </implementation_guide>

  <technical_specifications>
    - **Theme Resolution Priority (Highest to Lowest):**
      1. Node theme overrides (`AddTheme*Override`)
      2. Node's Theme property (Direct assignment)
      3. Parent node's Theme property (Inheritance)
      4. Project settings default theme
      5. Godot editor default theme
    - **Verbosity Levels:** `Verbosity.SILENT`, `Verbosity.QUIET`, `Verbosity.NORMAL`.
  </technical_specifications>

  <code_templates>
    <template name="Multi-Variant Theme Generator">
      <code><![CDATA[
      @tool
      extends ProgrammaticTheme

      const UPDATE_ON_SAVE = true
      var bg_color: Color
      var txt_color: Color

      func setup_light_theme():
          set_save_path("res://A1UIResources/ThemeGen/generated/light.tres")
          bg_color = Color.WHITE
          txt_color = Color.BLACK

      func setup_dark_theme():
          set_save_path("res://A1UIResources/ThemeGen/generated/dark.tres")
          bg_color = Color.BLACK
          txt_color = Color.WHITE

      func define_theme():
          define_style("PanelContainer", {
              panel = stylebox_flat({ bg_color = bg_color, content_ = content_margins(16) })
          })
          define_style("Label", { font_color = txt_color })
      ]]></code>
    </template>

    <template name="Shadow & Glow Design Patterns">
      <code><![CDATA[
      # Elevation effect with shadow
      var button_normal = stylebox_flat({
          bg_color = Color("#222222"),
          corner_ = corner_radius(6),
          content_ = content_margins(18, 10, 18, 10),
          shadow_color = Color(0, 0, 0, 0.4),
          shadow_size = 4,
          shadow_offset = Vector2(0, 2)
      })

      # Glow effect on focus using inheritance
      var lineedit_focus = inherit(styles.LineEdit.normal, {
          border_color = Color.CYAN,
          shadow_color = Color.CYAN.darkened(0.5),
          shadow_size = 4
      })
      ]]></code>
    </template>
    
    <template name="C# Theme Switcher Component">
      <code><![CDATA[
      using Godot;

      public partial class ThemeSwitcherComponentHelper : Node
      {
          [Export] public Theme LightTheme { get; set; }
          [Export] public Theme DarkTheme { get; set; }
          
          public void SwitchTheme(bool isDark)
          {
              GetTree().Root.Theme = isDark ? DarkTheme : LightTheme;
          }
      }
      ]]></code>
    </template>
  </code_templates>

  <core_rules>
    <rule>
      <description>ALWAYS define color palettes as variables in `setup_*()` functions.</description>
      <rationale>Hardcoding colors inside `define_theme()` breaks the multi-variant (light/dark) generation capability.</rationale>
    </rule>
    <rule>
      <description>ALWAYS use Godot Theme Type Variations (`define_variant_style`) instead of excessive custom C# wrapper classes for visual states.</description>
      <rationale>Native variants incur zero runtime overhead and cleanly integrate with the Godot Inspector.</rationale>
    </rule>
  </core_rules>
</layer_2_detailed_guide>

<layer_3_advanced>
  <troubleshooting>
    <error symptom="Theme definitions are not updating visually in the project.">
      <cause>Manual edits were made to the `.tres` file directly, or the script didn't regenerate.</cause>
      <fix>Discard `.tres` changes. Open the `.gd` theme script in Godot, ensure `const UPDATE_ON_SAVE = true`, save it, or press `Ctrl+Shift+X`.</fix>
    </error>
    <error symptom="Changing the color/style of one button at runtime changes all buttons of that type.">
      <cause>Modified a shared global `StyleBox` resource directly via `GetThemeStylebox()`.</cause>
      <fix>Append `.Duplicate()` to the `GetThemeStylebox()` call before modifying properties and applying it via `AddThemeStyleboxOverride()`.</fix>
    </error>
    <error symptom="Stack Overflow crash when theme is modified.">
      <cause>Theme overrides were applied inside `_Notification` during `NOTIFICATION_THEME_CHANGED`.</cause>
      <fix>Move override logic to `_Ready()`, state machines, or specific property setters outside the notification lifecycle.</fix>
    </error>
    <error symptom="Theme Type Variation ('VariantName') not found or not applying.">
      <cause>Typo in the variation name or case sensitivity mismatch.</cause>
      <fix>Verify exact string matches between GDScript `define_variant_style("Name", ...)` and C# `node.ThemeTypeVariation = "Name"`.</fix>
    </error>
    <error symptom="Styles correctly defined and generated but not visible in Godot Editor.">
      <cause>Editor cache stale.</cause>
      <fix>Close and reload the current scene, or restart the Godot editor entirely.</fix>
    </error>
  </troubleshooting>

  <best_practices>
    <rule>
      <description>ALWAYS follow the 90/10 Rule: 90% of UI styling MUST be in the ThemeGen `.gd` script. Only 10% (dynamic runtime states like HP bar colors) should exist as C# overrides.</description>
      <rationale>Theme switching is a highly optimized O(1) property assignment. Per-node `AddThemeOverride` scales linearly with node count, hurting performance.</rationale>
    </rule>
    <rule>
      <description>ALWAYS use `preload()` or exported `[Export] Theme` variables for theme resources if instant access without I/O stutter is required.</description>
      <rationale>`GD.Load` during runtime operations can cause frame drops. Preloading ensures the resource is in memory.</rationale>
    </rule>
  </best_practices>
</layer_3_advanced>