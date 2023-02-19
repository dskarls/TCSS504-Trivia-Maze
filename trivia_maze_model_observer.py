from abc import ABC, abstractmethod
from trivia_maze import TriviaMaze


class TriviaMazeModelObserver(ABC):

    def __init__(self, trivia_maze: TriviaMaze):
        self.__maze = trivia_maze
        self.__maze.register_observer(self)

    @abstractmethod
    def update(self, event):
        pass
