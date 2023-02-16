from abc import ABC, abstractmethod


class TriviaMazeModel(ABC):

    """
    I'm not sure if by nature of the class being abstract the concrete
    class would have to implement the following methods or by having the
    decorator here is no other way around it. -Sheehan
    """

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
    def use_item(self, option, current_room):
        pass

    @abstractmethod
    def create_adventurer(self):
        pass

    @abstractmethod
    def get_adventurer_hp(self):
        pass

    @abstractmethod
    def get_adventurer_coords(self):
        pass

    @abstractmethod
    def move_adventurer(self, command_key):
        pass
