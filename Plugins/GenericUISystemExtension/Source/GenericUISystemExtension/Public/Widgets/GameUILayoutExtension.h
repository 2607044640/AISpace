// GameUILayoutExtension.h
// C++ base class for WB_GUIS_GameUILayout with BindWidget layer stacks

#pragma once

#include "CoreMinimal.h"
#include "UI/GUIS_GameUILayout.h"
#include "GameUILayoutExtension.generated.h"

class UCommonActivatableWidgetContainerBase;

/**
 * C++ base class for the game UI layout widget.
 * Provides BindWidget properties for the 4 standard UI layer stacks.
 * 
 * Usage:
 * 1. Create a Blueprint widget inheriting from this class
 * 2. Add 4 CommonActivatableWidgetStack widgets named:
 *    - GameLayer_Stack
 *    - GameMenu_Stack
 *    - Menu_Stack
 *    - Modal_Stack
 * 3. The layers are automatically registered in NativeConstruct
 */
UCLASS(Abstract, Blueprintable)
class GENERICUISYSTEMEXTENSION_API UGameUILayoutExtension : public UGUIS_GameUILayout
{
	GENERATED_BODY()

public:
	UGameUILayoutExtension(const FObjectInitializer& ObjectInitializer);

protected:
	virtual void NativeConstruct() override;

	UPROPERTY(meta = (BindWidget))
	UCommonActivatableWidgetContainerBase* GameLayer_Stack;

	UPROPERTY(meta = (BindWidget))
	UCommonActivatableWidgetContainerBase* GameMenu_Stack;

	UPROPERTY(meta = (BindWidget))
	UCommonActivatableWidgetContainerBase* Menu_Stack;

	UPROPERTY(meta = (BindWidget))
	UCommonActivatableWidgetContainerBase* Modal_Stack;

private:
	void RegisterAllLayers();
};
