"""Used to define dimensions, messages, and styles for view"""
from enum import Enum, auto

##############################################################################
# Dimensions such as width, height, and padding options
##############################################################################
DIMENSIONS = {
    "map": {"width": 850, "height": 500, "padx": 5},
    "side_bar": {"width": 250, "padx": 0, "pady": 5},
    "hp_gauge": {"height": 30},
    "hp_gauge_label": {"padx": 5},
    "hp_gauge_bar": {"width": int(0.7 * 250), "padx": 5, "pady": 15},
    "event_log": {"height": 10, "padx": 3, "pady": 5},
    "in_game_menu": {"width": 400},
    "in_game_menu_title": {"pady": 5},
    "inventory": {"padx": 10, "pady": 8},
    "inventory_title": {"ipady": 10},
    "pillars": {"padx": 10, "pady": 8},
    "pillars_title": {"ipady": 10},
    # Dismissible popups
    "main_help_menu": {"ipadx": 10, "ipady": 8},
    "map_legend_menu": {"ipadx": 10, "ipady": 10},
    "command_legend_menu": {"ipadx": 10, "ipady": 10},
    "need_magic_key_menu": {"ipadx": 10, "ipady": 10},
    "game_won_menu": {"ipadx": 10, "ipady": 10},
    "game_lost_menu": {"ipadx": 10, "ipady": 10},
    "question_and_answer_menu": {"ipadx": 10, "ipady": 10},
}

##############################################################################
# Static messages for menus/popups
##############################################################################
__WELCOME_MESSAGE = """
_______________________________________________________
/_______________________________________________________\\
|               _____    _       _                       |
|              |_   _|  (_)     (_)                      |
|                | |_ __ ___   ___  __ _                 |
|                | | '__| \ \ / / |/ _` |                |
|                | | |  | |\ V /| | (_| |                |
|                \_/_|  |_| \_/ |_|\__,_|                |
|                                                        |
|                 ___  ___                               |
|                 |  \/  |                               |
|                 | .  . | __ _ _______                  |
|                 | |\/| |/ _` |_  / _ \                 |
|                 | |  | | (_| |/ /  __/                 |
|                 \_|  |_/\__,_/___\___|                 |
|                                                        |
\________________________________________________________/

     By Daniel S. Karls, Sheehan Smith, Tom J. Swanson
"""
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
__MAIN_HELP_MESSAGE = """
Your goal is to collect all four pillars of OOP and safely reach the exit of
the maze. The doors of many rooms will be locked and attempting to go through
them will pose a question you must answer in order to unlock them. If you
answer incorrectly, the door will be locked permanently and you must attempt to
find a magic key to unlock it. A suggestion potion, if currently held, can be
used to get hints to questions. Along the way, you may fall in pits and take
damage. However, healing potions can also be found throughout the maze.

Good luck!
"""

MESSAGES = {
    "main_menu": __WELCOME_MESSAGE,
    "main_help_menu": __MAIN_HELP_MESSAGE,
    "game_won_menu": __YOU_WIN_MESSAGE,
    "game_lost_menu": __YOU_DIED_MESSAGE,
    "need_magic_key_menu": "This door is permanently locked. To open it, find a magic key!",
}


##############################################################################
# Symbols used to represent things in the map
##############################################################################
class RoomContents(Enum):
    """Enumeration of the different contents of a room: entrance, exit,
    pit, potions, pillars, or nothing. This is defined in lieu of using
    global variables so that the same variables can be used throughout all
    calling modules and herein to refer to this finite set of possible
    values."""

    ENTRANCE = auto()
    EXIT = auto()

    ADVENTURER = auto()

    PIT = auto()

    HEALING_POTION = auto()
    VISION_POTION = auto()
    SUGGESTION_POTION = auto()
    MULTIPLE_ITEMS = auto()
    ABSTRACTION_PILLAR = auto()
    INHERITANCE_PILLAR = auto()
    ENCAPSULATION_PILLAR = auto()
    POLYMORPHISM_PILLAR = auto()
    MAGIC_KEY = auto()

    EMPTY = auto()


# Symbols that are placed in the string representation of a room to
# indicate its contents
ROOM_CONTENT_SYMBOL_KEY = "symbol"
ROOM_CONTENT_DESC_KEY = "description"
ROOM_CONTENT_SYMBOLS = {
    RoomContents.ENTRANCE: {
        ROOM_CONTENT_SYMBOL_KEY: "i",
        ROOM_CONTENT_DESC_KEY: "Entrance",
    },
    RoomContents.EXIT: {
        ROOM_CONTENT_SYMBOL_KEY: "O",
        ROOM_CONTENT_DESC_KEY: "Exit",
    },
    RoomContents.ADVENTURER: {
        ROOM_CONTENT_SYMBOL_KEY: "@",
        ROOM_CONTENT_DESC_KEY: "Adventurer",
    },
    RoomContents.PIT: {
        ROOM_CONTENT_SYMBOL_KEY: "X",
        ROOM_CONTENT_DESC_KEY: "Pit",
    },
    RoomContents.HEALING_POTION: {
        ROOM_CONTENT_SYMBOL_KEY: "H",
        ROOM_CONTENT_DESC_KEY: "Healing Potion",
    },
    RoomContents.VISION_POTION: {
        ROOM_CONTENT_SYMBOL_KEY: "V",
        ROOM_CONTENT_DESC_KEY: "Vision Potion",
    },
    RoomContents.SUGGESTION_POTION: {
        ROOM_CONTENT_SYMBOL_KEY: "S",
        ROOM_CONTENT_DESC_KEY: "Suggestion Potion",
    },
    RoomContents.MULTIPLE_ITEMS: {
        ROOM_CONTENT_SYMBOL_KEY: "M",
        ROOM_CONTENT_DESC_KEY: "Multiple items",
    },
    RoomContents.ABSTRACTION_PILLAR: {
        ROOM_CONTENT_SYMBOL_KEY: "A",
        ROOM_CONTENT_DESC_KEY: "Abstraction Pillar",
    },
    RoomContents.INHERITANCE_PILLAR: {
        ROOM_CONTENT_SYMBOL_KEY: "I",
        ROOM_CONTENT_DESC_KEY: "Inheritance Pillar",
    },
    RoomContents.ENCAPSULATION_PILLAR: {
        ROOM_CONTENT_SYMBOL_KEY: "E",
        ROOM_CONTENT_DESC_KEY: "Encapsulation Pillar",
    },
    RoomContents.POLYMORPHISM_PILLAR: {
        ROOM_CONTENT_SYMBOL_KEY: "P",
        ROOM_CONTENT_DESC_KEY: "Polymorphism Pillar",
    },
    RoomContents.MAGIC_KEY: {
        ROOM_CONTENT_SYMBOL_KEY: "K",
        ROOM_CONTENT_DESC_KEY: "Magic Key",
    },
    RoomContents.EMPTY: {
        ROOM_CONTENT_SYMBOL_KEY: " ",
        ROOM_CONTENT_DESC_KEY: "Empty room",
    },
}


class RoomSides(Enum):
    WALL = auto()
    DOOR_NORTH_SOUTH = auto()
    DOOR_EAST_WEST = auto()
    DOOR_LOCKED = auto()
    DOOR_PERMANENTLY_LOCKED = auto()


# Symbols that are placed in the string representation of a room to
# indicate its contents
ROOM_SIDE_SYMBOL_KEY = "symbol"
ROOM_SIDE_DESC_KEY = "description"
ROOM_SIDE_SYMBOLS = {
    RoomSides.WALL: {
        ROOM_SIDE_SYMBOL_KEY: "*",
        ROOM_SIDE_DESC_KEY: "Wall",
    },
    RoomSides.DOOR_NORTH_SOUTH: {
        ROOM_SIDE_SYMBOL_KEY: "_",
        ROOM_SIDE_DESC_KEY: "Door",
    },
    RoomSides.DOOR_EAST_WEST: {
        ROOM_SIDE_SYMBOL_KEY: "|",
        ROOM_SIDE_DESC_KEY: "Door",
    },
    RoomSides.DOOR_LOCKED: {
        ROOM_SIDE_SYMBOL_KEY: "L",
        ROOM_SIDE_DESC_KEY: "Locked Door",
    },
    RoomSides.DOOR_PERMANENTLY_LOCKED: {
        ROOM_SIDE_SYMBOL_KEY: "P",
        ROOM_SIDE_DESC_KEY: "Permanently Door",
    },
}


##############################################################################
# All styles to register with tk
##############################################################################
STYLES = {
    "main_menu": {"style": "main_menu.TLabel", "font": ("Courier New", 16)},
    "map": {"style": "map.TLabel", "font": ("Courier New", 26, "bold")},
    "hp_gauge_label": {
        "style": "hp_gauge_label.TLabel",
        "font": ("Arial", 16, "bold"),
    },
    "inventory_title": {
        "style": "inventory_title.TLabel",
        "font": ("Arial", 16, "bold"),
    },
    "inventory_item": {
        "style": "inventory_item.TLabel",
        "font": ("Arial", 15, "bold"),
    },
    "pillars_title": {
        "style": "pillars_title.TLabel",
        "font": ("Arial", 16, "bold"),
    },
    "pillars_item": {
        "style": "pillars_item.TLabel",
        "font": ("Arial", 15, "bold"),
    },
    # Dismissible popups
    "dismiss_text": {
        "style": "dismissible_text.TLabel",
        "font": ("Courier New", 18, "bold"),
    },
    "dismiss_bottom_label": {
        "style": "dismiss_bottom_label.TLabel",
        "font": ("Arial", 15),
    },
}
