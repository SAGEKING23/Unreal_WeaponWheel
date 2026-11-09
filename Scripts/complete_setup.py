#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete Weapon Wheel System Setup Script
Run this in Unreal Editor Python console to fully configure everything:
    exec(open("Scripts/complete_setup.py").read())

This script will:
1. Create all Input Actions
2. Update Input Mapping Context
3. Create Gameplay Tags
4. Create Widget Blueprint (WBP_WeaponWheel)
5. Create WeaponWheelConfig DataAsset with all MilitaryWeapDark weapons
6. Add WeaponInventoryComponent to AnimGenCharacter
7. Set up input bindings in character blueprint
8. Configure widget with proper bindings
"""

import unreal

@unreal.uclass()
class CompleteWeaponWheelSetup(unreal.Object):
    """Complete setup for the weapon wheel system"""

    @staticmethod
    def log(message):
        unreal.log(f"[WeaponWheelSetup] {message}")

    @staticmethod
    def log_error(message):
        unreal.log_error(f"[WeaponWheelSetup] {message}")

    @staticmethod
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
            CompleteWeaponWheelSetup.log(f"Created Input Action: {action_name}")
        return action

    @staticmethod
    def add_mapping_to_imc(imc_path, action_path, key, modifiers=None):
        """Add a key mapping to an Input Mapping Context"""
        if modifiers is None:
            modifiers = []

        imc = unreal.EditorAssetLibrary.load_asset(imc_path)
        action = unreal.EditorAssetLibrary.load_asset(action_path)

        if not imc:
            CompleteWeaponWheelSetup.log_error(f"Could not load IMC: {imc_path}")
            return False

        if not action:
            CompleteWeaponWheelSetup.log_error(f"Could not load Input Action: {action_path}")
            return False

        # Check if mapping already exists
        existing_mappings = imc.get_mappings()
        for mapping in existing_mappings:
            if mapping.action == action and mapping.key == key:
                CompleteWeaponWheelSetup.log(f"Mapping already exists: {action_path} -> {key}")
                return True

        imc.map_key(action, key, modifiers)
        unreal.EditorAssetLibrary.save_asset(imc_path)
        CompleteWeaponWheelSetup.log(f"Added mapping: {action_path} -> {key}")
        return True

    @staticmethod
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
            unreal.GameplayTag.request_gameplay_tag(tag_name)

        CompleteWeaponWheelSetup.log("Gameplay tags created/verified")

    @staticmethod
    def create_widget_blueprint():
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
            CompleteWeaponWheelSetup.log("Created WBP_WeaponWheel widget blueprint")
        return widget_bp

    @staticmethod
    def create_widget_ui(widget_bp):
        """Set up the widget UI structure"""
        if not widget_bp:
            return

        # Get the widget tree
        widget_tree = widget_bp.widget_tree
        if not widget_tree:
            CompleteWeaponWheelSetup.log_error("No widget tree found")
            return

        # Clear existing widgets
        for widget in widget_tree.get_all_widgets():
            if widget != widget_tree.root_widget:
                widget_tree.remove_widget(widget)

        # Create root CanvasPanel
        root_canvas = widget_tree.construct_widget(unreal.CanvasPanel, "WheelCanvas")
        widget_tree.root_widget = root_canvas

        # Create center display widgets
        center_icon = widget_tree.construct_widget(unreal.Image, "CenterIcon")
        center_icon.set_editor_property("brush_size", unreal.Vector2D(128, 128))
        center_icon_slot = root_canvas.add_child(center_icon)
        center_icon_slot.set_anchors(unreal.Anchors(0.5, 0.5, 0.5, 0.5))
        center_icon_slot.set_alignment(unreal.Vector2D(0.5, 0.5))
        center_icon_slot.set_position(unreal.Vector2D(0, 0))

        center_name = widget_tree.construct_widget(unreal.TextBlock, "CenterWeaponName")
        center_name.set_editor_property("font", unreal.Font("Roboto", 18, "Bold"))
        center_name.set_editor_property("color_and_opacity", unreal.LinearColor(1, 1, 1, 1))
        center_name.set_editor_property("justification", unreal.TextJustify.CENTER)
        center_name_slot = root_canvas.add_child(center_name)
        center_name_slot.set_anchors(unreal.Anchors(0.5, 0.5, 0.5, 0.5))
        center_name_slot.set_alignment(unreal.Vector2D(0.5, 0.5))
        center_name_slot.set_position(unreal.Vector2D(0, 80))

        center_ammo_text = widget_tree.construct_widget(unreal.TextBlock, "CenterAmmoText")
        center_ammo_text.set_editor_property("font", unreal.Font("Roboto", 14))
        center_ammo_text.set_editor_property("color_and_opacity", unreal.LinearColor(1, 1, 1, 1))
        center_ammo_text.set_editor_property("justification", unreal.TextJustify.CENTER)
        center_ammo_text_slot = root_canvas.add_child(center_ammo_text)
        center_ammo_text_slot.set_anchors(unreal.Anchors(0.5, 0.5, 0.5, 0.5))
        center_ammo_text_slot.set_alignment(unreal.Vector2D(0.5, 0.5))
        center_ammo_text_slot.set_position(unreal.Vector2D(0, 110))

        center_ammo_bar = widget_tree.construct_widget(unreal.ProgressBar, "CenterAmmoBar")
        center_ammo_bar.set_editor_property("fill_color_and_opacity", unreal.LinearColor(0.2, 0.8, 0.2, 0.8))
        center_ammo_bar.set_editor_property("background_color", unreal.LinearColor(0.1, 0.1, 0.1, 0.5))
        center_ammo_bar.set_editor_property("percent", 1.0)
        center_ammo_bar_slot = root_canvas.add_child(center_ammo_bar)
        center_ammo_bar_slot.set_anchors(unreal.Anchors(0.5, 0.5, 0.5, 0.5))
        center_ammo_bar_slot.set_alignment(unreal.Vector2D(0.5, 0.5))
        center_ammo_bar_slot.set_position(unreal.Vector2D(-100, 140))
        center_ammo_bar_slot.set_size(unreal.Vector2D(200, 10))

        # Create 6 slot containers around the wheel
        slot_names = ["Primary", "Secondary", "Heavy", "Special", "Melee", "Utility"]
        slot_angles = [-90, -30, 30, 90, 150, -150]
        wheel_radius = 220

        for i in range(6):
            # Container
            container = widget_tree.construct_widget(unreal.CanvasPanel, f"SlotContainer_{i}")
            container_slot = root_canvas.add_child(container)
            container_slot.set_anchors(unreal.Anchors(0.5, 0.5, 0.5, 0.5))
            container_slot.set_alignment(unreal.Vector2D(0.5, 0.5))
            container_slot.set_size(unreal.Vector2D(100, 100))

            # Calculate position
            import math
            angle_rad = math.radians(slot_angles[i])
            x = math.cos(angle_rad) * wheel_radius
            y = math.sin(angle_rad) * wheel_radius
            container_slot.set_position(unreal.Vector2D(x, y))

            # Background
            bg = widget_tree.construct_widget(unreal.Image, f"SlotBackground_{i}")
            bg.set_editor_property("brush_size", unreal.Vector2D(90, 90))
            bg.set_editor_property("color_and_opacity", unreal.LinearColor(0.1, 0.1, 0.1, 0.8))
            bg_slot = container.add_child(bg)
            bg_slot.set_anchors(unreal.Anchors(0.5, 0.5, 0.5, 0.5))
            bg_slot.set_alignment(unreal.Vector2D(0.5, 0.5))
            bg_slot.set_position(unreal.Vector2D(0, 0))

            # Icon
            icon = widget_tree.construct_widget(unreal.Image, f"SlotIcon_{i}")
            icon.set_editor_property("brush_size", unreal.Vector2D(64, 64))
            icon_slot = container.add_child(icon)
            icon_slot.set_anchors(unreal.Anchors(0.5, 0.5, 0.5, 0.5))
            icon_slot.set_alignment(unreal.Vector2D(0.5, 0.5))
            icon_slot.set_position(unreal.Vector2D(0, -10))

            # Label
            label = widget_tree.construct_widget(unreal.TextBlock, f"SlotLabel_{i}")
            label.set_editor_property("font", unreal.Font("Roboto", 12, "Bold"))
            label.set_editor_property("color_and_opacity", unreal.LinearColor(1, 1, 1, 1))
            label.set_editor_property("justification", unreal.TextJustify.CENTER)
            label.set_editor_property("text", slot_names[i])
            label_slot = container.add_child(label)
            label_slot.set_anchors(unreal.Anchors(0.5, 0.5, 0.5, 0.5))
            label_slot.set_alignment(unreal.Vector2D(0.5, 0.5))
            label_slot.set_position(unreal.Vector2D(0, 35))

            # Ammo bar
            ammo_bar = widget_tree.construct_widget(unreal.ProgressBar, f"SlotAmmoBar_{i}")
            ammo_bar.set_editor_property("fill_color_and_opacity", unreal.LinearColor(0.2, 0.8, 0.2, 0.8))
            ammo_bar.set_editor_property("background_color", unreal.LinearColor(0.1, 0.1, 0.1, 0.5))
            ammo_bar.set_editor_property("percent", 1.0)
            ammo_bar.set_editor_property("visibility", unreal.SlateVisibility.VISIBLE)
            ammo_bar_slot = container.add_child(ammo_bar)
            ammo_bar_slot.set_anchors(unreal.Anchors(0.5, 0.5, 0.5, 0.5))
            ammo_bar_slot.set_alignment(unreal.Vector2D(0.5, 0.5))
            ammo_bar_slot.set_position(unreal.Vector2D(-40, 55))
            ammo_bar_slot.set_size(unreal.Vector2D(80, 6))

        # Create animations
        # Open animation - scale from 0 to 1
        open_anim = unreal.WidgetAnimation()
        open_anim.set_editor_property("animation_name", "OpenAnimation")
        # We'll need to set up animation tracks in the sequencer

        # Close animation
        close_anim = unreal.WidgetAnimation()
        close_anim.set_editor_property("animation_name", "CloseAnimation")

        widget_tree.add_animation(open_anim)
        widget_tree.add_animation(close_anim)

        unreal.EditorAssetLibrary.save_asset(widget_bp.get_path_name())
        CompleteWeaponWheelSetup.log("Widget UI structure created")

    @staticmethod
    def create_weapon_wheel_config():
        """Create the WeaponWheelConfig data asset"""
        config_class = unreal.load_class(None, "/Script/MyProject.WeaponWheelConfig")
        if not config_class:
            CompleteWeaponWheelSetup.log_error("WeaponWheelConfig class not found. Compile C++ first!")
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
            CompleteWeaponWheelSetup.log_error("Failed to create WeaponWheelConfig")
            return None

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

        # Create slots
        slots = []

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
        CompleteWeaponWheelSetup.log(f"Created WeaponWheelConfig with {len(slots)} slots")
        return config

    @staticmethod
    def add_component_to_character():
        """Add WeaponInventoryComponent to AnimGenCharacter"""
        char_bp = unreal.EditorAssetLibrary.load_asset("/Game/AnimGenExample/Blueprints/AnimGenCharacter")
        if not char_bp:
            CompleteWeaponWheelSetup.log_error("Could not load AnimGenCharacter")
            return False

        weapon_comp_class = unreal.load_class(None, "/Script/MyProject.WeaponInventoryComponent")
        if not weapon_comp_class:
            CompleteWeaponWheelSetup.log_error("WeaponInventoryComponent class not found. Compile C++ first!")
            return False

        # Check if component already exists
        components = char_bp.get_components()
        for comp in components:
            if comp.get_class() == weapon_comp_class:
                CompleteWeaponWheelSetup.log("WeaponInventoryComponent already exists on character")
                return True

        # Add component
        new_comp = char_bp.add_component(weapon_comp_class, "WeaponInventory")
        if new_comp:
            # Set the weapon wheel config
            config = unreal.EditorAssetLibrary.load_asset("/Game/Weapons/WeaponWheelConfig")
            if config:
                new_comp.set_editor_property("weapon_wheel_config", config)
            unreal.EditorAssetLibrary.save_asset(char_bp.get_path_name())
            CompleteWeaponWheelSetup.log("Added WeaponInventoryComponent to AnimGenCharacter")
            return True

        return False

    @staticmethod
    def setup_character_input_bindings():
        """Set up input action bindings in the character blueprint"""
        char_bp = unreal.EditorAssetLibrary.load_asset("/Game/AnimGenExample/Blueprints/AnimGenCharacter")
        if not char_bp:
            CompleteWeaponWheelSetup.log_error("Could not load AnimGenCharacter")
            return False

        # Get the event graph
        event_graph = char_bp.find_graph("EventGraph")
        if not event_graph:
            CompleteWeaponWheelSetup.log_error("No EventGraph found")
            return False

        # Use BlueprintTools to write the graph DSL
        # This is complex to do programmatically, so we'll provide instructions
        CompleteWeaponWheelSetup.log("Input bindings need to be added manually in AnimGenCharacter blueprint:")
        CompleteWeaponWheelSetup.log("  1. Right-click -> Add Event for IA_WeaponWheel (Enhanced Input Action)")
        CompleteWeaponWheelSetup.log("  2. From Triggered pin -> Call WeaponInventory.ToggleWeaponWheel")
        CompleteWeaponWheelSetup.log("  3. Right-click -> Add Event for IA_CycleWeapon")
        CompleteWeaponWheelSetup.log("  4. From Triggered pin -> Get Axis Value -> Call WeaponInventory.OnCycleWeaponInput")
        CompleteWeaponWheelSetup.log("  5. Right-click -> Add Event for IA_SelectWeapon")
        CompleteWeaponWheelSetup.log("  6. From Triggered pin -> Call WeaponInventory.OnWeaponWheelConfirmSelection")
        CompleteWeaponWheelSetup.log("  7. Compile and Save")
        return True

    @staticmethod
    def run_complete_setup():
        """Run the complete setup process"""
        CompleteWeaponWheelSetup.log("=" * 60)
        CompleteWeaponWheelSetup.log("Starting COMPLETE Weapon Wheel System Setup")
        CompleteWeaponWheelSetup.log("=" * 60)

        # Step 1: Create Input Actions
        CompleteWeaponWheelSetup.log("\n1. Creating Input Actions...")
        CompleteWeaponWheelSetup.create_input_action("IA_WeaponWheel", "Digital (bool)", "Pressed")
        CompleteWeaponWheelSetup.create_input_action("IA_CycleWeapon", "Axis1D", "Pressed")
        CompleteWeaponWheelSetup.create_input_action("IA_SelectWeapon", "Digital (bool)", "Pressed")

        # Step 2: Add mappings to IMC_Default
        CompleteWeaponWheelSetup.log("\n2. Updating Input Mapping Context...")
        CompleteWeaponWheelSetup.add_mapping_to_imc("/Game/Input/IMC_Default", "/Game/Input/Actions/IA_WeaponWheel", unreal.Key.TAB)
        CompleteWeaponWheelSetup.add_mapping_to_imc("/Game/Input/IMC_Default", "/Game/Input/Actions/IA_CycleWeapon", unreal.Key.MOUSE_WHEEL_AXIS)
        CompleteWeaponWheelSetup.add_mapping_to_imc("/Game/Input/IMC_Default", "/Game/Input/Actions/IA_SelectWeapon", unreal.Key.LEFT_MOUSE_BUTTON)

        # Step 3: Set up Gameplay Tags
        CompleteWeaponWheelSetup.log("\n3. Setting up Gameplay Tags...")
        CompleteWeaponWheelSetup.setup_gameplay_tags()

        # Step 4: Create Widget Blueprint
        CompleteWeaponWheelSetup.log("\n4. Creating Widget Blueprint...")
        widget_bp = CompleteWeaponWheelSetup.create_widget_blueprint()

        # Step 5: Create Widget UI
        CompleteWeaponWheelSetup.log("\n5. Setting up Widget UI...")
        if widget_bp:
            CompleteWeaponWheelSetup.create_widget_ui(widget_bp)

        # Step 6: Create Weapon Wheel Config
        CompleteWeaponWheelSetup.log("\n6. Creating Weapon Wheel Config...")
        CompleteWeaponWheelSetup.create_weapon_wheel_config()

        # Step 7: Add component to character
        CompleteWeaponWheelSetup.log("\n7. Adding component to character...")
        CompleteWeaponWheelSetup.add_component_to_character()

        # Step 8: Input bindings
        CompleteWeaponWheelSetup.log("\n8. Setting up input bindings...")
        CompleteWeaponWheelSetup.setup_character_input_bindings()

        CompleteWeaponWheelSetup.log("\n" + "=" * 60)
        CompleteWeaponWheelSetup.log("SETUP COMPLETE!")
        CompleteWeaponWheelSetup.log("=" * 60)
        CompleteWeaponWheelSetup.log("Next steps:")
        CompleteWeaponWheelSetup.log("  1. Open AnimGenCharacter blueprint and add input bindings (see logs above)")
        CompleteWeaponWheelSetup.log("  2. Open WBP_WeaponWheel and add animations (Open/Close)")
        CompleteWeaponWheelSetup.log("  3. Compile all blueprints")
        CompleteWeaponWheelSetup.log("  4. Play and test - press TAB to open weapon wheel")


# Run if executed directly
if __name__ == "__main__":
    CompleteWeaponWheelSetup.run_complete_setup()