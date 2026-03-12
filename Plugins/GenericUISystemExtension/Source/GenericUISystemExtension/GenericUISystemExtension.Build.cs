// GenericUISystemExtension.Build.cs

using UnrealBuildTool;

public class GenericUISystemExtension : ModuleRules
{
	public GenericUISystemExtension(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[]
		{
			"Core",
			"CoreUObject",
			"Engine",
			"UMG",
			"Slate",
			"SlateCore",
			"CommonUI",
			"GameplayTags",
			"GenericUISystem",
			"EnhancedInput",
			"InputCore"
		});

		PrivateDependencyModuleNames.AddRange(new string[]
		{
		});
	}
}
