"""
UI Module - Appends Control nodes, layouts, and anchors to TscnBuilder
"""

from typing import Optional, Tuple
from ..core import TscnBuilder, TscnNode


class UIModule:
    """UI component generator that operates on a TscnBuilder instance"""
    
    def __init__(self, builder: TscnBuilder):
        """Initialize UI module
        
        Args:
            builder: TscnBuilder instance to operate on
        """
        self.builder = builder
    
    def setup_fullscreen_control(self, **properties) -> TscnNode:
        """Initialize root as fullscreen Control node"""
        return self.builder.initialize_root(
            layout_mode=3,
            anchors_preset=15,
            anchor_right=1.0,
            anchor_bottom=1.0,
            grow_horizontal=2,
            grow_vertical=2,
            **properties
        )
    
    def add_margin_container(self, name: str, parent: str = ".", 
                            uniform: Optional[int] = None,
                            left: Optional[int] = None, top: Optional[int] = None,
                            right: Optional[int] = None, bottom: Optional[int] = None,
                            script: Optional[str] = "res://addons/A1MyAddon/Helpers/MarginContainerHelper.cs",
                            use_anchors: bool = False,
                            vertical_margin: Optional[int] = None,
                            horizontal_margin: Optional[int] = None) -> TscnNode:
        """Add MarginContainer with optional MarginContainerHelper script"""
        properties = {
            "layout_mode": 1 if use_anchors else 2
        }
        
        if uniform is not None:
            properties["theme_override_constants/margin_left"] = uniform
            properties["theme_override_constants/margin_top"] = uniform
            properties["theme_override_constants/margin_right"] = uniform
            properties["theme_override_constants/margin_bottom"] = uniform
        else:
            if left is not None:
                properties["theme_override_constants/margin_left"] = left
            if top is not None:
                properties["theme_override_constants/margin_top"] = top
            if right is not None:
                properties["theme_override_constants/margin_right"] = right
            if bottom is not None:
                properties["theme_override_constants/margin_bottom"] = bottom
        
        if script is not None:
            res_id = self.builder.add_ext_resource("Script", script, "uid://bk83ics8idr7w")
            properties["script"] = f'ExtResource("{res_id}")'
            if uniform is not None:
                properties["UniformMargin"] = uniform
            if vertical_margin is not None:
                properties["VerticalMargin"] = vertical_margin
            if horizontal_margin is not None:
                properties["HorizontalMargin"] = horizontal_margin
        
        return self.builder.add_node(name, "MarginContainer", parent, **properties)
    
    def add_panel_container(self, name: str, parent: str = ".") -> TscnNode:
        """Add PanelContainer"""
        return self.builder.add_node(name, "PanelContainer", parent, layout_mode=2)
    
    def add_scroll_container(self, name: str, parent: str = ".",
                            horizontal_scroll: int = 0, 
                            vertical_scroll: int = 2, 
                            follow_focus: bool = True) -> TscnNode:
        """Add ScrollContainer"""
        properties = {
            "layout_mode": 2,
            "horizontal_scroll_mode": horizontal_scroll,
            "vertical_scroll_mode": vertical_scroll
        }
        if follow_focus:
            properties["follow_focus"] = "true"
        
        return self.builder.add_node(name, "ScrollContainer", parent, **properties)
    
    def add_vbox(self, name: str, parent: str = ".", separation: Optional[int] = None) -> TscnNode:
        """Add VBoxContainer"""
        properties = {"layout_mode": 2}
        if separation is not None:
            properties["theme_override_constants/separation"] = separation
        
        return self.builder.add_node(name, "VBoxContainer", parent, **properties)
    
    def add_hbox(self, name: str, parent: str = ".", separation: Optional[int] = None) -> TscnNode:
        """Add HBoxContainer"""
        properties = {"layout_mode": 2}
        if separation is not None:
            properties["theme_override_constants/separation"] = separation
        
        return self.builder.add_node(name, "HBoxContainer", parent, **properties)
    
    def add_color_rect(self, name: str, parent: str = ".",
                      color: Tuple[float, float, float, float] = (0.15, 0.15, 0.15, 1),
                      use_anchors: bool = False) -> TscnNode:
        """Add ColorRect"""
        properties = {}
        
        if use_anchors:
            properties.update({
                "layout_mode": 1,
                "anchors_preset": 15,
                "anchor_right": 1.0,
                "anchor_bottom": 1.0,
                "grow_horizontal": 2,
                "grow_vertical": 2
            })
        else:
            properties["layout_mode"] = 0
        
        properties["color"] = f"Color({color[0]}, {color[1]}, {color[2]}, {color[3]})"
        
        return self.builder.add_node(name, "ColorRect", parent, **properties)
    
    def add_label(self, name: str, parent: str = ".", text: str = "", 
                 align: str = "left", font_size: Optional[int] = None,
                 min_size: Optional[Tuple[float, float]] = None,
                 size_flags_h: Optional[int] = None) -> TscnNode:
        """Add Label"""
        properties = {"layout_mode": 2}
        
        if text:
            properties["text"] = f'"{text}"'
        
        align_map = {"left": 0, "center": 1, "right": 2}
        if align in align_map:
            properties["horizontal_alignment"] = align_map[align]
        
        if font_size:
            properties["theme_override_font_sizes/font_size"] = font_size
        
        if min_size:
            properties["custom_minimum_size"] = f"Vector2({min_size[0]}, {min_size[1]})"
        
        if size_flags_h is not None:
            properties["size_flags_horizontal"] = size_flags_h
        
        return self.builder.add_node(name, "Label", parent, **properties)
    
    def add_progress_bar(self, name: str, parent: str = ".", value: float = 0,
                        size_flags_h: Optional[int] = None,
                        size_flags_v: Optional[int] = None,
                        size_flags_stretch_ratio: Optional[float] = None,
                        min_size: Optional[Tuple[float, float]] = None,
                        show_percentage: bool = True) -> TscnNode:
        """Add ProgressBar"""
        properties = {
            "layout_mode": 2,
            "value": value
        }
        
        if size_flags_h is not None:
            properties["size_flags_horizontal"] = size_flags_h
        
        if size_flags_v is not None:
            properties["size_flags_vertical"] = size_flags_v
        
        if size_flags_stretch_ratio is not None:
            properties["size_flags_stretch_ratio"] = size_flags_stretch_ratio
        
        if min_size:
            properties["custom_minimum_size"] = f"Vector2({min_size[0]}, {min_size[1]})"
        
        if show_percentage:
            properties["show_percentage"] = "true"
        
        return self.builder.add_node(name, "ProgressBar", parent, **properties)
    
    def add_button(self, name: str, parent: str = ".", text: str = "",
                  size_flags_h: Optional[int] = None) -> TscnNode:
        """Add Button"""
        properties = {"layout_mode": 2}
        
        if text:
            properties["text"] = f'"{text}"'
        
        if size_flags_h is not None:
            properties["size_flags_horizontal"] = size_flags_h
        
        return self.builder.add_node(name, "Button", parent, **properties)
    
    def add_checkbox(self, name: str, parent: str = ".", text: str = "",
                    size_flags_h: Optional[int] = None,
                    button_pressed: bool = False) -> TscnNode:
        """Add CheckBox"""
        properties = {"layout_mode": 2}
        
        if text:
            properties["text"] = f'"{text}"'
        
        if size_flags_h is not None:
            properties["size_flags_horizontal"] = size_flags_h
        
        if button_pressed:
            properties["button_pressed"] = "true"
        
        return self.builder.add_node(name, "CheckBox", parent, **properties)
    
    def add_texture_rect(self, name: str, parent: str = ".",
                        texture_path: Optional[str] = None,
                        texture_uid: Optional[str] = None,
                        expand_mode: int = 0,
                        stretch_mode: int = 0) -> TscnNode:
        """Add TextureRect"""
        properties = {"layout_mode": 2}
        
        if texture_path and texture_uid:
            res_id = self.builder.add_ext_resource("Texture2D", texture_path, texture_uid)
            properties["texture"] = f'ExtResource("{res_id}")'
        
        properties["expand_mode"] = expand_mode
        properties["stretch_mode"] = stretch_mode
        
        return self.builder.add_node(name, "TextureRect", parent, **properties)
    
    def add_instance(self, name: str, parent: str = ".",
                    scene_path: str = "", scene_uid: str = "") -> TscnNode:
        """Add scene instance (prefab)
        
        Args:
            scene_uid: REQUIRED - use mcp_godot_get_uid to obtain correct UID
        """
        if not scene_uid:
            raise ValueError(f"scene_uid is REQUIRED. Use mcp_godot_get_uid for {scene_path}")
        
        res_id = self.builder.add_ext_resource("PackedScene", scene_path, scene_uid)
        
        properties = {
            "_is_instance": True,
            "_scene_path": scene_path
        }
        
        node = self.builder.add_node(name, "INSTANCE", parent, **properties)
        return node
    
    def add_separator(self, name: str, parent: str = ".",
                     separation: Optional[int] = None,
                     style_path: Optional[str] = None,
                     style_uid: Optional[str] = None) -> TscnNode:
        """Add HSeparator"""
        properties = {"layout_mode": 2}
        
        if separation is not None:
            properties["theme_override_constants/separation"] = separation
        
        if style_path and style_uid:
            res_id = self.builder.add_ext_resource("StyleBox", style_path, style_uid)
            properties["theme_override_styles/separator"] = f'ExtResource("{res_id}")'
        
        return self.builder.add_node(name, "HSeparator", parent, **properties)
