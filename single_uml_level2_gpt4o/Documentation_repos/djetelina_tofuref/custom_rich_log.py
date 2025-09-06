from textual.widgets import Log

class CustomRichLog(Log):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.border_title = "Log"
        self.border_subtitle = f"Version {__version__}"
        self.display = False