from abc import ABC, abstractmethod
from enum import Enum, auto
from maze_items import SuggestionPotion

from trivia_maze import SaveGameFileNotFound

_COMMAND_DESC_KEY = "description"
_COMMAND_KEY_KEY = "key"
_COMMAND_TYPE = "type"
_COMMAND_TYPE_OTHER = "other"
_COMMAND_TYPE_ITEM = "item"
_COMMAND_TYPE_MOVEMENT = "movement"


class CommandContext(ABC):
    """
    Interprets keystrokes within a specific context. For example, one context
    might be the main menu while one could be the primary game interface.
    """

    def __init__(self, maze_controller, maze_model, maze_view):
        self._maze_controller = maze_controller
        self._maze_model = maze_model
        self._maze_view = maze_view

    def __init_subclass__(cls, *args, **kwargs):
        """Force all subclasses to define a COMMANDS class attr"""
        super().__init_subclass__(*args, **kwargs)
        required_attrs = ("Command", "COMMANDS")
        for attr in required_attrs:
            if not hasattr(cls, attr):
                raise TypeError(
                    f"Subclasses of must define the {attr} class attr"
                )

    @abstractmethod
    def process_keystroke(self, key):
        """Interpret a keystroke and perform the relevant actions on the model
        and view based on the current context."""


class MenuCommandContext(CommandContext):
    class Command(Enum):
        """Enumeration used to fix commands to a small finite support set."""

        SELECT = auto()

    COMMANDS = {
        # Movement commands
        Command.SELECT: {
            _COMMAND_TYPE: _COMMAND_TYPE_OTHER,
            _COMMAND_DESC_KEY: "Select",
            _COMMAND_KEY_KEY: "Return",
        }
    }


class MainMenuCommandContext(MenuCommandContext):
    def process_keystroke(self, key):
        # NOTE: We ignore arrow keys here since the GUI is responsible for
        # having arrow keys traverse the menu. In fact, we actually only care
        # about the user hitting Return inside of this menu.
        if key != self.COMMANDS[self.Command.SELECT][_COMMAND_KEY_KEY]:
            return

        # Trigger the currently selected item in the main menu
        selected_option = (
            self._maze_view.get_main_menu_current_selection().lower()
        )

        # NOTE: One might choose to have the controller tell the view what options
        # to add to the menu when it creates it in order to avoid duplication
        if selected_option == "start game":
            # FIXME: Implement a difficulty selection and/or adventurer naming
            # menu and have the user go through that here. This may mean we
            # need to break up the stuff in the model's initialization so that
            # its __init__ doesn't really do anything.

            # Hide main menu so user can begin playing and switch contexts
            self._maze_model.reset()
            self._maze_view.reset_inventories()
            self._maze_view.hide_main_menu()

            # Clear view event log
            self._maze_view.clear_event_log()

            self._maze_controller.set_active_context("primary_interface")

        elif selected_option == "load game":
            try:
                self._maze_model.load_game()
                self._maze_view.hide_main_menu()

                # Clear view event log
                self._maze_view.clear_event_log()

                self._maze_controller.set_active_context("primary_interface")
            except SaveGameFileNotFound:
                self._maze_view.show_no_save_file_found_menu()
                self._maze_controller.set_active_context(
                    "no_save_file_found_menu"
                )

        elif selected_option == "help":
            self._maze_view.show_main_help_menu()
            self._maze_controller.set_active_context("main_help_menu")

        elif selected_option == "quit game":
            # Exit out of everything and close the window
            self._maze_view.quit_entire_game()


class InGameMenuCommandContext(MenuCommandContext):
    def process_keystroke(self, key):
        # NOTE: We ignore arrow keys here since the GUI is responsible for
        # having arrow keys traverse the menu. In fact, we actually only care
        # about the user hitting Return inside of this menu.
        if key != self.COMMANDS[self.Command.SELECT][_COMMAND_KEY_KEY]:
            return

        # Trigger the currently selected item in the main menu
        selected_option = (
            self._maze_view.get_in_game_menu_current_selection().lower()
        )

        # NOTE: One might choose to have the controller tell the view what options
        # to add to the menu when it creates it in order to avoid duplication
        if selected_option == "back to game":
            self._maze_view.hide_in_game_menu()
            self._maze_controller.set_active_context("primary_interface")

        elif selected_option == "display map legend":
            self._maze_view.show_map_legend_menu()
            self._maze_controller.set_active_context("map_legend_menu")

        elif selected_option == "display commands":
            # Generate legend symbols/descriptions to display
            symbols = tuple(
                entry[_COMMAND_KEY_KEY]
                for entry in PrimaryInterfaceCommandContext.COMMANDS.values()
            )
            descriptions = tuple(
                entry[_COMMAND_DESC_KEY]
                for entry in PrimaryInterfaceCommandContext.COMMANDS.values()
            )

            self._maze_view.show_command_legend_menu(
                symbols, descriptions, num_cols=2
            )
            self._maze_controller.set_active_context("command_legend_menu")

        elif selected_option == "save game":
            self._maze_model.save_game()
            self._maze_view.show_save_confirmation_menu()
            self._maze_controller.set_active_context("save_confirmation_menu")

        elif selected_option == "return to main menu":
            # Have the model create a completely new map and reset all item
            # counters to zero, etc.
            self._maze_model.reset()

            # Get rid of the in-game menu and put main menu over the top of the
            # reconstructed game
            self._maze_view.hide_in_game_menu()
            self._maze_view.show_main_menu()

            self._maze_controller.set_active_context("main_menu")

        elif selected_option == "quit game":
            # Exit out of everything and close the window
            self._maze_view.quit_entire_game()


class DismissibleCommandContext(CommandContext):
    class Command(Enum):
        """Enumeration used to fix commands to a small finite support set."""

        DISMISS = auto()

    COMMANDS = {
        # Movement commands
        Command.DISMISS: {
            _COMMAND_TYPE: _COMMAND_TYPE_OTHER,
            _COMMAND_DESC_KEY: "Dismiss",
            _COMMAND_KEY_KEY: "Return",
        }
    }


class NoSaveFileFoundMenuCommandContext(DismissibleCommandContext):
    def process_keystroke(self, key):
        if key == self.COMMANDS[self.Command.DISMISS][_COMMAND_KEY_KEY]:
            self._maze_view.hide_no_save_file_found_menu()
            self._maze_controller.set_active_context("main_menu")


class MainHelpMenuCommandContext(DismissibleCommandContext):
    def process_keystroke(self, key):
        if key == self.COMMANDS[self.Command.DISMISS][_COMMAND_KEY_KEY]:
            self._maze_view.hide_main_help_menu()
            self._maze_controller.set_active_context("main_menu")


class MapLegendCommandContext(DismissibleCommandContext):
    def process_keystroke(self, key):
        if key == self.COMMANDS[self.Command.DISMISS][_COMMAND_KEY_KEY]:
            self._maze_view.hide_map_legend_menu()
            self._maze_controller.set_active_context("in_game_menu")


class CommandLegendCommandContext(DismissibleCommandContext):
    def process_keystroke(self, key):
        if key == self.COMMANDS[self.Command.DISMISS][_COMMAND_KEY_KEY]:
            self._maze_view.hide_command_legend_menu()
            self._maze_controller.set_active_context("in_game_menu")


class SaveConfirmationCommandContext(DismissibleCommandContext):
    def process_keystroke(self, key):
        if key == self.COMMANDS[self.Command.DISMISS][_COMMAND_KEY_KEY]:
            self._maze_view.hide_save_confirmation_menu()
            self._maze_controller.set_active_context("in_game_menu")


class GameWonCommandContext(DismissibleCommandContext):
    def process_keystroke(self, key):
        if key == self.COMMANDS[self.Command.DISMISS][_COMMAND_KEY_KEY]:
            self._maze_view.hide_game_won_menu()
            self._maze_view.show_main_menu()
            self._maze_controller.set_active_context("main_menu")


class GameLostDiedCommandContext(DismissibleCommandContext):
    def process_keystroke(self, key):
        if key == self.COMMANDS[self.Command.DISMISS][_COMMAND_KEY_KEY]:
            self._maze_view.hide_game_lost_died_menu()
            self._maze_view.show_main_menu()
            self._maze_controller.set_active_context("main_menu")


class GameLostTrappedCommandContext(DismissibleCommandContext):
    def process_keystroke(self, key):
        if key == self.COMMANDS[self.Command.DISMISS][_COMMAND_KEY_KEY]:
            self._maze_view.hide_game_lost_trapped_menu()
            self._maze_view.show_main_menu()
            self._maze_controller.set_active_context("main_menu")


class NeedMagicKeyCommandContext(DismissibleCommandContext):
    def process_keystroke(self, key):
        if key == self.COMMANDS[self.Command.DISMISS][_COMMAND_KEY_KEY]:
            self._maze_view.hide_need_magic_key_menu()
            self._maze_controller.set_active_context("primary_interface")


class PrimaryInterfaceCommandContext(CommandContext):
    class Command(Enum):
        """Enumeration used to fix commands to a small finite support set."""

        # Movement commands
        MOVE_EAST = auto()
        MOVE_NORTH = auto()
        MOVE_WEST = auto()
        MOVE_SOUTH = auto()

        # Item commands
        USE_HEALING_POTION = auto()
        USE_VISION_POTION = auto()

        # Other commands
        SHOW_IN_GAME_MENU = auto()
        QUIT_GAME = auto()

    COMMANDS = {
        # Movement commands
        Command.MOVE_EAST: {
            _COMMAND_TYPE: _COMMAND_TYPE_MOVEMENT,
            _COMMAND_DESC_KEY: "Move east",
            _COMMAND_KEY_KEY: "Right",
        },
        Command.MOVE_NORTH: {
            _COMMAND_TYPE: _COMMAND_TYPE_MOVEMENT,
            _COMMAND_DESC_KEY: "Move north",
            _COMMAND_KEY_KEY: "Up",
        },
        Command.MOVE_WEST: {
            _COMMAND_TYPE: _COMMAND_TYPE_MOVEMENT,
            _COMMAND_DESC_KEY: "Move west",
            _COMMAND_KEY_KEY: "Left",
        },
        Command.MOVE_SOUTH: {
            _COMMAND_TYPE: _COMMAND_TYPE_MOVEMENT,
            _COMMAND_DESC_KEY: "Move south",
            _COMMAND_KEY_KEY: "Down",
        },
        # Item commands
        Command.USE_HEALING_POTION: {
            _COMMAND_TYPE: _COMMAND_TYPE_ITEM,
            _COMMAND_DESC_KEY: "Use healing potion",
            _COMMAND_KEY_KEY: "h",
        },
        Command.USE_VISION_POTION: {
            _COMMAND_TYPE: _COMMAND_TYPE_ITEM,
            _COMMAND_DESC_KEY: "Use vision potion",
            _COMMAND_KEY_KEY: "v",
        },
        # Other commands
        Command.SHOW_IN_GAME_MENU: {
            _COMMAND_TYPE: _COMMAND_TYPE_OTHER,
            _COMMAND_DESC_KEY: "Show in-game help menu",
            _COMMAND_KEY_KEY: "Escape",
        },
    }

    def process_keystroke(self, key):
        # Non-movement commands
        if (
            key
            == self.COMMANDS[self.Command.SHOW_IN_GAME_MENU][_COMMAND_KEY_KEY]
        ):
            self._maze_view.show_in_game_menu()
            self._maze_controller.set_active_context("in_game_menu")
        elif (
            key
            == self.COMMANDS[self.Command.USE_HEALING_POTION][_COMMAND_KEY_KEY]
        ):
            self._maze_model.use_item("healing potion")
        elif (
            key
            == self.COMMANDS[self.Command.USE_VISION_POTION][_COMMAND_KEY_KEY]
        ):
            self._maze_model.use_item("vision potion")
        else:
            # Movement commands
            KEY_TO_DIRECTION = {
                self.COMMANDS[self.Command.MOVE_WEST][
                    _COMMAND_KEY_KEY
                ]: "west",
                self.COMMANDS[self.Command.MOVE_EAST][
                    _COMMAND_KEY_KEY
                ]: "east",
                self.COMMANDS[self.Command.MOVE_NORTH][
                    _COMMAND_KEY_KEY
                ]: "north",
                self.COMMANDS[self.Command.MOVE_SOUTH][
                    _COMMAND_KEY_KEY
                ]: "south",
            }
            direction = KEY_TO_DIRECTION.get(key)

            if direction:
                # key was a movement command
                directive = self._maze_model.move_adventurer(direction)
                directive = directive.lower() if directive else None

                if directive == "use magic key":
                    self._maze_controller.set_active_context("magic_key")
                    self._maze_view.show_magic_key_menu()
                elif directive == "need magic key":
                    self._maze_controller.set_active_context("need_magic_key")
                    self._maze_view.show_need_magic_key_menu()


class ShortQuestionAndAnswerCommandContext(CommandContext):
    class Command(Enum):
        """Enumeration used to fix commands to a small finite support set."""

        # Item commands
        USE_SUGGESTION_POTION = auto()

        # Other commands
        SUBMIT_ANSWER = auto()

    COMMANDS = {
        # Item commands
        Command.USE_SUGGESTION_POTION: {
            _COMMAND_TYPE: _COMMAND_TYPE_ITEM,
            _COMMAND_DESC_KEY: "Use suggestion potion",
            _COMMAND_KEY_KEY: "F1",
        },
        # Other commands
        Command.SUBMIT_ANSWER: {
            _COMMAND_TYPE: _COMMAND_TYPE_OTHER,
            _COMMAND_DESC_KEY: "Submit answer",
            _COMMAND_KEY_KEY: "Return",
        },
    }

    def process_keystroke(self, key):
        # Retrieve Q&A object held by controller
        question_and_answer = self._maze_controller.question_and_answer

        if key == self.COMMANDS[self.Command.SUBMIT_ANSWER][_COMMAND_KEY_KEY]:
            # Take question and answer object from controller
            self._maze_controller.question_and_answer = None

            user_answer = self._maze_view.get_short_QA_user_answer()
            user_answer_correct = question_and_answer.answer_is_correct(
                user_answer
            )
            # Hide Q&A widget
            self._maze_view.hide_short_QA_menu()
            self._maze_view.clear_short_QA_user_answer()

            # Return command interpretation to primary interface
            self._maze_controller.set_active_context("primary_interface")

            # Inform the model
            # NOTE: This will cause the model to update its observers
            self._maze_model.inform_player_answer_correct_or_incorrect(
                user_answer_correct
            )

        elif (
            key
            == self.COMMANDS[self.Command.USE_SUGGESTION_POTION][
                _COMMAND_KEY_KEY
            ]
        ):
            # If user has at least one suggestion potion, use it
            adventurer_items = self._maze_model.get_adventurer_items()
            num_suggestion_potions = sum(
                isinstance(x, SuggestionPotion) for x in adventurer_items
            )
            if num_suggestion_potions > 0:
                self._maze_model.use_item("suggestion potion")
                self._maze_view.set_short_QA_hint(
                    question_and_answer.get_hint()
                )


class TrueOrFalseQuestionAndAnswerCommandContext(CommandContext):
    class Command(Enum):
        """Enumeration used to fix commands to a small finite support set."""

        # Answer selection commands
        SELECT_TRUE = auto()
        SELECT_FALSE = auto()

        # Other commands
        SUBMIT_ANSWER = auto()

    COMMANDS = {
        # Item commands
        Command.SELECT_TRUE: {
            _COMMAND_TYPE: _COMMAND_TYPE_OTHER,
            _COMMAND_DESC_KEY: "Select True",
            _COMMAND_KEY_KEY: "t",
        },
        Command.SELECT_FALSE: {
            _COMMAND_TYPE: _COMMAND_TYPE_OTHER,
            _COMMAND_DESC_KEY: "Select False",
            _COMMAND_KEY_KEY: "f",
        },
        # Other commands
        Command.SUBMIT_ANSWER: {
            _COMMAND_TYPE: _COMMAND_TYPE_OTHER,
            _COMMAND_DESC_KEY: "Submit answer",
            _COMMAND_KEY_KEY: "Return",
        },
    }

    def process_keystroke(self, key):
        if key == self.COMMANDS[self.Command.SUBMIT_ANSWER][_COMMAND_KEY_KEY]:
            # Take question and answer object from controller
            question_and_answer = self._maze_controller.question_and_answer
            self._maze_controller.question_and_answer = None

            user_answer = self._maze_view.get_true_or_false_QA_user_answer()
            user_answer_correct = question_and_answer.answer_is_correct(
                user_answer
            )

            # Hide Q&A widget
            self._maze_view.hide_true_or_false_QA_menu()
            self._maze_view.clear_true_or_false_QA_user_answer()

            # Return command interpretation to primary interface
            self._maze_controller.set_active_context("primary_interface")

            # Inform the model
            # NOTE: This will cause the model to update its observers
            self._maze_model.inform_player_answer_correct_or_incorrect(
                user_answer_correct
            )

        elif key == self.COMMANDS[self.Command.SELECT_TRUE][_COMMAND_KEY_KEY]:
            self._maze_view.select_true_or_false_QA_user_answer("True")

        elif key == self.COMMANDS[self.Command.SELECT_FALSE][_COMMAND_KEY_KEY]:
            self._maze_view.select_true_or_false_QA_user_answer("False")


class MultipleChoiceQuestionAndAnswerCommandContext(CommandContext):
    class Command(Enum):
        """Enumeration used to fix commands to a small finite support set."""

        # Item commands
        USE_SUGGESTION_POTION = auto()

        # Answer selection commands
        SELECT_A = auto()
        SELECT_B = auto()
        SELECT_C = auto()
        SELECT_D = auto()

        # Other commands
        SUBMIT_ANSWER = auto()

    COMMANDS = {
        # Item commands
        Command.USE_SUGGESTION_POTION: {
            _COMMAND_TYPE: _COMMAND_TYPE_ITEM,
            _COMMAND_DESC_KEY: "Use suggestion potion",
            _COMMAND_KEY_KEY: "F1",
        },
        # Other commands
        Command.SELECT_A: {
            _COMMAND_TYPE: _COMMAND_TYPE_OTHER,
            _COMMAND_DESC_KEY: "Select option A",
            _COMMAND_KEY_KEY: "a",
        },
        Command.SELECT_B: {
            _COMMAND_TYPE: _COMMAND_TYPE_OTHER,
            _COMMAND_DESC_KEY: "Select option B",
            _COMMAND_KEY_KEY: "b",
        },
        Command.SELECT_C: {
            _COMMAND_TYPE: _COMMAND_TYPE_OTHER,
            _COMMAND_DESC_KEY: "Select option C",
            _COMMAND_KEY_KEY: "c",
        },
        Command.SELECT_D: {
            _COMMAND_TYPE: _COMMAND_TYPE_OTHER,
            _COMMAND_DESC_KEY: "Select option D",
            _COMMAND_KEY_KEY: "d",
        },
        Command.SUBMIT_ANSWER: {
            _COMMAND_TYPE: _COMMAND_TYPE_OTHER,
            _COMMAND_DESC_KEY: "Submit answer",
            _COMMAND_KEY_KEY: "Return",
        },
    }

    def process_keystroke(self, key):
        # Retrieve Q&A object held by controller
        question_and_answer = self._maze_controller.question_and_answer

        if key == self.COMMANDS[self.Command.SUBMIT_ANSWER][_COMMAND_KEY_KEY]:
            # Take question and answer object from controller
            self._maze_controller.question_and_answer = None

            user_answer = self._maze_view.get_multiple_choice_QA_user_answer()
            user_answer_correct = question_and_answer.answer_is_correct(
                user_answer
            )

            # Hide Q&A widget
            self._maze_view.hide_multiple_choice_QA_menu()
            self._maze_view.clear_multiple_choice_QA_user_answer()

            # Return command interpretation to primary interface
            self._maze_controller.set_active_context("primary_interface")

            # Inform the model
            # NOTE: This will cause the model to update its observers
            self._maze_model.inform_player_answer_correct_or_incorrect(
                user_answer_correct
            )

        elif key == self.COMMANDS[self.Command.SELECT_A][_COMMAND_KEY_KEY]:
            self._maze_view.select_multiple_choice_QA_user_answer(
                question_and_answer.options[0]
            )

        elif key == self.COMMANDS[self.Command.SELECT_B][_COMMAND_KEY_KEY]:
            self._maze_view.select_multiple_choice_QA_user_answer(
                question_and_answer.options[1]
            )

        elif key == self.COMMANDS[self.Command.SELECT_C][_COMMAND_KEY_KEY]:
            self._maze_view.select_multiple_choice_QA_user_answer(
                question_and_answer.options[2]
            )

        elif key == self.COMMANDS[self.Command.SELECT_D][_COMMAND_KEY_KEY]:
            self._maze_view.select_multiple_choice_QA_user_answer(
                question_and_answer.options[3]
            )

        elif (
            key
            == self.COMMANDS[self.Command.USE_SUGGESTION_POTION][
                _COMMAND_KEY_KEY
            ]
        ):
            # If user has at least one suggestion potion, use it
            adventurer_items = self._maze_model.get_adventurer_items()
            num_suggestion_potions = sum(
                isinstance(x, SuggestionPotion) for x in adventurer_items
            )
            if num_suggestion_potions > 0:
                self._maze_model.use_item("suggestion potion")
                self._maze_view.set_multiple_choice_QA_hint(
                    question_and_answer.get_hint()
                )


class MagicKeyCommandContext(CommandContext):
    class Command(Enum):
        """Enumeration used to fix commands to a small finite support set."""

        # Item commands
        USE_MAGIC_KEY = auto()

        # Other commands
        DISMISS = auto()

    COMMANDS = {
        # Item commands
        Command.USE_MAGIC_KEY: {
            _COMMAND_TYPE: _COMMAND_TYPE_ITEM,
            _COMMAND_DESC_KEY: "Use magic key",
            _COMMAND_KEY_KEY: "y",
        },
        Command.DISMISS: {
            _COMMAND_TYPE: _COMMAND_TYPE_OTHER,
            _COMMAND_DESC_KEY: "Dismiss",
            _COMMAND_KEY_KEY: "n",
        },
    }

    def process_keystroke(self, key):
        if key == self.COMMANDS[self.Command.USE_MAGIC_KEY][_COMMAND_KEY_KEY]:
            self._maze_model.use_item("magic key")

            self._maze_controller.set_active_context("primary_interface")
            self._maze_view.hide_magic_key_menu()

        elif key == self.COMMANDS[self.Command.DISMISS][_COMMAND_KEY_KEY]:
            self._maze_controller.set_active_context("primary_interface")
            self._maze_view.hide_magic_key_menu()


IN_GAME_MENU_KEY = PrimaryInterfaceCommandContext.COMMANDS[
    PrimaryInterfaceCommandContext.Command.SHOW_IN_GAME_MENU
][_COMMAND_KEY_KEY]

DISMISS_KEYS = (
    DismissibleCommandContext.COMMANDS[
        DismissibleCommandContext.Command.DISMISS
    ][_COMMAND_KEY_KEY],
)

USE_SUGGESTION_POTION_KEY = ShortQuestionAndAnswerCommandContext.COMMANDS[
    ShortQuestionAndAnswerCommandContext.Command.USE_SUGGESTION_POTION
][_COMMAND_KEY_KEY]
