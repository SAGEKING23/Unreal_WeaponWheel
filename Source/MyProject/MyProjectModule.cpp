#include "MyProjectModule.h"

#define LOCTEXT_NAMESPACE "FMyProjectModule"

void FMyProjectModule::StartupModule()
{
}

void FMyProjectModule::ShutdownModule()
{
}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_MODULE(FMyProjectModule, MyProject)