"""Contains the Door class"""
import random
    
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
    __perm_locked : bool
        If QuestionAndAnswer recieves wrong answer door becomes permanently locked.
    """
    
    def __init__(self, locked=True):
        self.__locked = locked
        self.__perm_locked = False
        self.question_and_answer = None #QuestionAndAnswer() 
    
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
    
    @property
    def perm_locked(self):
        """
        Door can become permanently locked via answering a trivia
        question incorrectly. It is possible to change this state
        via a MagicKey MazeItem.
        
        Returns
        -------
        bool
            True if the door is permanently locked, False otherwise.
        """
        return self.__perm_locked
    
    @locked.setter
    def locked(self, state):
        """Sets the lock state for a Door"""
        self.__locked = state
    
    @perm_locked.setter
    def perm_locked(self, state):
        """Sets the permanently locked state for a Door"""
        self.__perm_locked = state
    
    
