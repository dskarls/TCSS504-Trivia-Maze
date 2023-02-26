from abc import ABC, abstractmethod
import random


class InvalidQuestionAndAnswerType(ValueError):
    """An invalid question type was used to try to instantiate a concrete
    QuestionAndAnswer object."""


class QuestionAndAnswer(ABC):
    """Abstract base class representing a question and answer.

    Attributes:
        question: (str) The question.
        correct_answer: (str) The correct answer to the question.
        category: (str) The category of the question.
        options : (list) The options for the user to choose from (may be None).
    """

    def __init__(self, question, correct_answer, category, options):
        self.question = question
        self.correct_answer = correct_answer
        self.category = category
        self.options = options

    def __hash__(self):
        """Compute the hash value based on its (globally unique) question content"""
        return hash(self.question)

    @abstractmethod
    def answer_is_correct(self, user_answer):
        """Check if the user's answer is correct.
        :param user_answer: (str) The user's answer.
        :return: (bool) True if the user's answer is correct, False otherwise.
        """
        return user_answer.lower() == self.correct_answer.lower()


class TrueOrFalseQA(QuestionAndAnswer):
    """Represents a true or false question and answer."""

    def __init__(self, question, correct_answer, category):
        """
        :param question: (str) The question.
        :param correct_answer: (str) The correct answer to the question.
        :param category: (str) The category of the question.
        """
        super().__init__(question, correct_answer, category, ["True", "False"])

    def answer_is_correct(self, user_answer):
        """Check if the user's answer is correct.
        :param user_answer: (str) The user's answer.
        :return: (bool) True if the user's answer is correct, False otherwise.
        """
        return user_answer.lower() == self.correct_answer.lower()


class HintableQuestionAndAnswer(QuestionAndAnswer):
    """A question and answer that provides a method for getting a hint of the
    correct answer."""

    @abstractmethod
    def get_hint(self):
        """Get a hint for the question.
        :return: (str) A hint for the question.
        """


class MultipleChoiceQA(HintableQuestionAndAnswer):
    """Represents a multiple choice question and answer."""

    def __init__(
        self,
        question,
        correct_answer,
        category,
        option_1,
        option_2,
        option_3,
        option_4,
    ):
        """
        :param question (str): The question.
        :param correct_answer (str): The correct answer to the question.
        :param category (str): The category of the question.
        :param option_1 (str): The first of the list of choices for the user to choose from.
        :param option_2 (str): The second of the list of choices for the user to choose from.
        :param option_3 (str): The third of the list of choices for the user to choose from.
        :param option_4 (str): The fourth of the list of choices for the user to choose from.
        """
        super().__init__(
            question,
            correct_answer,
            category,
            [option_1, option_2, option_3, option_4],
        )

    def answer_is_correct(self, user_answer):
        """Check if the user's answer is correct.
        :param user_answer: (str) The user's answer.
        :return: (bool) True if the user's answer is correct, False otherwise.
        """
        return user_answer.lower() == self.correct_answer.lower()

    def get_hint(self):
        """
        Get a hint for the question.
        :return: (str) A hint for the question.
        """
        hint = "The correct answer is NOT one of the following choices: \n"
        incorrect_options = [
            o for o in self.options if o != self.correct_answer
        ]
        hint += "- " + incorrect_options[0] + "\n"
        hint += "- " + incorrect_options[1] + "\n"
        return hint


class ShortAnswerQA(HintableQuestionAndAnswer):
    """Represents a short answer question and answer."""

    def answer_is_correct(self, user_answer):
        """Check if the user's answer is correct.
        :param user_answer: (str) The user's answer.
        :return: (bool) True if the user's answer is correct, False otherwise.
        """
        return user_answer.lower() == self.correct_answer.lower()

    def get_hint(self):
        """
        Get a hint for the question.
        :return: (str) A hint for the question.
        """
        hint = "Hint: "
        words = self.correct_answer.split()
        num_words = len(words)

        # Randomly decide which letters of the correct answer to expose
        for i in range(num_words):
            word = words[i]
            length = len(word)
            num_letters_to_show = (
                length // 2 if length % 2 == 0 else length // 2 + 1
            )
            indices_to_show = random.sample(range(length), num_letters_to_show)
            indices_to_show.sort()
            prev_index = -1
            for index in indices_to_show:
                if prev_index + 1 != index:
                    hint += " "
                hint += word[index]
                prev_index = index
            if i < num_words - 1:
                hint += " "
        return hint


def question_and_answer_factory(
    qa_type,
    category,
    question,
    correct_answer,
    option_1,
    option_2,
    option_3,
    option_4,
):
    """
    Construct an appropriate QuestionAndAnswer object based on strings related
    to its attributes.
    """
    qa_type = qa_type.lower()
    if qa_type == "true or false":
        return TrueOrFalseQA(question, correct_answer, category)
    elif qa_type == "multiple choice":
        return MultipleChoiceQA(
            question,
            correct_answer,
            category,
            option_1,
            option_2,
            option_3,
            option_4,
        )
    elif qa_type == "short answer":
        return ShortAnswerQA(question, correct_answer, category, options=None)

    raise InvalidQuestionAndAnswerType("")
