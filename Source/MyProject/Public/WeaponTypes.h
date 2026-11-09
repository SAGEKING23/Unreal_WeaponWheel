#pragma once

#include "CoreMinimal.h"
#include "GameplayTagContainer.h"
#include "Engine/DataAsset.h"
#include "WeaponTypes.generated.h"

class UAnimMontage;
class USkeletalMesh;
class UClass;

/**
 * Weapon category enumeration for the weapon wheel slots
 */
UENUM(BlueprintType)
enum class EWeaponCategory : uint8
{
	Primary UMETA(DisplayName = "Primary"),       // Assault Rifle, Sniper Rifle
	Secondary UMETA(DisplayName = "Secondary"),   // Pistol
	Heavy UMETA(DisplayName = "Heavy"),           // Rocket Launcher, Grenade Launcher
	Special UMETA(DisplayName = "Special"),       // Shotgun
	Melee UMETA(DisplayName = "Melee"),           // Knife
	Utility UMETA(DisplayName = "Utility"),       // Gadgets, etc.
	MAX UMETA(Hidden)
};

/**
 * Data for a single weapon class that can be equipped in a slot
 */
USTRUCT(BlueprintType)
struct FWeaponClassData
{
	GENERATED_BODY()

	/** Display name for this weapon variant */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Weapon")
	FText DisplayName;

	/** Gameplay tag identifying this weapon class */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Weapon")
	FGameplayTag WeaponTag;

	/** Skeletal mesh for the weapon */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Weapon")
	TSoftObjectPtr<USkeletalMesh> WeaponMesh;

	/** Weapon blueprint class to spawn */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Weapon")
	TSubclassOf<class AActor> WeaponClass;

	/** Animation montage for equipping this weapon */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Animation")
	TSoftObjectPtr<UAnimMontage> EquipMontage;

	/** Animation montage for firing this weapon */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Animation")
	TSoftObjectPtr<UAnimMontage> FireMontage;

	/** Animation montage for reloading this weapon */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Animation")
	TSoftObjectPtr<UAnimMontage> ReloadMontage;

	/** Icon texture for the weapon wheel */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UI")
	TSoftObjectPtr<class UTexture2D> IconTexture;

	/** Ammo type tag */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Ammo")
	FGameplayTag AmmoTag;

	/** Maximum ammo capacity */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Ammo")
	int32 MaxAmmo = 30;

	/** Current ammo in reserve */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Ammo")
	int32 ReserveAmmo = 90;

	/** Current ammo in magazine */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Ammo", Transient)
	int32 CurrentAmmo = 30;

	FWeaponClassData()
	{
		WeaponTag = FGameplayTag();
		MaxAmmo = 30;
		ReserveAmmo = 90;
		CurrentAmmo = 30;
	}
};

/**
 * Data for a weapon slot in the wheel (can hold multiple weapon classes)
 */
USTRUCT(BlueprintType)
struct FWeaponSlotData
{
	GENERATED_BODY()

	/** Category this slot represents */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Weapon Slot")
	EWeaponCategory Category;

	/** Display name for the slot */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Weapon Slot")
	FText SlotName;

	/** Angle offset for this slot on the wheel (degrees) */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Weapon Slot")
	float WheelAngle = 0.0f;

	/** Available weapon classes for this slot */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Weapon Slot")
	TArray<FWeaponClassData> AvailableWeapons;

	/** Index of currently selected weapon in AvailableWeapons */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Weapon Slot", Transient)
	int32 CurrentWeaponIndex = 0;

	/** Whether this slot is unlocked/available */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Weapon Slot")
	bool bIsUnlocked = true;

	FWeaponSlotData()
	{
		Category = EWeaponCategory::Primary;
		WheelAngle = 0.0f;
		CurrentWeaponIndex = 0;
		bIsUnlocked = true;
	}

	/** Get the currently selected weapon class data */
	UFUNCTION(BlueprintPure, Category = "Weapon Slot")
	const FWeaponClassData* GetCurrentWeapon() const
	{
		if (AvailableWeapons.IsValidIndex(CurrentWeaponIndex))
		{
			return &AvailableWeapons[CurrentWeaponIndex];
		}
		return nullptr;
	}

	/** Cycle to the next weapon in this slot */
	UFUNCTION(BlueprintCallable, Category = "Weapon Slot")
	void CycleWeapon(bool bForward = true)
	{
		if (AvailableWeapons.Num() <= 1) return;

		if (bForward)
		{
			CurrentWeaponIndex = (CurrentWeaponIndex + 1) % AvailableWeapons.Num();
		}
		else
		{
			CurrentWeaponIndex = (CurrentWeaponIndex - 1 + AvailableWeapons.Num()) % AvailableWeapons.Num();
		}
	}
};

/**
 * Data asset defining the weapon wheel configuration
 */
UCLASS(BlueprintType, Category = "Weapon System")
class MY_PROJECT_API UWeaponWheelConfig : public UDataAsset
{
	GENERATED_BODY()

public:
	/** Weapon slots arranged around the wheel */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Weapon Wheel")
	TArray<FWeaponSlotData> WeaponSlots;

	/** Number of slots to display on the wheel (max 8) */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Weapon Wheel", meta = (ClampMin = "2", ClampMax = "8"))
	int32 MaxVisibleSlots = 6;

	/** Radius of the weapon wheel */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Weapon Wheel", meta = (ClampMin = "100", ClampMax = "500"))
	float WheelRadius = 200.0f;

	/** Animation duration for wheel open/close */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Weapon Wheel", meta = (ClampMin = "0.1", ClampMax = "1.0"))
	float AnimationDuration = 0.25f;

	/** Input action to toggle the weapon wheel */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Input")
	TObjectPtr<class UInputAction> ToggleWeaponWheelAction;

	/** Input action for cycling weapons in current slot (mouse wheel) */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Input")
	TObjectPtr<class UInputAction> CycleWeaponAction;

	/** Input action for selecting weapon (mouse click) */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Input")
	TObjectPtr<class UInputAction> SelectWeaponAction;

	/** Widget class for the weapon wheel */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UI")
	TSubclassOf<class UUserWidget> WeaponWheelWidgetClass;

	/** Default weapon wheel configuration */
	UFUNCTION(BlueprintCallable, Category = "Weapon Wheel")
	static UWeaponWheelConfig* CreateDefaultConfig();
};