from rich.tree import Tree

from ui_components.abstract_layout import AbstractLayout


class SelectionTree(AbstractLayout):
    def __init__(self, title: str, items: list[str]):
        tree = Tree(f"[bold][yellow]{title}")
        for item in items:
            tree.add(f"[bold][green]{item}")
        super().__init__(tree)
