import re
import logging
import subprocess
from typing import Optional

PYTHON_VERSION_RE = re.compile(r"Python (\d+)\.(\d+)\.(\d+)")
logger = logging.getLogger(__name__)

class ActivePythonInfo:
    def __init__(self, command, path, version):
        self.command = command
        self.path = path
        self.version = version

class PythonVersion:
    def __init__(self, major, minor, patch):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __repr__(self):
        return f"PythonVersion({self.major}, {self.minor}, {self.patch})"

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    @property
    def as_release(self):
        return f"{self.major}.{self.minor}"

    @classmethod
    def from_cli(cls, version):
        match = PYTHON_VERSION_RE.match(version)
        if match:
            major, minor, patch = map(int, match.groups())
            return cls(major, minor, patch)
        raise ValueError(f"Invalid Python version string: {version}")

    @classmethod
    def this(cls):
        return cls(*subprocess.check_output(["python", "-c", "import sys; print('.'.join(map(str, sys.version_info[:3])))"]).decode().strip().split('.'))

    @property
    def version_tuple(self):
        return (self.major, self.minor, self.patch)

def get_active_python_info():
    commands = ["python", "python3", "python2"]
    for command in commands:
        try:
            path = subprocess.check_output(["which", command]).decode().strip()
            version = subprocess.check_output([command, "--version"]).decode().strip()
            return ActivePythonInfo(command, path, PythonVersion.from_cli(version))
        except subprocess.CalledProcessError:
            continue
    return None