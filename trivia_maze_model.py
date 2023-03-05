from abc import ABC, abstractmethod


class TriviaMazeModel(ABC):
    """Represents a trivia maze, which features a maze with a single entrance
    and single exit filled with items (and Q&A-enabled doors), an
    adventurer, and pits."""

    def __init__(self):
        self._maze_observers = []

    @abstractmethod
    def save_game(self):
        """
        Save the relevant parts of the model to a save file that can be loaded
        at a later time to continue the game.
        """

    @abstractmethod
    def load_game(self):
        """
        Load the relevant parts of a saved model from a save file.

        Raises
        ------
        SaveGameFileNotFound
            If no save game file can be found.
        """

    @abstractmethod
    def get_rooms(self):
        """Returns a 2d list of the rooms in the maze.

        Returns
        -------
        List[List[Room]]
            All of the rooms in the maze.
        """

    @abstractmethod
    def use_item(self, item):
        """
        Attempts to consume one of the adventurer's items. If they don't have
        the relevant item, no action is taken.

        NOTE: Successfully using a magic key will actually result in moving the
        adventurer to the relevant room.

        Parameters
        ----------
        item : str
            One of the consumable items the adventurer can use.
        """

    @abstractmethod
    def get_adventurer_hp(self):
        """Returns the adventurer's current hit points.

        Returns
        -------
        int
            The adventurer's current hp.
        """

    @abstractmethod
    def get_adventurer_coords(self):
        """Returns a tuple of the adventurer's current coordinates in the maze.

        Returns
        -------
        tuple[int]
            A 2-tuple containing the adventurer's current row and column as
            integers.
        """

    @abstractmethod
    def get_adventurer_items(self):
        """Get a list of all items held by the adventurer.

        Returns
        -------
        List[MazeItem]
            A list of all items currently held by the adventurer.
        """

    @abstractmethod
    def move_adventurer(self, direction):
        """
        Given a directional command will attempt to move the adventurer that
        direction if the move is legal (not a wall, not a locked/perm locked
        door).
        Parameters
        ----------
        direction : str
            direction the adventurer is trying to move.
        """

    @abstractmethod
    def register_observer(self, observer):
        """Add a TriviaMazeModelObserver object to the registered list of
        observers tracked by the model.

        Parameters
        ----------
        TriviaMazeModelObserver
            An observer object that should be notified whenever the model's
            internal state is updated.
        """
