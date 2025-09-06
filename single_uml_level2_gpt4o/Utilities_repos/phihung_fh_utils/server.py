import os
import sys
import logging
import uvicorn
from fastapi import FastAPI
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

FAST = "fast"
FULL = "full"

server = None
watcher = None

class CliException(Exception):
    pass

class Watcher:
    def __init__(self, **kwargs):
        self.should_exit = False
        self.watch_filter = kwargs.get("watch_filter", None)
        self.watcher = kwargs.get("watcher", None)

    def loop(self):
        while not self.should_exit:
            yield from self.watcher()

    def shutdown(self):
        self.should_exit = True

def no_reload(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def no_reload_cache(user_function):
    def wrapper(*args, **kwargs):
        return user_function(*args, **kwargs)
    return wrapper

def serve(appname, app, host, port, reload, reload_includes, reload_excludes, **kwargs):
    if reload:
        serve_dev(appname, app, host, port, reload_includes, reload_excludes, **kwargs)
    else:
        serve_prod(appname, app, host, port, **kwargs)

def _add_live_reload(app, **kwargs):
    pass

def _display_path(path):
    return str(path)

def _get_import_string(path, app_name):
    return f"{path}:{app_name}"

def _get_module_data_from_path(path):
    return _ModuleData()

def _patch_autoreload():
    pass

def _run_with_fast_reload(module_import_str, app_str, port, host, live, **kwargs):
    pass

def _terminate(port):
    pass

def serve_dev(path, app, host, port, live, reload, **kwargs):
    pass

def serve_prod(path, app, host, port, **kwargs):
    pass

class _ModuleData:
    pass