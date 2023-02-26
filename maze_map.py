from room import Room

from maze_items import (
    HealingPotion,
    VisionPotion,
    SuggestionPotion,
    AbstractionPillar,
    EncapsulationPillar,
    InheritancePillar,
    PolymorphismPillar,
    MagicKey,
)
from view_config import (
    RoomContents,
    ROOM_CONTENT_SYMBOLS,
    ROOM_CONTENT_SYMBOL_KEY,
    RoomSides,
    ROOM_SIDE_SYMBOLS,
    ROOM_SIDE_SYMBOL_KEY,
)


class MazeMap:
    """
    Contains a string representation of all rooms an adventurer has either
    visited or exposed by way of a vision potion.

    Instance attributes
    -------------------
    __num_rows : int
        How many rows of rooms there are in the maze.
    __room_strings : 2D list of str
        The string representation for each room in the map.
    __padding_col : str
        The spacing character(s) to use between vertical character columns in
        the string representation of a room.

    Instance methods
    ----------------
    update_room
        Updates the character rows and columns representing a room in the map.
    """

    def __init__(self, num_rows, num_cols, num_char_subrows, padding_col):
        """
        Create an "empty" maze map with a 2D array of empty strings, one for
        each room in the maze.

        Parameters
        ----------
        num_rows : int
            Number of rows in the maze.
        num_cols : int
            Number of columns in the maze.
        """
        self.__num_rows = num_rows
        self.__num_char_subrows = num_char_subrows
        self.__padding_col = padding_col
        no_room = f" {padding_col} {padding_col} \n" * 3
        self.__room_strings = [[no_room] * num_cols for _ in range(num_rows)]

    def __str__(self):
        """Join string representations for each room to give a global visual
        representation of the maze (with unexposed parts represented with
        spaces)."""

        printable_char_lines = [
            [] for _ in range(self.__num_rows * self.__num_char_subrows)
        ]

        for row in range(0, self.__num_rows):
            # Stringify this row
            this_row_room_strs = self.__room_strings[row][:]

            # Create a list with NUM_CHAR_SUBROWS empty sublists. As we loop
            # over the rooms in this row, we'll fill in these lists in stride.
            for room_str in this_row_room_strs:
                room_str_split = room_str.splitlines()
                # Add the char rows in this room to the appropriate sublists
                for room_char_line_ind, room_char_line in enumerate(
                    room_str_split
                ):
                    this_global_char_line_index = (
                        row * self.__num_char_subrows + room_char_line_ind
                    )

                    # First room in this row -> do not omit first
                    # column of characters even if option to eliminate
                    # duplicate dividers is on
                    char_line_to_append = room_char_line

                    printable_char_lines[this_global_char_line_index].append(
                        char_line_to_append
                    )

        maze_string = ""
        for char_row in printable_char_lines:
            if char_row:
                maze_string += ("").join(char_row) + "\n"

        # Remove final newline
        maze_string = maze_string.rstrip("\n")

        return maze_string

    def update_room(self, room):
        """
        Updates the character rows and columns for a room in the map using
        using its string representation. If the room has been visited already,
        it will be added to the map; if not, its all-spaces placeholder will
        remain in place.

        Parameters
        ----------
        room : Room
            A room in the maze. Must have a `coords` attr to get x and y
            coordinates in maze, as well as a str representation.
        """
        # Go to element in room strings corresponding to this room
        if room.visited:
            room_row, room_col = room.coords
            self.__room_strings[room_row][room_col] = self.__get_room_str(room)

    def __get_room_symbol(self, room):
        """
        Determine the symbol used to represent the contents of this room.

        Returns
        -------
        str
            A single character representing the contents of this room.
        """
        if room.is_entrance():
            return ROOM_CONTENT_SYMBOLS[RoomContents.ENTRANCE][
                ROOM_CONTENT_SYMBOL_KEY
            ]

        if room.is_exit():
            return ROOM_CONTENT_SYMBOLS[RoomContents.EXIT][
                ROOM_CONTENT_SYMBOL_KEY
            ]

        if room.get_pit():
            # Remember that if a room contains a pit, it cannot contain any
            # items
            return ROOM_CONTENT_SYMBOLS[RoomContents.PIT][
                ROOM_CONTENT_SYMBOL_KEY
            ]

        # Check if there are multiple items or at least a single item (either a
        # potion or pillar). Recall that self.__items contains potions and/or
        # pillars
        items = room.get_items()
        if len(items) == 0:
            return ROOM_CONTENT_SYMBOLS[RoomContents.EMPTY][
                ROOM_CONTENT_SYMBOL_KEY
            ]

        if len(items) > 1:
            # Multiple items gets an "M"
            return ROOM_CONTENT_SYMBOLS[RoomContents.MULTIPLE_ITEMS][
                ROOM_CONTENT_SYMBOL_KEY
            ]

        # Room must contain a single item (potion or pillar)
        item_types_to_room_contents = {
            HealingPotion: RoomContents.HEALING_POTION,
            VisionPotion: RoomContents.VISION_POTION,
            SuggestionPotion: RoomContents.VISION_POTION,
            AbstractionPillar: RoomContents.ABSTRACTION_PILLAR,
            EncapsulationPillar: RoomContents.ENCAPSULATION_PILLAR,
            InheritancePillar: RoomContents.INHERITANCE_PILLAR,
            PolymorphismPillar: RoomContents.POLYMORPHISM_PILLAR,
            MagicKey: RoomContents.MAGIC_KEY,
        }
        only_item = items[0]
        for item_type, enum_val in item_types_to_room_contents.items():
            if isinstance(only_item, item_type):
                return ROOM_CONTENT_SYMBOLS[enum_val][ROOM_CONTENT_SYMBOL_KEY]

    def __get_room_str(self, room):
        """The string representation of a room consists of three rows of
        characters collectively representing all four sides. A * is used at
        each corner and along walled sides, while a - represents a door on the
        north or south side and a | represents a door on the east or west
        sides. In the center of the room is a symbol representing the room's
        contents.

        NOTE: A room can contain both pillars and potions

        NOTE: A room that contains a pit cannot contain potions or pillars
        """
        room_symbol = self.__get_room_symbol(room)
        wall_symbol = ROOM_SIDE_SYMBOLS[RoomSides.WALL][ROOM_SIDE_SYMBOL_KEY]
        door_ns_symbol = ROOM_SIDE_SYMBOLS[RoomSides.DOOR_NORTH_SOUTH][
            ROOM_SIDE_SYMBOL_KEY
        ]
        door_ew_symbol = ROOM_SIDE_SYMBOLS[RoomSides.DOOR_EAST_WEST][
            ROOM_SIDE_SYMBOL_KEY
        ]
        door_locked_symbol = ROOM_SIDE_SYMBOLS[RoomSides.DOOR_LOCKED][
            ROOM_SIDE_SYMBOL_KEY
        ]
        door_permanently_locked_symbol = ROOM_SIDE_SYMBOLS[
            RoomSides.DOOR_PERMANENTLY_LOCKED
        ][ROOM_SIDE_SYMBOL_KEY]

        # Form north side
        padding_col = self.__padding_col
        room_str = wall_symbol
        north_side = room.get_side(Room.NORTH)
        if north_side == Room.WALL:
            room_str += f"{padding_col}{wall_symbol}{padding_col}"
        elif north_side.perm_locked:
            room_str += (
                f"{padding_col}{door_permanently_locked_symbol}{padding_col}"
            )
        elif north_side.locked:
            room_str += f"{padding_col}{door_locked_symbol}{padding_col}"
        else:
            room_str += f"{padding_col}{door_ns_symbol}{padding_col}"
        # room_str += f"*{padding}\n"
        room_str += f"{wall_symbol}\n"

        # West and East sides
        west_side = room.get_side(Room.WEST)
        if west_side == room.WALL:
            room_str += wall_symbol
        elif west_side.perm_locked:
            room_str += door_permanently_locked_symbol
        elif west_side.locked:
            room_str += door_locked_symbol
        else:
            room_str += door_ew_symbol

        if room.occupied_by_adventurer:
            after_adventurer_symbol = None
            if not padding_col:
                after_adventurer_symbol = ""
            elif len(padding_col) == 1:
                after_adventurer_symbol = padding_col[0]
            elif len(padding_col) >= 2:
                after_adventurer_symbol = padding_col[1]

            adventurer_symbol = ROOM_CONTENT_SYMBOLS[RoomContents.ADVENTURER][
                ROOM_CONTENT_SYMBOL_KEY
            ]
            room_str += f"{adventurer_symbol}{after_adventurer_symbol}"
        else:
            room_str += f"{padding_col}"

        room_str += f"{room_symbol}"
        east_side = room.get_side(Room.EAST)
        if east_side == Room.WALL:
            room_str += f"{padding_col}{wall_symbol}"
        elif east_side.perm_locked:
            room_str += f"{padding_col}{door_permanently_locked_symbol}"
        elif east_side.locked:
            room_str += f"{padding_col}{door_locked_symbol}"
        else:
            room_str += f"{padding_col}{door_ew_symbol}"

        room_str += "\n"

        # Form bottom row
        room_str += wall_symbol
        south_side = room.get_side(Room.SOUTH)
        if south_side == Room.WALL:
            room_str += f"{padding_col}{wall_symbol}{padding_col}"
        elif south_side.perm_locked:
            room_str += (
                f"{padding_col}{door_permanently_locked_symbol}{padding_col}"
            )
        elif south_side.locked:
            room_str += f"{padding_col}{door_locked_symbol}{padding_col}"
        else:
            room_str += f"{padding_col}{door_ns_symbol}{padding_col}"
        room_str += f"{wall_symbol}\n"

        return room_str
