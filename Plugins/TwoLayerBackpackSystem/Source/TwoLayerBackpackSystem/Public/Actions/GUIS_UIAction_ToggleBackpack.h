// GUIS_UIAction_OpenBackpack.h
// UIAction for toggling Backpack - inherits from UGUIS_UIAction_ToggleUI

#pragma once

#include "CoreMinimal.h"
#include "Actions/GUIS_UIAction_ToggleUI.h"
#include "GUIS_UIAction_ToggleBackpack.generated.h"

/**
 * UIAction that toggles the Backpack inventory.
 * 
 * Inherits layer priority check and toggle logic from UGUIS_UIAction_ToggleUI.
 * Uses reflection to call OpenBackpackInventory() on BackpackInventoryComponent.
 */
UCLASS(Blueprintable, meta = (DisplayName = "Toggle Backpack Action"))
class TWOLAYERBACKPACKSYSTEM_API UGUIS_UIAction_ToggleBackpack : public UGUIS_UIAction_ToggleUI
{
	GENERATED_BODY()

public:
	UGUIS_UIAction_ToggleBackpack();

protected:
	// Call OpenBackpackInventory() on BackpackInventoryComponent via reflection
	virtual void InvokeActionInternal_Implementation(const UObject* Data, APlayerController* PlayerController) const override;
};
