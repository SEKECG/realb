import logging
from typing import ClassVar, list, dict
from textual.widgets import OptionList
from textual.binding import BindingType
from textual import events
from textual.message import Message
from textual.app import App

from tofuref.data.providers import Provider
from tofuref.data.helpers import get_registry_api, is_provider_index_expired, save_to_cache, get_from_cache

LOGGER = logging.getLogger(__name__)

class ProvidersOptionList(OptionList):
    BINDINGS: ClassVar[list[BindingType]] = [
        BindingType("enter", "select", "Select"),
        BindingType("escape", "close", "Close"),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.border_title = "Providers"
        self.border_subtitle = ""

    def load_index(self) -> dict[str, Provider]:
        endpoint = "providers/index"
        cached_content = get_from_cache(endpoint)
        if cached_content and not is_provider_index_expired(cached_content):
            return Provider.from_json(cached_content)
        response = get_registry_api(endpoint, json=True, log_widget=self.log_widget)
        save_to_cache(endpoint, response)
        return Provider.from_json(response)

    def on_option_selected(self, option: OptionList.Option) -> None:
        self.post_message(Message("option_selected", option))

    def populate(self, providers: list[Provider] = None) -> None:
        self.clear()
        if providers is None:
            providers = self.load_index().values()
        for provider in providers:
            self.add_option(provider.display_name)
        self.border_subtitle = f"{len(providers)} providers"