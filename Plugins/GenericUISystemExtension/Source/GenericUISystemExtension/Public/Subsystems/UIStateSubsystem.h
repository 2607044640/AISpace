// UIStateSubsystem.h
// GameInstance subsystem for managing UI state with reference counting

#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "UIStateSubsystem.generated.h"

/**
 * Subsystem for managing game pause state and input mode when UI is open.
 * Uses reference counting to handle multiple overlapping UIs.
 * 
 * Usage:
 * - Call RequestPause() when opening a UI that should pause the game
 * - Call ReleasePause() when closing that UI
 * - Game only unpauses when all pause requests are released
 */
UCLASS()
class GENERICUISYSTEMEXTENSION_API UUIStateSubsystem : public UGameInstanceSubsystem
{
	GENERATED_BODY()

public:
	virtual void Initialize(FSubsystemCollectionBase& Collection) override;
	virtual void Deinitialize() override;

	UFUNCTION(BlueprintCallable, Category = "UI|State")
	void RequestPause();

	UFUNCTION(BlueprintCallable, Category = "UI|State")
	void ReleasePause();

	UFUNCTION(BlueprintPure, Category = "UI|State")
	bool IsPaused() const { return PauseRequestCount > 0; }

	UFUNCTION(BlueprintPure, Category = "UI|State")
	int32 GetPauseRequestCount() const { return PauseRequestCount; }

protected:
	int32 PauseRequestCount = 0;
	float OriginalTimeDilation = 1.0f;

	void ApplyPause();
	void RemovePause();
	class APlayerController* GetFirstLocalPlayerController() const;
};
