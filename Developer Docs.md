### Lamp Material Setup - Developer Docs

## Overview
The **Lamp Material Setup** is a Maya plugin designed to streamline the process of creating and managing materials with texture maps for **Arnold** and **Redshift** renderers. This documentation provides detailed information for developers who wish to understand, maintain, or extend the functionality of this tool.

### Note
The **Redshift** workflow requires specifying names and implementing functionality in accordance with the official documentation for the renderer. Currently, the existing implementation within the **Lamp Material Setup** is in an experimental stage: **rsMaterial** support is for demo purposes only.

## Class Structure

### MaterialCreator (Base Class)
**Purpose:**  
Abstract base class defining the interface for material creation.

**Key Methods:**
- `create_shader()`: Abstract method to be implemented in subclasses.
- `connect_textures(textures, use_substance_style, enable_normal_displacement, normal_map_type=None)`:  
  Connects textures to the appropriate shader inputs.
- `_connect_texture(material, file_node, texture_type, sg, normal_map_type, use_substance_style)`:  
  Abstract method for connecting individual texture nodes.

### ArnoldMaterialCreator (Subclass)
**Purpose:**  
Implements Arnold-specific material creation logic.

**Key Methods:**
- `create_shader()`: Creates an `aiStandardSurface` shader and shading group.
- `_connect_texture()`: Handles Arnold-specific texture connections including:
  - Base Color
  - Roughness
  - Metalness
  - Specular
  - Normal (supports both `aiNormalMap` and `bump2d`)
  - Displacement

### RedshiftMaterialCreator (Subclass)
**Purpose:**  
Implements Redshift-specific material creation logic.

**Key Methods:**
- `create_shader()`: Creates a `RedshiftMaterial` shader and shading group.
- `_connect_texture()`: Handles Redshift-specific texture connections including:
  - Diffuse Color
  - Reflection Roughness
  - Metalness
  - Specular
  - Normal (supports both `RedshiftNormalMap` and `bump2d`)
  - Displacement

### MaterialFactory
**Purpose:**  
Factory class for creating material instances based on the selected renderer.

**Key Method:**
- `create_material(renderer, material_name, normal_map_type=None)`:  
  Returns an instance of the appropriate material creator based on the specified renderer.

### MaterialCreatorUI
**Purpose:**  
Provides the graphical user interface for the material setup tool.

**Key Features:**
1. **Menu Bar:**
   - Edit Menu:
     - Reset Textures
     - Default Settings
   - Help Menu:
     - Documentation link
     - Contact information

2. **Main Interface Components:**
   - Renderer selection (Arnold/Redshift)
   - Object name display
   - Texture fields for:
     - Base Color
     - Metalness
     - Roughness
     - Specular
     - Normal
     - Displacement
   - Checkboxes for:
     - Enable Displacement & Normal
     - Use Substance style

3. **Texture Management:**
   - Automatic texture type detection based on filename keywords
   - Drag-and-drop support for single textures
   - Substance Painter workflow support

4. **Dynamic Updates:**
   - Real-time updates when selection changes
   - Adaptive UI elements based on renderer choice

**Key Methods:**
- `init_ui()`: Initializes the user interface components.
- `update_object_name()`: Updates the displayed object name based on current selection.
- `connect_selection_changed()`: Sets up script job for selection change events.
- `browse_texture(texture_type=None)`: Handles texture file browsing and assignment.
- `match_texture_type(file_name)`: Matches texture filenames to their types using predefined keywords.
- `create_material()`: Main method for creating and assigning materials.

## Implementation Details

### Texture Keywords Mapping
```python
TEXTURE_KEYWORDS = {
    "Base Color": ["basecolor", "albedo", "diffuse"],
    "Roughness": ["roughness", "rough"],
    "Metalness": ["metalness", "metal"],
    "Specular": ["specular"],
    "Normal": ["normal", "nmap"],
    "Displacement": ["displacement", "disp", "height"]
}
```

### Design Patterns Used
1. **Factory Pattern:**  
   Implemented through `MaterialFactory` for creating renderer-specific material instances.

2. **Template Method Pattern:**  
   Used in `connect_textures()` where the base class defines the algorithm structure while allowing subclasses to implement specific steps.

3. **Observer Pattern:**  
   Implemented through Maya's `scriptJob` for monitoring selection changes.

### Error Handling
- Checks for valid selections before material assignment.
- Provides warnings for mismatched texture types.
- Handles missing texture files gracefully.

## Extensibility

### Adding New Renderers
To add support for a new renderer:
1. Create a new subclass of `MaterialCreator`.
2. Implement `create_shader()` and `_connect_texture()` methods.
3. Update `MaterialFactory.create_material()` to handle the new renderer.

### Adding New Texture Types
1. Extend the `TEXTURE_KEYWORDS` dictionary with new mappings.
2. Update `_connect_texture()` methods in all renderer-specific classes.
3. Modify the UI layout to include fields for new texture types.

## Usage Guidelines

### Basic Workflow
1. Select target geometry in Maya.
2. Choose renderer (Arnold/Redshift).
3. Assign textures either manually or via drag-and-drop.
4. Configure options (Substance-style, displacement).
5. Click "Create Material" to generate and assign the material.

### Best Practices
- Organize texture files with consistent naming conventions matching `TEXTURE_KEYWORDS`.
- Use the "Reset Testures" option to clear previous settings when working on new assets.
- Keep texture files in the project's `textures` directory for easier access.

## API Reference

### Public Methods

#### MaterialFactory
- `create_material(renderer, material_name, normal_map_type=None)`: Creates material instance based on renderer.

## Notes
- The script automatically manages Maya's script jobs for selection monitoring.
- Proper cleanup is performed when closing the UI to prevent memory leaks.
- The UI dynamically adapts to different renderer requirements.

## Version Information
- **Version:** 2.1
- **Author:** rabbitGraned
- **License:** Apache 2.0

### Links:

- [GitHub Repository](https://github.com/rabbitGraned/lamp-material-setup.git)
- [Telegram Channel](https://t.me/rabbitGranedAnimation)
- [Author ArtStation](https://artstation.com/rabbitgraned)
