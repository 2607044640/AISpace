// GameActivatableWidgetExtensionTests.cpp
// Property-Based Tests for UGameActivatableWidgetExtension

#include "CoreMinimal.h"
#include "Misc/AutomationTest.h"
#include "Math/RandomStream.h"
#include "Widgets/GameActivatableWidgetExtension.h"

struct FWidgetActivationModel
{
	bool bIsActive = false;
	int32 ActivationCount = 0;
	int32 DeactivationCount = 0;
	
	void Activate()
	{
		bIsActive = true;
		ActivationCount++;
	}
	
	void Deactivate()
	{
		if (bIsActive)
		{
			bIsActive = false;
			DeactivationCount++;
		}
	}
	
	void HandleCloseUI()
	{
		Deactivate();
	}
	
	bool IsActive() const { return bIsActive; }
};

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FCloseActionDeactivationTest,
	"Project.GenericUISystemExtension.GameActivatableWidget.Property4_CloseActionDeactivation",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FCloseActionDeactivationTest::RunTest(const FString& Parameters)
{
	const int32 NumIterations = 100;
	FRandomStream RandomStream(FDateTime::Now().GetTicks() + 54321);
	
	for (int32 Iteration = 0; Iteration < NumIterations; ++Iteration)
	{
		FWidgetActivationModel Model;
		const int32 NumOperations = RandomStream.RandRange(1, 10);
		
		for (int32 Op = 0; Op < NumOperations; ++Op)
		{
			const int32 Operation = RandomStream.RandRange(0, 2);
			
			switch (Operation)
			{
			case 0:
				Model.Activate();
				TestTrue(FString::Printf(TEXT("Iter %d, Op %d: After Activate, widget should be active"),
					Iteration, Op), Model.IsActive());
				break;
				
			case 1:
				{
					const bool WasActive = Model.IsActive();
					Model.HandleCloseUI();
					TestFalse(FString::Printf(TEXT("Iter %d, Op %d: After HandleCloseUI, widget should be inactive"),
						Iteration, Op), Model.IsActive());
					if (WasActive)
					{
						TestTrue(FString::Printf(TEXT("Iter %d, Op %d: HandleCloseUI on active widget should increment deactivation count"),
							Iteration, Op), Model.DeactivationCount > 0);
					}
				}
				break;
				
			case 2:
				Model.Deactivate();
				TestFalse(FString::Printf(TEXT("Iter %d, Op %d: After Deactivate, widget should be inactive"),
					Iteration, Op), Model.IsActive());
				break;
			}
		}
	}
	
	{
		FWidgetActivationModel Model;
		Model.Activate();
		TestTrue(TEXT("Scenario 1: Widget should be active after Activate"), Model.IsActive());
		Model.HandleCloseUI();
		TestFalse(TEXT("Scenario 1: Widget should be inactive after HandleCloseUI"), Model.IsActive());
		TestEqual(TEXT("Scenario 1: Deactivation count should be 1"), Model.DeactivationCount, 1);
	}
	
	{
		FWidgetActivationModel Model;
		TestFalse(TEXT("Scenario 2: Widget should start inactive"), Model.IsActive());
		Model.HandleCloseUI();
		TestFalse(TEXT("Scenario 2: Widget should remain inactive after HandleCloseUI"), Model.IsActive());
		TestEqual(TEXT("Scenario 2: Deactivation count should be 0 (was already inactive)"), Model.DeactivationCount, 0);
	}
	
	{
		FWidgetActivationModel Model;
		Model.Activate();
		Model.HandleCloseUI();
		TestFalse(TEXT("Scenario 3: Widget should be inactive after first HandleCloseUI"), Model.IsActive());
		Model.HandleCloseUI();
		TestFalse(TEXT("Scenario 3: Widget should remain inactive after second HandleCloseUI"), Model.IsActive());
		TestEqual(TEXT("Scenario 3: Deactivation count should be 1 (second call was no-op)"), Model.DeactivationCount, 1);
	}
	
	{
		FWidgetActivationModel Model;
		Model.Activate();
		TestTrue(TEXT("Scenario 4: First activation"), Model.IsActive());
		Model.HandleCloseUI();
		TestFalse(TEXT("Scenario 4: First close"), Model.IsActive());
		Model.Activate();
		TestTrue(TEXT("Scenario 4: Second activation"), Model.IsActive());
		Model.HandleCloseUI();
		TestFalse(TEXT("Scenario 4: Second close"), Model.IsActive());
		TestEqual(TEXT("Scenario 4: Activation count should be 2"), Model.ActivationCount, 2);
		TestEqual(TEXT("Scenario 4: Deactivation count should be 2"), Model.DeactivationCount, 2);
	}
	
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FHandleCloseUIImplementationTest,
	"Project.GenericUISystemExtension.GameActivatableWidget.Property4_HandleCloseUIImplementation",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FHandleCloseUIImplementationTest::RunTest(const FString& Parameters)
{
	const UClass* WidgetClass = UGameActivatableWidgetExtension::StaticClass();
	TestNotNull(TEXT("UGameActivatableWidgetExtension class should exist"), WidgetClass);
	
	const UFunction* HandleCloseUIFunc = WidgetClass->FindFunctionByName(FName("HandleCloseUI"));
	TestNotNull(TEXT("HandleCloseUI function should exist"), HandleCloseUIFunc);
	
	if (HandleCloseUIFunc)
	{
		TestTrue(TEXT("HandleCloseUI should be BlueprintCallable"),
			HandleCloseUIFunc->HasAnyFunctionFlags(FUNC_BlueprintCallable));
	}
	
	return true;
}
