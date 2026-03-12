// GUIS_UIAction_ToggleUI.cpp

#include "Actions/GUIS_UIAction_ToggleUI.h"
#include "Widgets/GameActivatableWidgetExtension.h"
#include "Utilities/UILayerPriorityHelper.h"
#include "GameFramework/PlayerController.h"

UGUIS_UIAction_ToggleUI::UGUIS_UIAction_ToggleUI()
{
	bShouldDisplayInActionBar = false;
	bRequiresConfirmation = false;
}

bool UGUIS_UIAction_ToggleUI::IsCompatibleInternal_Implementation(const UObject* Data) const
{
	return Data != nullptr && Data->IsA<UGameActivatableWidgetExtension>();
}

bool UGUIS_UIAction_ToggleUI::ShouldCloseCurrentWidget(const UObject* Data) const
{
	if (Data == nullptr || TargetWidgetClassNameContains.IsEmpty())
	{
		return false;
	}

	const FString WidgetClassName = Data->GetClass()->GetName();
	return WidgetClassName.Contains(TargetWidgetClassNameContains);
}

bool UGUIS_UIAction_ToggleUI::CanInvokeInternal_Implementation(const UObject* Data, APlayerController* PlayerController) const
{
	if (Data == nullptr || PlayerController == nullptr)
	{
		return false;
	}

	// If on target widget, always allow (will close)
	if (ShouldCloseCurrentWidget(Data))
	{
		return true;
	}

	// Check layer priority - can only open if no higher priority layer is blocking
	if (TargetLayerTag.IsValid())
	{
		return UUILayerPriorityHelper::CanOpenUILayer(PlayerController, TargetLayerTag);
	}

	return true;
}

void UGUIS_UIAction_ToggleUI::InvokeActionInternal_Implementation(const UObject* Data, APlayerController* PlayerController) const
{
	bHandledAsClose = false;

	if (Data == nullptr)
	{
		UE_LOG(LogTemp, Warning, TEXT("UGUIS_UIAction_ToggleUI: Data is null"));
		return;
	}

	// Check if should close instead of open
	if (ShouldCloseCurrentWidget(Data))
	{
		UGameActivatableWidgetExtension* Widget = Cast<UGameActivatableWidgetExtension>(const_cast<UObject*>(Data));
		if (Widget)
		{
			UE_LOG(LogTemp, Log, TEXT("UGUIS_UIAction_ToggleUI: Closing widget %s (toggle)"), *Widget->GetName());
			Widget->HandleCloseUI();
			bHandledAsClose = true;
		}
	}
	// If not closing, subclass will handle open logic
}
