# print.py

from torchcolor.color import Color
from torchcolor.style import TextStyle

def print_color(text, text_color, bg_color):
    text_color_ansi = Color(text_color).to_ansi(is_background=False)
    bg_color_ansi = Color(bg_color).to_ansi(is_background=True)
    reset_color = Color.reset_color
    return f"{bg_color_ansi}{text_color_ansi}{text}{reset_color}"

def print_more(*args, **kwargs):
    separator = kwargs.get('separator', ' ')
    styled_texts = []
    for arg in args:
        if isinstance(arg, str):
            styled_texts.append(arg)
        elif isinstance(arg, TextStyle):
            styled_texts.append(arg.apply(arg.text))
    print(separator.join(styled_texts))