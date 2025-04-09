from abc import ABC, abstractmethod
from typing import List


class Entity(ABC):
    def __init__(self, tags: List[str]):
        self.tags = tags if tags else []

    def add_tags(self, tags):
        self.tags.extend(tags)

    def remove_tags(self, tags):
        for tag in tags:
            if tag in self.tags:
                self.tags.remove(tag)

    @abstractmethod
    def edit(self, changes_model):
        pass