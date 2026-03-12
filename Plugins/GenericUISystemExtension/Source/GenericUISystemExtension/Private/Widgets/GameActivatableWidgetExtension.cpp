// GameActivatableWidgetExtension.cpp

#include "Widgets/GameActivatableWidgetExtension.h"
#include "Subsystems/UIStateSubsystem.h"
#include "UI/Actions/GUIS_UIActionFactory.h"
#include "UI/Actions/GUIS_UIAction.h"
#include "Engine/GameInstance.h"
#include "Engine/Engine.h"
#include "Kismet/GameplayStatics.h"
#include "GameFramework/SaveGame.h"
#include "Input/CommonGenericInputActionDataTable.h"
#include "CommonUITypes.h"

UGameActivatableWidgetExtension::UGameActivatableWidgetExtension(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{
	// Set default input mode to Menu (shows mouse cursor, UI-only input)
	InputConfig = EGUIS_ActivatableWidgetInputMode::Menu;
	
	// Default to auto-register UI actions
	bAutoRegisterUIActions = true;
	
	// Default factory path - will be loaded at runtime
	GenericUIActionFactory = TSoftObjectPtr<UGUIS_UIActionFactory>(
		FSoftObjectPath(TEXT("/GenericUISystemExtension/GUIS/DA_GenericUIActions.DA_GenericUIActions")));
}

void UGameActivatableWidgetExtension::NativeConstruct()
{
	Super::NativeConstruct();
}

void UGameActivatableWidgetExtension::RegisterUIActions()
{
	
	if (!bAutoRegisterUIActions)
	{
		return;
	}
	
	if (GenericUIActionFactory.IsNull())
	{
		UE_LOG(LogTemp, Warning, TEXT("GameActivatableWidgetExtension: GenericUIActionFactory is null"));
		return;
	}
	
	// Load factory if not cached
	if (!CachedActionFactory)
	{
		CachedActionFactory = GenericUIActionFactory.LoadSynchronous();
		if (!CachedActionFactory)
		{
			UE_LOG(LogTemp, Warning, TEXT("GameActivatableWidgetExtension: Failed to load GenericUIActionFactory"));
			return;
		}
	}
	
	// Load user custom key bindings
	USaveGame* KeySettingsObj = nullptr;
	if (UGameplayStatics::DoesSaveGameExist(TEXT("KeyMap"), 0))
	{
		KeySettingsObj = UGameplayStatics::LoadGameFromSlot(TEXT("KeyMap"), 0);
	}
	
	// Get UserSaveKeyMap using reflection to avoid circular dependency
	TMap<FName, FKey> CustomKeys;
	if (KeySettingsObj)
	{
		FMapProperty* MapProperty = FindFProperty<FMapProperty>(KeySettingsObj->GetClass(), TEXT("UserSaveKeyMap"));
		if (MapProperty)
		{
			const void* MapPtr = MapProperty->ContainerPtrToValuePtr<void>(KeySettingsObj);
			FScriptMapHelper MapHelper(MapProperty, MapPtr);
			
			for (int32 i = 0; i < MapHelper.Num(); ++i)
			{
				FName* KeyPtr = reinterpret_cast<FName*>(MapHelper.GetKeyPtr(i));
				FKey* ValuePtr = reinterpret_cast<FKey*>(MapHelper.GetValuePtr(i));
				if (KeyPtr && ValuePtr)
				{
					CustomKeys.Add(*KeyPtr, *ValuePtr);
				}
			}
			
			UE_LOG(LogTemp, Log, TEXT("GameActivatableWidgetExtension: Loaded %d custom key bindings"), CustomKeys.Num());
		}
	}
	
	// Find available actions for this widget
	TArray<UGUIS_UIAction*> Actions = CachedActionFactory->FindAvailableUIActionsForData(this);
	
	for (const UGUIS_UIAction* Action : Actions)
	{
		if (Action->CanInvoke(this, GetOwningPlayer()))
		{
			FDataTableRowHandle InputHandle = Action->GetInputActionData();
			
			// Check if user has custom key for this action
			if (CustomKeys.Num() > 0 && InputHandle.DataTable)
			{
				FName RowName = InputHandle.RowName;
				if (CustomKeys.Contains(RowName))
				{
					FKey CustomKey = CustomKeys[RowName];
					
					// Get the DataTable row and modify it directly (cast away const)
					const UDataTable* ConstDataTable = InputHandle.DataTable.Get();
					UDataTable* DataTable = const_cast<UDataTable*>(ConstDataTable);
					if (UCommonGenericInputActionDataTable* CommonDataTable = Cast<UCommonGenericInputActionDataTable>(DataTable))
					{
						TMap<FName, uint8*>& RowMap = const_cast<TMap<FName, uint8*>&>(CommonDataTable->GetRowMap());
						if (uint8* RowPtr = RowMap.FindRef(RowName))
						{
							FCommonInputActionDataBase* RowData = reinterpret_cast<FCommonInputActionDataBase*>(RowPtr);
							
							// Use reflection to modify the KeyboardInputTypeInfo.Key field
							FStructProperty* TypeInfoProperty = FindFProperty<FStructProperty>(
								FCommonInputActionDataBase::StaticStruct(), TEXT("KeyboardInputTypeInfo"));
							
							if (TypeInfoProperty)
							{
								void* TypeInfoPtr = TypeInfoProperty->ContainerPtrToValuePtr<void>(RowData);
								FCommonInputTypeInfo* TypeInfo = reinterpret_cast<FCommonInputTypeInfo*>(TypeInfoPtr);
								
								// Modify the Key field in FCommonInputTypeInfo
								FStructProperty* KeyProperty = FindFProperty<FStructProperty>(
									FCommonInputTypeInfo::StaticStruct(), TEXT("Key"));
								
								if (KeyProperty)
								{
									void* KeyPtr = KeyProperty->ContainerPtrToValuePtr<void>(TypeInfo);
									*reinterpret_cast<FKey*>(KeyPtr) = CustomKey;
									
									UE_LOG(LogTemp, Log, TEXT("✅ Applied custom key %s to action %s"), 
										*CustomKey.ToString(), *RowName.ToString());
									
									if (GEngine)
									{
										FString Msg = FString::Printf(TEXT("✅ Binding: %s -> %s"), 
											*RowName.ToString(), *CustomKey.ToString());
										GEngine->AddOnScreenDebugMessage(-1, 3.f, FColor::Cyan, Msg, true, FVector2D(1.2f, 1.2f));
									}
								}
							}
						}
					}
				}
			}
			
			// Register action binding directly on THIS widget (not on a separate UIActionWidget)
			FBindUIActionArgs BindArgs(Action->GetInputActionData(), Action->GetShouldDisplayInActionBar(),
				FSimpleDelegate::CreateUObject(const_cast<UGameActivatableWidgetExtension*>(this), 
					&UGameActivatableWidgetExtension::HandleUIAction, Action));
			
			ActionBindings.Add(RegisterUIActionBinding(BindArgs));
			
			UE_LOG(LogTemp, Log, TEXT("GameActivatableWidgetExtension: Registered action %s for %s"), 
				*Action->GetActionID().ToString(), *GetName());
		}
	}
	
	UE_LOG(LogTemp, Log, TEXT("GameActivatableWidgetExtension: Registered %d UIActions for %s"), 
		ActionBindings.Num(), *GetName());
}

void UGameActivatableWidgetExtension::UnregisterUIActions()
{
	for (FUIActionBindingHandle& ActionBinding : ActionBindings)
	{
		ActionBinding.Unregister();
	}
	ActionBindings.Empty();
	
	UE_LOG(LogTemp, Log, TEXT("GameActivatableWidgetExtension: Unregistered UIActions for %s"), *GetName());
}

void UGameActivatableWidgetExtension::HandleUIAction(const UGUIS_UIAction* Action)
{
	if (!Action)
	{
		return;
	}
	
	UE_LOG(LogTemp, Log, TEXT("GameActivatableWidgetExtension: HandleUIAction %s on %s"), 
		*Action->GetActionID().ToString(), *GetName());
	
	if (Action->CanInvoke(this, GetOwningPlayer()))
	{
		Action->InvokeAction(this, GetOwningPlayer());
	}
}

void UGameActivatableWidgetExtension::HandleCloseUI()
{
	UE_LOG(LogTemp, Log, TEXT("HandleCloseUI called on: %s"), *GetName());
	DeactivateWidget();
}

void UGameActivatableWidgetExtension::NativeOnActivated()
{
	Super::NativeOnActivated();
	
	// Request pause
	if (bShouldPauseGame)
	{
		if (UGameInstance* GameInstance = GetGameInstance())
		{
			if (UUIStateSubsystem* UIStateSubsystem = GameInstance->GetSubsystem<UUIStateSubsystem>())
			{
				UIStateSubsystem->RequestPause();
			}
			else
			{
				UE_LOG(LogTemp, Warning, TEXT("GameActivatableWidgetExtension: UIStateSubsystem not found"));
			}
		}
	}
	
	// Register UI actions directly on this widget
	RegisterUIActions();
}

void UGameActivatableWidgetExtension::NativeOnDeactivated()
{
	UE_LOG(LogTemp, Log, TEXT("Widget DEACTIVATED: %s"), *GetName());

	// Unregister UI actions
	UnregisterUIActions();

	// Release pause
	if (bShouldPauseGame)
	{
		if (UGameInstance* GameInstance = GetGameInstance())
		{
			if (UUIStateSubsystem* UIStateSubsystem = GameInstance->GetSubsystem<UUIStateSubsystem>())
			{
				UIStateSubsystem->ReleasePause();
			}
		}
	}

	Super::NativeOnDeactivated();
}
