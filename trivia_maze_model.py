from abc import ABC, abstractmethod


class TriviaMazeModel(ABC):
    def __init__(self):
        self._maze_observers = []

    @abstractmethod
    def save_game(self):
        pass

    @abstractmethod
    def load_game(self):
        pass

    @abstractmethod
    def get_rooms(self):
        pass

    @abstractmethod
    def use_item(self, item):
        pass

    @abstractmethod
    def get_adventurer_hp(self):
        pass

    @abstractmethod
    def get_adventurer_coords(self):
        pass

    @abstractmethod
    def get_adventurer_items(self):
        """Get a list of references to all items held by the adventurer."""

    @abstractmethod
    def move_adventurer(self, direction):
        pass

    @abstractmethod
    def register_observer(self, observer):
        pass
