from abc import ABC, abstractmethod
import pathlib
import sqlite3
import csv


class TriviaDatabase(ABC):
    """
    This is an abstract base class for accessing a trivia database.
    """

    @abstractmethod
    def get_question(self):
        """
        Retrieve a trivia question, answer and hint by its ID.
        :return: a tuple of the form (question, answer, hint).
        """


class SQLiteTriviaDatabase(TriviaDatabase):
    """
    A concrete implementation of the TriviaDatabase interface that uses SQLite
    as the underlying database.
    """

    # Path of file to write sqlite db file to
    __DB_FILE_PATH = pathlib.Path("db") / "trivia_maze.db"

    # The one table that holds all data
    __TABLE_NAME = "question_and_answer"

    def __init__(self, file_path):
        """
        Create the database from the contents of a CSV file.
        :param file_path: the path to the CSV file to load into the database.
        """

        # Ensure path for db file exists
        parent_dir = self.__DB_FILE_PATH.parent
        if not parent_dir.exists():
            parent_dir.mkdir()

        # Open connection to file and recreate table
        self.__db_connection = sqlite3.connect(self.__DB_FILE_PATH)
        self.__db_connection.execute(
            f"DROP TABLE IF EXISTS {self.__TABLE_NAME}"
        )
        self.__db_connection.execute(
            f"""CREATE TABLE {self.__TABLE_NAME}
            (category TEXT, qa_type TEXT, difficulty TEXT, question TEXT,
            option_1 TEXT, option_2 TEXT, option_3 TEXT, option_4 TEXT,
            correct_answer TEXT)"""
        )

        # Populate the database with the file content
        self.__load_from_file(file_path)

    def __load_from_file(self, file_path):
        """
        Load the contents of a CSV file into the database.
        :param file_path: the path to the CSV file to load into the database.
        """
        with open(file_path, newline="") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self.__db_connection.execute(
                    f"INSERT INTO {self.__TABLE_NAME} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    row,
                )

    def __del__(self):
        """Delete the db file during garbage collection"""
        self.__DB_FILE_PATH.unlink()

    def get_question(self):
        """
        Retrieve a random trivia question, its correct answer, and its options.
        :return: a tuple of the form (question, correct_answer, option_1,
                 option,_2, option_3, option_4).
        """
        cursor = self.__db_connection.cursor()
        query = f"""
            SELECT question, correct_answer, option_1, option_2, option_3,
            option_4 FROM {self.__TABLE_NAME} ORDER BY RANDOM() LIMIT 1;
        """
        # query = f"""
        #    SELECT * FROM {self.__TABLE_NAME} ORDER BY RANDOM() LIMIT 1;
        # """
        return [s.strip() for s in cursor.execute(query).fetchone()]
