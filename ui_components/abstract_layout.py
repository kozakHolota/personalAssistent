from abc import ABC, abstractmethod
import rich


class AbstractLayout(ABC):
    def __init__(self, element):
        self.element = element

    def show(self):
        rich.print(self.element)