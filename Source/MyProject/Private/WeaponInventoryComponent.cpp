#include "WeaponInventoryComponent.h"
#include "GameFramework/Pawn.h"
#include "GameFramework/Character.h"
#include "Components/SkeletalMeshComponent.h"
#include "Engine/World.h"
#include "Engine/AssetManager.h"
#include "TimerManager.h"
#include "Blueprint/UserWidget.h"
#include "Kismet/GameplayStatics.h"

UWeaponInventoryComponent::UWeaponInventoryComponent()
{
	PrimaryComponentTick.bCanEverTick = false;
}

void UWeaponInventoryComponent::BeginPlay()
{
	Super::BeginPlay();

	OwningPawn = GetOwner<APawn>();
	if (ACharacter* Character = Cast<ACharacter>(OwningPawn))
	{
		CharacterMesh = Character->GetMesh();
	}
}

void UWeaponInventoryComponent::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	HideWeaponWheel();
	Super::EndPlay(EndPlayReason);
}

void UWeaponInventoryComponent::InitializeInventory(UWeaponWheelConfig* InConfig)
{
	WeaponWheelConfig = InConfig;

	if (WeaponWheelConfig)
	{
		WeaponSlots = WeaponWheelConfig->WeaponSlots;

		// Sort slots by wheel angle for consistent ordering
		WeaponSlots.Sort([](const FWeaponSlotData& A, const FWeaponSlotData& B)
		{
			return A.WheelAngle < B.WheelAngle;
		});

		// Auto-equip first unlocked weapon
		for (int32 i = 0; i < WeaponSlots.Num(); ++i)
		{
			if (WeaponSlots[i].bIsUnlocked && WeaponSlots[i].AvailableWeapons.Num() > 0)
			{
				CurrentSlotIndex = i;
				EquipWeapon(WeaponSlots[i].GetCurrentWeapon(), WeaponSlots[i].Category);
				break;
			}
		}
	}
}

void UWeaponInventoryComponent::ToggleWeaponWheel()
{
	if (bWeaponWheelVisible)
	{
		HideWeaponWheel();
	}
	else
	{
		ShowWeaponWheel();
	}
}

void UWeaponInventoryComponent::ShowWeaponWheel()
{
	if (bWeaponWheelVisible || !WeaponWheelConfig) return;

	bWeaponWheelVisible = true;
	CreateWeaponWheelWidget();
	UpdateWeaponWheelWidget();

	// Pause game input for wheel interaction
	if (APlayerController* PC = Cast<APlayerController>(OwningPawn->GetController()))
	{
		PC->SetInputMode(FInputModeGameAndUI());
		PC->SetShowMouseCursor(true);
	}
}

void UWeaponInventoryComponent::HideWeaponWheel()
{
	if (!bWeaponWheelVisible) return;

	bWeaponWheelVisible = false;

	if (WeaponWheelWidget)
	{
		WeaponWheelWidget->RemoveFromParent();
		WeaponWheelWidget = nullptr;
	}

	// Restore game input
	if (APlayerController* PC = Cast<APlayerController>(OwningPawn->GetController()))
	{
		PC->SetInputMode(FInputModeGameOnly());
		PC->SetShowMouseCursor(false);
	}
}

bool UWeaponInventoryComponent::SelectWeaponSlot(EWeaponCategory Category)
{
	int32 SlotIndex = FindSlotIndexByCategory(Category);
	return SelectWeaponSlotByIndex(SlotIndex);
}

bool UWeaponInventoryComponent::SelectWeaponSlotByIndex(int32 SlotIndex)
{
	if (!WeaponSlots.IsValidIndex(SlotIndex)) return false;
	if (!WeaponSlots[SlotIndex].bIsUnlocked) return false;
	if (WeaponSlots[SlotIndex].AvailableWeapons.Num() == 0) return false;

	CurrentSlotIndex = SlotIndex;

	const FWeaponSlotData& Slot = WeaponSlots[SlotIndex];
	EquipWeapon(Slot.GetCurrentWeapon(), Slot.Category);

	OnWeaponSlotChanged.Broadcast(Slot.Category);
	UpdateWeaponWheelWidget();

	return true;
}

void UWeaponInventoryComponent::CycleCurrentSlotWeapon(bool bForward)
{
	if (!WeaponSlots.IsValidIndex(CurrentSlotIndex)) return;

	FWeaponSlotData& Slot = WeaponSlots[CurrentSlotIndex];
	if (Slot.AvailableWeapons.Num() <= 1) return;

	Slot.CycleWeapon(bForward);
	EquipWeapon(Slot.GetCurrentWeapon(), Slot.Category);
	UpdateWeaponWheelWidget();
}

void UWeaponInventoryComponent::CycleSlotWeapon(EWeaponCategory Category, bool bForward)
{
	int32 SlotIndex = FindSlotIndexByCategory(Category);
	if (!WeaponSlots.IsValidIndex(SlotIndex)) return;

	FWeaponSlotData& Slot = WeaponSlots[SlotIndex];
	if (Slot.AvailableWeapons.Num() <= 1) return;

	Slot.CycleWeapon(bForward);

	// If this is the currently equipped slot, re-equip
	if (SlotIndex == CurrentSlotIndex)
	{
		EquipWeapon(Slot.GetCurrentWeapon(), Slot.Category);
	}

	UpdateWeaponWheelWidget();
}

const FWeaponClassData* UWeaponInventoryComponent::GetCurrentWeapon() const
{
	if (!WeaponSlots.IsValidIndex(CurrentSlotIndex)) return nullptr;
	return WeaponSlots[CurrentSlotIndex].GetCurrentWeapon();
}

const FWeaponSlotData* UWeaponInventoryComponent::GetWeaponSlot(EWeaponCategory Category) const
{
	int32 Index = FindSlotIndexByCategory(Category);
	if (WeaponSlots.IsValidIndex(Index))
	{
		return &WeaponSlots[Index];
	}
	return nullptr;
}

const FWeaponSlotData* UWeaponInventoryComponent::GetWeaponSlotByIndex(int32 SlotIndex) const
{
	if (WeaponSlots.IsValidIndex(SlotIndex))
	{
		return &WeaponSlots[SlotIndex];
	}
	return nullptr;
}

EWeaponCategory UWeaponInventoryComponent::GetCurrentSlotCategory() const
{
	if (WeaponSlots.IsValidIndex(CurrentSlotIndex))
	{
		return WeaponSlots[CurrentSlotIndex].Category;
	}
	return EWeaponCategory::Primary;
}

void UWeaponInventoryComponent::AddAmmo(const FGameplayTag& AmmoTag, int32 Amount)
{
	for (FWeaponSlotData& Slot : WeaponSlots)
	{
		for (FWeaponClassData& Weapon : Slot.AvailableWeapons)
		{
			if (Weapon.AmmoTag == AmmoTag)
			{
				Weapon.ReserveAmmo = FMath::Min(Weapon.ReserveAmmo + Amount, Weapon.MaxAmmo * 4);
				OnAmmoChanged.Broadcast(AmmoTag, Weapon.ReserveAmmo);
			}
		}
	}
}

int32 UWeaponInventoryComponent::GetCurrentAmmo(const FGameplayTag& AmmoTag) const
{
	for (const FWeaponSlotData& Slot : WeaponSlots)
	{
		for (const FWeaponClassData& Weapon : Slot.AvailableWeapons)
		{
			if (Weapon.AmmoTag == AmmoTag)
			{
				return Weapon.CurrentAmmo;
			}
		}
	}
	return 0;
}

int32 UWeaponInventoryComponent::GetReserveAmmo(const FGameplayTag& AmmoTag) const
{
	for (const FWeaponSlotData& Slot : WeaponSlots)
	{
		for (const FWeaponClassData& Weapon : Slot.AvailableWeapons)
		{
			if (Weapon.AmmoTag == AmmoTag)
			{
				return Weapon.ReserveAmmo;
			}
		}
	}
	return 0;
}

bool UWeaponInventoryComponent::ConsumeAmmo(int32 Amount)
{
	const FWeaponClassData* CurrentWeapon = GetCurrentWeapon();
	if (!CurrentWeapon) return false;

	// Find the mutable weapon data
	for (FWeaponSlotData& Slot : WeaponSlots)
	{
		for (FWeaponClassData& Weapon : Slot.AvailableWeapons)
		{
			if (Weapon.WeaponTag == CurrentWeapon->WeaponTag)
			{
				if (Weapon.CurrentAmmo >= Amount)
				{
					Weapon.CurrentAmmo -= Amount;
					OnAmmoChanged.Broadcast(Weapon.AmmoTag, Weapon.CurrentAmmo);
					return true;
				}
				return false;
			}
		}
	}
	return false;
}

bool UWeaponInventoryComponent::ReloadCurrentWeapon()
{
	const FWeaponClassData* CurrentWeapon = GetCurrentWeapon();
	if (!CurrentWeapon) return false;

	for (FWeaponSlotData& Slot : WeaponSlots)
	{
		for (FWeaponClassData& Weapon : Slot.AvailableWeapons)
		{
			if (Weapon.WeaponTag == CurrentWeapon->WeaponTag)
			{
				int32 AmmoNeeded = Weapon.MaxAmmo - Weapon.CurrentAmmo;
				int32 AmmoToUse = FMath::Min(AmmoNeeded, Weapon.ReserveAmmo);

				if (AmmoToUse > 0)
				{
					Weapon.CurrentAmmo += AmmoToUse;
					Weapon.ReserveAmmo -= AmmoToUse;
					OnAmmoChanged.Broadcast(Weapon.AmmoTag, Weapon.CurrentAmmo);
					return true;
				}
				return false;
			}
		}
	}
	return false;
}

bool UWeaponInventoryComponent::CanReloadCurrentWeapon() const
{
	const FWeaponClassData* CurrentWeapon = GetCurrentWeapon();
	if (!CurrentWeapon) return false;

	for (const FWeaponSlotData& Slot : WeaponSlots)
	{
		for (const FWeaponClassData& Weapon : Slot.AvailableWeapons)
		{
			if (Weapon.WeaponTag == CurrentWeapon->WeaponTag)
			{
				return Weapon.CurrentAmmo < Weapon.MaxAmmo && Weapon.ReserveAmmo > 0;
			}
		}
	}
	return false;
}

void UWeaponInventoryComponent::UnlockWeaponSlot(EWeaponCategory Category)
{
	int32 Index = FindSlotIndexByCategory(Category);
	if (WeaponSlots.IsValidIndex(Index))
	{
		WeaponSlots[Index].bIsUnlocked = true;
		UpdateWeaponWheelWidget();
	}
}

void UWeaponInventoryComponent::LockWeaponSlot(EWeaponCategory Category)
{
	int32 Index = FindSlotIndexByCategory(Category);
	if (WeaponSlots.IsValidIndex(Index))
	{
		WeaponSlots[Index].bIsUnlocked = false;
		UpdateWeaponWheelWidget();
	}
}

bool UWeaponInventoryComponent::AddWeaponToSlot(EWeaponCategory Category, const FWeaponClassData& WeaponData)
{
	int32 Index = FindSlotIndexByCategory(Category);
	if (!WeaponSlots.IsValidIndex(Index)) return false;

	WeaponSlots[Index].AvailableWeapons.Add(WeaponData);
	UpdateWeaponWheelWidget();
	return true;
}

bool UWeaponInventoryComponent::RemoveWeaponFromSlot(EWeaponCategory Category, const FGameplayTag& WeaponTag)
{
	int32 Index = FindSlotIndexByCategory(Category);
	if (!WeaponSlots.IsValidIndex(Index)) return false;

	FWeaponSlotData& Slot = WeaponSlots[Index];
	int32 RemoveIndex = INDEX_NONE;

	for (int32 i = 0; i < Slot.AvailableWeapons.Num(); ++i)
	{
		if (Slot.AvailableWeapons[i].WeaponTag == WeaponTag)
		{
			RemoveIndex = i;
			break;
		}
	}

	if (RemoveIndex != INDEX_NONE)
	{
		Slot.AvailableWeapons.RemoveAt(RemoveIndex);
		Slot.CurrentWeaponIndex = FMath::Clamp(Slot.CurrentWeaponIndex, 0, Slot.AvailableWeapons.Num() - 1);
		UpdateWeaponWheelWidget();
		return true;
	}
	return false;
}

void UWeaponInventoryComponent::OnWeaponWheelSelectionChanged(int32 SlotIndex)
{
	if (WeaponSlots.IsValidIndex(SlotIndex))
	{
		CurrentSlotIndex = SlotIndex;
		UpdateWeaponWheelWidget();
	}
}

void UWeaponInventoryComponent::OnWeaponWheelConfirmSelection()
{
	if (WeaponSlots.IsValidIndex(CurrentSlotIndex))
	{
		const FWeaponSlotData& Slot = WeaponSlots[CurrentSlotIndex];
		EquipWeapon(Slot.GetCurrentWeapon(), Slot.Category);
		OnWeaponSlotChanged.Broadcast(Slot.Category);
	}

	HideWeaponWheel();
}

void UWeaponInventoryComponent::OnCycleWeaponInput(float Value)
{
	if (!bWeaponWheelVisible) return;

	if (Value > 0.0f)
	{
		CycleCurrentSlotWeapon(true);
	}
	else if (Value < 0.0f)
	{
		CycleCurrentSlotWeapon(false);
	}
}

void UWeaponInventoryComponent::EquipWeapon(const FWeaponClassData* WeaponData, EWeaponCategory Category)
{
	if (!WeaponData || !WeaponData->WeaponClass) return;

	UnequipCurrentWeapon();

	FActorSpawnParameters SpawnParams;
	SpawnParams.Owner = OwningPawn;
	SpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

	FTransform SpawnTransform = FTransform::Identity;
	if (CharacterMesh)
	{
		// Try to attach to weapon socket
		FName SocketName = FName(*FString::Printf(TEXT("Weapon_%s"), *UEnum::GetValueAsString(Category)));
		if (!CharacterMesh->DoesSocketExist(SocketName))
		{
			SocketName = FName("Weapon_R");
		}
		SpawnTransform = CharacterMesh->GetSocketTransform(SocketName);
	}

	CurrentWeaponActor = GetWorld()->SpawnActor<AActor>(WeaponData->WeaponClass, SpawnTransform, SpawnParams);

	if (CurrentWeaponActor && CharacterMesh)
	{
		FName SocketName = FName(*FString::Printf(TEXT("Weapon_%s"), *UEnum::GetValueAsString(Category)));
		if (!CharacterMesh->DoesSocketExist(SocketName))
		{
			SocketName = FName("Weapon_R");
		}
		CurrentWeaponActor->AttachToComponent(CharacterMesh, FAttachmentTransformRules::SnapToTargetNotIncludingScale, SocketName);
	}

	OnWeaponEquipped.Broadcast(WeaponData);
}

void UWeaponInventoryComponent::UnequipCurrentWeapon()
{
	if (CurrentWeaponActor)
	{
		const FWeaponClassData* OldWeapon = GetCurrentWeapon();
		CurrentWeaponActor->Destroy();
		CurrentWeaponActor = nullptr;

		if (OldWeapon)
		{
			OnWeaponUnequipped.Broadcast(OldWeapon);
		}
	}
}

void UWeaponInventoryComponent::CreateWeaponWheelWidget()
{
	if (!WeaponWheelConfig || !WeaponWheelConfig->WeaponWheelWidgetClass) return;
	if (WeaponWheelWidget) return;

	WeaponWheelWidget = CreateWidget<UUserWidget>(GetWorld(), WeaponWheelConfig->WeaponWheelWidgetClass);
	if (WeaponWheelWidget)
	{
		WeaponWheelWidget->AddToViewport(100);
	}
}

void UWeaponInventoryComponent::UpdateWeaponWheelWidget()
{
	if (!WeaponWheelWidget) return;

	// The widget will bind to this component and read data via GetAllWeaponSlots, GetCurrentSlotIndex, etc.
	// We can also call a custom event on the widget if needed
}

EWeaponCategory UWeaponInventoryComponent::GetCategoryForSlotIndex(int32 SlotIndex) const
{
	if (WeaponSlots.IsValidIndex(SlotIndex))
	{
		return WeaponSlots[SlotIndex].Category;
	}
	return EWeaponCategory::Primary;
}

int32 UWeaponInventoryComponent::FindSlotIndexByCategory(EWeaponCategory Category) const
{
	for (int32 i = 0; i < WeaponSlots.Num(); ++i)
	{
		if (WeaponSlots[i].Category == Category)
		{
			return i;
		}
	}
	return INDEX_NONE;
}