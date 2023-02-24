from abc import ABC, abstractmethod
import random


class QuestionAndAnswer(ABC):
    """Abstract base class representing a question and answer.

    Attributes:
        question: (str) The question.
        correct_answer: (str) The correct answer to the question.
        category: (str) The category of the question.
    """

    def __init__(self, question, correct_answer, category):
        self.question = question
        self.correct_answer = correct_answer
        self.category = category

    def __hash__(self):
        """Compute the hash value based on the question, correct answer, and category"""
        return hash((self.question, self.correct_answer, self.category))

    @abstractmethod
    def get_hint(self):
        """Get a hint for the question.
        :return: (str) A hint for the question.
        """

    @abstractmethod
    def answer_is_correct(self, user_answer):
        """Check if the user's answer is correct.
        :param user_answer: (str) The user's answer.
        :return: (bool) True if the user's answer is correct, False otherwise.
        """
        return user_answer.lower() == self.correct_answer.lower()


class TrueOrFalseQA(QuestionAndAnswer):
    """Represents a true or false question and answer."""

    def __init__(self, question, correct_answer, category, option_1, option_2):
        """
        :param question: (str) The question.
        :param correct_answer: (str) The correct answer to the question.
        :param category: (str) The category of the question.
        :param option_1: (str) The first (True) choice for the user to choose from.
        :param option_2: (str) The second (False) choice for the user to choose from.
        """
        super().__init__(question, correct_answer, category)
        self.option_1 = option_1
        self.option_2 = option_2

        self.is_true = correct_answer.lower() == "true"

    def __hash__(self):
        return hash(
            (self.question, self.correct_answer, self.category, self.is_true)
        )

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
        super().__init__(question, correct_answer, category)
        self.option_1 = option_1
        self.option_2 = option_2
        self.option_3 = option_3
        self.option_4 = option_4

    def __hash__(self):
        return hash(
            (
                self.question,
                self.correct_answer,
                self.category,
                self.option_1,
                self.option_2,
                self.option_3,
                self.option_4,
            )
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
            o
            for o in [
                self.option_1,
                self.option_2,
                self.option_3,
                self.option_4,
            ]
            if o != self.correct_answer
        ]
        hint += "- " + incorrect_options[0] + "\n"
        hint += "- " + incorrect_options[1] + "\n"
        return hint


class ShortAnswerQA(HintableQuestionAndAnswer):
    """Represents a short answer question and answer."""

    def __hash__(self):
        return hash((self.question, self.correct_answer, self.category))

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


# TODO: Remove all useful content below here and put inside unit tests
# sample testing code
if __name__ == "__main__":
    # create an instance of each subclass and test the methods
    t = TrueOrFalseQA(
        "Do computers run on software?", "True", "General CS", "True", "False"
    )
    print(t.get_hint())
    print(t.answer_is_correct("True"))
    print("***** break *****")
    m = MultipleChoiceQA(
        "Which is NOT part of MVC?",
        "Database",
        "Design Patterns",
        "Model",
        "View",
        "Controller",
        "Database",
    )
    print(m.get_hint())
    print(m.answer_is_correct("Database"))
    print("***** break *****")
    s = ShortAnswerQA(
        "What does OOP stand for?",
        "Object-Oriented Programming",
        "Object-Oriented Programming",
    )
    print(s.get_hint())
    print(s.answer_is_correct("Programming"))
    print("***** break *****")

    # Test hashing for TrueOrFalseQA
    q1 = TrueOrFalseQA(
        "Are computers electronic?", "True", "General CS", "True", "False"
    )
    q2 = TrueOrFalseQA(
        "Are computers made of cheese?", "False", "General CS", "True", "False"
    )
    q3 = TrueOrFalseQA(
        "Where home computers invented in 1492?",
        "False",
        "General CS",
        "True",
        "False",
    )
    q4 = TrueOrFalseQA(
        "Are computers electronic?", "True", "General CS", "True", "False"
    )

    # Test if q1 and q4 have the same hash, but different hashes from q2 and q3
    assert hash(q1) == hash(q4)
    assert hash(q1) != hash(q2)
    assert hash(q1) != hash(q3)
    assert hash(q2) != hash(q3)

    hash1 = hash(q1)
    hash2 = hash(q2)
    hash3 = hash(q3)
    hash4 = hash(q4)

    print("Hash value of q1:", hash1)
    print("Hash value of q2:", hash2)
    print("Hash value of q3:", hash3)
    print("Hash value of q4:", hash4)

    if hash1 == hash2:
        print("hash(q1) == hash(q2)")
    else:
        print("hash(q1) != hash(q2)")

    if hash1 == hash4:
        print("hash(q1) == hash(q4)")
    else:
        print("hash(q1) != hash(q4)")
    print("***** break *****")

    # Test hashing for MultipleChoiceQA
    q1 = MultipleChoiceQA(
        "What does the R in RAM stand for?",
        "Random",
        "General CS",
        "Random",
        "Rye",
        "Robot",
        "Ruby",
    )
    q2 = MultipleChoiceQA(
        "What does the A in RAM stand for?",
        "Access",
        "General CS",
        "Aardvark",
        "Access",
        "Area",
        "Aliens",
    )
    q3 = MultipleChoiceQA(
        "What does the M in RAM stand for?",
        "Memory",
        "General CS",
        "Martian",
        "Money",
        "Machine",
        "Memory",
    )
    q4 = MultipleChoiceQA(
        "What does the R in RAM stand for?",
        "Random",
        "General CS",
        "Random",
        "Rye",
        "Robot",
        "Ruby",
    )

    # Test if q1 and q4 have the same hash, but different hashes from q2 and q3
    assert hash(q1) == hash(q4)
    assert hash(q1) != hash(q2)
    assert hash(q1) != hash(q3)
    assert hash(q2) != hash(q3)

    hash1 = hash(q1)
    hash2 = hash(q2)
    hash3 = hash(q3)
    hash4 = hash(q4)

    print("Hash value of q1:", hash1)
    print("Hash value of q2:", hash2)
    print("Hash value of q3:", hash3)
    print("Hash value of q4:", hash4)

    if hash1 == hash2:
        print("hash(q1) == hash(q2)")
    else:
        print("hash(q1) != hash(q2)")

    if hash1 == hash4:
        print("hash(q1) == hash(q4)")
    else:
        print("hash(q1) != hash(q4)")
    print("***** break *****")

    # Test hashing for ShortAnswerQA
    q1 = ShortAnswerQA(
        "What does the M in MVC stand for?", "Model", "Design Patterns"
    )
    q2 = ShortAnswerQA(
        "What does the V in MVC stand for?", "View", "Design Patterns"
    )
    q3 = ShortAnswerQA(
        "What does the C in MVC stand for?", "Controller", "Design Patterns"
    )
    q4 = ShortAnswerQA(
        "What does the M in MVC stand for?", "Model", "Design Patterns"
    )

    # Test if q1 and q4 have the same hash, but different hashes from q2 and q3
    assert hash(q1) == hash(q4)
    assert hash(q1) != hash(q2)
    assert hash(q1) != hash(q3)
    assert hash(q2) != hash(q3)

    hash1 = hash(q1)
    hash2 = hash(q2)
    hash3 = hash(q3)
    hash4 = hash(q4)

    print("Hash value of q1:", hash1)
    print("Hash value of q2:", hash2)
    print("Hash value of q3:", hash3)
    print("Hash value of q4:", hash4)

    if hash1 == hash2:
        print("hash(q1) == hash(q2)")
    else:
        print("hash(q1) != hash(q2)")

    if hash1 == hash4:
        print("hash(q1) == hash(q4)")
    else:
        print("hash(q1) != hash(q4)")
    print("***** break *****")
