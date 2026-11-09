# Changelog

All notable changes to the Weapon Wheel System will be documented in this file.

## [1.0.0] - 2026-11-09

### Added
- **Weapon Wheel System** - Complete radial weapon selection system
- **EWeaponCategory Enum** - 6 categories: Primary, Secondary, Heavy, Special, Melee, Utility
- **FWeaponClassData Struct** - Individual weapon variant data (mesh, class, animations, ammo, icons)
- **FWeaponSlotData Struct** - Wheel slots supporting multiple weapon classes with cycling
- **UWeaponWheelConfig DataAsset** - Configuration asset for entire wheel setup
- **UWeaponInventoryComponent** - Actor component managing inventory and wheel
- **UWeaponWheelWidget** - UMG widget with animated radial layout

### Features
- **Radial UI** - 6-slot circular weapon wheel with smooth scale/fade animations
- **Multi-Weapon Slots** - Each slot holds multiple weapon variants (cycle with mouse wheel)
- **Enhanced Input Integration** - TAB (toggle), Mouse Wheel (cycle), LMB (select)
- **AnimGenExample Character Support** - Designed for AnimGenExample plugin character
- **MilitaryWeapDark Weapons** - Pre-configured for all 7 weapon types:
  - Assault Rifle (Assault_Rifle_B)
  - Pistol (Pistols_B)
  - Grenade Launcher (Grenade_Launcher_B)
  - Rocket Launcher (Rocket_launcher_B)
  - Shotgun (Shotgun_B)
  - Sniper Rifle (Sniper_Rifle_B)
  - Combat Knife (Knife_B)
- **Ammo Management** - Current/reserve tracking per weapon with UI display
- **Blueprint Events** - OnWeaponEquipped, OnWeaponUnequipped, OnWeaponSlotChanged, OnAmmoChanged
- **Slot Locking** - Lock/unlock weapon slots for progression systems
- **Dynamic Weapon Addition** - Add/remove weapons at runtime

### C++ Classes
- `WeaponTypes.h` - Core data structures and enums
- `WeaponInventoryComponent.h/.cpp` - Inventory management
- `WeaponWheelWidget.h/.cpp` - UMG widget implementation
- `MyProjectModule.h/.cpp` - Module entry point
- `MyProject.Build.cs` - Build configuration with required modules

### Automation
- **Python Setup Script** (`Scripts/setup_weapon_wheel.py`) - Automates:
  - Input Action creation
  - Input Mapping Context updates
  - Gameplay Tag registration
  - Widget Blueprint creation
  - WeaponWheelConfig DataAsset creation
  - Component addition to AnimGenCharacter

### Documentation
- `README.md` - Project overview and quick start
- `README_WeaponWheel.md` - Comprehensive system documentation
- `docs/API.md` - Complete API reference
- `Content/Weapons/WeaponWheelSetupGuide.md` - Step-by-step manual setup guide
- `CHANGELOG.md` - This file

### Configuration
- Default 6-slot layout with customizable angles
- Weapon attachment socket mapping per category
- Fallback to `Weapon_R` socket
- Configurable wheel radius (100-500) and animation duration (0.1-1.0s)
- Up to 8 visible slots supported

---

## Planned Features (Future Versions)

### [1.1.0] - Planned
- [ ] Gamepad support (stick navigation, D-pad selection)
- [ ] Weapon preview animations in wheel center
- [ ] Ammo pickup/weapon pickup integration
- [ ] Save/load inventory state
- [ ] Weapon customization/attachments per variant

### [1.2.0] - Planned
- [ ] Multiplayer replication support
- [ ] AI weapon selection
- [ ] Weapon wheel hotkeys (number keys)
- [ ] Custom widget themes/skins