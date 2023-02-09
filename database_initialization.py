import sqlite3


class TriviaDatabase:
    """
    This is an abstract base class for accessing a trivia database.
    """
    def __init__(self):
        """
        Initialize the database backend.
        """
        self._db = None

    def connect(self, connection_string):
        """
        Connect to the database using the specified connection string.

        :param connection_string: the connection string to use when connecting to the database.
        :raise NotImplementedError: this method must be overridden by a concrete implementation.
        """
        raise NotImplementedError

    def get_question(self, question_id):
        """
        Retrieve a trivia question, answer and hint by its ID.

        :param question_id: the ID of the trivia question to retrieve.
        :return: a tuple of the form (question, answer, hint).
        :raise NotImplementedError: this method must be overridden by a concrete implementation.
        """
        raise NotImplementedError

    def add_question(self, question_id, difficulty, category, question, answer, hint):
        """
        Add a new trivia question, answer and hint to the database.

        :param question_id: the 4-digit identification number of the question to add.
        :param difficulty: the difficulty level of the question to add.
        :param category: the category of the question to add.
        :param question: the trivia question to add.
        :param answer: the correct answer to the trivia question.
        :param hint: a hint for the trivia question.
        :raise NotImplementedError: this method must be overridden by a concrete implementation.
        """
        raise NotImplementedError


class SQLiteTriviaDatabase(TriviaDatabase):
    """
    A concrete implementation of the TriviaDatabase interface that uses SQLite as the underlying database.
    """
    def connect(self, connection_string):
        """
        Connect to an SQLite database using the specified connection string.

        :param connection_string: the connection string to use when connecting to the SQLite database.
        """
        self._db = sqlite3.connect(connection_string)

    def get_question(self, question_id):
        """
        Retrieve a trivia question, answer and hint by its ID from an SQLite database.

        :param question_id: the ID of the trivia question to retrieve.
        :return: a tuple of the form (question, answer, hint).
        """
        cursor = self._db.cursor()
        cursor.execute("SELECT * FROM questions WHERE id = ?", (question_id,))
        question, answer, hint = cursor.fetchone()
        return question, answer, hint

    def add_question(self, question_id, difficulty, category, question, answer, hint):
        """
        Add a new trivia question to an SQLite database.

        :param question_id: the 4-digit identification number of the question to add.
        :param difficulty: the difficulty level of the question to add.
        :param category: the category of the question to add.
        :param question: the trivia question to add.
        :param answer: the correct answer to the trivia question.
        :param hint: a hint for the trivia question.
        """
        cursor = self._db.cursor()
        cursor.execute("INSERT INTO questions (question_id, dificulty, category, question, answer, hint) VALUES (?,?,?,?,?,?)", (question_id, difficulty, category, question, answer, hint))
        self._db.commit()
