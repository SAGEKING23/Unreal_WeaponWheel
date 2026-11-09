# Complete Setup Instructions

Follow these steps to fully set up the Weapon Wheel System in your Unreal project.

## Option 1: Run in Unreal Editor Python Console (Recommended)

1. **Open your project in Unreal Editor 5.8**
2. **Wait for C++ compilation to complete** (check Output Log)
3. **Open Python Console**: `Window` → `Output Log` → Click the `Python` tab (or `Tools` → `Python Console`)
4. **Run the complete setup script**:
   ```python
   exec(open("Scripts/complete_setup.py").read())
   ```
5. **Watch the Output Log** for progress messages
6. **Complete manual steps** listed at the end (input bindings in character blueprint)

## Option 2: Run as Commandlet (Headless)

```bash
# From your project directory
"C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe" MyProject.uproject -run=pythonscript -script=Scripts/complete_setup.py
```

## What the Script Does Automatically

✅ Creates **3 Input Actions**:
- `IA_WeaponWheel` (Digital/Bool, Tab key)
- `IA_CycleWeapon` (Axis1D, Mouse Wheel)
- `IA_SelectWeapon` (Digital/Bool, Left Mouse Button)

✅ Updates **IMC_Default** with all mappings

✅ Creates **13 Gameplay Tags**:
- Weapon.AssaultRifle, Pistol, GrenadeLauncher, RocketLauncher, Shotgun, SniperRifle, Knife
- Ammo.Rifle, Pistol, Grenade, Rocket, Shell, Sniper

✅ Creates **WBP_WeaponWheel** Widget Blueprint with:
- Root CanvasPanel (WheelCanvas)
- Center display: Icon, Name, Ammo Text, Ammo Bar
- 6 Slot containers with Background, Icon, Label, Ammo Bar
- Properly positioned at 60° intervals around 220px radius

✅ Creates **WeaponWheelConfig** DataAsset with all 7 MilitaryWeapDark weapons:
| Slot | Category | Weapons |
|------|----------|---------|
| 0 | Primary | Assault Rifle, Sniper Rifle |
| 1 | Secondary | Pistol |
| 2 | Heavy | Rocket Launcher, Grenade Launcher |
| 3 | Special | Shotgun |
| 4 | Melee | Combat Knife |
| 5 | Utility | (Locked) |

✅ Adds **WeaponInventoryComponent** to AnimGenCharacter with config reference

## Manual Steps Required After Script

### 1. Add Input Bindings in AnimGenCharacter Blueprint
1. Open `/Game/AnimGenExample/Blueprints/AnimGenCharacter`
2. Go to **Event Graph**
3. Right-click → **Add Event** → Search `IA_WeaponWheel` → Select **Enhanced Input Action**
4. From **Triggered** pin → Drag → Search `ToggleWeaponWheel` → Select `WeaponInventory.ToggleWeaponWheel`
5. Right-click → **Add Event** → Search `IA_CycleWeapon` → Select **Enhanced Input Action**
6. From **Triggered** pin → Drag → Search `Get Axis Value` → Connect to `WeaponInventory.OnCycleWeaponInput`
7. Right-click → **Add Event** → Search `IA_SelectWeapon` → Select **Enhanced Input Action**
8. From **Triggered** pin → Drag → Search `OnWeaponWheelConfirmSelection` → Select `WeaponInventory.OnWeaponWheelConfirmSelection`
9. **Compile** and **Save**

### 2. Add Animations to WBP_WeaponWheel
1. Open `/Game/Weapons/WBP_WeaponWheel`
2. Go to **Animations** tab
3. Create **OpenAnimation** (0.25s):
   - Add track for `WheelCanvas` → `RenderTransform.Scale` → 0 to 1
   - Add track for `WheelCanvas` → `RenderOpacity` → 0 to 1
4. Create **CloseAnimation** (0.25s):
   - Add track for `WheelCanvas` → `RenderTransform.Scale` → 1 to 0
   - Add track for `WheelCanvas` → `RenderOpacity` → 1 to 0
5. **Compile** and **Save**

### 3. Test
1. Click **Play** in the editor
2. Press **Tab** - weapon wheel should appear
3. Move mouse over slots - they should highlight
4. Scroll **Mouse Wheel** - should cycle weapons in hovered slot
5. Click **Left Mouse Button** - should equip weapon and close wheel

## Troubleshooting

### "WeaponInventoryComponent class not found"
- C++ hasn't compiled yet. Wait for compilation to finish (check Output Log)
- Or build from Visual Studio/Rider: Build → Build Solution

### "WeaponWheelConfig class not found"
- Same as above - compile C++ first

### Widget doesn't appear
- Check WBP_WeaponWheel parent class is `WeaponWheelWidget` (C++ class)
- Check WeaponWheelConfig has `WeaponWheelWidgetClass` set to `WBP_WeaponWheel_C`

### Input doesn't work
- Verify IMC_Default is in PlayerController's Input Mapping Contexts
- Check Input Actions have correct Value Types

### Weapons don't attach to character
- AnimGenCharacter mesh needs sockets: `Weapon_Primary`, `Weapon_Secondary`, `Weapon_Heavy`, `Weapon_Special`, `Weapon_Melee`, `Weapon_Utility`
- Falls back to `Weapon_R` if specific socket missing

## Verification Checklist

After setup, verify:
- [ ] C++ compiled successfully
- [ ] 3 Input Actions exist in `/Game/Input/Actions/`
- [ ] IMC_Default has 3 new mappings
- [ ] 13 Gameplay Tags exist in Project Settings
- [ ] WBP_WeaponWheel exists and has proper UI hierarchy
- [ ] WeaponWheelConfig exists with 6 slots and 7 weapons
- [ ] AnimGenCharacter has WeaponInventoryComponent
- [ ] Input bindings added in AnimGenCharacter Event Graph
- [ ] Open/Close animations created in WBP_WeaponWheel
- [ ] Play test works: Tab → hover → wheel → click

## Files Created

```
Scripts/
├── complete_setup.py              # Main setup script (run this)
├── CompleteSetupCommandlet.py     # Commandlet version
└── setup_weapon_wheel.py          # Original basic setup
```

## Support

If issues persist:
1. Check Output Log for errors
2. Verify all plugins enabled: AnimGenExample, EnhancedInput, GameplayAbilities
3. Ensure MilitaryWeapDark content is in project
4. Try rebuilding C++ project from IDE