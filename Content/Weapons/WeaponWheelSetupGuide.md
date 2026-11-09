# Weapon Wheel System Setup Guide

This guide walks you through setting up the weapon wheel system in the Unreal Editor after compiling the C++ code.

## 1. Compile C++ Code

1. Open the project in Unreal Editor
2. Open the **Output Log** (Window → Output Log)
3. The C++ code should compile automatically, or you can build from Visual Studio/Rider

## 2. Create Input Action for Weapon Wheel (IA_WeaponWheel)

1. Right-click in **Content Browser** → **Input** → **Input Action**
2. Name it `IA_WeaponWeapon`
3. Open it and set:
   - **Value Type**: Digital (bool)
   - **Trigger Type**: Pressed
   - **Is Triggered When Paused**: false

## 3. Create Input Action for Cycling Weapons (IA_CycleWeapon)

1. Right-click in **Content Browser** → **Input** → **Input Action**
2. Name it `IA_CycleWeapon`
3. Open it and set:
   - **Value Type**: Axis1D
   - **Trigger Type**: Down (or Pressed)

## 4. Create Input Action for Selecting Weapon (IA_SelectWeapon)

1. Right-click in **Content Browser** → **Input** → **Input Action**
2. Name it `IA_SelectWeapon`
3. Open it and set:
   - **Value Type**: Digital (bool)
   - **Trigger Type**: Pressed

## 5. Update Input Mapping Context (IMC_Default)

1. Open `/Game/Input/IMC_Default`
2. Add the following mappings:

| Input Action | Key | Modifiers |
|--------------|-----|-----------|
| IA_WeaponWheel | Tab | (none) |
| IA_CycleWeapon | Mouse Wheel Axis | (none) |
| IA_SelectWeapon | Left Mouse Button | (none) |

3. Save the asset

## 6. Create Weapon Wheel Widget (WBP_WeaponWheel)

1. Right-click in **Content/Weapons** → **User Interface** → **Widget Blueprint**
2. Name it `WBP_WeaponWheel`
3. Parent Class: `WeaponWheelWidget` (your C++ class)
4. Open the widget and design the UI:

### Widget Hierarchy:
```
CanvasPanel (WheelCanvas) - Root
├── CanvasPanel (SlotContainer_0) - For slot 0
│   ├── Image (Background_0)
│   ├── Image (Icon_0)
│   ├── TextBlock (Label_0)
│   └── ProgressBar (AmmoBar_0)
├── CanvasPanel (SlotContainer_1) - For slot 1
│   ├── Image (Background_1)
│   ├── Image (Icon_1)
│   ├── TextBlock (Label_1)
│   └── ProgressBar (AmmoBar_1)
... (repeat for up to 8 slots)
├── Image (CenterIcon) - Large center icon
├── TextBlock (CenterWeaponName) - Weapon name
├── TextBlock (CenterAmmoText) - Ammo count
└── ProgressBar (CenterAmmoBar) - Ammo bar
```

### Animations to Create:
- **OpenAnimation**: 0.25s - Scale from 0 to 1, fade in
- **CloseAnimation**: 0.25s - Scale from 1 to 0, fade out
- **SlotHoverAnimation**: 0.1s - Scale up slot background
- **SlotSelectAnimation**: 0.1s - Pulse effect

### Bind Widgets:
In the widget's Graph tab, bind all the named widgets to the C++ properties (they use `meta = (BindWidget)`).

## 7. Create Weapon Wheel Config Data Asset

1. Right-click in **Content/Weapons** → **Miscellaneous** → **Data Asset**
2. Select `WeaponWheelConfig` as the Data Asset Class
3. Name it `WeaponWheelConfig`
4. Open and configure:

### Weapon Slots (6 slots):

#### Slot 0 - Primary (Angle: -90°)
- **Category**: Primary
- **Slot Name**: "Primary"
- **Wheel Angle**: -90.0
- **Is Unlocked**: true
- **Available Weapons**:
  - **Assault Rifle**:
    - Display Name: "Assault Rifle"
    - Weapon Tag: Weapon.AssaultRifle
    - Weapon Class: `/Game/MilitaryWeapDark/Weapons/Assault_Rifle_B.Assault_Rifle_B_C`
    - Ammo Tag: Ammo.Rifle
    - Max Ammo: 30
    - Reserve Ammo: 120
    - Current Ammo: 30
  - **Sniper Rifle**:
    - Display Name: "Sniper Rifle"
    - Weapon Tag: Weapon.SniperRifle
    - Weapon Class: `/Game/MilitaryWeapDark/Weapons/Sniper_Rifle_B.Sniper_Rifle_B_C`
    - Ammo Tag: Ammo.Sniper
    - Max Ammo: 5
    - Reserve Ammo: 20
    - Current Ammo: 5

#### Slot 1 - Secondary (Angle: -30°)
- **Category**: Secondary
- **Slot Name**: "Secondary"
- **Wheel Angle**: -30.0
- **Is Unlocked**: true
- **Available Weapons**:
  - **Pistol**:
    - Display Name: "Pistol"
    - Weapon Tag: Weapon.Pistol
    - Weapon Class: `/Game/MilitaryWeapDark/Weapons/Pistols_B.Pistols_B_C`
    - Ammo Tag: Ammo.Pistol
    - Max Ammo: 15
    - Reserve Ammo: 60
    - Current Ammo: 15

#### Slot 2 - Heavy (Angle: 30°)
- **Category**: Heavy
- **Slot Name**: "Heavy"
- **Wheel Angle**: 30.0
- **Is Unlocked**: true
- **Available Weapons**:
  - **Rocket Launcher**:
    - Display Name: "Rocket Launcher"
    - Weapon Tag: Weapon.RocketLauncher
    - Weapon Class: `/Game/MilitaryWeapDark/Weapons/Rocket_launcher_B.Rocket_launcher_B_C`
    - Ammo Tag: Ammo.Rocket
    - Max Ammo: 1
    - Reserve Ammo: 3
    - Current Ammo: 1
  - **Grenade Launcher**:
    - Display Name: "Grenade Launcher"
    - Weapon Tag: Weapon.GrenadeLauncher
    - Weapon Class: `/Game/MilitaryWeapDark/Weapons/Grenade_Launcher_B.Grenade_Launcher_B_C`
    - Ammo Tag: Ammo.Grenade
    - Max Ammo: 1
    - Reserve Ammo: 6
    - Current Ammo: 1

#### Slot 3 - Special (Angle: 90°)
- **Category**: Special
- **Slot Name**: "Special"
- **Wheel Angle**: 90.0
- **Is Unlocked**: true
- **Available Weapons**:
  - **Shotgun**:
    - Display Name: "Shotgun"
    - Weapon Tag: Weapon.Shotgun
    - Weapon Class: `/Game/MilitaryWeapDark/Weapons/Shotgun_B.Shotgun_B_C`
    - Ammo Tag: Ammo.Shell
    - Max Ammo: 8
    - Reserve Ammo: 32
    - Current Ammo: 8

#### Slot 4 - Melee (Angle: 150°)
- **Category**: Melee
- **Slot Name**: "Melee"
- **Wheel Angle**: 150.0
- **Is Unlocked**: true
- **Available Weapons**:
  - **Combat Knife**:
    - Display Name: "Combat Knife"
    - Weapon Tag: Weapon.Knife
    - Weapon Class: `/Game/MilitaryWeapDark/Weapons/Knife_B.Knife_B_C`
    - Ammo Tag: (None)
    - Max Ammo: 0
    - Reserve Ammo: 0
    - Current Ammo: 0

#### Slot 5 - Utility (Angle: -150°) - Optional
- **Category**: Utility
- **Slot Name**: "Utility"
- **Wheel Angle**: -150.0
- **Is Unlocked**: false (locked by default)
- **Available Weapons**: (empty)

### Config Settings:
- **Max Visible Slots**: 6
- **Wheel Radius**: 220.0
- **Animation Duration**: 0.25
- **Weapon Wheel Widget Class**: `WBP_WeaponWheel_C`

## 8. Add WeaponInventoryComponent to AnimGen Character

1. Open `/Game/AnimGenExample/Blueprints/AnimGenCharacter`
2. Click **Add Component** → Search for `WeaponInventoryComponent`
3. Name it `WeaponInventory`
4. In the **Details** panel, set:
   - **Weapon Wheel Config**: `WeaponWheelConfig` (the data asset you created)
5. Compile and Save

## 9. Set Up Input Binding in Character Blueprint

1. In `AnimGenCharacter` blueprint, go to **Event Graph**
2. Right-click → Search for `IA_WeaponWheel` → **Enhanced Input Action** event
3. From the **Triggered** pin, call `WeaponInventory.ToggleWeaponWheel`
4. Repeat for `IA_CycleWeapon`:
   - Get the **Axis Value** from the event
   - Call `WeaponInventory.OnCycleWeaponInput` with the axis value
5. Repeat for `IA_SelectWeapon`:
   - From **Triggered**, call `WeaponInventory.OnWeaponWheelConfirmSelection`

## 10. Set Up Mouse Hover Detection for Slots

In `WBP_WeaponWheel` widget blueprint:

1. For each slot container, add **OnMouseEnter** event:
   - Call `SetHoveredSlot` with the slot index
2. Add **OnMouseLeave** event:
   - Call `SetHoveredSlot` with -1
3. Add **OnMouseButtonDown** event (Left Mouse Button):
   - Call `SetSelectedSlot` with the slot index
4. Add **OnMouseButtonUp** event (Left Mouse Button):
   - Call `HandleConfirmSelection`

Or use a single script that detects which slot is under the mouse cursor each tick.

## 11. Create Gameplay Tags

Go to **Project Settings** → **Gameplay Tags** and add:

```
Weapon
├── AssaultRifle
├── Pistol
├── GrenadeLauncher
├── RocketLauncher
├── Shotgun
├── SniperRifle
└── Knife

Ammo
├── Rifle
├── Pistol
├── Grenade
├── Rocket
├── Shell
└── Sniper
```

## 12. Test the System

1. Play the game
2. Press **Tab** to open the weapon wheel
3. Move mouse over slots to hover
4. Scroll **Mouse Wheel** to cycle weapons in the current slot
5. Click **Left Mouse Button** to select and close the wheel
6. The character should equip the selected weapon

## Troubleshooting

### Weapon not appearing on character:
- Check that the character mesh has sockets named `Weapon_Primary`, `Weapon_Secondary`, `Weapon_Heavy`, `Weapon_Special`, `Weapon_Melee`, `Weapon_Utility`
- Or it will fall back to `Weapon_R` socket

### Widget not showing:
- Verify `WeaponWheelConfig` has the correct `WeaponWheelWidgetClass` set
- Check that `WBP_WeaponWheel` inherits from `WeaponWheelWidget` C++ class

### Input not working:
- Verify `IMC_Default` is added to the player controller's input mapping contexts
- Check that the Input Actions have correct Value Types and Triggers

### C++ compilation errors:
- Ensure all module dependencies are in `MyProject.Build.cs`
- Check that `EnhancedInput`, `UMG`, `GameplayTags`, `GameplayAbilities` modules are listed