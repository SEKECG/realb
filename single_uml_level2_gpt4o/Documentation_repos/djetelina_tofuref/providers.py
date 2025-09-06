from typing import List, Dict, Any, Optional
from resources import Resource

class Provider:
    def __init__(self, raw_json: Optional[Dict] = None, log_widget: Optional[Any] = None):
        self._active_version: Optional[str] = None
        self._endpoint: Optional[str] = None
        self._overview: Optional[str] = None
        self.active_version: Optional[str] = None
        self.datasources: List[Resource] = []
        self.display_name: Optional[str] = None
        self.fork_of: Optional[str] = None
        self.functions: List[Resource] = []
        self.guides: List[Resource] = []
        self.log_widget: Optional[Any] = log_widget
        self.raw_json: Optional[Dict] = raw_json
        self.resources: List[Resource] = []
        self.use_configuration: Optional[str] = None
        self.versions: List[Dict[str, str]] = []

    def __rich__(self):
        return str(self.__dict__)

    def _endpoint_getter(self) -> str:
        return f"{self.raw_json['organization']}/{self.raw_json['name']}/{self.active_version}"

    @property
    def active_version_getter(self) -> str:
        if not self._active_version:
            self._active_version = self.versions[0]['id']
        return self._active_version

    @active_version_getter.setter
    def active_version_setter(self, value: str):
        self._active_version = value

    @property
    def display_name_getter(self) -> str:
        return f"{self.raw_json['organization']}/{self.raw_json['name']}"

    @classmethod
    def from_json(cls, data: Dict) -> "Provider":
        provider = cls(raw_json=data)
        provider.versions = data.get('versions', [])
        provider.fork_of = data.get('fork_of')
        provider.resources = [Resource(**res) for res in data.get('resources', [])]
        provider.datasources = [Resource(**ds) for ds in data.get('datasources', [])]
        provider.functions = [Resource(**func) for func in data.get('functions', [])]
        provider.guides = [Resource(**guide) for guide in data.get('guides', [])]
        return provider

    def load_resources(self):
        # Implementation for loading resources
        pass

    def overview(self) -> str:
        return self._overview

    @property
    def use_configuration_getter(self) -> str:
        return self.use_configuration