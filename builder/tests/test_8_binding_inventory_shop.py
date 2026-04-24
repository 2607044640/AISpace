"""
Test 8: C# Export Binding - Inventory Shop System
Tests dynamic slot generation with batch binding for inventory/shop UI
"""

import sys
sys.path.append("../..")

from builder.core import TscnBuilder
from builder.modules.ui import UIModule

print("=" * 60)
print("TEST 8: C# Export Binding - Inventory Shop System")
print("=" * 60)

# Initialize scene
scene = TscnBuilder(root_name="ShopUI", root_type="Control")
ui = UIModule(scene)
ui.setup_fullscreen_control()

# Background
ui.add_color_rect("Background", parent=".", color=(0.05, 0.05, 0.08, 1), use_anchors=True)

# Main layout
ui.add_margin_container("MainMargin", parent=".", uniform=30)
ui.add_hbox("MainHBox", parent="MainMargin", separation=30)

# ============================================================
# LEFT SIDE: Shop Inventory
# ============================================================

ui.add_vbox("ShopSection", parent="MainHBox", separation=15)
ui.add_label("ShopTitle", parent="ShopSection", text="🏪 Shop Inventory", 
            align="center", font_size=28)
ui.add_separator("ShopSep", parent="ShopSection")

# Shop info
ui.add_hbox("ShopInfoRow", parent="ShopSection", separation=10)
ui.add_label("ShopGoldLabel", parent="ShopInfoRow", text="💰 Your Gold:", font_size=16)
ui.add_label("ShopGoldValue", parent="ShopInfoRow", text="1,234", font_size=16, size_flags_h=3)

ui.add_separator("ShopInfoSep", parent="ShopSection")

# Shop grid container
ui.add_scroll_container("ShopScrollContainer", parent="ShopSection", vertical_scroll=2)
ui.add_vbox("ShopGrid", parent="ShopScrollContainer", separation=8)

# Generate 12 shop item slots dynamically
print("\n📝 Generating 12 shop item slots...")
shop_items = [
    ("Health Potion", "50"),
    ("Mana Potion", "40"),
    ("Sword", "500"),
    ("Shield", "300"),
    ("Armor", "800"),
    ("Helmet", "200"),
    ("Boots", "150"),
    ("Ring", "600"),
    ("Amulet", "700"),
    ("Scroll", "100"),
    ("Key", "250"),
    ("Map", "80")
]

for i, (item_name, price) in enumerate(shop_items):
    ui.add_panel_container(f"ShopSlot{i}Panel", parent="ShopGrid")
    ui.add_margin_container(f"ShopSlot{i}Margin", parent=f"ShopSlot{i}Panel", uniform=10)
    ui.add_hbox(f"ShopSlot{i}Content", parent=f"ShopSlot{i}Margin", separation=10)
    
    # Item icon placeholder
    ui.add_color_rect(f"ShopSlot{i}Icon", parent=f"ShopSlot{i}Content", 
                     color=(0.3, 0.3, 0.4, 1))
    ui.add_label(f"ShopSlot{i}IconText", parent=f"ShopSlot{i}Icon", 
                text=f"[{i+1}]", align="center", min_size=(50, 50))
    
    # Item info
    ui.add_vbox(f"ShopSlot{i}Info", parent=f"ShopSlot{i}Content", separation=5)
    ui.add_label(f"ShopSlot{i}Name", parent=f"ShopSlot{i}Info", 
                text=item_name, font_size=14)
    ui.add_label(f"ShopSlot{i}Price", parent=f"ShopSlot{i}Info", 
                text=f"💰 {price}g", font_size=12)
    
    # Buy button
    ui.add_button(f"ShopSlot{i}BuyButton", parent=f"ShopSlot{i}Content", 
                 text="Buy", size_flags_h=0)

# ============================================================
# RIGHT SIDE: Player Inventory
# ============================================================

ui.add_vbox("InventorySection", parent="MainHBox", separation=15)
ui.add_label("InventoryTitle", parent="InventorySection", text="🎒 Your Inventory", 
            align="center", font_size=28)
ui.add_separator("InventorySep", parent="InventorySection")

# Inventory info
ui.add_hbox("InventoryInfoRow", parent="InventorySection", separation=10)
ui.add_label("InventoryCapacityLabel", parent="InventoryInfoRow", text="Capacity:", font_size=16)
ui.add_label("InventoryCapacityValue", parent="InventoryInfoRow", text="8 / 20", 
            font_size=16, size_flags_h=3)

ui.add_separator("InventoryInfoSep", parent="InventorySection")

# Inventory grid container
ui.add_scroll_container("InventoryScrollContainer", parent="InventorySection", vertical_scroll=2)
ui.add_vbox("InventoryGrid", parent="InventoryScrollContainer", separation=8)

# Generate 20 inventory slots dynamically
print("📝 Generating 20 inventory slots...")
for i in range(20):
    ui.add_panel_container(f"InvSlot{i}Panel", parent="InventoryGrid")
    ui.add_margin_container(f"InvSlot{i}Margin", parent=f"InvSlot{i}Panel", uniform=10)
    ui.add_hbox(f"InvSlot{i}Content", parent=f"InvSlot{i}Margin", separation=10)
    
    # Slot icon placeholder
    ui.add_color_rect(f"InvSlot{i}Icon", parent=f"InvSlot{i}Content", 
                     color=(0.2, 0.2, 0.3, 1))
    ui.add_label(f"InvSlot{i}IconText", parent=f"InvSlot{i}Icon", 
                text=f"[{i+1}]", align="center", min_size=(50, 50))
    
    # Slot info
    ui.add_vbox(f"InvSlot{i}Info", parent=f"InvSlot{i}Content", separation=5)
    ui.add_label(f"InvSlot{i}Name", parent=f"InvSlot{i}Info", 
                text="Empty", font_size=14)
    ui.add_label(f"InvSlot{i}Quantity", parent=f"InvSlot{i}Info", 
                text="", font_size=12)
    
    # Use/Drop buttons
    ui.add_vbox(f"InvSlot{i}Buttons", parent=f"InvSlot{i}Content", separation=5)
    ui.add_button(f"InvSlot{i}UseButton", parent=f"InvSlot{i}Buttons", 
                 text="Use", size_flags_h=0)
    ui.add_button(f"InvSlot{i}DropButton", parent=f"InvSlot{i}Buttons", 
                 text="Drop", size_flags_h=0)

# ============================================================
# BOTTOM: Action buttons
# ============================================================

ui.add_separator("BottomSep", parent="MainMargin")
ui.add_hbox("BottomButtons", parent="MainMargin", separation=15)
ui.add_button("SortButton", parent="BottomButtons", text="Sort Inventory", size_flags_h=3)
ui.add_button("SellAllButton", parent="BottomButtons", text="Sell All Junk", size_flags_h=3)
ui.add_button("CloseButton", parent="BottomButtons", text="Close Shop", size_flags_h=3)

# ============================================================
# Add C# Controllers
# ============================================================

print("\n📝 Adding ShopController component...")
shop_controller_res_id = scene.add_ext_resource("Script",
                                               "res://B1Scripts/UI/ShopController.cs",
                                               "uid://shop_controller")
scene.add_node("ShopController", "Node", parent=".",
              script=f'ExtResource("{shop_controller_res_id}")')

print("📝 Adding InventoryController component...")
inv_controller_res_id = scene.add_ext_resource("Script",
                                              "res://B1Scripts/UI/InventoryController.cs",
                                              "uid://inventory_controller")
scene.add_node("InventoryController", "Node", parent=".",
              script=f'ExtResource("{inv_controller_res_id}")')

# ============================================================
# Bind Shop UI to ShopController
# ============================================================

print("\n🔗 Binding shop UI to ShopController...")

# Build shop slot bindings dynamically
shop_bindings = {
    "ShopGoldValue": "ShopGoldValue"
}

for i in range(12):
    shop_bindings[f"ShopSlot{i}Name"] = f"ShopSlot{i}Name"
    shop_bindings[f"ShopSlot{i}Price"] = f"ShopSlot{i}Price"
    shop_bindings[f"ShopSlot{i}BuyButton"] = f"ShopSlot{i}BuyButton"

scene.assign_multiple_node_paths("ShopController", shop_bindings)
print(f"✅ {len(shop_bindings)} shop elements bound to ShopController")

# ============================================================
# Bind Inventory UI to InventoryController
# ============================================================

print("🔗 Binding inventory UI to InventoryController...")

# Build inventory slot bindings dynamically
inv_bindings = {
    "InventoryCapacityValue": "InventoryCapacityValue",
    "SortButton": "SortButton",
    "SellAllButton": "SellAllButton",
    "CloseButton": "CloseButton"
}

for i in range(20):
    inv_bindings[f"InvSlot{i}Name"] = f"InvSlot{i}Name"
    inv_bindings[f"InvSlot{i}Quantity"] = f"InvSlot{i}Quantity"
    inv_bindings[f"InvSlot{i}UseButton"] = f"InvSlot{i}UseButton"
    inv_bindings[f"InvSlot{i}DropButton"] = f"InvSlot{i}DropButton"

scene.assign_multiple_node_paths("InventoryController", inv_bindings)
print(f"✅ {len(inv_bindings)} inventory elements bound to InventoryController")

# Verify bindings
print("\n📋 Verifying NodePath assignments:")
shop_ctrl = scene.get_node("ShopController")
inv_ctrl = scene.get_node("InventoryController")

if "ShopSlot0BuyButton" in shop_ctrl.properties:
    print(f"  ✅ ShopController.ShopSlot0BuyButton = {shop_ctrl.properties['ShopSlot0BuyButton']}")
if "InvSlot0UseButton" in inv_ctrl.properties:
    print(f"  ✅ InventoryController.InvSlot0UseButton = {inv_ctrl.properties['InvSlot0UseButton']}")

# Generate and save
print("\nGenerated Tree Structure (first 50 lines):")
tree_lines = scene.generate_tree_view().split('\n')
print('\n'.join(tree_lines[:50]))
print("... (truncated)")
print("\n" + "=" * 60)

scene.save("c:/Godot/TetrisBackpack/Scenes/Test_Binding_Inventory_Shop.tscn")

print("\n✅ Test 8 Complete: Inventory Shop binding scene generated")
print("   - 12 shop item slots with buy buttons")
print("   - 20 inventory slots with use/drop buttons")
print("   - 2 controllers: ShopController (37 bindings), InventoryController (84 bindings)")
print("   - Demonstrates dynamic slot generation with batch binding")
print("=" * 60)
