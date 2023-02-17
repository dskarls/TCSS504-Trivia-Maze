import os
from abc import ABC, abstractmethod
import textwrap

from tkinter import *
from tkinter.ttk import *

from view_config import DIMENSIONS, MESSAGES, KEYS, STYLES
from view_components import (
    MainMenu,
    InGameMenu,
    DismissiblePopUp,
    Map,
    SideBar,
    EventLog,
)


class TriviaMazeView(ABC):
    """
    A view to display the trivia maze game to the user and gather input
    commands.
    """

    def __init__(self, maze_controller):
        self.__maze_controller = maze_controller

    @abstractmethod
    def show_main_menu(self):
        """Display the main menu"""

    @abstractmethod
    def hide_main_menu(self):
        """Hide the main menu"""

    @abstractmethod
    def show_in_game_menu(self):
        """Show the in-game menu pop-up"""

    @abstractmethod
    def hide_in_game_menu(self):
        """Hide the in-game menu pop-up"""

    @abstractmethod
    def pose_question_and_get_answer(self, question_and_answer):
        """Show the user a question-and-answer pop-up and retrieve the
        answer, then hide the pop-up."""

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


class TextTriviaMazeView:
    """A text-based view for the Trivia Maze application that uses tkinter
    (specifically, themed-tkinter aka "ttk").

    NOTE: Currently, the size is fixed upon creation.
    NOTE: The primary interface (the map, hp gauge, inventory, and event log)
    is technically always shown. The main menu simply consists of overlaying
    the main menu window over the top of the primary interface. Showing the
    primary interface then simply amounts to hiding the main menu (or pop-ups).
    """

    def __init__(self, title, theme_path=None, theme_name=None):
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
        self.__hp_gauge, self.__inventory = self.__add_hp_gauge_and_inventory()
        self.__event_log = self.__create_event_log()

        # Create game won/lost menus
        self.__game_won_menu = self.__create_game_won_menu()
        self.hide_game_won_menu()
        self.__game_lost_menu = self.__create_game_lost_menu()
        self.hide_game_lost_menu()

        # Set up in-game menu
        self.__in_game_menu = self.__create_in_game_menu()
        self.hide_in_game_menu()

        # Create main menu
        self.__main_menu = self.__create_main_menu()
        self.show_main_menu()

        # Prevent resizing
        self.__window.resizable(False, False)

        # Intercept keystrokes from user
        self.__configure_keystroke_capture()

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

    def show_main_menu(self):
        self.__main_menu.show()

    def __create_in_game_menu(self):
        options = (
            "Back to Game",
            "Display Map Legend",
            "Display Commands",
            "Quit Game",
        )
        return InGameMenu(
            self.__window,
            DIMENSIONS["in_game_menu"]["width"],
            "In-Game Menu",
            DIMENSIONS["in_game_menu_title"]["pady"],
            options,
        )

    def show_in_game_menu(self):
        self.__in_game_menu.show()

    def hide_in_game_menu(self):
        self.__in_game_menu.hide()

    def __create_game_won_menu(self):
        return DismissiblePopUp(
            self.__window,
            None,
            textwrap.dedent(MESSAGES["game_won_menu"]),
            DIMENSIONS["game_won_menu"]["pady"],
            KEYS["game_won_menu"]["dismiss"],
        )

    def show_game_won_menu(self):
        self.__game_won_menu.show()

    def hide_game_won_menu(self):
        self.__game_won_menu.hide()

    def __create_game_lost_menu(self):
        return DismissiblePopUp(
            self.__window,
            None,
            textwrap.dedent(MESSAGES["game_lost_menu"]),
            DIMENSIONS["game_lost_menu"]["pady"],
            KEYS["game_lost_menu"]["dismiss"],
        )

    def show_game_lost_menu(self):
        self.__game_lost_menu.show()

    def hide_game_lost_menu(self):
        self.__game_lost_menu.hide()

    def __forward_keystroke_to_controller(self, event):
        # For regular keys
        key = event.char

        # If char was empty, check to see if it was an arrow key
        if not key or key in os.linesep:
            key = event.keysym

        if key:
            # If keysym wasn't empty, forward it to controller. Otherwise, just
            # ignore it since it's not a supported key command.

            # FIXME: This should really be sent to the controller. Just writing to
            # the event log here for demonstration purposes.
            self.write_to_event_log(f"You pressed {key}")

    def update_hp_gauge(self):
        # FIXME: Retrieve current adventurer HP from Model
        current_hp = 72

        self.__hp_gauge["value"] = current_hp

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
        # FIXME: Grab the map object from the model here
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

    def __add_hp_gauge_and_inventory(self):
        # Create inventory_labels
        inventory_item_labels = (
            "Health Potion",
            "Suggestion Potion",
            "Vision Potion",
            "Magic Key",
            "Pillar of Abstraction",
            "Pillar of Encapsulation",
            "Pillar of Inheritance",
            "Pillar of Polymorphism",
        )

        dims_side_bar = DIMENSIONS["side_bar"]
        dims_hp_gauge_bar = DIMENSIONS["hp_gauge_bar"]
        dims_inventory = DIMENSIONS["inventory"]

        side_bar = SideBar(
            window=self.__window,
            width=dims_side_bar["width"],
            height=DIMENSIONS["map"]["height"],
            row=0,
            column=1,
            rowspan=1,
            columnspan=1,
            padx=dims_side_bar["padx"],
            pady=dims_side_bar["pady"],
            hp_gauge_height=DIMENSIONS["hp_gauge"]["height"],
            hp_gauge_bar_width=dims_hp_gauge_bar["width"],
            hp_gauge_label_padx=DIMENSIONS["hp_gauge_label"]["padx"],
            hp_gauge_bar_padx=dims_hp_gauge_bar["padx"],
            hp_gauge_bar_pady=dims_hp_gauge_bar["pady"],
            inventory_title_ipady=DIMENSIONS["inventory_title"]["ipady"],
            inventory_padx=dims_inventory["padx"],
            inventory_pady=dims_inventory["pady"],
            inventory_item_labels=inventory_item_labels,
        )

        return side_bar.hp_gauge, side_bar.inventory

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


if __name__ == "__main__":
    view = TextTriviaMazeView("TriviaMaze")

    view.hide_main_menu()
    view.update_map()
    view.show_game_lost_menu()
    view.hide_game_lost_menu()
    for i in range(100):
        view.write_to_event_log(f"Here is message {i}")
    view.mainloop()
