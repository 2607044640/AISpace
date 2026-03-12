// UILayerPriorityHelper.cpp

#include "Utilities/UILayerPriorityHelper.h"
#include "GameFramework/PlayerController.h"
#include "UI/GUIS_GameUIPolicy.h"
#include "UI/GUIS_GameUILayout.h"
#include "Widgets/CommonActivatableWidgetContainer.h"

const TArray<FGameplayTag>& UUILayerPriorityHelper::GetOrderedLayerTags()
{
	static TArray<FGameplayTag> OrderedTags;
	
	if (OrderedTags.Num() == 0)
	{
		OrderedTags.Add(FGameplayTag::RequestGameplayTag(FName("GUIS.Layer.Game")));
		OrderedTags.Add(FGameplayTag::RequestGameplayTag(FName("GUIS.Layer.GameMenu")));
		OrderedTags.Add(FGameplayTag::RequestGameplayTag(FName("GUIS.Layer.Menu")));
		OrderedTags.Add(FGameplayTag::RequestGameplayTag(FName("GUIS.Layer.Modal")));
	}
	
	return OrderedTags;
}

int32 UUILayerPriorityHelper::GetLayerPriority(const FGameplayTag& LayerTag)
{
	const TArray<FGameplayTag>& OrderedTags = GetOrderedLayerTags();
	
	for (int32 i = 0; i < OrderedTags.Num(); ++i)
	{
		if (OrderedTags[i] == LayerTag)
		{
			return i;
		}
	}
	
	return -1;
}

bool UUILayerPriorityHelper::CanOpenUILayer(const APlayerController* PC, const FGameplayTag& TargetLayerTag)
{
	if (!PC)
	{
		UE_LOG(LogTemp, Warning, TEXT("UILayerPriorityHelper::CanOpenUILayer - PlayerController is null"));
		return false;
	}
	
	return !HasHigherPriorityActiveLayer(PC, TargetLayerTag);
}

FGameplayTag UUILayerPriorityHelper::GetHighestActiveLayerTag(const APlayerController* PC)
{
	if (!PC)
	{
		return FGameplayTag();
	}
	
	const ULocalPlayer* LocalPlayer = PC->GetLocalPlayer();
	if (!LocalPlayer)
	{
		return FGameplayTag();
	}
	
	UGUIS_GameUIPolicy* Policy = UGUIS_GameUIPolicy::GetGameUIPolicy(PC);
	if (!Policy)
	{
		return FGameplayTag();
	}
	
	UGUIS_GameUILayout* Layout = Policy->GetRootLayout(LocalPlayer);
	if (!Layout)
	{
		return FGameplayTag();
	}
	
	const TArray<FGameplayTag>& OrderedTags = GetOrderedLayerTags();
	for (int32 i = OrderedTags.Num() - 1; i >= 0; --i)
	{
		UCommonActivatableWidgetContainerBase* LayerStack = Layout->GetLayerWidget(OrderedTags[i]);
		if (LayerStack && LayerStack->GetNumWidgets() > 0)
		{
			return OrderedTags[i];
		}
	}
	
	return FGameplayTag();
}

bool UUILayerPriorityHelper::HasHigherPriorityActiveLayer(const APlayerController* PC, const FGameplayTag& TargetLayerTag)
{
	if (!PC)
	{
		return false;
	}
	
	const int32 TargetPriority = GetLayerPriority(TargetLayerTag);
	if (TargetPriority < 0)
	{
		UE_LOG(LogTemp, Warning, TEXT("UILayerPriorityHelper: Invalid TargetLayerTag %s"), *TargetLayerTag.ToString());
		return false;
	}
	
	const ULocalPlayer* LocalPlayer = PC->GetLocalPlayer();
	if (!LocalPlayer)
	{
		return false;
	}
	
	UGUIS_GameUIPolicy* Policy = UGUIS_GameUIPolicy::GetGameUIPolicy(PC);
	if (!Policy)
	{
		return false;
	}
	
	UGUIS_GameUILayout* Layout = Policy->GetRootLayout(LocalPlayer);
	if (!Layout)
	{
		return false;
	}
	
	const TArray<FGameplayTag>& OrderedTags = GetOrderedLayerTags();
	for (int32 i = TargetPriority + 1; i < OrderedTags.Num(); ++i)
	{
		UCommonActivatableWidgetContainerBase* LayerStack = Layout->GetLayerWidget(OrderedTags[i]);
		if (LayerStack && LayerStack->GetNumWidgets() > 0)
		{
			return true;
		}
	}
	
	return false;
}
