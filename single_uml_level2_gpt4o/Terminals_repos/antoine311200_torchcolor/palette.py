# palette.py

from typing import ClassVar, Dict, List
from torchcolor.color import Color

class Palette:
    _registry: ClassVar[Dict[str, "Palette"]] = {}
    disable_registry: bool = False

    def __init__(self, name: str, colors: List[Color]):
        self.name = name
        self.colors = colors
        self.__post_init__()

    def __post_init__(self):
        if not self.disable_registry:
            self._registry[self.name] = self

    def __getitem__(self, index: int) -> Color:
        return self.colors[index % len(self.colors)]

    @classmethod
    def get_palette(cls, name: str) -> "Palette":
        return cls._registry.get(name)

    def generate_gradient(self, n: int) -> List[Color]:
        if n <= 1:
            return [self.colors[0]]
        step = len(self.colors) / (n - 1)
        return [self.colors[int(i * step)] for i in range(n)]

    @classmethod
    def get(cls, name: str) -> "Palette":
        return cls._registry.get(name)

palette_autumn_foliage = Palette(
    "autumn_foliage",
    [
        Color("Light Pink"), Color("Powder Blue"), Color("Pale Green"), Color("Lemon Chiffon"),
        Color("Khaki"), Color("Magenta"), Color("Lime"), Color("Yellow"), Color("Black"),
        Color("Cyan"), Color("Red"), Color("Black"), Color("Dark Gray"), Color("Gray"),
        Color("Light Gray"), Color("White"), Color("Red"), Color("Orange"), Color("Yellow"),
        Color("Green"), Color("Blue"), Color("Indigo"), Color("Violet")
    ]
)

palette_forest_greens = Palette(
    "forest_greens",
    [
        Color("Lavender"), Color("Thistle"), Color("Medium Violet Red"), Color("Dark Orchid"),
        Color("Blue Violet"), Color("Orange Red"), Color("Saddle Brown"), Color("Brown"),
        Color("Chocolate"), Color("Gold"), Color("Light Pink"), Color("Powder Blue"),
        Color("Pale Green"), Color("Lemon Chiffon"), Color("Khaki"), Color("Magenta"),
        Color("Lime"), Color("Yellow"), Color("Black"), Color("Cyan"), Color("Red"),
        Color("Black"), Color("Dark Gray"), Color("Gray"), Color("Light Gray"), Color("White"),
        Color("Red"), Color("Orange"), Color("Yellow"), Color("Green"), Color("Blue"),
        Color("Indigo"), Color("Violet")
    ]
)

palette_lavender_dreams = Palette(
    "lavender_dreams",
    [
        Color("Orange Red"), Color("Saddle Brown"), Color("Brown"), Color("Chocolate"),
        Color("Gold"), Color("Light Pink"), Color("Powder Blue"), Color("Pale Green"),
        Color("Lemon Chiffon"), Color("Khaki"), Color("Magenta"), Color("Lime"), Color("Yellow"),
        Color("Black"), Color("Cyan"), Color("Red"), Color("Black"), Color("Dark Gray"),
        Color("Gray"), Color("Light Gray"), Color("White"), Color("Red"), Color("Orange"),
        Color("Yellow"), Color("Green"), Color("Blue"), Color("Indigo"), Color("Violet")
    ]
)

palette_monochrome = Palette(
    "monochrome",
    [
        Color("Red"), Color("Orange"), Color("Yellow"), Color("Green"), Color("Blue"),
        Color("Indigo"), Color("Violet")
    ]
)

palette_ocean_breeze = Palette(
    "ocean_breeze",
    [
        Color("Forest Green"), Color("Dark Green"), Color("Sea Green"), Color("Dark Sea Green"),
        Color("Pale Green"), Color("Lavender"), Color("Thistle"), Color("Medium Violet Red"),
        Color("Dark Orchid"), Color("Blue Violet"), Color("Orange Red"), Color("Saddle Brown"),
        Color("Brown"), Color("Chocolate"), Color("Gold"), Color("Light Pink"), Color("Powder Blue"),
        Color("Pale Green"), Color("Lemon Chiffon"), Color("Khaki"), Color("Magenta"), Color("Lime"),
        Color("Yellow"), Color("Black"), Color("Cyan"), Color("Red"), Color("Black"), Color("Dark Gray"),
        Color("Gray"), Color("Light Gray"), Color("White"), Color("Red"), Color("Orange"), Color("Yellow"),
        Color("Green"), Color("Blue"), Color("Indigo"), Color("Violet")
    ]
)

palette_pastel = Palette(
    "pastel",
    [
        Color("Magenta"), Color("Lime"), Color("Yellow"), Color("Black"), Color("Cyan"),
        Color("Red"), Color("Black"), Color("Dark Gray"), Color("Gray"), Color("Light Gray"),
        Color("White"), Color("Red"), Color("Orange"), Color("Yellow"), Color("Green"),
        Color("Blue"), Color("Indigo"), Color("Violet")
    ]
)

palette_rainbow = Palette(
    "rainbow",
    [
        Color("Red"), Color("Orange"), Color("Yellow"), Color("Green"), Color("Blue"),
        Color("Indigo"), Color("Violet")
    ]
)

palette_retro_neon = Palette(
    "retro_neon",
    [
        Color("Black"), Color("Dark Gray"), Color("Gray"), Color("Light Gray"), Color("White"),
        Color("Red"), Color("Orange"), Color("Yellow"), Color("Green"), Color("Blue"),
        Color("Indigo"), Color("Violet")
    ]
)

palette_warm_sunset = Palette(
    "warm_sunset",
    [
        Color("Dark Turquoise"), Color("Light Sea Green"), Color("Medium Turquoise"), Color("Turquoise"),
        Color("Aquamarine"), Color("Forest Green"), Color("Dark Green"), Color("Sea Green"),
        Color("Dark Sea Green"), Color("Pale Green"), Color("Lavender"), Color("Thistle"),
        Color("Medium Violet Red"), Color("Dark Orchid"), Color("Blue Violet"), Color("Orange Red"),
        Color("Saddle Brown"), Color("Brown"), Color("Chocolate"), Color("Gold"), Color("Light Pink"),
        Color("Powder Blue"), Color("Pale Green"), Color("Lemon Chiffon"), Color("Khaki"),
        Color("Magenta"), Color("Lime"), Color("Yellow"), Color("Black"), Color("Cyan"),
        Color("Red"), Color("Black"), Color("Dark Gray"), Color("Gray"), Color("Light Gray"),
        Color("White"), Color("Red"), Color("Orange"), Color("Yellow"), Color("Green"),
        Color("Blue"), Color("Indigo"), Color("Violet")
    ]
)