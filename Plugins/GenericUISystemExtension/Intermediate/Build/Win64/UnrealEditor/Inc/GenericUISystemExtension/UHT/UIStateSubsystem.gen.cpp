// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "Subsystems/UIStateSubsystem.h"
#include "Engine/GameInstance.h"

PRAGMA_DISABLE_DEPRECATION_WARNINGS
static_assert(!UE_WITH_CONSTINIT_UOBJECT, "This generated code can only be compiled with !UE_WITH_CONSTINIT_OBJECT");
void EmptyLinkFunctionForGeneratedCodeUIStateSubsystem() {}

// ********** Begin Cross Module References ********************************************************
ENGINE_API UClass* Z_Construct_UClass_UGameInstanceSubsystem();
GENERICUISYSTEMEXTENSION_API UClass* Z_Construct_UClass_UUIStateSubsystem();
GENERICUISYSTEMEXTENSION_API UClass* Z_Construct_UClass_UUIStateSubsystem_NoRegister();
UPackage* Z_Construct_UPackage__Script_GenericUISystemExtension();
// ********** End Cross Module References **********************************************************

// ********** Begin Class UUIStateSubsystem Function GetPauseRequestCount **************************
struct Z_Construct_UFunction_UUIStateSubsystem_GetPauseRequestCount_Statics
{
	struct UIStateSubsystem_eventGetPauseRequestCount_Parms
	{
		int32 ReturnValue;
	};
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Function_MetaDataParams[] = {
		{ "Category", "UI|State" },
		{ "ModuleRelativePath", "Public/Subsystems/UIStateSubsystem.h" },
	};
#endif // WITH_METADATA

// ********** Begin Function GetPauseRequestCount constinit property declarations ******************
	static const UECodeGen_Private::FIntPropertyParams NewProp_ReturnValue;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
// ********** End Function GetPauseRequestCount constinit property declarations ********************
	static const UECodeGen_Private::FFunctionParams FuncParams;
};

// ********** Begin Function GetPauseRequestCount Property Definitions *****************************
const UECodeGen_Private::FIntPropertyParams Z_Construct_UFunction_UUIStateSubsystem_GetPauseRequestCount_Statics::NewProp_ReturnValue = { "ReturnValue", nullptr, (EPropertyFlags)0x0010000000000580, UECodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UIStateSubsystem_eventGetPauseRequestCount_Parms, ReturnValue), METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_UUIStateSubsystem_GetPauseRequestCount_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UUIStateSubsystem_GetPauseRequestCount_Statics::NewProp_ReturnValue,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UFunction_UUIStateSubsystem_GetPauseRequestCount_Statics::PropPointers) < 2048);
// ********** End Function GetPauseRequestCount Property Definitions *******************************
const UECodeGen_Private::FFunctionParams Z_Construct_UFunction_UUIStateSubsystem_GetPauseRequestCount_Statics::FuncParams = { { (UObject*(*)())Z_Construct_UClass_UUIStateSubsystem, nullptr, "GetPauseRequestCount", 	Z_Construct_UFunction_UUIStateSubsystem_GetPauseRequestCount_Statics::PropPointers, 
	UE_ARRAY_COUNT(Z_Construct_UFunction_UUIStateSubsystem_GetPauseRequestCount_Statics::PropPointers), 
sizeof(Z_Construct_UFunction_UUIStateSubsystem_GetPauseRequestCount_Statics::UIStateSubsystem_eventGetPauseRequestCount_Parms),
RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x54020401, 0, 0, METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UFunction_UUIStateSubsystem_GetPauseRequestCount_Statics::Function_MetaDataParams), Z_Construct_UFunction_UUIStateSubsystem_GetPauseRequestCount_Statics::Function_MetaDataParams)},  };
static_assert(sizeof(Z_Construct_UFunction_UUIStateSubsystem_GetPauseRequestCount_Statics::UIStateSubsystem_eventGetPauseRequestCount_Parms) < MAX_uint16);
UFunction* Z_Construct_UFunction_UUIStateSubsystem_GetPauseRequestCount()
{
	static UFunction* ReturnFunction = nullptr;
	if (!ReturnFunction)
	{
		UECodeGen_Private::ConstructUFunction(&ReturnFunction, Z_Construct_UFunction_UUIStateSubsystem_GetPauseRequestCount_Statics::FuncParams);
	}
	return ReturnFunction;
}
DEFINE_FUNCTION(UUIStateSubsystem::execGetPauseRequestCount)
{
	P_FINISH;
	P_NATIVE_BEGIN;
	*(int32*)Z_Param__Result=P_THIS->GetPauseRequestCount();
	P_NATIVE_END;
}
// ********** End Class UUIStateSubsystem Function GetPauseRequestCount ****************************

// ********** Begin Class UUIStateSubsystem Function IsPaused **************************************
struct Z_Construct_UFunction_UUIStateSubsystem_IsPaused_Statics
{
	struct UIStateSubsystem_eventIsPaused_Parms
	{
		bool ReturnValue;
	};
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Function_MetaDataParams[] = {
		{ "Category", "UI|State" },
		{ "ModuleRelativePath", "Public/Subsystems/UIStateSubsystem.h" },
	};
#endif // WITH_METADATA

// ********** Begin Function IsPaused constinit property declarations ******************************
	static void NewProp_ReturnValue_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_ReturnValue;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
// ********** End Function IsPaused constinit property declarations ********************************
	static const UECodeGen_Private::FFunctionParams FuncParams;
};

// ********** Begin Function IsPaused Property Definitions *****************************************
void Z_Construct_UFunction_UUIStateSubsystem_IsPaused_Statics::NewProp_ReturnValue_SetBit(void* Obj)
{
	((UIStateSubsystem_eventIsPaused_Parms*)Obj)->ReturnValue = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UFunction_UUIStateSubsystem_IsPaused_Statics::NewProp_ReturnValue = { "ReturnValue", nullptr, (EPropertyFlags)0x0010000000000580, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(UIStateSubsystem_eventIsPaused_Parms), &Z_Construct_UFunction_UUIStateSubsystem_IsPaused_Statics::NewProp_ReturnValue_SetBit, METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_UUIStateSubsystem_IsPaused_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UUIStateSubsystem_IsPaused_Statics::NewProp_ReturnValue,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UFunction_UUIStateSubsystem_IsPaused_Statics::PropPointers) < 2048);
// ********** End Function IsPaused Property Definitions *******************************************
const UECodeGen_Private::FFunctionParams Z_Construct_UFunction_UUIStateSubsystem_IsPaused_Statics::FuncParams = { { (UObject*(*)())Z_Construct_UClass_UUIStateSubsystem, nullptr, "IsPaused", 	Z_Construct_UFunction_UUIStateSubsystem_IsPaused_Statics::PropPointers, 
	UE_ARRAY_COUNT(Z_Construct_UFunction_UUIStateSubsystem_IsPaused_Statics::PropPointers), 
sizeof(Z_Construct_UFunction_UUIStateSubsystem_IsPaused_Statics::UIStateSubsystem_eventIsPaused_Parms),
RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x54020401, 0, 0, METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UFunction_UUIStateSubsystem_IsPaused_Statics::Function_MetaDataParams), Z_Construct_UFunction_UUIStateSubsystem_IsPaused_Statics::Function_MetaDataParams)},  };
static_assert(sizeof(Z_Construct_UFunction_UUIStateSubsystem_IsPaused_Statics::UIStateSubsystem_eventIsPaused_Parms) < MAX_uint16);
UFunction* Z_Construct_UFunction_UUIStateSubsystem_IsPaused()
{
	static UFunction* ReturnFunction = nullptr;
	if (!ReturnFunction)
	{
		UECodeGen_Private::ConstructUFunction(&ReturnFunction, Z_Construct_UFunction_UUIStateSubsystem_IsPaused_Statics::FuncParams);
	}
	return ReturnFunction;
}
DEFINE_FUNCTION(UUIStateSubsystem::execIsPaused)
{
	P_FINISH;
	P_NATIVE_BEGIN;
	*(bool*)Z_Param__Result=P_THIS->IsPaused();
	P_NATIVE_END;
}
// ********** End Class UUIStateSubsystem Function IsPaused ****************************************

// ********** Begin Class UUIStateSubsystem Function ReleasePause **********************************
struct Z_Construct_UFunction_UUIStateSubsystem_ReleasePause_Statics
{
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Function_MetaDataParams[] = {
		{ "Category", "UI|State" },
		{ "ModuleRelativePath", "Public/Subsystems/UIStateSubsystem.h" },
	};
#endif // WITH_METADATA

// ********** Begin Function ReleasePause constinit property declarations **************************
// ********** End Function ReleasePause constinit property declarations ****************************
	static const UECodeGen_Private::FFunctionParams FuncParams;
};
const UECodeGen_Private::FFunctionParams Z_Construct_UFunction_UUIStateSubsystem_ReleasePause_Statics::FuncParams = { { (UObject*(*)())Z_Construct_UClass_UUIStateSubsystem, nullptr, "ReleasePause", 	nullptr, 
	0, 
0,
RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x04020401, 0, 0, METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UFunction_UUIStateSubsystem_ReleasePause_Statics::Function_MetaDataParams), Z_Construct_UFunction_UUIStateSubsystem_ReleasePause_Statics::Function_MetaDataParams)},  };
UFunction* Z_Construct_UFunction_UUIStateSubsystem_ReleasePause()
{
	static UFunction* ReturnFunction = nullptr;
	if (!ReturnFunction)
	{
		UECodeGen_Private::ConstructUFunction(&ReturnFunction, Z_Construct_UFunction_UUIStateSubsystem_ReleasePause_Statics::FuncParams);
	}
	return ReturnFunction;
}
DEFINE_FUNCTION(UUIStateSubsystem::execReleasePause)
{
	P_FINISH;
	P_NATIVE_BEGIN;
	P_THIS->ReleasePause();
	P_NATIVE_END;
}
// ********** End Class UUIStateSubsystem Function ReleasePause ************************************

// ********** Begin Class UUIStateSubsystem Function RequestPause **********************************
struct Z_Construct_UFunction_UUIStateSubsystem_RequestPause_Statics
{
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Function_MetaDataParams[] = {
		{ "Category", "UI|State" },
		{ "ModuleRelativePath", "Public/Subsystems/UIStateSubsystem.h" },
	};
#endif // WITH_METADATA

// ********** Begin Function RequestPause constinit property declarations **************************
// ********** End Function RequestPause constinit property declarations ****************************
	static const UECodeGen_Private::FFunctionParams FuncParams;
};
const UECodeGen_Private::FFunctionParams Z_Construct_UFunction_UUIStateSubsystem_RequestPause_Statics::FuncParams = { { (UObject*(*)())Z_Construct_UClass_UUIStateSubsystem, nullptr, "RequestPause", 	nullptr, 
	0, 
0,
RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x04020401, 0, 0, METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UFunction_UUIStateSubsystem_RequestPause_Statics::Function_MetaDataParams), Z_Construct_UFunction_UUIStateSubsystem_RequestPause_Statics::Function_MetaDataParams)},  };
UFunction* Z_Construct_UFunction_UUIStateSubsystem_RequestPause()
{
	static UFunction* ReturnFunction = nullptr;
	if (!ReturnFunction)
	{
		UECodeGen_Private::ConstructUFunction(&ReturnFunction, Z_Construct_UFunction_UUIStateSubsystem_RequestPause_Statics::FuncParams);
	}
	return ReturnFunction;
}
DEFINE_FUNCTION(UUIStateSubsystem::execRequestPause)
{
	P_FINISH;
	P_NATIVE_BEGIN;
	P_THIS->RequestPause();
	P_NATIVE_END;
}
// ********** End Class UUIStateSubsystem Function RequestPause ************************************

// ********** Begin Class UUIStateSubsystem ********************************************************
FClassRegistrationInfo Z_Registration_Info_UClass_UUIStateSubsystem;
UClass* UUIStateSubsystem::GetPrivateStaticClass()
{
	using TClass = UUIStateSubsystem;
	if (!Z_Registration_Info_UClass_UUIStateSubsystem.InnerSingleton)
	{
		GetPrivateStaticClassBody(
			TClass::StaticPackage(),
			TEXT("UIStateSubsystem"),
			Z_Registration_Info_UClass_UUIStateSubsystem.InnerSingleton,
			StaticRegisterNativesUUIStateSubsystem,
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
	return Z_Registration_Info_UClass_UUIStateSubsystem.InnerSingleton;
}
UClass* Z_Construct_UClass_UUIStateSubsystem_NoRegister()
{
	return UUIStateSubsystem::GetPrivateStaticClass();
}
struct Z_Construct_UClass_UUIStateSubsystem_Statics
{
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Class_MetaDataParams[] = {
#if !UE_BUILD_SHIPPING
		{ "Comment", "/**\n * Subsystem for managing game pause state and input mode when UI is open.\n * Uses reference counting to handle multiple overlapping UIs.\n * \n * Usage:\n * - Call RequestPause() when opening a UI that should pause the game\n * - Call ReleasePause() when closing that UI\n * - Game only unpauses when all pause requests are released\n */" },
#endif
		{ "IncludePath", "Subsystems/UIStateSubsystem.h" },
		{ "ModuleRelativePath", "Public/Subsystems/UIStateSubsystem.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Subsystem for managing game pause state and input mode when UI is open.\nUses reference counting to handle multiple overlapping UIs.\n\nUsage:\n- Call RequestPause() when opening a UI that should pause the game\n- Call ReleasePause() when closing that UI\n- Game only unpauses when all pause requests are released" },
#endif
	};
#endif // WITH_METADATA

// ********** Begin Class UUIStateSubsystem constinit property declarations ************************
// ********** End Class UUIStateSubsystem constinit property declarations **************************
	static constexpr UE::CodeGen::FClassNativeFunction Funcs[] = {
		{ .NameUTF8 = UTF8TEXT("GetPauseRequestCount"), .Pointer = &UUIStateSubsystem::execGetPauseRequestCount },
		{ .NameUTF8 = UTF8TEXT("IsPaused"), .Pointer = &UUIStateSubsystem::execIsPaused },
		{ .NameUTF8 = UTF8TEXT("ReleasePause"), .Pointer = &UUIStateSubsystem::execReleasePause },
		{ .NameUTF8 = UTF8TEXT("RequestPause"), .Pointer = &UUIStateSubsystem::execRequestPause },
	};
	static UObject* (*const DependentSingletons[])();
	static constexpr FClassFunctionLinkInfo FuncInfo[] = {
		{ &Z_Construct_UFunction_UUIStateSubsystem_GetPauseRequestCount, "GetPauseRequestCount" }, // 3154500766
		{ &Z_Construct_UFunction_UUIStateSubsystem_IsPaused, "IsPaused" }, // 705989523
		{ &Z_Construct_UFunction_UUIStateSubsystem_ReleasePause, "ReleasePause" }, // 4142651333
		{ &Z_Construct_UFunction_UUIStateSubsystem_RequestPause, "RequestPause" }, // 3539187436
	};
	static_assert(UE_ARRAY_COUNT(FuncInfo) < 2048);
	static constexpr FCppClassTypeInfoStatic StaticCppClassTypeInfo = {
		TCppClassTypeTraits<UUIStateSubsystem>::IsAbstract,
	};
	static const UECodeGen_Private::FClassParams ClassParams;
}; // struct Z_Construct_UClass_UUIStateSubsystem_Statics
UObject* (*const Z_Construct_UClass_UUIStateSubsystem_Statics::DependentSingletons[])() = {
	(UObject* (*)())Z_Construct_UClass_UGameInstanceSubsystem,
	(UObject* (*)())Z_Construct_UPackage__Script_GenericUISystemExtension,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_UUIStateSubsystem_Statics::DependentSingletons) < 16);
const UECodeGen_Private::FClassParams Z_Construct_UClass_UUIStateSubsystem_Statics::ClassParams = {
	&UUIStateSubsystem::StaticClass,
	nullptr,
	&StaticCppClassTypeInfo,
	DependentSingletons,
	FuncInfo,
	nullptr,
	nullptr,
	UE_ARRAY_COUNT(DependentSingletons),
	UE_ARRAY_COUNT(FuncInfo),
	0,
	0,
	0x001000A0u,
	METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UClass_UUIStateSubsystem_Statics::Class_MetaDataParams), Z_Construct_UClass_UUIStateSubsystem_Statics::Class_MetaDataParams)
};
void UUIStateSubsystem::StaticRegisterNativesUUIStateSubsystem()
{
	UClass* Class = UUIStateSubsystem::StaticClass();
	FNativeFunctionRegistrar::RegisterFunctions(Class, MakeConstArrayView(Z_Construct_UClass_UUIStateSubsystem_Statics::Funcs));
}
UClass* Z_Construct_UClass_UUIStateSubsystem()
{
	if (!Z_Registration_Info_UClass_UUIStateSubsystem.OuterSingleton)
	{
		UECodeGen_Private::ConstructUClass(Z_Registration_Info_UClass_UUIStateSubsystem.OuterSingleton, Z_Construct_UClass_UUIStateSubsystem_Statics::ClassParams);
	}
	return Z_Registration_Info_UClass_UUIStateSubsystem.OuterSingleton;
}
UUIStateSubsystem::UUIStateSubsystem() {}
DEFINE_VTABLE_PTR_HELPER_CTOR_NS(, UUIStateSubsystem);
UUIStateSubsystem::~UUIStateSubsystem() {}
// ********** End Class UUIStateSubsystem **********************************************************

// ********** Begin Registration *******************************************************************
struct Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Subsystems_UIStateSubsystem_h__Script_GenericUISystemExtension_Statics
{
	static constexpr FClassRegisterCompiledInInfo ClassInfo[] = {
		{ Z_Construct_UClass_UUIStateSubsystem, UUIStateSubsystem::StaticClass, TEXT("UUIStateSubsystem"), &Z_Registration_Info_UClass_UUIStateSubsystem, CONSTRUCT_RELOAD_VERSION_INFO(FClassReloadVersionInfo, sizeof(UUIStateSubsystem), 3378497206U) },
	};
}; // Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Subsystems_UIStateSubsystem_h__Script_GenericUISystemExtension_Statics 
static FRegisterCompiledInInfo Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Subsystems_UIStateSubsystem_h__Script_GenericUISystemExtension_85925877{
	TEXT("/Script/GenericUISystemExtension"),
	Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Subsystems_UIStateSubsystem_h__Script_GenericUISystemExtension_Statics::ClassInfo, UE_ARRAY_COUNT(Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Subsystems_UIStateSubsystem_h__Script_GenericUISystemExtension_Statics::ClassInfo),
	nullptr, 0,
	nullptr, 0,
};
// ********** End Registration *********************************************************************

PRAGMA_ENABLE_DEPRECATION_WARNINGS
