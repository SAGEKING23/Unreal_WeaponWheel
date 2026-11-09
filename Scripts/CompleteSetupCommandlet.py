#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unreal Editor Commandlet for Weapon Wheel Setup
Run from command line:
    UnrealEditor.exe -run=pythonscript -script=Scripts/CompleteSetupCommandlet.py
"""

import unreal
import sys

# Import our setup class
exec(open(r"C:\Users\SAGEKING\Documents\Unreal Projects\MyProject\Scripts\complete_setup.py").read())

if __name__ == "__main__":
    # This runs when executed as a commandlet
    unreal.log("Running Weapon Wheel Setup Commandlet...")
    CompleteWeaponWheelSetup.run_complete_setup()
    unreal.log("Commandlet complete!")