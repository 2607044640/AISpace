// GUIS_UIAction_CloseUI.cpp

#include "Actions/GUIS_UIAction_CloseUI.h"
#include "Widgets/GameActivatableWidgetExtension.h"

UGUIS_UIAction_CloseUI::UGUIS_UIAction_CloseUI()
{
	DisplayName = FText::FromString(TEXT("Close"));
	ActionID = FName("CloseUI");
	bShouldDisplayInActionBar = false;
	bRequiresConfirmation = false;
}

bool UGUIS_UIAction_CloseUI::IsCompatibleInternal_Implementation(const UObject* Data) const
{
	return Data != nullptr && Data->IsA<UGameActivatableWidgetExtension>();
}

bool UGUIS_UIAction_CloseUI::CanInvokeInternal_Implementation(const UObject* Data, APlayerController* PlayerController) const
{
	if (Data == nullptr)
	{
		return false;
	}
	
	const UGameActivatableWidgetExtension* Widget = Cast<UGameActivatableWidgetExtension>(Data);
	return Widget != nullptr && Widget->IsActivated();
}

void UGUIS_UIAction_CloseUI::InvokeActionInternal_Implementation(const UObject* Data, APlayerController* PlayerController) const
{
	Super::InvokeActionInternal_Implementation(Data, PlayerController);
	
	if (Data == nullptr)
	{
		UE_LOG(LogTemp, Warning, TEXT("UGUIS_UIAction_CloseUI: Data is null"));
		return;
	}

	UGameActivatableWidgetExtension* Widget = Cast<UGameActivatableWidgetExtension>(const_cast<UObject*>(Data));

	if (Widget)
	{
		UE_LOG(LogTemp, Log, TEXT("UGUIS_UIAction_CloseUI: Closing widget %s"), *Widget->GetName());
		Widget->HandleCloseUI();
	}
	else
	{
		UE_LOG(LogTemp, Warning, TEXT("UGUIS_UIAction_CloseUI: Failed to cast Data to UGameActivatableWidgetExtension"));
	}
}
