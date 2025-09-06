import os
import pathlib
import json
from typing import Optional

CACHE_DIR = pathlib.Path(os.path.expanduser("~/.cache/pirel"))
CACHE_FILE_GLOB = "*.json"

def calc_cache_age_days(cache_file):
    """Returns the age of the cache in days."""
    cache_mtime = cache_file.stat().st_mtime
    cache_age = (pathlib.Path().stat().st_mtime - cache_mtime) / 86400
    return int(cache_age)

def clear(clear_all):
    """Delete old or all cache files."""
    if clear_all:
        for cache_file in CACHE_DIR.glob(CACHE_FILE_GLOB):
            cache_file.unlink()
    else:
        latest_cache_file = get_latest_cache_file()
        if latest_cache_file:
            latest_cache_file.unlink()

def filename():
    """The name of today's cache file."""
    return CACHE_DIR / f"{pathlib.Path().stat().st_mtime}.json"

def get_latest_cache_file():
    """Returns the path to the latest cache file `None` if no cache exists."""
    cache_files = list(CACHE_DIR.glob(CACHE_FILE_GLOB))
    if not cache_files:
        return None
    return max(cache_files, key=lambda f: f.stat().st_mtime)

def load(cache_file):
    """Loads the data from a cache file path."""
    with open(cache_file, 'r') as f:
        return json.load(f)

def save(data):
    """Save data to new cache file."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with open(filename(), 'w') as f:
        json.dump(data, f)