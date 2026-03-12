#pragma once

#include "Modules/ModuleManager.h"

class FTwoLayerBackpackSystemModule : public IModuleInterface
{
public:
	virtual void StartupModule() override;
	virtual void ShutdownModule() override;
};
