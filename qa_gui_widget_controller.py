from typing import List
from trivia_maze_model_observer import TriviaMazeModelObserver
from adventurer import Adventurer
from question_and_answer import *
from qa_gui_widget_view import QAGUIWidgetView


class QAGUIWidgetController:
    """
    This class represents the controller of the Trivia Maze game.

    Attributes:
        model (TriviaMazeModelObserver): The model that the controller interacts with.
        view (QAGUIWidgetView): The view that the controller interacts with.
        adventurer (Adventurer): The adventurer in the game.
        question_number (int): The number of the current question.
        questions (List[Question]): The list of questions to be asked in the game.

    Methods:
        set_view(view: QAGUIWidgetView): Sets the view that the controller interacts with.
        set_model(model: TriviaMazeModelObserver): Sets the model that the controller interacts with.
        set_adventurer(adventurer: Adventurer): Sets the adventurer in the game.
        set_questions(questions: List[Question]): Sets the list of questions to be asked in the game.
        start_game(): Starts the game.
        display_question(question: Question): Displays the current question.
        handle_input(input: str): Handles input from the view.
        check_answer(answer: str): Checks the player's answer against the correct answer.
        show_feedback(is_correct: bool): Shows feedback to the player based on whether their answer is correct or not.
    """

    def __init__(self):
        """
        Initializes a QAGUIWidgetController object.
        """
        self.model = None
        self.view = None
        self.adventurer = None
        self.question_number = 0
        self.questions = []

    def set_view(self, view: QAGUIWidgetView):
        """
        Sets the view that the controller interacts with.

        Args:
            view (QAGUIWidgetView): The view that the controller interacts with.
        """
        self.view = view

    def set_model(self, model: TriviaMazeModelObserver):
        """
        Sets the model that the controller interacts with.

        Args:
            model (TriviaMazeModelObserver): The model that the controller interacts with.
        """
        self.model = model

    def set_adventurer(self, adventurer: Adventurer):
        """
        Sets the adventurer in the game.

        Args:
            adventurer (Adventurer): The adventurer in the game.
        """
        self.adventurer = adventurer

    def set_questions(self, questions: List[QuestionAndAnswer]):
        """
        Sets the list of questions to be asked in the game.

        Args:
            questions (List[Question]): The list of questions to be asked in the game.
        """
        self.questions = questions

    def start_game(self):
        """
        Starts the game.
        """
        self.question_number = 0
        self.display_question(self.questions[self.question_number])

    def display_question(self, question: QuestionAndAnswer):
        """
        Displays the current question.

        Args:
            question (Question): The current question to display.
        """
        self.view.show_question(question.text)
        if question.type == QuestionAndAnswer.TrueOrFalseQA:
            self.view.show_true_false_choices()
        elif question.type == QuestionAndAnswer.MultipleChoiceQA:
            self.view.show_multiple_option_options(question.options)
        else:
            self.view.hide_options()
        self.view.show_input_field()

    def handle_input(self, input: str):
        """
        Handles input from the view.

        Args:
            input (str): The input from the view.
        """
        self.check_answer(input)

    def submit_answer(self, answer: str):
        """
        Submits an answer to a question to the model.

        Args:
            answer (str): The answer to be submitted.
        """
        if self.model.check_answer(answer):
            self.view.show_message("Correct!")
            self.model.unlock_door()
        else:
            self.view.show_message("Incorrect!")
        self.view.return_to_game()
