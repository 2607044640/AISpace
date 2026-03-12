// UIStateSubsystem.cpp

#include "Subsystems/UIStateSubsystem.h"
#include "GameFramework/WorldSettings.h"
#include "GameFramework/PlayerController.h"
#include "Engine/World.h"
#include "Engine/Engine.h"
#include "Kismet/GameplayStatics.h"

void UUIStateSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
	Super::Initialize(Collection);
	PauseRequestCount = 0;
	OriginalTimeDilation = 1.0f;
	UE_LOG(LogTemp, Log, TEXT("UIStateSubsystem: Initialized"));
}

void UUIStateSubsystem::Deinitialize()
{
	if (PauseRequestCount > 0)
	{
		UE_LOG(LogTemp, Warning, TEXT("UIStateSubsystem: Deinitializing with %d active pause requests"), PauseRequestCount);
		PauseRequestCount = 0;
		RemovePause();
	}
	Super::Deinitialize();
}

APlayerController* UUIStateSubsystem::GetFirstLocalPlayerController() const
{
	UWorld* World = GetWorld();
	if (!World) return nullptr;
	return UGameplayStatics::GetPlayerController(World, 0);
}

void UUIStateSubsystem::RequestPause()
{
	PauseRequestCount++;
	UE_LOG(LogTemp, Log, TEXT("UIStateSubsystem: RequestPause (count: %d)"), PauseRequestCount);

	if (PauseRequestCount == 1)
	{
		ApplyPause();
	}
}

void UUIStateSubsystem::ReleasePause()
{
	if (PauseRequestCount <= 0)
	{
		UE_LOG(LogTemp, Warning, TEXT("UIStateSubsystem: ReleasePause called but count is already %d"), PauseRequestCount);
		return;
	}

	PauseRequestCount--;
	UE_LOG(LogTemp, Log, TEXT("UIStateSubsystem: ReleasePause (count: %d)"), PauseRequestCount);

	if (PauseRequestCount == 0)
	{
		RemovePause();
	}
}

void UUIStateSubsystem::ApplyPause()
{
	UWorld* World = GetWorld();
	if (!World)
	{
		UE_LOG(LogTemp, Warning, TEXT("UIStateSubsystem: Cannot apply pause - no world"));
		return;
	}

	AWorldSettings* WorldSettings = World->GetWorldSettings();
	if (WorldSettings)
	{
		OriginalTimeDilation = WorldSettings->TimeDilation;
		WorldSettings->SetTimeDilation(0.0f);
	}

	if (APlayerController* PC = GetFirstLocalPlayerController())
	{
		PC->SetShowMouseCursor(true);
		PC->SetIgnoreLookInput(true);
	}

	UE_LOG(LogTemp, Log, TEXT("UIStateSubsystem: PAUSED"));
}

void UUIStateSubsystem::RemovePause()
{
	UWorld* World = GetWorld();
	if (!World)
	{
		UE_LOG(LogTemp, Warning, TEXT("UIStateSubsystem: Cannot remove pause - no world"));
		return;
	}

	AWorldSettings* WorldSettings = World->GetWorldSettings();
	if (WorldSettings)
	{
		WorldSettings->SetTimeDilation(OriginalTimeDilation);
	}

	if (APlayerController* PC = GetFirstLocalPlayerController())
	{
		PC->SetInputMode(FInputModeGameOnly());
		PC->SetShowMouseCursor(false);
		PC->SetIgnoreLookInput(false);
	}

	UE_LOG(LogTemp, Log, TEXT("UIStateSubsystem: RESUMED + Game Input Mode"));
}
