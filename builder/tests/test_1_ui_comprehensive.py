"""
Test 1: Comprehensive UI Builder Test
Tests all container types, controls, layouts, and nesting capabilities
"""

import sys
sys.path.append("../..")

from builder.core import TscnBuilder
from builder.modules.ui import UIModule

print("=" * 60)
print("TEST 1: Comprehensive UI Builder")
print("=" * 60)

# Initialize scene
scene = TscnBuilder(root_name="UITestScene", root_type="Control")
ui = UIModule(scene)
ui.setup_fullscreen_control()

# Background
ui.add_color_rect("Background", parent=".", color=(0.1, 0.1, 0.15, 1), use_anchors=True)

# Main layout with margins
ui.add_margin_container("MainMargin", parent=".", uniform=30)
ui.add_vbox("MainVBox", parent="MainMargin", separation=20)

# Header section
ui.add_panel_container("HeaderPanel", parent="MainVBox")
ui.add_margin_container("HeaderMargin", parent="HeaderPanel", uniform=15)
ui.add_label("HeaderLabel", parent="HeaderMargin", text="UI Component Test Suite", 
             align="center", font_size=28)

# Test Section 1: Labels and Text
ui.add_label("Section1Title", parent="MainVBox", text="Section 1: Text Controls", font_size=20)
ui.add_hbox("LabelTestBox", parent="MainVBox", separation=10)
ui.add_label("LeftLabel", parent="LabelTestBox", text="Left Aligned", align="left", size_flags_h=3)
ui.add_label("CenterLabel", parent="LabelTestBox", text="Center Aligned", align="center", size_flags_h=3)
ui.add_label("RightLabel", parent="LabelTestBox", text="Right Aligned", align="right", size_flags_h=3)

ui.add_separator("Sep1", parent="MainVBox")

# Test Section 2: Progress Bars
ui.add_label("Section2Title", parent="MainVBox", text="Section 2: Progress Bars", font_size=20)
ui.add_vbox("ProgressBox", parent="MainVBox", separation=8)

ui.add_hbox("HealthBar", parent="ProgressBox", separation=10)
ui.add_label("HealthLabel", parent="HealthBar", text="Health:", min_size=(100, 0))
ui.add_progress_bar("HealthProgress", parent="HealthBar", value=85, size_flags_h=3)

ui.add_hbox("ManaBar", parent="ProgressBox", separation=10)
ui.add_label("ManaLabel", parent="ManaBar", text="Mana:", min_size=(100, 0))
ui.add_progress_bar("ManaProgress", parent="ManaBar", value=60, size_flags_h=3)

ui.add_hbox("StaminaBar", parent="ProgressBox", separation=10)
ui.add_label("StaminaLabel", parent="StaminaBar", text="Stamina:", min_size=(100, 0))
ui.add_progress_bar("StaminaProgress", parent="StaminaBar", value=40, size_flags_h=3)

ui.add_separator("Sep2", parent="MainVBox")

# Test Section 3: Buttons and Checkboxes
ui.add_label("Section3Title", parent="MainVBox", text="Section 3: Interactive Controls", font_size=20)
ui.add_hbox("ButtonBox", parent="MainVBox", separation=10)
ui.add_button("PrimaryButton", parent="ButtonBox", text="Primary Action", size_flags_h=3)
ui.add_button("SecondaryButton", parent="ButtonBox", text="Secondary Action", size_flags_h=3)
ui.add_button("DangerButton", parent="ButtonBox", text="Danger Action", size_flags_h=3)

ui.add_hbox("CheckboxBox", parent="MainVBox", separation=15)
ui.add_checkbox("EnableSound", parent="CheckboxBox", text="Enable Sound", button_pressed=True)
ui.add_checkbox("EnableMusic", parent="CheckboxBox", text="Enable Music", button_pressed=True)
ui.add_checkbox("EnableVibration", parent="CheckboxBox", text="Enable Vibration", button_pressed=False)

ui.add_separator("Sep3", parent="MainVBox")

# Test Section 4: Scroll Container
ui.add_label("Section4Title", parent="MainVBox", text="Section 4: Scroll Container", font_size=20)
ui.add_scroll_container("ScrollTest", parent="MainVBox", vertical_scroll=2)
ui.add_vbox("ScrollContent", parent="ScrollTest", separation=5)

for i in range(10):
    ui.add_label(f"ScrollItem{i}", parent="ScrollContent", text=f"Scrollable Item {i + 1}")

ui.add_separator("Sep4", parent="MainVBox")

# Test Section 5: Nested Containers
ui.add_label("Section5Title", parent="MainVBox", text="Section 5: Nested Layouts", font_size=20)
ui.add_hbox("NestedBox", parent="MainVBox", separation=10)

# Left column
ui.add_vbox("LeftColumn", parent="NestedBox", separation=5)
ui.add_panel_container("LeftPanel1", parent="LeftColumn")
ui.add_margin_container("LeftPanelMargin1", parent="LeftPanel1", uniform=10)
ui.add_label("LeftPanelLabel1", parent="LeftPanelMargin1", text="Left Panel 1", align="center")

ui.add_panel_container("LeftPanel2", parent="LeftColumn")
ui.add_margin_container("LeftPanelMargin2", parent="LeftPanel2", uniform=10)
ui.add_label("LeftPanelLabel2", parent="LeftPanelMargin2", text="Left Panel 2", align="center")

# Right column
ui.add_vbox("RightColumn", parent="NestedBox", separation=5)
ui.add_panel_container("RightPanel1", parent="RightColumn")
ui.add_margin_container("RightPanelMargin1", parent="RightPanel1", uniform=10)
ui.add_label("RightPanelLabel1", parent="RightPanelMargin1", text="Right Panel 1", align="center")

ui.add_panel_container("RightPanel2", parent="RightColumn")
ui.add_margin_container("RightPanelMargin2", parent="RightPanel2", uniform=10)
ui.add_label("RightPanelLabel2", parent="RightPanelMargin2", text="Right Panel 2", align="center")

# Footer
ui.add_separator("FooterSep", parent="MainVBox")
ui.add_label("FooterLabel", parent="MainVBox", text="Test Complete - All UI Components Rendered", 
             align="center", font_size=16)

# Generate and save
print("\nGenerated Tree Structure:")
print(scene.generate_tree_view())
print("\n" + "=" * 60)

scene.save("c:/Godot/3d-practice/Scenes/Test_UI_Comprehensive.tscn")

print("✅ Test 1 Complete: UI scene generated successfully")
print("=" * 60)
