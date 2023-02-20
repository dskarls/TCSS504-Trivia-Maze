from abc import ABC, abstractmethod
from enum import Enum, auto

from text_trivia_maze_view import TextTriviaMazeView


class TriviaMazeModelObserver(ABC):
    def __init__(self, maze_model):
        self._maze_model = maze_model

    @abstractmethod
    def update(self):
        pass


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

    __COMMAND_DESC_KEY = "description"
    __COMMAND_KEY_KEY = "key"
    __COMMAND_TYPE = "type"
    __COMMAND_TYPE_MOVEMENT = "movement"
    __COMMAND_TYPE_ITEM = "item"
    __COMMAND_TYPE_OTHER = "other"
    __COMMAND_TYPE_HIDDEN = "hidden"

    class __Command(Enum):
        """Enumeration used to fix commands to a small finite support set."""

        # Movement commands
        MOVE_EAST = auto()
        MOVE_NORTH = auto()
        MOVE_WEST = auto()
        MOVE_SOUTH = auto()

        # Item commands
        USE_HEALING_POTION = auto()
        USE_VISION_POTION = auto()
        USE_MAGIC_KEY = auto()

        # Other commands
        PRINT_HELP_MENU = auto()
        QUIT_GAME = auto()

        # Hidden commands (don't show up in help menu)
        SHOW_FULL_MAP = auto()

    __COMMANDS = {
        # Movement commands
        __Command.MOVE_EAST: {
            __COMMAND_TYPE: __COMMAND_TYPE_MOVEMENT,
            __COMMAND_DESC_KEY: "Move east",
            __COMMAND_KEY_KEY: "Right",
        },
        __Command.MOVE_NORTH: {
            __COMMAND_TYPE: __COMMAND_TYPE_MOVEMENT,
            __COMMAND_DESC_KEY: "Move north",
            __COMMAND_KEY_KEY: "Up",
        },
        __Command.MOVE_WEST: {
            __COMMAND_TYPE: __COMMAND_TYPE_MOVEMENT,
            __COMMAND_DESC_KEY: "Move west",
            __COMMAND_KEY_KEY: "Left",
        },
        __Command.MOVE_SOUTH: {
            __COMMAND_TYPE: __COMMAND_TYPE_MOVEMENT,
            __COMMAND_DESC_KEY: "Move south",
            __COMMAND_KEY_KEY: "Down",
        },
        # Item commands
        __Command.USE_HEALING_POTION: {
            __COMMAND_TYPE: __COMMAND_TYPE_ITEM,
            __COMMAND_DESC_KEY: "Use healing potion",
            __COMMAND_KEY_KEY: "p",
        },
        __Command.USE_VISION_POTION: {
            __COMMAND_TYPE: __COMMAND_TYPE_ITEM,
            __COMMAND_DESC_KEY: "Use vision potion",
            __COMMAND_KEY_KEY: "v",
        },
        __Command.USE_MAGIC_KEY: {
            __COMMAND_TYPE: __COMMAND_TYPE_ITEM,
            __COMMAND_DESC_KEY: "Use magic key",
            __COMMAND_KEY_KEY: "k",
        },
        # Other commands
        __Command.PRINT_HELP_MENU: {
            __COMMAND_TYPE: __COMMAND_TYPE_OTHER,
            __COMMAND_DESC_KEY: "Print help menu",
            __COMMAND_KEY_KEY: "h",
        },
        __Command.QUIT_GAME: {
            __COMMAND_TYPE: __COMMAND_TYPE_OTHER,
            __COMMAND_DESC_KEY: "Quit game",
            __COMMAND_KEY_KEY: "q",
        },
        # Hidden commands
        __Command.SHOW_FULL_MAP: {
            __COMMAND_TYPE: __COMMAND_TYPE_HIDDEN,
            __COMMAND_DESC_KEY: "Display full map",
            __COMMAND_KEY_KEY: "z",
        },
    }

    def __init__(self, maze_model):
        super().__init__(maze_model)

        # Create a view object
        self.__maze_view = TextTriviaMazeView(maze_model, self, "Trivia Maze")

        # Initialize command interpretation contexts
        self.__main_menu_context = MainMenuCommandContext(
            self, self._maze_model, self.__maze_view
        )

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
        if context_specifier == "main_menu":
            self.__active_context = self.__main_menu_context

    def update(self):
        # FIXME: Implement what should happen here when model changes
        pass


class CommandContext(ABC):
    """
    Interprets keystrokes within a specific context. For example, one context
    might be the main menu while one could be the primary game interface.
    """

    def __init__(self, maze_controller, maze_model, maze_view):
        self._maze_controller = maze_controller
        self._maze_model = maze_model
        self._maze_view = maze_view

    @abstractmethod
    def process_keystroke(self, key):
        """Interpret a keystroke and perform the relevant actions on the model
        and view based on the current context."""


class MainMenuCommandContext(CommandContext):
    def process_keystroke(self, key):
        # NOTE: We ignore arrow keys here since the GUI is responsible for
        # having arrow keys traverse the menu. In fact, we actually only care
        # about the user hitting Return inside of this menu.
        if key != "Return":
            return

        # Trigger the currently selected item in the main menu
        selected_option = self._maze_view.get_main_menu_current_selection()

        # NOTE: One might choose to have the controller tell the view what options
        # to add to the menu when it creates it in order to avoid duplication
        if selected_option == "Start game":
            # FIXME: Implement a difficulty selection and/or adventurer naming
            # menu and have the user go through that here. This may mean we
            # need to break up the stuff in the model's initialization so that
            # its __init__ doesn't really do anything.

            # Hide main menu so user can begin playing and switch contexts
            self._maze_view.hide_main_menu()

            self._maze_controller.set_active_context("primary_interface")

        elif selected_option == "Help":
            self._maze_view.show_main_menu_help()
            self._maze_controller.set_active_context("main_menu_help")

        elif selected_option == "Quit game":
            # Exit out of everything and close the window
            self._maze_view.quit_entire_game()
