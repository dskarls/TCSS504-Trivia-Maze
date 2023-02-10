"""Contains the Door class"""
    
class Door:
    """
    This class represents a single door for a single room. A Door will store
    a QuestionAndAnswer object.
    
    Attributes
    ----------
    question_and_answer : QuestionAndAnswer
        Reference to the QuestionAndAnswer class
    __locked : bool
        The locked state of a Door. True for locked, False for unlocked.
    perm_locked : bool
        If QuestionAndAnswer recieves wrong answer door becomes permanently locked.
    """
    
    def __init__(self, locked=True):
        self.__locked = locked
        self.perm_locked = False
        self.question_and_answer = None
    
    @property
    def locked(self):
        """
        The locked state of a Door. True for locked, False for unlocked.
        
        Returns
        -------
        bool
            True if the door is locked, False otherwise.
        """
        return self.__locked
    
    
    @locked.setter
    def locked(self, state):
        """Sets the lock state of the Door"""
        self.__locked = state
