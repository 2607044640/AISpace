// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "Widgets/GameUILayoutExtension.h"

PRAGMA_DISABLE_DEPRECATION_WARNINGS
static_assert(!UE_WITH_CONSTINIT_UOBJECT, "This generated code can only be compiled with !UE_WITH_CONSTINIT_OBJECT");
void EmptyLinkFunctionForGeneratedCodeGameUILayoutExtension() {}

// ********** Begin Cross Module References ********************************************************
COMMONUI_API UClass* Z_Construct_UClass_UCommonActivatableWidgetContainerBase_NoRegister();
GENERICUISYSTEM_API UClass* Z_Construct_UClass_UGUIS_GameUILayout();
GENERICUISYSTEMEXTENSION_API UClass* Z_Construct_UClass_UGameUILayoutExtension();
GENERICUISYSTEMEXTENSION_API UClass* Z_Construct_UClass_UGameUILayoutExtension_NoRegister();
UPackage* Z_Construct_UPackage__Script_GenericUISystemExtension();
// ********** End Cross Module References **********************************************************

// ********** Begin Class UGameUILayoutExtension ***************************************************
FClassRegistrationInfo Z_Registration_Info_UClass_UGameUILayoutExtension;
UClass* UGameUILayoutExtension::GetPrivateStaticClass()
{
	using TClass = UGameUILayoutExtension;
	if (!Z_Registration_Info_UClass_UGameUILayoutExtension.InnerSingleton)
	{
		GetPrivateStaticClassBody(
			TClass::StaticPackage(),
			TEXT("GameUILayoutExtension"),
			Z_Registration_Info_UClass_UGameUILayoutExtension.InnerSingleton,
			StaticRegisterNativesUGameUILayoutExtension,
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
	return Z_Registration_Info_UClass_UGameUILayoutExtension.InnerSingleton;
}
UClass* Z_Construct_UClass_UGameUILayoutExtension_NoRegister()
{
	return UGameUILayoutExtension::GetPrivateStaticClass();
}
struct Z_Construct_UClass_UGameUILayoutExtension_Statics
{
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Class_MetaDataParams[] = {
		{ "BlueprintType", "true" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "/**\n * C++ base class for the game UI layout widget.\n * Provides BindWidget properties for the 4 standard UI layer stacks.\n * \n * Usage:\n * 1. Create a Blueprint widget inheriting from this class\n * 2. Add 4 CommonActivatableWidgetStack widgets named:\n *    - GameLayer_Stack\n *    - GameMenu_Stack\n *    - Menu_Stack\n *    - Modal_Stack\n * 3. The layers are automatically registered in NativeConstruct\n */" },
#endif
		{ "IncludePath", "Widgets/GameUILayoutExtension.h" },
		{ "IsBlueprintBase", "true" },
		{ "ModuleRelativePath", "Public/Widgets/GameUILayoutExtension.h" },
		{ "ObjectInitializerConstructorDeclared", "" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "C++ base class for the game UI layout widget.\nProvides BindWidget properties for the 4 standard UI layer stacks.\n\nUsage:\n1. Create a Blueprint widget inheriting from this class\n2. Add 4 CommonActivatableWidgetStack widgets named:\n   - GameLayer_Stack\n   - GameMenu_Stack\n   - Menu_Stack\n   - Modal_Stack\n3. The layers are automatically registered in NativeConstruct" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_GameLayer_Stack_MetaData[] = {
		{ "BindWidget", "" },
		{ "EditInline", "true" },
		{ "ModuleRelativePath", "Public/Widgets/GameUILayoutExtension.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_GameMenu_Stack_MetaData[] = {
		{ "BindWidget", "" },
		{ "EditInline", "true" },
		{ "ModuleRelativePath", "Public/Widgets/GameUILayoutExtension.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_Menu_Stack_MetaData[] = {
		{ "BindWidget", "" },
		{ "EditInline", "true" },
		{ "ModuleRelativePath", "Public/Widgets/GameUILayoutExtension.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_Modal_Stack_MetaData[] = {
		{ "BindWidget", "" },
		{ "EditInline", "true" },
		{ "ModuleRelativePath", "Public/Widgets/GameUILayoutExtension.h" },
	};
#endif // WITH_METADATA

// ********** Begin Class UGameUILayoutExtension constinit property declarations *******************
	static const UECodeGen_Private::FObjectPropertyParams NewProp_GameLayer_Stack;
	static const UECodeGen_Private::FObjectPropertyParams NewProp_GameMenu_Stack;
	static const UECodeGen_Private::FObjectPropertyParams NewProp_Menu_Stack;
	static const UECodeGen_Private::FObjectPropertyParams NewProp_Modal_Stack;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
// ********** End Class UGameUILayoutExtension constinit property declarations *********************
	static UObject* (*const DependentSingletons[])();
	static constexpr FCppClassTypeInfoStatic StaticCppClassTypeInfo = {
		TCppClassTypeTraits<UGameUILayoutExtension>::IsAbstract,
	};
	static const UECodeGen_Private::FClassParams ClassParams;
}; // struct Z_Construct_UClass_UGameUILayoutExtension_Statics

// ********** Begin Class UGameUILayoutExtension Property Definitions ******************************
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UClass_UGameUILayoutExtension_Statics::NewProp_GameLayer_Stack = { "GameLayer_Stack", nullptr, (EPropertyFlags)0x0020080000080008, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UGameUILayoutExtension, GameLayer_Stack), Z_Construct_UClass_UCommonActivatableWidgetContainerBase_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_GameLayer_Stack_MetaData), NewProp_GameLayer_Stack_MetaData) };
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UClass_UGameUILayoutExtension_Statics::NewProp_GameMenu_Stack = { "GameMenu_Stack", nullptr, (EPropertyFlags)0x0020080000080008, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UGameUILayoutExtension, GameMenu_Stack), Z_Construct_UClass_UCommonActivatableWidgetContainerBase_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_GameMenu_Stack_MetaData), NewProp_GameMenu_Stack_MetaData) };
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UClass_UGameUILayoutExtension_Statics::NewProp_Menu_Stack = { "Menu_Stack", nullptr, (EPropertyFlags)0x0020080000080008, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UGameUILayoutExtension, Menu_Stack), Z_Construct_UClass_UCommonActivatableWidgetContainerBase_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_Menu_Stack_MetaData), NewProp_Menu_Stack_MetaData) };
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UClass_UGameUILayoutExtension_Statics::NewProp_Modal_Stack = { "Modal_Stack", nullptr, (EPropertyFlags)0x0020080000080008, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UGameUILayoutExtension, Modal_Stack), Z_Construct_UClass_UCommonActivatableWidgetContainerBase_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_Modal_Stack_MetaData), NewProp_Modal_Stack_MetaData) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UClass_UGameUILayoutExtension_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UGameUILayoutExtension_Statics::NewProp_GameLayer_Stack,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UGameUILayoutExtension_Statics::NewProp_GameMenu_Stack,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UGameUILayoutExtension_Statics::NewProp_Menu_Stack,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UGameUILayoutExtension_Statics::NewProp_Modal_Stack,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_UGameUILayoutExtension_Statics::PropPointers) < 2048);
// ********** End Class UGameUILayoutExtension Property Definitions ********************************
UObject* (*const Z_Construct_UClass_UGameUILayoutExtension_Statics::DependentSingletons[])() = {
	(UObject* (*)())Z_Construct_UClass_UGUIS_GameUILayout,
	(UObject* (*)())Z_Construct_UPackage__Script_GenericUISystemExtension,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_UGameUILayoutExtension_Statics::DependentSingletons) < 16);
const UECodeGen_Private::FClassParams Z_Construct_UClass_UGameUILayoutExtension_Statics::ClassParams = {
	&UGameUILayoutExtension::StaticClass,
	nullptr,
	&StaticCppClassTypeInfo,
	DependentSingletons,
	nullptr,
	Z_Construct_UClass_UGameUILayoutExtension_Statics::PropPointers,
	nullptr,
	UE_ARRAY_COUNT(DependentSingletons),
	0,
	UE_ARRAY_COUNT(Z_Construct_UClass_UGameUILayoutExtension_Statics::PropPointers),
	0,
	0x00B010A1u,
	METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UClass_UGameUILayoutExtension_Statics::Class_MetaDataParams), Z_Construct_UClass_UGameUILayoutExtension_Statics::Class_MetaDataParams)
};
void UGameUILayoutExtension::StaticRegisterNativesUGameUILayoutExtension()
{
}
UClass* Z_Construct_UClass_UGameUILayoutExtension()
{
	if (!Z_Registration_Info_UClass_UGameUILayoutExtension.OuterSingleton)
	{
		UECodeGen_Private::ConstructUClass(Z_Registration_Info_UClass_UGameUILayoutExtension.OuterSingleton, Z_Construct_UClass_UGameUILayoutExtension_Statics::ClassParams);
	}
	return Z_Registration_Info_UClass_UGameUILayoutExtension.OuterSingleton;
}
DEFINE_VTABLE_PTR_HELPER_CTOR_NS(, UGameUILayoutExtension);
UGameUILayoutExtension::~UGameUILayoutExtension() {}
// ********** End Class UGameUILayoutExtension *****************************************************

// ********** Begin Registration *******************************************************************
struct Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Widgets_GameUILayoutExtension_h__Script_GenericUISystemExtension_Statics
{
	static constexpr FClassRegisterCompiledInInfo ClassInfo[] = {
		{ Z_Construct_UClass_UGameUILayoutExtension, UGameUILayoutExtension::StaticClass, TEXT("UGameUILayoutExtension"), &Z_Registration_Info_UClass_UGameUILayoutExtension, CONSTRUCT_RELOAD_VERSION_INFO(FClassReloadVersionInfo, sizeof(UGameUILayoutExtension), 3380013485U) },
	};
}; // Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Widgets_GameUILayoutExtension_h__Script_GenericUISystemExtension_Statics 
static FRegisterCompiledInInfo Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Widgets_GameUILayoutExtension_h__Script_GenericUISystemExtension_694362396{
	TEXT("/Script/GenericUISystemExtension"),
	Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Widgets_GameUILayoutExtension_h__Script_GenericUISystemExtension_Statics::ClassInfo, UE_ARRAY_COUNT(Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Widgets_GameUILayoutExtension_h__Script_GenericUISystemExtension_Statics::ClassInfo),
	nullptr, 0,
	nullptr, 0,
};
// ********** End Registration *********************************************************************

PRAGMA_ENABLE_DEPRECATION_WARNINGS
