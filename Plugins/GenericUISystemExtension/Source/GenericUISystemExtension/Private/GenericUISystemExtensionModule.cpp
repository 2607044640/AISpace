// GenericUISystemExtensionModule.cpp

#include "GenericUISystemExtensionModule.h"

#define LOCTEXT_NAMESPACE "FGenericUISystemExtensionModule"

void FGenericUISystemExtensionModule::StartupModule()
{
	UE_LOG(LogTemp, Log, TEXT("GenericUISystemExtension: Module started"));
}

void FGenericUISystemExtensionModule::ShutdownModule()
{
	UE_LOG(LogTemp, Log, TEXT("GenericUISystemExtension: Module shutdown"));
}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_MODULE(FGenericUISystemExtensionModule, GenericUISystemExtension)
