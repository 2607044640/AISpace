// BackpackWidget.h
// Base widget for backpack UI, inherits from UGUIS_ActivatableWidget
// Automatically handles input mode switching and game pause

#pragma once

#include "CoreMinimal.h"
#include "Widgets/GameActivatableWidgetExtension.h"
#include "BackpackWidget.generated.h"

/**
 * Base widget for backpack/inventory UI.
 * 
 * Features:
 * - Inherits from UGUIS_ActivatableWidget for CommonUI integration
 * - Automatically switches to Menu input mode when activated
 * - Pauses game (TimeDilation = 0) when activated
 * - Resumes game when deactivated
 * 
 * Usage:
 * 1. Create a Blueprint widget inheriting from this class
 * 2. Design your backpack UI in the Blueprint
 * 3. Use UGUIS_GameUIFunctionLibrary::PushContentToUILayer_ForPlayer() to show
 * 4. Use UGUIS_GameUIFunctionLibrary::PopContentFromUILayer() to hide
 */
UCLASS(Abstract, Blueprintable)
class TWOLAYERBACKPACKSYSTEM_API UBackpackWidget : public UGameActivatableWidgetExtension
{
	GENERATED_BODY()

public:
	UBackpackWidget(const FObjectInitializer& ObjectInitializer);

protected:
	// Note: Pause functionality is now handled by UGameActivatableWidgetExtension
	// via UIStateSubsystem with reference counting
};
