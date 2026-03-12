// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

// IWYU pragma: private, include "BackpackInventoryComponent.h"

#ifdef TWOLAYERBACKPACKSYSTEM_BackpackInventoryComponent_generated_h
#error "BackpackInventoryComponent.generated.h already included, missing '#pragma once' in BackpackInventoryComponent.h"
#endif
#define TWOLAYERBACKPACKSYSTEM_BackpackInventoryComponent_generated_h

#include "UObject/ObjectMacros.h"
#include "UObject/ScriptMacros.h"

PRAGMA_DISABLE_DEPRECATION_WARNINGS

// ********** Begin Class UBackpackInventoryComponent **********************************************
#define FID_UEprojects_JeffGame001_Plugins_TwoLayerBackpackSystem_Source_TwoLayerBackpackSystem_Public_BackpackInventoryComponent_h_28_RPC_WRAPPERS_NO_PURE_DECLS \
	DECLARE_FUNCTION(execIsBackpackOpen); \
	DECLARE_FUNCTION(execOpenBackpackInventory);


struct Z_Construct_UClass_UBackpackInventoryComponent_Statics;
TWOLAYERBACKPACKSYSTEM_API UClass* Z_Construct_UClass_UBackpackInventoryComponent_NoRegister();

#define FID_UEprojects_JeffGame001_Plugins_TwoLayerBackpackSystem_Source_TwoLayerBackpackSystem_Public_BackpackInventoryComponent_h_28_INCLASS_NO_PURE_DECLS \
private: \
	static void StaticRegisterNativesUBackpackInventoryComponent(); \
	friend struct ::Z_Construct_UClass_UBackpackInventoryComponent_Statics; \
	static UClass* GetPrivateStaticClass(); \
	friend TWOLAYERBACKPACKSYSTEM_API UClass* ::Z_Construct_UClass_UBackpackInventoryComponent_NoRegister(); \
public: \
	DECLARE_CLASS2(UBackpackInventoryComponent, UActorComponent, COMPILED_IN_FLAGS(0 | CLASS_Config), CASTCLASS_None, TEXT("/Script/TwoLayerBackpackSystem"), Z_Construct_UClass_UBackpackInventoryComponent_NoRegister) \
	DECLARE_SERIALIZER(UBackpackInventoryComponent)


#define FID_UEprojects_JeffGame001_Plugins_TwoLayerBackpackSystem_Source_TwoLayerBackpackSystem_Public_BackpackInventoryComponent_h_28_ENHANCED_CONSTRUCTORS \
	/** Deleted move- and copy-constructors, should never be used */ \
	UBackpackInventoryComponent(UBackpackInventoryComponent&&) = delete; \
	UBackpackInventoryComponent(const UBackpackInventoryComponent&) = delete; \
	DECLARE_VTABLE_PTR_HELPER_CTOR(NO_API, UBackpackInventoryComponent); \
	DEFINE_VTABLE_PTR_HELPER_CTOR_CALLER(UBackpackInventoryComponent); \
	DEFINE_DEFAULT_CONSTRUCTOR_CALL(UBackpackInventoryComponent) \
	NO_API virtual ~UBackpackInventoryComponent();


#define FID_UEprojects_JeffGame001_Plugins_TwoLayerBackpackSystem_Source_TwoLayerBackpackSystem_Public_BackpackInventoryComponent_h_25_PROLOG
#define FID_UEprojects_JeffGame001_Plugins_TwoLayerBackpackSystem_Source_TwoLayerBackpackSystem_Public_BackpackInventoryComponent_h_28_GENERATED_BODY \
PRAGMA_DISABLE_DEPRECATION_WARNINGS \
public: \
	FID_UEprojects_JeffGame001_Plugins_TwoLayerBackpackSystem_Source_TwoLayerBackpackSystem_Public_BackpackInventoryComponent_h_28_RPC_WRAPPERS_NO_PURE_DECLS \
	FID_UEprojects_JeffGame001_Plugins_TwoLayerBackpackSystem_Source_TwoLayerBackpackSystem_Public_BackpackInventoryComponent_h_28_INCLASS_NO_PURE_DECLS \
	FID_UEprojects_JeffGame001_Plugins_TwoLayerBackpackSystem_Source_TwoLayerBackpackSystem_Public_BackpackInventoryComponent_h_28_ENHANCED_CONSTRUCTORS \
private: \
PRAGMA_ENABLE_DEPRECATION_WARNINGS


class UBackpackInventoryComponent;

// ********** End Class UBackpackInventoryComponent ************************************************

#undef CURRENT_FILE_ID
#define CURRENT_FILE_ID FID_UEprojects_JeffGame001_Plugins_TwoLayerBackpackSystem_Source_TwoLayerBackpackSystem_Public_BackpackInventoryComponent_h

PRAGMA_ENABLE_DEPRECATION_WARNINGS
