"""Used to define dimensions, messages, and styles for view"""

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
    "main_help_menu": {"pady": 5},
    "map_legend_menu": {"pady": 5},
    "commands_help_menu": {"pady": 5},
    "game_won_menu": {"pady": 5},
    "game_lost_menu": {"pady": 5},
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
}

##############################################################################
# Symbols used to represent things in the map
##############################################################################
ROOM_CONTENT_SYMBOLS = {
    "Entrance": "i",
    "Exit": "o",
    "Adventurer": "@",
    "Pit": "X",
    "Healing Potion": "H",
    "Vision Potion": "V",
    "Multiple Items": "M",
    "Pillar of Abstraction": "A",
    "Pillar of Inheritance": "I",
    "Pillar of Encapsulation": "E",
    "Pillar of Polymorphism": "P",
    "Magic Key": "K",
    "Empty room": " ",
}

##############################################################################
# Keyboard sequences that need to be communicated to the user
##############################################################################
# FIXME: This should be done away with. The controller should simply tell the
# view to display the relevant components' strings with the keys it expects to
# be pressed. Or, since the view has a reference to the controller, it could
# just access the keys for different actions directly.
KEYS = {
    "game_won_menu": {"dismiss": "Return"},
    "game_lost_menu": {"dismiss": "Return"},
    "main_help_menu": {"dismiss": "Return"},
    "map_legend_menu": {"dismiss": "Return"},
    "commands_help_menu": {"dismiss": "Return"},
}


##############################################################################
# All styles to register with tk
##############################################################################
STYLES = {
    "main_menu": {"style": "main_menu.TLabel", "font": ("Courier New", 16)},
    "map": {"style": "map.TLabel", "font": ("Courier New", 26, "bold")},
    "game_won_menu": {"style": "game_won.TLabel", "font": ("Courier New", 16)},
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
}
