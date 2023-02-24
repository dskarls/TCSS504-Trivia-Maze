from collections import deque
import os
from abc import ABC, abstractmethod
import textwrap

from tkinter import *
from tkinter.ttk import *

from view_config import (
    DIMENSIONS,
    MESSAGES,
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
    ShortAnswerQuestionAndAnswer,
    EventLog,
    SubWindow,
)


class TriviaMazeModelObserver(ABC):
    def __init__(self, maze_model):
        self._maze_model = maze_model

    @abstractmethod
    def update(self):
        """Perform any necessary updates to self whenever the maze model emits
        a notification."""


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
    def pose_question_and_get_answer(self, question_and_answer):
        """Show the user a question-and-answer pop-up and retrieve the answer,
        then hide the pop-up."""

    @abstractmethod
    def update_map(self):
        """Update the map according to the latest state of the Model."""

    @abstractmethod
    def update_hp_gauge(self):
        """Update the HP gauge to reflect the adventurer's current health
        points."""

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
    def show_game_lost_menu(self):
        """Display a pop-up to the user telling them they lost the game."""

    @abstractmethod
    def hide_game_lost_menu(self):
        """Hide the pop-up to the user telling them they lost the game."""

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
        ) = self.__create_side_bar()
        self.__event_log = self.__create_event_log()

        # Add separator lines to divide UI cleanly
        # NOTE: The separators need to be created after the primary interface
        # components but before any of the pop-up widgets that can show up on
        # top of it.
        self.__separators = self.__create_separators()

        # Create game won/lost menus
        self.__game_won_menu = self.__create_game_won_menu()
        self.hide_game_won_menu()

        self.__game_lost_menu = self.__create_game_lost_menu()
        self.hide_game_lost_menu()

        # Create dialog for needing magic key
        self.__need_magic_key_menu = self.__create_need_magic_key_menu()
        self.hide_need_magic_key_menu()

        # Set up in-game menu
        self.__in_game_menu = self.__create_in_game_menu()
        self.hide_in_game_menu()

        self.__map_legend_menu = self.__create_map_legend_menu()
        self.hide_map_legend_menu()

        # Create empty commands help menu
        self.__command_legend_menu = self.__create_command_legend_menu()
        self.hide_command_legend_menu()

        # Creat empty question & answer menu
        self.__question_and_answer_menu = (
            self.__create_question_and_answer_menu()
        )
        self.hide_question_and_answer_menu()

        # Create main menu and the help menu accessible from it
        self.__main_menu = self.__create_main_menu()

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
        for separator_and_place_params in self.__separators:
            separator, place_params = separator_and_place_params
            separator.place(**place_params)

    def __hide_separators(self):
        for separator_and_place_params in self.__separators:
            separator, _ = separator_and_place_params
            separator.place_forget()

    @staticmethod
    def __configure_styles():
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
        options = ("Start game", "Help", "Quit game")
        return MainMenu(self.__window, MESSAGES["main_menu"], options)

    def get_main_menu_current_selection(self):
        return self.__main_menu.selected_option

    def hide_main_menu(self):
        self.__main_menu.hide()
        self.__show_separators()

    def show_main_menu(self):
        self.__main_menu.show()
        self.__hide_separators()

    def __create_in_game_menu(self):
        options = (
            "Back to Game",
            "Display Map Legend",
            "Display Commands",
            "Return to Main Menu",
            "Quit Game",
        )
        return InGameMenu(
            self.__window,
            DIMENSIONS["in_game_menu"]["width"],
            "In-Game Menu",
            DIMENSIONS["in_game_menu_title"]["pady"],
            options,
        )

    def get_in_game_menu_current_selection(self):
        return self.__in_game_menu.selected_option

    def show_in_game_menu(self):
        self.__in_game_menu.show()

    def hide_in_game_menu(self):
        self.__in_game_menu.hide()

    def __create_question_and_answer_menu(self):
        return ShortAnswerQuestionAndAnswer(
            self.__window,
            None,
            "Q & A",
            DIMENSIONS["question_and_answer_menu"]["pady"],
        )

    def set_question(self, question, options, hint):
        self.__question_and_answer_menu.set_question(question)
        self.__question_and_answer_menu.set_options(options)
        self.__question_and_answer_menu.set_hint(hint)

    def show_question_and_answer_menu(self):
        self.__question_and_answer_menu.show()

    def hide_question_and_answer_menu(self):
        self.__question_and_answer_menu.hide()

    def __create_main_help_menu(self):
        dismiss_message = (
            f"Press {' or '.join(self.__dismiss_keys)} to return to the main "
            "menu"
        )
        return DismissiblePopUp(
            self.__window,
            None,
            textwrap.dedent(MESSAGES["main_help_menu"]),
            DIMENSIONS["main_help_menu"]["pady"],
            dismiss_message,
        )

    def show_main_help_menu(self):
        self.__main_help_menu.show()

    def hide_main_help_menu(self):
        self.__main_help_menu.hide()

    def __create_need_magic_key_menu(self):
        """This menu is displayed to the player when they attempt to pass
        through a permanently locked door and do not hold any magic keys."""
        dismiss_message = (
            f"Press {' or '.join(self.__dismiss_keys)} to return to the game"
        )
        return DismissiblePopUp(
            self.__window,
            None,
            textwrap.dedent(MESSAGES["need_magic_key_menu"]),
            DIMENSIONS["need_magic_key_menu"]["pady"],
            dismiss_message,
        )

    def show_need_magic_key_menu(self):
        self.__need_magic_key_menu.show()

    def hide_need_magic_key_menu(self):
        self.__need_magic_key_menu.hide()

    def __create_game_won_menu(self):
        dismiss_message = (
            f"Press {' or '.join(self.__dismiss_keys)} to return to the main "
            "menu"
        )
        return DismissiblePopUp(
            self.__window,
            None,
            textwrap.dedent(MESSAGES["game_won_menu"]),
            DIMENSIONS["game_won_menu"]["pady"],
            dismiss_message,
        )

    def show_game_won_menu(self):
        self.__game_won_menu.show()

    def hide_game_won_menu(self):
        self.__game_won_menu.hide()

    def __create_game_lost_menu(self):
        dismiss_message = (
            f"Press {' or '.join(self.__dismiss_keys)} to return to the main "
            "menu"
        )
        return DismissiblePopUp(
            self.__window,
            None,
            textwrap.dedent(MESSAGES["game_lost_menu"]),
            DIMENSIONS["game_lost_menu"]["pady"],
            dismiss_message,
        )

    def show_game_lost_menu(self):
        self.__game_lost_menu.show()

    def hide_game_lost_menu(self):
        self.__game_lost_menu.hide()

    def __forward_keystroke_to_controller(self, event):
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

    def update_hp_gauge(self):
        # FIXME: Retrieve current adventurer HP from Model
        current_hp = 72

        self.__hp_gauge.set(current_hp)

    def __create_map(self):
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

    def update_map(self):
        # FIXME: Grab the Rooms objects from the model here
        MAP_EXAMPLE = """
        *  *  **  *  **  *  **  *  **  *  **  *  **  *  *
        *  P  ||     ||     ||     ||  I  **@ i  **     *
        *  -  **  *  **  *  **  *  **  -  **  -  **  -  *
        *  -  **  *  **  *  **  *  **  -  **  -  **  -  *
        *  X  ||  V  ||  X  **  V  ||     **     ||     *
        *  *  **  *  **  -  **  -  **  -  **  *  **  -  *
        *  *  **  *  **  -  **  -  **  -  **  *  **  -  *
        *  H  ||  M  **  H  **  O  **     ||  H  **     *
        *  -  **  *  **  -  **  -  **  *  **  *  **  -  *
        *  -  **  *  **  -  **  -  **  *  **  *  **  -  *
        *  A  ||     **     **     **     ||  H  **     *
        *  -  **  -  **  -  **  -  **  -  **  -  **  -  *
        *  -  **  -  **  -  **  -  **  -  **  -  **  -  *
        *     **     ||  H  **     ||     **  H  ||  H  *
        *  *  **  *  **  *  **  *  **  *  **  *  **  *  *
        """
        self.__map.contents = textwrap.dedent(MAP_EXAMPLE)

    def __create_side_bar(self):
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

        inventory_item_labels = (
            "Health Potion",
            "Suggestion Potion",
            "Vision Potion",
            "Magic Key",
        )

        dims_inventory = DIMENSIONS["inventory"]
        inventory = EnumeratedInventory(
            window=side_bar.frame,
            title="Inventory",
            title_ipady=DIMENSIONS["inventory_title"]["ipady"],
            padx=dims_inventory["padx"],
            pady=dims_inventory["pady"],
            item_labels=inventory_item_labels,
        )

        pillars_item_labels = (
            "Abstraction",
            "Encapsulation",
            "Inheritance",
            "Polymorphism",
        )

        dims_pillars = DIMENSIONS["pillars"]
        pillars_inventory = CheckboxInventory(
            window=side_bar.frame,
            title="Pillars of OOP",
            title_ipady=DIMENSIONS["pillars_title"]["ipady"],
            padx=dims_pillars["padx"],
            pady=dims_pillars["pady"],
            item_labels=pillars_item_labels,
        )

        return hp_gauge, inventory, pillars_inventory

    def __create_map_legend_menu(
        self,
        num_cols=2,
    ):
        symbol_overrides = {" ": "<space>"}
        legend_rows = self.__generate_rows_for_multicolumn_display(
            symbols=ROOM_CONTENT_SYMBOLS.values(),
            descriptions=ROOM_CONTENT_SYMBOLS.keys(),
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
            DIMENSIONS["map_legend_menu"]["pady"],
            dismiss_message,
        )

    @staticmethod
    def __generate_rows_for_multicolumn_display(
        symbols, descriptions, num_cols, symbol_overrides
    ):
        # Determine longest description and symbol strings
        symbol_max_len = len(max(symbols, key=len))
        if symbol_overrides:
            symbol_max_len = max(
                symbol_max_len,
                len(max(symbol_overrides.values(), key=len)),
            )
        description_max_len = len(max(descriptions, key=len))

        entries = deque()

        for symbol, description in zip(symbols, descriptions):
            # Special handling to account for space character (empty room)
            if symbol in symbol_overrides:
                symbol = symbol_overrides[symbol]

            entries.append(
                f"{symbol:>{symbol_max_len}}: {description:<{description_max_len}}"
            )

        max_width_of_one_row = num_cols * len(entries[0])

        rows = []
        row = 0
        while entries:
            # Pop off next element and put in next column
            for col in range(num_cols):
                if col == 0:
                    # Begin string for this row
                    rows.append("")

                rows[row] += entries.popleft()

                if col == num_cols - 1:
                    # Begin new row
                    row += 1

                # Pad the bottom row to the right with spaces
                if not entries:
                    rows[row] = rows[row].ljust(max_width_of_one_row)
                    break

        return rows

    def show_map_legend_menu(self):
        self.__map_legend_menu.show()

    def hide_map_legend_menu(self):
        self.__map_legend_menu.hide()

    def __create_command_legend_menu(self):
        dismiss_message = (
            f"Press {' or '.join(self.__dismiss_keys)} to return to the "
            "in-game menu"
        )
        return DismissiblePopUp(
            self.__window,
            None,
            None,
            DIMENSIONS["command_legend_menu"]["pady"],
            dismiss_message,
        )

    def show_command_legend_menu(self, symbols, descriptions, num_cols):
        """
        Fills the commands help pop-up based on a dict containing command
        keystrokes and their description, then displays it on top of the
        primary interface.

        Parameters
        ----------
        commands_info : tuple of dict
            Each entry is a dict containing the keys 'key' (which indicates the
            command keystroke) and 'description' (which indicates the
            description to display for that keystroke.)
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
        self.__command_legend_menu.hide()

    def __create_event_log(self):
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
        self.__event_log.write(message)

    def update(self):
        # FIXME: Implement this
        pass

    def pose_question_and_get_answer(self):
        # FIXME: Implement this
        pass

    def quit_entire_game(self):
        self.__window.destroy()
