from typing import List

from rich import box
from rich.table import Table

from ui_components.abstract_layout import AbstractLayout


class ConsoleTable(AbstractLayout):
    def __init__(self, title: str, headers: list[str]):
        table = Table(title=title, box=box.SQUARE_DOUBLE_HEAD, expand=True)
        for header in headers:
            table.add_column(header, justify="center", style="yellow", no_wrap=True)
        super().__init__(table)

    def add_row(self, row: List[str]):
        self.element.add_row(*row)
