from maze import Maze
from trivia_database import SQLiteTriviaDatabase


class QuestionAndAnswer:
    """A class that represents a single question and answer, including its
    associated question type, hint, and answer options."""

    def __init__(self, question, question_type, hint, options, answer):
        """Create a new QuestionAndAnswer instance with the provided
        question, question_type, hint, options, and answer."""
        self.question = question
        self.question_type = question_type
        self.hint = hint
        self.options = options
        self.__answer = answer

    def answer_is_correct(self, user_answer):
        """Return True if the provided user_answer matches the answer for
        this question (case-insensitive), and False otherwise."""
        return user_answer.lower() == self.__answer.lower()


class TriviaMaze:
    """A class that represents the main game logic for a trivia maze game."""

    def __init__(self, num_rows, num_cols, db_file_path):
        """Create a new TriviaMaze instance with the specified number of rows
        and columns in the maze, and the path to the SQLite trivia database
        file to use for questions and answers."""
        self.num_rows = num_rows
        self.num_cols = num_cols

        self.__db = SQLiteTriviaDatabase(db_file_path)

        self.__maze = Maze(num_rows, num_cols, self.__db)
        self.__observers = []

        self.__question_and_answer_buffer = []

        # Artificially add a Q&A to the buffer (pretend the user just walked
        # into a locked door)
        question = "This is the text of a question"
        question_type = "multiple_choice"
        hint = "This is the text of a hint"
        options = ("option1", "option2", "option3", "option4")
        answer = "option3"
        self.__question_and_answer_buffer.append(
            QuestionAndAnswer(question, question_type, hint, options, answer)
        )

    def save_game(self):
        """Save the current game state to a file."""
        pass

    def load_game(self):
        """Load a saved game state from a file."""
        pass

    def get_rooms(self):
        """Return the list of Room instances in the maze."""
        return self.__maze.rooms

    def get_adventurer_hp(self):
        """Return the current hit points of the adventurer."""
        pass

    def get_adventurer_coords(self):
        """Return the current coordinates of the adventurer in the maze."""
        pass

    def move_adventurer(self, direction):
        """Move the adventurer in the specified direction (one of 'north',
        'south', 'east', or 'west') and notify all registered observers of
        the change."""
        self.__notify_observers()

    def use_item(self, item_name):
        """Use the specified item (if it is in the adventurer's inventory) and
        notify all registered observers of the change."""
        # NOTE: This should return False or None if the user did not hold any
        # of the item
        self.__notify_observers()

    def register_observer(self, observer):
        """Register the specified observer to be notified of changes to the
        game state."""
        self.__observers.append(observer)

    def reset(self):
        """Reset the game state to its initial values."""
        pass

    def flush_question_and_answer_buffer(self):
        """Remove and return the next QuestionAndAnswer instance from the
        buffer."""
        return self.__question_and_answer_buffer.pop()

    def flush_event_log_buffer(self):
        """Clear the event log buffer."""
        pass

    def inform_user_answer_correct_or_incorrect(self, answer_was_correct):
        """Display a message to the user indicating whether their answer to
        the previous question was correct or incorrect."""
        pass

    def get_game_status(self):
        """Return a string representing the current status of the game."""
        pass

    def __notify_observers(self):
        """Notify all observers of changes to the game state."""
        for observer in self.__observers:
            observer.update()
