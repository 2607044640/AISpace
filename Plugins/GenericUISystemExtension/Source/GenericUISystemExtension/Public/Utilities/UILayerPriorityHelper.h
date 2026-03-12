// UILayerPriorityHelper.h
// Static utility class for UI layer priority operations

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "GameplayTagContainer.h"
#include "UILayerPriorityHelper.generated.h"

class APlayerController;

/**
 * Static utility class for UI layer priority operations.
 * 
 * Layer Priority Order (lowest to highest):
 * - Game (0): HUD elements, always-visible UI
 * - GameMenu (1): In-game menus like inventory
 * - Menu (2): Full menus like settings
 * - Modal (3): Dialogs, confirmations, highest priority
 */
UCLASS()
class GENERICUISYSTEMEXTENSION_API UUILayerPriorityHelper : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()

public:
	static constexpr int32 LAYER_PRIORITY_GAME = 0;
	static constexpr int32 LAYER_PRIORITY_GAMEMENU = 1;
	static constexpr int32 LAYER_PRIORITY_MENU = 2;
	static constexpr int32 LAYER_PRIORITY_MODAL = 3;

	UFUNCTION(BlueprintCallable, Category = "UI|Layer")
	static int32 GetLayerPriority(const FGameplayTag& LayerTag);

	UFUNCTION(BlueprintCallable, Category = "UI|Layer")
	static bool CanOpenUILayer(const APlayerController* PC, const FGameplayTag& TargetLayerTag);

	UFUNCTION(BlueprintCallable, Category = "UI|Layer")
	static FGameplayTag GetHighestActiveLayerTag(const APlayerController* PC);

	UFUNCTION(BlueprintCallable, Category = "UI|Layer")
	static bool HasHigherPriorityActiveLayer(const APlayerController* PC, const FGameplayTag& TargetLayerTag);

private:
	static const TArray<FGameplayTag>& GetOrderedLayerTags();
};
