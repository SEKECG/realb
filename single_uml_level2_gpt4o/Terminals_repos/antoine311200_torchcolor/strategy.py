# strategy.py

from typing import Any, Dict, List, Union
from torchcolor.style import TextStyle, FunctionalStyle
from torchcolor.printer import ModuleStyle

class ColorStrategy:
    _registry = {}

    @classmethod
    def get_strategy(cls, key, *args, **kwargs):
        if key not in cls._registry:
            raise ValueError(f"Strategy '{key}' is not registered.")
        return cls._registry[key](*args, **kwargs)

    @classmethod
    def available_strategies(cls):
        return list(cls._registry.keys())

    @classmethod
    def create(cls, key, *args, **kwargs):
        return cls.get_strategy(key, *args, **kwargs)

    def get_style(self, module, params):
        raise NotImplementedError("Subclasses should implement this method.")

    @classmethod
    def register(cls, key):
        def decorator(strategy_cls):
            cls._registry[key] = strategy_cls
            return strategy_cls
        return decorator

@ColorStrategy.register("constant")
class ConstantColorStrategy(ColorStrategy):
    def __init__(self, color=""):
        self.color = color

    def get_style(self, module, config):
        return ModuleStyle(
            name_style=TextStyle(fg_style=self.color, double_underline=True, italic=True),
            layer_style=TextStyle(fg_style=self.color),
            extra_style=TextStyle(fg_style=self.color)
        )

@ColorStrategy.register("layer")
class LayerColorStrategy(ColorStrategy):
    def get_style(self, module):
        return ModuleStyle(
            name_style=TextStyle(fg_style="blue"),
            layer_style=TextStyle(fg_style="green"),
            extra_style=TextStyle(fg_style="yellow")
        )

@ColorStrategy.register("trainable")
class TrainableStrategy(ColorStrategy):
    def get_style(self, module, config):
        if config.get("is_root", False):
            return ModuleStyle(
                name_style=TextStyle(fg_style="red"),
                layer_style=TextStyle(fg_style="red"),
                extra_style=TextStyle(fg_style="red")
            )
        elif module.requires_grad:
            return ModuleStyle(
                name_style=TextStyle(fg_style="green"),
                layer_style=TextStyle(fg_style="green"),
                extra_style=TextStyle(fg_style="green")
            )
        else:
            return ModuleStyle(
                name_style=TextStyle(fg_style="yellow"),
                layer_style=TextStyle(fg_style="yellow"),
                extra_style=TextStyle(fg_style="yellow")
            )