"""Contains the Door class"""


class Door:
    """
    This class represents a single door for a single room. A Door will store
    a QuestionAndAnswer object.

    Attributes
    ----------
    question_and_answer : QuestionAndAnswer
        Reference to the QuestionAndAnswer class
    locked : bool
        The locked state of a Door. True for locked, False for unlocked.
    perm_locked : bool
        If QuestionAndAnswer receives wrong answer door becomes permanently locked.
    """

    def __init__(self, locked=True):
        self.locked = locked
        self.perm_locked = False
        self.question_and_answer = None
