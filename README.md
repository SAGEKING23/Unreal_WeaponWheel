# MyProject - Weapon Wheel System

A complete weapon wheel implementation for Unreal Engine 5.8 featuring radial weapon selection, multi-weapon slots, and integration with the AnimGenExample character and MilitaryWeapDark weapon collection.

## Features

- **Radial Weapon Wheel** - 6-slot circular weapon selection UI with smooth animations
- **Multi-Weapon Slots** - Each slot supports multiple weapon variants (cycle with mouse wheel)
- **Enhanced Input Integration** - Uses UE5 Enhanced Input system (TAB to open, Mouse Wheel to cycle, LMB to select)
- **AnimGen Character Support** - Designed for the AnimGenExample plugin character
- **MilitaryWeapDark Weapons** - Pre-configured for all 7 weapon types
- **Ammo Management** - Tracks current/reserve ammo per weapon with UI display
- **Blueprint Extensible** - Full Blueprint exposure for customization

## Weapon Configuration

| Slot | Category | Angle | Weapons |
|------|----------|-------|---------|
| 0 | Primary | -90° (Top) | Assault Rifle, Sniper Rifle |
| 1 | Secondary | -30° (Top-Right) | Pistol |
| 2 | Heavy | 30° (Bottom-Right) | Rocket Launcher, Grenade Launcher |
| 3 | Special | 90° (Bottom) | Shotgun |
| 4 | Melee | 150° (Bottom-Left) | Combat Knife |
| 5 | Utility | -150° (Top-Left) | Locked by default |

## Quick Start

### Prerequisites
- Unreal Engine 5.8+
- AnimGenExample plugin enabled
- MilitaryWeapDark content pack
- Enhanced Input plugin (enabled by default)
- Gameplay Abilities plugin (for GameplayTags)

### Installation

1. Clone this repository
2. Open `MyProject.uproject` in Unreal Editor 5.8
3. Allow C++ compilation when prompted
4. Run the setup script in the Editor Python console:
   ```python
   exec(open("Scripts/setup_weapon_wheel.py").read())
   ```
5. Follow the manual steps in `Content/Weapons/WeaponWheelSetupGuide.md` to complete widget setup

### Manual Setup (if not using script)

See [WeaponWheelSetupGuide.md](Content/Weapons/WeaponWheelSetupGuide.md) for detailed instructions.

## Architecture

### C++ Classes

```
Source/MyProject/
├── Public/
│   ├── WeaponTypes.h              # Core data structures
│   ├── WeaponInventoryComponent.h # Inventory management component
│   ├── WeaponWheelWidget.h        # UMG widget for weapon wheel
│   └── MyProject.h                # Module header
├── Private/
│   ├── WeaponInventoryComponent.cpp
│   ├── WeaponWheelWidget.cpp
│   ├── MyProjectModule.h/.cpp     # Module implementation
│   └── MyProjectPrivatePCH.h
└── MyProject.Build.cs             # Build configuration
```

### Core Data Structures

**WeaponTypes.h**
- `EWeaponCategory` - Enum for weapon slots
- `FWeaponClassData` - Individual weapon variant data
- `FWeaponSlotData` - Wheel slot with multiple weapon support
- `UWeaponWheelConfig` - Data asset for wheel configuration

**WeaponInventoryComponent**
- Weapon equipping/unequipping with socket attachment
- Ammo management (current/reserve per weapon)
- Weapon wheel widget lifecycle management
- Blueprint events: `OnWeaponEquipped`, `OnWeaponUnequipped`, `OnWeaponSlotChanged`, `OnAmmoChanged`

**WeaponWheelWidget**
- Radial layout with animated open/close
- Dynamic slot creation (up to 8 slots)
- Hover/selection visual feedback
- Center display for weapon details
- Mouse wheel cycling support

## Input Bindings

| Action | Key | Description |
|--------|-----|-------------|
| IA_WeaponWheel | Tab | Toggle weapon wheel |
| IA_CycleWeapon | Mouse Wheel | Cycle weapons in current slot |
| IA_SelectWeapon | Left Mouse Button | Confirm selection |

## Gameplay Tags

```
Weapon.AssaultRifle, Weapon.Pistol, Weapon.GrenadeLauncher
Weapon.RocketLauncher, Weapon.Shotgun, Weapon.SniperRifle, Weapon.Knife
Ammo.Rifle, Ammo.Pistol, Ammo.Grenade, Ammo.Rocket, Ammo.Shell, Ammo.Sniper
```

## Extending the System

### Add Weapon to Slot (C++)
```cpp
UWeaponInventoryComponent* Inventory = GetWeaponInventory();
FWeaponClassData NewWeapon;
NewWeapon.DisplayName = FText::FromString("New Weapon");
NewWeapon.WeaponTag = FGameplayTag::RequestGameplayTag("Weapon.NewWeapon");
NewWeapon.WeaponClass = ANewWeaponClass::StaticClass();
NewWeapon.AmmoTag = FGameplayTag::RequestGameplayTag("Ammo.NewType");
NewWeapon.MaxAmmo = 30;
NewWeapon.ReserveAmmo = 120;
NewWeapon.CurrentAmmo = 30;

Inventory->AddWeaponToSlot(EWeaponCategory::Primary, NewWeapon);
```

### Unlock Utility Slot
```cpp
Inventory->UnlockWeaponSlot(EWeaponCategory::Utility);
```

### Add Ammo
```cpp
Inventory->AddAmmo(AmmoTag, Amount);
```

### Get Current Weapon
```cpp
const FWeaponClassData* CurrentWeapon = Inventory->GetCurrentWeapon();
```

## Weapon Attachment Sockets

Expected sockets on character mesh:
- `Weapon_Primary`, `Weapon_Secondary`, `Weapon_Heavy`
- `Weapon_Special`, `Weapon_Melee`, `Weapon_Utility`

Falls back to `Weapon_R` if specific socket not found.

## Project Structure

```
MyProject/
├── Source/MyProject/           # C++ source code
├── Content/
│   ├── Weapons/               # Weapon assets, configs, widgets
│   │   ├── WeaponWheelSetupGuide.md
│   │   └── (generated assets)
│   ├── Input/                 # Enhanced Input actions/contexts
│   └── Maps/                  # Levels
├── Scripts/
│   └── setup_weapon_wheel.py  # Automated setup script
├── MyProject.uproject         # Project descriptor
├── README.md                  # This file
└── README_WeaponWheel.md      # Detailed system documentation
```

## License

This project is for educational and development purposes.

## Credits

- AnimGenExample plugin by Epic Games
- MilitaryWeapDark weapon pack
- Unreal Engine 5.8