// BackpackInventoryComponent.h
// Component for managing backpack/inventory UI using GenericUISystem

#pragma once

#include "CoreMinimal.h"
#include "GameplayTagContainer.h"
#include "BackpackInventoryComponent.generated.h"

class UBackpackWidget;

/**
 * Component for managing backpack/inventory UI.
 * 
 * Uses GenericUISystem for UI layer management:
 * - Push/Pop widget to UI layer stack
 * - Automatic input mode switching (handled by BackpackWidget)
 * - Automatic game pause (handled by BackpackWidget)
 * 
 * Usage:
 * 1. Add this component to your character/pawn
 * 2. Set BackpackWidgetClass to your Blueprint widget (derived from UBackpackWidget)
 * 3. Call OpenInventory() to show the backpack (ESC/A key closes it)
 */
UCLASS(Blueprintable, ClassGroup=(Custom), meta=(BlueprintSpawnableComponent))
class TWOLAYERBACKPACKSYSTEM_API UBackpackInventoryComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UBackpackInventoryComponent();

	// Open backpack UI (replaces ToggleInventory)
	// Returns false if already open or blocked by higher priority layer
	UFUNCTION(BlueprintCallable, Category = "Backpack")
	bool OpenBackpackInventory();
	
	// Check if backpack is currently open
	UFUNCTION(BlueprintPure, Category = "Backpack")
	bool IsBackpackOpen() const;

protected:
	virtual void BeginPlay() override;

	// Get owning player controller
	APlayerController* GetPlayerController() const;

	// Backpack widget class (set in Blueprint, must derive from UBackpackWidget)
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Backpack|UI")
	TSubclassOf<UBackpackWidget> BackpackWidgetClass;

	// UI Layer tag for backpack (default: GUIS.Layer.Menu)
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Backpack|UI", meta = (Categories = "UI.Layer,GUIS.Layer"))
	FGameplayTag UILayerTag;

private:
	// Current backpack widget instance (nullptr when closed)
	UPROPERTY()
	TWeakObjectPtr<UBackpackWidget> BackpackWidget;
};
