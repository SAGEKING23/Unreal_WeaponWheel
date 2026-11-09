#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Weapon Wheel System Setup Script for Unreal Editor
Run this in the Unreal Editor Python console:
    exec(open("Scripts/setup_weapon_wheel.py").read())

Or run as a commandlet:
    UnrealEditor.exe -run=pythonscript -script=Scripts/setup_weapon_wheel.py
"""

import unreal

@unreal.uclass()
class WeaponWheelSetup(unreal.Object):
    """Utility class for setting up the weapon wheel system"""

    @unreal.ufunction(static=True)
    def create_input_action(action_name, value_type="Digital (bool)", trigger_type="Pressed"):
        """Create an Enhanced Input Action asset"""
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        factory = unreal.InputActionFactory()

        if "Axis" in value_type:
            factory.input_action_value_type = unreal.InputActionValueType.AXIS1D
        else:
            factory.input_action_value_type = unreal.InputActionValueType.DIGITAL_BOOL

        action = asset_tools.create_asset(
            asset_name=action_name,
            package_path="/Game/Input/Actions",
            asset_class=unreal.InputAction,
            factory=factory
        )

        if action:
            if "Axis" in value_type:
                action.set_editor_property("value_type", unreal.InputActionValueType.AXIS1D)
            else:
                action.set_editor_property("value_type", unreal.InputActionValueType.DIGITAL_BOOL)

            if trigger_type == "Pressed":
                action.set_editor_property("trigger_type", unreal.InputTriggerType.PRESSED)
            else:
                action.set_editor_property("trigger_type", unreal.InputTriggerType.RELEASED)

            unreal.EditorAssetLibrary.save_asset(action.get_path_name())
            unreal.log(f"Created Input Action: {action_name}")
        return action

    @unreal.ufunction(static=True)
    def add_mapping_to_imc(imc_path, action_path, key, modifiers=None):
        """Add a key mapping to an Input Mapping Context"""
        if modifiers is None:
            modifiers = []

        imc = unreal.EditorAssetLibrary.load_asset(imc_path)
        action = unreal.EditorAssetLibrary.load_asset(action_path)

        if not imc:
            unreal.log_error(f"Could not load IMC: {imc_path}")
            return False

        if not action:
            unreal.log_error(f"Could not load Input Action: {action_path}")
            return False

        # Check if mapping already exists
        existing_mappings = imc.get_mappings()
        for mapping in existing_mappings:
            if mapping.action == action and mapping.key == key:
                unreal.log(f"Mapping already exists: {action_path} -> {key}")
                return True

        imc.map_key(action, key, modifiers)
        unreal.EditorAssetLibrary.save_asset(imc_path)
        unreal.log(f"Added mapping: {action_path} -> {key}")
        return True

    @unreal.ufunction(static=True)
    def create_gameplay_tag(tag_name):
        """Create a gameplay tag if it doesn't exist"""
        tag = unreal.GameplayTag.request_gameplay_tag(tag_name)
        return tag

    @unreal.ufunction(static=True)
    def setup_gameplay_tags():
        """Set up all required gameplay tags"""
        tags = [
            "Weapon.AssaultRifle",
            "Weapon.Pistol",
            "Weapon.GrenadeLauncher",
            "Weapon.RocketLauncher",
            "Weapon.Shotgun",
            "Weapon.SniperRifle",
            "Weapon.Knife",
            "Ammo.Rifle",
            "Ammo.Pistol",
            "Ammo.Grenade",
            "Ammo.Rocket",
            "Ammo.Shell",
            "Ammo.Sniper"
        ]

        for tag_name in tags:
            WeaponWheelSetup.create_gameplay_tag(tag_name)

        unreal.log("Gameplay tags created/verified")

    @unreal.ufunction(static=True)
    def create_weapon_wheel_widget():
        """Create the Weapon Wheel Widget Blueprint"""
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        factory = unreal.WidgetBlueprintFactory()

        # Get the C++ widget class
        widget_class = unreal.load_class(None, "/Script/MyProject.WeaponWheelWidget")

        widget_bp = asset_tools.create_asset(
            asset_name="WBP_WeaponWheel",
            package_path="/Game/Weapons",
            asset_class=unreal.WidgetBlueprint,
            factory=factory
        )

        if widget_bp:
            # Set parent class to our C++ widget
            widget_bp.set_editor_property("parent_class", widget_class)
            unreal.EditorAssetLibrary.save_asset(widget_bp.get_path_name())
            unreal.log("Created WBP_WeaponWheel widget blueprint")
        return widget_bp

    @unreal.ufunction(static=True)
    def create_weapon_wheel_config():
        """Create the WeaponWheelConfig data asset"""
        # This requires the C++ class to be compiled
        config_class = unreal.load_class(None, "/Script/MyProject.WeaponWheelConfig")
        if not config_class:
            unreal.log_error("WeaponWheelConfig class not found. Compile C++ first!")
            return None

        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        factory = unreal.DataAssetFactory()
        factory.data_asset_class = config_class

        config = asset_tools.create_asset(
            asset_name="WeaponWheelConfig",
            package_path="/Game/Weapons",
            asset_class=config_class,
            factory=factory
        )

        if not config:
            unreal.log_error("Failed to create WeaponWheelConfig")
            return None

        # Define weapon data
        weapon_classes = {
            "AssaultRifle": "/Game/MilitaryWeapDark/Weapons/Assault_Rifle_B.Assault_Rifle_B_C",
            "Pistol": "/Game/MilitaryWeapDark/Weapons/Pistols_B.Pistols_B_C",
            "GrenadeLauncher": "/Game/MilitaryWeapDark/Weapons/Grenade_Launcher_B.Grenade_Launcher_B_C",
            "RocketLauncher": "/Game/MilitaryWeapDark/Weapons/Rocket_launcher_B.Rocket_launcher_B_C",
            "Shotgun": "/Game/MilitaryWeapDark/Weapons/Shotgun_B.Shotgun_B_C",
            "SniperRifle": "/Game/MilitaryWeapDark/Weapons/Sniper_Rifle_B.Sniper_Rifle_B_C",
            "Knife": "/Game/MilitaryWeapDark/Weapons/Knife_B.Knife_B_C",
        }

        # Create slots
        slots = []

        # Helper to create weapon data
        def create_weapon_data(name, tag_name, class_path, ammo_tag_name, max_ammo, reserve_ammo):
            weapon_data = unreal.WeaponClassData()
            weapon_data.display_name = unreal.Text.from_string(name)
            weapon_data.weapon_tag = unreal.GameplayTag.request_gameplay_tag(tag_name)
            weapon_data.weapon_class = unreal.load_class(None, class_path)
            weapon_data.ammo_tag = unreal.GameplayTag.request_gameplay_tag(ammo_tag_name) if ammo_tag_name else unreal.GameplayTag()
            weapon_data.max_ammo = max_ammo
            weapon_data.reserve_ammo = reserve_ammo
            weapon_data.current_ammo = max_ammo
            return weapon_data

        # Slot 0: Primary (-90°)
        primary_slot = unreal.WeaponSlotData()
        primary_slot.category = unreal.EWeaponCategory.PRIMARY
        primary_slot.slot_name = unreal.Text.from_string("Primary")
        primary_slot.wheel_angle = -90.0
        primary_slot.is_unlocked = True
        primary_slot.available_weapons.append(
            create_weapon_data("Assault Rifle", "Weapon.AssaultRifle", weapon_classes["AssaultRifle"],
                              "Ammo.Rifle", 30, 120)
        )
        primary_slot.available_weapons.append(
            create_weapon_data("Sniper Rifle", "Weapon.SniperRifle", weapon_classes["SniperRifle"],
                              "Ammo.Sniper", 5, 20)
        )
        slots.append(primary_slot)

        # Slot 1: Secondary (-30°)
        secondary_slot = unreal.WeaponSlotData()
        secondary_slot.category = unreal.EWeaponCategory.SECONDARY
        secondary_slot.slot_name = unreal.Text.from_string("Secondary")
        secondary_slot.wheel_angle = -30.0
        secondary_slot.is_unlocked = True
        secondary_slot.available_weapons.append(
            create_weapon_data("Pistol", "Weapon.Pistol", weapon_classes["Pistol"],
                              "Ammo.Pistol", 15, 60)
        )
        slots.append(secondary_slot)

        # Slot 2: Heavy (30°)
        heavy_slot = unreal.WeaponSlotData()
        heavy_slot.category = unreal.EWeaponCategory.HEAVY
        heavy_slot.slot_name = unreal.Text.from_string("Heavy")
        heavy_slot.wheel_angle = 30.0
        heavy_slot.is_unlocked = True
        heavy_slot.available_weapons.append(
            create_weapon_data("Rocket Launcher", "Weapon.RocketLauncher", weapon_classes["RocketLauncher"],
                              "Ammo.Rocket", 1, 3)
        )
        heavy_slot.available_weapons.append(
            create_weapon_data("Grenade Launcher", "Weapon.GrenadeLauncher", weapon_classes["GrenadeLauncher"],
                              "Ammo.Grenade", 1, 6)
        )
        slots.append(heavy_slot)

        # Slot 3: Special (90°)
        special_slot = unreal.WeaponSlotData()
        special_slot.category = unreal.EWeaponCategory.SPECIAL
        special_slot.slot_name = unreal.Text.from_string("Special")
        special_slot.wheel_angle = 90.0
        special_slot.is_unlocked = True
        special_slot.available_weapons.append(
            create_weapon_data("Shotgun", "Weapon.Shotgun", weapon_classes["Shotgun"],
                              "Ammo.Shell", 8, 32)
        )
        slots.append(special_slot)

        # Slot 4: Melee (150°)
        melee_slot = unreal.WeaponSlotData()
        melee_slot.category = unreal.EWeaponCategory.MELEE
        melee_slot.slot_name = unreal.Text.from_string("Melee")
        melee_slot.wheel_angle = 150.0
        melee_slot.is_unlocked = True
        melee_slot.available_weapons.append(
            create_weapon_data("Combat Knife", "Weapon.Knife", weapon_classes["Knife"],
                              "", 0, 0)
        )
        slots.append(melee_slot)

        # Slot 5: Utility (-150°) - Locked by default
        utility_slot = unreal.WeaponSlotData()
        utility_slot.category = unreal.EWeaponCategory.UTILITY
        utility_slot.slot_name = unreal.Text.from_string("Utility")
        utility_slot.wheel_angle = -150.0
        utility_slot.is_unlocked = False
        slots.append(utility_slot)

        # Set config properties
        config.set_editor_property("weapon_slots", slots)
        config.set_editor_property("max_visible_slots", 6)
        config.set_editor_property("wheel_radius", 220.0)
        config.set_editor_property("animation_duration", 0.25)

        # Set widget class
        widget_bp = unreal.EditorAssetLibrary.load_asset("/Game/Weapons/WBP_WeaponWheel")
        if widget_bp:
            config.set_editor_property("weapon_wheel_widget_class", widget_bp.generated_class)

        unreal.EditorAssetLibrary.save_asset(config.get_path_name())
        unreal.log(f"Created WeaponWheelConfig with {len(slots)} slots")
        return config

    @unreal.ufunction(static=True)
    def add_component_to_character():
        """Add WeaponInventoryComponent to AnimGenCharacter"""
        char_bp = unreal.EditorAssetLibrary.load_asset("/Game/AnimGenExample/Blueprints/AnimGenCharacter")
        if not char_bp:
            unreal.log_error("Could not load AnimGenCharacter")
            return False

        weapon_comp_class = unreal.load_class(None, "/Script/MyProject.WeaponInventoryComponent")
        if not weapon_comp_class:
            unreal.log_error("WeaponInventoryComponent class not found. Compile C++ first!")
            return False

        # Check if component already exists
        components = char_bp.get_components()
        for comp in components:
            if comp.get_class() == weapon_comp_class:
                unreal.log("WeaponInventoryComponent already exists on character")
                return True

        # Add component
        new_comp = char_bp.add_component(weapon_comp_class, "WeaponInventory")
        if new_comp:
            unreal.EditorAssetLibrary.save_asset(char_bp.get_path_name())
            unreal.log("Added WeaponInventoryComponent to AnimGenCharacter")
            return True

        return False

    @unreal.ufunction(static=True)
    def setup_input_bindings():
        """Set up input action bindings in the character blueprint"""
        char_bp = unreal.EditorAssetLibrary.load_asset("/Game/AnimGenExample/Blueprints/AnimGenCharacter")
        if not char_bp:
            unreal.log_error("Could not load AnimGenCharacter")
            return False

        # This would require Blueprint graph manipulation which is complex
        # Better to do manually in the editor
        unreal.log("Input bindings need to be set up manually in the AnimGenCharacter blueprint:")
        unreal.log("  1. Add Event for IA_WeaponWheel -> Call WeaponInventory.ToggleWeaponWheel")
        unreal.log("  2. Add Event for IA_CycleWeapon -> Call WeaponInventory.OnCycleWeaponInput(AxisValue)")
        unreal.log("  3. Add Event for IA_SelectWeapon -> Call WeaponInventory.OnWeaponWheelConfirmSelection")
        return True

    @unreal.ufunction(static=True)
    def run_full_setup():
        """Run the complete setup process"""
        unreal.log("=" * 50)
        unreal.log("Starting Weapon Wheel System Setup")
        unreal.log("=" * 50)

        # Step 1: Create Input Actions
        unreal.log("\n1. Creating Input Actions...")
        WeaponWheelSetup.create_input_action("IA_WeaponWheel", "Digital (bool)", "Pressed")
        WeaponWheelSetup.create_input_action("IA_CycleWeapon", "Axis1D", "Pressed")
        WeaponWheelSetup.create_input_action("IA_SelectWeapon", "Digital (bool)", "Pressed")

        # Step 2: Add mappings to IMC_Default
        unreal.log("\n2. Updating Input Mapping Context...")
        WeaponWheelSetup.add_mapping_to_imc("/Game/Input/IMC_Default", "/Game/Input/Actions/IA_WeaponWheel", unreal.Key.TAB)
        WeaponWheelSetup.add_mapping_to_imc("/Game/Input/IMC_Default", "/Game/Input/Actions/IA_CycleWeapon", unreal.Key.MOUSE_WHEEL_AXIS)
        WeaponWheelSetup.add_mapping_to_imc("/Game/Input/IMC_Default", "/Game/Input/Actions/IA_SelectWeapon", unreal.Key.LEFT_MOUSE_BUTTON)

        # Step 3: Set up Gameplay Tags
        unreal.log("\n3. Setting up Gameplay Tags...")
        WeaponWheelSetup.setup_gameplay_tags()

        # Step 4: Create Widget Blueprint
        unreal.log("\n4. Creating Widget Blueprint...")
        WeaponWheelSetup.create_weapon_wheel_widget()

        # Step 5: Create Weapon Wheel Config (requires C++ compilation)
        unreal.log("\n5. Creating Weapon Wheel Config...")
        config = WeaponWheelSetup.create_weapon_wheel_config()

        # Step 6: Add component to character
        unreal.log("\n6. Adding component to character...")
        WeaponWheelSetup.add_component_to_character()

        # Step 7: Input bindings (manual)
        unreal.log("\n7. Input bindings (manual step required)...")
        WeaponWheelSetup.setup_input_bindings()

        unreal.log("\n" + "=" * 50)
        unreal.log("Setup Complete!")
        unreal.log("=" * 50)
        unreal.log("Next steps:")
        unreal.log("  1. Compile C++ code if not already done")
        unreal.log("  2. Open WBP_WeaponWheel and design the UI (see WeaponWheelSetupGuide.md)")
        unreal.log("  3. Set up input bindings in AnimGenCharacter blueprint")
        unreal.log("  4. Test in Play mode - press TAB to open weapon wheel")


# Run the setup if executed directly
if __name__ == "__main__":
    WeaponWheelSetup.run_full_setup()