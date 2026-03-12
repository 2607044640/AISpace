// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "Subsystems/GUIS_InputOverrideSubsystem.h"
#include "Engine/GameInstance.h"

PRAGMA_DISABLE_DEPRECATION_WARNINGS
static_assert(!UE_WITH_CONSTINIT_UOBJECT, "This generated code can only be compiled with !UE_WITH_CONSTINIT_OBJECT");
void EmptyLinkFunctionForGeneratedCodeGUIS_InputOverrideSubsystem() {}

// ********** Begin Cross Module References ********************************************************
COMMONUI_API UClass* Z_Construct_UClass_UCommonGenericInputActionDataTable_NoRegister();
ENGINE_API UClass* Z_Construct_UClass_UGameInstanceSubsystem();
GENERICUISYSTEMEXTENSION_API UClass* Z_Construct_UClass_UGUIS_InputOverrideSubsystem();
GENERICUISYSTEMEXTENSION_API UClass* Z_Construct_UClass_UGUIS_InputOverrideSubsystem_NoRegister();
UPackage* Z_Construct_UPackage__Script_GenericUISystemExtension();
// ********** End Cross Module References **********************************************************

// ********** Begin Class UGUIS_InputOverrideSubsystem Function ApplyCustomKeysToDataTable *********
struct Z_Construct_UFunction_UGUIS_InputOverrideSubsystem_ApplyCustomKeysToDataTable_Statics
{
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Function_MetaDataParams[] = {
		{ "Category", "GUIS|Input" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// Apply user custom keys from KeySettingData to DT_GenericInputActions\n" },
#endif
		{ "ModuleRelativePath", "Public/Subsystems/GUIS_InputOverrideSubsystem.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Apply user custom keys from KeySettingData to DT_GenericInputActions" },
#endif
	};
#endif // WITH_METADATA

// ********** Begin Function ApplyCustomKeysToDataTable constinit property declarations ************
// ********** End Function ApplyCustomKeysToDataTable constinit property declarations **************
	static const UECodeGen_Private::FFunctionParams FuncParams;
};
const UECodeGen_Private::FFunctionParams Z_Construct_UFunction_UGUIS_InputOverrideSubsystem_ApplyCustomKeysToDataTable_Statics::FuncParams = { { (UObject*(*)())Z_Construct_UClass_UGUIS_InputOverrideSubsystem, nullptr, "ApplyCustomKeysToDataTable", 	nullptr, 
	0, 
0,
RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x04020401, 0, 0, METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UFunction_UGUIS_InputOverrideSubsystem_ApplyCustomKeysToDataTable_Statics::Function_MetaDataParams), Z_Construct_UFunction_UGUIS_InputOverrideSubsystem_ApplyCustomKeysToDataTable_Statics::Function_MetaDataParams)},  };
UFunction* Z_Construct_UFunction_UGUIS_InputOverrideSubsystem_ApplyCustomKeysToDataTable()
{
	static UFunction* ReturnFunction = nullptr;
	if (!ReturnFunction)
	{
		UECodeGen_Private::ConstructUFunction(&ReturnFunction, Z_Construct_UFunction_UGUIS_InputOverrideSubsystem_ApplyCustomKeysToDataTable_Statics::FuncParams);
	}
	return ReturnFunction;
}
DEFINE_FUNCTION(UGUIS_InputOverrideSubsystem::execApplyCustomKeysToDataTable)
{
	P_FINISH;
	P_NATIVE_BEGIN;
	P_THIS->ApplyCustomKeysToDataTable();
	P_NATIVE_END;
}
// ********** End Class UGUIS_InputOverrideSubsystem Function ApplyCustomKeysToDataTable ***********

// ********** Begin Class UGUIS_InputOverrideSubsystem *********************************************
FClassRegistrationInfo Z_Registration_Info_UClass_UGUIS_InputOverrideSubsystem;
UClass* UGUIS_InputOverrideSubsystem::GetPrivateStaticClass()
{
	using TClass = UGUIS_InputOverrideSubsystem;
	if (!Z_Registration_Info_UClass_UGUIS_InputOverrideSubsystem.InnerSingleton)
	{
		GetPrivateStaticClassBody(
			TClass::StaticPackage(),
			TEXT("GUIS_InputOverrideSubsystem"),
			Z_Registration_Info_UClass_UGUIS_InputOverrideSubsystem.InnerSingleton,
			StaticRegisterNativesUGUIS_InputOverrideSubsystem,
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
	return Z_Registration_Info_UClass_UGUIS_InputOverrideSubsystem.InnerSingleton;
}
UClass* Z_Construct_UClass_UGUIS_InputOverrideSubsystem_NoRegister()
{
	return UGUIS_InputOverrideSubsystem::GetPrivateStaticClass();
}
struct Z_Construct_UClass_UGUIS_InputOverrideSubsystem_Statics
{
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Class_MetaDataParams[] = {
#if !UE_BUILD_SHIPPING
		{ "Comment", "/**\n * Subsystem that modifies DT_GenericInputActions at runtime to apply user custom key bindings\n * This ensures GUIS widgets use custom keys when registering input actions\n */" },
#endif
		{ "IncludePath", "Subsystems/GUIS_InputOverrideSubsystem.h" },
		{ "ModuleRelativePath", "Public/Subsystems/GUIS_InputOverrideSubsystem.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Subsystem that modifies DT_GenericInputActions at runtime to apply user custom key bindings\nThis ensures GUIS widgets use custom keys when registering input actions" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_InputDataTable_MetaData[] = {
		{ "ModuleRelativePath", "Public/Subsystems/GUIS_InputOverrideSubsystem.h" },
	};
#endif // WITH_METADATA

// ********** Begin Class UGUIS_InputOverrideSubsystem constinit property declarations *************
	static const UECodeGen_Private::FObjectPropertyParams NewProp_InputDataTable;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
// ********** End Class UGUIS_InputOverrideSubsystem constinit property declarations ***************
	static constexpr UE::CodeGen::FClassNativeFunction Funcs[] = {
		{ .NameUTF8 = UTF8TEXT("ApplyCustomKeysToDataTable"), .Pointer = &UGUIS_InputOverrideSubsystem::execApplyCustomKeysToDataTable },
	};
	static UObject* (*const DependentSingletons[])();
	static constexpr FClassFunctionLinkInfo FuncInfo[] = {
		{ &Z_Construct_UFunction_UGUIS_InputOverrideSubsystem_ApplyCustomKeysToDataTable, "ApplyCustomKeysToDataTable" }, // 4079483649
	};
	static_assert(UE_ARRAY_COUNT(FuncInfo) < 2048);
	static constexpr FCppClassTypeInfoStatic StaticCppClassTypeInfo = {
		TCppClassTypeTraits<UGUIS_InputOverrideSubsystem>::IsAbstract,
	};
	static const UECodeGen_Private::FClassParams ClassParams;
}; // struct Z_Construct_UClass_UGUIS_InputOverrideSubsystem_Statics

// ********** Begin Class UGUIS_InputOverrideSubsystem Property Definitions ************************
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UClass_UGUIS_InputOverrideSubsystem_Statics::NewProp_InputDataTable = { "InputDataTable", nullptr, (EPropertyFlags)0x0144000000000000, UECodeGen_Private::EPropertyGenFlags::Object | UECodeGen_Private::EPropertyGenFlags::ObjectPtr, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UGUIS_InputOverrideSubsystem, InputDataTable), Z_Construct_UClass_UCommonGenericInputActionDataTable_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_InputDataTable_MetaData), NewProp_InputDataTable_MetaData) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UClass_UGUIS_InputOverrideSubsystem_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UGUIS_InputOverrideSubsystem_Statics::NewProp_InputDataTable,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_UGUIS_InputOverrideSubsystem_Statics::PropPointers) < 2048);
// ********** End Class UGUIS_InputOverrideSubsystem Property Definitions **************************
UObject* (*const Z_Construct_UClass_UGUIS_InputOverrideSubsystem_Statics::DependentSingletons[])() = {
	(UObject* (*)())Z_Construct_UClass_UGameInstanceSubsystem,
	(UObject* (*)())Z_Construct_UPackage__Script_GenericUISystemExtension,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_UGUIS_InputOverrideSubsystem_Statics::DependentSingletons) < 16);
const UECodeGen_Private::FClassParams Z_Construct_UClass_UGUIS_InputOverrideSubsystem_Statics::ClassParams = {
	&UGUIS_InputOverrideSubsystem::StaticClass,
	nullptr,
	&StaticCppClassTypeInfo,
	DependentSingletons,
	FuncInfo,
	Z_Construct_UClass_UGUIS_InputOverrideSubsystem_Statics::PropPointers,
	nullptr,
	UE_ARRAY_COUNT(DependentSingletons),
	UE_ARRAY_COUNT(FuncInfo),
	UE_ARRAY_COUNT(Z_Construct_UClass_UGUIS_InputOverrideSubsystem_Statics::PropPointers),
	0,
	0x001000A0u,
	METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UClass_UGUIS_InputOverrideSubsystem_Statics::Class_MetaDataParams), Z_Construct_UClass_UGUIS_InputOverrideSubsystem_Statics::Class_MetaDataParams)
};
void UGUIS_InputOverrideSubsystem::StaticRegisterNativesUGUIS_InputOverrideSubsystem()
{
	UClass* Class = UGUIS_InputOverrideSubsystem::StaticClass();
	FNativeFunctionRegistrar::RegisterFunctions(Class, MakeConstArrayView(Z_Construct_UClass_UGUIS_InputOverrideSubsystem_Statics::Funcs));
}
UClass* Z_Construct_UClass_UGUIS_InputOverrideSubsystem()
{
	if (!Z_Registration_Info_UClass_UGUIS_InputOverrideSubsystem.OuterSingleton)
	{
		UECodeGen_Private::ConstructUClass(Z_Registration_Info_UClass_UGUIS_InputOverrideSubsystem.OuterSingleton, Z_Construct_UClass_UGUIS_InputOverrideSubsystem_Statics::ClassParams);
	}
	return Z_Registration_Info_UClass_UGUIS_InputOverrideSubsystem.OuterSingleton;
}
UGUIS_InputOverrideSubsystem::UGUIS_InputOverrideSubsystem() {}
DEFINE_VTABLE_PTR_HELPER_CTOR_NS(, UGUIS_InputOverrideSubsystem);
UGUIS_InputOverrideSubsystem::~UGUIS_InputOverrideSubsystem() {}
// ********** End Class UGUIS_InputOverrideSubsystem ***********************************************

// ********** Begin Registration *******************************************************************
struct Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Subsystems_GUIS_InputOverrideSubsystem_h__Script_GenericUISystemExtension_Statics
{
	static constexpr FClassRegisterCompiledInInfo ClassInfo[] = {
		{ Z_Construct_UClass_UGUIS_InputOverrideSubsystem, UGUIS_InputOverrideSubsystem::StaticClass, TEXT("UGUIS_InputOverrideSubsystem"), &Z_Registration_Info_UClass_UGUIS_InputOverrideSubsystem, CONSTRUCT_RELOAD_VERSION_INFO(FClassReloadVersionInfo, sizeof(UGUIS_InputOverrideSubsystem), 295500693U) },
	};
}; // Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Subsystems_GUIS_InputOverrideSubsystem_h__Script_GenericUISystemExtension_Statics 
static FRegisterCompiledInInfo Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Subsystems_GUIS_InputOverrideSubsystem_h__Script_GenericUISystemExtension_2720187295{
	TEXT("/Script/GenericUISystemExtension"),
	Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Subsystems_GUIS_InputOverrideSubsystem_h__Script_GenericUISystemExtension_Statics::ClassInfo, UE_ARRAY_COUNT(Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Subsystems_GUIS_InputOverrideSubsystem_h__Script_GenericUISystemExtension_Statics::ClassInfo),
	nullptr, 0,
	nullptr, 0,
};
// ********** End Registration *********************************************************************

PRAGMA_ENABLE_DEPRECATION_WARNINGS
