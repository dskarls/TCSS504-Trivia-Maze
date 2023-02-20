from abc import ABC, abstractmethod
from trivia_maze import TriviaMaze


class TriviaMazeModelObserver(ABC):

    def __init__(self, trivia_maze: TriviaMaze):
        self._maze = trivia_maze
        self._maze.register_observer(self)

    @abstractmethod
    def update(self, event):
        pass
