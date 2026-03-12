// GUIS_UIAction_ToggleUI.h
// Abstract base class for UIActions that toggle UI widgets (open/close)

#pragma once

#include "CoreMinimal.h"
#include "UI/Actions/GUIS_UIAction.h"
#include "GameplayTagContainer.h"
#include "GUIS_UIAction_ToggleUI.generated.h"

/**
 * Abstract base class for UIActions that toggle UI widgets.
 * 
 * Toggle logic:
 * - If current widget matches TargetWidgetClassNameContains: CLOSE it
 * - Otherwise: OPEN the target widget (subclass implements)
 * 
 * Provides common logic for:
 * - Compatibility check (GameActivatableWidgetExtension)
 * - Layer priority check (via TargetLayerTag)
 * - Auto close detection (via TargetWidgetClassNameContains)
 * 
 * Subclasses must:
 * 1. Call Super::InvokeActionInternal_Implementation first
 * 2. Check bHandledAsClose - if true, return immediately
 * 3. Otherwise perform the open logic
 * 
 * Example subclasses:
 * - UGUIS_UIAction_OpenSettings (in JeffGame001)
 * - UGUIS_UIAction_OpenBackpack (in TwoLayerBackpackSystem)
 */
UCLASS(Abstract, Blueprintable)
class GENERICUISYSTEMEXTENSION_API UGUIS_UIAction_ToggleUI : public UGUIS_UIAction
{
	GENERATED_BODY()

public:
	UGUIS_UIAction_ToggleUI();

protected:
	// Widget class name substring for toggle detection
	// e.g., "SettingsUI" - if current widget contains this, close it instead of open
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "UIAction|ToggleUI")
	FString TargetWidgetClassNameContains;

	// Target UI layer tag for priority check
	// e.g., "GUIS.Layer.Menu" or "GUIS.Layer.GameMenu"
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "UIAction|ToggleUI")
	FGameplayTag TargetLayerTag;

	// Set by base class InvokeActionInternal - true if close was handled
	// Subclasses should check this after calling Super:: and return if true
	mutable bool bHandledAsClose = false;

	// Compatible with any UGameActivatableWidgetExtension
	virtual bool IsCompatibleInternal_Implementation(const UObject* Data) const override;

	// Check layer priority (toggle is always allowed on matching widget)
	virtual bool CanInvokeInternal_Implementation(const UObject* Data, APlayerController* PlayerController) const override;

	// Base implementation handles close logic, sets bHandledAsClose
	// Subclasses MUST call Super:: first, then check bHandledAsClose
	virtual void InvokeActionInternal_Implementation(const UObject* Data, APlayerController* PlayerController) const override;

	// Helper: check if current widget matches target (should close)
	bool ShouldCloseCurrentWidget(const UObject* Data) const;
};
