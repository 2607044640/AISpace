// GameActivatableWidgetExtension.h
// Base widget class that integrates with UIStateSubsystem for pause management

#pragma once

#include "CoreMinimal.h"
#include "UI/GUIS_ActivatableWidget.h"
#include "Input/CommonUIInputTypes.h"
#include "GameActivatableWidgetExtension.generated.h"

class UGUIS_UIActionFactory;
class UGUIS_UIAction;

/**
 * Base widget class for game UI that should pause the game when shown.
 * 
 * Features:
 * - Inherits from UGUIS_ActivatableWidget for GenericUISystem integration
 * - Automatically requests pause from UIStateSubsystem when activated
 * - Automatically releases pause when deactivated
 * - Reference counting ensures game stays paused when multiple UIs are open
 * - Auto-creates and manages UGUIS_UIActionWidget for generic UI actions (Close, OpenSettings, etc.)
 * 
 * Usage:
 * 1. Create a Blueprint widget inheriting from this class
 * 2. Use UGUIS_GameUIFunctionLibrary::PushContentToUILayer_ForPlayer() to show
 * 3. Pause is automatically managed
 * 4. UIActions (Close, OpenSettings) are automatically registered when bAutoRegisterUIActions = true
 */
UCLASS(Abstract, Blueprintable)
class GENERICUISYSTEMEXTENSION_API UGameActivatableWidgetExtension : public UGUIS_ActivatableWidget
{
	GENERATED_BODY()

public:
	UGameActivatableWidgetExtension(const FObjectInitializer& ObjectInitializer);

	/**
	 * Handle close UI action - closes this widget
	 * Called by UIAction system when close input is triggered
	 */
	UFUNCTION(BlueprintCallable, Category = "UI")
	void HandleCloseUI();

protected:
	virtual void NativeConstruct() override;
	virtual void NativeOnActivated() override;
	virtual void NativeOnDeactivated() override;

	// Whether this widget should pause the game when shown
	UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category = "UI|GameState")
	bool bShouldPauseGame = true;

	// Whether to automatically create and register UIActions (Close, OpenSettings, etc.)
	// When true, no Blueprint setup is needed for basic UI actions
	UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category = "UI|Actions")
	bool bAutoRegisterUIActions = true;

	// The UIActionFactory to use for auto-registered actions
	// Default: DA_GenericUIActions (loaded at runtime)
	UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category = "UI|Actions", meta = (EditCondition = "bAutoRegisterUIActions"))
	TSoftObjectPtr<UGUIS_UIActionFactory> GenericUIActionFactory;

private:
	// Action bindings registered on this widget (not on a separate UIActionWidget)
	TArray<FUIActionBindingHandle> ActionBindings;
	
	// Cached action factory
	UPROPERTY()
	TObjectPtr<UGUIS_UIActionFactory> CachedActionFactory;

	// Register UI actions directly on this widget
	void RegisterUIActions();
	
	// Unregister UI actions
	void UnregisterUIActions();
	
	// Handle UI action invocation
	void HandleUIAction(const UGUIS_UIAction* Action);
};
