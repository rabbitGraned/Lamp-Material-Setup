### Lamp Material Setup
---

 ![screenshot_01](https://github.com/user-attachments/assets/dfdae246-828c-46b7-ad4e-d90b268d2b3f)

This version of the plugin is supported in **Autodesk Maya**™ 2024 and higher.

![Version](https://img.shields.io/badge/Latest_Stable_Release-2.1.0-blue)

# About
**Lamp Material Setup** is a plugin for **Autodesk Maya**™ designed to simplify the creation and management of materials with texture maps for **Arnold**™ and **Redshift**™ renderers. This tool automates the process of assigning texture maps and configuring shaders.

## Key Features
A special mode `Use Substance style` allows you to quickly assign the correct color space, node parameters, and invert normal maps.

# Build

Just clone the repository:

`git clone https://github.com/rabbitGraned/Lamp-Material-Setup`

And open the `lampMaterialSetup.py` file in your text code editor.
#### Plug-in
To install the tool as a Maya script, download the archive directly from GitHub or clone the repository to the `C:\Users\[Username]\Documents\maya\modules` folder.

In the Maya menu, go to `Window > Settings/Preferences > Plug-in Manager`.
Find the **lampMSPlugin.py** plugin and load it. If the plugin is not loaded automatically, select it using the `Plug-in Manager > Browse > path/lampMSPlugin.py`.

#### Script

You can simply run the `lampMaterialSetup` script in Maya, add to the shelf and replace with the plugin icon if desired. This will simplify debugging and installation.

# Contribution

Detailed documentation on editing the script is available in the [`Developer Docs`](Developer%20Docs.md) file.

**Note**: Keep API stable - don't change key function names and signatures, split logic into independent components.

Also check the project Wiki-page.

# License

Lamp Material Setup is licensed under the  [Apache 2.0](LICENSE). 
Copyright (C) 2025 rabbitGraned

## Links:

- [GitHub Repository](https://github.com/rabbitGraned/lamp-material-setup.git)
- [Telegram Channel](https://t.me/rabbitGranedAnimation)
- [Author ArtStation](https://artstation.com/rabbitgraned)
