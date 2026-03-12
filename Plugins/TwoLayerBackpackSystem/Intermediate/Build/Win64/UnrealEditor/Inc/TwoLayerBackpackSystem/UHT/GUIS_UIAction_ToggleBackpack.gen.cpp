// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "Actions/GUIS_UIAction_ToggleBackpack.h"

PRAGMA_DISABLE_DEPRECATION_WARNINGS
static_assert(!UE_WITH_CONSTINIT_UOBJECT, "This generated code can only be compiled with !UE_WITH_CONSTINIT_OBJECT");
void EmptyLinkFunctionForGeneratedCodeGUIS_UIAction_ToggleBackpack() {}

// ********** Begin Cross Module References ********************************************************
GENERICUISYSTEMEXTENSION_API UClass* Z_Construct_UClass_UGUIS_UIAction_ToggleUI();
TWOLAYERBACKPACKSYSTEM_API UClass* Z_Construct_UClass_UGUIS_UIAction_ToggleBackpack();
TWOLAYERBACKPACKSYSTEM_API UClass* Z_Construct_UClass_UGUIS_UIAction_ToggleBackpack_NoRegister();
UPackage* Z_Construct_UPackage__Script_TwoLayerBackpackSystem();
// ********** End Cross Module References **********************************************************

// ********** Begin Class UGUIS_UIAction_ToggleBackpack ********************************************
FClassRegistrationInfo Z_Registration_Info_UClass_UGUIS_UIAction_ToggleBackpack;
UClass* UGUIS_UIAction_ToggleBackpack::GetPrivateStaticClass()
{
	using TClass = UGUIS_UIAction_ToggleBackpack;
	if (!Z_Registration_Info_UClass_UGUIS_UIAction_ToggleBackpack.InnerSingleton)
	{
		GetPrivateStaticClassBody(
			TClass::StaticPackage(),
			TEXT("GUIS_UIAction_ToggleBackpack"),
			Z_Registration_Info_UClass_UGUIS_UIAction_ToggleBackpack.InnerSingleton,
			StaticRegisterNativesUGUIS_UIAction_ToggleBackpack,
			sizeof(TClass),
			alignof(TClass),
			TClass::StaticClassFlags,
			TClass::StaticClassCastFlags(),
			TClass::StaticConfigName(),
			(UClass::ClassConstructorType)InternalConstructor<TClass>,
			(UClass::ClassVTableHelperCtorCallerType)InternalVTableHelperCtorCaller<TClass>,
			UOBJECT_CPPCLASS_STATICFUNCTIONS_FORCLASS(TClass),
			&TClass::Super::StaticClass,
			&TClass::WithinClass::StaticClass
		);
	}
	return Z_Registration_Info_UClass_UGUIS_UIAction_ToggleBackpack.InnerSingleton;
}
UClass* Z_Construct_UClass_UGUIS_UIAction_ToggleBackpack_NoRegister()
{
	return UGUIS_UIAction_ToggleBackpack::GetPrivateStaticClass();
}
struct Z_Construct_UClass_UGUIS_UIAction_ToggleBackpack_Statics
{
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Class_MetaDataParams[] = {
		{ "BlueprintType", "true" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "/**\n * UIAction that toggles the Backpack inventory.\n * \n * Inherits layer priority check and toggle logic from UGUIS_UIAction_ToggleUI.\n * Uses reflection to call OpenBackpackInventory() on BackpackInventoryComponent.\n */" },
#endif
		{ "DisplayName", "Toggle Backpack Action" },
		{ "IncludePath", "Actions/GUIS_UIAction_ToggleBackpack.h" },
		{ "IsBlueprintBase", "true" },
		{ "ModuleRelativePath", "Public/Actions/GUIS_UIAction_ToggleBackpack.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "UIAction that toggles the Backpack inventory.\n\nInherits layer priority check and toggle logic from UGUIS_UIAction_ToggleUI.\nUses reflection to call OpenBackpackInventory() on BackpackInventoryComponent." },
#endif
	};
#endif // WITH_METADATA

// ********** Begin Class UGUIS_UIAction_ToggleBackpack constinit property declarations ************
// ********** End Class UGUIS_UIAction_ToggleBackpack constinit property declarations **************
	static UObject* (*const DependentSingletons[])();
	static constexpr FCppClassTypeInfoStatic StaticCppClassTypeInfo = {
		TCppClassTypeTraits<UGUIS_UIAction_ToggleBackpack>::IsAbstract,
	};
	static const UECodeGen_Private::FClassParams ClassParams;
}; // struct Z_Construct_UClass_UGUIS_UIAction_ToggleBackpack_Statics
UObject* (*const Z_Construct_UClass_UGUIS_UIAction_ToggleBackpack_Statics::DependentSingletons[])() = {
	(UObject* (*)())Z_Construct_UClass_UGUIS_UIAction_ToggleUI,
	(UObject* (*)())Z_Construct_UPackage__Script_TwoLayerBackpackSystem,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_UGUIS_UIAction_ToggleBackpack_Statics::DependentSingletons) < 16);
const UECodeGen_Private::FClassParams Z_Construct_UClass_UGUIS_UIAction_ToggleBackpack_Statics::ClassParams = {
	&UGUIS_UIAction_ToggleBackpack::StaticClass,
	nullptr,
	&StaticCppClassTypeInfo,
	DependentSingletons,
	nullptr,
	nullptr,
	nullptr,
	UE_ARRAY_COUNT(DependentSingletons),
	0,
	0,
	0,
	0x003130A0u,
	METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UClass_UGUIS_UIAction_ToggleBackpack_Statics::Class_MetaDataParams), Z_Construct_UClass_UGUIS_UIAction_ToggleBackpack_Statics::Class_MetaDataParams)
};
void UGUIS_UIAction_ToggleBackpack::StaticRegisterNativesUGUIS_UIAction_ToggleBackpack()
{
}
UClass* Z_Construct_UClass_UGUIS_UIAction_ToggleBackpack()
{
	if (!Z_Registration_Info_UClass_UGUIS_UIAction_ToggleBackpack.OuterSingleton)
	{
		UECodeGen_Private::ConstructUClass(Z_Registration_Info_UClass_UGUIS_UIAction_ToggleBackpack.OuterSingleton, Z_Construct_UClass_UGUIS_UIAction_ToggleBackpack_Statics::ClassParams);
	}
	return Z_Registration_Info_UClass_UGUIS_UIAction_ToggleBackpack.OuterSingleton;
}
DEFINE_VTABLE_PTR_HELPER_CTOR_NS(, UGUIS_UIAction_ToggleBackpack);
UGUIS_UIAction_ToggleBackpack::~UGUIS_UIAction_ToggleBackpack() {}
// ********** End Class UGUIS_UIAction_ToggleBackpack **********************************************

// ********** Begin Registration *******************************************************************
struct Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_TwoLayerBackpackSystem_Source_TwoLayerBackpackSystem_Public_Actions_GUIS_UIAction_ToggleBackpack_h__Script_TwoLayerBackpackSystem_Statics
{
	static constexpr FClassRegisterCompiledInInfo ClassInfo[] = {
		{ Z_Construct_UClass_UGUIS_UIAction_ToggleBackpack, UGUIS_UIAction_ToggleBackpack::StaticClass, TEXT("UGUIS_UIAction_ToggleBackpack"), &Z_Registration_Info_UClass_UGUIS_UIAction_ToggleBackpack, CONSTRUCT_RELOAD_VERSION_INFO(FClassReloadVersionInfo, sizeof(UGUIS_UIAction_ToggleBackpack), 2409527249U) },
	};
}; // Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_TwoLayerBackpackSystem_Source_TwoLayerBackpackSystem_Public_Actions_GUIS_UIAction_ToggleBackpack_h__Script_TwoLayerBackpackSystem_Statics 
static FRegisterCompiledInInfo Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_TwoLayerBackpackSystem_Source_TwoLayerBackpackSystem_Public_Actions_GUIS_UIAction_ToggleBackpack_h__Script_TwoLayerBackpackSystem_907955116{
	TEXT("/Script/TwoLayerBackpackSystem"),
	Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_TwoLayerBackpackSystem_Source_TwoLayerBackpackSystem_Public_Actions_GUIS_UIAction_ToggleBackpack_h__Script_TwoLayerBackpackSystem_Statics::ClassInfo, UE_ARRAY_COUNT(Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_TwoLayerBackpackSystem_Source_TwoLayerBackpackSystem_Public_Actions_GUIS_UIAction_ToggleBackpack_h__Script_TwoLayerBackpackSystem_Statics::ClassInfo),
	nullptr, 0,
	nullptr, 0,
};
// ********** End Registration *********************************************************************

PRAGMA_ENABLE_DEPRECATION_WARNINGS
