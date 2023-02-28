import pathlib
from maze import Maze
from trivia_database import SQLiteTriviaDatabase


class QuestionAndAnswer:
    def __init__(self, question, question_type, hint, options, answer):
        self.question = question
        self.question_type = question_type
        self.hint = hint
        self.options = options
        self.__answer = answer

    def answer_is_correct(self, user_answer):
        return user_answer.lower() == self.__answer.lower()


class TriviaMaze:
    def __init__(self, num_rows, num_cols, db_file_path):
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
        pass

    def load_game(self):
        pass

    def get_rooms(self):
        return self.__maze.rooms

    def get_adventurer_hp(self):
        pass

    def get_adventurer_coords(self):
        pass

    def move_adventurer(self, direction):
        self.__notify_observers()

    def use_item(self, item_name):
        # NOTE: This should return False or None if the user did not hold any
        # of the item
        self.__notify_observers()

    def register_observer(self, observer):
        self.__observers.append(observer)

    def reset(self):
        pass

    def flush_question_and_answer_buffer(self):
        return self.__question_and_answer_buffer.pop()

    def flush_event_log_buffer(self):
        pass

    def inform_user_answer_correct_or_incorrect(self, answer_was_correct):
        pass

    def get_game_status(self):
        pass

    def __notify_observers(self):
        for observer in self.__observers:
            observer.update()
