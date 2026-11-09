#!/usr/bin/env python3
"""
Setup script for Weapon Wheel System
Run this in Unreal Editor Python console or as a commandlet
"""

import unreal

def create_input_action(action_name, label, description, value_type="Digital (bool)", trigger_type="Pressed"):
    """Create an Enhanced Input Action asset"""
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory = unreal.InputActionFactory()
    factory.input_action_value_type = unreal.InputActionValueType.DIGITAL_BOOL if "Digital" in value_type else unreal.InputActionValueType.AXIS1D

    action = asset_tools.create_asset(
        asset_name=action_name,
        package_path="/Game/Input/Actions",
        asset_class=unreal.InputAction,
        factory=factory
    )

    if action:
        action.set_editor_property("value_type", unreal.InputActionValueType.DIGITAL_BOOL if "Digital" in value_type else unreal.InputActionValueType.AXIS1D)
        action.set_editor_property("trigger_type", unreal.InputTriggerType.PRESSED if trigger_type == "Pressed" else unreal.InputTriggerType.RELEASED)
        unreal.EditorAssetLibrary.save_asset(action.get_path_name())
        print(f"Created Input Action: {action_name}")
    return action

def create_input_mapping_context(name, mappings):
    """Create an Input Mapping Context with the given mappings"""
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory = unreal.InputMappingContextFactory()

    imc = asset_tools.create_asset(
        asset_name=name,
        package_path="/Game/Input",
        asset_class=unreal.InputMappingContext,
        factory=factory
    )

    if imc:
        for mapping in mappings:
            imc.map_key(mapping["action"], mapping["key"], mapping.get("modifiers", []))
        unreal.EditorAssetLibrary.save_asset(imc.get_path_name())
        print(f"Created Input Mapping Context: {name}")
    return imc

def update_existing_imc(imc_path, new_mappings):
    """Add mappings to an existing Input Mapping Context"""
    imc = unreal.EditorAssetLibrary.load_asset(imc_path)
    if not imc:
        print(f"Could not load IMC: {imc_path}")
        return None

    for mapping in new_mappings:
        action = unreal.EditorAssetLibrary.load_asset(mapping["action_path"])
        if action:
            imc.map_key(action, mapping["key"], mapping.get("modifiers", []))

    unreal.EditorAssetLibrary.save_asset(imc_path)
    print(f"Updated IMC: {imc_path}")
    return imc

def create_weapon_wheel_config():
    """Create the WeaponWheelConfig data asset with MilitaryWeapDark weapons"""
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory = unreal.DataAssetFactory()
    factory.data_asset_class = unreal.load_class(None, "/Script/MyProject.WeaponWheelConfig")

    config = asset_tools.create_asset(
        asset_name="WeaponWheelConfig",
        package_path="/Game/Weapons",
        asset_class=unreal.load_class(None, "/Script/MyProject.WeaponWheelConfig"),
        factory=factory
    )

    if not config:
        print("Could not create WeaponWheelConfig - class may not be compiled yet")
        return None

    # Define weapon tags
    weapon_tags = {
        "AssaultRifle": unreal.GameplayTag.request_gameplay_tag("Weapon.AssaultRifle"),
        "Pistol": unreal.GameplayTag.request_gameplay_tag("Weapon.Pistol"),
        "GrenadeLauncher": unreal.GameplayTag.request_gameplay_tag("Weapon.GrenadeLauncher"),
        "RocketLauncher": unreal.GameplayTag.request_gameplay_tag("Weapon.RocketLauncher"),
        "Shotgun": unreal.GameplayTag.request_gameplay_tag("Weapon.Shotgun"),
        "SniperRifle": unreal.GameplayTag.request_gameplay_tag("Weapon.SniperRifle"),
        "Knife": unreal.GameplayTag.request_gameplay_tag("Weapon.Knife"),
    }

    ammo_tags = {
        "Rifle": unreal.GameplayTag.request_gameplay_tag("Ammo.Rifle"),
        "Pistol": unreal.GameplayTag.request_gameplay_tag("Ammo.Pistol"),
        "Grenade": unreal.GameplayTag.request_gameplay_tag("Ammo.Grenade"),
        "Rocket": unreal.GameplayTag.request_gameplay_tag("Ammo.Rocket"),
        "Shell": unreal.GameplayTag.request_gameplay_tag("Ammo.Shell"),
        "Sniper": unreal.GameplayTag.request_gameplay_tag("Ammo.Sniper"),
    }

    # Weapon class paths from MilitaryWeapDark
    weapon_classes = {
        "AssaultRifle": "/Game/MilitaryWeapDark/Weapons/Assault_Rifle_B.Assault_Rifle_B_C",
        "Pistol": "/Game/MilitaryWeapDark/Weapons/Pistols_B.Pistols_B_C",
        "GrenadeLauncher": "/Game/MilitaryWeapDark/Weapons/Grenade_Launcher_B.Grenade_Launcher_B_C",
        "RocketLauncher": "/Game/MilitaryWeapDark/Weapons/Rocket_launcher_B.Rocket_launcher_B_C",
        "Shotgun": "/Game/MilitaryWeapDark/Weapons/Shotgun_B.Shotgun_B_C",
        "SniperRifle": "/Game/MilitaryWeapDark/Weapons/Sniper_Rifle_B.Sniper_Rifle_B_C",
        "Knife": "/Game/MilitaryWeapDark/Weapons/Knife_B.Knife_B_C",
    }

    # Create weapon slot data
    slots = []

    # Primary Slot (Assault Rifle, Sniper Rifle)
    primary_slot = unreal.WeaponSlotData()
    primary_slot.category = unreal.EWeaponCategory.PRIMARY
    primary_slot.slot_name = unreal.Text.from_string("Primary")
    primary_slot.wheel_angle = -90.0  # Top
    primary_slot.is_unlocked = True

    # Assault Rifle variant
    ar_data = unreal.WeaponClassData()
    ar_data.display_name = unreal.Text.from_string("Assault Rifle")
    ar_data.weapon_tag = weapon_tags["AssaultRifle"]
    ar_data.weapon_class = unreal.load_class(None, weapon_classes["AssaultRifle"])
    ar_data.ammo_tag = ammo_tags["Rifle"]
    ar_data.max_ammo = 30
    ar_data.reserve_ammo = 120
    ar_data.current_ammo = 30
    primary_slot.available_weapons.append(ar_data)

    # Sniper Rifle variant
    sr_data = unreal.WeaponClassData()
    sr_data.display_name = unreal.Text.from_string("Sniper Rifle")
    sr_data.weapon_tag = weapon_tags["SniperRifle"]
    sr_data.weapon_class = unreal.load_class(None, weapon_classes["SniperRifle"])
    sr_data.ammo_tag = ammo_tags["Sniper"]
    sr_data.max_ammo = 5
    sr_data.reserve_ammo = 20
    sr_data.current_ammo = 5
    primary_slot.available_weapons.append(sr_data)

    slots.append(primary_slot)

    # Secondary Slot (Pistol)
    secondary_slot = unreal.WeaponSlotData()
    secondary_slot.category = unreal.EWeaponCategory.SECONDARY
    secondary_slot.slot_name = unreal.Text.from_string("Secondary")
    secondary_slot.wheel_angle = -30.0  # Top-right
    secondary_slot.is_unlocked = True

    pistol_data = unreal.WeaponClassData()
    pistol_data.display_name = unreal.Text.from_string("Pistol")
    pistol_data.weapon_tag = weapon_tags["Pistol"]
    pistol_data.weapon_class = unreal.load_class(None, weapon_classes["Pistol"])
    pistol_data.ammo_tag = ammo_tags["Pistol"]
    pistol_data.max_ammo = 15
    pistol_data.reserve_ammo = 60
    pistol_data.current_ammo = 15
    secondary_slot.available_weapons.append(pistol_data)

    slots.append(secondary_slot)

    # Heavy Slot (Rocket Launcher, Grenade Launcher)
    heavy_slot = unreal.WeaponSlotData()
    heavy_slot.category = unreal.EWeaponCategory.HEAVY
    heavy_slot.slot_name = unreal.Text.from_string("Heavy")
    heavy_slot.wheel_angle = 30.0  # Bottom-right
    heavy_slot.is_unlocked = True

    rl_data = unreal.WeaponClassData()
    rl_data.display_name = unreal.Text.from_string("Rocket Launcher")
    rl_data.weapon_tag = weapon_tags["RocketLauncher"]
    rl_data.weapon_class = unreal.load_class(None, weapon_classes["RocketLauncher"])
    rl_data.ammo_tag = ammo_tags["Rocket"]
    rl_data.max_ammo = 1
    rl_data.reserve_ammo = 3
    rl_data.current_ammo = 1
    heavy_slot.available_weapons.append(rl_data)

    gl_data = unreal.WeaponClassData()
    gl_data.display_name = unreal.Text.from_string("Grenade Launcher")
    gl_data.weapon_tag = weapon_tags["GrenadeLauncher"]
    gl_data.weapon_class = unreal.load_class(None, weapon_classes["GrenadeLauncher"])
    gl_data.ammo_tag = ammo_tags["Grenade"]
    gl_data.max_ammo = 1
    gl_data.reserve_ammo = 6
    gl_data.current_ammo = 1
    heavy_slot.available_weapons.append(gl_data)

    slots.append(heavy_slot)

    # Special Slot (Shotgun)
    special_slot = unreal.WeaponSlotData()
    special_slot.category = unreal.EWeaponCategory.SPECIAL
    special_slot.slot_name = unreal.Text.from_string("Special")
    special_slot.wheel_angle = 90.0  # Bottom
    special_slot.is_unlocked = True

    sg_data = unreal.WeaponClassData()
    sg_data.display_name = unreal.Text.from_string("Shotgun")
    sg_data.weapon_tag = weapon_tags["Shotgun"]
    sg_data.weapon_class = unreal.load_class(None, weapon_classes["Shotgun"])
    sg_data.ammo_tag = ammo_tags["Shell"]
    sg_data.max_ammo = 8
    sg_data.reserve_ammo = 32
    sg_data.current_ammo = 8
    special_slot.available_weapons.append(sg_data)

    slots.append(special_slot)

    # Melee Slot (Knife)
    melee_slot = unreal.WeaponSlotData()
    melee_slot.category = unreal.EWeaponCategory.MELEE
    melee_slot.slot_name = unreal.Text.from_string("Melee")
    melee_slot.wheel_angle = 150.0  # Bottom-left
    melee_slot.is_unlocked = True

    knife_data = unreal.WeaponClassData()
    knife_data.display_name = unreal.Text.from_string("Combat Knife")
    knife_data.weapon_tag = weapon_tags["Knife"]
    knife_data.weapon_class = unreal.load_class(None, weapon_classes["Knife"])
    knife_data.ammo_tag = unreal.GameplayTag()  # No ammo
    knife_data.max_ammo = 0
    knife_data.reserve_ammo = 0
    knife_data.current_ammo = 0
    melee_slot.available_weapons.append(knife_data)

    slots.append(melee_slot)

    # Set config properties
    config.weapon_slots = slots
    config.max_visible_slots = 6
    config.wheel_radius = 220.0
    config.animation_duration = 0.25

    # Try to load the widget class
    widget_class = unreal.load_class(None, "/Game/Weapons/WBP_WeaponWheel.WBP_WeaponWheel_C")
    if widget_class:
        config.weapon_wheel_widget_class = widget_class

    unreal.EditorAssetLibrary.save_asset(config.get_path_name())
    print(f"Created WeaponWheelConfig with {len(slots)} slots")
    return config

def create_weapon_wheel_widget():
    """Create the Weapon Wheel UMG Widget Blueprint"""
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory = unreal.WidgetBlueprintFactory()

    widget_bp = asset_tools.create_asset(
        asset_name="WBP_WeaponWheel",
        package_path="/Game/Weapons",
        asset_class=unreal.WidgetBlueprint,
        factory=factory
    )

    if widget_bp:
        # The widget will be designed in the editor
        # But we can set up the basic structure here
        unreal.EditorAssetLibrary.save_asset(widget_bp.get_path_name())
        print("Created WBP_WeaponWheel widget blueprint")
    return widget_bp

def setup_animgen_character():
    """Add WeaponInventoryComponent to the AnimGen character"""
    # Load the AnimGen character blueprint
    char_bp = unreal.EditorAssetLibrary.load_asset("/Game/AnimGenExample/Blueprints/AnimGenCharacter")
    if not char_bp:
        print("Could not load AnimGenCharacter")
        return

    # Add the component
    weapon_comp_class = unreal.load_class(None, "/Script/MyProject.WeaponInventoryComponent")
    if weapon_comp_class:
        # Add component to blueprint
        char_bp.add_component(weapon_comp_class, "WeaponInventory")
        unreal.EditorAssetLibrary.save_asset(char_bp.get_path_name())
        print("Added WeaponInventoryComponent to AnimGenCharacter")

def main():
    print("Setting up Weapon Wheel System...")

    # Create Input Actions
    ia_weapon_wheel = create_input_action(
        "IA_WeaponWheel", "Weapon Wheel", "Toggle weapon wheel",
        "Digital (bool)", "Pressed"
    )

    ia_cycle_weapon = create_input_action(
        "IA_CycleWeapon", "Cycle Weapon", "Cycle weapons in current slot",
        "Axis1D", "Pressed"
    )

    ia_select_weapon = create_input_action(
        "IA_SelectWeapon", "Select Weapon", "Confirm weapon selection",
        "Digital (bool)", "Pressed"
    )

    # Update existing IMC_Default to include weapon wheel mappings
    update_existing_imc("/Game/Input/IMC_Default", [
        {
            "action_path": "/Game/Input/Actions/IA_WeaponWheel",
            "key": unreal.Key.Tab,
            "modifiers": []
        },
        {
            "action_path": "/Game/Input/Actions/IA_CycleWeapon",
            "key": unreal.Key.MouseWheelAxis,
            "modifiers": []
        },
        {
            "action_path": "/Game/Input/Actions/IA_SelectWeapon",
            "key": unreal.Key.LeftMouseButton,
            "modifiers": []
        }
    ])

    # Create the weapon wheel widget
    create_weapon_wheel_widget()

    # Create weapon wheel config (will work after C++ compilation)
    # create_weapon_wheel_config()

    print("Setup complete! Please compile C++ code, then run create_weapon_wheel_config()")

if __name__ == "__main__":
    main()