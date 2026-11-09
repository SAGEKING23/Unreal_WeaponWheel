using UnrealBuildTool;

public class MyProject : ModuleRules
{
	public MyProject(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[] {
			"Core",
			"CoreUObject",
			"Engine",
			"InputCore",
			"EnhancedInput",
			"UMG",
			"Slate",
			"SlateCore",
			"GameplayTags",
			"GameplayAbilities",
			"GameplayTasks"
		});

		PrivateDependencyModuleNames.AddRange(new string[] {
			"AnimGraphRuntime",
			"AnimationModifiers",
			"SkeletalMesh",
			"PhysicsCore"
		});
	}
}