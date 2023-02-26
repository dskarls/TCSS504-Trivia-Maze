"""Contains the Door class"""


class Door:
    """
    This class represents a single door for a single room. A Door may store a
    QuestionAndAnswer object.

    Attributes
    ----------
    question_and_answer : QuestionAndAnswer
        An object representing a question and answer.
    locked : bool
        The locked state of a Door. True for locked, False for unlocked.
    perm_locked : bool
        If QuestionAndAnswer receives wrong answer door becomes permanently locked.
    """

    def __init__(self, question_and_answer=None):
        self.question_and_answer = question_and_answer
        self.locked = True if question_and_answer else False
        self.perm_locked = False
