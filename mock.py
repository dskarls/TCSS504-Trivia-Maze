class QuestionAndAnswer:
    def __init__(self, question, question_type, hint, options, answer):
        self.question = question
        self.question_type = question_type
        self.hint = hint
        self.options = options
        self.__answer = answer

    def answer_is_correct(self, user_answer):
        return user_answer.lower() == self.__answer.lower()


class TextTriviaMazeModel:
    def save_game(self):
        pass

    def load_game(self):
        pass

    def get_rooms(self):
        pass

    def get_adventurer_hp(self):
        pass

    def move_adventurer(self, direction):
        pass

    def use_item(self, item_name):
        # NOTE: This should return False or None if the user did not hold any
        # of the item
        pass

    def register_observer(self):
        pass

    def reset(self):
        pass
