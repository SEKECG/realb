import datetime
import logging
import requests
from rich.console import Console
from rich.table import Table

DATE_NOW = datetime.date.today()
RELEASE_CYCLE_URL = "https://raw.githubusercontent.com/python/devguide/master/releases.json"
STATUS_TO_EMOJI = {
    "feature": "✨",
    "prerelease": "🔧",
    "bugfix": "🐛",
    "security": "🔒",
    "end-of-life": "💀"
}
STATUS_TO_TEXT = {
    "feature": "Feature",
    "prerelease": "Pre-release",
    "bugfix": "Bugfix",
    "security": "Security",
    "end-of-life": "End-of-life"
}
logger = logging.getLogger(__name__)

class PythonRelease:
    def __init__(self, version, data):
        self._version = version
        self._status = data["status"]
        self._released = data["released"]
        self._end_of_life = data["end_of_life"]
        self._release_manager = data["release_manager"]

    def __repr__(self):
        return f"PythonRelease(version={self._version}, status={self._status})"

    def __str__(self):
        return f"{STATUS_TO_EMOJI[self._status]} {self._version} ({self.status})"

    @property
    def end_of_life(self):
        return wrap_style(self._end_of_life, eol_color(parse_date(self._end_of_life)))

    @property
    def is_eol(self):
        return self._status == "end-of-life"

    @property
    def released(self):
        return wrap_style(self._released, date_style(parse_date(self._released)))

    @property
    def status(self):
        return wrap_style(STATUS_TO_TEXT[self._status], status_style(self._status))

    @property
    def version(self):
        return self._version

    @property
    def version_tuple(self):
        return tuple(map(int, self._version.split(".")))

class PythonReleases:
    def __init__(self, releases_data):
        self.releases = {version: PythonRelease(version, data) for version, data in releases_data.items()}

    def __getitem__(self, version):
        return self.releases[version]

    def to_list(self):
        return list(self.releases.values())

    def to_table(self, active_python_version=None):
        table = Table(title="Python Releases")
        table.add_column("Version", justify="right", style="cyan", no_wrap=True)
        table.add_column("Status", style="magenta")
        table.add_column("Released", justify="right", style="green")
        table.add_column("End of Life", justify="right", style="red")

        for release in self.to_list():
            style = "bold" if release.version == active_python_version else None
            table.add_row(
                wrap_style(release.version, style),
                release.status,
                release.released,
                release.end_of_life
            )
        return table

def load_releases():
    response = requests.get(RELEASE_CYCLE_URL)
    response.raise_for_status()
    return PythonReleases(response.json())

def date_style(date):
    if date < DATE_NOW:
        return "dim"
    return "bold"

def eol_color(eol):
    if eol < DATE_NOW:
        return "red"
    elif (eol - DATE_NOW).days <= 180:
        return "dark_orange"
    elif (eol - DATE_NOW).days <= 365:
        return "yellow"
    return "green"

def parse_date(date_str):
    parts = date_str.split("-")
    if len(parts) == 2:
        return datetime.date(int(parts[0]), int(parts[1]), 1)
    return datetime.date(int(parts[0]), int(parts[1]), int(parts[2]))

def status_style(status):
    styles = {
        "feature": "blue",
        "prerelease": "cyan",
        "bugfix": "green",
        "security": "yellow",
        "end-of-life": "red"
    }
    return styles.get(status, "white")

def wrap_style(text, style):
    return f"[{style}]{text}[/{style}]"