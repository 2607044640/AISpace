// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "Actions/GUIS_UIAction_ToggleUI.h"
#include "GameplayTagContainer.h"

PRAGMA_DISABLE_DEPRECATION_WARNINGS
static_assert(!UE_WITH_CONSTINIT_UOBJECT, "This generated code can only be compiled with !UE_WITH_CONSTINIT_OBJECT");
void EmptyLinkFunctionForGeneratedCodeGUIS_UIAction_ToggleUI() {}

// ********** Begin Cross Module References ********************************************************
GAMEPLAYTAGS_API UScriptStruct* Z_Construct_UScriptStruct_FGameplayTag();
GENERICUISYSTEM_API UClass* Z_Construct_UClass_UGUIS_UIAction();
GENERICUISYSTEMEXTENSION_API UClass* Z_Construct_UClass_UGUIS_UIAction_ToggleUI();
GENERICUISYSTEMEXTENSION_API UClass* Z_Construct_UClass_UGUIS_UIAction_ToggleUI_NoRegister();
UPackage* Z_Construct_UPackage__Script_GenericUISystemExtension();
// ********** End Cross Module References **********************************************************

// ********** Begin Class UGUIS_UIAction_ToggleUI **************************************************
FClassRegistrationInfo Z_Registration_Info_UClass_UGUIS_UIAction_ToggleUI;
UClass* UGUIS_UIAction_ToggleUI::GetPrivateStaticClass()
{
	using TClass = UGUIS_UIAction_ToggleUI;
	if (!Z_Registration_Info_UClass_UGUIS_UIAction_ToggleUI.InnerSingleton)
	{
		GetPrivateStaticClassBody(
			TClass::StaticPackage(),
			TEXT("GUIS_UIAction_ToggleUI"),
			Z_Registration_Info_UClass_UGUIS_UIAction_ToggleUI.InnerSingleton,
			StaticRegisterNativesUGUIS_UIAction_ToggleUI,
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
	return Z_Registration_Info_UClass_UGUIS_UIAction_ToggleUI.InnerSingleton;
}
UClass* Z_Construct_UClass_UGUIS_UIAction_ToggleUI_NoRegister()
{
	return UGUIS_UIAction_ToggleUI::GetPrivateStaticClass();
}
struct Z_Construct_UClass_UGUIS_UIAction_ToggleUI_Statics
{
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Class_MetaDataParams[] = {
		{ "BlueprintType", "true" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "/**\n * Abstract base class for UIActions that toggle UI widgets.\n * \n * Toggle logic:\n * - If current widget matches TargetWidgetClassNameContains: CLOSE it\n * - Otherwise: OPEN the target widget (subclass implements)\n * \n * Provides common logic for:\n * - Compatibility check (GameActivatableWidgetExtension)\n * - Layer priority check (via TargetLayerTag)\n * - Auto close detection (via TargetWidgetClassNameContains)\n * \n * Subclasses must:\n * 1. Call Super::InvokeActionInternal_Implementation first\n * 2. Check bHandledAsClose - if true, return immediately\n * 3. Otherwise perform the open logic\n * \n * Example subclasses:\n * - UGUIS_UIAction_OpenSettings (in JeffGame001)\n * - UGUIS_UIAction_OpenBackpack (in TwoLayerBackpackSystem)\n */" },
#endif
		{ "IncludePath", "Actions/GUIS_UIAction_ToggleUI.h" },
		{ "IsBlueprintBase", "true" },
		{ "ModuleRelativePath", "Public/Actions/GUIS_UIAction_ToggleUI.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Abstract base class for UIActions that toggle UI widgets.\n\nToggle logic:\n- If current widget matches TargetWidgetClassNameContains: CLOSE it\n- Otherwise: OPEN the target widget (subclass implements)\n\nProvides common logic for:\n- Compatibility check (GameActivatableWidgetExtension)\n- Layer priority check (via TargetLayerTag)\n- Auto close detection (via TargetWidgetClassNameContains)\n\nSubclasses must:\n1. Call Super::InvokeActionInternal_Implementation first\n2. Check bHandledAsClose - if true, return immediately\n3. Otherwise perform the open logic\n\nExample subclasses:\n- UGUIS_UIAction_OpenSettings (in JeffGame001)\n- UGUIS_UIAction_OpenBackpack (in TwoLayerBackpackSystem)" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_TargetWidgetClassNameContains_MetaData[] = {
		{ "Category", "UIAction|ToggleUI" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// Widget class name substring for toggle detection\n// e.g., \"SettingsUI\" - if current widget contains this, close it instead of open\n" },
#endif
		{ "ModuleRelativePath", "Public/Actions/GUIS_UIAction_ToggleUI.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Widget class name substring for toggle detection\ne.g., \"SettingsUI\" - if current widget contains this, close it instead of open" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_TargetLayerTag_MetaData[] = {
		{ "Category", "UIAction|ToggleUI" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// Target UI layer tag for priority check\n// e.g., \"GUIS.Layer.Menu\" or \"GUIS.Layer.GameMenu\"\n" },
#endif
		{ "ModuleRelativePath", "Public/Actions/GUIS_UIAction_ToggleUI.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Target UI layer tag for priority check\ne.g., \"GUIS.Layer.Menu\" or \"GUIS.Layer.GameMenu\"" },
#endif
	};
#endif // WITH_METADATA

// ********** Begin Class UGUIS_UIAction_ToggleUI constinit property declarations ******************
	static const UECodeGen_Private::FStrPropertyParams NewProp_TargetWidgetClassNameContains;
	static const UECodeGen_Private::FStructPropertyParams NewProp_TargetLayerTag;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
// ********** End Class UGUIS_UIAction_ToggleUI constinit property declarations ********************
	static UObject* (*const DependentSingletons[])();
	static constexpr FCppClassTypeInfoStatic StaticCppClassTypeInfo = {
		TCppClassTypeTraits<UGUIS_UIAction_ToggleUI>::IsAbstract,
	};
	static const UECodeGen_Private::FClassParams ClassParams;
}; // struct Z_Construct_UClass_UGUIS_UIAction_ToggleUI_Statics

// ********** Begin Class UGUIS_UIAction_ToggleUI Property Definitions *****************************
const UECodeGen_Private::FStrPropertyParams Z_Construct_UClass_UGUIS_UIAction_ToggleUI_Statics::NewProp_TargetWidgetClassNameContains = { "TargetWidgetClassNameContains", nullptr, (EPropertyFlags)0x0020080000010015, UECodeGen_Private::EPropertyGenFlags::Str, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UGUIS_UIAction_ToggleUI, TargetWidgetClassNameContains), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_TargetWidgetClassNameContains_MetaData), NewProp_TargetWidgetClassNameContains_MetaData) };
const UECodeGen_Private::FStructPropertyParams Z_Construct_UClass_UGUIS_UIAction_ToggleUI_Statics::NewProp_TargetLayerTag = { "TargetLayerTag", nullptr, (EPropertyFlags)0x0020080000010015, UECodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UGUIS_UIAction_ToggleUI, TargetLayerTag), Z_Construct_UScriptStruct_FGameplayTag, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_TargetLayerTag_MetaData), NewProp_TargetLayerTag_MetaData) }; // 517357616
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UClass_UGUIS_UIAction_ToggleUI_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UGUIS_UIAction_ToggleUI_Statics::NewProp_TargetWidgetClassNameContains,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UGUIS_UIAction_ToggleUI_Statics::NewProp_TargetLayerTag,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_UGUIS_UIAction_ToggleUI_Statics::PropPointers) < 2048);
// ********** End Class UGUIS_UIAction_ToggleUI Property Definitions *******************************
UObject* (*const Z_Construct_UClass_UGUIS_UIAction_ToggleUI_Statics::DependentSingletons[])() = {
	(UObject* (*)())Z_Construct_UClass_UGUIS_UIAction,
	(UObject* (*)())Z_Construct_UPackage__Script_GenericUISystemExtension,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_UGUIS_UIAction_ToggleUI_Statics::DependentSingletons) < 16);
const UECodeGen_Private::FClassParams Z_Construct_UClass_UGUIS_UIAction_ToggleUI_Statics::ClassParams = {
	&UGUIS_UIAction_ToggleUI::StaticClass,
	nullptr,
	&StaticCppClassTypeInfo,
	DependentSingletons,
	nullptr,
	Z_Construct_UClass_UGUIS_UIAction_ToggleUI_Statics::PropPointers,
	nullptr,
	UE_ARRAY_COUNT(DependentSingletons),
	0,
	UE_ARRAY_COUNT(Z_Construct_UClass_UGUIS_UIAction_ToggleUI_Statics::PropPointers),
	0,
	0x003130A1u,
	METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UClass_UGUIS_UIAction_ToggleUI_Statics::Class_MetaDataParams), Z_Construct_UClass_UGUIS_UIAction_ToggleUI_Statics::Class_MetaDataParams)
};
void UGUIS_UIAction_ToggleUI::StaticRegisterNativesUGUIS_UIAction_ToggleUI()
{
}
UClass* Z_Construct_UClass_UGUIS_UIAction_ToggleUI()
{
	if (!Z_Registration_Info_UClass_UGUIS_UIAction_ToggleUI.OuterSingleton)
	{
		UECodeGen_Private::ConstructUClass(Z_Registration_Info_UClass_UGUIS_UIAction_ToggleUI.OuterSingleton, Z_Construct_UClass_UGUIS_UIAction_ToggleUI_Statics::ClassParams);
	}
	return Z_Registration_Info_UClass_UGUIS_UIAction_ToggleUI.OuterSingleton;
}
DEFINE_VTABLE_PTR_HELPER_CTOR_NS(, UGUIS_UIAction_ToggleUI);
UGUIS_UIAction_ToggleUI::~UGUIS_UIAction_ToggleUI() {}
// ********** End Class UGUIS_UIAction_ToggleUI ****************************************************

// ********** Begin Registration *******************************************************************
struct Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Actions_GUIS_UIAction_ToggleUI_h__Script_GenericUISystemExtension_Statics
{
	static constexpr FClassRegisterCompiledInInfo ClassInfo[] = {
		{ Z_Construct_UClass_UGUIS_UIAction_ToggleUI, UGUIS_UIAction_ToggleUI::StaticClass, TEXT("UGUIS_UIAction_ToggleUI"), &Z_Registration_Info_UClass_UGUIS_UIAction_ToggleUI, CONSTRUCT_RELOAD_VERSION_INFO(FClassReloadVersionInfo, sizeof(UGUIS_UIAction_ToggleUI), 3858632705U) },
	};
}; // Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Actions_GUIS_UIAction_ToggleUI_h__Script_GenericUISystemExtension_Statics 
static FRegisterCompiledInInfo Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Actions_GUIS_UIAction_ToggleUI_h__Script_GenericUISystemExtension_766804476{
	TEXT("/Script/GenericUISystemExtension"),
	Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Actions_GUIS_UIAction_ToggleUI_h__Script_GenericUISystemExtension_Statics::ClassInfo, UE_ARRAY_COUNT(Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Actions_GUIS_UIAction_ToggleUI_h__Script_GenericUISystemExtension_Statics::ClassInfo),
	nullptr, 0,
	nullptr, 0,
};
// ********** End Registration *********************************************************************

PRAGMA_ENABLE_DEPRECATION_WARNINGS
