from abc import ABC, abstractmethod
from trivia_maze import TriviaMaze

class TriviaMazeModelObserver(ABC):
    
    def __init__(self):
        self.__maze = TriviaMaze()
        self.__maze.register_observer(self)
    
    @abstractmethod
    def update(self, event):
        pass
    