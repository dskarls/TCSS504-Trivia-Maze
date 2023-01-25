from room import Room


class DungeonMap:
    """
    Contains a string representation of all rooms an adventurer has either
    visited or exposed by way of a vision potion.

    Instance attributes
    -------------------
    __num_rows : int
        How many rows of rooms there are in the dungeon.
    __room_strings : 2D list of str
        The string representation for each room in the map.

    Instance methods
    ----------------
    update_room
        Updates the character rows and columns representing a room in the map.
    """

    def __init__(
        self,
        num_rows,
        num_cols,
    ):
        """
        Create an "empty" dungeon map with a 2D array of empty strings, one for
        each room in the dungeon.

        Parameters
        ----------
        num_rows : int
            Number of rows in the dungeon.
        num_cols : int
            Number of columns in the dungeon.
        """
        self.__num_rows = num_rows
        no_room = f" {Room.STR_REPR_PADDING} {Room.STR_REPR_PADDING} \n" * 3
        self.__room_strings = [[no_room] * num_cols for _ in range(num_rows)]

    def __str__(self):
        """Join string representations for each room to give a global visual
        representation of the dungeon (with unexposed parts represented with
        spaces)."""

        printable_char_lines = [
            [] for _ in range(self.__num_rows * Room.NUM_CHAR_SUBROWS)
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
                        row * Room.NUM_CHAR_SUBROWS + room_char_line_ind
                    )

                    # First room in this row -> do not omit first
                    # column of characters even if option to eliminate
                    # duplicate dividers is on
                    char_line_to_append = room_char_line

                    printable_char_lines[this_global_char_line_index].append(
                        char_line_to_append
                    )

        dungeon_string = ""
        for char_row in printable_char_lines:
            if char_row:
                dungeon_string += ("").join(char_row) + "\n"

        # Remove final newline
        dungeon_string = dungeon_string.rstrip("\n")

        return dungeon_string

    def update_room(self, room):
        """
        Updates the character rows and columns for a room in the map using
        using its string representation.

        Parameters
        ----------
        room : Room
            A room in the dungeon. Must have a `coords` attr to get x and y
            coordinates in maze, as well as a str representation.
        """
        # Go to element in room strings corresponding to this room
        room_row, room_col = room.coords
        self.__room_strings[room_row][room_col] = str(room)
