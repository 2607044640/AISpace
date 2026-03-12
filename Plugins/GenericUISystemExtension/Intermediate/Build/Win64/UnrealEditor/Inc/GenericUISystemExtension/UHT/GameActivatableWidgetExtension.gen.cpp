// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "Widgets/GameActivatableWidgetExtension.h"

PRAGMA_DISABLE_DEPRECATION_WARNINGS
static_assert(!UE_WITH_CONSTINIT_UOBJECT, "This generated code can only be compiled with !UE_WITH_CONSTINIT_OBJECT");
void EmptyLinkFunctionForGeneratedCodeGameActivatableWidgetExtension() {}

// ********** Begin Cross Module References ********************************************************
GENERICUISYSTEM_API UClass* Z_Construct_UClass_UGUIS_ActivatableWidget();
GENERICUISYSTEM_API UClass* Z_Construct_UClass_UGUIS_UIActionFactory_NoRegister();
GENERICUISYSTEMEXTENSION_API UClass* Z_Construct_UClass_UGameActivatableWidgetExtension();
GENERICUISYSTEMEXTENSION_API UClass* Z_Construct_UClass_UGameActivatableWidgetExtension_NoRegister();
UPackage* Z_Construct_UPackage__Script_GenericUISystemExtension();
// ********** End Cross Module References **********************************************************

// ********** Begin Class UGameActivatableWidgetExtension Function HandleCloseUI *******************
struct Z_Construct_UFunction_UGameActivatableWidgetExtension_HandleCloseUI_Statics
{
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Function_MetaDataParams[] = {
		{ "Category", "UI" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "/**\n\x09 * Handle close UI action - closes this widget\n\x09 * Called by UIAction system when close input is triggered\n\x09 */" },
#endif
		{ "ModuleRelativePath", "Public/Widgets/GameActivatableWidgetExtension.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Handle close UI action - closes this widget\nCalled by UIAction system when close input is triggered" },
#endif
	};
#endif // WITH_METADATA

// ********** Begin Function HandleCloseUI constinit property declarations *************************
// ********** End Function HandleCloseUI constinit property declarations ***************************
	static const UECodeGen_Private::FFunctionParams FuncParams;
};
const UECodeGen_Private::FFunctionParams Z_Construct_UFunction_UGameActivatableWidgetExtension_HandleCloseUI_Statics::FuncParams = { { (UObject*(*)())Z_Construct_UClass_UGameActivatableWidgetExtension, nullptr, "HandleCloseUI", 	nullptr, 
	0, 
0,
RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x04020401, 0, 0, METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UFunction_UGameActivatableWidgetExtension_HandleCloseUI_Statics::Function_MetaDataParams), Z_Construct_UFunction_UGameActivatableWidgetExtension_HandleCloseUI_Statics::Function_MetaDataParams)},  };
UFunction* Z_Construct_UFunction_UGameActivatableWidgetExtension_HandleCloseUI()
{
	static UFunction* ReturnFunction = nullptr;
	if (!ReturnFunction)
	{
		UECodeGen_Private::ConstructUFunction(&ReturnFunction, Z_Construct_UFunction_UGameActivatableWidgetExtension_HandleCloseUI_Statics::FuncParams);
	}
	return ReturnFunction;
}
DEFINE_FUNCTION(UGameActivatableWidgetExtension::execHandleCloseUI)
{
	P_FINISH;
	P_NATIVE_BEGIN;
	P_THIS->HandleCloseUI();
	P_NATIVE_END;
}
// ********** End Class UGameActivatableWidgetExtension Function HandleCloseUI *********************

// ********** Begin Class UGameActivatableWidgetExtension ******************************************
FClassRegistrationInfo Z_Registration_Info_UClass_UGameActivatableWidgetExtension;
UClass* UGameActivatableWidgetExtension::GetPrivateStaticClass()
{
	using TClass = UGameActivatableWidgetExtension;
	if (!Z_Registration_Info_UClass_UGameActivatableWidgetExtension.InnerSingleton)
	{
		GetPrivateStaticClassBody(
			TClass::StaticPackage(),
			TEXT("GameActivatableWidgetExtension"),
			Z_Registration_Info_UClass_UGameActivatableWidgetExtension.InnerSingleton,
			StaticRegisterNativesUGameActivatableWidgetExtension,
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
	return Z_Registration_Info_UClass_UGameActivatableWidgetExtension.InnerSingleton;
}
UClass* Z_Construct_UClass_UGameActivatableWidgetExtension_NoRegister()
{
	return UGameActivatableWidgetExtension::GetPrivateStaticClass();
}
struct Z_Construct_UClass_UGameActivatableWidgetExtension_Statics
{
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Class_MetaDataParams[] = {
		{ "BlueprintType", "true" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "/**\n * Base widget class for game UI that should pause the game when shown.\n * \n * Features:\n * - Inherits from UGUIS_ActivatableWidget for GenericUISystem integration\n * - Automatically requests pause from UIStateSubsystem when activated\n * - Automatically releases pause when deactivated\n * - Reference counting ensures game stays paused when multiple UIs are open\n * - Auto-creates and manages UGUIS_UIActionWidget for generic UI actions (Close, OpenSettings, etc.)\n * \n * Usage:\n * 1. Create a Blueprint widget inheriting from this class\n * 2. Use UGUIS_GameUIFunctionLibrary::PushContentToUILayer_ForPlayer() to show\n * 3. Pause is automatically managed\n * 4. UIActions (Close, OpenSettings) are automatically registered when bAutoRegisterUIActions = true\n */" },
#endif
		{ "IncludePath", "Widgets/GameActivatableWidgetExtension.h" },
		{ "IsBlueprintBase", "true" },
		{ "ModuleRelativePath", "Public/Widgets/GameActivatableWidgetExtension.h" },
		{ "ObjectInitializerConstructorDeclared", "" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Base widget class for game UI that should pause the game when shown.\n\nFeatures:\n- Inherits from UGUIS_ActivatableWidget for GenericUISystem integration\n- Automatically requests pause from UIStateSubsystem when activated\n- Automatically releases pause when deactivated\n- Reference counting ensures game stays paused when multiple UIs are open\n- Auto-creates and manages UGUIS_UIActionWidget for generic UI actions (Close, OpenSettings, etc.)\n\nUsage:\n1. Create a Blueprint widget inheriting from this class\n2. Use UGUIS_GameUIFunctionLibrary::PushContentToUILayer_ForPlayer() to show\n3. Pause is automatically managed\n4. UIActions (Close, OpenSettings) are automatically registered when bAutoRegisterUIActions = true" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bShouldPauseGame_MetaData[] = {
		{ "Category", "UI|GameState" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// Whether this widget should pause the game when shown\n" },
#endif
		{ "ModuleRelativePath", "Public/Widgets/GameActivatableWidgetExtension.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Whether this widget should pause the game when shown" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bAutoRegisterUIActions_MetaData[] = {
		{ "Category", "UI|Actions" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// Whether to automatically create and register UIActions (Close, OpenSettings, etc.)\n// When true, no Blueprint setup is needed for basic UI actions\n" },
#endif
		{ "ModuleRelativePath", "Public/Widgets/GameActivatableWidgetExtension.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Whether to automatically create and register UIActions (Close, OpenSettings, etc.)\nWhen true, no Blueprint setup is needed for basic UI actions" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_GenericUIActionFactory_MetaData[] = {
		{ "Category", "UI|Actions" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// The UIActionFactory to use for auto-registered actions\n// Default: DA_GenericUIActions (loaded at runtime)\n" },
#endif
		{ "EditCondition", "bAutoRegisterUIActions" },
		{ "ModuleRelativePath", "Public/Widgets/GameActivatableWidgetExtension.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "The UIActionFactory to use for auto-registered actions\nDefault: DA_GenericUIActions (loaded at runtime)" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_CachedActionFactory_MetaData[] = {
#if !UE_BUILD_SHIPPING
		{ "Comment", "// Cached action factory\n" },
#endif
		{ "ModuleRelativePath", "Public/Widgets/GameActivatableWidgetExtension.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Cached action factory" },
#endif
	};
#endif // WITH_METADATA

// ********** Begin Class UGameActivatableWidgetExtension constinit property declarations **********
	static void NewProp_bShouldPauseGame_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bShouldPauseGame;
	static void NewProp_bAutoRegisterUIActions_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bAutoRegisterUIActions;
	static const UECodeGen_Private::FSoftObjectPropertyParams NewProp_GenericUIActionFactory;
	static const UECodeGen_Private::FObjectPropertyParams NewProp_CachedActionFactory;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
// ********** End Class UGameActivatableWidgetExtension constinit property declarations ************
	static constexpr UE::CodeGen::FClassNativeFunction Funcs[] = {
		{ .NameUTF8 = UTF8TEXT("HandleCloseUI"), .Pointer = &UGameActivatableWidgetExtension::execHandleCloseUI },
	};
	static UObject* (*const DependentSingletons[])();
	static constexpr FClassFunctionLinkInfo FuncInfo[] = {
		{ &Z_Construct_UFunction_UGameActivatableWidgetExtension_HandleCloseUI, "HandleCloseUI" }, // 1891208689
	};
	static_assert(UE_ARRAY_COUNT(FuncInfo) < 2048);
	static constexpr FCppClassTypeInfoStatic StaticCppClassTypeInfo = {
		TCppClassTypeTraits<UGameActivatableWidgetExtension>::IsAbstract,
	};
	static const UECodeGen_Private::FClassParams ClassParams;
}; // struct Z_Construct_UClass_UGameActivatableWidgetExtension_Statics

// ********** Begin Class UGameActivatableWidgetExtension Property Definitions *********************
void Z_Construct_UClass_UGameActivatableWidgetExtension_Statics::NewProp_bShouldPauseGame_SetBit(void* Obj)
{
	((UGameActivatableWidgetExtension*)Obj)->bShouldPauseGame = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_UGameActivatableWidgetExtension_Statics::NewProp_bShouldPauseGame = { "bShouldPauseGame", nullptr, (EPropertyFlags)0x0020080000010005, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(UGameActivatableWidgetExtension), &Z_Construct_UClass_UGameActivatableWidgetExtension_Statics::NewProp_bShouldPauseGame_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bShouldPauseGame_MetaData), NewProp_bShouldPauseGame_MetaData) };
void Z_Construct_UClass_UGameActivatableWidgetExtension_Statics::NewProp_bAutoRegisterUIActions_SetBit(void* Obj)
{
	((UGameActivatableWidgetExtension*)Obj)->bAutoRegisterUIActions = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_UGameActivatableWidgetExtension_Statics::NewProp_bAutoRegisterUIActions = { "bAutoRegisterUIActions", nullptr, (EPropertyFlags)0x0020080000010005, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(UGameActivatableWidgetExtension), &Z_Construct_UClass_UGameActivatableWidgetExtension_Statics::NewProp_bAutoRegisterUIActions_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bAutoRegisterUIActions_MetaData), NewProp_bAutoRegisterUIActions_MetaData) };
const UECodeGen_Private::FSoftObjectPropertyParams Z_Construct_UClass_UGameActivatableWidgetExtension_Statics::NewProp_GenericUIActionFactory = { "GenericUIActionFactory", nullptr, (EPropertyFlags)0x0024080000010005, UECodeGen_Private::EPropertyGenFlags::SoftObject, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UGameActivatableWidgetExtension, GenericUIActionFactory), Z_Construct_UClass_UGUIS_UIActionFactory_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_GenericUIActionFactory_MetaData), NewProp_GenericUIActionFactory_MetaData) };
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UClass_UGameActivatableWidgetExtension_Statics::NewProp_CachedActionFactory = { "CachedActionFactory", nullptr, (EPropertyFlags)0x0144000000000000, UECodeGen_Private::EPropertyGenFlags::Object | UECodeGen_Private::EPropertyGenFlags::ObjectPtr, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UGameActivatableWidgetExtension, CachedActionFactory), Z_Construct_UClass_UGUIS_UIActionFactory_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_CachedActionFactory_MetaData), NewProp_CachedActionFactory_MetaData) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UClass_UGameActivatableWidgetExtension_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UGameActivatableWidgetExtension_Statics::NewProp_bShouldPauseGame,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UGameActivatableWidgetExtension_Statics::NewProp_bAutoRegisterUIActions,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UGameActivatableWidgetExtension_Statics::NewProp_GenericUIActionFactory,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UGameActivatableWidgetExtension_Statics::NewProp_CachedActionFactory,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_UGameActivatableWidgetExtension_Statics::PropPointers) < 2048);
// ********** End Class UGameActivatableWidgetExtension Property Definitions ***********************
UObject* (*const Z_Construct_UClass_UGameActivatableWidgetExtension_Statics::DependentSingletons[])() = {
	(UObject* (*)())Z_Construct_UClass_UGUIS_ActivatableWidget,
	(UObject* (*)())Z_Construct_UPackage__Script_GenericUISystemExtension,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_UGameActivatableWidgetExtension_Statics::DependentSingletons) < 16);
const UECodeGen_Private::FClassParams Z_Construct_UClass_UGameActivatableWidgetExtension_Statics::ClassParams = {
	&UGameActivatableWidgetExtension::StaticClass,
	nullptr,
	&StaticCppClassTypeInfo,
	DependentSingletons,
	FuncInfo,
	Z_Construct_UClass_UGameActivatableWidgetExtension_Statics::PropPointers,
	nullptr,
	UE_ARRAY_COUNT(DependentSingletons),
	UE_ARRAY_COUNT(FuncInfo),
	UE_ARRAY_COUNT(Z_Construct_UClass_UGameActivatableWidgetExtension_Statics::PropPointers),
	0,
	0x00B010A1u,
	METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UClass_UGameActivatableWidgetExtension_Statics::Class_MetaDataParams), Z_Construct_UClass_UGameActivatableWidgetExtension_Statics::Class_MetaDataParams)
};
void UGameActivatableWidgetExtension::StaticRegisterNativesUGameActivatableWidgetExtension()
{
	UClass* Class = UGameActivatableWidgetExtension::StaticClass();
	FNativeFunctionRegistrar::RegisterFunctions(Class, MakeConstArrayView(Z_Construct_UClass_UGameActivatableWidgetExtension_Statics::Funcs));
}
UClass* Z_Construct_UClass_UGameActivatableWidgetExtension()
{
	if (!Z_Registration_Info_UClass_UGameActivatableWidgetExtension.OuterSingleton)
	{
		UECodeGen_Private::ConstructUClass(Z_Registration_Info_UClass_UGameActivatableWidgetExtension.OuterSingleton, Z_Construct_UClass_UGameActivatableWidgetExtension_Statics::ClassParams);
	}
	return Z_Registration_Info_UClass_UGameActivatableWidgetExtension.OuterSingleton;
}
DEFINE_VTABLE_PTR_HELPER_CTOR_NS(, UGameActivatableWidgetExtension);
UGameActivatableWidgetExtension::~UGameActivatableWidgetExtension() {}
// ********** End Class UGameActivatableWidgetExtension ********************************************

// ********** Begin Registration *******************************************************************
struct Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Widgets_GameActivatableWidgetExtension_h__Script_GenericUISystemExtension_Statics
{
	static constexpr FClassRegisterCompiledInInfo ClassInfo[] = {
		{ Z_Construct_UClass_UGameActivatableWidgetExtension, UGameActivatableWidgetExtension::StaticClass, TEXT("UGameActivatableWidgetExtension"), &Z_Registration_Info_UClass_UGameActivatableWidgetExtension, CONSTRUCT_RELOAD_VERSION_INFO(FClassReloadVersionInfo, sizeof(UGameActivatableWidgetExtension), 3874619220U) },
	};
}; // Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Widgets_GameActivatableWidgetExtension_h__Script_GenericUISystemExtension_Statics 
static FRegisterCompiledInInfo Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Widgets_GameActivatableWidgetExtension_h__Script_GenericUISystemExtension_1018692786{
	TEXT("/Script/GenericUISystemExtension"),
	Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Widgets_GameActivatableWidgetExtension_h__Script_GenericUISystemExtension_Statics::ClassInfo, UE_ARRAY_COUNT(Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Widgets_GameActivatableWidgetExtension_h__Script_GenericUISystemExtension_Statics::ClassInfo),
	nullptr, 0,
	nullptr, 0,
};
// ********** End Registration *********************************************************************

PRAGMA_ENABLE_DEPRECATION_WARNINGS
