import re
from typing import Union, List

from torchcolor.color import Color
from torchcolor.gradient import Gradient
from torchcolor.palette import Palette

LAYER_SPLITTER = re.compile(r'\s*->\s*')
KeyType = str
DelimiterType = str
AnyType = Union[str, int, float, bool]
FunctionalType = Union[Color, Gradient, str, tuple]

def colorize(text, text_color=None, bg_color=None):
    fg_code = Color(text_color).to_ansi(is_background=False) if text_color else ""
    bg_code = Color(bg_color).to_ansi(is_background=True) if bg_color else ""
    return f"{fg_code}{bg_code}{text}{Color.reset_color}"

def clean_style(text):
    return re.sub(r'\x1b\[.*?m', '', text)

def infer_type(self, value):
    if isinstance(value, str):
        return KeyType
    elif isinstance(value, int):
        return DelimiterType
    elif isinstance(value, float):
        return AnyType
    elif isinstance(value, bool):
        return FunctionalType
    else:
        return AnyType

class TextStyle:
    def __init__(self, fg_style=None, bg_style=None, bold=False, italic=False, underline=False, double_underline=False, crossed=False, darken=False):
        self.fg_style = fg_style
        self.bg_style = bg_style
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.double_underline = double_underline
        self.crossed = crossed
        self.darken = darken
        self.__post_init__()

    def __post_init__(self):
        self.fg_style = self._ensure_style(self.fg_style)
        self.bg_style = self._ensure_style(self.bg_style)

    def _ensure_style(self, value):
        if isinstance(value, (Color, Gradient)):
            return value
        return Color(value)

    def apply(self, text):
        style_code = ""
        if self.bold:
            style_code += "\x1b[1m"
        if self.italic:
            style_code += "\x1b[3m"
        if self.underline:
            style_code += "\x1b[4m"
        if self.double_underline:
            style_code += "\x1b[21m"
        if self.crossed:
            style_code += "\x1b[9m"
        if self.darken:
            style_code += "\x1b[2m"
        fg_code = self.fg_style.to_ansi(is_background=False) if self.fg_style else ""
        bg_code = self.bg_style.to_ansi(is_background=True) if self.bg_style else ""
        return f"{style_code}{fg_code}{bg_code}{text}{Color.reset_color}"

class FunctionalStyle:
    def __init__(self, infer_func=None):
        self.infer_func = infer_func
        self.__post_init__()

    def __post_init__(self):
        self.styles = {}

    def apply(self, text):
        parts = LAYER_SPLITTER.split(text)
        styled_parts = [self.infer_func(part).apply(part) for part in parts]
        return ''.join(styled_parts)