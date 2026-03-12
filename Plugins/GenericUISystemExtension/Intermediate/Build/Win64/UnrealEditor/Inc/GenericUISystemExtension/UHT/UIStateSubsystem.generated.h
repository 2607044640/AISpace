// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

// IWYU pragma: private, include "Subsystems/UIStateSubsystem.h"

#ifdef GENERICUISYSTEMEXTENSION_UIStateSubsystem_generated_h
#error "UIStateSubsystem.generated.h already included, missing '#pragma once' in UIStateSubsystem.h"
#endif
#define GENERICUISYSTEMEXTENSION_UIStateSubsystem_generated_h

#include "UObject/ObjectMacros.h"
#include "UObject/ScriptMacros.h"

PRAGMA_DISABLE_DEPRECATION_WARNINGS

// ********** Begin Class UUIStateSubsystem ********************************************************
#define FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Subsystems_UIStateSubsystem_h_22_RPC_WRAPPERS_NO_PURE_DECLS \
	DECLARE_FUNCTION(execGetPauseRequestCount); \
	DECLARE_FUNCTION(execIsPaused); \
	DECLARE_FUNCTION(execReleasePause); \
	DECLARE_FUNCTION(execRequestPause);


struct Z_Construct_UClass_UUIStateSubsystem_Statics;
GENERICUISYSTEMEXTENSION_API UClass* Z_Construct_UClass_UUIStateSubsystem_NoRegister();

#define FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Subsystems_UIStateSubsystem_h_22_INCLASS_NO_PURE_DECLS \
private: \
	static void StaticRegisterNativesUUIStateSubsystem(); \
	friend struct ::Z_Construct_UClass_UUIStateSubsystem_Statics; \
	static UClass* GetPrivateStaticClass(); \
	friend GENERICUISYSTEMEXTENSION_API UClass* ::Z_Construct_UClass_UUIStateSubsystem_NoRegister(); \
public: \
	DECLARE_CLASS2(UUIStateSubsystem, UGameInstanceSubsystem, COMPILED_IN_FLAGS(0), CASTCLASS_None, TEXT("/Script/GenericUISystemExtension"), Z_Construct_UClass_UUIStateSubsystem_NoRegister) \
	DECLARE_SERIALIZER(UUIStateSubsystem)


#define FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Subsystems_UIStateSubsystem_h_22_ENHANCED_CONSTRUCTORS \
	/** Standard constructor, called after all reflected properties have been initialized */ \
	NO_API UUIStateSubsystem(); \
	/** Deleted move- and copy-constructors, should never be used */ \
	UUIStateSubsystem(UUIStateSubsystem&&) = delete; \
	UUIStateSubsystem(const UUIStateSubsystem&) = delete; \
	DECLARE_VTABLE_PTR_HELPER_CTOR(NO_API, UUIStateSubsystem); \
	DEFINE_VTABLE_PTR_HELPER_CTOR_CALLER(UUIStateSubsystem); \
	DEFINE_DEFAULT_CONSTRUCTOR_CALL(UUIStateSubsystem) \
	NO_API virtual ~UUIStateSubsystem();


#define FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Subsystems_UIStateSubsystem_h_19_PROLOG
#define FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Subsystems_UIStateSubsystem_h_22_GENERATED_BODY \
PRAGMA_DISABLE_DEPRECATION_WARNINGS \
public: \
	FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Subsystems_UIStateSubsystem_h_22_RPC_WRAPPERS_NO_PURE_DECLS \
	FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Subsystems_UIStateSubsystem_h_22_INCLASS_NO_PURE_DECLS \
	FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Subsystems_UIStateSubsystem_h_22_ENHANCED_CONSTRUCTORS \
private: \
PRAGMA_ENABLE_DEPRECATION_WARNINGS


class UUIStateSubsystem;

// ********** End Class UUIStateSubsystem **********************************************************

#undef CURRENT_FILE_ID
#define CURRENT_FILE_ID FID_UEprojects_JeffGame001_Plugins_GenericUISystemExtension_Source_GenericUISystemExtension_Public_Subsystems_UIStateSubsystem_h

PRAGMA_ENABLE_DEPRECATION_WARNINGS
