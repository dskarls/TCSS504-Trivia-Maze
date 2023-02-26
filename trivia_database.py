from abc import ABC, abstractmethod
import sqlite3
import csv


class TriviaDatabase(ABC):
    """
    This is an abstract base class for accessing a trivia database.
    """

    @abstractmethod
    def get_question(self):
        """
        Retrieve a random trivia question type, its question, its correct
        answer, and its options.
        :return: a dict containing the keys "qa_type", "category", "question",
                 "correct_answer", "option_1", "option_2",
                 "option_3", "option_4". See db table docs for meaning of
                 these.
        """


class SQLiteTriviaDatabase(TriviaDatabase):
    """
    A concrete implementation of the TriviaDatabase interface that uses SQLite
    as the underlying database.
    """

    # The one table that holds all data
    __TABLE_NAME = "question_and_answer"

    def __init__(self, file_path):
        """
        Create the database from the contents of a CSV file.
        :param file_path: the path to the CSV file to load into the database.
        """

        # Open connection to file in memory and recreate table
        self.__db_connection = sqlite3.connect(":memory:")
        self.__db_connection.execute(
            f"DROP TABLE IF EXISTS {self.__TABLE_NAME}"
        )
        self.__db_connection.execute(
            f"""CREATE TABLE {self.__TABLE_NAME}
            (category TEXT, qa_type TEXT, difficulty TEXT, question TEXT,
            option_1 TEXT, option_2 TEXT, option_3 TEXT, option_4 TEXT,
            correct_answer TEXT)"""
        )
        # Allow for dict returns from cursors using this connection
        self.__db_connection.row_factory = self.__dict_factory

        # Populate the database with the file content
        self.__load_from_file(file_path)

    @staticmethod
    def __dict_factory(cursor, row):
        """Factory for converting a row of the database as a dict. Taken from
        https://docs.python.org/3/library/sqlite3.html#sqlite3-howto-row-factory
        (Zero Clause BSD license).
        """
        fields = [column[0] for column in cursor.description]
        return {key: value for key, value in zip(fields, row)}

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

    def get_question(self):
        """
        Retrieve a random trivia question type, its question, its correct
        answer, and its options.
        :return: a dict containing the keys "qa_type", "category", "question",
                 "correct_answer", "option_1", "option_2",
                 "option_3", "option_4". See db table docs for meaning of
                 these.
        """
        cursor = self.__db_connection.cursor()
        query = f"""
            SELECT qa_type, question, category, correct_answer, option_1, option_2,
            option_3, option_4 FROM {self.__TABLE_NAME} ORDER BY RANDOM() LIMIT
            1;
        """
        res = cursor.execute(query).fetchone()

        return self.__postprocess_record(res)

    @staticmethod
    def __postprocess_record(record):
        """Clean up a single record dict returned from the database by doing
        string normalizations of its values."""
        # Strip leading and trailing spaces
        record = {
            col_name: col_val.strip() for col_name, col_val in record.items()
        }

        # Convert "null" strings to None
        for col_name, col_val in record.items():
            if col_val.lower() == "null":
                record[col_name] = None

            # TODO: Also convert "true" and "false" strings to True and False?

        return record
