// BackpackInventoryComponent.cpp

#include "BackpackInventoryComponent.h"
#include "BackpackWidget.h"
#include "UI/GUIS_GameUIFunctionLibrary.h"
#include "Utilities/UILayerPriorityHelper.h"
#include "GameFramework/PlayerController.h"
#include "Engine/Engine.h"
#include "UObject/ConstructorHelpers.h"

UBackpackInventoryComponent::UBackpackInventoryComponent()
{
	PrimaryComponentTick.bCanEverTick = false;

	// Default UI layer tag - GameMenu for inventory-type UIs
	UILayerTag = FGameplayTag::RequestGameplayTag(FName("GUIS.Layer.GameMenu"));
}

void UBackpackInventoryComponent::BeginPlay()
{
	Super::BeginPlay();

	// Validate widget class is set
	if (!BackpackWidgetClass)
	{
		UE_LOG(LogTemp, Warning, TEXT("BackpackInventoryComponent: BackpackWidgetClass not set! Please set it in Blueprint."));
	}
}

APlayerController* UBackpackInventoryComponent::GetPlayerController() const
{
	if (AActor* Owner = GetOwner())
	{
		if (APawn* OwnerPawn = Cast<APawn>(Owner))
		{
			return Cast<APlayerController>(OwnerPawn->GetController());
		}
	}
	return nullptr;
}

bool UBackpackInventoryComponent::IsBackpackOpen() const
{
	// Check both pointer validity AND activation state
	// Widget may still exist (pooled by CommonUI) but be deactivated
	return BackpackWidget.IsValid() && BackpackWidget->IsActivated();
}


bool UBackpackInventoryComponent::OpenBackpackInventory()
{
	UE_LOG(LogTemp, Log, TEXT("BackpackInventoryComponent: OpenInventory called, IsOpen=%s"), 
		IsBackpackOpen() ? TEXT("true") : TEXT("false"));

	// Check if already open (idempotent - return false, don't push duplicate)
	// Use IsBackpackOpen() which checks both validity AND activation state
	if (IsBackpackOpen())
	{
		UE_LOG(LogTemp, Log, TEXT("BackpackInventoryComponent: Backpack already open, ignoring"));
		return false;
	}

	APlayerController* PC = GetPlayerController();
	if (!PC)
	{
		UE_LOG(LogTemp, Warning, TEXT("BackpackInventoryComponent: No PlayerController"));
		return false;
	}

	if (!BackpackWidgetClass)
	{
		UE_LOG(LogTemp, Error, TEXT("BackpackInventoryComponent: BackpackWidgetClass not set!"));
		return false;
	}

	// Check layer priority - block if higher priority layer is active
	if (!UUILayerPriorityHelper::CanOpenUILayer(PC, UILayerTag))
	{
		UE_LOG(LogTemp, Log, TEXT("BackpackInventoryComponent: Blocked by higher priority layer"));
		return false;
	}

	// Open backpack - Push to UI layer
	UE_LOG(LogTemp, Log, TEXT("BackpackInventoryComponent: Opening backpack"));
	
	UCommonActivatableWidget* Widget = UGUIS_GameUIFunctionLibrary::PushContentToUILayer_ForPlayer(
		PC,
		UILayerTag,
		BackpackWidgetClass
	);

	BackpackWidget = Cast<UBackpackWidget>(Widget);

	if (!BackpackWidget.IsValid())
	{
		UE_LOG(LogTemp, Error, TEXT("BackpackInventoryComponent: Failed to create backpack widget!"));
		return false;
	}

	return true;
}
