from abc import abstractmethod

from trivia_maze_model_observer import TriviaMazeModelObserver


class TriviaMazeController(TriviaMazeModelObserver):
    """An agent that observes a maze model and controls it based on user input
    forwarded by the view."""

    @abstractmethod
    def process_keystroke(self, key):
        """
        Takes a keyboard input and interprets it as a command to be issued to
        the model or view which is then called as appropriate.
        """

    @abstractmethod
    def start_main_event_loop(self):
        """
        Display main menu and start listening for input from user
        """
