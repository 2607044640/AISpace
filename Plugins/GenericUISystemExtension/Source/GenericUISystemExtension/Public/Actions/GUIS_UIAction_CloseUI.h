// GUIS_UIAction_CloseUI.h
// UIAction for closing widgets - works with any GameActivatableWidgetExtension

#pragma once

#include "CoreMinimal.h"
#include "UI/Actions/GUIS_UIAction.h"
#include "GUIS_UIAction_CloseUI.generated.h"

/**
 * UIAction that closes the associated widget.
 * 
 * Usage:
 * 1. Create a UGUIS_UIActionFactory DataAsset with this action
 * 2. Add UGUIS_UIActionWidget to your widget Blueprint
 * 3. Set ActionFactory on the UIActionWidget
 * 4. OnActivated: SetAssociatedData(self), then RegisterActions()
 * 5. OnDeactivated: UnregisterActions()
 * 
 * When the bound input is triggered, this action will call HandleCloseUI()
 * on the associated widget, which deactivates it.
 */
UCLASS(Blueprintable, meta = (DisplayName = "Close UI Action"))
class GENERICUISYSTEMEXTENSION_API UGUIS_UIAction_CloseUI : public UGUIS_UIAction
{
	GENERATED_BODY()

public:
	UGUIS_UIAction_CloseUI();

protected:
	// Compatible with any UGameActivatableWidgetExtension
	virtual bool IsCompatibleInternal_Implementation(const UObject* Data) const override;

	// Always can invoke (close is always allowed)
	virtual bool CanInvokeInternal_Implementation(const UObject* Data, APlayerController* PlayerController) const override;

	// Call HandleCloseUI() on the widget
	virtual void InvokeActionInternal_Implementation(const UObject* Data, APlayerController* PlayerController) const override;
};
