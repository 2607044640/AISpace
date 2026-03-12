// GUIS_UIAction_OpenBackpack.cpp

#include "Actions/GUIS_UIAction_ToggleBackpack.h"
#include "BackpackInventoryComponent.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/Pawn.h"

UGUIS_UIAction_ToggleBackpack::UGUIS_UIAction_ToggleBackpack()
{
	DisplayName = FText::FromString(TEXT("Backpack"));
	ActionID = FName("ToggleBackpack");
	
	// Configure base class properties
	TargetWidgetClassNameContains = TEXT("Backpack");
	TargetLayerTag = FGameplayTag::RequestGameplayTag(FName("GUIS.Layer.GameMenu"));
}

void UGUIS_UIAction_ToggleBackpack::InvokeActionInternal_Implementation(const UObject* Data, APlayerController* PlayerController) const
{
	// Let base class handle close logic first
	Super::InvokeActionInternal_Implementation(Data, PlayerController);
	
	// If base class handled close, don't open
	if (bHandledAsClose)
	{
		return;
	}

	if (!PlayerController)
	{
		UE_LOG(LogTemp, Warning, TEXT("UGUIS_UIAction_OpenBackpack: PlayerController is null"));
		return;
	}

	APawn* Pawn = PlayerController->GetPawn();
	if (!Pawn)
	{
		UE_LOG(LogTemp, Warning, TEXT("UGUIS_UIAction_OpenBackpack: Pawn is null"));
		return;
	}

	UBackpackInventoryComponent* BackpackComp = Pawn->FindComponentByClass<UBackpackInventoryComponent>();
	if (!BackpackComp)
	{
		UE_LOG(LogTemp, Warning, TEXT("UGUIS_UIAction_OpenBackpack: BackpackInventoryComponent not found on Pawn"));
		return;
	}

	UE_LOG(LogTemp, Log, TEXT("UGUIS_UIAction_OpenBackpack: Calling OpenBackpackInventory"));
	bool bResult = BackpackComp->OpenBackpackInventory();
	UE_LOG(LogTemp, Log, TEXT("UGUIS_UIAction_OpenBackpack: OpenBackpackInventory returned %s"), 
		bResult ? TEXT("true") : TEXT("false"));
}
