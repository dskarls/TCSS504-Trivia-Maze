from abc import ABC, abstractmethod
import textwrap

from tkinter import *
from tkinter.ttk import *


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

    # Primary display config params
    __MAP_WIDTH = 800
    __MAP_HEIGHT = 500
    __SIDEBAR_WIDTH = 250
    __SIDEBAR_HORIZONTAL_PADDING = 15
    __HP_GAUGE_HEIGHT = 30
    __HP_GAUGE_BAR_WIDTH = int(0.8 * __SIDEBAR_WIDTH)
    __EVENT_LOG_HEIGHT = 50
    __EVENT_LOG_NUM_LINES = 10

    # In-game menu config params
    __IN_GAME_MENU_WIDTH = 200
    __IN_GAME_MENU_TITLE_VERTICAL_PADDING = 5
    __IN_GAME_MENU_OPTION_VERTICAL_PADDING = 5

    __YOU_WIN_MESSAGE = """
    _________________________________________________
        __   __                     _         _
        \ \ / /                    (_)       | |
         \ V /___  _   _  __      ___ _ __   | |
          \ // _ \| | | | \ \ /\ / / | '_ \  | |
          | | (_) | |_| |  \ V  V /| | | | | |_|
          \_/\___/ \__,_|   \_/\_/ |_|_| |_| (_)
    _________________________________________________
    """
    __YOU_DIED_MESSAGE = """
     ______     __   __                _ _          _
    /       \   \ \ / /               | (_)        | |
    | @   @ |    \ V /___  _   _    __| |_  ___  __| |
    \   0   /     \ // _ \| | | |  / _` | |/ _ \/ _` |
     |_|_|_|      | | (_) | |_| | | (_| | |  __/ (_| |
                  \_/\___/ \__,_|  \__,_|_|\___|\__,_|
    """

    # Keyboard inputs
    # FIXME: These should all be moved to the controller and accessed by the
    # view through its reference to the controller!
    __KEY_DISMISS_YOU_WIN_OR_GAME_LOST = "Return"

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

        # Set minimum row/col sizes to prevent frames from collapsing to their
        # contained content
        self.__window.rowconfigure(0, minsize=self.__MAP_HEIGHT)
        self.__window.columnconfigure(0, minsize=self.__MAP_WIDTH)
        self.__window.columnconfigure(1, minsize=self.__SIDEBAR_WIDTH)

        # Create primary interface windows
        # NOTE: These windows should be created first. Otherwise, the other
        # widgets will always be "hidden" behind them. You could also get
        # around this by using the 'lift()' and 'lower()' methods of the frame
        # widgets, but it's simpler just to make them in order.
        self.__map = self.__add_map()
        self.__hp_gauge, self.__inventory = self.__add_hp_gauge_and_inventory()
        self.__event_log = self.__add_event_log()

        # Create game won/lost menus
        self.__game_won_menu = self.__create_game_won_menu()
        self.__game_lost_menu = self.__create_game_lost_menu()

        # Set up in-game menu
        self.__in_game_menu = self.__create_in_game_menu()
        self.hide_in_game_menu()

        # Create main menu
        self.__main_menu = self.__create_main_menu()

        # Prevent resizing
        self.__window.resizable(False, False)

        # Intercept keystrokes from user
        self.__configure_keystroke_capture()

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
        return self.__add_subwindow(
            width=self.__MAP_WIDTH + self.__SIDEBAR_WIDTH,
            height=self.__MAP_HEIGHT + self.__EVENT_LOG_HEIGHT,
            row=0,
            column=0,
            rowspan=2,
            columnspan=2,
        )

    def hide_main_menu(self):
        self.__main_menu.grid_remove()

    def show_main_menu(self):
        self.__main_menu.grid()

    @staticmethod
    def __place_pop_up_at_center_of_window(frame, width):
        frame.place(
            relx=0.5,
            rely=0.5,
            anchor=CENTER,
            width=width,
        )

    def __create_pop_up_window(self, width):
        frm = Frame(
            master=self.__window,
            relief=RIDGE,
        )
        self.__place_pop_up_at_center_of_window(frm, width)
        return frm

    def __create_in_game_menu(self):
        # Create the frame for the whole in-game menu
        frm = self.__create_pop_up_window(self.__IN_GAME_MENU_WIDTH)

        # Create header with title in it
        frm_title = Frame(master=frm, relief=RIDGE)
        frm_title.pack(fill=BOTH, anchor=CENTER)
        lbl = Label(
            master=frm_title,
            text="In-Game Menu",
            justify=CENTER,
            anchor=CENTER,
        )
        lbl.pack(fill=BOTH, pady=self.__IN_GAME_MENU_TITLE_VERTICAL_PADDING)

        options = (
            "Display map legend",
            "Back to Game",
            "Quit Game",
        )
        for option in options:
            lbl = Label(master=frm, text=option, justify=CENTER, anchor=CENTER)
            lbl.pack(
                fill=BOTH,
                padx=self.__IN_GAME_MENU_OPTION_VERTICAL_PADDING,
                pady=self.__IN_GAME_MENU_OPTION_VERTICAL_PADDING,
            )
        return frm

    def show_in_game_menu(self):
        self.__in_game_menu.place(
            relx=0.5, rely=0.5, anchor=CENTER, width=self.__IN_GAME_MENU_WIDTH
        )

    def hide_in_game_menu(self):
        self.__in_game_menu.place_forget()

    def __create_message_menu_with_only_dismiss_option(
        self, text, dismiss_key, style_name
    ):
        frm = self.__create_pop_up_window(width=None)

        lbl = Label(
            master=frm,
            text=text,
            justify=CENTER,
            anchor=CENTER,
            style=style_name,
        )
        lbl.pack(fill=BOTH, pady=self.__IN_GAME_MENU_TITLE_VERTICAL_PADDING)

        # Put return to main menu option below
        lbl = Label(
            master=frm,
            text=f"Press [{dismiss_key}] to return to main menu",
            justify=CENTER,
            anchor=CENTER,
        )
        lbl.pack(
            fill=BOTH,
        )
        return frm

    def __create_game_won_menu(self):
        # TODO: Store all styles in a single place (possibly some kind of view
        # configuration class)
        style_name = "you_won.TLabel"
        sty = Style()
        sty.configure(style_name, font=("Courier New", 16))

        return self.__create_message_menu_with_only_dismiss_option(
            textwrap.dedent(self.__YOU_WIN_MESSAGE),
            self.__KEY_DISMISS_YOU_WIN_OR_GAME_LOST,
            style_name,
        )

    def __create_game_lost_menu(self):
        # TODO: Store all styles in a single place (possibly some kind of view
        # configuration class)
        style_name = "you_died.TLabel"
        sty = Style()
        sty.configure(style_name, font=("Courier New", 16))

        return self.__create_message_menu_with_only_dismiss_option(
            textwrap.dedent(self.__YOU_DIED_MESSAGE),
            self.__KEY_DISMISS_YOU_WIN_OR_GAME_LOST,
            style_name,
        )

    def __forward_keystroke_to_controller(self, event):
        # For regular keys
        key = event.char

        # If char was empty, check to see if it was an arrow key
        if not key:
            key = event.keysym

        if key:
            # If keysym wasn't empty, forward it to controller. Otherwise, just
            # ignore it since it's not a supported key command.

            # FIXME: This should really be sent to the controller. Just writing to
            # the event log here for demonstration purposes.
            self.write_to_event_log(f"You pressed {key}")

    def __add_subwindow(
        self, width, height, row, column, rowspan=1, columnspan=1
    ):
        frm = Frame(
            master=self.__window, width=width, height=height, relief=RIDGE
        )

        frm.grid(
            row=row,
            column=column,
            rowspan=rowspan,
            columnspan=columnspan,
            sticky="nsew",
        )

        return frm

    @staticmethod
    def __add_scrollable_readonly_textbox_to_subwindow(subwindow, num_lines):
        frm = subwindow
        scrlbar = Scrollbar(master=frm, orient=VERTICAL)
        scrlbar.pack(side=RIGHT, pady=5, fill=Y, padx=3)

        scrltxt = Text(
            master=frm,
            height=num_lines,
            yscrollcommand=scrlbar.set,
        )
        scrltxt.pack(fill=BOTH, pady=2)

        # Enable dragging of scroll bar now that text box exists (has to be
        # done in this order)
        scrlbar.config(command=scrltxt.yview)

        # Make text box read-only
        scrltxt.config(state=DISABLED)

    def update_hp_gauge(self):
        # FIXME: Retrieve current adventurer HP from Model
        current_hp = 72

        self.__hp_gauge["value"] = current_hp

    def __add_map(self):
        return self.__add_subwindow(self.__MAP_WIDTH, self.__MAP_HEIGHT, 0, 0)

    def __add_hp_gauge_and_inventory(self):
        # Create vertical sidebar frame
        frm_sidebar = self.__add_subwindow(
            width=self.__SIDEBAR_WIDTH,
            height=self.__MAP_HEIGHT,
            row=0,
            column=1,
        )

        # Create frame to hold hp gauge label and bar
        frm_hp = Frame(master=frm_sidebar, height=self.__HP_GAUGE_HEIGHT)
        frm_hp.grid(
            row=0,
            column=0,
            padx=self.__SIDEBAR_HORIZONTAL_PADDING,
            pady=15,
            sticky="nsew",
        )

        # Create label for hp gauge
        lbl_hp_gauge = Label(master=frm_hp, text="HP ")
        lbl_hp_gauge.pack(side=LEFT)

        # Create bar for hp gauge
        bar_hp_gauge = Progressbar(
            master=frm_hp,
            orient=HORIZONTAL,
            length=self.__HP_GAUGE_BAR_WIDTH,
            mode="determinate",
        )
        bar_hp_gauge.pack(side=LEFT)
        bar_hp_gauge["value"] = 100

        # Create label for inventory
        lbl_inventory = Label(
            master=frm_sidebar,
            text="Inventory",
            relief=RIDGE,
            anchor=CENTER,
        )
        lbl_inventory.grid(sticky="nsew", pady=(5, 10))

        inventory_quantity_labels = self.__create_inventory_item_labels(
            frm_sidebar, self.__SIDEBAR_HORIZONTAL_PADDING
        )

        return bar_hp_gauge, inventory_quantity_labels

    @staticmethod
    def __create_inventory_item_labels(frm, padx):
        # Create inventory_labels
        item_labels = (
            "Health Potion",
            "Suggestion Potion",
            "Vision Potion",
            "Magic Key",
            "Pillar of Abstraction",
            "Pillar of Encapsulation",
            "Pillar of Inheritance",
            "Pillar of Polymorphism",
        )
        inventory_quantity_labels = {}
        for item in item_labels:
            # Create frame for this item
            frm_item = Frame(master=frm)
            frm_item.grid(sticky="nsew", padx=padx, pady=10)

            # Create label for item
            lbl_item = Label(master=frm_item, text=item)
            lbl_item.pack(side=LEFT, padx=padx)

            # Create label holding quantity of item
            lbl_quantity = Label(master=frm_item, text="0")
            lbl_quantity.pack(side=RIGHT, padx=padx)

            inventory_quantity_labels[item] = lbl_quantity

        return inventory_quantity_labels

    def __add_event_log(self):
        # event_log_name = "event log"
        frm = self.__add_subwindow(
            None, self.__EVENT_LOG_HEIGHT, 1, 0, columnspan=2
        )
        self.__add_scrollable_readonly_textbox_to_subwindow(
            frm, self.__EVENT_LOG_NUM_LINES
        )
        return frm

    def write_to_event_log(self, message):
        event_log_text_box = self.__event_log.children["!text"]

        # Make text box writable for a brief instant, write to it, then make it
        # read-only again
        event_log_text_box.config(state=NORMAL)
        event_log_text_box.insert(END, message + "\n")
        event_log_text_box.config(state=DISABLED)

        # Scroll down as far as possible
        event_log_text_box.yview(END)


if __name__ == "__main__":
    view = TextTriviaMazeView("TriviaMaze")

    for i in range(100):
        view.write_to_event_log(f"Here is message {i}")
    view.mainloop()
