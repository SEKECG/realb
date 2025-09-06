# color.py

import re

background_colors = {
    'black': '40',
    'red': '41',
    'green': '42',
    'yellow': '43',
    'blue': '44',
    'magenta': '45',
    'cyan': '46',
    'white': '47',
    'reset': '49'
}

foreground_colors = {
    'black': '30',
    'red': '31',
    'green': '32',
    'yellow': '33',
    'blue': '34',
    'magenta': '35',
    'cyan': '36',
    'white': '37',
    'reset': '39'
}

reset_color = '\033[0m'

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def is_rgb(color):
    return isinstance(color, tuple) and len(color) == 3 and all(isinstance(c, int) and 0 <= c <= 255 for c in color)

class Color:
    def __init__(self, value):
        self.value = value

    def to_ansi(self, is_background=False):
        if isinstance(self.value, str):
            if self.value in foreground_colors:
                return f'\033[{foreground_colors[self.value]}m' if not is_background else f'\033[{background_colors[self.value]}m'
            elif re.match(r'^#[0-9A-Fa-f]{6}$', self.value):
                r, g, b = hex_to_rgb(self.value)
                return f'\033[38;2;{r};{g};{b}m' if not is_background else f'\033[48;2;{r};{g};{b}m'
        elif is_rgb(self.value):
            r, g, b = self.value
            return f'\033[38;2;{r};{g};{b}m' if not is_background else f'\033[48;2;{r};{g};{b}m'
        return reset_color

    def to_rgb(self):
        if isinstance(self.value, str):
            if re.match(r'^#[0-9A-Fa-f]{6}$', self.value):
                return hex_to_rgb(self.value)
            elif self.value in foreground_colors:
                return foreground_colors[self.value]
        elif is_rgb(self.value):
            return self.value
        return (0, 0, 0)