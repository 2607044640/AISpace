using UnrealBuildTool;

public class TwoLayerBackpackSystem : ModuleRules
{
	public TwoLayerBackpackSystem(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = ModuleRules.PCHUsageMode.UseExplicitOrSharedPCHs;
		PublicIncludePaths.AddRange(new string[] { });
		PrivateIncludePaths.AddRange(new string[] { });
		PublicDependencyModuleNames.AddRange(new string[]
		{
			"Core",
			"GenericUISystem",           // For UGUIS_ActivatableWidget and UI layer management
			"GenericUISystemExtension",  // For UGameActivatableWidgetExtension and UIStateSubsystem
			"GameplayTags"               // For FGameplayTag
		});
		PrivateDependencyModuleNames.AddRange(new string[]
		{
			"CoreUObject",
			"Engine",
			"Slate",
			"SlateCore",
			"UMG",
			"CommonUI",        // For UCommonActivatableWidget base
			"CommonInput"      // For input mode handling
		});
		DynamicallyLoadedModuleNames.AddRange(new string[] { });
	}
}
