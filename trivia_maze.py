from collections import deque
from enum import Enum, auto
import sys
import textwrap

from adventurer import Adventurer, InvalidAdventurerName
from maze import Maze
from maze_map import MazeMap
from room import Room


class TriviaMaze:
    """
    Driver for maze adventure game

    NOTE: There is a hidden command, currently set to the key 'z' that can be
    used to display the entire maze at any iteration of the game.

    Class Attributes
    ------------------
    __COMMAND_DESC_KEY : str
    __COMMAND_KEY_KEY : str
    __COMMAND_TYPE : str
    __COMMAND_TYPE_MOVEMENT : str
    __COMMAND_TYPE_ITEM : str
    __COMMAND_TYPE_DISPLAY : str
    __COMMAND_TYPE_OTHER : str
    __COMMAND_TYPE_HIDDEN : str
        All of the above are used in defining the __COMMANDS class attr.
    __COMMANDS : dict
        Contains information about each command, including its type and
        description.
    __CONSOLE_WIDTH : int
        Width of terminal used to play game.
    __DEFAULT_NUM_ROWS : int
        Number of rows to use if user skips through rows prompt.
    __DEFAULT_NUM_COLS: int
        Number of columns to use if user skips through rows prompt.
    __WELCOME_MESSAGE : str
        String to print when game is started.
    __YOU_DIED_MESSAGE : str
        String to print when adventurer dies.
    __YOU_WIN_MESSAGE : str
        String to print when adventurer wins the game.

    Instance Attributes
    ------------------
    __adventurer : Adventurer
        An adventurer that is initialized to traverse the maze.
    __adventurer_current_row : int
        Current x coordinate (row) of the adventurer
    __adventurer_current_col : int
        Current y coordinate (column) of the adventurer.
    __maze : Maze
        Two-dimensional array of Room objects that comprise the maze. They are
        located in the array according to their two-dimensional coords, e.g. the
        Room at indices [1][2] corresponds to row 1, column 2 (both zero-based
        indexing).
    __maze_map : MazeMap
        A map of the maze that displays what rooms the adventurer has either
        visited or revealed using a vision potion.
    __maze_map_filled_in : MazeMap
        A map of the maze that displays all current rooms and items.

    Methods
    -------
    __create_adventurer
        Create an adventurer
    __get_adjacent_rooms_in_maze
        Get a list of all rooms in the maze that are adjacent to the
        adventurer's current room.
    __get_num_rows_and_cols_from_user
        Get the number of rows and columns from the user that they want to use
        to build the maze.
    __print_instructions
        Display the instructions at the beginning of the game.
    __print_help_menu
        Display the help menu of command keys
    __play_game
        Start the game
    __move_and_get_next_room
        Move the adventurer around the maze
    __apply_pit_damage_to_adventurer
        Apply the damage value of a pit to an adventurer when they step into
        it.
    """

    # NOTE: Welcome string generated using https://patorjk.com/ using the
    # 'Doom' style.
    __WELCOME_MESSAGE = """
  ______________________________________________________
 /                                                      \\
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
 \______________________________________________________/

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

    __MAZE_MAP_FILLED_IN_MESSAGE = "Here's what the whole maze looked like:"

    # How many char columns we have in the terminal. Used for choosing length
    # of horizontal rules and text wraps.
    __CONSOLE_WIDTH = 79

    __DEFAULT_NUM_ROWS = 3
    __DEFAULT_NUM_COLS = 3

    __COMMAND_DESC_KEY = "description"
    __COMMAND_KEY_KEY = "key"
    __COMMAND_TYPE = "type"
    __COMMAND_TYPE_MOVEMENT = "movement"
    __COMMAND_TYPE_ITEM = "item"
    __COMMAND_TYPE_DISPLAY = "display"
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

        # Display commands
        SHOW_ADVENTURER_STATUS = auto()
        SHOW_MAP = auto()

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
            __COMMAND_KEY_KEY: "d",
        },
        __Command.MOVE_NORTH: {
            __COMMAND_TYPE: __COMMAND_TYPE_MOVEMENT,
            __COMMAND_DESC_KEY: "Move north",
            __COMMAND_KEY_KEY: "w",
        },
        __Command.MOVE_WEST: {
            __COMMAND_TYPE: __COMMAND_TYPE_MOVEMENT,
            __COMMAND_DESC_KEY: "Move west",
            __COMMAND_KEY_KEY: "a",
        },
        __Command.MOVE_SOUTH: {
            __COMMAND_TYPE: __COMMAND_TYPE_MOVEMENT,
            __COMMAND_DESC_KEY: "Move south",
            __COMMAND_KEY_KEY: "s",
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
        # Display commands
        __Command.SHOW_ADVENTURER_STATUS: {
            __COMMAND_TYPE: __COMMAND_TYPE_DISPLAY,
            __COMMAND_DESC_KEY: "Display adventurer status",
            __COMMAND_KEY_KEY: "i",
        },
        __Command.SHOW_MAP: {
            __COMMAND_TYPE: __COMMAND_TYPE_DISPLAY,
            __COMMAND_DESC_KEY: "Display maze map",
            __COMMAND_KEY_KEY: "m",
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

    def __init__(self):
        self.__print_instructions()

        num_rows, num_col = self.__get_num_rows_and_cols_from_user()
        self.__maze = Maze(num_rows, num_col)
        self.__maze_map = MazeMap(num_rows, num_col)

        # Also keep a maze map that is filled in entirely here and gets
        # updated as the adventurer walks through the maze
        self.__maze_map_filled_in = MazeMap(num_rows, num_col)
        for room_row in self.__maze.rooms:
            for room in room_row:
                self.__maze_map_filled_in.update_room(room)

        self.__adventurer = self.__create_adventurer()

        print("\nCurrent status")
        print(self.__adventurer)

        # NOTE: adventurer coordinate attrs are set inside play_game()
        self.__adventurer_current_row, self.__adventurer_current_col = (
            None,
            None,
        )

        # Start the game
        self.__play_game()

    def __get_num_rows_and_cols_from_user(self):
        """Prompt user for desired number of rows and columns. If user skips
        through dialogue, use default values.

        Returns
        -------
        tuple
            The number of rows and columns to use to create maze maze.
        """
        row_str = input("Enter the desired number of rows in the maze (default: 3): ")
        try:
            num_rows = int(row_str.strip())
        except ValueError:
            num_rows = self.__DEFAULT_NUM_ROWS

        col_str = input(
            "Enter the desired number of columns in the maze (default: 3): "
        )
        try:
            num_columns = int(col_str.strip())
        except ValueError:
            num_columns = self.__DEFAULT_NUM_COLS

        return num_rows, num_columns

    def __create_adventurer(self):
        """Ask for player name input and return an Adventurer.

        Returns
        -------
        adv : Adventurer
            An adventurer initialized with the name inputted by the user.
        """
        while True:
            name = input("Enter adventurer name (non-empty): ")
            try:
                adv = Adventurer(name)
            except InvalidAdventurerName:
                continue
            else:
                break

        return adv

    def __print_instructions(self):
        """Display the game instructions."""
        print(self.__WELCOME_MESSAGE)
        INSTRUCTIONS_MESSAGE = """\
        Your goal:
           1) Collect all the four pillars of OOP
           2) Get to the exit safely

        Items randomly placed in each room:
           1) Healing potion (random heal amount)
           2) Vision potion (reveal adjacent rooms)
           3) Pit (random damage to adventurer)
           4) OOP pillars ("A", "P", "I", "E")

        Select 'h' to open help menu.

        Good luck!
        """
        print(textwrap.dedent(INSTRUCTIONS_MESSAGE))

    def __print_help_menu(self):
        """Display help menu with list of command keys"""
        print("Help Menu\n")
        # NOTE: Do not include hidden commands in the types being iterated over
        # here
        for command_type in (
            self.__COMMAND_TYPE_MOVEMENT,
            self.__COMMAND_TYPE_ITEM,
            self.__COMMAND_TYPE_DISPLAY,
            self.__COMMAND_TYPE_OTHER,
        ):
            print(f"{command_type.capitalize()} commands:")
            commands_of_this_type = (
                cmd
                for cmd, cmd_info in self.__COMMANDS.items()
                if cmd_info[self.__COMMAND_TYPE] == command_type
            )

            for cmd in commands_of_this_type:
                print(
                    f"'{self.__COMMANDS[cmd][self.__COMMAND_KEY_KEY]}': "
                    f"{self.__COMMANDS[cmd][self.__COMMAND_DESC_KEY]}"
                )
            print()

    def __create_legend_string(
        self, symbol_column_width=7, description_column_width=20, num_cols=3
    ):
        """
        Return a map legend printable string.

        Parameters
        ----------
        symbol_column_width : int
            How many characters to allow for the symbol in a legend column.
        description_column_width : int
            How many characters to allow for the description in a legend column.
        num_cols : int
            How many columns to have in the legend.

        Returns
        -------
        str
            The map legend as a printable string.
        """
        legend_entries = deque()
        for symbol_info in Room.ROOM_CONTENT_SYMBOLS.values():
            symbol = symbol_info[Room.ROOM_CONTENT_SYMBOL_KEY]

            # Special handling to account for space character (empty room)
            if symbol == " ":
                symbol = "<space>"

            description = symbol_info[Room.ROOM_CONTENT_DESC_KEY]
            legend_entries.append(
                f"{symbol:>{symbol_column_width}}: {description:{description_column_width}}"
            )

        legend_str = ""
        while legend_entries:
            for col in range(num_cols):
                legend_str += legend_entries.popleft()
                if col != num_cols - 1:
                    legend_str += " "
                else:
                    legend_str += "\n"

        return textwrap.dedent(legend_str).rstrip()

    def __print_maze_map_and_legend(self):
        """Print out the maze map and the map legend below it."""
        print()
        print("Maze map (empty portions are undiscovered):")
        print(self.__maze_map)
        print(" ______________ ")
        print("|____Legend____|")
        print(self.__create_legend_string())

    def __update_room_in_maze_maps(self, room):
        """Update the specified room in both the maze map the adventurer
        sees, as well as the hidden maze map that's fully revealed.

        Parameters
        ----------
        room : Room
            An arbitrary room that the adventurer has passed through.
        """
        self.__maze_map.update_room(room)
        self.__maze_map_filled_in.update_room(room)

    def __play_game(self):
        """Start the game"""
        (
            self.__adventurer_current_row,
            self.__adventurer_current_col,
        ) = self.__maze.entrance
        current_room = self.__maze.rooms[self.__adventurer_current_row][
            self.__adventurer_current_col
        ]
        current_room.occupied_by_adventurer = True
        self.__update_room_in_maze_maps(current_room)

        valid_options = tuple(
            info[self.__COMMAND_KEY_KEY] for info in self.__COMMANDS.values()
        )

        game_over = False
        while not game_over:
            # Initialize adjacent rooms to empty (will be populated if vision
            # potion is used)
            rooms_to_update_in_map = []

            # Initialize this iter assuming no vision potion was used. If a
            # vision potion is used, we automatically display the map and
            # legend.
            vision_potion_used = False

            # Separator to help user discriminate from previous input iteration
            print("\n" + "-" * self.__CONSOLE_WIDTH)

            # Print current room
            print("Current room:\n")
            print(current_room)

            # Ask for user input until a valid option is received
            while True:
                option = input("Enter an option: ").rstrip().lower()

                if option in valid_options:
                    break

                # Option entered was invalid
                print(
                    "Invalid input, please try again. You can view a list of "
                    "all commands by accessing the help menu "
                    f"('{self.__COMMANDS[self.__Command.PRINT_HELP_MENU][self.__COMMAND_KEY_KEY]}')."
                )

            # If options are other than move
            if (
                option
                == self.__COMMANDS[self.__Command.SHOW_ADVENTURER_STATUS][
                    self.__COMMAND_KEY_KEY
                ]
            ):
                # print Adventurer info
                print(self.__adventurer)
            elif (
                option
                == self.__COMMANDS[self.__Command.SHOW_MAP][self.__COMMAND_KEY_KEY]
            ):
                # Print out discovered portion of maze
                self.__print_maze_map_and_legend()

            elif (
                option
                == self.__COMMANDS[self.__Command.QUIT_GAME][self.__COMMAND_KEY_KEY]
            ):
                # Quit the game
                game_over = True
                continue
            elif (
                option
                == self.__COMMANDS[self.__Command.PRINT_HELP_MENU][
                    self.__COMMAND_KEY_KEY
                ]
            ):
                # Print help menu
                self.__print_help_menu()
            elif (
                option
                == self.__COMMANDS[self.__Command.USE_HEALING_POTION][
                    self.__COMMAND_KEY_KEY
                ]
            ):
                # Use healing potion
                hit_points_recovered = self.__adventurer.consume_healing_potion()
                if hit_points_recovered:
                    print(
                        "You consume a healing potion and gain "
                        f"{hit_points_recovered} hit points! "
                        f"{self.__adventurer.hit_points} health remaining."
                    )
            elif (
                option
                == self.__COMMANDS[self.__Command.USE_VISION_POTION][
                    self.__COMMAND_KEY_KEY
                ]
            ):
                # Use vision potion
                vision_potion = self.__adventurer.consume_vision_potion()
                print(f"You used a {str(vision_potion)}!")

                # Get set of adjacent rooms inside maze and add to maze map
                rooms_to_update_in_map = self.__get_adjacent_rooms_in_maze(current_room)

                vision_potion_used = True
            elif (
                option
                == self.__COMMANDS[self.__Command.USE_MAGIC_KEY][self.__COMMAND_KEY_KEY]
            ):
                # Use magic key
                magic_key = self.__adventurer.consume_magic_key()
                print(f"You used a {str(magic_key)}!")

                # unlock permanently locked door
                self.unlock_perm_locked_door()
            elif (
                option
                == self.__COMMANDS[self.__Command.SHOW_FULL_MAP][self.__COMMAND_KEY_KEY]
            ):
                print(self.__MAZE_MAP_FILLED_IN_MESSAGE)
                print(self.__maze_map_filled_in)

            # If selected to move a direction
            else:
                # Check to see if move is valid (e.g. can't move west from a
                # room on the far west wall of the maze)....or just don't
                # present an option for an invalid move
                # Navigate to new room
                # adventurer_location = <some coords>
                # current_room = <new room according to the move>
                next_room = self.__move_and_get_next_room(option, current_room)
                current_room.occupied_by_adventurer = False
                next_room.occupied_by_adventurer = True
                rooms_to_update_in_map.append(current_room)
                current_room = next_room

                if next_room.get_pit():
                    # Apply damage to adventurer
                    self.__apply_pit_damage_to_adventurer(current_room.get_pit())

                # Check to see if this room was the exit
                if current_room.is_exit():
                    if len(self.__adventurer.get_pillars_found()) == 4:
                        print(self.__YOU_WIN_MESSAGE)
                        print()
                        print(self.__MAZE_MAP_FILLED_IN_MESSAGE)
                        print(self.__maze_map_filled_in)
                        game_over = True
                    else:
                        print(
                            "You have reached the exit but don't have all of "
                            "the OOP pillars. Go find them!"
                        )

            # Pick up items in room
            all_items_from_room = current_room.remove_items()
            if all_items_from_room:
                print(" " + ". " * (self.__CONSOLE_WIDTH // 2 - 1))
                print(
                    f"You found the following items: {', '.join(map(str, all_items_from_room))}!"
                )

            for item in all_items_from_room:
                self.__adventurer.pick_up_item(item)
                self.__maze.mark_maze_item_as_found(item)

            # Update maze map with this room (after all items picked up)
            for room in [current_room] + rooms_to_update_in_map:
                self.__update_room_in_maze_maps(room)

            if vision_potion_used:
                self.__print_maze_map_and_legend()

            # Check adventurer's hit point
            if self.__adventurer.hit_points == 0:
                print(self.__YOU_DIED_MESSAGE)
                print(self.__MAZE_MAP_FILLED_IN_MESSAGE)
                print(self.__maze_map_filled_in)
                sys.exit(0)

    def __move_and_get_next_room(self, command_key, current_room):
        """
        Move the adventurer within the maze based on command input received.

        Parameters
        ----------
        command_key : str
            Input command indicating which direction the adventurer is trying
            to move.
        current_room : Room
            The room the adventurer currently occupies.

        Returns
        -------
        Room
            If the adventurer was capable of moving to the next room, i.e. did
            not hit a wall, the room to which they moved.
        """
        HIT_WALL_MSG = "You hit a wall. Try moving through a door."
        LOCKED_DOOR_MSG = "This door is locked. Answer a trivia question."
        PERM_LOCKED_DOOR_MSG = "This door is permanently locked. Find a magic key to open or find another route."

        # Possible commands (dicts containing key commands & descriptions)
        north_command = self.__COMMANDS[self.__Command.MOVE_NORTH]
        south_command = self.__COMMANDS[self.__Command.MOVE_SOUTH]
        east_command = self.__COMMANDS[self.__Command.MOVE_EAST]
        west_command = self.__COMMANDS[self.__Command.MOVE_WEST]

        coords_before = (self.__adventurer_current_row, self.__adventurer_current_col)

        if command_key == west_command[self.__COMMAND_KEY_KEY]:
            if current_room.get_side(Room.WEST) == Room.WALL:
                print(HIT_WALL_MSG)
            elif current_room.get_side(Room.WEST).perm_locked:
                print(PERM_LOCKED_DOOR_MSG)
            elif not current_room.get_side(Room.WEST).locked:
                self.__adventurer_current_col -= 1
            else:
                print(LOCKED_DOOR_MSG)
                answer = input("Question?")
                # simulates a user answering a question correctly
                if isinstance(answer, str):
                    # moves adventurer to room they are trying to move into
                    self.__adventurer_current_col -= 1
                    # unlocks the door as the question was answered "correctly"
                    current_room.get_side(Room.WEST).locked = False
        elif command_key == east_command[self.__COMMAND_KEY_KEY]:
            if current_room.get_side(Room.EAST) == Room.WALL:
                print(HIT_WALL_MSG)
            elif current_room.get_side(Room.EAST).perm_locked:
                print(PERM_LOCKED_DOOR_MSG)
            elif not current_room.get_side(Room.EAST).locked:
                self.__adventurer_current_col += 1
            else:
                print(LOCKED_DOOR_MSG)
                answer = input("Question?")
                if isinstance(answer, str):
                    self.__adventurer_current_col += 1
                    current_room.get_side(Room.EAST).locked = False
        elif command_key == north_command[self.__COMMAND_KEY_KEY]:
            if current_room.get_side(Room.NORTH) == Room.WALL:
                print(HIT_WALL_MSG)
            elif current_room.get_side(Room.NORTH).perm_locked:
                print(PERM_LOCKED_DOOR_MSG)
            elif not current_room.get_side(Room.NORTH).locked:
                self.__adventurer_current_row -= 1
            else:
                print(LOCKED_DOOR_MSG)
                answer = input("Question?")
                if isinstance(answer, str):
                    self.__adventurer_current_row -= 1
                    current_room.get_side(Room.NORTH).locked = False
        elif command_key == south_command[self.__COMMAND_KEY_KEY]:
            if current_room.get_side(Room.SOUTH) == Room.WALL:
                print(HIT_WALL_MSG)
            elif current_room.get_side(Room.SOUTH).perm_locked:
                print(PERM_LOCKED_DOOR_MSG)
            elif not current_room.get_side(Room.SOUTH).locked:
                self.__adventurer_current_row += 1
            else:
                print(LOCKED_DOOR_MSG)
                answer = input("Question?")
                if isinstance(answer, str):
                    self.__adventurer_current_row += 1
                    current_room.get_side(Room.SOUTH).locked = False

        coords_after = (self.__adventurer_current_row, self.__adventurer_current_col)
        if coords_before != coords_after:
            new_room = self.__maze.rooms[self.__adventurer_current_row][
                self.__adventurer_current_col
            ]
            self.unlock_adjacent_door(command_key, new_room)

        # Return the new room
        return self.__maze.rooms[self.__adventurer_current_row][
            self.__adventurer_current_col
        ]

    def __get_adjacent_rooms_in_maze(self, room):
        """
        Determine which rooms adjacent to the current room, out of a maximum
        possible 8, fall inside the maze.

        Parameters
        ----------
        room : Room
            A room inside the maze.

        Returns
        -------
        adjacent_rooms : list
            A list of all of the adjacent rooms that fall within the maze.
        """
        row, col = room.coords
        num_rows, num_cols = self.__maze.num_rows, self.__maze.num_cols

        # Set top left and bottom right of maze rectangle
        if row == 0:
            row_coord_of_top_left = row
            row_coord_of_bottom_right = row + 1
        elif row == num_rows - 1:
            row_coord_of_top_left = row - 1
            row_coord_of_bottom_right = row
        else:
            row_coord_of_top_left = row - 1
            row_coord_of_bottom_right = row + 1

        if col == 0:
            col_coord_of_top_left = col
            col_coord_of_bottom_right = col + 1
        elif col == num_cols - 1:
            col_coord_of_top_left = col - 1
            col_coord_of_bottom_right = col
        else:
            col_coord_of_top_left = col - 1
            col_coord_of_bottom_right = col + 1

        top_left_coords = (row_coord_of_top_left, col_coord_of_top_left)
        bottom_right_coords = (
            row_coord_of_bottom_right,
            col_coord_of_bottom_right,
        )

        # Take top left and bottom right coordinates and loop over to build the
        # list of adjacent rooms
        adjacent_rooms = []
        for row_ in range(top_left_coords[0], bottom_right_coords[0] + 1):
            for col_ in range(top_left_coords[1], bottom_right_coords[1] + 1):
                adjacent_rooms.append(self.__maze.rooms[row_][col_])

        return adjacent_rooms

    def __apply_pit_damage_to_adventurer(self, pit):
        """Adventurer takes damage from pit."""
        self.__adventurer.hit_points -= pit.damage_value
        print(
            f"You fell into a pit and sustained {pit.damage_value} damage! "
            f"{self.__adventurer.hit_points} health remaining!"
        )

    def unlock_perm_locked_door(self):
        pass


if __name__ == "__main__":
    # Start the game
    TriviaMaze()
