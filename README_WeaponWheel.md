# Weapon Wheel System for MyProject

A complete weapon wheel implementation for Unreal Engine 5.8 using the AnimGenExample character and MilitaryWeapDark weapon collection.

## Features

- **Radial Weapon Wheel**: Round wheel with 6 weapon slots (Primary, Secondary, Heavy, Special, Melee, Utility)
- **Weapon Classes per Slot**: Each slot supports multiple weapon variants (e.g., Primary has Assault Rifle + Sniper Rifle)
- **Mouse Wheel Cycling**: Scroll to cycle through weapons in the currently hovered slot
- **Hover Selection**: Move mouse over slots to preview, click to equip
- **Enhanced Input Integration**: Uses UE5 Enhanced Input system (TAB to open, Mouse Wheel to cycle, LMB to select)
- **Ammo Management**: Tracks current/reserve ammo per weapon with UI display
- **AnimGen Character Integration**: Designed for the AnimGenExample character blueprint
- **MilitaryWeapDark Weapons**: Pre-configured for all 7 weapon types in the collection

## Weapon Slots Configuration

| Slot | Category | Angle | Weapons |
|------|----------|-------|---------|
| 0 | Primary | -90° (Top) | Assault Rifle, Sniper Rifle |
| 1 | Secondary | -30° (Top-Right) | Pistol |
| 2 | Heavy | 30° (Bottom-Right) | Rocket Launcher, Grenade Launcher |
| 3 | Special | 90° (Bottom) | Shotgun |
| 4 | Melee | 150° (Bottom-Left) | Combat Knife |
| 5 | Utility | -150° (Top-Left) | (Locked/Empty) |

## Quick Start

### 1. Compile C++ Code
Open the project in Unreal Editor. The C++ code should compile automatically. If not, build from your IDE (Visual Studio/Rider).

### 2. Run Setup Script
In the Unreal Editor Python console:
```python
exec(open("Scripts/setup_weapon_wheel.py").read())
```

Or run the full setup:
```python
import unreal
from Scripts.setup_weapon_wheel import WeaponWheelSetup
WeaponWheelSetup.run_full_setup()
```

### 3. Manual Setup Steps (if not using script)

#### Create Input Actions
1. **IA_WeaponWheel** - Digital (bool), Trigger: Pressed
2. **IA_CycleWeapon** - Axis1D, Trigger: Pressed
3. **IA_SelectWeapon** - Digital (bool), Trigger: Pressed

#### Update IMC_Default
Add mappings:
- `IA_WeaponWheel` → `Tab`
- `IA_CycleWeapon` → `Mouse Wheel Axis`
- `IA_SelectWeapon` → `Left Mouse Button`

#### Create Gameplay Tags
Add to Project Settings → Gameplay Tags:
```
Weapon.AssaultRifle, Weapon.Pistol, Weapon.GrenadeLauncher, Weapon.RocketLauncher
Weapon.Shotgun, Weapon.SniperRifle, Weapon.Knife
Ammo.Rifle, Ammo.Pistol, Ammo.Grenade, Ammo.Rocket, Ammo.Shell, Ammo.Sniper
```

#### Create Widget Blueprint
1. Right-click Content/Weapons → User Interface → Widget Blueprint
2. Name: `WBP_WeaponWheel`
3. Parent Class: `WeaponWheelWidget` (C++ class)
4. Design UI per `WeaponWheelSetupGuide.md`

#### Create WeaponWheelConfig Data Asset
1. Right-click Content/Weapons → Miscellaneous → Data Asset
2. Class: `WeaponWheelConfig`
3. Configure 6 slots with MilitaryWeapDark weapon classes

#### Add Component to Character
1. Open `/Game/AnimGenExample/Blueprints/AnimGenCharacter`
2. Add Component → `WeaponInventoryComponent`
3. Set `Weapon Wheel Config` to your data asset

#### Bind Input in Character Blueprint
In AnimGenCharacter Event Graph:
- `IA_WeaponWheel` (Triggered) → `WeaponInventory.ToggleWeaponWheel`
- `IA_CycleWeapon` (Triggered) → `WeaponInventory.OnCycleWeaponInput(AxisValue)`
- `IA_SelectWeapon` (Triggered) → `WeaponInventory.OnWeaponWheelConfirmSelection`

### 4. Test
1. Press **Play**
2. Press **Tab** to open weapon wheel
3. Hover mouse over slots
4. Scroll **Mouse Wheel** to cycle weapons in slot
5. Click **Left Mouse Button** to equip and close

## C++ Classes

### WeaponTypes.h
- `EWeaponCategory` - Enum for weapon slots (Primary, Secondary, Heavy, Special, Melee, Utility)
- `FWeaponClassData` - Data for individual weapon variants
- `FWeaponSlotData` - Data for a wheel slot (holds multiple weapon classes)
- `UWeaponWheelConfig` - Data asset for wheel configuration

### WeaponInventoryComponent.h/cpp
- Manages weapon inventory and wheel state
- Handles equipping/unequipping weapons
- Manages ammo (current/reserve)
- Creates and updates the weapon wheel widget
- Blueprint events for weapon equipped/unequipped/slot changed/ammo changed

### WeaponWheelWidget.h/cpp
- UMG widget for the radial weapon wheel
- Animates open/close with scale/fade
- Displays slot icons, labels, ammo bars
- Center display for selected weapon details
- Hover/selection visual feedback

## Weapon Attachment Sockets

The system expects these sockets on the character mesh:
- `Weapon_Primary` - Primary weapons
- `Weapon_Secondary` - Secondary weapons
- `Weapon_Heavy` - Heavy weapons
- `Weapon_Special` - Special weapons
- `Weapon_Melee` - Melee weapons
- `Weapon_Utility` - Utility items

Falls back to `Weapon_R` if specific socket not found.

## Extending the System

### Adding New Weapon Classes to a Slot
```cpp
// In C++ or Blueprint
WeaponInventory->AddWeaponToSlot(EWeaponCategory::Primary, NewWeaponData);
```

### Unlocking Utility Slot
```cpp
WeaponInventory->UnlockWeaponSlot(EWeaponCategory::Utility);
```

### Adding Ammo
```cpp
WeaponInventory->AddAmmo(AmmoTag, Amount);
```

### Getting Current Weapon
```cpp
const FWeaponClassData* CurrentWeapon = WeaponInventory->GetCurrentWeapon();
```

## Files

```
Source/MyProject/
├── Public/
│   ├── WeaponTypes.h           # Data structures and config
│   ├── WeaponInventoryComponent.h
│   ├── WeaponWheelWidget.h
│   └── MyProject.h
├── Private/
│   ├── WeaponInventoryComponent.cpp
│   ├── WeaponWheelWidget.cpp
│   ├── MyProjectModule.h/.cpp
│   └── MyProjectPrivatePCH.h
└── MyProject.Build.cs

Content/Weapons/
├── WeaponWheelSetupGuide.md    # Detailed setup guide
└── (Widget and Config assets created at runtime)

Scripts/
└── setup_weapon_wheel.py       # Automated setup script
```

## Requirements

- Unreal Engine 5.8+
- AnimGenExample plugin enabled
- MilitaryWeapDark content pack
- Enhanced Input plugin (enabled by default)
- Gameplay Abilities plugin (for GameplayTags)

## Troubleshooting

**Widget not appearing?**
- Verify `WeaponWheelConfig.WeaponWheelWidgetClass` points to `WBP_WeaponWheel_C`
- Check `WBP_WeaponWheel` inherits from `WeaponWheelWidget` C++ class

**Weapons not attaching?**
- Ensure character mesh has weapon sockets (`Weapon_Primary`, `Weapon_Secondary`, etc.)
- Check weapon blueprints have proper collision/attachment setup

**Input not working?**
- Verify `IMC_Default` is in PlayerController's Input Mapping Contexts
- Check Input Actions have correct Value Types

**C++ compile errors?**
- Ensure all modules in `MyProject.Build.cs` PublicDependencyModuleNames
- Run `GenerateProjectFiles.bat` and rebuild