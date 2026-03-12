// GUIS_InputOverrideSubsystem.h
// Subsystem to apply user custom key bindings to DT_GenericInputActions at runtime

#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "GUIS_InputOverrideSubsystem.generated.h"

class UCommonGenericInputActionDataTable;
class UKeySettingData;

/**
 * Subsystem that modifies DT_GenericInputActions at runtime to apply user custom key bindings
 * This ensures GUIS widgets use custom keys when registering input actions
 */
UCLASS()
class GENERICUISYSTEMEXTENSION_API UGUIS_InputOverrideSubsystem : public UGameInstanceSubsystem
{
	GENERATED_BODY()

public:
	virtual void Initialize(FSubsystemCollectionBase& Collection) override;
	
	// Apply user custom keys from KeySettingData to DT_GenericInputActions
	UFUNCTION(BlueprintCallable, Category = "GUIS|Input")
	void ApplyCustomKeysToDataTable();
	
private:
	UPROPERTY()
	TObjectPtr<UCommonGenericInputActionDataTable> InputDataTable;
};
