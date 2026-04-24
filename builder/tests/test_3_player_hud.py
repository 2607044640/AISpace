"""
Test 3: Creative Scene - Player HUD
Tests complex UI layout with health/stamina bars, minimap, hotbar, and status effects
"""

import sys
sys.path.append("../..")

from builder.core import TscnBuilder
from builder.modules.ui import UIModule

print("=" * 60)
print("TEST 3: Creative Scene - Player HUD")
print("=" * 60)

# Initialize scene
scene = TscnBuilder(root_name="PlayerHUD", root_type="Control")
ui = UIModule(scene)
ui.setup_fullscreen_control()

# Main HUD container
ui.add_margin_container("HUDMargin", parent=".", left=20, top=20, right=20, bottom=20)
ui.add_vbox("HUDLayout", parent="HUDMargin", separation=0)

# Top section: Health and Stamina
ui.add_hbox("TopSection", parent="HUDLayout", separation=20)

# Left side: Player stats
ui.add_vbox("PlayerStats", parent="TopSection", separation=8)
ui.add_panel_container("StatsPanel", parent="PlayerStats")
ui.add_margin_container("StatsPanelMargin", parent="StatsPanel", uniform=12)
ui.add_vbox("StatsContent", parent="StatsPanelMargin", separation=10)

# Player name and level
ui.add_label("PlayerName", parent="StatsContent", text="Warrior", font_size=20)
ui.add_label("PlayerLevel", parent="StatsContent", text="Level 42", font_size=14)

ui.add_separator("StatsSep1", parent="StatsContent")

# Health bar
ui.add_label("HealthLabel", parent="StatsContent", text="Health")
ui.add_progress_bar("HealthBar", parent="StatsContent", value=75, 
                   min_size=(250, 24), show_percentage=True)
ui.add_label("HealthValue", parent="StatsContent", text="750 / 1000", font_size=12)

# Stamina bar
ui.add_label("StaminaLabel", parent="StatsContent", text="Stamina")
ui.add_progress_bar("StaminaBar", parent="StatsContent", value=60, 
                   min_size=(250, 24), show_percentage=True)
ui.add_label("StaminaValue", parent="StatsContent", text="60 / 100", font_size=12)

# Mana bar
ui.add_label("ManaLabel", parent="StatsContent", text="Mana")
ui.add_progress_bar("ManaBar", parent="StatsContent", value=90, 
                   min_size=(250, 24), show_percentage=True)
ui.add_label("ManaValue", parent="StatsContent", text="450 / 500", font_size=12)

# Spacer
ui.add_color_rect("Spacer1", parent="TopSection", color=(0, 0, 0, 0))

# Right side: Minimap
ui.add_vbox("MinimapContainer", parent="TopSection", separation=5)
ui.add_label("MinimapTitle", parent="MinimapContainer", text="Minimap", align="center")
ui.add_panel_container("MinimapPanel", parent="MinimapContainer")
ui.add_color_rect("MinimapPlaceholder", parent="MinimapPanel", 
                 color=(0.2, 0.3, 0.2, 0.8))
ui.add_margin_container("MinimapMargin", parent="MinimapPlaceholder", uniform=5)
ui.add_label("MinimapText", parent="MinimapMargin", text="[Minimap]\n150x150", 
            align="center", min_size=(150, 150))

# Middle spacer (pushes content to top and bottom)
ui.add_color_rect("MiddleSpacer", parent="HUDLayout", color=(0, 0, 0, 0))

# Bottom section: Hotbar and status effects
ui.add_vbox("BottomSection", parent="HUDLayout", separation=15)

# Status effects
ui.add_hbox("StatusEffects", parent="BottomSection", separation=10)
ui.add_label("StatusLabel", parent="StatusEffects", text="Status:", min_size=(80, 0))

ui.add_panel_container("BuffPanel1", parent="StatusEffects")
ui.add_margin_container("BuffMargin1", parent="BuffPanel1", uniform=8)
ui.add_label("Buff1", parent="BuffMargin1", text="🛡️ Shield", align="center")

ui.add_panel_container("BuffPanel2", parent="StatusEffects")
ui.add_margin_container("BuffMargin2", parent="BuffPanel2", uniform=8)
ui.add_label("Buff2", parent="BuffMargin2", text="⚡ Haste", align="center")

ui.add_panel_container("DebuffPanel1", parent="StatusEffects")
ui.add_margin_container("DebuffMargin1", parent="DebuffPanel1", uniform=8)
ui.add_label("Debuff1", parent="DebuffMargin1", text="🔥 Burn", align="center")

# Hotbar
ui.add_panel_container("HotbarPanel", parent="BottomSection")
ui.add_margin_container("HotbarMargin", parent="HotbarPanel", uniform=10)
ui.add_vbox("HotbarContent", parent="HotbarMargin", separation=8)

ui.add_label("HotbarTitle", parent="HotbarContent", text="Hotbar", align="center", font_size=16)
ui.add_hbox("HotbarSlots", parent="HotbarContent", separation=8)

# Create 8 hotbar slots
for i in range(8):
    ui.add_panel_container(f"Slot{i}Panel", parent="HotbarSlots")
    ui.add_margin_container(f"Slot{i}Margin", parent=f"Slot{i}Panel", uniform=5)
    ui.add_vbox(f"Slot{i}Content", parent=f"Slot{i}Margin", separation=2)
    
    # Slot icon placeholder
    ui.add_color_rect(f"Slot{i}Icon", parent=f"Slot{i}Content", 
                     color=(0.3, 0.3, 0.4, 1))
    ui.add_label(f"Slot{i}IconText", parent=f"Slot{i}Icon", 
                text=f"[{i+1}]", align="center", min_size=(50, 50))
    
    # Slot keybind
    ui.add_label(f"Slot{i}Key", parent=f"Slot{i}Content", 
                text=str(i+1), align="center", font_size=12)

# Bottom info bar
ui.add_separator("BottomSep", parent="BottomSection")
ui.add_hbox("InfoBar", parent="BottomSection", separation=20)
ui.add_label("GoldLabel", parent="InfoBar", text="💰 Gold: 1,234", font_size=14)
ui.add_label("LocationLabel", parent="InfoBar", text="📍 Location: Dark Forest", font_size=14)
ui.add_label("QuestLabel", parent="InfoBar", text="📜 Quest: Defeat the Dragon (3/5)", font_size=14)

# Generate and save
print("\nGenerated Tree Structure:")
print(scene.generate_tree_view())
print("\n" + "=" * 60)

scene.save("c:/Godot/TetrisBackpack/Scenes/Test_PlayerHUD.tscn")

print("✅ Test 3 Complete: Player HUD scene generated successfully")
print("=" * 60)
