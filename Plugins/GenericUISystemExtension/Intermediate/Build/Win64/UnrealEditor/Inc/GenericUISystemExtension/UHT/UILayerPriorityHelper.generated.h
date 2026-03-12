// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

// IWYU pragma: private, include "Utilities/UILayerPriorityHelper.h"

#ifdef GENERICUISYSTEMEXTENSION_UILayerPriorityHelper_generated_h
#error "UILayerPriorityHelper.generated.h already included, missing '#pragma once' in UILayerPriorityHelper.h"
#endif
#define GENERICUISYSTEMEXTENSION_UILayerPriorityHelper_generated_h

#include "UObject/ObjectMacros.h"
#include "UObject/ScriptMacros.h"

PRAGMA_DISABLE_DEPRECATION_WARNINGS
class APlayerController;
struct FGameplayTag;

// ********** Begin Class UUILayerPriorityHelper ***************************************************
#define FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Utilities_UILayerPriorityHelper_h_25_RPC_WRAPPERS_NO_PURE_DECLS \
	DECLARE_FUNCTION(execHasHigherPriorityActiveLayer); \
	DECLARE_FUNCTION(execGetHighestActiveLayerTag); \
	DECLARE_FUNCTION(execCanOpenUILayer); \
	DECLARE_FUNCTION(execGetLayerPriority);


struct Z_Construct_UClass_UUILayerPriorityHelper_Statics;
GENERICUISYSTEMEXTENSION_API UClass* Z_Construct_UClass_UUILayerPriorityHelper_NoRegister();

#define FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Utilities_UILayerPriorityHelper_h_25_INCLASS_NO_PURE_DECLS \
private: \
	static void StaticRegisterNativesUUILayerPriorityHelper(); \
	friend struct ::Z_Construct_UClass_UUILayerPriorityHelper_Statics; \
	static UClass* GetPrivateStaticClass(); \
	friend GENERICUISYSTEMEXTENSION_API UClass* ::Z_Construct_UClass_UUILayerPriorityHelper_NoRegister(); \
public: \
	DECLARE_CLASS2(UUILayerPriorityHelper, UBlueprintFunctionLibrary, COMPILED_IN_FLAGS(0), CASTCLASS_None, TEXT("/Script/GenericUISystemExtension"), Z_Construct_UClass_UUILayerPriorityHelper_NoRegister) \
	DECLARE_SERIALIZER(UUILayerPriorityHelper)


#define FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Utilities_UILayerPriorityHelper_h_25_ENHANCED_CONSTRUCTORS \
	/** Standard constructor, called after all reflected properties have been initialized */ \
	NO_API UUILayerPriorityHelper(const FObjectInitializer& ObjectInitializer = FObjectInitializer::Get()); \
	/** Deleted move- and copy-constructors, should never be used */ \
	UUILayerPriorityHelper(UUILayerPriorityHelper&&) = delete; \
	UUILayerPriorityHelper(const UUILayerPriorityHelper&) = delete; \
	DECLARE_VTABLE_PTR_HELPER_CTOR(NO_API, UUILayerPriorityHelper); \
	DEFINE_VTABLE_PTR_HELPER_CTOR_CALLER(UUILayerPriorityHelper); \
	DEFINE_DEFAULT_OBJECT_INITIALIZER_CONSTRUCTOR_CALL(UUILayerPriorityHelper) \
	NO_API virtual ~UUILayerPriorityHelper();


#define FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Utilities_UILayerPriorityHelper_h_22_PROLOG
#define FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Utilities_UILayerPriorityHelper_h_25_GENERATED_BODY \
PRAGMA_DISABLE_DEPRECATION_WARNINGS \
public: \
	FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Utilities_UILayerPriorityHelper_h_25_RPC_WRAPPERS_NO_PURE_DECLS \
	FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Utilities_UILayerPriorityHelper_h_25_INCLASS_NO_PURE_DECLS \
	FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Utilities_UILayerPriorityHelper_h_25_ENHANCED_CONSTRUCTORS \
private: \
PRAGMA_ENABLE_DEPRECATION_WARNINGS


class UUILayerPriorityHelper;

// ********** End Class UUILayerPriorityHelper *****************************************************

#undef CURRENT_FILE_ID
#define CURRENT_FILE_ID FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Utilities_UILayerPriorityHelper_h

PRAGMA_ENABLE_DEPRECATION_WARNINGS
