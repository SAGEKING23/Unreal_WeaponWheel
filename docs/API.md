# Weapon Wheel System - API Reference

## UWeaponWheelConfig

Data asset defining the weapon wheel configuration.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `WeaponSlots` | `TArray<FWeaponSlotData>` | Weapon slots arranged around the wheel |
| `MaxVisibleSlots` | `int32` | Number of slots to display (2-8) |
| `WheelRadius` | `float` | Radius of the weapon wheel (100-500) |
| `AnimationDuration` | `float` | Open/close animation duration (0.1-1.0) |
| `ToggleWeaponWheelAction` | `UInputAction*` | Input action to toggle wheel |
| `CycleWeaponAction` | `UInputAction*` | Input action for cycling weapons |
| `SelectWeaponAction` | `UInputAction*` | Input action for selecting weapon |
| `WeaponWheelWidgetClass` | `TSubclassOf<UUserWidget>` | Widget class for the weapon wheel |

### Functions

#### CreateDefaultConfig
```cpp
static UWeaponWheelConfig* CreateDefaultConfig();
```
Creates a default weapon wheel configuration.

---

## FWeaponSlotData

Data for a weapon slot in the wheel.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `Category` | `EWeaponCategory` | Category this slot represents |
| `SlotName` | `FText` | Display name for the slot |
| `WheelAngle` | `float` | Angle offset on wheel (degrees) |
| `AvailableWeapons` | `TArray<FWeaponClassData>` | Available weapon classes |
| `CurrentWeaponIndex` | `int32` | Index of selected weapon |
| `bIsUnlocked` | `bool` | Whether slot is available |

### Functions

#### GetCurrentWeapon
```cpp
const FWeaponClassData* GetCurrentWeapon() const;
```
Returns the currently selected weapon data, or nullptr if none.

#### CycleWeapon
```cpp
void CycleWeapon(bool bForward = true);
```
Cycles to next/previous weapon in the slot.

---

## FWeaponClassData

Data for a single weapon class.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `DisplayName` | `FText` | Display name for weapon variant |
| `WeaponTag` | `FGameplayTag` | Gameplay tag identifying weapon |
| `WeaponMesh` | `TSoftObjectPtr<USkeletalMesh>` | Weapon skeletal mesh |
| `WeaponClass` | `TSubclassOf<AActor>` | Weapon blueprint class |
| `EquipMontage` | `TSoftObjectPtr<UAnimMontage>` | Equip animation montage |
| `FireMontage` | `TSoftObjectPtr<UAnimMontage>` | Fire animation montage |
| `ReloadMontage` | `TSoftObjectPtr<UAnimMontage>` | Reload animation montage |
| `IconTexture` | `TSoftObjectPtr<UTexture2D>` | Icon for weapon wheel |
| `AmmoTag` | `FGameplayTag` | Ammo type tag |
| `MaxAmmo` | `int32` | Maximum magazine capacity |
| `ReserveAmmo` | `int32` | Current reserve ammo |
| `CurrentAmmo` | `int32` | Current ammo in magazine |

---

## UWeaponInventoryComponent

Component managing weapon inventory and wheel.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `OnWeaponEquipped` | `FOnWeaponEquipped` | Broadcast when weapon equipped |
| `OnWeaponUnequipped` | `FOnWeaponUnequipped` | Broadcast when weapon unequipped |
| `OnWeaponSlotChanged` | `FOnWeaponSlotChanged` | Broadcast when slot changed |
| `OnAmmoChanged` | `FOnAmmoChanged` | Broadcast when ammo changed |

### Functions

#### InitializeInventory
```cpp
void InitializeInventory(UWeaponWheelConfig* InConfig);
```
Initializes the inventory with a weapon wheel config.

#### ToggleWeaponWheel
```cpp
void ToggleWeaponWheel();
```
Toggles weapon wheel visibility.

#### ShowWeaponWheel / HideWeaponWheel
```cpp
void ShowWeaponWheel();
void HideWeaponWheel();
```
Shows/hides the weapon wheel.

#### IsWeaponWheelVisible
```cpp
bool IsWeaponWheelVisible() const;
```
Returns true if wheel is visible.

#### SelectWeaponSlot
```cpp
bool SelectWeaponSlot(EWeaponCategory Category);
```
Selects a weapon slot by category.

#### SelectWeaponSlotByIndex
```cpp
bool SelectWeaponSlotByIndex(int32 SlotIndex);
```
Selects a weapon slot by index.

#### CycleCurrentSlotWeapon
```cpp
void CycleCurrentSlotWeapon(bool bForward = true);
```
Cycles weapon in currently selected slot.

#### CycleSlotWeapon
```cpp
void CycleSlotWeapon(EWeaponCategory Category, bool bForward = true);
```
Cycles weapon in specific slot.

#### GetCurrentWeapon
```cpp
const FWeaponClassData* GetCurrentWeapon() const;
```
Returns currently equipped weapon data.

#### GetWeaponSlot
```cpp
const FWeaponSlotData* GetWeaponSlot(EWeaponCategory Category) const;
```
Returns slot data for category.

#### GetWeaponSlotByIndex
```cpp
const FWeaponSlotData* GetWeaponSlotByIndex(int32 SlotIndex) const;
```
Returns slot data for index.

#### GetAllWeaponSlots
```cpp
const TArray<FWeaponSlotData>& GetAllWeaponSlots() const;
```
Returns all weapon slots.

#### GetCurrentSlotIndex
```cpp
int32 GetCurrentSlotIndex() const;
```
Returns current slot index.

#### GetCurrentSlotCategory
```cpp
EWeaponCategory GetCurrentSlotCategory() const;
```
Returns current slot category.

#### AddAmmo
```cpp
void AddAmmo(const FGameplayTag& AmmoTag, int32 Amount);
```
Adds ammo to weapons matching tag.

#### GetCurrentAmmo
```cpp
int32 GetCurrentAmmo(const FGameplayTag& AmmoTag) const;
```
Returns current ammo for tag.

#### GetReserveAmmo
```cpp
int32 GetReserveAmmo(const FGameplayTag& AmmoTag) const;
```
Returns reserve ammo for tag.

#### ConsumeAmmo
```cpp
bool ConsumeAmmo(int32 Amount = 1);
```
Consumes ammo from current weapon.

#### ReloadCurrentWeapon
```cpp
bool ReloadCurrentWeapon();
```
Reloads current weapon from reserves.

#### CanReloadCurrentWeapon
```cpp
bool CanReloadCurrentWeapon() const;
```
Returns true if current weapon can reload.

#### UnlockWeaponSlot / LockWeaponSlot
```cpp
void UnlockWeaponSlot(EWeaponCategory Category);
void LockWeaponSlot(EWeaponCategory Category);
```
Unlocks/locks a weapon slot.

#### AddWeaponToSlot
```cpp
bool AddWeaponToSlot(EWeaponCategory Category, const FWeaponClassData& WeaponData);
```
Adds a weapon class to a slot.

#### RemoveWeaponFromSlot
```cpp
bool RemoveWeaponFromSlot(EWeaponCategory Category, const FGameplayTag& WeaponTag);
```
Removes a weapon class from a slot.

#### GetWeaponWheelWidget
```cpp
UUserWidget* GetWeaponWheelWidget() const;
```
Returns the weapon wheel widget instance.

#### OnWeaponWheelSelectionChanged
```cpp
void OnWeaponWheelSelectionChanged(int32 SlotIndex);
```
Called when wheel selection changes (from UI).

#### OnWeaponWheelConfirmSelection
```cpp
void OnWeaponWheelConfirmSelection();
```
Called when wheel confirms selection.

#### OnCycleWeaponInput
```cpp
void OnCycleWeaponInput(float Value);
```
Called when cycling weapons via input.

---

## UWeaponWheelWidget

UMG widget for the radial weapon wheel.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `WheelCanvas` | `UCanvasPanel*` | Root canvas panel |
| `CenterIcon` | `UImage*` | Center weapon icon |
| `CenterWeaponName` | `UTextBlock*` | Center weapon name |
| `CenterAmmoText` | `UTextBlock*` | Center ammo text |
| `CenterAmmoBar` | `UProgressBar*` | Center ammo bar |
| `OpenAnimation` | `UWidgetAnimation*` | Open animation |
| `CloseAnimation` | `UWidgetAnimation*` | Close animation |
| `SlotHoverAnimation` | `UWidgetAnimation*` | Slot hover animation |
| `SlotSelectAnimation` | `UWidgetAnimation*` | Slot select animation |

### Functions

#### InitializeWidget
```cpp
void InitializeWidget(UWeaponInventoryComponent* InInventoryComponent);
```
Initializes widget with inventory component.

#### UpdateWheel
```cpp
void UpdateWheel();
```
Updates the wheel display.

#### SetHoveredSlot
```cpp
void SetHoveredSlot(int32 SlotIndex);
```
Sets hovered slot index.

#### GetHoveredSlot
```cpp
int32 GetHoveredSlot() const;
```
Returns hovered slot index.

#### SetSelectedSlot
```cpp
void SetSelectedSlot(int32 SlotIndex);
```
Sets selected slot index.

#### HandleMouseWheel
```cpp
void HandleMouseWheel(float Delta);
```
Handles mouse wheel for cycling weapons.

#### HandleConfirmSelection
```cpp
void HandleConfirmSelection();
```
Handles confirm selection (click/enter).

---

## Delegates

### FOnWeaponEquipped
```cpp
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnWeaponEquipped, const FWeaponClassData*, WeaponData);
```
Broadcast when a weapon is equipped.

### FOnWeaponUnequipped
```cpp
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnWeaponUnequipped, const FWeaponClassData*, WeaponData);
```
Broadcast when a weapon is unequipped.

### FOnWeaponSlotChanged
```cpp
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnWeaponSlotChanged, EWeaponCategory, NewCategory);
```
Broadcast when weapon slot changes.

### FOnAmmoChanged
```cpp
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnAmmoChanged, const FGameplayTag&, AmmoTag, int32, NewAmount);
```
Broadcast when ammo amount changes.

---

## EWeaponCategory Enum

```cpp
enum class EWeaponCategory : uint8
{
    Primary,       // Assault Rifle, Sniper Rifle
    Secondary,     // Pistol
    Heavy,         // Rocket Launcher, Grenade Launcher
    Special,       // Shotgun
    Melee,         // Knife
    Utility,       // Gadgets, etc.
    MAX
};
```

---

## Usage Examples

### Blueprint: Toggle Weapon Wheel
```
Event IA_WeaponWheel (Triggered)
    -> WeaponInventory.ToggleWeaponWheel
```

### Blueprint: Cycle Weapon
```
Event IA_CycleWeapon (Triggered)
    -> Get Axis Value
    -> WeaponInventory.OnCycleWeaponInput(AxisValue)
```

### Blueprint: Select Weapon
```
Event IA_SelectWeapon (Triggered)
    -> WeaponInventory.OnWeaponWheelConfirmSelection
```

### C++: Add Custom Weapon
```cpp
UWeaponInventoryComponent* Inventory = Cast<UWeaponInventoryComponent>(
    GetOwner()->GetComponentByClass(UWeaponInventoryComponent::StaticClass())
);

if (Inventory)
{
    FWeaponClassData NewWeapon;
    NewWeapon.DisplayName = FText::FromString("Custom Weapon");
    NewWeapon.WeaponTag = FGameplayTag::RequestGameplayTag("Weapon.Custom");
    NewWeapon.WeaponClass = ACustomWeapon::StaticClass();
    NewWeapon.AmmoTag = FGameplayTag::RequestGameplayTag("Ammo.Custom");
    NewWeapon.MaxAmmo = 25;
    NewWeapon.ReserveAmmo = 100;
    NewWeapon.CurrentAmmo = 25;
    
    Inventory->AddWeaponToSlot(EWeaponCategory::Primary, NewWeapon);
}
```

### C++: Listen for Weapon Changes
```cpp
// In your character or component
UWeaponInventoryComponent* Inventory = ...;

Inventory->OnWeaponEquipped.AddDynamic(this, &AMyCharacter::OnWeaponEquipped);
Inventory->OnWeaponSlotChanged.AddDynamic(this, &AMyCharacter::OnWeaponSlotChanged);
Inventory->OnAmmoChanged.AddDynamic(this, &AMyCharacter::OnAmmoChanged);

void AMyCharacter::OnWeaponEquipped(const FWeaponClassData* WeaponData)
{
    if (WeaponData)
    {
        UE_LOG(LogTemp, Log, TEXT("Equipped: %s"), *WeaponData->DisplayName.ToString());
    }
}

void AMyCharacter::OnWeaponSlotChanged(EWeaponCategory NewCategory)
{
    UE_LOG(LogTemp, Log, TEXT("Slot changed to: %d"), (int32)NewCategory);
}

void AMyCharacter::OnAmmoChanged(const FGameplayTag& AmmoTag, int32 NewAmount)
{
    UE_LOG(LogTemp, Log, TEXT("Ammo %s: %d"), *AmmoTag.ToString(), NewAmount);
}
```