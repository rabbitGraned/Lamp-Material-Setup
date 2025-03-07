"""
lampMSPlugin
Lamp Material Setup (plugin-script for Maya)

Version:    2.1
Author:     rabbitGraned
License:    Apache 2.0

"""

import maya.cmds as cmds
from lampMaterialSetup import show_ui
import os

def initializePlugin(plugin):

    plugin_name = "Lamp Material Setup"
    version = "2.1"
    author = "rabbitGraned"

    try:
        if not cmds.commandPort(':7005', query=True):
            cmds.commandPort(name=':7005', sourceType="python")
    except RuntimeError:
        pass
    
    cmds.evalDeferred("import lampMaterialSetup; lampMaterialSetup.show_ui()")

    cmds.evalDeferred(add_shelf_button)
    
    print(f"{plugin_name} v{version} by {author} loaded successfully.")

def uninitializePlugin(plugin):

    if cmds.commandPort(name=':7005', query=True):
        cmds.commandPort(name=':7005', close=True)
    print("Lamp Material Setup unloaded.")

def add_shelf_button():

    shelf_name = "Custom"
    button_label = ""
    button_tooltip = "Lamp Material Setup"
    icon_name = "lampMSPlugin_icon.png"

    if not cmds.shelfLayout(shelf_name, exists=True):
        cmds.shelfLayout(shelf_name, parent="ShelfLayout")
    
    icon_path = os.path.join(cmds.internalVar(userAppDir=True), "modules", "lamp_material_setup", "icons", icon_name)

    if not os.path.exists(icon_path):
        cmds.warning(f"Icon not found at path: {icon_path}")
        return
    
    command = "import lampMaterialSetup; lampMaterialSetup.show_ui()"

    try:
        cmds.shelfButton(
            label=button_label,
            annotation=button_tooltip,
            image=icon_path,
            command=command,
            parent=shelf_name,
            imageOverlayLabel=button_label,
            sourceType="python"
        )
        print(f"Button '{button_label}' added to shelf '{shelf_name}'.")
    except Exception as e:
        cmds.warning(f"Failed to add shelf button: {e}")
