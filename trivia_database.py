from abc import ABC, abstractmethod
import sqlite3
import csv


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

    @abstractmethod
    def db_loader(self, file_path):
        """
        Load the contents of a CSV file into the database.
        :param file_path: the path to the CSV file to load into the database.
        :raise NotImplementedError: this method must be overridden by a concrete implementation.
        """

    @abstractmethod
    def get_question(self, qa_type, difficulty):
        """
        Retrieve a trivia question, answer and hint by its ID.
        :param qa_type: The type of question (true/false, multiple choice, or short answer)
        :param difficulty: the difficulty of the trivia question to retrieve.
        :return: a tuple of the form (question, answer, hint).
        :raise NotImplementedError: this method must be overridden by a concrete implementation.
        """


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

    def db_loader(self, file_path):
        """
        Load the contents of a CSV file into the SQLite database.
        :param file_path: the path to the CSV file to load into the database.
        """
        with open(file_path, newline="") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self.__db_connection.execute(
                    "INSERT INTO Lone_Rangers_QA_DB VALUES (?, ?, ?, ?, ?, ?)",
                    row,
                )

    def get_question(self, qa_type, difficulty):
        """
        Retrieve a trivia question, answer and hint by its ID from an SQLite database.
        :param qa_type: The type of question (true/false, multiple choice, or short answer)
        :param difficulty: the difficulty of the trivia question to retrieve.
        :return: a tuple of the form (question, correct_answer, option_1, option,_2, option_3, option_4).
        """
        cursor = self._sqlite.cursor()
        (
            question,
            correct_answer,
            option_1,
            option_2,
            option_3,
            option_4,
        ) = cursor.fetchone()
        return question, correct_answer, option_1, option_2, option_3, option_4
