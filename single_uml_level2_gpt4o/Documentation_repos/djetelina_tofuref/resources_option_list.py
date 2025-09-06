# resources_option_list.py

from typing import ClassVar, List
from textual.widgets import OptionList
from textual.binding import BindingType
from textual import events
from textual.message import Message
from textual.reactive import Reactive
from textual.widget import Widget
from textual.app import App
from textual import log

from ..data.providers import Provider
from ..data.resources import Resource

class ResourcesOptionList(OptionList):
    BINDINGS: ClassVar[List[BindingType]] = [
        BindingType("enter", "select", "Select"),
        BindingType("escape", "close", "Close"),
    ]

    border_subtitle: Reactive[str] = Reactive("")
    border_title: Reactive[str] = Reactive("Resources")
    highlighted: Reactive[bool] = Reactive(False)
    loading: Reactive[bool] = Reactive(False)

    def __init__(self, **kwargs):
        super().__init__(name="Resources", id="nav-resources", classes="nav-selector bordered", **kwargs)
        self.border_title = "Resources"

    async def load_provider_resources(self, provider: Provider):
        self.loading = True
        self.clear()
        resources = provider.resources
        self.populate(provider, resources)
        self.loading = False

    async def on_option_selected(self, option: OptionList.Option):
        resource = option.data
        if isinstance(resource, Resource):
            await self.app.action_content(resource.content)

    def populate(self, provider: Provider, resources: List[Resource] = None):
        self.clear()
        if resources is None:
            resources = provider.resources
        self.border_subtitle = f"{len(resources)} resources"
        for resource in resources:
            self.add_option(resource.name, resource)