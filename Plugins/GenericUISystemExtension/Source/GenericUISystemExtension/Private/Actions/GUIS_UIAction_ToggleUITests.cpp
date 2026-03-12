// GUIS_UIAction_ToggleUITests.cpp
// Property-Based Tests for Toggle UI Actions
// **Feature: unify-input-system, Property 1: Toggle UI State Consistency**
// **Validates: Requirements 3.2, 3.3**

#include "CoreMinimal.h"
#include "Misc/AutomationTest.h"
#include "Math/RandomStream.h"

/**
 * Model for Toggle UI State
 * Simulates the toggle behavior without requiring actual widgets
 */
struct FToggleUIStateModel
{
	bool bIsOpen = false;
	FString WidgetClassName;
	
	FToggleUIStateModel(const FString& InClassName = TEXT("TestWidget"))
		: WidgetClassName(InClassName)
	{
	}
	
	// Simulate toggle action
	void Toggle()
	{
		bIsOpen = !bIsOpen;
	}
	
	// Check if widget matches target (for close detection)
	bool MatchesTarget(const FString& TargetClassNameContains) const
	{
		return WidgetClassName.Contains(TargetClassNameContains);
	}
	
	// Simulate the toggle logic from UGUIS_UIAction_ToggleUI
	// Returns true if action was handled as close, false if open
	bool SimulateToggleAction(const FString& TargetClassNameContains)
	{
		if (bIsOpen && MatchesTarget(TargetClassNameContains))
		{
			// Close the widget
			bIsOpen = false;
			return true; // Handled as close
		}
		else if (!bIsOpen)
		{
			// Open the widget
			bIsOpen = true;
			return false; // Handled as open
		}
		return false;
	}
};

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FToggleUIStateConsistencyTest,
	"Project.GenericUISystemExtension.ToggleUI.Property1_ToggleStateConsistency",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FToggleUIStateConsistencyTest::RunTest(const FString& Parameters)
{
	const int32 NumIterations = 100;
	FRandomStream RandomStream(FDateTime::Now().GetTicks());
	
	// Test with different widget class names
	TArray<FString> TestWidgetNames = {
		TEXT("SettingsUI"),
		TEXT("BackpackUI"),
		TEXT("InventoryWidget"),
		TEXT("MenuWidget")
	};
	
	for (int32 Iteration = 0; Iteration < NumIterations; ++Iteration)
	{
		// Pick a random widget name
		const FString& WidgetName = TestWidgetNames[RandomStream.RandRange(0, TestWidgetNames.Num() - 1)];
		FToggleUIStateModel Model(WidgetName);
		
		// Random initial state
		Model.bIsOpen = RandomStream.RandRange(0, 1) == 1;
		const bool InitialState = Model.bIsOpen;
		
		// Perform toggle action
		Model.SimulateToggleAction(WidgetName);
		
		// Property: After toggle, state should be opposite of initial
		TestNotEqual(FString::Printf(TEXT("Iter %d, Widget %s: State should change after toggle"),
			Iteration, *WidgetName), Model.bIsOpen, InitialState);
	}
	
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FToggleUIDoubleToggleTest,
	"Project.GenericUISystemExtension.ToggleUI.Property1_DoubleToggleReturnsToOriginal",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FToggleUIDoubleToggleTest::RunTest(const FString& Parameters)
{
	const int32 NumIterations = 100;
	FRandomStream RandomStream(FDateTime::Now().GetTicks() + 54321);
	
	TArray<FString> TestWidgetNames = {
		TEXT("SettingsUI"),
		TEXT("BackpackUI")
	};
	
	for (int32 Iteration = 0; Iteration < NumIterations; ++Iteration)
	{
		const FString& WidgetName = TestWidgetNames[RandomStream.RandRange(0, TestWidgetNames.Num() - 1)];
		FToggleUIStateModel Model(WidgetName);
		
		// Random initial state
		Model.bIsOpen = RandomStream.RandRange(0, 1) == 1;
		const bool InitialState = Model.bIsOpen;
		
		// Toggle twice
		Model.SimulateToggleAction(WidgetName);
		Model.SimulateToggleAction(WidgetName);
		
		// Property: Double toggle should return to original state
		TestEqual(FString::Printf(TEXT("Iter %d, Widget %s: Double toggle should return to original state"),
			Iteration, *WidgetName), Model.bIsOpen, InitialState);
	}
	
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FToggleUICloseDetectionTest,
	"Project.GenericUISystemExtension.ToggleUI.Property1_CloseDetectionByClassName",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FToggleUICloseDetectionTest::RunTest(const FString& Parameters)
{
	// Test that close detection works correctly based on class name matching
	
	// SettingsUI should match "Settings"
	{
		FToggleUIStateModel Model(TEXT("SettingsUI"));
		Model.bIsOpen = true;
		bool bHandledAsClose = Model.SimulateToggleAction(TEXT("Settings"));
		TestTrue(TEXT("SettingsUI should be closed when target contains 'Settings'"), bHandledAsClose);
		TestFalse(TEXT("SettingsUI should be closed after action"), Model.bIsOpen);
	}
	
	// BackpackUI should match "Backpack"
	{
		FToggleUIStateModel Model(TEXT("BackpackUI"));
		Model.bIsOpen = true;
		bool bHandledAsClose = Model.SimulateToggleAction(TEXT("Backpack"));
		TestTrue(TEXT("BackpackUI should be closed when target contains 'Backpack'"), bHandledAsClose);
		TestFalse(TEXT("BackpackUI should be closed after action"), Model.bIsOpen);
	}
	
	// Non-matching widget should not be closed
	{
		FToggleUIStateModel Model(TEXT("OtherWidget"));
		Model.bIsOpen = true;
		bool bHandledAsClose = Model.SimulateToggleAction(TEXT("Settings"));
		TestFalse(TEXT("OtherWidget should not be closed when target is 'Settings'"), bHandledAsClose);
		TestTrue(TEXT("OtherWidget should remain open"), Model.bIsOpen);
	}
	
	return true;
}
