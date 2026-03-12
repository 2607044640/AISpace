// GUIS_InputOverrideSubsystem.cpp

#include "Subsystems/GUIS_InputOverrideSubsystem.h"
#include "Input/CommonGenericInputActionDataTable.h"
#include "CommonUITypes.h"
#include "CommonInputTypeEnum.h"
#include "Kismet/GameplayStatics.h"
#include "GameFramework/SaveGame.h"
#include "Engine/Engine.h"

void UGUIS_InputOverrideSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
	Super::Initialize(Collection);
	
	// Load DT_GenericInputActions
	const FString DataTablePath = TEXT("/Script/CommonUI.CommonGenericInputActionDataTable'/GenericUISystemExtension/GUIS/DT_GenericInputActions.DT_GenericInputActions'");
	InputDataTable = Cast<UCommonGenericInputActionDataTable>(
		StaticLoadObject(UCommonGenericInputActionDataTable::StaticClass(), nullptr, *DataTablePath));
	
	if (!InputDataTable)
	{
		UE_LOG(LogTemp, Error, TEXT("GUIS_InputOverrideSubsystem: Failed to load DT_GenericInputActions from %s"), *DataTablePath);
		return;
	}
	
	// Apply custom keys at startup
	ApplyCustomKeysToDataTable();
	
	UE_LOG(LogTemp, Log, TEXT("GUIS_InputOverrideSubsystem: Initialized"));
}

void UGUIS_InputOverrideSubsystem::ApplyCustomKeysToDataTable()
{
	if (!InputDataTable)
	{
		UE_LOG(LogTemp, Warning, TEXT("GUIS_InputOverrideSubsystem: InputDataTable is null"));
		return;
	}
	
	// Load user custom keys from save game
	USaveGame* SaveGameObject = nullptr;
	if (UGameplayStatics::DoesSaveGameExist(TEXT("KeyMap"), 0))
	{
		SaveGameObject = UGameplayStatics::LoadGameFromSlot(TEXT("KeyMap"), 0);
	}
	
	if (!SaveGameObject)
	{
		UE_LOG(LogTemp, Log, TEXT("GUIS_InputOverrideSubsystem: No custom keys save file found"));
		return;
	}
	
	// Get UserSaveKeyMap using reflection (to avoid circular dependency)
	FMapProperty* MapProperty = FindFProperty<FMapProperty>(SaveGameObject->GetClass(), TEXT("UserSaveKeyMap"));
	if (!MapProperty)
	{
		UE_LOG(LogTemp, Error, TEXT("GUIS_InputOverrideSubsystem: UserSaveKeyMap property not found"));
		return;
	}
	
	const void* MapPtr = MapProperty->ContainerPtrToValuePtr<void>(SaveGameObject);
	FScriptMapHelper MapHelper(MapProperty, MapPtr);
	
	if (MapHelper.Num() == 0)
	{
		UE_LOG(LogTemp, Log, TEXT("GUIS_InputOverrideSubsystem: No custom keys found in save data"));
		return;
	}
	
	// Iterate through DataTable rows and apply custom keys
	int32 AppliedCount = 0;
	for (auto& RowPair : InputDataTable->GetRowMap())
	{
		FName RowName = RowPair.Key;
		FCommonInputActionDataBase* RowData = reinterpret_cast<FCommonInputActionDataBase*>(RowPair.Value);
		
		if (!RowData)
		{
			continue;
		}
		
		// Check if user has custom key for this row
		for (int32 i = 0; i < MapHelper.Num(); ++i)
		{
			FName* KeyPtr = reinterpret_cast<FName*>(MapHelper.GetKeyPtr(i));
			FKey* ValuePtr = reinterpret_cast<FKey*>(MapHelper.GetValuePtr(i));
			
			if (KeyPtr && ValuePtr && *KeyPtr == RowName)
			{
				// Found custom key - use reflection to modify the DataTable row
				FKey CustomKey = *ValuePtr;
				
				// Get KeyboardInputTypeInfo using GetInputTypeInfo
				FCommonInputTypeInfo TypeInfo = RowData->GetInputTypeInfo(ECommonInputType::MouseAndKeyboard, NAME_None);
				
				// Use reflection to set the private Key field
				FStructProperty* KeyProperty = FindFProperty<FStructProperty>(FCommonInputTypeInfo::StaticStruct(), TEXT("Key"));
				if (KeyProperty)
				{
					void* KeyValuePtr = KeyProperty->ContainerPtrToValuePtr<void>(&TypeInfo);
					*reinterpret_cast<FKey*>(KeyValuePtr) = CustomKey;
					
					// Now we need to set this back to the RowData
					// Access the protected KeyboardInputTypeInfo field using reflection
					FStructProperty* TypeInfoProperty = FindFProperty<FStructProperty>(FCommonInputActionDataBase::StaticStruct(), TEXT("KeyboardInputTypeInfo"));
					if (TypeInfoProperty)
					{
						void* TypeInfoValuePtr = TypeInfoProperty->ContainerPtrToValuePtr<void>(RowData);
						*reinterpret_cast<FCommonInputTypeInfo*>(TypeInfoValuePtr) = TypeInfo;
						
						AppliedCount++;
						UE_LOG(LogTemp, Log, TEXT("GUIS_InputOverrideSubsystem: Applied custom key %s to row %s"), 
							*CustomKey.ToString(), *RowName.ToString());
						
						// Show on screen for debugging
						if (GEngine)
						{
							FString Msg = FString::Printf(TEXT("✅ Applied: %s -> %s"), *RowName.ToString(), *CustomKey.ToString());
							GEngine->AddOnScreenDebugMessage(-1, 5.f, FColor::Green, Msg, true, FVector2D(1.5f, 1.5f));
						}
					}
				}
				
				break;
			}
		}
	}
	
	UE_LOG(LogTemp, Log, TEXT("GUIS_InputOverrideSubsystem: Applied %d custom keys to DataTable"), AppliedCount);
}
