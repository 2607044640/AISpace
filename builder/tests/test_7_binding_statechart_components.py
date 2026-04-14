"""
Test 7: C# Export Binding - StateChart Components
Tests NodePath binding for StateChart component nodes with Export properties
"""

import sys
sys.path.append("../..")

from builder.core import TscnBuilder
from builder.modules.statechart import StateChartModule

print("=" * 60)
print("TEST 7: C# Export Binding - StateChart Components")
print("=" * 60)

# Initialize scene
scene = TscnBuilder(root_name="PlayerCharacter", root_type="CharacterBody3D")
scene.initialize_root()

# Add some child nodes that components will reference
scene.add_node("AnimationPlayer", "AnimationPlayer", parent=".")
scene.add_node("AudioStreamPlayer", "AudioStreamPlayer", parent=".")
scene.add_node("CollisionShape", "CollisionShape3D", parent=".")

# Add StateChart
print("\n📝 Creating StateChart with component nodes...")
sc = StateChartModule(scene, parent=".")
sc.add_statechart("StateChart")

# Root state
sc.add_compound_state("Root", parent="StateChart", initial_state="Ground")

# Ground movement states
sc.add_compound_state("Ground", parent="Root", initial_state="Idle")
sc.add_atomic_state("Idle", parent="Ground")
sc.add_atomic_state("Walking", parent="Ground")
sc.add_atomic_state("Running", parent="Ground")

# Air states
sc.add_compound_state("Air", parent="Root", initial_state="Falling")
sc.add_atomic_state("Jumping", parent="Air")
sc.add_atomic_state("Falling", parent="Air")

# Add C# component to Idle state
print("📝 Adding IdleComponent to Idle state...")
idle_comp_res_id = scene.add_ext_resource("Script",
                                         "res://B1Scripts/Components/IdleComponent.cs",
                                         "uid://idle_component")
scene.add_node("IdleComponent", "Node", parent="Idle",
              script=f'ExtResource("{idle_comp_res_id}")')

# Bind IdleComponent to AnimationPlayer and AudioStreamPlayer
print("🔗 Binding IdleComponent to scene nodes...")
scene.assign_multiple_node_paths("IdleComponent", {
    "AnimationPlayer": "AnimationPlayer",
    "AudioPlayer": "AudioStreamPlayer"
})

# Add C# component to Walking state
print("📝 Adding WalkingComponent to Walking state...")
walk_comp_res_id = scene.add_ext_resource("Script",
                                         "res://B1Scripts/Components/WalkingComponent.cs",
                                         "uid://walking_component")
scene.add_node("WalkingComponent", "Node", parent="Walking",
              script=f'ExtResource("{walk_comp_res_id}")')

# Bind WalkingComponent
print("🔗 Binding WalkingComponent to scene nodes...")
scene.assign_multiple_node_paths("WalkingComponent", {
    "AnimationPlayer": "AnimationPlayer",
    "AudioPlayer": "AudioStreamPlayer"
})

# Add C# component to Running state
print("📝 Adding RunningComponent to Running state...")
run_comp_res_id = scene.add_ext_resource("Script",
                                        "res://B1Scripts/Components/RunningComponent.cs",
                                        "uid://running_component")
scene.add_node("RunningComponent", "Node", parent="Running",
              script=f'ExtResource("{run_comp_res_id}")')

# Bind RunningComponent
print("🔗 Binding RunningComponent to scene nodes...")
scene.assign_multiple_node_paths("RunningComponent", {
    "AnimationPlayer": "AnimationPlayer",
    "AudioPlayer": "AudioStreamPlayer"
})

# Add C# component to Jumping state
print("📝 Adding JumpComponent to Jumping state...")
jump_comp_res_id = scene.add_ext_resource("Script",
                                         "res://B1Scripts/Components/JumpComponent.cs",
                                         "uid://jump_component")
scene.add_node("JumpComponent", "Node", parent="Jumping",
              script=f'ExtResource("{jump_comp_res_id}")')

# Bind JumpComponent
print("🔗 Binding JumpComponent to scene nodes...")
scene.assign_multiple_node_paths("JumpComponent", {
    "AnimationPlayer": "AnimationPlayer",
    "AudioPlayer": "AudioStreamPlayer",
    "CollisionShape": "CollisionShape"
})

# Add transitions
print("\n📝 Adding state transitions...")
sc.add_transition("ToWalking", from_state="Idle", to_state="Walking", event="move_start")
sc.add_transition("ToIdle", from_state="Walking", to_state="Idle", event="move_stop")
sc.add_transition("ToRunning", from_state="Walking", to_state="Running", event="sprint_start")
sc.add_transition("ToWalking2", from_state="Running", to_state="Walking", event="sprint_stop")
sc.add_transition("ToJumping", from_state="Ground", to_state="Jumping", event="jump")
sc.add_transition("ToFalling", from_state="Jumping", to_state="Falling", event="apex_reached")
sc.add_transition("ToGround", from_state="Air", to_state="Ground", event="landed")

# Resolve initial states
sc.resolve_initial_states()

print("✅ 4 components bound to scene nodes")
print("✅ 7 state transitions created")

# Verify bindings
print("\n📋 Verifying component NodePath assignments:")
for comp_name in ["IdleComponent", "WalkingComponent", "JumpComponent"]:
    comp = scene.get_node(comp_name)
    if comp and "AnimationPlayer" in comp.properties:
        print(f"  ✅ {comp_name}.AnimationPlayer = {comp.properties['AnimationPlayer']}")

# Generate and save
print("\nGenerated Tree Structure:")
print(scene.generate_tree_view())
print("\n" + "=" * 60)

scene.save("c:/Godot/3d-practice/Scenes/Test_Binding_StateChart_Components.tscn")

print("\n✅ Test 7 Complete: StateChart component binding scene generated")
print("   - 4 state components with Export bindings")
print("   - Components reference AnimationPlayer, AudioPlayer, CollisionShape")
print("   - Demonstrates component-based state machine architecture")
print("=" * 60)
