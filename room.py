"""Definition of a room in the maze and relevant exceptions"""
from enum import Enum, auto
from door import Door

from maze_items import (
    AbstractionPillar,
    MazeItem,
    EncapsulationPillar,
    HealingPotion,
    InheritancePillar,
    PillarOfOOP,
    PolymorphismPillar,
    VisionPotion,
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
    NUM_CHAR_SUBROWS : str
        The number of character subrows used to represent a room as a string.
    STR_REPR_PADDING : str
        The spacing character(s) to use between vertical character columns in
        the string representation of a room.
    ROOM_CONTENT_SYMBOL_KEY : str
        The key used to access a room content symbol in ROOM_CONTENT_SYMBOLS.
    ROOM_CONTENT_DESC_KEY : str
        The key used to access a room content description in ROOM_CONTENT_SYMBOLS.
    ROOM_CONTENT_SYMBOLS : dict
        Contains room content symbols and descriptions for anything that might
        be in a room (including an adventurer.)

    Instance attributes
    -------------------
    occupied_by_adventurer : False
        Whether the adventurer occupies this room.
    coords : tuple of int
        The coordinates of the room, i.e. (row, col).
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

    # How many lines of characters compose each str representation
    NUM_CHAR_SUBROWS = 3

    # Used for delimiting parts of the string repr of a room for improving
    # readability
    STR_REPR_PADDING = "  "

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
        MULTIPLE_ITEMS = auto()
        ABSTRACTION_PILLAR = auto()
        INHERITANCE_PILLAR = auto()
        ENCAPSULATION_PILLAR = auto()
        POLYMORPHISM_PILLAR = auto()

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
        RoomContents.EMPTY: {
            ROOM_CONTENT_SYMBOL_KEY: " ",
            ROOM_CONTENT_DESC_KEY: "Empty room",
        },
    }

    def __init__(self, row, col):
        """
        Create an empty room with doors on all sides that is not an entrance,
        exit, or dead end..
        """
        self.__exit = False
        self.__entrance = False
        self.__pit = False
        self.__items = []
        self.occupied_by_adventurer = False

        # Set coords attr to specified row/col
        self.coords = (row, col)

        # Initialize all sides to be walls (rather than doors)
        self.__east_side = self.WALL
        self.__north_side = self.WALL
        self.__west_side = self.WALL
        self.__south_side = self.WALL

    def place_item(self, item):
        """Put a MazeItem in this room.

        Parameters
        ----------
        item : MazeItem
            Any valid MazeItem object.
        """
        if not isinstance(item, MazeItem):
            raise ValueError(
                "Attempted to insert a non-MazeItem into a Room!"
            )
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
            If the side is a Door object
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

    def set_side(self, direction, door_or_wall):
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
        """
        door_or_wall = door_or_wall.lower()
        if door_or_wall not in {self.DOOR, self.WALL}:
            raise InvalidRoomSideValue(
                "A side of a room must be one of the following: "
                f"{(', ').join((self.DOOR, self.WALL))}"
            )
        
        if door_or_wall == "door":
            door_or_wall = Door()

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

    def __get_room_symbol(self):
        """
        Determine the symbol used to represent the contents of this room.

        Returns
        -------
        str
            A single character representing the contents of this room.
        """
        if self.is_entrance():
            return self.ROOM_CONTENT_SYMBOLS[self.RoomContents.ENTRANCE][
                self.ROOM_CONTENT_SYMBOL_KEY
            ]

        if self.is_exit():
            return self.ROOM_CONTENT_SYMBOLS[self.RoomContents.EXIT][
                self.ROOM_CONTENT_SYMBOL_KEY
            ]

        if self.get_pit():
            # Remember that if a room contains a pit, it cannot contain any
            # items
            return self.ROOM_CONTENT_SYMBOLS[self.RoomContents.PIT][
                self.ROOM_CONTENT_SYMBOL_KEY
            ]

        # Check if there are multiple items or at least a single item (either a
        # potion or pillar). Recall that self.__items contains potions and/or
        # pillars

        if len(self.__items) == 0:
            return self.ROOM_CONTENT_SYMBOLS[self.RoomContents.EMPTY][
                self.ROOM_CONTENT_SYMBOL_KEY
            ]

        if len(self.__items) > 1:
            # Multiple items gets an "M"
            return self.ROOM_CONTENT_SYMBOLS[self.RoomContents.MULTIPLE_ITEMS][
                self.ROOM_CONTENT_SYMBOL_KEY
            ]

        # Room must contain a single item (potion or pillar)
        item_types_to_room_contents_enum = {
            HealingPotion: self.RoomContents.HEALING_POTION,
            VisionPotion: self.RoomContents.VISION_POTION,
            AbstractionPillar: self.RoomContents.ABSTRACTION_PILLAR,
            EncapsulationPillar: self.RoomContents.ENCAPSULATION_PILLAR,
            InheritancePillar: self.RoomContents.INHERITANCE_PILLAR,
            PolymorphismPillar: self.RoomContents.POLYMORPHISM_PILLAR,
        }
        only_item = self.__items[0]
        for item_type, enum_val in item_types_to_room_contents_enum.items():
            if isinstance(only_item, item_type):
                return self.ROOM_CONTENT_SYMBOLS[enum_val][
                    self.ROOM_CONTENT_SYMBOL_KEY
                ]

    def __str__(self):
        """The string representation of a room consists of three rows of
        characters collectively representing all four sides. A * is used at
        each corner and along walled sides, while a - represents a door on the
        north or south side and a | represents a door on the east or west
        sides. In the center of the room is a symbol representing the room's
        contents.

        NOTE: A room can contain both pillars and potions

        NOTE: A room that contains a pit cannot contain potions or pillars
        """

        room_symbol = self.__get_room_symbol()

        # Form north side
        room_str = "*"
        if self.__north_side == self.WALL:
            room_str += f"{self.STR_REPR_PADDING}*{self.STR_REPR_PADDING}"
        elif self.__north_side.perm_locked:
            room_str += f"{self.STR_REPR_PADDING}P{self.STR_REPR_PADDING}"
        elif self.__north_side.locked:
            room_str += f"{self.STR_REPR_PADDING}T{self.STR_REPR_PADDING}"
        else:
            room_str += f"{self.STR_REPR_PADDING}-{self.STR_REPR_PADDING}"
        # room_str += f"*{self.STR_REPR_PADDING}\n"
        room_str += "*\n"

        # West and East sides
        if self.__west_side == self.WALL:
            room_str += "*"
        elif self.__west_side.perm_locked:
            room_str += "P" #place holder string for a permanently locked door    
        elif self.__west_side.locked:
            room_str += "T" #place holder string for a locked door
        else:
            room_str += "|"

        if self.occupied_by_adventurer:

            if not self.STR_REPR_PADDING:
                after_adventurer_symbol = ""
            elif len(self.STR_REPR_PADDING) == 1:
                after_adventurer_symbol = self.STR_REPR_PADDING[0]
            elif len(self.STR_REPR_PADDING) >= 2:
                after_adventurer_symbol = self.STR_REPR_PADDING[1]

            adventurer_symbol = self.ROOM_CONTENT_SYMBOLS[
                self.RoomContents.ADVENTURER
            ][self.ROOM_CONTENT_SYMBOL_KEY]
            room_str += f"{adventurer_symbol}{after_adventurer_symbol}"
        else:
            room_str += f"{self.STR_REPR_PADDING}"

        room_str += f"{room_symbol}"
        if self.__east_side == self.WALL:
            room_str += f"{self.STR_REPR_PADDING}*"
        elif self.__east_side.perm_locked:
            room_str += f"{self.STR_REPR_PADDING}P"
        elif self.__east_side.locked:
            room_str += f"{self.STR_REPR_PADDING}T"
        else:
            room_str += f"{self.STR_REPR_PADDING}|"

        room_str += "\n"

        # Form bottom row
        room_str += "*"
        if self.__south_side == self.WALL:
            room_str += f"{self.STR_REPR_PADDING}*{self.STR_REPR_PADDING}"
        elif self.__south_side.perm_locked:
            room_str += f"{self.STR_REPR_PADDING}P{self.STR_REPR_PADDING}"
        elif self.__south_side.locked:
            room_str += f"{self.STR_REPR_PADDING}T{self.STR_REPR_PADDING}"
        else:
            room_str += f"{self.STR_REPR_PADDING}-{self.STR_REPR_PADDING}"
        # room_str += f"*{self.STR_REPR_PADDING}\n"
        room_str += "*\n"

        return room_str

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
        


