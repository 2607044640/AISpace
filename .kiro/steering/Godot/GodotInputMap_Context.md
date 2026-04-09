---
inclusion: manual
---
# Godot Input Map Configuration Rules

<instructions>
## Editor Configuration Workflow

**Add and Bind Inputs:**
1. Navigate to `Project > Project Settings > Input Map`.
2. Type the action name (e.g., `jump`) and click `Add`.
3. Click the `+` button next to the action to bind physical inputs:
   - Keyboard: Select `Key`, press the target key.
   - Mouse: Select `Mouse Button`, specify the button.
   - Gamepad: Select `Joypad Buttons` or `Joypad Axes`.

**Adjust and Maintain:**
- Modify Deadzone: Expand the action and change the value directly (default 0.5).
- Delete Input: Click the trash can icon next to the specific input.

**Restart Rules:**
- **No restart needed**: Adding/modifying actions or adjusting deadzones within the editor.
- **Rerun game (F5)**: Apply and test new input mappings.
- **Restart editor**: Only after manually editing the external `project.godot` file.
</instructions>

<reference>
## Gamepad Button & Axis Mapping Reference

**Xbox / PlayStation Standard Mapping:**
| Index | Xbox | PlayStation | Common Convention |
|---|---|---|---|
| 0 | A | Cross (×) | Jump / Confirm |
| 1 | B | Circle (○) | Cancel / Interact |
| 2 | X | Square (□) | Reload / Use |
| 3 | Y | Triangle (△) | Toggle View |
| 4/5 | LB/RB | L1/R1 | Skill 1 / 2 |
| 6/7 | LT/RT | L2/R2 | Aim / Attack |
| 8/9 | Back/Start | Share/Options | Map / Menu |
| 10/11| L3/R3 | L3/R3 | Sprint / Lock-on |

**Joystick Axis Mapping:**
| Axis | Control Target | Value Range (axis_value) |
|---|---|---|
| 0 / 1 | Left Stick X / Y | -1.0 (Left/Up) to 1.0 (Right/Down) |
| 2 / 3 | Right Stick X / Y | -1.0 (Left/Up) to 1.0 (Right/Down) |

**Configuration Storage:**
Input Map data is serialized under the `[input]` node in the `project.godot` file. Ensure this file is committed to version control.
</reference>

<examples>
## Core Input Pattern Examples

<example>
<description>Polling Key States (State Detection)</description>
<code>
// Hold detection (continuous)
if (Input.IsActionPressed("jump")) { /* Execute hold logic */ }

// Just pressed (triggers once)
if (Input.IsActionJustPressed("jump")) { velocity.Y = JumpVelocity; }

// Just released
if (Input.IsActionJustReleased("jump")) { /* Execute interrupt or end logic */ }
</code>
</example>

<example>
<description>Getting Axis and Strength Input</description>
<code>
// Single axis input (returns -1.0 to 1.0)
float horizontal = Input.GetAxis("move_left", "move_right");

// Analog stick strength (returns 0.0 to 1.0)
float strength = Input.GetActionStrength("accelerate");

// Combine two axes into a normalized Vector2
Vector2 inputDir = Input.GetVector("move_left", "move_right", "move_forward", "move_backward");
</code>
</example>

<example>
<description>Standard 3D Character Movement</description>
<code>
public override void _PhysicsProcess(double delta)
{
    Vector2 inputDir = Input.GetVector("move_left", "move_right", "move_forward", "move_backward");
    Vector3 direction = (Transform.Basis * new Vector3(inputDir.X, 0, inputDir.Y)).Normalized();
    
    if (direction != Vector3.Zero)
    {
        velocity.X = direction.X * Speed;
        velocity.Z = direction.Z * Speed;
    }
    
    if (Input.IsActionJustPressed("jump") && IsOnFloor())
    {
        velocity.Y = JumpVelocity;
    }
    
    MoveAndSlide();
}
</code>
</example>
</examples>

<troubleshooting>
## Troubleshooting

- **Unresponsive Input**: Verify exact string matches between code and the Input Map action names (case-sensitive).
- **Gamepad Not Recognized**: Connect the gamepad before launching the game. Check the Input device Index (`-1` = all devices, `0` = first device).
- **Stick Drift**: Expand the target action in the Input Map and increase the `deadzone` value (e.g., from 0.2 to 0.3).
- **Input Lag or Physics Jitter**: Always process movement-related Input logic inside `_PhysicsProcess()`. Never process physics inputs in `_Process()`.
</troubleshooting>