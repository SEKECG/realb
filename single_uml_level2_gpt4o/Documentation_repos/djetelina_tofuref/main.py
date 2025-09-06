import logging
from textual.app import App
from textual.widgets import Placeholder
from textual import events

from tofuref.data.providers import Provider
from tofuref.data.resources import Resource
from tofuref.widgets.code_block_select import CodeBlockSelect
from tofuref.widgets.content_window import ContentWindow
from tofuref.widgets.custom_rich_log import CustomRichLog
from tofuref.widgets.providers_option_list import ProvidersOptionList
from tofuref.widgets.resources_option_list import ResourcesOptionList
from tofuref.widgets.search_input import SearchInput

LOGGER = logging.getLogger(__name__)

class TofuRefApp(App):
    BINDINGS = [
        ("ctrl+f", "action_fullscreen", "Toggle Fullscreen"),
        ("ctrl+p", "action_providers", "Show Providers"),
        ("ctrl+r", "action_resources", "Show Resources"),
        ("ctrl+s", "action_search", "Focus Search"),
        ("ctrl+l", "action_log", "Toggle Log"),
        ("ctrl+c", "action_content", "Show Content"),
    ]
    CSS_PATH = "styles.css"
    ESCAPE_TO_MINIMIZE = True
    TITLE = "TofuRef - OpenTofu Provider Reference Application"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active_provider = None
        self.active_resource = None
        self.code_block_selector = CodeBlockSelect()
        self.content_markdown = ContentWindow()
        self.fullscreen_mode = False
        self.log_widget = CustomRichLog()
        self.navigation_providers = ProvidersOptionList()
        self.navigation_resources = ResourcesOptionList()
        self.providers = []
        self.search = SearchInput()

    def action_content(self):
        self.content_markdown.maximize()
        self.content_markdown.focus()

    def action_fullscreen(self):
        self.fullscreen_mode = not self.fullscreen_mode
        self.set_fullscreen(self.fullscreen_mode)

    def action_log(self):
        self.log_widget.toggle_display()

    def action_providers(self):
        self.navigation_providers.maximize()
        self.navigation_providers.focus()

    def action_resources(self):
        self.navigation_resources.maximize()
        self.navigation_resources.focus()

    def action_search(self):
        self.search.focus()

    def action_use(self):
        pass

    def action_version(self):
        pass

    def change_provider_version(self, event):
        pass

    def compose(self):
        return [
            self.navigation_providers,
            self.navigation_resources,
            self.content_markdown,
            self.log_widget,
            self.search,
            self.code_block_selector,
        ]

    def get_system_commands(self, screen):
        return [
            ("Toggle Log", "ctrl+l", self.action_log),
        ]

    def on_ready(self):
        LOGGER.info("TofuRefApp is ready")

    def option_list_option_selected(self, event):
        pass

    def search_input_changed(self, event):
        pass

    def search_input_submitted(self, event):
        pass

def main():
    LOGGER.info("Starting TofuRef application")
    app = TofuRefApp()
    app.run()

if __name__ == "__main__":
    main()