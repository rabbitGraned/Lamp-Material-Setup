### Lamp Material Setup
---

<img width="1920" height="1040" alt="LMS5GIT" src="https://github.com/user-attachments/assets/6fd0e622-898e-4eca-8516-3246fa1cb245" />

This version of the plugin is supported in Maya 2024.

![Version](https://img.shields.io/badge/Latest_Development_Release-none-green)\
![Version](https://img.shields.io/badge/Latest_Stable_Release-2.4.2-blue)

This `legacy` branch of the project contains the latest stable version of **Lamp Material Setup** for **Maya 2024** and below (until 2020), which is not supported in versions **Maya 2025** and above.

For the **Maya 2025** version, use the `release` branch.

# About
**Lamp Material Setup** is a plugin for **Autodesk Maya**™ designed to simplify the creation and management of materials with texture maps for **Arnold**™ and **Redshift**™ renderers. This tool automates the process of assigning texture maps and configuring shaders.

## Key Features
A special mode `Use Substance style` allows you to quickly assign the correct color space, node parameters, and invert normal maps.

# Get-Started

Just clone the repository:

`git clone https://github.com/rabbitGraned/Lamp-Material-Setup`

or download ZIP.
#### Plug-in
To install the tool as a Maya script, download the archive directly from GitHub or clone the repository to the `C:\Users\[Username]\Documents\maya\[version]\scripts` folder.

In the Maya menu, go to `Window > Settings/Preferences > Plug-in Manager`.
Find the **lampMaterialSetup_Plugin.py** plugin and load it. If the plugin is not loaded automatically, select it using the `Plug-in Manager > Browse > path/lampMSPlugin.py`.

#### Script

You can simply run the `lampMaterialSetup` script in Maya, add to the shelf and replace with the plugin icon if desired. This will simplify debugging and installation.

# For Developers

Clone the repository and open the `lampMaterialSetup.py` file in your text code editor.

# Contribution

Detailed documentation on editing the script is available in the [`Developer Docs`](Developer%20Docs.md) file.

**Note**: Keep API stable - don't change key function names and signatures, split logic into independent components.

Also check the project Wiki-page.

# License

Lamp Material Setup is licensed under the [Apache 2.0](LICENSE).

## Links:

- [GitHub Repository](https://github.com/rabbitGraned/lamp-material-setup.git)
- [Telegram Channel](https://t.me/rabbitGranedAnimation)
- [Author ArtStation](https://artstation.com/rabbitgraned)
