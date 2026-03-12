/**
 * Global Asset Paths and Values
 *
 * Centralized location for all hardcoded asset paths in the project.
 * This prevents path duplication and makes asset refactoring easier.
 *
 * Usage:
 *   TSoftObjectPtr<UDataTable> MyTable(FSoftObjectPath(GlobalPaths::KeyDataTable));
 *   
 *   Incorrect path-> TEXT("/Script/UMGEditor.WidgetBlueprint'/Game/A1Blueprint/UMG/Backpack/WBP_ItemSlotWidget.WBP_ItemSlotWidget'");
 *   Correct path-> TEXT("/Game/A1Blueprint/UMG/Backpack/WBP_ItemSlotWidget.WBP_ItemSlotWidget_C");
 *
 *   Incorrect path-> TEXT("/Script/Engine.DataTable'/Game/A1Other/DataTable/DT_Input.DT_Input'");
 *   Correct path-> TEXT("/Game/A1Other/DataTable/DT_Input.DT_Input");
 */

#pragma once

namespace GlobalPaths
{
	// UMG Widgets(TwoLayerBackpackSystem plugin)
	//inline const FString WBP_InventoryWidget = TEXT("/Game/A1TwoLayerBackpackPlugin/Blueprints/UMG/WBP_InventoryWidget.WBP_InventoryWidget_C");
	
}

namespace GlobalValues
{
	// Grid constants
	inline constexpr float GRID_SLOT_SIZE = 64.0f;
	inline constexpr int32 DEFAULT_GRID_WIDTH = 9;
	inline constexpr int32 DEFAULT_GRID_HEIGHT = 6;

	// Drag-drop position offset (for Selected Viewport mode correction)
	// Negative Y = shift upwards
	inline constexpr float DRAG_DROP_Y_OFFSET = -30.0f;
}

// Deprecated - use GlobalPaths namespace instead
inline const FString YourClass_StaticPath = TEXT("");