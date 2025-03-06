## Lamp Material Setup - User Guide

## Overview
**Lamp Material Setup** is a plugin for **Autodesk Maya** designed to simplify the creation and management of materials with texture maps for **Arnold** and **Redshift** renderers. This tool automates the process of assigning texture maps and configuring shaders.
### Note
The **Redshift** workflow requires specifying names and implementing functionality in accordance with the official documentation for the renderer. Currently, the existing implementation within the **Lamp Material Setup** is in an experimental stage: **rsMaterial** support is for informational purposes only.

---

## Interface

### Main Interface Elements:

1. Selection:
   - **Renderer:** Choose between **Arnold** and **Redshift**.
   - **Object:** Displays the name of the selected object.

2. **Textures:**
   - Fields for assigning textures:
     - **Base Color**
     - **Metalness**
     - **Roughness**
     - **Specular**
     - **Normal**
     - **Displacement**

3. **Settings:**
   - **Enable Displacement & Normal:** Activates the use of normal and displacement maps.
   - **Use Substance style:** Enables the workflow for textures exported from **Substance Painter**.
   - Creates the material and assigns it to the selected object with **Create Material** button.

---

## Step-by-Step Workflow

### 1. Preparation
- Ensure that textures are stored in the project folder (preferably in the `textures` directory).
- Texture filenames should include keywords corresponding to their types:
  - **Base Color:** `basecolor`, `albedo`, `diffuse`
  - **Roughness:** `roughness`, `rough`
  - **Metalness:** `metalness`, `metal`
  - **Specular:** `specular`
  - **Normal:** `normal`, `nmap`
  - **Displacement:** `displacement`, `disp`, `height`

### 2. Creating a Material
1. Select an object in the scene.
2. Choose a renderer (**Arnold** or **Redshift**) from the dropdown menu.
3. Assign textures using one of the following methods:
   - Click the `...` button next to each texture type and select a file.
   - You have the option of multiple texture selections.
4. Configure the settings:
   - **Use Substance style:** If you are using textures exported from Substance Painter, enable this option. It will automatically:
     - Use the alpha channel for **Roughness** and **Metalness** maps.
     - Set the color space to "Raw" for technical textures.
   - **Enable Displacement & Normal:** Activates the use of normal and displacement maps.
5. Click the **Create Material** button.

---

## Key Features
### Working with Substance Painter
If you are using textures exported from Substance Painter:
- Enable the **Use Substance style** option.
- The script will automatically:
  - Use the alpha channel for Roughness and Metalness maps.
  - Set the color space to "Raw" for technical textures (Roughness, Metalness, Specular, Normal).

### Normal Maps
- For **Arnold**:
  - You can choose between `aiNormalMap` and `bump2d`.
  - When using Substance-style, the normal map will automatically invert the Y-axis.
- For **Redshift**:
  - Uses `RedshiftNormalMap` when Substance-style is enabled.
  - Otherwise, uses `bump2d`.

### Displacement
- To use displacement maps:
  - Enable the **Enable Displacement & Normal** option.
  - Assign a displacement map.

---

## Best Practices

1. **File Organization:**
   - Store textures in the `textures` directory within your project.
   - Use clear filenames that include relevant keywords (e.g., `BaseColor`, `Roughness`).

2. **Clearing Fields:**
   - Use **Reset Textures** to clear all fields before creating a new material.

3. **Checking Warnings:**
   - If a texture is assigned to the wrong slot (e.g., Roughness instead of Base Color), the script will issue a warning.  

---

## Links:

- [GitHub Repository](https://github.com/rabbitGraned/lamp-material-setup.git)
- [Telegram Channel](https://t.me/rabbitGranedAnimation)
- [Author ArtStation](https://artstation.com/rabbitgraned)
