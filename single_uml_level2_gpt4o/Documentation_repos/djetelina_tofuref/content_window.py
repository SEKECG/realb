from textual.app import App
from textual.widgets import Markdown
from textual.binding import Binding
from textual.widget import Widget

class ContentWindow(Widget):
    ALLOW_MAXIMIZE = True
    BINDINGS = [
        Binding("down", "action_down", "Scroll Down"),
        Binding("pagedown", "action_page_down", "Page Down"),
        Binding("pageup", "action_page_up", "Page Up"),
        Binding("end", "action_scroll_end", "Scroll End"),
        Binding("home", "action_scroll_home", "Scroll Home"),
        Binding("t", "action_toggle_toc", "Toggle TOC"),
        Binding("y", "action_yank", "Yank Code Block"),
        Binding("up", "action_up", "Scroll Up"),
    ]

    def __init__(self, content, **kwargs):
        super().__init__(**kwargs)
        self.content = content
        self.show_table_of_contents = False
        self.markdown = Markdown(content)

    def action_down(self):
        self.markdown.scroll_down()

    def action_page_down(self):
        self.markdown.page_down()

    def action_page_up(self):
        self.markdown.page_up()

    def action_scroll_end(self):
        self.markdown.scroll_end()

    def action_scroll_home(self):
        self.markdown.scroll_home()

    def action_toggle_toc(self):
        self.show_table_of_contents = not self.show_table_of_contents
        if self.show_table_of_contents:
            self.markdown.show_toc()
        else:
            self.markdown.hide_toc()

    def action_up(self):
        self.markdown.scroll_up()

    def action_yank(self):
        # Assuming there's a method to extract code blocks
        code_blocks = self.markdown.extract_code_blocks()
        # Assuming there's a CodeBlockSelect widget to handle this
        self.app.show_code_block_selector(code_blocks)

    def go(self, location):
        self.markdown.open_link(location)

    def update(self, markdown):
        self.markdown.update(markdown)