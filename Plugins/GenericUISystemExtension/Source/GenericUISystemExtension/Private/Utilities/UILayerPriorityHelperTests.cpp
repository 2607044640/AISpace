// UILayerPriorityHelperTests.cpp
// Property-Based Tests for UUILayerPriorityHelper

#include "CoreMinimal.h"
#include "Misc/AutomationTest.h"
#include "Math/RandomStream.h"
#include "Utilities/UILayerPriorityHelper.h"
#include "GameplayTagContainer.h"

struct FLayerStateModel
{
	TArray<int32> LayerWidgetCounts;
	
	FLayerStateModel()
	{
		LayerWidgetCounts.SetNum(4);
		for (int32& Count : LayerWidgetCounts)
		{
			Count = 0;
		}
	}
	
	void SetWidgetCount(int32 LayerPriority, int32 Count)
	{
		if (LayerPriority >= 0 && LayerPriority < 4)
		{
			LayerWidgetCounts[LayerPriority] = FMath::Max(0, Count);
		}
	}
	
	int32 GetWidgetCount(int32 LayerPriority) const
	{
		if (LayerPriority >= 0 && LayerPriority < 4)
		{
			return LayerWidgetCounts[LayerPriority];
		}
		return 0;
	}
	
	bool HasActiveWidgets(int32 LayerPriority) const
	{
		return GetWidgetCount(LayerPriority) > 0;
	}
	
	bool CanOpenLayer(int32 TargetPriority) const
	{
		if (TargetPriority < 0 || TargetPriority >= 4)
		{
			return false;
		}
		
		for (int32 i = TargetPriority + 1; i < 4; ++i)
		{
			if (HasActiveWidgets(i))
			{
				return false;
			}
		}
		return true;
	}
	
	int32 GetHighestActiveLayerPriority() const
	{
		for (int32 i = 3; i >= 0; --i)
		{
			if (HasActiveWidgets(i))
			{
				return i;
			}
		}
		return -1;
	}
	
	bool HasHigherPriorityActiveLayer(int32 TargetPriority) const
	{
		if (TargetPriority < 0 || TargetPriority >= 4)
		{
			return false;
		}
		
		for (int32 i = TargetPriority + 1; i < 4; ++i)
		{
			if (HasActiveWidgets(i))
			{
				return true;
			}
		}
		return false;
	}
};

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FUILayerPriorityBlockingTest,
	"Project.GenericUISystemExtension.UILayerPriority.Property1_LayerPriorityBlocking",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FUILayerPriorityBlockingTest::RunTest(const FString& Parameters)
{
	const int32 NumIterations = 100;
	FRandomStream RandomStream(FDateTime::Now().GetTicks());
	
	TestEqual(TEXT("Game layer priority should be 0"),
		UUILayerPriorityHelper::GetLayerPriority(FGameplayTag::RequestGameplayTag(FName("GUIS.Layer.Game"))),
		UUILayerPriorityHelper::LAYER_PRIORITY_GAME);
	TestEqual(TEXT("GameMenu layer priority should be 1"),
		UUILayerPriorityHelper::GetLayerPriority(FGameplayTag::RequestGameplayTag(FName("GUIS.Layer.GameMenu"))),
		UUILayerPriorityHelper::LAYER_PRIORITY_GAMEMENU);
	TestEqual(TEXT("Menu layer priority should be 2"),
		UUILayerPriorityHelper::GetLayerPriority(FGameplayTag::RequestGameplayTag(FName("GUIS.Layer.Menu"))),
		UUILayerPriorityHelper::LAYER_PRIORITY_MENU);
	TestEqual(TEXT("Modal layer priority should be 3"),
		UUILayerPriorityHelper::GetLayerPriority(FGameplayTag::RequestGameplayTag(FName("GUIS.Layer.Modal"))),
		UUILayerPriorityHelper::LAYER_PRIORITY_MODAL);
	TestEqual(TEXT("Empty tag should return -1"),
		UUILayerPriorityHelper::GetLayerPriority(FGameplayTag()),
		-1);
	
	for (int32 Iteration = 0; Iteration < NumIterations; ++Iteration)
	{
		FLayerStateModel Model;
		
		for (int32 Layer = 0; Layer < 4; ++Layer)
		{
			Model.SetWidgetCount(Layer, RandomStream.RandRange(0, 3));
		}
		
		for (int32 TargetLayer = 0; TargetLayer < 4; ++TargetLayer)
		{
			const bool ModelCanOpen = Model.CanOpenLayer(TargetLayer);
			const bool ModelHasHigherActive = Model.HasHigherPriorityActiveLayer(TargetLayer);
			
			TestEqual(FString::Printf(TEXT("Iter %d, Layer %d: CanOpen should be !HasHigherActive"),
				Iteration, TargetLayer), ModelCanOpen, !ModelHasHigherActive);
			
			bool ExpectedBlocked = false;
			for (int32 HigherLayer = TargetLayer + 1; HigherLayer < 4; ++HigherLayer)
			{
				if (Model.HasActiveWidgets(HigherLayer))
				{
					ExpectedBlocked = true;
					break;
				}
			}
			
			TestEqual(FString::Printf(TEXT("Iter %d, Layer %d: Blocking logic should match expected"),
				Iteration, TargetLayer), !ModelCanOpen, ExpectedBlocked);
		}
	}
	
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FUIHighestActiveLayerTest,
	"Project.GenericUISystemExtension.UILayerPriority.Property2_HighestActiveLayerDetection",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FUIHighestActiveLayerTest::RunTest(const FString& Parameters)
{
	const int32 NumIterations = 100;
	FRandomStream RandomStream(FDateTime::Now().GetTicks() + 12345);
	
	for (int32 Iteration = 0; Iteration < NumIterations; ++Iteration)
	{
		FLayerStateModel Model;
		
		for (int32 Layer = 0; Layer < 4; ++Layer)
		{
			Model.SetWidgetCount(Layer, RandomStream.RandRange(0, 3));
		}
		
		const int32 ExpectedHighestPriority = Model.GetHighestActiveLayerPriority();
		
		if (ExpectedHighestPriority == -1)
		{
			for (int32 Layer = 0; Layer < 4; ++Layer)
			{
				TestEqual(FString::Printf(TEXT("Iter %d: Layer %d should have 0 widgets when no active layers"),
					Iteration, Layer), Model.GetWidgetCount(Layer), 0);
			}
		}
		else
		{
			TestTrue(FString::Printf(TEXT("Iter %d: Highest active layer %d should have widgets"),
				Iteration, ExpectedHighestPriority), Model.HasActiveWidgets(ExpectedHighestPriority));
			
			for (int32 HigherLayer = ExpectedHighestPriority + 1; HigherLayer < 4; ++HigherLayer)
			{
				TestFalse(FString::Printf(TEXT("Iter %d: Layer %d (higher than %d) should have no widgets"),
					Iteration, HigherLayer, ExpectedHighestPriority), Model.HasActiveWidgets(HigherLayer));
			}
		}
	}
	
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FUILayerBlockingScenarioTest,
	"Project.GenericUISystemExtension.UILayerPriority.Property1_BlockingScenarios",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FUILayerBlockingScenarioTest::RunTest(const FString& Parameters)
{
	{
		FLayerStateModel Model;
		Model.SetWidgetCount(UUILayerPriorityHelper::LAYER_PRIORITY_MENU, 1);
		TestFalse(TEXT("Req 4.1: GameMenu should be blocked when Menu is active"),
			Model.CanOpenLayer(UUILayerPriorityHelper::LAYER_PRIORITY_GAMEMENU));
	}
	
	{
		FLayerStateModel Model;
		Model.SetWidgetCount(UUILayerPriorityHelper::LAYER_PRIORITY_MODAL, 1);
		TestFalse(TEXT("Req 4.2: GameMenu should be blocked when Modal is active"),
			Model.CanOpenLayer(UUILayerPriorityHelper::LAYER_PRIORITY_GAMEMENU));
	}
	
	{
		FLayerStateModel Model;
		Model.SetWidgetCount(UUILayerPriorityHelper::LAYER_PRIORITY_MODAL, 1);
		TestFalse(TEXT("Req 4.3: Menu should be blocked when Modal is active"),
			Model.CanOpenLayer(UUILayerPriorityHelper::LAYER_PRIORITY_MENU));
	}
	
	{
		TestTrue(TEXT("Req 4.4: Game(0) < GameMenu(1)"),
			UUILayerPriorityHelper::LAYER_PRIORITY_GAME < UUILayerPriorityHelper::LAYER_PRIORITY_GAMEMENU);
		TestTrue(TEXT("Req 4.4: GameMenu(1) < Menu(2)"),
			UUILayerPriorityHelper::LAYER_PRIORITY_GAMEMENU < UUILayerPriorityHelper::LAYER_PRIORITY_MENU);
		TestTrue(TEXT("Req 4.4: Menu(2) < Modal(3)"),
			UUILayerPriorityHelper::LAYER_PRIORITY_MENU < UUILayerPriorityHelper::LAYER_PRIORITY_MODAL);
	}
	
	{
		FLayerStateModel Model;
		Model.SetWidgetCount(UUILayerPriorityHelper::LAYER_PRIORITY_GAMEMENU, 1);
		TestTrue(TEXT("Same priority: GameMenu should not block GameMenu"),
			Model.CanOpenLayer(UUILayerPriorityHelper::LAYER_PRIORITY_GAMEMENU));
	}
	
	{
		FLayerStateModel Model;
		Model.SetWidgetCount(UUILayerPriorityHelper::LAYER_PRIORITY_GAME, 1);
		Model.SetWidgetCount(UUILayerPriorityHelper::LAYER_PRIORITY_GAMEMENU, 1);
		TestTrue(TEXT("Lower priority should not block: Menu can open when Game/GameMenu active"),
			Model.CanOpenLayer(UUILayerPriorityHelper::LAYER_PRIORITY_MENU));
		TestTrue(TEXT("Lower priority should not block: Modal can open when Game/GameMenu active"),
			Model.CanOpenLayer(UUILayerPriorityHelper::LAYER_PRIORITY_MODAL));
	}
	
	return true;
}
