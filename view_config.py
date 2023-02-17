"""Used to define dimensions, messages, and styles for view"""

##############################################################################
# Dimensions such as width, height, and padding options
##############################################################################
DIMENSIONS = {
    "map": {"width": 900, "height": 500, "padx": 5},
    "sidebar": {"width": 250},
    "hp_gauge": {"height": 30},
    "hp_gauge_bar": {"width": int(0.8 * 30)},
    "event_log": {"height": 10},
    "in_game_menu": {"width": 400},
    "in_game_menu_title": {"pady": 5},
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

MESSAGES = {
    "main_menu": __WELCOME_MESSAGE,
    "game_won_menu": __YOU_WIN_MESSAGE,
    "game_lost_menu": __YOU_DIED_MESSAGE,
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
}


# All styles to register with tk
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
}