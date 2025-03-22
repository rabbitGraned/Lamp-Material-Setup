"""
Lamp Material Setup
Desctiption:
An approved version of the script, implemented as a plug-in for Maya.
Version:    2.2
Author:     rabbitGraned
License:    Apache 2.0
"""
from PySide2 import QtWidgets, QtCore, QtGui
import maya.cmds as cmds
from pathlib import Path
from functools import partial
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui

VERSION = "2.2"

class MaterialCreator:
    def __init__(self, material_name):
        self.material_name = material_name

    def create_shader(self):
        raise NotImplementedError("Method must be implemented in subclass")

    def connect_textures(self, textures, use_substance_style, enable_normal_displacement, normal_map_type=None):
        material, sg = self.create_shader()
        for texture_type, file_path in textures.items():
            if not file_path or (texture_type in ["Normal", "Displacement"] and not enable_normal_displacement):
                continue
            file_node = cmds.shadingNode("file", asTexture=True, name=f"{self.material_name}_{texture_type}")
            cmds.setAttr(f"{file_node}.fileTextureName", file_path, type="string")
            if use_substance_style:
                if texture_type in ["Roughness", "Metalness"]:
                    cmds.setAttr(f"{file_node}.alphaIsLuminance", True)
                if texture_type in ["Roughness", "Metalness", "Specular", "Normal"]:
                    cmds.setAttr(f"{file_node}.colorSpace", "Raw", type="string")
            self._connect_texture(material, file_node, texture_type, sg, normal_map_type, use_substance_style)
        return material, sg

    def _connect_texture(self, material, file_node, texture_type, sg, normal_map_type=None, use_substance_style=False):
        raise NotImplementedError("Method must be implemented in subclass")

    def connect_displacement(self, file_node, sg):
        disp_shader = cmds.shadingNode("displacementShader", asUtility=True, name=f"{self.material_name}_dispShader")
        cmds.connectAttr(f"{file_node}.outAlpha", f"{disp_shader}.displacement")
        cmds.connectAttr(f"{disp_shader}.displacement", f"{sg}.displacementShader")

class ArnoldMaterialCreator(MaterialCreator):
    def __init__(self, material_name, normal_map_type):
        super().__init__(material_name)
        self.normal_map_type = normal_map_type

    def create_shader(self):
        material = cmds.shadingNode("aiStandardSurface", asShader=True, name=self.material_name)
        sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f"{self.material_name}SG")
        cmds.connectAttr(f"{material}.outColor", f"{sg}.surfaceShader")
        return material, sg

    def _connect_texture(self, material, file_node, texture_type, sg, normal_map_type, use_substance_style):
        if texture_type == "Base Color":
            cmds.connectAttr(f"{file_node}.outColor", f"{material}.baseColor")
        elif texture_type == "Roughness":
            cmds.connectAttr(f"{file_node}.outAlpha", f"{material}.specularRoughness")
        elif texture_type == "Metalness":
            cmds.connectAttr(f"{file_node}.outAlpha", f"{material}.metalness")
        elif texture_type == "Specular":
            cmds.connectAttr(f"{file_node}.outColor", f"{material}.specularColor")
        elif texture_type == "Normal":
            if self.normal_map_type == "aiNormalMap":
                normal_node = cmds.shadingNode("aiNormalMap", asUtility=True, name=f"{self.material_name}_aiNormalMap")
                cmds.connectAttr(f"{file_node}.outColor", f"{normal_node}.input")
                cmds.connectAttr(f"{normal_node}.outValue", f"{material}.normalCamera")
                if use_substance_style:
                    cmds.setAttr(f"{normal_node}.invertY", True)
            else:
                bump_node = cmds.shadingNode("bump2d", asUtility=True, name=f"{self.material_name}_bump2d")
                cmds.setAttr(f"{bump_node}.bumpInterp", 0)
                cmds.connectAttr(f"{file_node}.outAlpha", f"{bump_node}.bumpValue")
                cmds.connectAttr(f"{bump_node}.outNormal", f"{material}.normalCamera")
                if use_substance_style:
                    cmds.setAttr(f"{bump_node}.flipY", True)
        elif texture_type == "Displacement":
            self.connect_displacement(file_node, sg)

class RedshiftMaterialCreator(MaterialCreator):
    def create_shader(self):
        material = cmds.shadingNode("RedshiftMaterial", asShader=True, name=self.material_name)
        sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f"{self.material_name}SG")
        cmds.connectAttr(f"{material}.outColor", f"{sg}.surfaceShader")
        return material, sg

    def _connect_texture(self, material, file_node, texture_type, sg, normal_map_type, use_substance_style):
        if texture_type == "Base Color":
            cmds.connectAttr(f"{file_node}.outColor", f"{material}.diffuse_color")
        elif texture_type == "Roughness":
            cmds.connectAttr(f"{file_node}.outAlpha", f"{material}.refl_roughness")
        elif texture_type == "Metalness":
            cmds.setAttr(f"{material}.refl_fresnel_mode", 2)
            cmds.connectAttr(f"{file_node}.outAlpha", f"{material}.refl_metalness")
        elif texture_type == "Specular":
            cmds.connectAttr(f"{file_node}.outColor", f"{material}.refl_color")
        elif texture_type == "Normal":
            if use_substance_style:
                normal_node = cmds.shadingNode("RedshiftNormalMap", asUtility=True, name=f"{self.material_name}_rsNormalMap")
                cmds.setAttr(f"{normal_node}.flipY", True)
                cmds.connectAttr(f"{file_node}.outColor", f"{normal_node}.input")
                cmds.connectAttr(f"{normal_node}.out", f"{material}.bump_input")
            else:
                bump_node = cmds.shadingNode("bump2d", asUtility=True, name=f"{self.material_name}_bump2d")
                cmds.setAttr(f"{bump_node}.bumpInterp", 0)
                cmds.connectAttr(f"{file_node}.outAlpha", f"{bump_node}.bumpValue")
                cmds.connectAttr(f"{bump_node}.outNormal", f"{material}.bump_input")
            cmds.setAttr(f"{material}.enableBumpMap", True)
        elif texture_type == "Displacement":
            disp_node = cmds.shadingNode("RedshiftDisplacement", asUtility=True, name=f"{self.material_name}_rsDisplacement")
            cmds.connectAttr(f"{file_node}.outAlpha", f"{disp_node}.texMap")
            cmds.connectAttr(f"{disp_node}.out", f"{sg}.displacementShader")

class MaterialFactory:
    @staticmethod
    def create_material(renderer, material_name, normal_map_type=None):
        if renderer == "Arnold":
            return ArnoldMaterialCreator(material_name, normal_map_type)
        elif renderer == "Redshift":
            return RedshiftMaterialCreator(material_name)
        else:
            raise ValueError(f"Renderer {renderer} is not supported.")

class MaterialCreatorUI(QtWidgets.QDialog):
    TEXTURE_KEYWORDS = {
        "Base Color": ["basecolor", "albedo", "diffuse"],
        "Roughness": ["roughness", "rough"],
        "Metalness": ["metalness", "metal"],
        "Specular": ["specular"],
        "Normal": ["normal", "nmap"],
        "Displacement": ["displacement", "disp", "height"]
    }

    def __init__(self, parent=None):
        super(MaterialCreatorUI, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle("Lamp Material Setup")
        self.resize(400, 600)
        self.textures = {key: None for key in self.TEXTURE_KEYWORDS.keys()}
        self.use_substance_style = True
        self.enable_normal_displacement = False
        self.renderer = "Arnold"
        self.project_dir = Path(cmds.workspace(q=True, rd=True))
        self.texture_dir = self.project_dir / "textures"
        self.last_texture_dir = None
        self.init_ui()
        self.update_object_name()
        self.connect_selection_changed()

    def init_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        menu_bar = QtWidgets.QMenuBar()
        edit_menu = menu_bar.addMenu("Edit")
        reset_action = QtWidgets.QAction("Reset Textures", self)
        reset_action.triggered.connect(self.reset_fields)
        edit_menu.addAction(reset_action)
        default_action = QtWidgets.QAction("Default Settings", self)
        default_action.triggered.connect(self.default_settings)
        edit_menu.addAction(default_action)
        help_menu = menu_bar.addMenu("Help")
        about_action = QtWidgets.QAction("Docs", self)
        about_action.triggered.connect(lambda: __import__('webbrowser').open("https://github.com/rabbitGraned/Lamp-Material-Setup/wiki"))
        help_menu.addAction(about_action)
        about_action = QtWidgets.QAction("About", self)
        about_action.triggered.connect(lambda: __import__('webbrowser').open("https://github.com/rabbitGraned/Lamp-Material-Setup"))
        help_menu.addAction(about_action)
        help_menu.addSeparator()
        version_action = QtWidgets.QAction(f"Version {VERSION}", self)
        version_action.setEnabled(False)
        help_menu.addAction(version_action)
        main_layout.addWidget(menu_bar)
        renderer_layout = QtWidgets.QHBoxLayout()
        renderer_label = QtWidgets.QLabel("Renderer:")
        self.renderer_combo = QtWidgets.QComboBox()
        self.renderer_combo.addItems(["Arnold", "Redshift"])
        self.renderer_combo.setMaximumWidth(150)
        self.renderer_combo.currentTextChanged.connect(self.update_renderer_and_material_info)
        renderer_layout.addWidget(renderer_label)
        renderer_layout.addWidget(self.renderer_combo)
        renderer_layout.addStretch()
        main_layout.addLayout(renderer_layout)
        self.material_info_label = QtWidgets.QLabel("Material: aiStandardSurface")
        main_layout.addWidget(self.material_info_label)
        object_layout = QtWidgets.QHBoxLayout()
        object_label = QtWidgets.QLabel("Object:") 
        object_label.setFixedWidth(100)
        self.object_name_field = QtWidgets.QLineEdit()
        self.object_name_field.setReadOnly(True)
        self.object_name_field.setMinimumWidth(250)
        object_layout.addWidget(object_label)
        object_layout.addSpacing(10)
        object_layout.addWidget(self.object_name_field)
        object_layout.addStretch()
        main_layout.addLayout(object_layout)
        textures_group = QtWidgets.QGroupBox("Textures")
        textures_layout = QtWidgets.QVBoxLayout()
        self.texture_widgets = {}
        for texture_type in ["Base Color", "Metalness", "Roughness", "Specular"]:
            texture_layout = QtWidgets.QHBoxLayout()
            texture_label = QtWidgets.QLabel(f"{texture_type}:")
            texture_label.setFixedWidth(100)
            texture_field = QtWidgets.QLineEdit()
            texture_field.setMinimumWidth(250) 
            browse_button = QtWidgets.QToolButton()
            browse_button.setIcon(QtGui.QIcon(":browseFolder.png"))
            browse_button.setIconSize(QtCore.QSize(32, 32))
            browse_button.setFixedSize(32, 32)
            browse_button.setStyleSheet("border: none; background-color: transparent;")
            browse_button.clicked.connect(partial(self.browse_texture, texture_type))
            texture_layout.addWidget(texture_label)
            texture_layout.addWidget(texture_field)
            texture_layout.addWidget(browse_button)
            texture_layout.setSpacing(2)    # SP
            textures_layout.addLayout(texture_layout)
            self.texture_widgets[texture_type] = texture_field
            texture_field.textChanged.connect(partial(self.update_texture_dict, texture_type))
        textures_group.setLayout(textures_layout)
        main_layout.addWidget(textures_group)
        self.normal_displacement_group = QtWidgets.QGroupBox("Displacement and Normal")
        self.normal_displacement_layout = QtWidgets.QVBoxLayout()
        normal_layout = QtWidgets.QHBoxLayout()
        normal_label = QtWidgets.QLabel("Normal:")
        normal_label.setFixedWidth(100)
        self.normal_combo = QtWidgets.QComboBox()
        self.normal_combo.addItems(["aiNormalMap", "bump2d"])
        self.normal_combo.setMaximumWidth(100)
        normal_layout.addWidget(normal_label)
        normal_layout.addWidget(self.normal_combo)
        normal_layout.addStretch()
        self.normal_displacement_layout.addLayout(normal_layout)
        normal_field_layout = QtWidgets.QHBoxLayout()
        normal_field_label = QtWidgets.QLabel("")
        normal_field_label.setFixedWidth(100)
        self.normal_field = QtWidgets.QLineEdit()
        normal_browse = QtWidgets.QToolButton()
        normal_browse.setIcon(QtGui.QIcon(":browseFolder.png"))
        normal_browse.setIconSize(QtCore.QSize(32, 32))
        normal_browse.setFixedSize(32, 32)
        normal_browse.setStyleSheet("border: none; background-color: transparent;")
        normal_browse.clicked.connect(partial(self.browse_texture, "Normal"))
        normal_field_layout.addWidget(normal_field_label)
        normal_field_layout.addWidget(self.normal_field)
        normal_field_layout.addWidget(normal_browse)
        normal_field_layout.setSpacing(2)
        self.normal_displacement_layout.addLayout(normal_field_layout)
        self.texture_widgets["Normal"] = self.normal_field
        self.normal_field.textChanged.connect(partial(self.update_texture_dict, "Normal"))
        displacement_layout = QtWidgets.QHBoxLayout()
        displacement_label = QtWidgets.QLabel("Displacement:")
        displacement_label.setFixedWidth(100)
        self.displacement_field = QtWidgets.QLineEdit()
        displacement_browse = QtWidgets.QToolButton()
        displacement_browse.setIcon(QtGui.QIcon(":browseFolder.png"))
        displacement_browse.setIconSize(QtCore.QSize(32, 32))
        displacement_browse.setFixedSize(32, 32)
        displacement_browse.setStyleSheet("border: none; background-color: transparent;")
        displacement_browse.clicked.connect(partial(self.browse_texture, "Displacement"))
        displacement_layout.addWidget(displacement_label)
        displacement_layout.addWidget(self.displacement_field)
        displacement_layout.addWidget(displacement_browse)
        displacement_layout.setSpacing(2)
        self.normal_displacement_layout.addLayout(displacement_layout)
        self.texture_widgets["Displacement"] = self.displacement_field
        self.displacement_field.textChanged.connect(partial(self.update_texture_dict, "Displacement"))
        self.normal_displacement_group.setLayout(self.normal_displacement_layout)
        self.normal_displacement_group.setEnabled(False)
        main_layout.addWidget(self.normal_displacement_group)
        checkboxes_layout = QtWidgets.QHBoxLayout()
        self.enable_normal_disp_checkbox = QtWidgets.QCheckBox("Enable Displacement && Normal")
        self.enable_normal_disp_checkbox.setChecked(False)
        self.enable_normal_disp_checkbox.stateChanged.connect(self.toggle_normal_displacement_block)
        self.substance_checkbox = QtWidgets.QCheckBox("Use Substance style")
        self.substance_checkbox.setChecked(True)
        self.substance_checkbox.stateChanged.connect(self.toggle_substance_style)
        self.substance_checkbox.setToolTip(
            "Substance Painter Workflow:\n"
            "- Enables the use of Substance-style texture mapping.\n"
            "- Roughness and Metalness use Alpha Channels.\n"
            "- Color Spaces are set to 'Raw' for relevant maps.")
        checkboxes_layout.addWidget(self.enable_normal_disp_checkbox)
        checkboxes_layout.addWidget(self.substance_checkbox)
        main_layout.addLayout(checkboxes_layout)
        main_layout.addStretch()
        create_button = QtWidgets.QPushButton("Create Material")
        create_button.clicked.connect(self.create_material)
        main_layout.addWidget(create_button)

    def update_object_name(self):
        selection = cmds.ls(selection=True)
        object_name = selection[0] if selection else "None"
        self.object_name_field.setText(object_name)

    def connect_selection_changed(self):
        script_job_id = cmds.scriptJob(event=["SelectionChanged", self.update_object_name])
        self.script_job_id = script_job_id

    def closeEvent(self, event):
        if hasattr(self, "script_job_id"):
            cmds.scriptJob(kill=self.script_job_id, force=True)
        super(MaterialCreatorUI, self).closeEvent(event)

    def update_renderer_and_material_info(self, renderer):
        self.renderer = renderer
        material_type = "aiStandardSurface" if renderer == "Arnold" else "rsMaterial (Experimental)"
        self.material_info_label.setText(f"Material: {material_type}")
        if renderer == "Redshift":
            self.normal_combo.setCurrentText("bump2d")
            self.normal_combo.setEnabled(False)
        else:
            self.normal_combo.setEnabled(True)

    def toggle_substance_style(self, state):
        self.use_substance_style = bool(state)

    def toggle_normal_displacement_block(self, state):
        self.enable_normal_displacement = bool(state)
        self.normal_displacement_group.setEnabled(state)

    def update_texture_dict(self, texture_type, new_text):
        self.textures[texture_type] = new_text.strip() or None

    def reset_fields(self):
        for texture_type, field in self.texture_widgets.items():
            field.clear()
            self.textures[texture_type] = None

    def default_settings(self):
        self.renderer_combo.setCurrentText("Arnold")
        self.substance_checkbox.setChecked(True)
        self.enable_normal_disp_checkbox.setChecked(False)
        self.reset_fields()

    def browse_texture(self, texture_type=None):
        start_dir = self.last_texture_dir if self.last_texture_dir else (self.texture_dir if self.texture_dir.exists() else self.project_dir)
        file_paths, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self, "Select Texture(s)", str(start_dir), "Image Files (*.jpg *.png *.exr *.hdr)"
        )
        if not file_paths:
            return
        if len(file_paths) == 1 and texture_type:
            file_path = file_paths[0]
            self.texture_widgets[texture_type].setText(file_path)
            self.textures[texture_type] = file_path
            self.last_texture_dir = Path(file_path).parent
            matched_type = self.match_texture_type(Path(file_path).name.lower())
            if matched_type and matched_type != texture_type:
                cmds.warning(f"Selected texture '{file_path}' seems to be a {matched_type} map, but assigned to {texture_type}.")
        else:
            for file_path in file_paths:
                base_name = Path(file_path).name.lower()
                matched_type = self.match_texture_type(base_name)
                if matched_type:
                    if not self.enable_normal_displacement and matched_type in ["Normal", "Displacement"]:
                        continue
                    self.texture_widgets[matched_type].setText(file_path)
                    self.textures[matched_type] = file_path
                    self.last_texture_dir = Path(file_path).parent

    def match_texture_type(self, file_name):
        for texture_type, keywords in self.TEXTURE_KEYWORDS.items():
            if any(keyword in file_name for keyword in keywords):
                return texture_type
        return None

    def create_material(self):
        selection = cmds.ls(selection=True)
        material_name = f"{selection[0]}M" if selection else "newMaterial"
        filtered_textures = {
            k: v for k, v in self.textures.items()
            if self.enable_normal_displacement or k not in ["Normal", "Displacement"]
        }
        normal_map_type = self.normal_combo.currentText() if self.renderer == "Arnold" else None
        creator = MaterialFactory.create_material(self.renderer, material_name, normal_map_type)
        material, sg = creator.connect_textures(filtered_textures, self.use_substance_style, self.enable_normal_displacement, normal_map_type)
        if selection:
            try:
                cmds.sets(selection, edit=True, forceElement=sg)
            except Exception as e:
                cmds.warning(f"Failed to assign material to selected objects: {e}")
        else:
            cmds.warning("No geometry selected. Material created but not assigned.")

def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QMainWindow)

def show_ui():
    try:
        global material_creator_ui
        if material_creator_ui and material_creator_ui.isVisible():
            material_creator_ui.close()
            material_creator_ui.deleteLater()
    except NameError:
        pass
    parent = get_maya_main_window()
    material_creator_ui = MaterialCreatorUI(parent)
    material_creator_ui.show()

show_ui()
