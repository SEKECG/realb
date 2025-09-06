from textual.widgets import Input
from textual.binding import Binding

class SearchInput(Input):
    BINDINGS = [
        Binding("escape", "close", "Close search")
    ]

    def __init__(self, **kwargs):
        super().__init__(placeholder="Search...", id="search-input", classes="bordered", **kwargs)
        self.border_title = "Search"

    def action_close(self):
        self.post_message(self.Changed(self, ""))
        self.post_message(self.Submitted(self, None))