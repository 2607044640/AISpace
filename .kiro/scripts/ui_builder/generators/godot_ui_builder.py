"""
Godot UI Builder - 程序化生成Godot UI的Python工具
让AI能够方便地操作Godot UI，而不是直接面对冗长的.tscn文本
"""

import random
from typing import Optional, Tuple, List, Dict, Any


class UINode:
    """表示一个UI节点"""
    
    def __init__(self, name: str, node_type: str, unique_id: Optional[int] = None, auto_suffix: bool = True):
        # 自动添加节点类型后缀（如果启用且名称中没有后缀）
        if auto_suffix and not name.endswith(f"_{node_type}"):
            self.name = f"{name}_{node_type}"
        else:
            self.name = name
        self.node_type = node_type
        self.unique_id = unique_id or random.randint(1, 2**31 - 1)
        self.parent_path = "."
        self.properties: Dict[str, Any] = {}
        self.children: List['UINode'] = []
        self.parent: Optional['UINode'] = None
    
    def get_path_from_root(self) -> List['UINode']:
        """获取从根节点到当前节点的完整节点路径列表"""
        path = []
        current = self
        while current is not None:
            path.append(current)
            current = current.parent
        return path[::-1]  # 反转列表，变成 [Root, Child, GrandChild, Self]
    
    def get_relative_path_to(self, target: 'UINode') -> str:
        """核心防幻觉功能：自动计算从当前节点到目标节点的精确相对 NodePath。
        
        例如自动算出：../../Air/FlyMode
        
        Args:
            target: 目标节点
            
        Returns:
            相对路径字符串，如 "../../Air/FlyMode" 或 "." (同一节点)
            
        Raises:
            ValueError: 如果两个节点不在同一个树中
        """
        my_path = self.get_path_from_root()
        target_path = target.get_path_from_root()
        
        # 1. 寻找最近公共祖先 (LCA)
        lca_index = -1
        for i in range(min(len(my_path), len(target_path))):
            if my_path[i] == target_path[i]:
                lca_index = i
            else:
                break
        
        if lca_index == -1:
            raise ValueError(f"节点 {self.name} 和 {target.name} 不在同一个树中！")
        
        # 2. 计算需要向上返回多少层 (即生成多少个 "..")
        # my_path 长度减去 1 (自己)，再减去 LCA 的索引
        steps_up = len(my_path) - 1 - lca_index
        
        # 3. 计算从 LCA 向下的路径
        down_path = [node.name for node in target_path[lca_index + 1:]]
        
        # 4. 拼接路径
        if steps_up == 0 and not down_path:
            return "."  # 是同一个节点
        
        parts = [".."] * steps_up + down_path
        return "/".join(parts)
    
    def _add_child(self, child: 'UINode') -> 'UINode':
        """内部方法：添加子节点"""
        child.parent = self
        self.children.append(child)
        # 计算parent_path
        if self.parent is None:
            # 根节点的子节点
            child.parent_path = "."
        else:
            # 非根节点的子节点
            if self.parent_path == ".":
                child.parent_path = self.name
            else:
                child.parent_path = f"{self.parent_path}/{self.name}"
        return child
    
    def set_property(self, key: str, value: Any) -> 'UINode':
        """设置属性（链式调用）"""
        self.properties[key] = value
        return self
    
    # === 通用容器方法 ===
    
    def add_margin_container(self, name: str, uniform: Optional[int] = None,
                            left: Optional[int] = None, top: Optional[int] = None,
                            right: Optional[int] = None, bottom: Optional[int] = None,
                            script: Optional[str] = "res://addons/A1MyAddon/Helpers/MarginContainerHelper.cs",
                            use_anchors: bool = False,
                            vertical_margin: Optional[int] = None,
                            horizontal_margin: Optional[int] = None) -> 'UINode':
        """添加MarginContainer（默认使用MarginContainerHelper）
        
        Args:
            script: 脚本路径，默认使用MarginContainerHelper。设为None可禁用脚本
            use_anchors: 如果为True，使用锚点模式（layout_mode=1）而不是容器模式（layout_mode=2）
            vertical_margin: 垂直边距（用于MarginContainerHelper）
            horizontal_margin: 水平边距（用于MarginContainerHelper）
        """
        node = UINode(name, "MarginContainer")
        
        # 根据是否使用锚点选择layout_mode
        if use_anchors:
            node.properties["layout_mode"] = 1
        else:
            node.properties["layout_mode"] = 2
        
        if uniform is not None:
            node.properties["theme_override_constants/margin_left"] = uniform
            node.properties["theme_override_constants/margin_top"] = uniform
            node.properties["theme_override_constants/margin_right"] = uniform
            node.properties["theme_override_constants/margin_bottom"] = uniform
        else:
            if left is not None:
                node.properties["theme_override_constants/margin_left"] = left
            if top is not None:
                node.properties["theme_override_constants/margin_top"] = top
            if right is not None:
                node.properties["theme_override_constants/margin_right"] = right
            if bottom is not None:
                node.properties["theme_override_constants/margin_bottom"] = bottom
        
        # 默认使用MarginContainerHelper（除非显式设为None）
        if script is not None:
            # 需要在UIBuilder中注册ext_resource
            node.properties["script"] = f'ExtResource("script_{name}")'
            node.properties["_script_path"] = script
            if uniform is not None:
                node.properties["UniformMargin"] = uniform
            if vertical_margin is not None:
                node.properties["VerticalMargin"] = vertical_margin
            if horizontal_margin is not None:
                node.properties["HorizontalMargin"] = horizontal_margin
            node.properties['metadata/_custom_type_script'] = '"uid://bk83ics8idr7w"'
        
        return self._add_child(node)
    
    def add_panel_container(self, name: str) -> 'UINode':
        """添加PanelContainer"""
        node = UINode(name, "PanelContainer")
        node.properties["layout_mode"] = 2
        return self._add_child(node)
    
    def add_scroll_container(self, name: str, horizontal_scroll: int = 0, 
                            vertical_scroll: int = 2, follow_focus: bool = True) -> 'UINode':
        """添加ScrollContainer（滚动容器）
        
        Args:
            horizontal_scroll: 水平滚动模式 (0=禁用, 1=自动, 2=总是显示, 3=总是隐藏)
            vertical_scroll: 垂直滚动模式 (0=禁用, 1=自动, 2=总是显示, 3=总是隐藏)
            follow_focus: 是否自动跟随焦点元素
        """
        node = UINode(name, "ScrollContainer")
        node.properties["layout_mode"] = 2
        node.properties["horizontal_scroll_mode"] = horizontal_scroll
        node.properties["vertical_scroll_mode"] = vertical_scroll
        if follow_focus:
            node.properties["follow_focus"] = "true"
        return self._add_child(node)
    
    def add_vbox(self, name: str, separation: Optional[int] = None) -> 'UINode':
        """添加VBoxContainer"""
        node = UINode(name, "VBoxContainer")
        node.properties["layout_mode"] = 2
        if separation is not None:
            node.properties["theme_override_constants/separation"] = separation
        return self._add_child(node)
    
    def add_hbox(self, name: str, separation: Optional[int] = None) -> 'UINode':
        """添加HBoxContainer"""
        node = UINode(name, "HBoxContainer")
        node.properties["layout_mode"] = 2
        if separation is not None:
            node.properties["theme_override_constants/separation"] = separation
        return self._add_child(node)
    
    # === UI控件方法 ===
    
    def add_color_rect(self, name: str, color: Tuple[float, float, float, float] = (0.15, 0.15, 0.15, 1),
                      use_anchors: bool = False) -> 'UINode':
        """添加ColorRect
        
        Args:
            use_anchors: 如果为True，使用锚点模式填充整个父容器
        """
        node = UINode(name, "ColorRect")
        
        if use_anchors:
            node.properties["layout_mode"] = 1
            node.properties["anchors_preset"] = 15
            node.properties["anchor_right"] = 1.0
            node.properties["anchor_bottom"] = 1.0
            node.properties["grow_horizontal"] = 2
            node.properties["grow_vertical"] = 2
        else:
            node.properties["layout_mode"] = 0
        
        node.properties["color"] = f"Color({color[0]}, {color[1]}, {color[2]}, {color[3]})"
        return self._add_child(node)
    
    def add_label(self, name: str, text: str = "", align: str = "left",
                 font_size: Optional[int] = None, min_size: Optional[Tuple[float, float]] = None,
                 size_flags_h: Optional[int] = None) -> 'UINode':
        """添加Label"""
        node = UINode(name, "Label")
        node.properties["layout_mode"] = 2
        
        if text:
            node.properties["text"] = f'"{text}"'
        
        # 对齐方式映射
        align_map = {"left": 0, "center": 1, "right": 2}
        if align in align_map:
            node.properties["horizontal_alignment"] = align_map[align]
        
        if font_size:
            node.properties["theme_override_font_sizes/font_size"] = font_size
        
        if min_size:
            node.properties["custom_minimum_size"] = f"Vector2({min_size[0]}, {min_size[1]})"
        
        if size_flags_h is not None:
            node.properties["size_flags_horizontal"] = size_flags_h
        
        return self._add_child(node)
    
    def add_progress_bar(self, name: str, value: float = 0, 
                        size_flags_h: Optional[int] = None,
                        size_flags_v: Optional[int] = None,
                        size_flags_stretch_ratio: Optional[float] = None,
                        min_size: Optional[Tuple[float, float]] = None,
                        show_percentage: bool = True) -> 'UINode':
        """添加ProgressBar"""
        node = UINode(name, "ProgressBar")
        node.properties["layout_mode"] = 2
        
        if size_flags_h is not None:
            node.properties["size_flags_horizontal"] = size_flags_h
        
        if size_flags_v is not None:
            node.properties["size_flags_vertical"] = size_flags_v
        
        if size_flags_stretch_ratio is not None:
            node.properties["size_flags_stretch_ratio"] = size_flags_stretch_ratio
        
        node.properties["value"] = value
        
        if min_size:
            node.properties["custom_minimum_size"] = f"Vector2({min_size[0]}, {min_size[1]})"
        
        if show_percentage:
            node.properties["show_percentage"] = "true"
        
        return self._add_child(node)
    
    def add_button(self, name: str, text: str = "", size_flags_h: Optional[int] = None) -> 'UINode':
        """添加Button"""
        node = UINode(name, "Button")
        node.properties["layout_mode"] = 2
        
        if text:
            node.properties["text"] = f'"{text}"'
        
        if size_flags_h is not None:
            node.properties["size_flags_horizontal"] = size_flags_h
        
        return self._add_child(node)
    
    def add_checkbox(self, name: str, text: str = "", size_flags_h: Optional[int] = None,
                    button_pressed: bool = False) -> 'UINode':
        """添加CheckBox"""
        node = UINode(name, "CheckBox")
        node.properties["layout_mode"] = 2
        
        if text:
            node.properties["text"] = f'"{text}"'
        
        if size_flags_h is not None:
            node.properties["size_flags_horizontal"] = size_flags_h
        
        if button_pressed:
            node.properties["button_pressed"] = "true"
        
        return self._add_child(node)
    
    def add_instance(self, name: str, scene_path: str, scene_uid: Optional[str] = None) -> 'UINode':
        """添加场景实例（prefab）
        
        Args:
            name: 实例节点名称
            scene_path: 场景文件路径（如 "res://A1UIScenes/UIComponents/SliderElement.tscn"）
            scene_uid: 场景UID（REQUIRED - use mcp_godot_get_uid to obtain correct UID）
        
        Example:
            # Get UID first via MCP tool
            uid_result = mcp_godot_get_uid(
                projectPath="c:/Godot/3d-practice",
                filePath="A1UIScenes/UIComponents/DropdownComponent.tscn"
            )
            # Then use it
            container.add_instance("DisplayMode", "res://A1UIScenes/UIComponents/DropdownComponent.tscn", 
                                  scene_uid="uid://0st2knyluaer")
        """
        if scene_uid is None:
            raise ValueError(f"scene_uid is REQUIRED for add_instance(). Use mcp_godot_get_uid to obtain the correct UID for {scene_path}")
        
        node = UINode(name, "INSTANCE", auto_suffix=False)
        node.properties["_is_instance"] = True
        node.properties["_scene_path"] = scene_path
        node.properties["_scene_uid"] = scene_uid
        return self._add_child(node)
    
    def add_separator(self, name: str, separation: Optional[int] = None,
                     style: Optional[str] = None) -> 'UINode':
        """添加HSeparator"""
        node = UINode(name, "HSeparator")
        node.properties["layout_mode"] = 2
        
        if separation is not None:
            node.properties["theme_override_constants/separation"] = separation
        
        if style:
            # 需要在UIBuilder中注册ext_resource
            node.properties["theme_override_styles/separator"] = f'ExtResource("style_{name}")'
            node.properties["_style_path"] = style
        
        return self._add_child(node)


class UIBuilder:
    """UI构建器"""
    
    def __init__(self, scene_name: str, scene_uid: Optional[str] = None):
        self.scene_name = scene_name
        self.scene_uid = scene_uid or self._generate_uid()
        self.root: Optional[UINode] = None
        self.ext_resources: List[Dict[str, str]] = []
        self._resource_counter = 1
    
    def _generate_uid(self) -> str:
        """生成随机UID"""
        chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        return "uid://" + "".join(random.choice(chars) for _ in range(14))
    
    def create_control(self, name: str = "Control", fullscreen: bool = True) -> UINode:
        """创建根Control节点"""
        self.root = UINode(name, "Control")
        
        if fullscreen:
            self.root.properties["layout_mode"] = 3
            self.root.properties["anchors_preset"] = 15
            self.root.properties["anchor_right"] = 1.0
            self.root.properties["anchor_bottom"] = 1.0
            self.root.properties["grow_horizontal"] = 2
            self.root.properties["grow_vertical"] = 2
        
        return self.root
    
    def _collect_ext_resources(self, node: UINode):
        """收集所有外部资源引用"""
        # 检查script
        if "_script_path" in node.properties:
            script_path = node.properties["_script_path"]
            if not any(r["path"] == script_path for r in self.ext_resources):
                self.ext_resources.append({
                    "type": "Script",
                    "path": script_path,
                    "id": f"{self._resource_counter}_dsrpe",
                    "uid": "uid://bk83ics8idr7w"  # MarginContainerHelper的固定uid
                })
                self._resource_counter += 1
        
        # 检查style
        if "_style_path" in node.properties:
            style_path = node.properties["_style_path"]
            if not any(r["path"] == style_path for r in self.ext_resources):
                self.ext_resources.append({
                    "type": "StyleBox",
                    "path": style_path,
                    "id": f"{self._resource_counter}_dsrpe",
                    "uid": "uid://dbfc62yrw0q43"  # new_style_box_line的固定uid
                })
                self._resource_counter += 1
        
        # 检查scene instance
        if "_scene_path" in node.properties:
            scene_path = node.properties["_scene_path"]
            if not any(r["path"] == scene_path for r in self.ext_resources):
                self.ext_resources.append({
                    "type": "PackedScene",
                    "path": scene_path,
                    "id": f"{self._resource_counter}_scene",
                    "uid": node.properties.get("_scene_uid", "uid://placeholder")
                })
                self._resource_counter += 1
        
        # 递归处理子节点
        for child in node.children:
            self._collect_ext_resources(child)
    
    def generate_tree_view(self) -> str:
        """生成树状图（给AI看）"""
        if not self.root:
            return "No root node"
        
        lines = []
        
        def _traverse(node: UINode, prefix: str = "", is_last: bool = True):
            # 节点信息
            if node.properties.get("_is_instance"):
                info = f"{node.name} [INSTANCE: {node.properties['_scene_path']}]"
            else:
                info = f"{node.name} ({node.node_type})"
            
            # 添加关键属性
            extras = []
            if "text" in node.properties:
                extras.append(node.properties["text"].strip('"'))
            if "_script_path" in node.properties:
                extras.append("[script]")
            if node == self.root:
                extras.append("[root]")
            
            if extras:
                info += f" {' '.join(extras)}"
            
            # 绘制树形结构
            connector = "└── " if is_last else "├── "
            lines.append(prefix + connector + info)
            
            # 递归子节点
            child_prefix = prefix + ("    " if is_last else "│   ")
            for i, child in enumerate(node.children):
                _traverse(child, child_prefix, i == len(node.children) - 1)
        
        # 根节点特殊处理
        lines.append(f"{self.root.name} ({self.root.node_type}) [root]")
        for i, child in enumerate(self.root.children):
            _traverse(child, "", i == len(self.root.children) - 1)
        
        return "\n".join(lines)
    
    def generate_tscn(self) -> str:
        """生成.tscn文本"""
        if not self.root:
            raise ValueError("No root node created")
        
        # 收集外部资源
        self._collect_ext_resources(self.root)
        
        lines = []
        
        # 文件头
        lines.append(f'[gd_scene format=3 uid="{self.scene_uid}"]')
        lines.append("")
        
        # 外部资源
        for res in self.ext_resources:
            lines.append(f'[ext_resource type="{res["type"]}" uid="{res["uid"]}" path="{res["path"]}" id="{res["id"]}"]')
        
        if self.ext_resources:
            lines.append("")
        
        # 节点定义
        def _write_node(node: UINode):
            # 检查是否是实例节点
            if node.properties.get("_is_instance"):
                # 实例节点格式
                scene_path = node.properties["_scene_path"]
                # 查找对应的PackedScene资源ID
                scene_res_id = None
                for res in self.ext_resources:
                    if res["type"] == "PackedScene" and res["path"] == scene_path:
                        scene_res_id = res["id"]
                        break
                
                if node == self.root:
                    lines.append(f'[node name="{node.name}" instance=ExtResource("{scene_res_id}")]')
                else:
                    lines.append(f'[node name="{node.name}" parent="{node.parent_path}" instance=ExtResource("{scene_res_id}")]')
                
                # ✅ 修复：输出实例节点的自定义属性（非内部属性）
                for key, value in node.properties.items():
                    # 跳过内部属性
                    if key.startswith("_"):
                        continue
                    
                    # 写入属性
                    if isinstance(value, str):
                        lines.append(f'{key} = "{value}"')
                    elif isinstance(value, bool):
                        lines.append(f'{key} = {"true" if value else "false"}')
                    elif isinstance(value, (int, float)):
                        lines.append(f"{key} = {value}")
                    else:
                        lines.append(f"{key} = {value}")
                
                lines.append("")
                
                # 实例节点的子节点仍然正常处理
                for child in node.children:
                    _write_node(child)
                return
            
            # 普通节点头
            if node == self.root:
                lines.append(f'[node name="{node.name}" type="{node.node_type}" unique_id={node.unique_id}]')
            else:
                lines.append(f'[node name="{node.name}" type="{node.node_type}" parent="{node.parent_path}" unique_id={node.unique_id}]')
            
            # 属性
            for key, value in node.properties.items():
                # 跳过内部属性
                if key.startswith("_"):
                    continue
                
                # 处理ExtResource引用
                if isinstance(value, str) and value.startswith("ExtResource"):
                    # 查找对应的资源ID
                    if "script" in key:
                        for res in self.ext_resources:
                            if res["type"] == "Script":
                                value = f'ExtResource("{res["id"]}")'
                                break
                    elif "separator" in key:
                        for res in self.ext_resources:
                            if res["type"] == "StyleBox":
                                value = f'ExtResource("{res["id"]}")'
                                break
                
                # 写入属性
                if isinstance(value, str):
                    lines.append(f"{key} = {value}")
                elif isinstance(value, (int, float)):
                    lines.append(f"{key} = {value}")
                else:
                    lines.append(f"{key} = {value}")
            
            lines.append("")
            
            # 递归子节点
            for child in node.children:
                _write_node(child)
        
        _write_node(self.root)
        
        return "\n".join(lines)
    
    def save(self, output_path: str):
        """保存到文件"""
        content = self.generate_tscn()
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ UI saved to: {output_path}")
