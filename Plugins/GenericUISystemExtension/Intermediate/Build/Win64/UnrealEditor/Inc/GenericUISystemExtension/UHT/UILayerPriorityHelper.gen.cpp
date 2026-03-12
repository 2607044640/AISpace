// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "Utilities/UILayerPriorityHelper.h"
#include "GameplayTagContainer.h"

PRAGMA_DISABLE_DEPRECATION_WARNINGS
static_assert(!UE_WITH_CONSTINIT_UOBJECT, "This generated code can only be compiled with !UE_WITH_CONSTINIT_OBJECT");
void EmptyLinkFunctionForGeneratedCodeUILayerPriorityHelper() {}

// ********** Begin Cross Module References ********************************************************
ENGINE_API UClass* Z_Construct_UClass_APlayerController_NoRegister();
ENGINE_API UClass* Z_Construct_UClass_UBlueprintFunctionLibrary();
GAMEPLAYTAGS_API UScriptStruct* Z_Construct_UScriptStruct_FGameplayTag();
GENERICUISYSTEMEXTENSION_API UClass* Z_Construct_UClass_UUILayerPriorityHelper();
GENERICUISYSTEMEXTENSION_API UClass* Z_Construct_UClass_UUILayerPriorityHelper_NoRegister();
UPackage* Z_Construct_UPackage__Script_GenericUISystemExtension();
// ********** End Cross Module References **********************************************************

// ********** Begin Class UUILayerPriorityHelper Function CanOpenUILayer ***************************
struct Z_Construct_UFunction_UUILayerPriorityHelper_CanOpenUILayer_Statics
{
	struct UILayerPriorityHelper_eventCanOpenUILayer_Parms
	{
		const APlayerController* PC;
		FGameplayTag TargetLayerTag;
		bool ReturnValue;
	};
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Function_MetaDataParams[] = {
		{ "Category", "UI|Layer" },
		{ "ModuleRelativePath", "Public/Utilities/UILayerPriorityHelper.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_PC_MetaData[] = {
		{ "NativeConst", "" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_TargetLayerTag_MetaData[] = {
		{ "NativeConst", "" },
	};
#endif // WITH_METADATA

// ********** Begin Function CanOpenUILayer constinit property declarations ************************
	static const UECodeGen_Private::FObjectPropertyParams NewProp_PC;
	static const UECodeGen_Private::FStructPropertyParams NewProp_TargetLayerTag;
	static void NewProp_ReturnValue_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_ReturnValue;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
// ********** End Function CanOpenUILayer constinit property declarations **************************
	static const UECodeGen_Private::FFunctionParams FuncParams;
};

// ********** Begin Function CanOpenUILayer Property Definitions ***********************************
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_UUILayerPriorityHelper_CanOpenUILayer_Statics::NewProp_PC = { "PC", nullptr, (EPropertyFlags)0x0010000000000082, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UILayerPriorityHelper_eventCanOpenUILayer_Parms, PC), Z_Construct_UClass_APlayerController_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_PC_MetaData), NewProp_PC_MetaData) };
const UECodeGen_Private::FStructPropertyParams Z_Construct_UFunction_UUILayerPriorityHelper_CanOpenUILayer_Statics::NewProp_TargetLayerTag = { "TargetLayerTag", nullptr, (EPropertyFlags)0x0010000008000182, UECodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UILayerPriorityHelper_eventCanOpenUILayer_Parms, TargetLayerTag), Z_Construct_UScriptStruct_FGameplayTag, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_TargetLayerTag_MetaData), NewProp_TargetLayerTag_MetaData) }; // 517357616
void Z_Construct_UFunction_UUILayerPriorityHelper_CanOpenUILayer_Statics::NewProp_ReturnValue_SetBit(void* Obj)
{
	((UILayerPriorityHelper_eventCanOpenUILayer_Parms*)Obj)->ReturnValue = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UFunction_UUILayerPriorityHelper_CanOpenUILayer_Statics::NewProp_ReturnValue = { "ReturnValue", nullptr, (EPropertyFlags)0x0010000000000580, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(UILayerPriorityHelper_eventCanOpenUILayer_Parms), &Z_Construct_UFunction_UUILayerPriorityHelper_CanOpenUILayer_Statics::NewProp_ReturnValue_SetBit, METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_UUILayerPriorityHelper_CanOpenUILayer_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UUILayerPriorityHelper_CanOpenUILayer_Statics::NewProp_PC,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UUILayerPriorityHelper_CanOpenUILayer_Statics::NewProp_TargetLayerTag,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UUILayerPriorityHelper_CanOpenUILayer_Statics::NewProp_ReturnValue,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UFunction_UUILayerPriorityHelper_CanOpenUILayer_Statics::PropPointers) < 2048);
// ********** End Function CanOpenUILayer Property Definitions *************************************
const UECodeGen_Private::FFunctionParams Z_Construct_UFunction_UUILayerPriorityHelper_CanOpenUILayer_Statics::FuncParams = { { (UObject*(*)())Z_Construct_UClass_UUILayerPriorityHelper, nullptr, "CanOpenUILayer", 	Z_Construct_UFunction_UUILayerPriorityHelper_CanOpenUILayer_Statics::PropPointers, 
	UE_ARRAY_COUNT(Z_Construct_UFunction_UUILayerPriorityHelper_CanOpenUILayer_Statics::PropPointers), 
sizeof(Z_Construct_UFunction_UUILayerPriorityHelper_CanOpenUILayer_Statics::UILayerPriorityHelper_eventCanOpenUILayer_Parms),
RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x04422401, 0, 0, METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UFunction_UUILayerPriorityHelper_CanOpenUILayer_Statics::Function_MetaDataParams), Z_Construct_UFunction_UUILayerPriorityHelper_CanOpenUILayer_Statics::Function_MetaDataParams)},  };
static_assert(sizeof(Z_Construct_UFunction_UUILayerPriorityHelper_CanOpenUILayer_Statics::UILayerPriorityHelper_eventCanOpenUILayer_Parms) < MAX_uint16);
UFunction* Z_Construct_UFunction_UUILayerPriorityHelper_CanOpenUILayer()
{
	static UFunction* ReturnFunction = nullptr;
	if (!ReturnFunction)
	{
		UECodeGen_Private::ConstructUFunction(&ReturnFunction, Z_Construct_UFunction_UUILayerPriorityHelper_CanOpenUILayer_Statics::FuncParams);
	}
	return ReturnFunction;
}
DEFINE_FUNCTION(UUILayerPriorityHelper::execCanOpenUILayer)
{
	P_GET_OBJECT(APlayerController,Z_Param_PC);
	P_GET_STRUCT_REF(FGameplayTag,Z_Param_Out_TargetLayerTag);
	P_FINISH;
	P_NATIVE_BEGIN;
	*(bool*)Z_Param__Result=UUILayerPriorityHelper::CanOpenUILayer(Z_Param_PC,Z_Param_Out_TargetLayerTag);
	P_NATIVE_END;
}
// ********** End Class UUILayerPriorityHelper Function CanOpenUILayer *****************************

// ********** Begin Class UUILayerPriorityHelper Function GetHighestActiveLayerTag *****************
struct Z_Construct_UFunction_UUILayerPriorityHelper_GetHighestActiveLayerTag_Statics
{
	struct UILayerPriorityHelper_eventGetHighestActiveLayerTag_Parms
	{
		const APlayerController* PC;
		FGameplayTag ReturnValue;
	};
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Function_MetaDataParams[] = {
		{ "Category", "UI|Layer" },
		{ "ModuleRelativePath", "Public/Utilities/UILayerPriorityHelper.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_PC_MetaData[] = {
		{ "NativeConst", "" },
	};
#endif // WITH_METADATA

// ********** Begin Function GetHighestActiveLayerTag constinit property declarations **************
	static const UECodeGen_Private::FObjectPropertyParams NewProp_PC;
	static const UECodeGen_Private::FStructPropertyParams NewProp_ReturnValue;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
// ********** End Function GetHighestActiveLayerTag constinit property declarations ****************
	static const UECodeGen_Private::FFunctionParams FuncParams;
};

// ********** Begin Function GetHighestActiveLayerTag Property Definitions *************************
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_UUILayerPriorityHelper_GetHighestActiveLayerTag_Statics::NewProp_PC = { "PC", nullptr, (EPropertyFlags)0x0010000000000082, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UILayerPriorityHelper_eventGetHighestActiveLayerTag_Parms, PC), Z_Construct_UClass_APlayerController_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_PC_MetaData), NewProp_PC_MetaData) };
const UECodeGen_Private::FStructPropertyParams Z_Construct_UFunction_UUILayerPriorityHelper_GetHighestActiveLayerTag_Statics::NewProp_ReturnValue = { "ReturnValue", nullptr, (EPropertyFlags)0x0010000000000580, UECodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UILayerPriorityHelper_eventGetHighestActiveLayerTag_Parms, ReturnValue), Z_Construct_UScriptStruct_FGameplayTag, METADATA_PARAMS(0, nullptr) }; // 517357616
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_UUILayerPriorityHelper_GetHighestActiveLayerTag_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UUILayerPriorityHelper_GetHighestActiveLayerTag_Statics::NewProp_PC,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UUILayerPriorityHelper_GetHighestActiveLayerTag_Statics::NewProp_ReturnValue,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UFunction_UUILayerPriorityHelper_GetHighestActiveLayerTag_Statics::PropPointers) < 2048);
// ********** End Function GetHighestActiveLayerTag Property Definitions ***************************
const UECodeGen_Private::FFunctionParams Z_Construct_UFunction_UUILayerPriorityHelper_GetHighestActiveLayerTag_Statics::FuncParams = { { (UObject*(*)())Z_Construct_UClass_UUILayerPriorityHelper, nullptr, "GetHighestActiveLayerTag", 	Z_Construct_UFunction_UUILayerPriorityHelper_GetHighestActiveLayerTag_Statics::PropPointers, 
	UE_ARRAY_COUNT(Z_Construct_UFunction_UUILayerPriorityHelper_GetHighestActiveLayerTag_Statics::PropPointers), 
sizeof(Z_Construct_UFunction_UUILayerPriorityHelper_GetHighestActiveLayerTag_Statics::UILayerPriorityHelper_eventGetHighestActiveLayerTag_Parms),
RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x04022401, 0, 0, METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UFunction_UUILayerPriorityHelper_GetHighestActiveLayerTag_Statics::Function_MetaDataParams), Z_Construct_UFunction_UUILayerPriorityHelper_GetHighestActiveLayerTag_Statics::Function_MetaDataParams)},  };
static_assert(sizeof(Z_Construct_UFunction_UUILayerPriorityHelper_GetHighestActiveLayerTag_Statics::UILayerPriorityHelper_eventGetHighestActiveLayerTag_Parms) < MAX_uint16);
UFunction* Z_Construct_UFunction_UUILayerPriorityHelper_GetHighestActiveLayerTag()
{
	static UFunction* ReturnFunction = nullptr;
	if (!ReturnFunction)
	{
		UECodeGen_Private::ConstructUFunction(&ReturnFunction, Z_Construct_UFunction_UUILayerPriorityHelper_GetHighestActiveLayerTag_Statics::FuncParams);
	}
	return ReturnFunction;
}
DEFINE_FUNCTION(UUILayerPriorityHelper::execGetHighestActiveLayerTag)
{
	P_GET_OBJECT(APlayerController,Z_Param_PC);
	P_FINISH;
	P_NATIVE_BEGIN;
	*(FGameplayTag*)Z_Param__Result=UUILayerPriorityHelper::GetHighestActiveLayerTag(Z_Param_PC);
	P_NATIVE_END;
}
// ********** End Class UUILayerPriorityHelper Function GetHighestActiveLayerTag *******************

// ********** Begin Class UUILayerPriorityHelper Function GetLayerPriority *************************
struct Z_Construct_UFunction_UUILayerPriorityHelper_GetLayerPriority_Statics
{
	struct UILayerPriorityHelper_eventGetLayerPriority_Parms
	{
		FGameplayTag LayerTag;
		int32 ReturnValue;
	};
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Function_MetaDataParams[] = {
		{ "Category", "UI|Layer" },
		{ "ModuleRelativePath", "Public/Utilities/UILayerPriorityHelper.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_LayerTag_MetaData[] = {
		{ "NativeConst", "" },
	};
#endif // WITH_METADATA

// ********** Begin Function GetLayerPriority constinit property declarations **********************
	static const UECodeGen_Private::FStructPropertyParams NewProp_LayerTag;
	static const UECodeGen_Private::FIntPropertyParams NewProp_ReturnValue;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
// ********** End Function GetLayerPriority constinit property declarations ************************
	static const UECodeGen_Private::FFunctionParams FuncParams;
};

// ********** Begin Function GetLayerPriority Property Definitions *********************************
const UECodeGen_Private::FStructPropertyParams Z_Construct_UFunction_UUILayerPriorityHelper_GetLayerPriority_Statics::NewProp_LayerTag = { "LayerTag", nullptr, (EPropertyFlags)0x0010000008000182, UECodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UILayerPriorityHelper_eventGetLayerPriority_Parms, LayerTag), Z_Construct_UScriptStruct_FGameplayTag, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_LayerTag_MetaData), NewProp_LayerTag_MetaData) }; // 517357616
const UECodeGen_Private::FIntPropertyParams Z_Construct_UFunction_UUILayerPriorityHelper_GetLayerPriority_Statics::NewProp_ReturnValue = { "ReturnValue", nullptr, (EPropertyFlags)0x0010000000000580, UECodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UILayerPriorityHelper_eventGetLayerPriority_Parms, ReturnValue), METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_UUILayerPriorityHelper_GetLayerPriority_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UUILayerPriorityHelper_GetLayerPriority_Statics::NewProp_LayerTag,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UUILayerPriorityHelper_GetLayerPriority_Statics::NewProp_ReturnValue,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UFunction_UUILayerPriorityHelper_GetLayerPriority_Statics::PropPointers) < 2048);
// ********** End Function GetLayerPriority Property Definitions ***********************************
const UECodeGen_Private::FFunctionParams Z_Construct_UFunction_UUILayerPriorityHelper_GetLayerPriority_Statics::FuncParams = { { (UObject*(*)())Z_Construct_UClass_UUILayerPriorityHelper, nullptr, "GetLayerPriority", 	Z_Construct_UFunction_UUILayerPriorityHelper_GetLayerPriority_Statics::PropPointers, 
	UE_ARRAY_COUNT(Z_Construct_UFunction_UUILayerPriorityHelper_GetLayerPriority_Statics::PropPointers), 
sizeof(Z_Construct_UFunction_UUILayerPriorityHelper_GetLayerPriority_Statics::UILayerPriorityHelper_eventGetLayerPriority_Parms),
RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x04422401, 0, 0, METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UFunction_UUILayerPriorityHelper_GetLayerPriority_Statics::Function_MetaDataParams), Z_Construct_UFunction_UUILayerPriorityHelper_GetLayerPriority_Statics::Function_MetaDataParams)},  };
static_assert(sizeof(Z_Construct_UFunction_UUILayerPriorityHelper_GetLayerPriority_Statics::UILayerPriorityHelper_eventGetLayerPriority_Parms) < MAX_uint16);
UFunction* Z_Construct_UFunction_UUILayerPriorityHelper_GetLayerPriority()
{
	static UFunction* ReturnFunction = nullptr;
	if (!ReturnFunction)
	{
		UECodeGen_Private::ConstructUFunction(&ReturnFunction, Z_Construct_UFunction_UUILayerPriorityHelper_GetLayerPriority_Statics::FuncParams);
	}
	return ReturnFunction;
}
DEFINE_FUNCTION(UUILayerPriorityHelper::execGetLayerPriority)
{
	P_GET_STRUCT_REF(FGameplayTag,Z_Param_Out_LayerTag);
	P_FINISH;
	P_NATIVE_BEGIN;
	*(int32*)Z_Param__Result=UUILayerPriorityHelper::GetLayerPriority(Z_Param_Out_LayerTag);
	P_NATIVE_END;
}
// ********** End Class UUILayerPriorityHelper Function GetLayerPriority ***************************

// ********** Begin Class UUILayerPriorityHelper Function HasHigherPriorityActiveLayer *************
struct Z_Construct_UFunction_UUILayerPriorityHelper_HasHigherPriorityActiveLayer_Statics
{
	struct UILayerPriorityHelper_eventHasHigherPriorityActiveLayer_Parms
	{
		const APlayerController* PC;
		FGameplayTag TargetLayerTag;
		bool ReturnValue;
	};
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Function_MetaDataParams[] = {
		{ "Category", "UI|Layer" },
		{ "ModuleRelativePath", "Public/Utilities/UILayerPriorityHelper.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_PC_MetaData[] = {
		{ "NativeConst", "" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_TargetLayerTag_MetaData[] = {
		{ "NativeConst", "" },
	};
#endif // WITH_METADATA

// ********** Begin Function HasHigherPriorityActiveLayer constinit property declarations **********
	static const UECodeGen_Private::FObjectPropertyParams NewProp_PC;
	static const UECodeGen_Private::FStructPropertyParams NewProp_TargetLayerTag;
	static void NewProp_ReturnValue_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_ReturnValue;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
// ********** End Function HasHigherPriorityActiveLayer constinit property declarations ************
	static const UECodeGen_Private::FFunctionParams FuncParams;
};

// ********** Begin Function HasHigherPriorityActiveLayer Property Definitions *********************
const UECodeGen_Private::FObjectPropertyParams Z_Construct_UFunction_UUILayerPriorityHelper_HasHigherPriorityActiveLayer_Statics::NewProp_PC = { "PC", nullptr, (EPropertyFlags)0x0010000000000082, UECodeGen_Private::EPropertyGenFlags::Object, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UILayerPriorityHelper_eventHasHigherPriorityActiveLayer_Parms, PC), Z_Construct_UClass_APlayerController_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_PC_MetaData), NewProp_PC_MetaData) };
const UECodeGen_Private::FStructPropertyParams Z_Construct_UFunction_UUILayerPriorityHelper_HasHigherPriorityActiveLayer_Statics::NewProp_TargetLayerTag = { "TargetLayerTag", nullptr, (EPropertyFlags)0x0010000008000182, UECodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UILayerPriorityHelper_eventHasHigherPriorityActiveLayer_Parms, TargetLayerTag), Z_Construct_UScriptStruct_FGameplayTag, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_TargetLayerTag_MetaData), NewProp_TargetLayerTag_MetaData) }; // 517357616
void Z_Construct_UFunction_UUILayerPriorityHelper_HasHigherPriorityActiveLayer_Statics::NewProp_ReturnValue_SetBit(void* Obj)
{
	((UILayerPriorityHelper_eventHasHigherPriorityActiveLayer_Parms*)Obj)->ReturnValue = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UFunction_UUILayerPriorityHelper_HasHigherPriorityActiveLayer_Statics::NewProp_ReturnValue = { "ReturnValue", nullptr, (EPropertyFlags)0x0010000000000580, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(UILayerPriorityHelper_eventHasHigherPriorityActiveLayer_Parms), &Z_Construct_UFunction_UUILayerPriorityHelper_HasHigherPriorityActiveLayer_Statics::NewProp_ReturnValue_SetBit, METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_UUILayerPriorityHelper_HasHigherPriorityActiveLayer_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UUILayerPriorityHelper_HasHigherPriorityActiveLayer_Statics::NewProp_PC,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UUILayerPriorityHelper_HasHigherPriorityActiveLayer_Statics::NewProp_TargetLayerTag,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UUILayerPriorityHelper_HasHigherPriorityActiveLayer_Statics::NewProp_ReturnValue,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UFunction_UUILayerPriorityHelper_HasHigherPriorityActiveLayer_Statics::PropPointers) < 2048);
// ********** End Function HasHigherPriorityActiveLayer Property Definitions ***********************
const UECodeGen_Private::FFunctionParams Z_Construct_UFunction_UUILayerPriorityHelper_HasHigherPriorityActiveLayer_Statics::FuncParams = { { (UObject*(*)())Z_Construct_UClass_UUILayerPriorityHelper, nullptr, "HasHigherPriorityActiveLayer", 	Z_Construct_UFunction_UUILayerPriorityHelper_HasHigherPriorityActiveLayer_Statics::PropPointers, 
	UE_ARRAY_COUNT(Z_Construct_UFunction_UUILayerPriorityHelper_HasHigherPriorityActiveLayer_Statics::PropPointers), 
sizeof(Z_Construct_UFunction_UUILayerPriorityHelper_HasHigherPriorityActiveLayer_Statics::UILayerPriorityHelper_eventHasHigherPriorityActiveLayer_Parms),
RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x04422401, 0, 0, METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UFunction_UUILayerPriorityHelper_HasHigherPriorityActiveLayer_Statics::Function_MetaDataParams), Z_Construct_UFunction_UUILayerPriorityHelper_HasHigherPriorityActiveLayer_Statics::Function_MetaDataParams)},  };
static_assert(sizeof(Z_Construct_UFunction_UUILayerPriorityHelper_HasHigherPriorityActiveLayer_Statics::UILayerPriorityHelper_eventHasHigherPriorityActiveLayer_Parms) < MAX_uint16);
UFunction* Z_Construct_UFunction_UUILayerPriorityHelper_HasHigherPriorityActiveLayer()
{
	static UFunction* ReturnFunction = nullptr;
	if (!ReturnFunction)
	{
		UECodeGen_Private::ConstructUFunction(&ReturnFunction, Z_Construct_UFunction_UUILayerPriorityHelper_HasHigherPriorityActiveLayer_Statics::FuncParams);
	}
	return ReturnFunction;
}
DEFINE_FUNCTION(UUILayerPriorityHelper::execHasHigherPriorityActiveLayer)
{
	P_GET_OBJECT(APlayerController,Z_Param_PC);
	P_GET_STRUCT_REF(FGameplayTag,Z_Param_Out_TargetLayerTag);
	P_FINISH;
	P_NATIVE_BEGIN;
	*(bool*)Z_Param__Result=UUILayerPriorityHelper::HasHigherPriorityActiveLayer(Z_Param_PC,Z_Param_Out_TargetLayerTag);
	P_NATIVE_END;
}
// ********** End Class UUILayerPriorityHelper Function HasHigherPriorityActiveLayer ***************

// ********** Begin Class UUILayerPriorityHelper ***************************************************
FClassRegistrationInfo Z_Registration_Info_UClass_UUILayerPriorityHelper;
UClass* UUILayerPriorityHelper::GetPrivateStaticClass()
{
	using TClass = UUILayerPriorityHelper;
	if (!Z_Registration_Info_UClass_UUILayerPriorityHelper.InnerSingleton)
	{
		GetPrivateStaticClassBody(
			TClass::StaticPackage(),
			TEXT("UILayerPriorityHelper"),
			Z_Registration_Info_UClass_UUILayerPriorityHelper.InnerSingleton,
			StaticRegisterNativesUUILayerPriorityHelper,
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
	return Z_Registration_Info_UClass_UUILayerPriorityHelper.InnerSingleton;
}
UClass* Z_Construct_UClass_UUILayerPriorityHelper_NoRegister()
{
	return UUILayerPriorityHelper::GetPrivateStaticClass();
}
struct Z_Construct_UClass_UUILayerPriorityHelper_Statics
{
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Class_MetaDataParams[] = {
#if !UE_BUILD_SHIPPING
		{ "Comment", "/**\n * Static utility class for UI layer priority operations.\n * \n * Layer Priority Order (lowest to highest):\n * - Game (0): HUD elements, always-visible UI\n * - GameMenu (1): In-game menus like inventory\n * - Menu (2): Full menus like settings\n * - Modal (3): Dialogs, confirmations, highest priority\n */" },
#endif
		{ "IncludePath", "Utilities/UILayerPriorityHelper.h" },
		{ "ModuleRelativePath", "Public/Utilities/UILayerPriorityHelper.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Static utility class for UI layer priority operations.\n\nLayer Priority Order (lowest to highest):\n- Game (0): HUD elements, always-visible UI\n- GameMenu (1): In-game menus like inventory\n- Menu (2): Full menus like settings\n- Modal (3): Dialogs, confirmations, highest priority" },
#endif
	};
#endif // WITH_METADATA

// ********** Begin Class UUILayerPriorityHelper constinit property declarations *******************
// ********** End Class UUILayerPriorityHelper constinit property declarations *********************
	static constexpr UE::CodeGen::FClassNativeFunction Funcs[] = {
		{ .NameUTF8 = UTF8TEXT("CanOpenUILayer"), .Pointer = &UUILayerPriorityHelper::execCanOpenUILayer },
		{ .NameUTF8 = UTF8TEXT("GetHighestActiveLayerTag"), .Pointer = &UUILayerPriorityHelper::execGetHighestActiveLayerTag },
		{ .NameUTF8 = UTF8TEXT("GetLayerPriority"), .Pointer = &UUILayerPriorityHelper::execGetLayerPriority },
		{ .NameUTF8 = UTF8TEXT("HasHigherPriorityActiveLayer"), .Pointer = &UUILayerPriorityHelper::execHasHigherPriorityActiveLayer },
	};
	static UObject* (*const DependentSingletons[])();
	static constexpr FClassFunctionLinkInfo FuncInfo[] = {
		{ &Z_Construct_UFunction_UUILayerPriorityHelper_CanOpenUILayer, "CanOpenUILayer" }, // 2019999416
		{ &Z_Construct_UFunction_UUILayerPriorityHelper_GetHighestActiveLayerTag, "GetHighestActiveLayerTag" }, // 3561711524
		{ &Z_Construct_UFunction_UUILayerPriorityHelper_GetLayerPriority, "GetLayerPriority" }, // 3508106206
		{ &Z_Construct_UFunction_UUILayerPriorityHelper_HasHigherPriorityActiveLayer, "HasHigherPriorityActiveLayer" }, // 827506628
	};
	static_assert(UE_ARRAY_COUNT(FuncInfo) < 2048);
	static constexpr FCppClassTypeInfoStatic StaticCppClassTypeInfo = {
		TCppClassTypeTraits<UUILayerPriorityHelper>::IsAbstract,
	};
	static const UECodeGen_Private::FClassParams ClassParams;
}; // struct Z_Construct_UClass_UUILayerPriorityHelper_Statics
UObject* (*const Z_Construct_UClass_UUILayerPriorityHelper_Statics::DependentSingletons[])() = {
	(UObject* (*)())Z_Construct_UClass_UBlueprintFunctionLibrary,
	(UObject* (*)())Z_Construct_UPackage__Script_GenericUISystemExtension,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_UUILayerPriorityHelper_Statics::DependentSingletons) < 16);
const UECodeGen_Private::FClassParams Z_Construct_UClass_UUILayerPriorityHelper_Statics::ClassParams = {
	&UUILayerPriorityHelper::StaticClass,
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
	METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UClass_UUILayerPriorityHelper_Statics::Class_MetaDataParams), Z_Construct_UClass_UUILayerPriorityHelper_Statics::Class_MetaDataParams)
};
void UUILayerPriorityHelper::StaticRegisterNativesUUILayerPriorityHelper()
{
	UClass* Class = UUILayerPriorityHelper::StaticClass();
	FNativeFunctionRegistrar::RegisterFunctions(Class, MakeConstArrayView(Z_Construct_UClass_UUILayerPriorityHelper_Statics::Funcs));
}
UClass* Z_Construct_UClass_UUILayerPriorityHelper()
{
	if (!Z_Registration_Info_UClass_UUILayerPriorityHelper.OuterSingleton)
	{
		UECodeGen_Private::ConstructUClass(Z_Registration_Info_UClass_UUILayerPriorityHelper.OuterSingleton, Z_Construct_UClass_UUILayerPriorityHelper_Statics::ClassParams);
	}
	return Z_Registration_Info_UClass_UUILayerPriorityHelper.OuterSingleton;
}
UUILayerPriorityHelper::UUILayerPriorityHelper(const FObjectInitializer& ObjectInitializer) : Super(ObjectInitializer) {}
DEFINE_VTABLE_PTR_HELPER_CTOR_NS(, UUILayerPriorityHelper);
UUILayerPriorityHelper::~UUILayerPriorityHelper() {}
// ********** End Class UUILayerPriorityHelper *****************************************************

// ********** Begin Registration *******************************************************************
struct Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Utilities_UILayerPriorityHelper_h__Script_GenericUISystemExtension_Statics
{
	static constexpr FClassRegisterCompiledInInfo ClassInfo[] = {
		{ Z_Construct_UClass_UUILayerPriorityHelper, UUILayerPriorityHelper::StaticClass, TEXT("UUILayerPriorityHelper"), &Z_Registration_Info_UClass_UUILayerPriorityHelper, CONSTRUCT_RELOAD_VERSION_INFO(FClassReloadVersionInfo, sizeof(UUILayerPriorityHelper), 567775032U) },
	};
}; // Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Utilities_UILayerPriorityHelper_h__Script_GenericUISystemExtension_Statics 
static FRegisterCompiledInInfo Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Utilities_UILayerPriorityHelper_h__Script_GenericUISystemExtension_804110259{
	TEXT("/Script/GenericUISystemExtension"),
	Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Utilities_UILayerPriorityHelper_h__Script_GenericUISystemExtension_Statics::ClassInfo, UE_ARRAY_COUNT(Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Utilities_UILayerPriorityHelper_h__Script_GenericUISystemExtension_Statics::ClassInfo),
	nullptr, 0,
	nullptr, 0,
};
// ********** End Registration *********************************************************************

PRAGMA_ENABLE_DEPRECATION_WARNINGS
