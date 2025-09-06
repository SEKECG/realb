import time
import os
import io
import socket
import ssl
import sqlite3
import threading
import builtins
from contextvars import ContextVar
from typing import Callable, Iterable, Iterator, Any, List, Dict

class BlockingError(Exception):
    def __init__(self, func):
        super().__init__(f"Blocking call detected: {func}")

class BlockBusterFunction:
    def __init__(self, module, func_name, scanned_modules=None, excluded_modules=None, can_block_functions=None, can_block_predicate=None):
        self.module = module
        self.func_name = func_name
        self.scanned_modules = scanned_modules
        self.excluded_modules = excluded_modules
        self.can_block_functions = can_block_functions or []
        self.can_block_predicate = can_block_predicate
        self.full_name = f"{module.__name__}.{func_name}"
        self.original_func = getattr(module, func_name)
        self.activated = False

    def activate(self):
        if not self.activated:
            setattr(self.module, self.func_name, self._wrap_blocking(self.original_func))
            self.activated = True
        return self

    def deactivate(self):
        if self.activated:
            setattr(self.module, self.func_name, self.original_func)
            self.activated = False
        return self

    def can_block_in(self, filename, functions):
        self.can_block_functions.append((filename, functions))
        return self

    def _wrap_blocking(self, func):
        def wrapper(*args, **kwargs):
            if blockbuster_skip.get():
                return func(*args, **kwargs)
            if self.can_block_predicate and self.can_block_predicate(*args, **kwargs):
                return func(*args, **kwargs)
            raise BlockingError(func)
        return wrapper

class BlockBuster:
    def __init__(self, scanned_modules=None, excluded_modules=None):
        self.scanned_modules = scanned_modules
        self.excluded_modules = excluded_modules
        self.functions = self._get_wrapped_functions()

    def activate(self):
        for func in self.functions.values():
            func.activate()

    def deactivate(self):
        for func in self.functions.values():
            func.deactivate()

    def _get_wrapped_functions(self):
        functions = {}
        functions.update(self._get_builtins_wrapped_functions())
        functions.update(self._get_io_wrapped_functions())
        functions.update(self._get_lock_wrapped_functions())
        functions.update(self._get_os_wrapped_functions())
        functions.update(self._get_socket_wrapped_functions())
        functions.update(self._get_sqlite_wrapped_functions())
        functions.update(self._get_ssl_wrapped_functions())
        functions.update(self._get_time_wrapped_functions())
        return functions

    def _get_builtins_wrapped_functions(self):
        return {name: BlockBusterFunction(builtins, name, self.scanned_modules, self.excluded_modules) for name in dir(builtins) if callable(getattr(builtins, name))}

    def _get_io_wrapped_functions(self):
        return {name: BlockBusterFunction(io, name, self.scanned_modules, self.excluded_modules) for name in dir(io) if callable(getattr(io, name))}

    def _get_lock_wrapped_functions(self):
        return {name: BlockBusterFunction(threading, name, self.scanned_modules, self.excluded_modules) for name in dir(threading) if callable(getattr(threading, name))}

    def _get_os_wrapped_functions(self):
        return {name: BlockBusterFunction(os, name, self.scanned_modules, self.excluded_modules) for name in dir(os) if callable(getattr(os, name))}

    def _get_socket_wrapped_functions(self):
        return {name: BlockBusterFunction(socket, name, self.scanned_modules, self.excluded_modules) for name in dir(socket) if callable(getattr(socket, name))}

    def _get_sqlite_wrapped_functions(self):
        return {name: BlockBusterFunction(sqlite3, name, self.scanned_modules, self.excluded_modules) for name in dir(sqlite3) if callable(getattr(sqlite3, name))}

    def _get_ssl_wrapped_functions(self):
        return {name: BlockBusterFunction(ssl, name, self.scanned_modules, self.excluded_modules) for name in dir(ssl) if callable(getattr(ssl, name))}

    def _get_time_wrapped_functions(self):
        return {name: BlockBusterFunction(time, name, self.scanned_modules, self.excluded_modules) for name in dir(time) if callable(getattr(time, name))}

blockbuster_skip = ContextVar('blockbuster_skip', default=False)

def blockbuster_ctx(scanned_modules=None, excluded_modules=None):
    bb = BlockBuster(scanned_modules, excluded_modules)
    bb.activate()
    try:
        yield bb
    finally:
        bb.deactivate()