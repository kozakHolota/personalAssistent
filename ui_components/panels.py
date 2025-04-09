from rich.panel import Panel

from ui_components.abstract_layout import AbstractLayout


class AbstractPanel(AbstractLayout):
    def __init__(self, title: str, text: str, color: str):
        super().__init__(Panel.fit(f"[{color}]{text}[/{color}]", title=title))

class ErrorPanel(AbstractPanel):
    def __init__(self, title: str, text: str):
        super().__init__(title, f"❌ {text}", "red")

class WarningPanel(AbstractPanel):
    def __init__(self, title: str, text: str):
        super().__init__(title, f":warning: {text}", "yellow")

class InfoPanel(AbstractPanel):
    def __init__(self, title: str, text: str):
        super().__init__(title, f"ℹ️ {text}", "green")