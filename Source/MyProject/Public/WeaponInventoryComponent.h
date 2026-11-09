#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "GameplayTagContainer.h"
#include "WeaponTypes.h"
#include "WeaponInventoryComponent.generated.h"

class APawn;
class USkeletalMeshComponent;
class UAnimInstance;
class UWeaponWheelConfig;
class UUserWidget;

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnWeaponEquipped, const FWeaponClassData*, WeaponData);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnWeaponUnequipped, const FWeaponClassData*, WeaponData);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnWeaponSlotChanged, EWeaponCategory, NewCategory);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnAmmoChanged, const FGameplayTag&, AmmoTag, int32, NewAmount);

/**
 * Component that manages the player's weapon inventory and weapon wheel
 */
UCLASS(ClassGroup = (Custom), meta = (BlueprintSpawnableComponent))
class MY_PROJECT_API UWeaponInventoryComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UWeaponInventoryComponent();

	virtual void BeginPlay() override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;

	/** Initialize the weapon inventory with a configuration */
	UFUNCTION(BlueprintCallable, Category = "Weapon Inventory")
	void InitializeInventory(UWeaponWheelConfig* InConfig);

	/** Toggle the weapon wheel visibility */
	UFUNCTION(BlueprintCallable, Category = "Weapon Wheel")
	void ToggleWeaponWheel();

	/** Show the weapon wheel */
	UFUNCTION(BlueprintCallable, Category = "Weapon Wheel")
	void ShowWeaponWheel();

	/** Hide the weapon wheel */
	UFUNCTION(BlueprintCallable, Category = "Weapon Wheel")
	void HideWeaponWheel();

	/** Check if weapon wheel is currently visible */
	UFUNCTION(BlueprintPure, Category = "Weapon Wheel")
	bool IsWeaponWheelVisible() const { return bWeaponWheelVisible; }

	/** Select a weapon slot by category */
	UFUNCTION(BlueprintCallable, Category = "Weapon Inventory")
	bool SelectWeaponSlot(EWeaponCategory Category);

	/** Select a weapon slot by index */
	UFUNCTION(BlueprintCallable, Category = "Weapon Inventory")
	bool SelectWeaponSlotByIndex(int32 SlotIndex);

	/** Cycle weapon in the currently selected slot */
	UFUNCTION(BlueprintCallable, Category = "Weapon Inventory")
	void CycleCurrentSlotWeapon(bool bForward = true);

	/** Cycle weapon in a specific slot */
	UFUNCTION(BlueprintCallable, Category = "Weapon Inventory")
	void CycleSlotWeapon(EWeaponCategory Category, bool bForward = true);

	/** Get the currently equipped weapon data */
	UFUNCTION(BlueprintPure, Category = "Weapon Inventory")
	const FWeaponClassData* GetCurrentWeapon() const;

	/** Get weapon data for a specific slot */
	UFUNCTION(BlueprintPure, Category = "Weapon Inventory")
	const FWeaponSlotData* GetWeaponSlot(EWeaponCategory Category) const;

	/** Get weapon data for a specific slot by index */
	UFUNCTION(BlueprintPure, Category = "Weapon Inventory")
	const FWeaponSlotData* GetWeaponSlotByIndex(int32 SlotIndex) const;

	/** Get all weapon slots */
	UFUNCTION(BlueprintPure, Category = "Weapon Inventory")
	const TArray<FWeaponSlotData>& GetAllWeaponSlots() const { return WeaponSlots; }

	/** Get the currently selected slot index */
	UFUNCTION(BlueprintPure, Category = "Weapon Inventory")
	int32 GetCurrentSlotIndex() const { return CurrentSlotIndex; }

	/** Get the currently selected slot category */
	UFUNCTION(BlueprintPure, Category = "Weapon Inventory")
	EWeaponCategory GetCurrentSlotCategory() const;

	/** Add ammo to a weapon */
	UFUNCTION(BlueprintCallable, Category = "Ammo")
	void AddAmmo(const FGameplayTag& AmmoTag, int32 Amount);

	/** Get current ammo for a weapon */
	UFUNCTION(BlueprintPure, Category = "Ammo")
	int32 GetCurrentAmmo(const FGameplayTag& AmmoTag) const;

	/** Get reserve ammo for a weapon */
	UFUNCTION(BlueprintPure, Category = "Ammo")
	int32 GetReserveAmmo(const FGameplayTag& AmmoTag) const;

	/** Consume ammo from current weapon */
	UFUNCTION(BlueprintCallable, Category = "Ammo")
	bool ConsumeAmmo(int32 Amount = 1);

	/** Reload current weapon */
	UFUNCTION(BlueprintCallable, Category = "Ammo")
	bool ReloadCurrentWeapon();

	/** Check if current weapon can reload */
	UFUNCTION(BlueprintPure, Category = "Ammo")
	bool CanReloadCurrentWeapon() const;

	/** Unlock a weapon slot */
	UFUNCTION(BlueprintCallable, Category = "Weapon Inventory")
	void UnlockWeaponSlot(EWeaponCategory Category);

	/** Lock a weapon slot */
	UFUNCTION(BlueprintCallable, Category = "Weapon Inventory")
	void LockWeaponSlot(EWeaponCategory Category);

	/** Add a weapon class to a slot */
	UFUNCTION(BlueprintCallable, Category = "Weapon Inventory")
	bool AddWeaponToSlot(EWeaponCategory Category, const FWeaponClassData& WeaponData);

	/** Remove a weapon class from a slot */
	UFUNCTION(BlueprintCallable, Category = "Weapon Inventory")
	bool RemoveWeaponFromSlot(EWeaponCategory Category, const FGameplayTag& WeaponTag);

	/** Get the weapon wheel widget instance */
	UFUNCTION(BlueprintPure, Category = "Weapon Wheel")
	UUserWidget* GetWeaponWheelWidget() const { return WeaponWheelWidget; }

	/** Called when the weapon wheel selection changes (from UI) */
	UFUNCTION(BlueprintCallable, Category = "Weapon Wheel")
	void OnWeaponWheelSelectionChanged(int32 SlotIndex);

	/** Called when the weapon wheel confirms selection */
	UFUNCTION(BlueprintCallable, Category = "Weapon Wheel")
	void OnWeaponWheelConfirmSelection();

	/** Called when cycling weapons via input */
	UFUNCTION(BlueprintCallable, Category = "Weapon Wheel")
	void OnCycleWeaponInput(float Value);

	/** Events */
	UPROPERTY(BlueprintAssignable, Category = "Weapon Inventory")
	FOnWeaponEquipped OnWeaponEquipped;

	UPROPERTY(BlueprintAssignable, Category = "Weapon Inventory")
	FOnWeaponUnequipped OnWeaponUnequipped;

	UPROPERTY(BlueprintAssignable, Category = "Weapon Inventory")
	FOnWeaponSlotChanged OnWeaponSlotChanged;

	UPROPERTY(BlueprintAssignable, Category = "Ammo")
	FOnAmmoChanged OnAmmoChanged;

protected:
	/** Weapon wheel configuration */
	UPROPERTY()
	UWeaponWheelConfig* WeaponWheelConfig;

	/** Weapon slots data */
	UPROPERTY()
	TArray<FWeaponSlotData> WeaponSlots;

	/** Currently selected slot index */
	UPROPERTY()
	int32 CurrentSlotIndex = 0;

	/** Currently equipped weapon actor */
	UPROPERTY()
	TObjectPtr<AActor> CurrentWeaponActor;

	/** Weapon wheel widget instance */
	UPROPERTY()
	TObjectPtr<UUserWidget> WeaponWheelWidget;

	/** Whether weapon wheel is currently visible */
	UPROPERTY()
	bool bWeaponWheelVisible = false;

	/** Owning pawn */
	UPROPERTY()
	TObjectPtr<APawn> OwningPawn;

	/** Owning character's mesh */
	UPROPERTY()
	TObjectPtr<USkeletalMeshComponent> CharacterMesh;

	/** Equip a weapon from slot data */
	void EquipWeapon(const FWeaponClassData* WeaponData, EWeaponCategory Category);

	/** Unequip current weapon */
	void UnequipCurrentWeapon();

	/** Create the weapon wheel widget */
	void CreateWeaponWheelWidget();

	/** Update the weapon wheel widget with current data */
	void UpdateWeaponWheelWidget();

	/** Get the category for a slot index */
	EWeaponCategory GetCategoryForSlotIndex(int32 SlotIndex) const;

	/** Find slot index by category */
	int32 FindSlotIndexByCategory(EWeaponCategory Category) const;
};