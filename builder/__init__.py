"""
TSCN Builder - Component-Based Architecture for Godot Scene Generation
Composition over Inheritance pattern for flexible scene construction
"""

from .core import TscnBuilder
from .modules.ui import UIModule
from .modules.statechart import StateChartModule

__all__ = ["TscnBuilder", "UIModule", "StateChartModule"]
