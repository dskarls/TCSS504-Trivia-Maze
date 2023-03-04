from abc import abstractmethod
import textwrap
from tkinter import *
from tkinter.ttk import *

from maze_map import MazeMap
from trivia_maze_model_observer import TriviaMazeModelObserver
from view_config import (
    DIMENSIONS,
    MESSAGES,
    ROOM_CONTENT_DESC_KEY,
    ROOM_CONTENT_SYMBOL_KEY,
    ROOM_CONTENT_SYMBOLS,
    STYLES,
)
from view_components import (
    HPGauge,
    EnumeratedInventory,
    CheckboxInventory,
    MainMenu,
    InGameMenu,
    DismissiblePopUp,
    Map,
    MultipleChoiceQuestionAndAnswerMenu,
    ShortAnswerQuestionAndAnswer,
    TrueFalseQuestionAndAnswerMenu,
    EventLog,
    SubWindow,
)
from maze_items import (
    HealingPotion,
    VisionPotion,
    SuggestionPotion,
    MagicKey,
    AbstractionPillar,
    EncapsulationPillar,
    PolymorphismPillar,
    InheritancePillar,
)


class TriviaMazeView(TriviaMazeModelObserver):
    """
    A view to display the trivia maze game to the user and gather input
    commands.
    """

    def __init__(self, maze_model, maze_controller):
        super().__init__(maze_model)
        self._maze_controller = maze_controller

    @abstractmethod
    def show_main_menu(self):
        """Display the main menu"""

    @abstractmethod
    def hide_main_menu(self):
        """Hide the main menu"""

    @abstractmethod
    def show_main_help_menu(self):
        """Display the help menu accessible from the main menu. Explains rules
        of the game."""

    @abstractmethod
    def hide_main_help_menu(self):
        """hide the help menu accessible from the main menu."""

    @abstractmethod
    def show_in_game_menu(self):
        """Show the in-game menu pop-up"""

    @abstractmethod
    def hide_in_game_menu(self):
        """Hide the in-game menu pop-up"""

    @abstractmethod
    def clear_short_QA_user_answer(self):
        """Clear the contents of the text entry box in the short answer Q&A
        widget."""

    @abstractmethod
    def show_short_QA_menu(self):
        """Show the short answer Q&A widget."""

    @abstractmethod
    def hide_short_QA_menu(self):
        """Hide the short answer Q&A widget."""

    @abstractmethod
    def show_true_or_false_QA_menu(self):
        """Show the true or false answer Q&A widget."""

    @abstractmethod
    def hide_true_or_false_QA_menu(self):
        """Hide the true or false answer Q&A widget."""

    @abstractmethod
    def select_true_or_false_QA_user_answer(self, option_index):
        """Select the option in the true of false QA widget with the text value
        given by `option` (should be "True" or "False").

        Parameters
        ----------
        option_index : int
            Index associated with desired option. Indices are zero-based and go
            left-to-right, top-to-bottom.
        """

    @abstractmethod
    def show_multiple_choice_QA_menu(self):
        """Show the multiple choice answer Q&A widget."""

    @abstractmethod
    def hide_multiple_choice_QA_menu(self):
        """Hide the multiple choice answer Q&A widget."""

    @abstractmethod
    def select_multiple_choice_QA_user_answer(self, option_index):
        """Select the option in the multiple choice QA widget with the text
        value given by `option`.

        Parameters
        ----------
        option_index : int
            Index associated with desired option. Indices are zero-based and go
            left-to-right, top-to-bottom.
        """

    @abstractmethod
    def write_to_event_log(self):
        """Write a message to the event log."""

    @abstractmethod
    def show_game_won_menu(self):
        """Display a pop-up to the user telling them they won the game."""

    @abstractmethod
    def hide_game_won_menu(self):
        """Hide the pop-up to the user telling them they won the game."""

    @abstractmethod
    def show_game_lost_died_menu(self):
        """
        Display a pop-up to the user telling them they lost the game from
        reaching 0 hitpoints.
        """

    @abstractmethod
    def hide_game_lost_died_menu(self):
        """
        Hide the pop-up to the user telling them they lost the game from
        reaching 0 hitpoints.
        """

    @abstractmethod
    def show_game_lost_trapped_menu(self):
        """
        Display a pop-up to the user telling them they lost the game from
        getting trapped in the maze.
        """

    @abstractmethod
    def hide_game_lost_trapped_menu(self):
        """
        Hide the pop-up to the user telling them they lost the game from
        getting trapped in the maze.
        """

    @abstractmethod
    def show_no_save_file_found_menu(self):
        """Show the pop-up telling the user that they can't load a game because
        no save file was found."""

    @abstractmethod
    def hide_no_save_file_found_menu(self):
        """Hide the pop-up telling the user that they can't load a game because
        no save file was found."""

    @abstractmethod
    def quit_entire_game(self):
        """Destroy the entire game and close the window"""


class TextTriviaMazeView(TriviaMazeView):
    """A text-based view for the Trivia Maze application that uses tkinter
    (specifically, themed-tkinter aka "ttk").

    NOTE: Currently, the size is fixed upon creation.
    NOTE: The primary interface (the map, hp gauge, inventory, and event log)
    is technically always shown. The main menu simply consists of overlaying
    the main menu window over the top of the primary interface. Showing the
    primary interface then simply amounts to hiding the main menu (or pop-ups).
    """

    __PILLAR_TYPE_LABELS = {
        AbstractionPillar: "Abstraction",
        EncapsulationPillar: "Encapsulation",
        InheritancePillar: "Inheritance",
        PolymorphismPillar: "Polymorphism",
    }
    __INVENTORY_TYPE_LABELS = {
        HealingPotion: "Health Potion",
        SuggestionPotion: "Suggestion Potion",
        VisionPotion: "Vision Potion",
        MagicKey: "Magic Key",
    }

    def __init__(
        self,
        maze_model,
        maze_controller,
        title,
        dismiss_keys,
        theme_path=None,
        theme_name=None,
    ):
        super().__init__(maze_model, maze_controller)
        self.__dismiss_keys = dismiss_keys

        # Create primary tkinter window and bind mainloop method (might fit
        # better in the driver and we can just pass the main Tk window into the
        # view init?
        self.__window = Tk()
        self.__window.title(title)
        self.mainloop = self.__window.mainloop

        if theme_path and theme_name:
            # To use this theme, clone the relevant repo and then give the path to its
            # azure.tcl file here
            self.__window.tk.call("source", theme_path)
            self.__window.tk.call("set_theme", theme_name)

        # Define styles in memory for tk
        self.__configure_styles()

        # Set minimum row/col sizes to prevent frames from collapsing to their
        # contained content
        self.__window.rowconfigure(0, minsize=DIMENSIONS["map"]["height"])
        self.__window.columnconfigure(0, minsize=DIMENSIONS["map"]["width"])
        self.__window.columnconfigure(
            1, minsize=DIMENSIONS["side_bar"]["width"]
        )

        # Create primary interface windows
        # NOTE: These windows should be created first. Otherwise, the other
        # widgets will always be "hidden" behind them. You could also get
        # around this by using the 'lift()' and 'lower()' methods of the frame
        # widgets, but it's simpler just to make them in order.
        self.__map = self.__create_map()
        (
            self.__hp_gauge,
            self.__inventory,
            self.__pillars_inventory,
            self.__menu_access_label,
        ) = self.__create_side_bar()
        self.__event_log = self.__create_event_log()

        # Create a MazeMap object that can be used to generate map context
        self.__maze_map = MazeMap(
            self._maze_model.num_rows,
            self._maze_model.num_cols,
            3,
            padding_col="  ",
        )
        self.__update_map()

        # Add separator lines to divide UI cleanly
        # NOTE: The separators need to be created after the primary interface
        # components but before any of the pop-up widgets that can show up on
        # top of it.
        self.__separators = self.__create_separators()

        # Create game won/lost menus
        self.__game_won_menu = self.__create_game_won_menu()
        self.hide_game_won_menu()

        self.__game_lost_died_menu = self.__create_game_lost_died_menu()
        self.hide_game_lost_died_menu()

        self.__game_lost_trapped_menu = self.__create_game_lost_trapped_menu()
        self.hide_game_lost_trapped_menu()

        # Create dialog for needing magic key
        self.__need_magic_key_menu = self.__create_need_magic_key_menu()
        self.hide_need_magic_key_menu()

        # Create dialog for using magic key
        self.__magic_key_menu = self.__create_magic_key_menu()
        self.hide_magic_key_menu()

        # Set up in-game menu
        self.__in_game_menu = self.__create_in_game_menu()
        self.hide_in_game_menu()

        # Map legend menu
        self.__map_legend_menu = self.__create_map_legend_menu()
        self.hide_map_legend_menu()

        # Create pop-up to confirm user save game
        self.__save_confirmation_menu = self.__create_save_confirmation_menu()
        self.hide_save_confirmation_menu()

        # Create empty commands help menu
        self.__command_legend_menu = self.__create_command_legend_menu()
        self.hide_command_legend_menu()

        # Creat empty short answer question & answer menu
        self.__short_QA_menu = self.__create_short_QA_menu()
        self.hide_short_QA_menu()

        # Creat empty true or false question & answer menu
        self.__true_or_false_QA_menu = self.__create_true_or_false_QA_menu()
        self.hide_true_or_false_QA_menu()

        # Creat empty short answer question & answer menu
        self.__multiple_choice_QA_menu = (
            self.__create_multiple_choice_QA_menu()
        )
        self.hide_multiple_choice_QA_menu()

        # Create main menu and the help menu accessible from it
        self.__main_menu = self.__create_main_menu()

        # Create pop-up to tell user that load game failed because no save file
        # could be found
        self.__no_save_file_found_menu = (
            self.__create_no_save_file_found_menu()
        )
        self.hide_no_save_file_found_menu()

        # Help menu accessible from main menu
        self.__main_help_menu = self.__create_main_help_menu()
        self.hide_main_help_menu()

        # Prevent resizing
        self.__window.resizable(False, False)

        # Show main menu and have it take focus
        self.show_main_menu()

        # Intercept keystrokes from user
        self.__configure_keystroke_capture()

    def __create_separators(self):
        """Creates a set of desired separators and their relevant dimensions,
        packed as Separator-dict 2-tuples."""
        separators = []

        # Vertical line along right edge of map
        separators.append(
            (
                Separator(self.__window, orient=VERTICAL),
                {
                    "x": DIMENSIONS["map"]["width"],
                    "height": DIMENSIONS["map"]["height"],
                },
            )
        )

        # Horizontal line along bottom edge of map
        separators.append(
            (
                Separator(self.__window, orient=HORIZONTAL),
                {
                    "y": DIMENSIONS["map"]["height"],
                    "width": DIMENSIONS["map"]["width"],
                },
            )
        )

        # Horizonal line under hp gauge
        separators.append(
            (
                Separator(self.__window, orient=HORIZONTAL),
                {
                    "x": DIMENSIONS["map"]["width"],
                    "y": DIMENSIONS["hp_gauge"]["height"]
                    + DIMENSIONS["hp_gauge_bar"]["pady"],
                    "width": DIMENSIONS["side_bar"]["width"],
                },
            )
        )

        return separators

    def __show_separators(self):
        """Show the separator lines in the application master frame (intended
        to show up in the primary interface)."""
        for separator_and_place_params in self.__separators:
            separator, place_params = separator_and_place_params
            separator.place(**place_params)

    def __hide_separators(self):
        """Hide the separator lines in the application master frame (intended
        to show up in the primary interface)."""
        for separator_and_place_params in self.__separators:
            separator, _ = separator_and_place_params
            separator.place_forget()

    @staticmethod
    def __configure_styles():
        """Loop over the themed-tk (ttk) styles defined in the view config and
        make sure they're registered in ttk's style namespace."""
        for style in STYLES.values():
            Style().configure(**style)

    def __configure_keystroke_capture(self):
        """Capture keystrokes so they can be sent to the controller for
        interpretation"""
        self.__window.bind(
            "<KeyPress>", self.__forward_keystroke_to_controller
        )
        # Also capture arrow keys
        for arrow_key_event in {"<Left>", "<Right>", "<Up>", "<Down>"}:
            self.__window.bind(
                arrow_key_event,
                self.__forward_keystroke_to_controller,
            )

    def __create_main_menu(self):
        """Create a main menu widget, insert it into the application master
        frame, and return it."""
        options = ("Start game", "Load Game", "Help", "Quit game")
        return MainMenu(self.__window, MESSAGES["main_menu"], options)

    def get_main_menu_current_selection(self):
        """Return the currently selected option in the main menu."""
        return self.__main_menu.selected_option

    def hide_main_menu(self):
        """Hide the main menu widget and show the primary interface
        separators"""
        self.__main_menu.hide()
        self.__show_separators()

    def show_main_menu(self):
        """Show the main menu widget and hide the primary interface
        separators"""
        self.__main_menu.show()
        self.__hide_separators()

    def __create_in_game_menu(self):
        """Create the in-game menu widget, which is accessible to the user from
        the primary interface while they're actually playing the game."""
        options = (
            "Back to Game",
            "Display Map Legend",
            "Display Commands",
            "Save Game",
            "Return to Main Menu",
            "Quit Game",
        )
        return InGameMenu(
            self.__window,
            DIMENSIONS["in_game_menu"]["width"],
            "In-Game Menu",
            DIMENSIONS["in_game_menu_title"]["padx"],
            DIMENSIONS["in_game_menu_title"]["pady"],
            options,
        )

    def get_in_game_menu_current_selection(self):
        """Return the currently selected option in the in-game menu."""
        return self.__in_game_menu.selected_option

    def show_in_game_menu(self):
        """Show the in-game menu."""
        self.__in_game_menu.show()

    def hide_in_game_menu(self):
        """Hide the in-game menu."""
        self.__in_game_menu.hide()

    def __create_short_QA_menu(self):
        """Create a generic question and answer widget that doesn't hold any
        content yet. Its content can be populated by the controller using the
        `set_short_QA_question` and `set_short_WA_hint` methods."""
        return ShortAnswerQuestionAndAnswer(
            self.__window,
            None,
            DIMENSIONS["question_and_answer_menu"]["wraplength"],
            "Short Question & Answer",
            DIMENSIONS["question_and_answer_menu"]["padx"],
            DIMENSIONS["question_and_answer_menu"]["ipady"],
        )

    def set_short_QA_question(self, question_text):
        """Populate the short answer question and answer widget with the
        question contents."""
        self.__short_QA_menu.set_question(question_text)

    def set_short_QA_hint(self, hint_text):
        """Fill in the hint portion of the short question and answer widget
        with the hint contents."""
        self.__short_QA_menu.set_hint(hint_text)

    def show_short_QA_menu(self):
        """Show the question and answer widget."""
        self.__short_QA_menu.show()

    def hide_short_QA_menu(self):
        """Hide the question and answer widget."""
        self.__short_QA_menu.hide()

    def get_short_QA_user_answer(self):
        """Return the user's current answer to the relevant Q&A prompt."""
        return self.__short_QA_menu.get_user_answer()

    def clear_short_QA_user_answer(self):
        """Clear the contents of the text entry box in the short answer Q&A
        widget."""
        return self.__short_QA_menu.clear_user_answer()

    def __create_multiple_choice_QA_menu(self):
        """Create a generic question and answer widget that doesn't hold any
        content yet. Its content can be populated by the controller using the
        `set_multiple_choice_QA_question` and `set_multiple_choice_WA_hint` methods.
        """
        return MultipleChoiceQuestionAndAnswerMenu(
            self.__window,
            None,
            DIMENSIONS["question_and_answer_menu"]["wraplength"],
            "Short Question & Answer",
            DIMENSIONS["question_and_answer_menu"]["padx"],
            DIMENSIONS["question_and_answer_menu"]["ipady"],
        )

    def set_multiple_choice_QA_question(self, question_text):
        """Populate the multiple_choice answer question and answer widget with the
        question contents."""
        self.__multiple_choice_QA_menu.set_question(question_text)

    def set_multiple_choice_QA_hint(self, hint_text):
        """Fill in the hint portion of the multiple_choice question and answer widget
        with the hint contents."""
        self.__multiple_choice_QA_menu.set_hint(hint_text)

    def set_multiple_choice_QA_options(self, options):
        """Sets the options for selection to those in ``options``.

        Parameters
        ----------
        options : List
            List of strings comprising selection options.
        """
        return self.__multiple_choice_QA_menu.set_options(options)

    def show_multiple_choice_QA_menu(self):
        """Show the question and answer widget."""
        self.__multiple_choice_QA_menu.show()

    def hide_multiple_choice_QA_menu(self):
        """Hide the question and answer widget."""
        self.__multiple_choice_QA_menu.hide()

    def get_multiple_choice_QA_user_answer(self):
        """Return the user's current answer to the relevant Q&A prompt."""
        return self.__multiple_choice_QA_menu.get_user_answer()

    def clear_multiple_choice_QA_user_answer(self):
        """Clear the contents of the text entry box in the short answer Q&A
        widget."""
        return self.__multiple_choice_QA_menu.clear_selection()

    def select_multiple_choice_QA_user_answer(self, option_index):
        """Select the option in the multiple choice QA widget with the text
        value given by `option`.

        Parameters
        ----------
        option_index : int
            Index associated with desired option. Indices are zero-based and go
            left-to-right, top-to-bottom.
        """
        self.__multiple_choice_QA_menu.select_user_option(option_index)

    def __create_true_or_false_QA_menu(self):
        """Create a generic T/F question and answer widget that doesn't hold
        any content yet. Its content can be populated by the controller using
        `set_true_or_false_QA_question` and `set_true_or_false_WA_hint`
        methods.
        """
        return TrueFalseQuestionAndAnswerMenu(
            self.__window,
            None,
            DIMENSIONS["question_and_answer_menu"]["wraplength"],
            "True/False Question & Answer",
            DIMENSIONS["question_and_answer_menu"]["padx"],
            DIMENSIONS["question_and_answer_menu"]["ipady"],
        )

    def set_true_or_false_QA_question(self, question_text):
        """Populate the true or false question and answer widget with the
        question contents."""
        self.__true_or_false_QA_menu.set_question(question_text)

    def clear_true_or_false_QA_user_answer(self):
        """Clear the contents of the text entry box in the short answer Q&A
        widget."""
        return self.__true_or_false_QA_menu.clear_selection()

    def select_true_or_false_QA_user_answer(self, option_index):
        """Select the option in the true of false QA widget with the text value
        given by `option` (should be "True" or "False").

        Parameters
        ----------
        option_index : int
            Index associated with desired option. Indices are zero-based and go
            left-to-right, top-to-bottom.
        """
        self.__true_or_false_QA_menu.select_user_option(option_index)

    def show_true_or_false_QA_menu(self):
        """Show the question and answer widget."""
        self.__true_or_false_QA_menu.show()

    def hide_true_or_false_QA_menu(self):
        """Hide the question and answer widget."""
        self.__true_or_false_QA_menu.hide()

    def get_true_or_false_QA_user_answer(self):
        """Return the user's current answer to the relevant Q&A prompt."""
        return self.__true_or_false_QA_menu.get_user_answer()

    def __create_no_save_file_found_menu(self):
        """Create pop-up that tells the user that they couldn't load a game
        because no save file could be found."""
        dismiss_message = (
            f"Press {' or '.join(self.__dismiss_keys)} to return to the main "
            "menu"
        )
        return DismissiblePopUp(
            self.__window,
            None,
            textwrap.dedent(MESSAGES["no_save_file_found_menu"]),
            dismiss_message,
            DIMENSIONS["no_save_file_found_menu"]["ipadx"],
            DIMENSIONS["no_save_file_found_menu"]["ipady"],
            STYLES["dismiss_text"]["style"],
            STYLES["dismiss_bottom_label"]["style"],
        )

    def show_no_save_file_found_menu(self):
        """Show the pop-up telling the user that they can't load a game because
        no save file was found."""
        self.__no_save_file_found_menu.show()

    def hide_no_save_file_found_menu(self):
        """Hide the pop-up telling the user that they can't load a game because
        no save file was found."""
        self.__no_save_file_found_menu.hide()

    def __create_save_confirmation_menu(self):
        """Create pop-up that tells the user that their save game was
        successful."""
        dismiss_message = (
            f"Press {' or '.join(self.__dismiss_keys)} to return to the "
            "in-game menu"
        )
        return DismissiblePopUp(
            self.__window,
            None,
            textwrap.dedent(MESSAGES["save_confirmation_menu"]),
            dismiss_message,
            DIMENSIONS["save_confirmation_menu"]["ipadx"],
            DIMENSIONS["save_confirmation_menu"]["ipady"],
            STYLES["dismiss_text"]["style"],
            STYLES["dismiss_bottom_label"]["style"],
        )

    def show_save_confirmation_menu(self):
        """Show the pop-up that tells the user their save game was
        successful."""
        self.__save_confirmation_menu.show()

    def hide_save_confirmation_menu(self):
        """Hide the pop-up that tells the user their save game was
        successful."""
        self.__save_confirmation_menu.hide()

    def __create_main_help_menu(self):
        """Create the main help menu. This is the help menu that is accessed
        from the main menu."""
        dismiss_message = (
            f"Press {' or '.join(self.__dismiss_keys)} to return to the main "
            "menu"
        )
        return DismissiblePopUp(
            self.__window,
            None,
            textwrap.dedent(MESSAGES["main_help_menu"]),
            dismiss_message,
            DIMENSIONS["main_help_menu"]["ipadx"],
            DIMENSIONS["main_help_menu"]["ipady"],
            STYLES["dismiss_text"]["style"],
            STYLES["dismiss_bottom_label"]["style"],
        )

    def show_main_help_menu(self):
        """Show the main help menu."""
        self.__main_help_menu.show()

    def hide_main_help_menu(self):
        """Hide the main help menu."""
        self.__main_help_menu.hide()

    def __create_need_magic_key_menu(self):
        """Create the widget for when the player tries to pass through a
        permanently locked door and do not hold any magic keys. It tells them
        they need to find a magic key if they want to unlock the door."""
        dismiss_message = (
            f"Press {' or '.join(self.__dismiss_keys)} to return to the game"
        )
        return DismissiblePopUp(
            self.__window,
            None,
            textwrap.dedent(MESSAGES["need_magic_key_menu"]),
            dismiss_message,
            DIMENSIONS["need_magic_key_menu"]["ipadx"],
            DIMENSIONS["need_magic_key_menu"]["ipady"],
            STYLES["dismiss_text"]["style"],
            STYLES["dismiss_bottom_label"]["style"],
        )

    def show_need_magic_key_menu(self):
        """Show the widget that tells the player they need a magic key to
        unlock a permanently locked door."""
        self.__need_magic_key_menu.show()

    def hide_need_magic_key_menu(self):
        """Hide the widget that tells the player they need a magic key to
        unlock a permanently locked door."""
        self.__need_magic_key_menu.hide()

    def __create_magic_key_menu(self):
        """Create the widget for when the player tries to pass through a
        permanently locked door and holds a magic key. It asks them if they
        would like to use a magic key or not."""
        dismiss_message = f"Press 'y' to use a magic key if not press 'n'"
        return DismissiblePopUp(
            self.__window,
            None,
            textwrap.dedent(MESSAGES["use_magic_key_menu"]),
            dismiss_message,
            DIMENSIONS["magic_key_menu"]["ipadx"],
            DIMENSIONS["magic_key_menu"]["ipady"],
            STYLES["dismiss_text"]["style"],
            STYLES["dismiss_bottom_label"]["style"],
        )

    def show_magic_key_menu(self):
        """Show the widget that tells the player they can use a magic key to
        unlock a permanently locked door."""
        self.__magic_key_menu.show()

    def hide_magic_key_menu(self):
        """Hide the widget that tells the player they can use a magic key to
        unlock a permanently locked door."""
        self.__magic_key_menu.hide()

    def __create_game_won_menu(self):
        """Create the widget telling the player they won the game."""
        dismiss_message = (
            f"Press {' or '.join(self.__dismiss_keys)} to return to the main "
            "menu"
        )
        return DismissiblePopUp(
            self.__window,
            None,
            textwrap.dedent(MESSAGES["game_won_menu"]),
            dismiss_message,
            DIMENSIONS["game_won_menu"]["ipadx"],
            DIMENSIONS["game_won_menu"]["ipady"],
            STYLES["dismiss_text"]["style"],
            STYLES["dismiss_bottom_label"]["style"],
        )

    def show_game_won_menu(self):
        """Show the widget telling the player they won the game."""
        self.__game_won_menu.show()

    def hide_game_won_menu(self):
        """Hide the widget telling the player they won the game."""
        self.__game_won_menu.hide()

    def __create_game_lost_died_menu(self):
        """Create the widget telling the player they lost the game
        from the adventurer reaching 0 hitpoints."""
        dismiss_message = (
            f"Press {' or '.join(self.__dismiss_keys)} to return to the main "
            "menu"
        )
        return DismissiblePopUp(
            self.__window,
            None,
            textwrap.dedent(MESSAGES["game_lost_died_menu"]),
            dismiss_message,
            DIMENSIONS["game_lost_died_menu"]["ipadx"],
            DIMENSIONS["game_lost_died_menu"]["ipady"],
            STYLES["dismiss_text"]["style"],
            STYLES["dismiss_bottom_label"]["style"],
        )

    def show_game_lost_died_menu(self):
        """Show the widget telling the player they lost the game."""
        self.__game_lost_died_menu.show()

    def hide_game_lost_died_menu(self):
        """Hide the widget telling the player they lost the game."""
        self.__game_lost_died_menu.hide()

    def __create_game_lost_trapped_menu(self):
        """Create the widget telling the player they lost the game by
        getting trapped in the maze."""
        dismiss_message = (
            f"Press {' or '.join(self.__dismiss_keys)} to return to the main "
            "menu"
        )
        return DismissiblePopUp(
            self.__window,
            None,
            textwrap.dedent(MESSAGES["game_lost_trapped_menu"]),
            dismiss_message,
            DIMENSIONS["game_lost_trapped_menu"]["ipadx"],
            DIMENSIONS["game_lost_trapped_menu"]["ipady"],
            STYLES["dismiss_text"]["style"],
            STYLES["dismiss_bottom_label"]["style"],
        )

    def show_game_lost_trapped_menu(self):
        """Show the widget telling the player they lost the game
        from getting trapped."""
        self.__game_lost_trapped_menu.show()

    def hide_game_lost_trapped_menu(self):
        """Hide the widget telling the player they lost the game
        from getting trapped."""
        self.__game_lost_trapped_menu.hide()

    def __forward_keystroke_to_controller(self, event):
        """Given a tkinter event, attempt to map it to a corresponding
        keystroke and pass it to the controller for interpretation as a
        command."""
        NEWLINE = 13
        ESCAPE = 27
        LINEFEED = 10

        # For regular keys
        key = event.char

        # If char was empty, check to see if it was an arrow key
        if not key or event.keycode in (NEWLINE, ESCAPE, LINEFEED):
            key = event.keysym

        if key:
            # If keysym wasn't empty, forward it to controller. Otherwise, just
            # ignore it since it's not a supported key command.
            self._maze_controller.process_keystroke(key)

    def __create_map(self):
        """Create the map widget that is displayed in the primary interface."""
        dims = DIMENSIONS["map"]
        return Map(
            self.__window,
            dims["width"],
            dims["height"],
            0,
            0,
            dims["padx"],
            "",
        )

    def __update_map(self):
        """Update the contents of the map by looping over all rooms in the maze
        and redrawing them."""
        for room_row in self._maze_model.get_rooms():
            for room in room_row:
                self.__maze_map.update_room(room)
        self.__map.contents = str(self.__maze_map)

    def __create_side_bar(self):
        """Create the sidebar frame that holds the hp gauge, inventory, and
        pillar inventory."""
        dims_side_bar = DIMENSIONS["side_bar"]

        side_bar = SubWindow(
            window=self.__window,
            width=dims_side_bar["width"],
            height=DIMENSIONS["map"]["height"],
            row=0,
            column=1,
            rowspan=1,
            columnspan=1,
        )

        dims_hp_gauge_bar = DIMENSIONS["hp_gauge_bar"]
        hp_gauge = HPGauge(
            window=side_bar.frame,
            height=DIMENSIONS["hp_gauge"]["height"],
            bar_width=dims_hp_gauge_bar["width"],
            label_padx=DIMENSIONS["hp_gauge_label"]["padx"],
            bar_padx=dims_hp_gauge_bar["padx"],
            bar_pady=dims_hp_gauge_bar["pady"],
        )

        dims_inventory = DIMENSIONS["inventory"]
        inventory = EnumeratedInventory(
            window=side_bar.frame,
            title="Inventory",
            title_ipady=DIMENSIONS["inventory_title"]["ipady"],
            padx=dims_inventory["padx"],
            pady=dims_inventory["pady"],
            item_labels=self.__INVENTORY_TYPE_LABELS.values(),
        )

        dims_pillars = DIMENSIONS["pillars"]
        pillars_inventory = CheckboxInventory(
            window=side_bar.frame,
            title="Pillars of OOP",
            title_ipady=DIMENSIONS["pillars_title"]["ipady"],
            padx=dims_pillars["padx"],
            pady=dims_pillars["pady"],
            item_labels=self.__PILLAR_TYPE_LABELS.values(),
        )

        menu_access_label = Label(
            master=side_bar.frame,
            text="",
            justify=CENTER,
            anchor=CENTER,
            style=STYLES["menu_access_label"]["style"],
            wraplength=DIMENSIONS["side_bar"]["width"]
            - DIMENSIONS["menu_access_label"]["ipadx"],
        )
        menu_access_label.pack(
            side=BOTTOM,
            ipadx=DIMENSIONS["menu_access_label"]["ipadx"],
            ipady=DIMENSIONS["menu_access_label"]["ipady"],
        )
        return hp_gauge, inventory, pillars_inventory, menu_access_label

    def populate_menu_access_label(self, text):
        """
        Fills in the content of the help message label at the bottom of the
        side bar.

        Parameters
        ----------
        text : str
            An instruction to the user as to how they can pull up the in-game
            menu.
        """
        self.__menu_access_label.configure(text=text)

    def __create_map_legend_menu(
        self,
        num_cols=2,
    ):
        """Create the widget that can be accessed from the in-game menu to
        display the legend of symbols used in the map.

        Parameters
        ----------
        num_cols : int
            How many columns of symbol-description pairs should be constructed
            in the map legend.
        """
        symbols = []
        descriptions = []
        for _, entry in ROOM_CONTENT_SYMBOLS.items():
            symbols.append(entry[ROOM_CONTENT_SYMBOL_KEY])
            descriptions.append(entry[ROOM_CONTENT_DESC_KEY])

        symbol_overrides = {" ": "<space>"}
        legend_rows = self.__generate_rows_for_multicolumn_display(
            symbols=symbols,
            descriptions=descriptions,
            num_cols=num_cols,
            symbol_overrides=symbol_overrides,
        )

        dismiss_message = (
            f"Press {' or '.join(self.__dismiss_keys)} to return to the "
            "in-game menu"
        )
        return DismissiblePopUp(
            self.__window,
            None,
            ("\n").join(legend_rows),
            dismiss_message,
            DIMENSIONS["map_legend_menu"]["ipadx"],
            DIMENSIONS["map_legend_menu"]["ipady"],
            STYLES["dismiss_text"]["style"],
            STYLES["dismiss_bottom_label"]["style"],
        )

    @staticmethod
    def __generate_rows_for_multicolumn_display(
        symbols, descriptions, num_cols, symbol_overrides
    ):
        """Given a set of symbols and descriptions for a legend, pack them into
        a specified number of formatted columns so that they can be displayed
        as a giant string. Symbols can be overridden using a dictionary
        parameter.

        Parameters
        ----------
        symbols : list
            Abbreviated symbols that need descriptions.
        descriptions : list
            Description that explain the abbreviated symbols.
        num_cols : int
            How many columns of symbol-description pairs should be constructed
            in the display.
        symbol_overrides : dict
            Maps strings in ``symbols`` to strings that should be written into
            the display instead, e.g. an space doesn't display well so we
            replace it with "<space>".

        Returns
        -------
        list
            The individual rows of text that make up the display content. These
            will typically be joined by newlines by the caller to come up with
            the final display string.
        """
        # Separation to place between columns
        COL_SEP = "  "
        SYMBOL_DESC_SEP = ": "

        # Initialize 2D array that will contain some number of display rows
        # (depending on the length of symbols and descriptions), each of which
        # will contain 2*num_cols entries corresponding to the symbol and
        # description of each column.
        rows = []
        row = -1
        col = 0
        for symbol, description in zip(symbols, descriptions):
            if symbol in symbol_overrides:
                symbol = symbol_overrides[symbol]

            if col == 0:
                # Begin list for this row
                rows.append([])
                row += 1

            rows[row].append([symbol, description])

            col += 1

            if col == num_cols:
                # Reset column counter
                col = 0

        # Find the longest symbol string in each symbol subcolumn
        symbol_max_len_by_col = []
        description_max_len_by_col = []

        # Maximum possible width of a given row of chars
        total_width = len(COL_SEP) * (num_cols - 1)

        for col in range(num_cols):
            # For this column, assemble all symbols for it by looping over all
            # of the rows
            symbols_in_col = []
            descriptions_in_col = []
            for row in rows:
                # If this row doesn't have an entry for all columns, append
                # empty string entries.
                if col >= len(row):
                    symbols_in_col.append("")
                    descriptions_in_col.append("")
                else:
                    symbols_in_col.append(row[col][0])
                    descriptions_in_col.append(row[col][1])

            symbol_max_len_in_this_col = len(max(symbols_in_col, key=len))
            description_max_len_in_this_col = len(
                max(descriptions_in_col, key=len)
            )
            description_max_len_by_col.append(description_max_len_in_this_col)
            symbol_max_len_by_col.append(symbol_max_len_in_this_col)

            total_width += (
                symbol_max_len_in_this_col
                + len(SYMBOL_DESC_SEP)
                + description_max_len_in_this_col
            )

        row_entries = []
        for row in rows:
            row_str = ""
            for col, (symbol, description) in enumerate(row):
                row_str += (
                    f"{symbol:>{symbol_max_len_by_col[col]}}{SYMBOL_DESC_SEP}"
                    f"{description:<{description_max_len_by_col[col]}}"
                )
                if col < len(row) - 1:
                    row_str += COL_SEP

            row_entries.append(row_str)

        # Pad the bottom row to the right with spaces
        row_entries[-1] = row_entries[-1].ljust(total_width)

        return row_entries

    def show_map_legend_menu(self):
        """Show the widget that can be accessed from the in-game menu to
        display the legend of symbols used in the map."""
        self.__map_legend_menu.show()

    def hide_map_legend_menu(self):
        """Hide the widget that can be accessed from the in-game menu to
        display the legend of symbols used in the map."""
        self.__map_legend_menu.hide()

    def __create_command_legend_menu(self):
        """Create the widget that can be accessed from the in-game menu to
        display the commands accessible in the primary interface. Note that the
        contents are initially empty, and are set via arguments passed to the
        `show_commands_legend_menu()` method."""
        dismiss_message = (
            f"Press {' or '.join(self.__dismiss_keys)} to return to the "
            "in-game menu"
        )
        return DismissiblePopUp(
            self.__window,
            None,
            None,
            dismiss_message,
            DIMENSIONS["command_legend_menu"]["ipadx"],
            DIMENSIONS["command_legend_menu"]["ipady"],
            STYLES["dismiss_text"]["style"],
            STYLES["dismiss_bottom_label"]["style"],
        )

    def show_command_legend_menu(self, symbols, descriptions, num_cols):
        """
        Fills the commands legend widget based on a set of symbols, their
        descriptions, and a number of columns to arrange them in.

        Parameters
        ----------
        symbols : list
            Abbreviated symbols used in the map.
        descriptions : list
            Description of each symbol used in the map.
        num_cols : int
            How many columns of symbol-description pairs should be constructed
            in the command legend.
        """
        legend_rows = self.__generate_rows_for_multicolumn_display(
            symbols=symbols,
            descriptions=descriptions,
            num_cols=num_cols,
            symbol_overrides={},
        )

        self.__command_legend_menu.set_text(("\n").join(legend_rows))
        self.__command_legend_menu.show()

    def hide_command_legend_menu(self):
        """Hide the widget that can be accessed from the in-game menu to
        display the commands accessible in the primary interface."""
        self.__command_legend_menu.hide()

    def __create_event_log(self):
        """Create the event log widget, which is used to record log messages
        for display to the user in the primary interface when a notable event
        occurs."""
        dims = DIMENSIONS["event_log"]
        return EventLog(
            self.__window,
            None,
            dims["height"],
            1,
            0,
            1,
            2,
            dims["padx"],
            dims["pady"],
        )

    def write_to_event_log(self, message):
        """Write a message on a new line in the event log widget.

        Parameters
        ----------
        message : str
            Text to write into the chat log.
        """
        self.__event_log.write(message)

    def update(self):
        # Update map
        self.__update_map()

        # Update adventurer HP
        self.__hp_gauge.set(self._maze_model.get_adventurer_hp())

        # Grab event log entries and write them out
        for log_message in self._maze_model.flush_event_log_buffer():
            self.write_to_event_log(log_message)

        # Update inventories
        self.__update_inventories()

    def __update_inventories(self):
        """Update the count of all items in regular inventory and pillar
        inventory"""
        current_items = self._maze_model.get_adventurer_items()
        self.__update_inventory(current_items)
        self.__update_pillar_inventory(current_items)

    def __update_inventory(self, current_items):
        """Update the counts of all items in the enumerated inventory."""
        for item_type, item_label in self.__INVENTORY_TYPE_LABELS.items():
            item_count = sum(
                isinstance(item, item_type) for item in current_items
            )
            self.__inventory.update_item_quantity(item_label, item_count)

    def __update_pillar_inventory(self, current_items):
        """Check any boxes in the pillar inventory if the adventurer holds the
        relevant pillar."""
        for pillar_type, pillar_label in self.__PILLAR_TYPE_LABELS.items():
            if any((isinstance(item, pillar_type) for item in current_items)):
                self.__pillars_inventory.check_item(pillar_label)

    def reset_inventories(self):
        """Set all inventory quantities to zero and uncheck all pillar
        boxes."""
        self.__inventory.clear()
        self.__pillars_inventory.clear()

    def clear_event_log(self):
        """Remove all contents from the event log."""
        self.__event_log.clear()

    def quit_entire_game(self):
        """Tear down the entire application and quit."""
        self.__window.destroy()
