"""Definition of a room in the maze and relevant exceptions"""
from door import Door

from maze_items import (
    MazeItem,
    PillarOfOOP,
    MagicKey,
)


class InvalidRoomSideValue(ValueError):
    """If one attempts to set the side of a room to an invalid value."""


class InvalidDirection(ValueError):
    """If an invalid direction (that is, one not in the set {"east", "north",
    "west", "south"}) is specified."""


class Room:
    """
    Every maze is composed of rooms, which may contain items (potions or
    pillars), pits, or nothing. Every maze has one room that is an entrance
    and one that is an exit.

    Class attributes
    ----------------
    DOOR : str
        Indicates that a room side is a door.
    WALL : str
        Indicates that a room side is a wall.
    EAST : str
        Indicates the east side of a room.
    NORTH : str
        The north side of a room.
    WEST : str
        The west side of a room.
    SOUTH : str
        The south side of a room.

    Instance attributes
    -------------------
    occupied_by_adventurer : False
        Whether the adventurer occupies this room.
    coords : tuple of int
        The coordinates of the room, i.e. (row, col).
    visited : bool
        Whether the adventurer has been in or is currently in this room. Should
        be set to True by the caller.
    __entrance : bool
        Whether the room is an entrance.
    __exit : bool
        Whether the room is an exit.
    __pit : Pit
        The Pit object, if any, contained in the room.
    __items : list of MazeItem
        List of items in the room.
    __east_side : str
        Whether the east side of the room is a door or wall.
    __north_side : str
        Whether the north side of the room is a door or wall.
    __west_side : str
        Whether the west side of the room is a door or wall.
    __south_side : str
        Whether the south side of the room is a door or wall.

    Instance methods
    ----------------
    place_item
        Place a maze item in the room.
    remove_items
        Remove and return all maze items, if any, held by the room.
    contains_pillar
        Return whether the room contains a pillar or not.
    contains_magic_key
        Return whether the room contains a magic key or not.
    get_items
        Get the items, if any, held by the room.
    get_pillar
        Get the pillar, if any, held by the room.
    get_side
        Return the side of a room (wall or door).
    set_side
        Set the side of a room to be a wall or door.
    is_dead_end
        Returns whether the room is a dead end.
    is_entrance
        Returns whether the room is an entrance or not.
    set_entrance
        Set the room to be an entrance.
    is_exit
        Returns whether the room is an exit or not.
    set_exit
        Set the room to be an exit.
    set_pit
        Set the room to hold the specified Pit object.
    get_pit
        Return the Pit object, if any, held by the room.
    reset_decorations
        Remove all items from the room.
    __get_room_symbol
        Return the symbol to be placed in the center of the room's string
        representation.
    """

    # Names used for the value of a room side
    DOOR = "door"
    WALL = "wall"

    EAST = "east"
    NORTH = "north"
    WEST = "west"
    SOUTH = "south"

    def __init__(self, row, col):
        """
        Create an empty room with doors on all sides that is not an entrance,
        exit, or dead end..
        """
        self.__exit = False
        self.__entrance = False
        self.__pit = None
        self.__items = []
        self.occupied_by_adventurer = False

        # Set coords attr to specified row/col
        self.coords = (row, col)

        self.visited = False

        # Initialize all sides to be walls (rather than doors)
        self.__east_side = self.WALL
        self.__north_side = self.WALL
        self.__west_side = self.WALL
        self.__south_side = self.WALL

    def __eq__(self, other):
        return self.coords == other.coords

    def place_item(self, item):
        """Put a MazeItem in this room.

        Parameters
        ----------
        item : MazeItem
            Any valid MazeItem object.
        """
        if not isinstance(item, MazeItem):
            raise ValueError("Attempted to insert a non-MazeItem into a Room!")
        self.__items.append(item)

    def remove_items(self):
        """Remove all items from this room and return them as a list. If the
        room contains no items, the returned list will be empty.

        Returns
        -------
        all_items_from_room : list
            List containing all items removed from this room.
        """
        all_items_from_room = []
        while self.__items:
            all_items_from_room.append(self.__items.pop())

        return all_items_from_room

    def contains_magic_key(self):
        """If this room contains a magic key, return True; otherwise, return
        False.

        Returns
        -------
        bool
            True if the room contains a magic key; otherwise False.
        """
        return any(isinstance(item, MagicKey) for item in self.__items)

    def contains_pillar(self):
        """If this room contains a pillar, return True; otherwise, return
        False. Note that a given room will only ever contain at most one pillar.

        Returns
        -------
        bool
            True if the room contains a pillar; otherwise False.
        """
        return any(isinstance(item, PillarOfOOP) for item in self.__items)

    def get_pillar(self):
        """
        If this room contains a pillar object, return it. Otherwise, return None.

        Returns
        -------
        PillarofOOP
            The pillar contained in the room.
        """
        for item in self.__items:
            if isinstance(item, PillarOfOOP):
                return item

        return None

    def get_side(self, direction):
        """
        Return whether the side of the room given by the specified direction is
        a Door object or wall ("wall").

        Parameters
        ----------
        direction : str
            The cardinal direction of the side of the room that is inspected.

        Returns
        -------
        str
            If the side is a wall
        Door
            If the side is a door
        Raises
        ------
        InvalidDirection
            If an invalid direction is passed in.
        """
        if direction == self.EAST:
            return self.__east_side
        elif direction == self.NORTH:
            return self.__north_side
        elif direction == self.WEST:
            return self.__west_side
        elif direction == self.SOUTH:
            return self.__south_side
        else:
            raise InvalidDirection(
                f"Direction must be one of '{self.EAST}', '{self.NORTH}', "
                f"'{self.WEST}', or '{self.SOUTH}'."
            )

    def set_side(self, direction, door_or_wall, question_and_answer=None):
        """
        Set one side of a room ("east", "north", "west", or "south") to be
        either a Door object or a wall.

        Parameters
        ----------
        direction : str
            Which side of the room to set. Possible options are "east",
            "north", "west", or "south".
        door_or_wall : str
            What to set the side of the room as. Options are "door" or "wall".
        question_and_answer : QuestionAndAnswer
            Only used if ``door_or_wall``==Room.DOOR. Sets lock state when placing a Door.
        """
        door_or_wall = door_or_wall.lower()
        if door_or_wall not in {self.DOOR, self.WALL}:
            raise InvalidRoomSideValue(
                "A side of a room must be one of the following: "
                f"{(', ').join((self.DOOR, self.WALL))}"
            )

        if door_or_wall == self.DOOR:
            # If `question_and_answer` is None, put an unlocked door.
            # Otherwise, lock the door with the given question-and-answer.
            door_or_wall = Door(question_and_answer)

        direction = direction.lower()
        if direction == self.EAST:
            self.__east_side = door_or_wall
        elif direction == self.NORTH:
            self.__north_side = door_or_wall
        elif direction == self.WEST:
            self.__west_side = door_or_wall
        elif direction == self.SOUTH:
            self.__south_side = door_or_wall
        else:
            raise InvalidDirection(
                f"Direction must be one of '{self.EAST}', '{self.NORTH}', "
                f"'{self.WEST}', or '{self.SOUTH}'."
            )

    def is_dead_end(self):
        """Return True if three sides of the room are walls."""
        sides = [
            self.__east_side,
            self.__north_side,
            self.__west_side,
            self.__south_side,
        ]
        return sides.count(self.WALL) == 3

    def is_entrance(self):
        """Return True if this room is an entrance; otherwise return False."""
        return self.__entrance

    def set_entrance(self):
        """Set this room to be an entrance of the maze."""
        self.__entrance = True

    def is_exit(self):
        """Return True if this room is an exit; otherwise return False."""
        return self.__exit

    def set_exit(self):
        """Set this room to be an exit of the maze."""
        self.__exit = True

    def set_pit(self, pit):
        """Decorate this room with the supplied pit. Upon an adventurer
        entering a room with a pit, it triggers automatically.

        Parameters
        ----------
        pit : Pit
            A pit with some specific hit point damage value.
        """
        self.__pit = pit

    def get_pit(self):
        """If this room contains a pit, return it; otherwise, return None.

        Returns
        -------
        Pit or None
            The pit object held by the room or, if it doesn't contain one, None.
        """
        return self.__pit

    def reset_decorations(self):
        """Remove all items, if any, contained in this room. Also remove its
        pit, if it has one."""
        self.__items = []
        self.set_pit(None)

    def get_items(self):
        return self.__items
