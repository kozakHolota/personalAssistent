from abc import ABC, abstractmethod


class Entity(ABC):
    @abstractmethod
    def edit(self, changes_model):
        pass