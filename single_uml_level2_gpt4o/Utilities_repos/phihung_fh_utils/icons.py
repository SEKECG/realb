import os
import requests
from pathlib import Path

cache = {}
pat = "path/to/icons"
xmlns = "http://www.w3.org/2000/svg"

def BoxIcon(name, variant, **kwargs):
    return _get_boxicon(name, variant)

def FaIcon(name, variant, **kwargs):
    return _get_fa(name, variant)

def HeroIcon(name, variant, **kwargs):
    return _get_heroicon(name, variant)

def IonIcon(name, variant, **kwargs):
    return _get_ionicon(name, variant)

def LcIcon(name, variant, **kwargs):
    return _get_lucide(name, variant)

def PhIcon(name, variant, **kwargs):
    return _get_phosphor_icon(name, variant)

def BsIcon(name, variant, **kwargs):
    return _get_boostrap(name, variant)

def _get_boostrap(name, variant):
    url = f"https://github.com/twbs/icons/blob/main/icons/{name}-{variant}.svg"
    response = requests.get(url)
    return _parse(response.text)

def _get_boxicon(name, variant):
    url = f"https://github.com/atisawd/boxicons/blob/master/svg/{variant}/{name}.svg"
    response = requests.get(url)
    return _parse(response.text)

def _get_fa(name, variant):
    url = f"https://github.com/FortAwesome/Font-Awesome/blob/master/svgs/{variant}/{name}.svg"
    response = requests.get(url)
    return _parse(response.text)

def _get_heroicon(name, variant):
    url = f"https://github.com/tailwindlabs/heroicons/blob/master/solid/{name}.svg"
    response = requests.get(url)
    return _parse(response.text)

def _get_ionicon(name, variant):
    url = f"https://github.com/ionic-team/ionicons/blob/master/src/svg/{name}.svg"
    response = requests.get(url)
    return _parse(response.text)

def _get_lucide(name, variant):
    url = f"https://github.com/lucide-icons/lucide/blob/master/icons/{name}.svg"
    response = requests.get(url)
    return _parse(response.text)

def _get_phosphor_icon(name, variant):
    url = f"https://github.com/phosphor-icons/phosphor-icons/blob/master/src/{variant}/{name}.svg"
    response = requests.get(url)
    return _parse(response.text)

def _make(width, height, content, **kwargs):
    return f'<svg width="{width}" height="{height}" xmlns="{xmlns}" {kwargs}>{content}</svg>'

def _parse(svg):
    # Dummy implementation for parsing SVG content
    width = "24"
    height = "24"
    children = svg
    return _make(width, height, children)