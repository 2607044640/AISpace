// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "Actions/GUIS_UIAction_CloseUI.h"

PRAGMA_DISABLE_DEPRECATION_WARNINGS
static_assert(!UE_WITH_CONSTINIT_UOBJECT, "This generated code can only be compiled with !UE_WITH_CONSTINIT_OBJECT");
void EmptyLinkFunctionForGeneratedCodeGUIS_UIAction_CloseUI() {}

// ********** Begin Cross Module References ********************************************************
GENERICUISYSTEM_API UClass* Z_Construct_UClass_UGUIS_UIAction();
GENERICUISYSTEMEXTENSION_API UClass* Z_Construct_UClass_UGUIS_UIAction_CloseUI();
GENERICUISYSTEMEXTENSION_API UClass* Z_Construct_UClass_UGUIS_UIAction_CloseUI_NoRegister();
UPackage* Z_Construct_UPackage__Script_GenericUISystemExtension();
// ********** End Cross Module References **********************************************************

// ********** Begin Class UGUIS_UIAction_CloseUI ***************************************************
FClassRegistrationInfo Z_Registration_Info_UClass_UGUIS_UIAction_CloseUI;
UClass* UGUIS_UIAction_CloseUI::GetPrivateStaticClass()
{
	using TClass = UGUIS_UIAction_CloseUI;
	if (!Z_Registration_Info_UClass_UGUIS_UIAction_CloseUI.InnerSingleton)
	{
		GetPrivateStaticClassBody(
			TClass::StaticPackage(),
			TEXT("GUIS_UIAction_CloseUI"),
			Z_Registration_Info_UClass_UGUIS_UIAction_CloseUI.InnerSingleton,
			StaticRegisterNativesUGUIS_UIAction_CloseUI,
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
	return Z_Registration_Info_UClass_UGUIS_UIAction_CloseUI.InnerSingleton;
}
UClass* Z_Construct_UClass_UGUIS_UIAction_CloseUI_NoRegister()
{
	return UGUIS_UIAction_CloseUI::GetPrivateStaticClass();
}
struct Z_Construct_UClass_UGUIS_UIAction_CloseUI_Statics
{
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Class_MetaDataParams[] = {
		{ "BlueprintType", "true" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "/**\n * UIAction that closes the associated widget.\n * \n * Usage:\n * 1. Create a UGUIS_UIActionFactory DataAsset with this action\n * 2. Add UGUIS_UIActionWidget to your widget Blueprint\n * 3. Set ActionFactory on the UIActionWidget\n * 4. OnActivated: SetAssociatedData(self), then RegisterActions()\n * 5. OnDeactivated: UnregisterActions()\n * \n * When the bound input is triggered, this action will call HandleCloseUI()\n * on the associated widget, which deactivates it.\n */" },
#endif
		{ "DisplayName", "Close UI Action" },
		{ "IncludePath", "Actions/GUIS_UIAction_CloseUI.h" },
		{ "IsBlueprintBase", "true" },
		{ "ModuleRelativePath", "Public/Actions/GUIS_UIAction_CloseUI.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "UIAction that closes the associated widget.\n\nUsage:\n1. Create a UGUIS_UIActionFactory DataAsset with this action\n2. Add UGUIS_UIActionWidget to your widget Blueprint\n3. Set ActionFactory on the UIActionWidget\n4. OnActivated: SetAssociatedData(self), then RegisterActions()\n5. OnDeactivated: UnregisterActions()\n\nWhen the bound input is triggered, this action will call HandleCloseUI()\non the associated widget, which deactivates it." },
#endif
	};
#endif // WITH_METADATA

// ********** Begin Class UGUIS_UIAction_CloseUI constinit property declarations *******************
// ********** End Class UGUIS_UIAction_CloseUI constinit property declarations *********************
	static UObject* (*const DependentSingletons[])();
	static constexpr FCppClassTypeInfoStatic StaticCppClassTypeInfo = {
		TCppClassTypeTraits<UGUIS_UIAction_CloseUI>::IsAbstract,
	};
	static const UECodeGen_Private::FClassParams ClassParams;
}; // struct Z_Construct_UClass_UGUIS_UIAction_CloseUI_Statics
UObject* (*const Z_Construct_UClass_UGUIS_UIAction_CloseUI_Statics::DependentSingletons[])() = {
	(UObject* (*)())Z_Construct_UClass_UGUIS_UIAction,
	(UObject* (*)())Z_Construct_UPackage__Script_GenericUISystemExtension,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_UGUIS_UIAction_CloseUI_Statics::DependentSingletons) < 16);
const UECodeGen_Private::FClassParams Z_Construct_UClass_UGUIS_UIAction_CloseUI_Statics::ClassParams = {
	&UGUIS_UIAction_CloseUI::StaticClass,
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
	METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UClass_UGUIS_UIAction_CloseUI_Statics::Class_MetaDataParams), Z_Construct_UClass_UGUIS_UIAction_CloseUI_Statics::Class_MetaDataParams)
};
void UGUIS_UIAction_CloseUI::StaticRegisterNativesUGUIS_UIAction_CloseUI()
{
}
UClass* Z_Construct_UClass_UGUIS_UIAction_CloseUI()
{
	if (!Z_Registration_Info_UClass_UGUIS_UIAction_CloseUI.OuterSingleton)
	{
		UECodeGen_Private::ConstructUClass(Z_Registration_Info_UClass_UGUIS_UIAction_CloseUI.OuterSingleton, Z_Construct_UClass_UGUIS_UIAction_CloseUI_Statics::ClassParams);
	}
	return Z_Registration_Info_UClass_UGUIS_UIAction_CloseUI.OuterSingleton;
}
DEFINE_VTABLE_PTR_HELPER_CTOR_NS(, UGUIS_UIAction_CloseUI);
UGUIS_UIAction_CloseUI::~UGUIS_UIAction_CloseUI() {}
// ********** End Class UGUIS_UIAction_CloseUI *****************************************************

// ********** Begin Registration *******************************************************************
struct Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Actions_GUIS_UIAction_CloseUI_h__Script_GenericUISystemExtension_Statics
{
	static constexpr FClassRegisterCompiledInInfo ClassInfo[] = {
		{ Z_Construct_UClass_UGUIS_UIAction_CloseUI, UGUIS_UIAction_CloseUI::StaticClass, TEXT("UGUIS_UIAction_CloseUI"), &Z_Registration_Info_UClass_UGUIS_UIAction_CloseUI, CONSTRUCT_RELOAD_VERSION_INFO(FClassReloadVersionInfo, sizeof(UGUIS_UIAction_CloseUI), 1525103506U) },
	};
}; // Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Actions_GUIS_UIAction_CloseUI_h__Script_GenericUISystemExtension_Statics 
static FRegisterCompiledInInfo Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Actions_GUIS_UIAction_CloseUI_h__Script_GenericUISystemExtension_623314064{
	TEXT("/Script/GenericUISystemExtension"),
	Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Actions_GUIS_UIAction_CloseUI_h__Script_GenericUISystemExtension_Statics::ClassInfo, UE_ARRAY_COUNT(Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Actions_GUIS_UIAction_CloseUI_h__Script_GenericUISystemExtension_Statics::ClassInfo),
	nullptr, 0,
	nullptr, 0,
};
// ********** End Registration *********************************************************************

PRAGMA_ENABLE_DEPRECATION_WARNINGS
