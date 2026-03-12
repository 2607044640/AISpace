// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "BackpackWidget.h"

PRAGMA_DISABLE_DEPRECATION_WARNINGS
static_assert(!UE_WITH_CONSTINIT_UOBJECT, "This generated code can only be compiled with !UE_WITH_CONSTINIT_OBJECT");
void EmptyLinkFunctionForGeneratedCodeBackpackWidget() {}

// ********** Begin Cross Module References ********************************************************
GENERICUISYSTEMEXTENSION_API UClass* Z_Construct_UClass_UGameActivatableWidgetExtension();
TWOLAYERBACKPACKSYSTEM_API UClass* Z_Construct_UClass_UBackpackWidget();
TWOLAYERBACKPACKSYSTEM_API UClass* Z_Construct_UClass_UBackpackWidget_NoRegister();
UPackage* Z_Construct_UPackage__Script_TwoLayerBackpackSystem();
// ********** End Cross Module References **********************************************************

// ********** Begin Class UBackpackWidget **********************************************************
FClassRegistrationInfo Z_Registration_Info_UClass_UBackpackWidget;
UClass* UBackpackWidget::GetPrivateStaticClass()
{
	using TClass = UBackpackWidget;
	if (!Z_Registration_Info_UClass_UBackpackWidget.InnerSingleton)
	{
		GetPrivateStaticClassBody(
			TClass::StaticPackage(),
			TEXT("BackpackWidget"),
			Z_Registration_Info_UClass_UBackpackWidget.InnerSingleton,
			StaticRegisterNativesUBackpackWidget,
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
	return Z_Registration_Info_UClass_UBackpackWidget.InnerSingleton;
}
UClass* Z_Construct_UClass_UBackpackWidget_NoRegister()
{
	return UBackpackWidget::GetPrivateStaticClass();
}
struct Z_Construct_UClass_UBackpackWidget_Statics
{
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Class_MetaDataParams[] = {
		{ "BlueprintType", "true" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "/**\n * Base widget for backpack/inventory UI.\n * \n * Features:\n * - Inherits from UGUIS_ActivatableWidget for CommonUI integration\n * - Automatically switches to Menu input mode when activated\n * - Pauses game (TimeDilation = 0) when activated\n * - Resumes game when deactivated\n * \n * Usage:\n * 1. Create a Blueprint widget inheriting from this class\n * 2. Design your backpack UI in the Blueprint\n * 3. Use UGUIS_GameUIFunctionLibrary::PushContentToUILayer_ForPlayer() to show\n * 4. Use UGUIS_GameUIFunctionLibrary::PopContentFromUILayer() to hide\n */" },
#endif
		{ "IncludePath", "BackpackWidget.h" },
		{ "IsBlueprintBase", "true" },
		{ "ModuleRelativePath", "Public/BackpackWidget.h" },
		{ "ObjectInitializerConstructorDeclared", "" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Base widget for backpack/inventory UI.\n\nFeatures:\n- Inherits from UGUIS_ActivatableWidget for CommonUI integration\n- Automatically switches to Menu input mode when activated\n- Pauses game (TimeDilation = 0) when activated\n- Resumes game when deactivated\n\nUsage:\n1. Create a Blueprint widget inheriting from this class\n2. Design your backpack UI in the Blueprint\n3. Use UGUIS_GameUIFunctionLibrary::PushContentToUILayer_ForPlayer() to show\n4. Use UGUIS_GameUIFunctionLibrary::PopContentFromUILayer() to hide" },
#endif
	};
#endif // WITH_METADATA

// ********** Begin Class UBackpackWidget constinit property declarations **************************
// ********** End Class UBackpackWidget constinit property declarations ****************************
	static UObject* (*const DependentSingletons[])();
	static constexpr FCppClassTypeInfoStatic StaticCppClassTypeInfo = {
		TCppClassTypeTraits<UBackpackWidget>::IsAbstract,
	};
	static const UECodeGen_Private::FClassParams ClassParams;
}; // struct Z_Construct_UClass_UBackpackWidget_Statics
UObject* (*const Z_Construct_UClass_UBackpackWidget_Statics::DependentSingletons[])() = {
	(UObject* (*)())Z_Construct_UClass_UGameActivatableWidgetExtension,
	(UObject* (*)())Z_Construct_UPackage__Script_TwoLayerBackpackSystem,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_UBackpackWidget_Statics::DependentSingletons) < 16);
const UECodeGen_Private::FClassParams Z_Construct_UClass_UBackpackWidget_Statics::ClassParams = {
	&UBackpackWidget::StaticClass,
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
	0x00B010A1u,
	METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UClass_UBackpackWidget_Statics::Class_MetaDataParams), Z_Construct_UClass_UBackpackWidget_Statics::Class_MetaDataParams)
};
void UBackpackWidget::StaticRegisterNativesUBackpackWidget()
{
}
UClass* Z_Construct_UClass_UBackpackWidget()
{
	if (!Z_Registration_Info_UClass_UBackpackWidget.OuterSingleton)
	{
		UECodeGen_Private::ConstructUClass(Z_Registration_Info_UClass_UBackpackWidget.OuterSingleton, Z_Construct_UClass_UBackpackWidget_Statics::ClassParams);
	}
	return Z_Registration_Info_UClass_UBackpackWidget.OuterSingleton;
}
DEFINE_VTABLE_PTR_HELPER_CTOR_NS(, UBackpackWidget);
UBackpackWidget::~UBackpackWidget() {}
// ********** End Class UBackpackWidget ************************************************************

// ********** Begin Registration *******************************************************************
struct Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_TwoLayerBackpackSystem_Source_TwoLayerBackpackSystem_Public_BackpackWidget_h__Script_TwoLayerBackpackSystem_Statics
{
	static constexpr FClassRegisterCompiledInInfo ClassInfo[] = {
		{ Z_Construct_UClass_UBackpackWidget, UBackpackWidget::StaticClass, TEXT("UBackpackWidget"), &Z_Registration_Info_UClass_UBackpackWidget, CONSTRUCT_RELOAD_VERSION_INFO(FClassReloadVersionInfo, sizeof(UBackpackWidget), 376397781U) },
	};
}; // Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_TwoLayerBackpackSystem_Source_TwoLayerBackpackSystem_Public_BackpackWidget_h__Script_TwoLayerBackpackSystem_Statics 
static FRegisterCompiledInInfo Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_TwoLayerBackpackSystem_Source_TwoLayerBackpackSystem_Public_BackpackWidget_h__Script_TwoLayerBackpackSystem_779216254{
	TEXT("/Script/TwoLayerBackpackSystem"),
	Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_TwoLayerBackpackSystem_Source_TwoLayerBackpackSystem_Public_BackpackWidget_h__Script_TwoLayerBackpackSystem_Statics::ClassInfo, UE_ARRAY_COUNT(Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_TwoLayerBackpackSystem_Source_TwoLayerBackpackSystem_Public_BackpackWidget_h__Script_TwoLayerBackpackSystem_Statics::ClassInfo),
	nullptr, 0,
	nullptr, 0,
};
// ********** End Registration *********************************************************************

PRAGMA_ENABLE_DEPRECATION_WARNINGS
