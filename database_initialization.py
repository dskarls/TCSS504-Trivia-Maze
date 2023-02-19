from abc import ABC, abstractmethod
import sqlite3


class TriviaDatabase(ABC):
    """
    This is an abstract base class for accessing a trivia database.
    """

    @abstractmethod
    def connect(self, connection):
        """
        Connect to the database using the specified connection string.

        :param connection: the connection string to use when connecting to the database.
        :raise NotImplementedError: this method must be overridden by a concrete implementation.
        """
        pass

    @abstractmethod
    def get_question(self, difficulty):
        """
        Retrieve a trivia question, answer and hint by its ID.

        :param difficulty: the difficulty of the trivia question to retrieve.
        :return: a tuple of the form (question, answer, hint).
        :raise NotImplementedError: this method must be overridden by a concrete implementation.
        """
        pass

    @abstractmethod
    def add_question(self, question_id, difficulty, qa_type, category, question, option_1, option_2, option_3, option_4, answer, hint):
        """
        Add a new trivia question, answer and hint to the database.

        :param question_id: a unique integer used to identify each question.
        :param difficulty: the difficulty level of the question to add.
        :param category: the category of the question to add.
        :param qa_type: the type of question (True or False, Multiple Choice, or Short Answer) to add.
        :param question: the trivia question to add.
        :param option_1: 1st column open to containing an answer option.
        :param option_2: 2nd column open to containing an answer option.
        :param option_3: 3rd column open to containing an answer option.
        :param option_4: 4th column open to containing an answer option.
        :param answer: the correct answer to the trivia question.
        :param hint: a hint for the trivia question.
        :raise NotImplementedError: this method must be overridden by a concrete implementation.
        """
        pass


class SQLiteTriviaDatabase(TriviaDatabase):
    """
    A concrete implementation of the TriviaDatabase interface that uses SQLite as the underlying database.
    """

    def __init__(self):  # PyCharm's suggestion to make __db_connection work
        super().__init__()
        self.__db_connection = None

    def connect(self, connection):
        """
        Connect to an SQLite database using the specified connection.

        :param connection: the connection string to use when connecting to the SQLite database.
        """
        self.__db_connection = sqlite3.connect(connection)

    def get_question(self, difficulty):
        """
        Retrieve a trivia question, answer and hint by its ID from an SQLite database.

        :param difficulty: the difficulty of the trivia question to retrieve.
        :return: a tuple of the form (question, answer, option_1, option,_2, option_3, option_4,, hint).
        """
        cursor = self._sqlite.cursor()
        question, answer, option_1, option,_2, option_3, option_4, hint = cursor.fetchone()
        return question, answer, option_1, option,_2, option_3, option_4, hint

    def add_question(self, question_id, difficulty, category, qa_type, question, option_1, option_2, option_3, option_4, answer, hint):
        """
        Add a new trivia question to an SQLite database.

        :param question_id: the 4-digit identification number of the question to add.
        :param difficulty: the difficulty level of the question to add.
        :param category: the category of the question to add.
        :param qa_type: the type of question (True or False, Multiple Choice, or Short Answer) to add.
        :param question: the trivia question to add.
        :param option_1: 1st column open to containing an answer option.
        :param option_2: 2nd column open to containing an answer option.
        :param option_3: 3rd column open to containing an answer option.
        :param option_4: 4th column open to containing an answer option.
        :param answer: the correct answer to the trivia question.
        :param hint: a hint for the trivia question.
        """
        cursor = self._sqlite.cursor()
        cursor.execute('INSERT INTO questions (question_id, difficulty, category, qa_type, question, option_1, option_2, option_3, option_4, answer, hint) VALUES (?,?,?,?,?,?,?,?,?,?,?)', (question_id, difficulty, category, qa_type, question, option_1, option_2, option_3, option_4, answer, hint))
        self._sqlite.commit()
