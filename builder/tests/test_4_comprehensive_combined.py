"""
Test 4: Comprehensive Combined Scene
Tests UI + StateChart integration with a complete interactive game entity
Creates a Boss Enemy with health bar UI and complex AI state machine
"""

import sys
sys.path.append("../..")

from builder.core import TscnBuilder
from builder.modules.ui import UIModule
from builder.modules.statechart import StateChartModule

print("=" * 60)
print("TEST 4: Comprehensive Combined Scene (UI + StateChart)")
print("=" * 60)

# Initialize scene - Boss enemy with UI overlay
scene = TscnBuilder(root_name="BossEnemy", root_type="CharacterBody3D")
scene.initialize_root()

# ============================================================
# PART 1: UI COMPONENTS (Health bar, name plate, phase indicator)
# ============================================================

# Add UI overlay as child of 3D entity
ui = UIModule(scene)

# Create a Control node for UI overlay
scene.add_node("UIOverlay", "Control", parent=".", 
              layout_mode=3, anchors_preset=15, 
              anchor_right=1.0, anchor_bottom=1.0,
              grow_horizontal=2, grow_vertical=2)

# Boss name plate at top
ui.add_margin_container("NamePlateMargin", parent="UIOverlay", top=20, left=20, right=20)
ui.add_panel_container("NamePlatePanel", parent="NamePlateMargin")
ui.add_margin_container("NamePlatePadding", parent="NamePlatePanel", uniform=15)
ui.add_vbox("NamePlateContent", parent="NamePlatePadding", separation=8)

ui.add_label("BossName", parent="NamePlateContent", 
            text="🔥 Ancient Dragon Lord 🔥", align="center", font_size=32)
ui.add_label("BossTitle", parent="NamePlateContent", 
            text="Guardian of the Eternal Flame", align="center", font_size=16)

ui.add_separator("NameSep", parent="NamePlateContent")

# Health bar
ui.add_hbox("HealthBarContainer", parent="NamePlateContent", separation=10)
ui.add_label("HealthIcon", parent="HealthBarContainer", text="❤️", font_size=24)
ui.add_vbox("HealthBarStack", parent="HealthBarContainer", separation=4)

ui.add_hbox("HealthBarRow", parent="HealthBarStack", separation=10)
ui.add_label("HealthLabel", parent="HealthBarRow", text="Health:", min_size=(80, 0))
ui.add_progress_bar("BossHealthBar", parent="HealthBarRow", value=100, 
                   size_flags_h=3, min_size=(0, 30), show_percentage=True)

ui.add_label("HealthValue", parent="HealthBarStack", 
            text="50,000 / 50,000 HP", align="right", font_size=14)

# Phase indicator
ui.add_separator("PhaseSep", parent="NamePlateContent")
ui.add_hbox("PhaseIndicator", parent="NamePlateContent", separation=10)
ui.add_label("PhaseLabel", parent="PhaseIndicator", text="Phase:", font_size=18)
ui.add_label("CurrentPhase", parent="PhaseIndicator", text="I", font_size=24)
ui.add_label("PhaseSlash", parent="PhaseIndicator", text="/", font_size=18)
ui.add_label("TotalPhases", parent="PhaseIndicator", text="III", font_size=18)

# Ability cooldowns at bottom
ui.add_margin_container("AbilityMargin", parent="UIOverlay", bottom=20, left=20, right=20)
ui.add_panel_container("AbilityPanel", parent="AbilityMargin")
ui.add_margin_container("AbilityPadding", parent="AbilityPanel", uniform=10)
ui.add_hbox("AbilityContainer", parent="AbilityPadding", separation=15)

# Create ability slots
abilities = [
    ("FireBreath", "🔥 Fire Breath", 85),
    ("TailSwipe", "💥 Tail Swipe", 60),
    ("WingGust", "🌪️ Wing Gust", 40),
    ("Roar", "📢 Roar", 100)
]

for ability_id, ability_name, cooldown_value in abilities:
    ui.add_vbox(f"{ability_id}Slot", parent="AbilityContainer", separation=5)
    ui.add_label(f"{ability_id}Name", parent=f"{ability_id}Slot", 
                text=ability_name, align="center", font_size=14)
    ui.add_progress_bar(f"{ability_id}Cooldown", parent=f"{ability_id}Slot", 
                       value=cooldown_value, min_size=(120, 20), show_percentage=False)
    ui.add_label(f"{ability_id}Status", parent=f"{ability_id}Slot", 
                text="Ready" if cooldown_value == 100 else "Cooling...", 
                align="center", font_size=11)

# ============================================================
# PART 2: STATECHART COMPONENTS (Complex AI behavior)
# ============================================================

sc = StateChartModule(scene, parent=".")
sc.add_statechart("StateChart")

# Root state with phase management
sc.add_compound_state("Root", parent="StateChart", initial_state="Phase1")

# ===== PHASE 1: Basic attacks =====
sc.add_compound_state("Phase1", parent="Root", initial_state="Idle")

sc.add_atomic_state("Idle", parent="Phase1")
sc.add_atomic_state("Circling", parent="Phase1")
sc.add_atomic_state("FireBreath", parent="Phase1")
sc.add_atomic_state("TailSwipe", parent="Phase1")

# Phase 1 transitions
sc.add_transition("StartCircling", from_state="Idle", to_state="Circling", 
                 event="player_in_range")
sc.add_transition("UseFireBreath", from_state="Circling", to_state="FireBreath", 
                 event="ability_ready", delay=0.5)
sc.add_transition("UseTailSwipe", from_state="Circling", to_state="TailSwipe", 
                 event="player_close")
sc.add_transition("BackToCircling1", from_state="FireBreath", to_state="Circling", 
                 event="ability_complete")
sc.add_transition("BackToCircling2", from_state="TailSwipe", to_state="Circling", 
                 event="ability_complete")

# ===== PHASE 2: Enhanced attacks + flight =====
sc.add_compound_state("Phase2", parent="Root", initial_state="Flying")

sc.add_atomic_state("Flying", parent="Phase2")
sc.add_atomic_state("DiveBomb", parent="Phase2")
sc.add_atomic_state("WingGust", parent="Phase2")
sc.add_atomic_state("AerialFireBreath", parent="Phase2")
sc.add_atomic_state("Landing", parent="Phase2")

# Phase 2 transitions
sc.add_transition("DoDiveBomb", from_state="Flying", to_state="DiveBomb", 
                 event="dive_attack")
sc.add_transition("DoWingGust", from_state="Flying", to_state="WingGust", 
                 event="wing_attack")
sc.add_transition("DoAerialFire", from_state="Flying", to_state="AerialFireBreath", 
                 event="fire_attack")
sc.add_transition("BackToFlying1", from_state="DiveBomb", to_state="Flying", 
                 event="attack_complete")
sc.add_transition("BackToFlying2", from_state="WingGust", to_state="Flying", 
                 event="attack_complete")
sc.add_transition("BackToFlying3", from_state="AerialFireBreath", to_state="Flying", 
                 event="attack_complete")
sc.add_transition("LandNow", from_state="Flying", to_state="Landing", 
                 event="phase_transition", delay=1.0)

# ===== PHASE 3: Enraged state with all abilities =====
sc.add_compound_state("Phase3", parent="Root", initial_state="Enraged")

sc.add_atomic_state("Enraged", parent="Phase3")
sc.add_atomic_state("MegaFireBreath", parent="Phase3")
sc.add_atomic_state("EarthquakeStomp", parent="Phase3")
sc.add_atomic_state("Roar", parent="Phase3")
sc.add_atomic_state("BerserkCombo", parent="Phase3")

# Phase 3 transitions
sc.add_transition("DoMegaFire", from_state="Enraged", to_state="MegaFireBreath", 
                 event="ultimate_ready")
sc.add_transition("DoEarthquake", from_state="Enraged", to_state="EarthquakeStomp", 
                 event="stomp_ready")
sc.add_transition("DoRoar", from_state="Enraged", to_state="Roar", 
                 event="roar_ready")
sc.add_transition("DoBerserk", from_state="Enraged", to_state="BerserkCombo", 
                 event="low_health")
sc.add_transition("BackToEnraged1", from_state="MegaFireBreath", to_state="Enraged", 
                 event="attack_complete")
sc.add_transition("BackToEnraged2", from_state="EarthquakeStomp", to_state="Enraged", 
                 event="attack_complete")
sc.add_transition("BackToEnraged3", from_state="Roar", to_state="Enraged", 
                 event="attack_complete")
sc.add_transition("BackToEnraged4", from_state="BerserkCombo", to_state="Enraged", 
                 event="combo_complete")

# ===== DEATH STATE =====
sc.add_atomic_state("Defeated", parent="Root")

# Phase transitions (now that all phases exist)
sc.add_transition("ToPhase2", from_state="Phase1", to_state="Phase2", 
                 event="health_below_66")
sc.add_transition("ToPhase3", from_state="Phase2", to_state="Phase3", 
                 event="health_below_33")

# Death transitions from any phase
sc.add_transition("Death1", from_state="Phase1", to_state="Defeated", event="health_zero")
sc.add_transition("Death2", from_state="Phase2", to_state="Defeated", event="health_zero")
sc.add_transition("Death3", from_state="Phase3", to_state="Defeated", event="health_zero")

# ===== PARALLEL STATE: Animation and VFX =====
sc.add_parallel_state("Effects", parent="Root")

# Animation state
sc.add_compound_state("Animation", parent="Effects", initial_state="IdleAnim")
sc.add_atomic_state("IdleAnim", parent="Animation")
sc.add_atomic_state("AttackAnim", parent="Animation")
sc.add_atomic_state("FlyAnim", parent="Animation")
sc.add_atomic_state("HurtAnim", parent="Animation")
sc.add_atomic_state("DeathAnim", parent="Animation")

# VFX state
sc.add_compound_state("VFX", parent="Effects", initial_state="NoVFX")
sc.add_atomic_state("NoVFX", parent="VFX")
sc.add_atomic_state("FireVFX", parent="VFX")
sc.add_atomic_state("WindVFX", parent="VFX")
sc.add_atomic_state("EnrageVFX", parent="VFX")

# Add guards for phase transitions
sc.add_expression_guard("HealthCheck66", parent="ToPhase2", 
                       expression="health_percent <= 66")
sc.add_expression_guard("HealthCheck33", parent="ToPhase3", 
                       expression="health_percent <= 33")
sc.add_expression_guard("BerserkCheck", parent="DoBerserk", 
                       expression="health_percent < 15")

# Resolve initial states
sc.resolve_initial_states()

# ============================================================
# PART 3: Add collision shape for 3D entity
# ============================================================

# Add collision shape as sub-resource
scene.add_sub_resource("CapsuleShape3D", "CapsuleShape3D_boss", 
                      radius=2.0, height=5.0)

# Add CollisionShape3D node
scene.add_node("CollisionShape", "CollisionShape3D", parent=".",
              shape='SubResource("CapsuleShape3D_boss")')

# Generate and save
print("\nGenerated Tree Structure:")
print(scene.generate_tree_view())
print("\n" + "=" * 60)

scene.save("c:/Godot/TetrisBackpack/Scenes/Test_Comprehensive_Combined.tscn")

print("✅ Test 4 Complete: Comprehensive combined scene generated successfully")
print("   - UI: Boss health bar, name plate, phase indicator, ability cooldowns")
print("   - StateChart: 3-phase AI with 15+ states, parallel animation/VFX")
print("   - 3D: CharacterBody3D with collision shape")
print("=" * 60)
