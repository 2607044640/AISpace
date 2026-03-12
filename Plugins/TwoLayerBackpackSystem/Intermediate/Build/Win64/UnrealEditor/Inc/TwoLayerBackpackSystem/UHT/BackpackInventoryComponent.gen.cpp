// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "BackpackInventoryComponent.h"
#include "GameplayTagContainer.h"

PRAGMA_DISABLE_DEPRECATION_WARNINGS
static_assert(!UE_WITH_CONSTINIT_UOBJECT, "This generated code can only be compiled with !UE_WITH_CONSTINIT_OBJECT");
void EmptyLinkFunctionForGeneratedCodeBackpackInventoryComponent() {}

// ********** Begin Cross Module References ********************************************************
COREUOBJECT_API UClass* Z_Construct_UClass_UClass_NoRegister();
ENGINE_API UClass* Z_Construct_UClass_UActorComponent();
GAMEPLAYTAGS_API UScriptStruct* Z_Construct_UScriptStruct_FGameplayTag();
TWOLAYERBACKPACKSYSTEM_API UClass* Z_Construct_UClass_UBackpackInventoryComponent();
TWOLAYERBACKPACKSYSTEM_API UClass* Z_Construct_UClass_UBackpackInventoryComponent_NoRegister();
TWOLAYERBACKPACKSYSTEM_API UClass* Z_Construct_UClass_UBackpackWidget_NoRegister();
UPackage* Z_Construct_UPackage__Script_TwoLayerBackpackSystem();
// ********** End Cross Module References **********************************************************

// ********** Begin Class UBackpackInventoryComponent Function IsBackpackOpen **********************
struct Z_Construct_UFunction_UBackpackInventoryComponent_IsBackpackOpen_Statics
{
	struct BackpackInventoryComponent_eventIsBackpackOpen_Parms
	{
		bool ReturnValue;
	};
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Function_MetaDataParams[] = {
		{ "Category", "Backpack" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// Check if backpack is currently open\n" },
#endif
		{ "ModuleRelativePath", "Public/BackpackInventoryComponent.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Check if backpack is currently open" },
#endif
	};
#endif // WITH_METADATA

// ********** Begin Function IsBackpackOpen constinit property declarations ************************
	static void NewProp_ReturnValue_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_ReturnValue;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
// ********** End Function IsBackpackOpen constinit property declarations **************************
	static const UECodeGen_Private::FFunctionParams FuncParams;
};

// ********** Begin Function IsBackpackOpen Property Definitions ***********************************
void Z_Construct_UFunction_UBackpackInventoryComponent_IsBackpackOpen_Statics::NewProp_ReturnValue_SetBit(void* Obj)
{
	((BackpackInventoryComponent_eventIsBackpackOpen_Parms*)Obj)->ReturnValue = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UFunction_UBackpackInventoryComponent_IsBackpackOpen_Statics::NewProp_ReturnValue = { "ReturnValue", nullptr, (EPropertyFlags)0x0010000000000580, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(BackpackInventoryComponent_eventIsBackpackOpen_Parms), &Z_Construct_UFunction_UBackpackInventoryComponent_IsBackpackOpen_Statics::NewProp_ReturnValue_SetBit, METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_UBackpackInventoryComponent_IsBackpackOpen_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBackpackInventoryComponent_IsBackpackOpen_Statics::NewProp_ReturnValue,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UFunction_UBackpackInventoryComponent_IsBackpackOpen_Statics::PropPointers) < 2048);
// ********** End Function IsBackpackOpen Property Definitions *************************************
const UECodeGen_Private::FFunctionParams Z_Construct_UFunction_UBackpackInventoryComponent_IsBackpackOpen_Statics::FuncParams = { { (UObject*(*)())Z_Construct_UClass_UBackpackInventoryComponent, nullptr, "IsBackpackOpen", 	Z_Construct_UFunction_UBackpackInventoryComponent_IsBackpackOpen_Statics::PropPointers, 
	UE_ARRAY_COUNT(Z_Construct_UFunction_UBackpackInventoryComponent_IsBackpackOpen_Statics::PropPointers), 
sizeof(Z_Construct_UFunction_UBackpackInventoryComponent_IsBackpackOpen_Statics::BackpackInventoryComponent_eventIsBackpackOpen_Parms),
RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x54020401, 0, 0, METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UFunction_UBackpackInventoryComponent_IsBackpackOpen_Statics::Function_MetaDataParams), Z_Construct_UFunction_UBackpackInventoryComponent_IsBackpackOpen_Statics::Function_MetaDataParams)},  };
static_assert(sizeof(Z_Construct_UFunction_UBackpackInventoryComponent_IsBackpackOpen_Statics::BackpackInventoryComponent_eventIsBackpackOpen_Parms) < MAX_uint16);
UFunction* Z_Construct_UFunction_UBackpackInventoryComponent_IsBackpackOpen()
{
	static UFunction* ReturnFunction = nullptr;
	if (!ReturnFunction)
	{
		UECodeGen_Private::ConstructUFunction(&ReturnFunction, Z_Construct_UFunction_UBackpackInventoryComponent_IsBackpackOpen_Statics::FuncParams);
	}
	return ReturnFunction;
}
DEFINE_FUNCTION(UBackpackInventoryComponent::execIsBackpackOpen)
{
	P_FINISH;
	P_NATIVE_BEGIN;
	*(bool*)Z_Param__Result=P_THIS->IsBackpackOpen();
	P_NATIVE_END;
}
// ********** End Class UBackpackInventoryComponent Function IsBackpackOpen ************************

// ********** Begin Class UBackpackInventoryComponent Function OpenBackpackInventory ***************
struct Z_Construct_UFunction_UBackpackInventoryComponent_OpenBackpackInventory_Statics
{
	struct BackpackInventoryComponent_eventOpenBackpackInventory_Parms
	{
		bool ReturnValue;
	};
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Function_MetaDataParams[] = {
		{ "Category", "Backpack" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// Open backpack UI (replaces ToggleInventory)\n// Returns false if already open or blocked by higher priority layer\n" },
#endif
		{ "ModuleRelativePath", "Public/BackpackInventoryComponent.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Open backpack UI (replaces ToggleInventory)\nReturns false if already open or blocked by higher priority layer" },
#endif
	};
#endif // WITH_METADATA

// ********** Begin Function OpenBackpackInventory constinit property declarations *****************
	static void NewProp_ReturnValue_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_ReturnValue;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
// ********** End Function OpenBackpackInventory constinit property declarations *******************
	static const UECodeGen_Private::FFunctionParams FuncParams;
};

// ********** Begin Function OpenBackpackInventory Property Definitions ****************************
void Z_Construct_UFunction_UBackpackInventoryComponent_OpenBackpackInventory_Statics::NewProp_ReturnValue_SetBit(void* Obj)
{
	((BackpackInventoryComponent_eventOpenBackpackInventory_Parms*)Obj)->ReturnValue = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UFunction_UBackpackInventoryComponent_OpenBackpackInventory_Statics::NewProp_ReturnValue = { "ReturnValue", nullptr, (EPropertyFlags)0x0010000000000580, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(BackpackInventoryComponent_eventOpenBackpackInventory_Parms), &Z_Construct_UFunction_UBackpackInventoryComponent_OpenBackpackInventory_Statics::NewProp_ReturnValue_SetBit, METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UFunction_UBackpackInventoryComponent_OpenBackpackInventory_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UFunction_UBackpackInventoryComponent_OpenBackpackInventory_Statics::NewProp_ReturnValue,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UFunction_UBackpackInventoryComponent_OpenBackpackInventory_Statics::PropPointers) < 2048);
// ********** End Function OpenBackpackInventory Property Definitions ******************************
const UECodeGen_Private::FFunctionParams Z_Construct_UFunction_UBackpackInventoryComponent_OpenBackpackInventory_Statics::FuncParams = { { (UObject*(*)())Z_Construct_UClass_UBackpackInventoryComponent, nullptr, "OpenBackpackInventory", 	Z_Construct_UFunction_UBackpackInventoryComponent_OpenBackpackInventory_Statics::PropPointers, 
	UE_ARRAY_COUNT(Z_Construct_UFunction_UBackpackInventoryComponent_OpenBackpackInventory_Statics::PropPointers), 
sizeof(Z_Construct_UFunction_UBackpackInventoryComponent_OpenBackpackInventory_Statics::BackpackInventoryComponent_eventOpenBackpackInventory_Parms),
RF_Public|RF_Transient|RF_MarkAsNative, (EFunctionFlags)0x04020401, 0, 0, METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UFunction_UBackpackInventoryComponent_OpenBackpackInventory_Statics::Function_MetaDataParams), Z_Construct_UFunction_UBackpackInventoryComponent_OpenBackpackInventory_Statics::Function_MetaDataParams)},  };
static_assert(sizeof(Z_Construct_UFunction_UBackpackInventoryComponent_OpenBackpackInventory_Statics::BackpackInventoryComponent_eventOpenBackpackInventory_Parms) < MAX_uint16);
UFunction* Z_Construct_UFunction_UBackpackInventoryComponent_OpenBackpackInventory()
{
	static UFunction* ReturnFunction = nullptr;
	if (!ReturnFunction)
	{
		UECodeGen_Private::ConstructUFunction(&ReturnFunction, Z_Construct_UFunction_UBackpackInventoryComponent_OpenBackpackInventory_Statics::FuncParams);
	}
	return ReturnFunction;
}
DEFINE_FUNCTION(UBackpackInventoryComponent::execOpenBackpackInventory)
{
	P_FINISH;
	P_NATIVE_BEGIN;
	*(bool*)Z_Param__Result=P_THIS->OpenBackpackInventory();
	P_NATIVE_END;
}
// ********** End Class UBackpackInventoryComponent Function OpenBackpackInventory *****************

// ********** Begin Class UBackpackInventoryComponent **********************************************
FClassRegistrationInfo Z_Registration_Info_UClass_UBackpackInventoryComponent;
UClass* UBackpackInventoryComponent::GetPrivateStaticClass()
{
	using TClass = UBackpackInventoryComponent;
	if (!Z_Registration_Info_UClass_UBackpackInventoryComponent.InnerSingleton)
	{
		GetPrivateStaticClassBody(
			TClass::StaticPackage(),
			TEXT("BackpackInventoryComponent"),
			Z_Registration_Info_UClass_UBackpackInventoryComponent.InnerSingleton,
			StaticRegisterNativesUBackpackInventoryComponent,
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
	return Z_Registration_Info_UClass_UBackpackInventoryComponent.InnerSingleton;
}
UClass* Z_Construct_UClass_UBackpackInventoryComponent_NoRegister()
{
	return UBackpackInventoryComponent::GetPrivateStaticClass();
}
struct Z_Construct_UClass_UBackpackInventoryComponent_Statics
{
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Class_MetaDataParams[] = {
		{ "BlueprintSpawnableComponent", "" },
		{ "BlueprintType", "true" },
		{ "ClassGroupNames", "Custom" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "/**\n * Component for managing backpack/inventory UI.\n * \n * Uses GenericUISystem for UI layer management:\n * - Push/Pop widget to UI layer stack\n * - Automatic input mode switching (handled by BackpackWidget)\n * - Automatic game pause (handled by BackpackWidget)\n * \n * Usage:\n * 1. Add this component to your character/pawn\n * 2. Set BackpackWidgetClass to your Blueprint widget (derived from UBackpackWidget)\n * 3. Call OpenInventory() to show the backpack (ESC/A key closes it)\n */" },
#endif
		{ "IncludePath", "BackpackInventoryComponent.h" },
		{ "IsBlueprintBase", "true" },
		{ "ModuleRelativePath", "Public/BackpackInventoryComponent.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Component for managing backpack/inventory UI.\n\nUses GenericUISystem for UI layer management:\n- Push/Pop widget to UI layer stack\n- Automatic input mode switching (handled by BackpackWidget)\n- Automatic game pause (handled by BackpackWidget)\n\nUsage:\n1. Add this component to your character/pawn\n2. Set BackpackWidgetClass to your Blueprint widget (derived from UBackpackWidget)\n3. Call OpenInventory() to show the backpack (ESC/A key closes it)" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_BackpackWidgetClass_MetaData[] = {
		{ "Category", "Backpack|UI" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// Backpack widget class (set in Blueprint, must derive from UBackpackWidget)\n" },
#endif
		{ "ModuleRelativePath", "Public/BackpackInventoryComponent.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Backpack widget class (set in Blueprint, must derive from UBackpackWidget)" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_UILayerTag_MetaData[] = {
		{ "Categories", "UI.Layer,GUIS.Layer" },
		{ "Category", "Backpack|UI" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "// UI Layer tag for backpack (default: GUIS.Layer.Menu)\n" },
#endif
		{ "ModuleRelativePath", "Public/BackpackInventoryComponent.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "UI Layer tag for backpack (default: GUIS.Layer.Menu)" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_BackpackWidget_MetaData[] = {
#if !UE_BUILD_SHIPPING
		{ "Comment", "// Current backpack widget instance (nullptr when closed)\n" },
#endif
		{ "ModuleRelativePath", "Public/BackpackInventoryComponent.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Current backpack widget instance (nullptr when closed)" },
#endif
	};
#endif // WITH_METADATA

// ********** Begin Class UBackpackInventoryComponent constinit property declarations **************
	static const UECodeGen_Private::FClassPropertyParams NewProp_BackpackWidgetClass;
	static const UECodeGen_Private::FStructPropertyParams NewProp_UILayerTag;
	static const UECodeGen_Private::FWeakObjectPropertyParams NewProp_BackpackWidget;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
// ********** End Class UBackpackInventoryComponent constinit property declarations ****************
	static constexpr UE::CodeGen::FClassNativeFunction Funcs[] = {
		{ .NameUTF8 = UTF8TEXT("IsBackpackOpen"), .Pointer = &UBackpackInventoryComponent::execIsBackpackOpen },
		{ .NameUTF8 = UTF8TEXT("OpenBackpackInventory"), .Pointer = &UBackpackInventoryComponent::execOpenBackpackInventory },
	};
	static UObject* (*const DependentSingletons[])();
	static constexpr FClassFunctionLinkInfo FuncInfo[] = {
		{ &Z_Construct_UFunction_UBackpackInventoryComponent_IsBackpackOpen, "IsBackpackOpen" }, // 2307544655
		{ &Z_Construct_UFunction_UBackpackInventoryComponent_OpenBackpackInventory, "OpenBackpackInventory" }, // 1500800991
	};
	static_assert(UE_ARRAY_COUNT(FuncInfo) < 2048);
	static constexpr FCppClassTypeInfoStatic StaticCppClassTypeInfo = {
		TCppClassTypeTraits<UBackpackInventoryComponent>::IsAbstract,
	};
	static const UECodeGen_Private::FClassParams ClassParams;
}; // struct Z_Construct_UClass_UBackpackInventoryComponent_Statics

// ********** Begin Class UBackpackInventoryComponent Property Definitions *************************
const UECodeGen_Private::FClassPropertyParams Z_Construct_UClass_UBackpackInventoryComponent_Statics::NewProp_BackpackWidgetClass = { "BackpackWidgetClass", nullptr, (EPropertyFlags)0x0024080000000005, UECodeGen_Private::EPropertyGenFlags::Class, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBackpackInventoryComponent, BackpackWidgetClass), Z_Construct_UClass_UClass_NoRegister, Z_Construct_UClass_UBackpackWidget_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_BackpackWidgetClass_MetaData), NewProp_BackpackWidgetClass_MetaData) };
const UECodeGen_Private::FStructPropertyParams Z_Construct_UClass_UBackpackInventoryComponent_Statics::NewProp_UILayerTag = { "UILayerTag", nullptr, (EPropertyFlags)0x0020080000000005, UECodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBackpackInventoryComponent, UILayerTag), Z_Construct_UScriptStruct_FGameplayTag, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_UILayerTag_MetaData), NewProp_UILayerTag_MetaData) }; // 517357616
const UECodeGen_Private::FWeakObjectPropertyParams Z_Construct_UClass_UBackpackInventoryComponent_Statics::NewProp_BackpackWidget = { "BackpackWidget", nullptr, (EPropertyFlags)0x0044000000080008, UECodeGen_Private::EPropertyGenFlags::WeakObject, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBackpackInventoryComponent, BackpackWidget), Z_Construct_UClass_UBackpackWidget_NoRegister, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_BackpackWidget_MetaData), NewProp_BackpackWidget_MetaData) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UClass_UBackpackInventoryComponent_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBackpackInventoryComponent_Statics::NewProp_BackpackWidgetClass,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBackpackInventoryComponent_Statics::NewProp_UILayerTag,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBackpackInventoryComponent_Statics::NewProp_BackpackWidget,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_UBackpackInventoryComponent_Statics::PropPointers) < 2048);
// ********** End Class UBackpackInventoryComponent Property Definitions ***************************
UObject* (*const Z_Construct_UClass_UBackpackInventoryComponent_Statics::DependentSingletons[])() = {
	(UObject* (*)())Z_Construct_UClass_UActorComponent,
	(UObject* (*)())Z_Construct_UPackage__Script_TwoLayerBackpackSystem,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_UBackpackInventoryComponent_Statics::DependentSingletons) < 16);
const UECodeGen_Private::FClassParams Z_Construct_UClass_UBackpackInventoryComponent_Statics::ClassParams = {
	&UBackpackInventoryComponent::StaticClass,
	"Engine",
	&StaticCppClassTypeInfo,
	DependentSingletons,
	FuncInfo,
	Z_Construct_UClass_UBackpackInventoryComponent_Statics::PropPointers,
	nullptr,
	UE_ARRAY_COUNT(DependentSingletons),
	UE_ARRAY_COUNT(FuncInfo),
	UE_ARRAY_COUNT(Z_Construct_UClass_UBackpackInventoryComponent_Statics::PropPointers),
	0,
	0x00B000A4u,
	METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UClass_UBackpackInventoryComponent_Statics::Class_MetaDataParams), Z_Construct_UClass_UBackpackInventoryComponent_Statics::Class_MetaDataParams)
};
void UBackpackInventoryComponent::StaticRegisterNativesUBackpackInventoryComponent()
{
	UClass* Class = UBackpackInventoryComponent::StaticClass();
	FNativeFunctionRegistrar::RegisterFunctions(Class, MakeConstArrayView(Z_Construct_UClass_UBackpackInventoryComponent_Statics::Funcs));
}
UClass* Z_Construct_UClass_UBackpackInventoryComponent()
{
	if (!Z_Registration_Info_UClass_UBackpackInventoryComponent.OuterSingleton)
	{
		UECodeGen_Private::ConstructUClass(Z_Registration_Info_UClass_UBackpackInventoryComponent.OuterSingleton, Z_Construct_UClass_UBackpackInventoryComponent_Statics::ClassParams);
	}
	return Z_Registration_Info_UClass_UBackpackInventoryComponent.OuterSingleton;
}
DEFINE_VTABLE_PTR_HELPER_CTOR_NS(, UBackpackInventoryComponent);
UBackpackInventoryComponent::~UBackpackInventoryComponent() {}
// ********** End Class UBackpackInventoryComponent ************************************************

// ********** Begin Registration *******************************************************************
struct Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_TwoLayerBackpackSystem_Source_TwoLayerBackpackSystem_Public_BackpackInventoryComponent_h__Script_TwoLayerBackpackSystem_Statics
{
	static constexpr FClassRegisterCompiledInInfo ClassInfo[] = {
		{ Z_Construct_UClass_UBackpackInventoryComponent, UBackpackInventoryComponent::StaticClass, TEXT("UBackpackInventoryComponent"), &Z_Registration_Info_UClass_UBackpackInventoryComponent, CONSTRUCT_RELOAD_VERSION_INFO(FClassReloadVersionInfo, sizeof(UBackpackInventoryComponent), 747932601U) },
	};
}; // Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_TwoLayerBackpackSystem_Source_TwoLayerBackpackSystem_Public_BackpackInventoryComponent_h__Script_TwoLayerBackpackSystem_Statics 
static FRegisterCompiledInInfo Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_TwoLayerBackpackSystem_Source_TwoLayerBackpackSystem_Public_BackpackInventoryComponent_h__Script_TwoLayerBackpackSystem_342311246{
	TEXT("/Script/TwoLayerBackpackSystem"),
	Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_TwoLayerBackpackSystem_Source_TwoLayerBackpackSystem_Public_BackpackInventoryComponent_h__Script_TwoLayerBackpackSystem_Statics::ClassInfo, UE_ARRAY_COUNT(Z_CompiledInDeferFile_FID_UEprojects_JeffGame001_Plugins_TwoLayerBackpackSystem_Source_TwoLayerBackpackSystem_Public_BackpackInventoryComponent_h__Script_TwoLayerBackpackSystem_Statics::ClassInfo),
	nullptr, 0,
	nullptr, 0,
};
// ********** End Registration *********************************************************************

PRAGMA_ENABLE_DEPRECATION_WARNINGS
