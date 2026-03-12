// GameUILayoutExtension.cpp

#include "Widgets/GameUILayoutExtension.h"
#include "Widgets/CommonActivatableWidgetContainer.h"
#include "GameplayTagContainer.h"

UGameUILayoutExtension::UGameUILayoutExtension(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{
}

void UGameUILayoutExtension::NativeConstruct()
{
	Super::NativeConstruct();
	RegisterAllLayers();
	UE_LOG(LogTemp, Log, TEXT("GameUILayoutExtension: NativeConstruct completed, layers registered"));
}

void UGameUILayoutExtension::RegisterAllLayers()
{
	if (GameLayer_Stack)
	{
		RegisterLayer(FGameplayTag::RequestGameplayTag(FName("GUIS.Layer.Game")), GameLayer_Stack);
		UE_LOG(LogTemp, Log, TEXT("GameUILayoutExtension: Registered GameLayer_Stack"));
	}

	if (GameMenu_Stack)
	{
		RegisterLayer(FGameplayTag::RequestGameplayTag(FName("GUIS.Layer.GameMenu")), GameMenu_Stack);
		UE_LOG(LogTemp, Log, TEXT("GameUILayoutExtension: Registered GameMenu_Stack"));
	}

	if (Menu_Stack)
	{
		RegisterLayer(FGameplayTag::RequestGameplayTag(FName("GUIS.Layer.Menu")), Menu_Stack);
		UE_LOG(LogTemp, Log, TEXT("GameUILayoutExtension: Registered Menu_Stack"));
	}

	if (Modal_Stack)
	{
		RegisterLayer(FGameplayTag::RequestGameplayTag(FName("GUIS.Layer.Modal")), Modal_Stack);
		UE_LOG(LogTemp, Log, TEXT("GameUILayoutExtension: Registered Modal_Stack"));
	}
}
