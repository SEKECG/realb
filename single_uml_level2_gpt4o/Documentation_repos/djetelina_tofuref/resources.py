```python
# resources.py

from typing import Optional, Any

class Resource:
    def __init__(self, provider: 'Provider', name: str, type: str, content: Optional[str] = None):
        self.provider = provider
        self.name = name
        self.type = type
        self._content = content

    def __gt__(self, other: 'Resource') -> bool:
        return self.name > other.name

    def __hash__(self) -> int:
        return hash((self.provider.name, self.type, self.name))

    def __lt__(self, other: 'Resource') -> bool:
        return self.name < other.name

    def __rich__(self) -> str:
        return f"[{self.type}] {self.name}"

    def __str__(self) -> str:
        return f"[cyan]{self.type}[/cyan] {self.name}"

    @property
    def content(self) -> Optional[str]:
        return self._content

class ResourceType:
    GUIDE = "guide"
    RESOURCE = "resource"
    DATASOURCE = "datasource"
    FUNCTION = "function"
```