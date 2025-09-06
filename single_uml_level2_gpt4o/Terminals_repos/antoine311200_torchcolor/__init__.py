# torchcolor/__init__.py

from .color import hex_to_rgb, is_rgb, Color, background_colors, foreground_colors, reset_color
from .gradient import Gradient, GradientChunk
from .palette import Palette, palette_autumn_foliage, palette_forest_greens, palette_lavender_dreams, palette_monochrome, palette_ocean_breeze, palette_pastel, palette_rainbow, palette_retro_neon, palette_warm_sunset
from .print import print_color, print_more
from .printer import _addindent, summarize_repeated_modules, ModuleParam, Printer
from .strategy import ColorStrategy, ModuleStyle, ConstantColorStrategy, LayerColorStrategy, TrainableStrategy
from .style import colorize, clean_style, infer_type, TextStyle, FunctionalStyle

__all__ = [
    'hex_to_rgb', 'is_rgb', 'Color', 'background_colors', 'foreground_colors', 'reset_color',
    'Gradient', 'GradientChunk',
    'Palette', 'palette_autumn_foliage', 'palette_forest_greens', 'palette_lavender_dreams', 'palette_monochrome', 'palette_ocean_breeze', 'palette_pastel', 'palette_rainbow', 'palette_retro_neon', 'palette_warm_sunset',
    'print_color', 'print_more',
    '_addindent', 'summarize_repeated_modules', 'ModuleParam', 'Printer',
    'ColorStrategy', 'ModuleStyle', 'ConstantColorStrategy', 'LayerColorStrategy', 'TrainableStrategy',
    'colorize', 'clean_style', 'infer_type', 'TextStyle', 'FunctionalStyle'
]