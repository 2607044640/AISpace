"""
Test 2: Comprehensive StateChart Test
Tests compound states, atomic states, parallel states, transitions, and guards
"""

import sys
sys.path.append("../..")

from builder.core import TscnBuilder
from builder.modules.statechart import StateChartModule

print("=" * 60)
print("TEST 2: Comprehensive StateChart Builder")
print("=" * 60)

# Initialize scene
scene = TscnBuilder(root_name="EnemyAI", root_type="CharacterBody3D")
scene.initialize_root()

# Attach StateChart
sc = StateChartModule(scene, parent=".")
sc.add_statechart("StateChart")

# Root compound state
sc.add_compound_state("Root", parent="StateChart", initial_state="Patrol")

# Main behavior states
sc.add_compound_state("Patrol", parent="Root", initial_state="Walking")
sc.add_atomic_state("Walking", parent="Patrol")
sc.add_atomic_state("Investigating", parent="Patrol")

sc.add_compound_state("Combat", parent="Root", initial_state="Attacking")
sc.add_atomic_state("Attacking", parent="Combat")
sc.add_atomic_state("Defending", parent="Combat")
sc.add_atomic_state("Retreating", parent="Combat")

sc.add_atomic_state("Dead", parent="Root")

# Patrol transitions
sc.add_transition("ToInvestigating", from_state="Walking", to_state="Investigating", 
                 event="noise_detected", delay=0.5)
sc.add_transition("BackToWalking", from_state="Investigating", to_state="Walking", 
                 event="investigation_complete", delay=1.0)

# Combat entry transitions
sc.add_transition("ToCombat", from_state="Patrol", to_state="Combat", 
                 event="player_spotted")

# Combat internal transitions
sc.add_transition("ToDefending", from_state="Attacking", to_state="Defending", 
                 event="heavy_damage_taken")
sc.add_transition("BackToAttacking", from_state="Defending", to_state="Attacking", 
                 event="defense_complete")
sc.add_transition("ToRetreating", from_state="Attacking", to_state="Retreating", 
                 event="low_health")
sc.add_transition("ToRetreating2", from_state="Defending", to_state="Retreating", 
                 event="low_health")

# Combat exit transition
sc.add_transition("BackToPatrol", from_state="Combat", to_state="Patrol", 
                 event="player_lost")

# Death transitions (from any state)
sc.add_transition("ToDeath1", from_state="Patrol", to_state="Dead", event="killed")
sc.add_transition("ToDeath2", from_state="Combat", to_state="Dead", event="killed")

# Add guards to some transitions
sc.add_expression_guard("HealthCheck", parent="ToRetreating", 
                       expression="health < 30")
sc.add_expression_guard("DistanceCheck", parent="ToCombat", 
                       expression="distance_to_player < 10")

# Add parallel state for animations/audio
sc.add_parallel_state("Effects", parent="Root")
sc.add_compound_state("Animation", parent="Effects", initial_state="IdleAnim")
sc.add_atomic_state("IdleAnim", parent="Animation")
sc.add_atomic_state("WalkAnim", parent="Animation")
sc.add_atomic_state("AttackAnim", parent="Animation")

sc.add_compound_state("Audio", parent="Effects", initial_state="Silence")
sc.add_atomic_state("Silence", parent="Audio")
sc.add_atomic_state("Footsteps", parent="Audio")
sc.add_atomic_state("CombatSounds", parent="Audio")

# Animation transitions
sc.add_transition("ToWalkAnim", from_state="IdleAnim", to_state="WalkAnim", event="start_walking")
sc.add_transition("ToIdleAnim", from_state="WalkAnim", to_state="IdleAnim", event="stop_walking")
sc.add_transition("ToAttackAnim", from_state="IdleAnim", to_state="AttackAnim", event="attack")
sc.add_transition("ToAttackAnim2", from_state="WalkAnim", to_state="AttackAnim", event="attack")

# Audio transitions
sc.add_transition("ToFootsteps", from_state="Silence", to_state="Footsteps", event="start_walking")
sc.add_transition("ToSilence", from_state="Footsteps", to_state="Silence", event="stop_walking")
sc.add_transition("ToCombatSounds", from_state="Silence", to_state="CombatSounds", event="enter_combat")
sc.add_transition("ToCombatSounds2", from_state="Footsteps", to_state="CombatSounds", event="enter_combat")

# Resolve initial states
sc.resolve_initial_states()

# Generate and save
print("\nGenerated Tree Structure:")
print(scene.generate_tree_view())
print("\n" + "=" * 60)

scene.save("c:/Godot/3d-practice/Scenes/Test_StateChart_Comprehensive.tscn")

print("✅ Test 2 Complete: StateChart scene generated successfully")
print("=" * 60)
