from abc import abstractmethod
from maze_items import SuggestionPotion
from question_and_answer import MultipleChoiceQA, ShortAnswerQA, TrueOrFalseQA
from trivia_maze_model_observer import TriviaMazeModelObserver
from text_trivia_maze_view import TextTriviaMazeView

from command_context import (
    IN_GAME_MENU_KEY,
    DISMISS_KEYS,
    USE_SUGGESTION_POTION_KEY,
)
from command_context import (
    MainMenuCommandContext,
    MainHelpMenuCommandContext,
    NoSaveFileFoundMenuCommandContext,
    PrimaryInterfaceCommandContext,
    InGameMenuCommandContext,
    MapLegendCommandContext,
    CommandLegendCommandContext,
    SaveConfirmationCommandContext,
    GameWonCommandContext,
    GameLostDiedCommandContext,
    GameLostTrappedCommandContext,
    TrueOrFalseQuestionAndAnswerCommandContext,
    MultipleChoiceQuestionAndAnswerCommandContext,
    ShortQuestionAndAnswerCommandContext,
    MagicKeyCommandContext,
    NeedMagicKeyCommandContext,
)


class TriviaMazeController(TriviaMazeModelObserver):
    @abstractmethod
    def process_keystroke(self, key):
        """
        Takes a keyboard input and interprets it as a command to be issued to
        the model or view which is then called as appropriate.
        """

    @abstractmethod
    def start_main_event_loop(self):
        """
        Display main menu and start listening for input from user
        """


class TextTriviaMazeController(TriviaMazeController):
    """
    Controls view and model based on keyboard input received by the view, as
    well as potentially information exposed by the model (e.g. if the model
    has a question and answer to be asked, the controller has the view ask it
    and get an answer.)
    """

    def __init__(self, maze_model):
        super().__init__(maze_model)

        # Create view and do initial configuration based on recognized keystrokes
        self.__maze_view = TextTriviaMazeView(
            maze_model, self, "Trivia Maze", DISMISS_KEYS
        )

        self.__maze_view.populate_menu_access_label(
            f"Press <{IN_GAME_MENU_KEY}> to access the in-game menu"
        )

        # Initialize command interpretation contexts
        self.__main_menu_context = MainMenuCommandContext(
            self, self._maze_model, self.__maze_view
        )
        self.__no_save_file_found_menu_context = (
            NoSaveFileFoundMenuCommandContext(
                self, self._maze_model, self.__maze_view
            )
        )
        self.__main_help_menu_context = MainHelpMenuCommandContext(
            self, self._maze_model, self.__maze_view
        )
        self.__primary_interface_context = PrimaryInterfaceCommandContext(
            self, self._maze_model, self.__maze_view
        )
        self.__in_game_menu_context = InGameMenuCommandContext(
            self, self._maze_model, self.__maze_view
        )
        self.__map_legend_menu_context = MapLegendCommandContext(
            self, self._maze_model, self.__maze_view
        )
        self.__command_legend_menu_context = CommandLegendCommandContext(
            self, self._maze_model, self.__maze_view
        )
        self.__save_confirmation_menu_context = SaveConfirmationCommandContext(
            self, self._maze_model, self.__maze_view
        )
        self.__game_won_menu_context = GameWonCommandContext(
            self, self._maze_model, self.__maze_view
        )
        self.__game_lost_died_menu_context = GameLostDiedCommandContext(
            self, self._maze_model, self.__maze_view
        )
        self.__game_lost_trapped_menu_context = GameLostTrappedCommandContext(
            self, self._maze_model, self.__maze_view
        )
        self.__short_QA_context = ShortQuestionAndAnswerCommandContext(
            self, self._maze_model, self.__maze_view
        )
        self.__true_or_false_QA_context = (
            TrueOrFalseQuestionAndAnswerCommandContext(
                self, self._maze_model, self.__maze_view
            )
        )
        self.__multiple_choice_QA_context = (
            MultipleChoiceQuestionAndAnswerCommandContext(
                self, self._maze_model, self.__maze_view
            )
        )
        self.__magic_key_context = MagicKeyCommandContext(
            self, self._maze_model, self.__maze_view
        )
        self.__need_magic_key_context = NeedMagicKeyCommandContext(
            self, self._maze_model, self.__maze_view
        )

        # Initialize question and answer (used between different command
        # contexts) attr
        self.question_and_answer = None

        # Player starts out at the main menu, so make that the active context.
        # NOTE: This sets the `__active_context` instance attr
        self.set_active_context("main_menu")

    def start_main_event_loop(self):
        self.__maze_view.mainloop()

    def process_keystroke(self, key):
        self.__active_context.process_keystroke(key)

    def get_active_context(self):
        return self.__active_context

    def set_active_context(self, context_specifier):
        contexts = {
            "main_menu": self.__main_menu_context,
            "no_save_file_found_menu": self.__no_save_file_found_menu_context,
            "main_help_menu": self.__main_help_menu_context,
            "primary_interface": self.__primary_interface_context,
            "in_game_menu": self.__in_game_menu_context,
            "map_legend_menu": self.__map_legend_menu_context,
            "command_legend_menu": self.__command_legend_menu_context,
            "save_confirmation_menu": self.__save_confirmation_menu_context,
            "game_won_menu": self.__game_won_menu_context,
            "game_lost_died_menu": self.__game_lost_died_menu_context,
            "game_lost_trapped_menu": self.__game_lost_trapped_menu_context,
            "short_QA_menu": self.__short_QA_context,
            "true_or_false_QA_menu": self.__true_or_false_QA_context,
            "multiple_choice_QA_menu": self.__multiple_choice_QA_context,
            "magic_key": self.__magic_key_context,
            "need_magic_key": self.__need_magic_key_context,
        }
        self.__active_context = contexts[context_specifier]

    def update(self):
        """Observer response method to model changes."""
        # Check if game is over
        game_status = self._maze_model.game_status()
        if game_status == "died":
            self.__maze_view.show_game_lost_died_menu()
            self.set_active_context("game_lost_died_menu")
            return
        elif game_status == "trapped":
            self.__maze_view.show_game_lost_trapped_menu()
            self.set_active_context("game_lost_trapped_menu")
            return
        elif game_status == "win":
            self.__maze_view.show_game_won_menu()
            self.set_active_context("game_won_menu")
            return

        # If game still ongoing, check if there is a new Q&A to pose to the
        # user
        if self.__active_context == self.__primary_interface_context:
            self.__process_question_and_answer_buffer()

    def __process_question_and_answer_buffer(self):
        """If the model put a QuestionAndAnswer object in its corresponding
        buffer, tell the view to pose it to the user and switch to the
        appropriate command context to get their answer (and, if applicable,
        allow them to use a suggestion potion)."""
        self.question_and_answer = (
            self._maze_model.flush_question_and_answer_buffer()
        )
        if self.question_and_answer:
            if isinstance(self.question_and_answer, ShortAnswerQA):
                self.__maze_view.set_short_QA_question(
                    self.question_and_answer.question,
                )

                self.__maze_view.set_short_QA_hint(
                    self.__get_initial_hint_content()
                )

                self.__maze_view.show_short_QA_menu()
                self.set_active_context("short_QA_menu")

            elif isinstance(self.question_and_answer, TrueOrFalseQA):
                self.__maze_view.set_true_or_false_QA_question(
                    self.question_and_answer.question,
                )
                self.__maze_view.set_true_or_false_QA_options(
                    self.__create_options_for_true_false()
                )

                self.__maze_view.show_true_or_false_QA_menu()
                self.set_active_context("true_or_false_QA_menu")

            elif isinstance(self.question_and_answer, MultipleChoiceQA):
                self.__maze_view.set_multiple_choice_QA_question(
                    self.question_and_answer.question,
                )

                self.__maze_view.set_multiple_choice_QA_options(
                    self.__create_options_for_multiple_choice(
                        self.question_and_answer.options
                    )
                )

                self.__maze_view.set_multiple_choice_QA_hint(
                    self.__get_initial_hint_content()
                )

                self.__maze_view.show_multiple_choice_QA_menu()
                self.set_active_context("multiple_choice_QA_menu")

    def __get_initial_hint_content(self):
        """Determine whether to show the hint label for a hintable Q&A
        component and, if so, what its contents should be.

        Returns
        -------
        str
            The content to place in the hint label of a hintable Q&A widget.
        """

        num_suggestion_potions = self.__get_num_suggestion_potions()
        if num_suggestion_potions > 0:
            return (
                f"To see a hint, press <{USE_SUGGESTION_POTION_KEY}> to use one of your "
                f"{num_suggestion_potions} suggestion potions."
            )

    def __get_num_suggestion_potions(self):
        """Get number of suggestion potions held by adventurer from
        model.

        Returns
        -------
        int
            The number of suggestion potions the adventurer has.
        """
        adventurer_items = self._maze_model.get_adventurer_items()

        # If user has at least one suggestion potion, show hint box
        return sum(
            isinstance(item, SuggestionPotion) for item in adventurer_items
        )

    @staticmethod
    def __create_options_for_true_false():
        """
        Generate the options for a T/F question.

        Returns
        -------
        list
            List of strings
        """
        return ["<T> True", "<F> False"]

    @staticmethod
    def __create_options_for_multiple_choice(options):
        """
        Generate the options for a multiple choice question.

        Returns
        -------
        list
            List of strings
        """
        options_with_prefixes = []
        ind_to_letter = {0: "A", 1: "B", 2: "C", 3: "D"}

        for ind, option in enumerate(options):
            options_with_prefixes.append(f"<{ind_to_letter[ind]}> {option}")

        return options_with_prefixes
