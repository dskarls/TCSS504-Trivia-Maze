"""Contains definition of dungeon items and pits, which may decorate a dungeon
room."""
from abc import ABC, abstractmethod
from util import generate_random_int


class DungeonItem(ABC):
    """A parent for all dungeon items. Every dungeon item has a name.
    Subclasses must override init."""

    @abstractmethod
    def __init__(self, name):
        """Create a dungeon item and assign it with the name passed in.

        Parameters
        ----------
        name : str
            The name of the dungeon item (used for string representation).
        """
        self.__name = name

    def __str__(self):
        """Generate a string representation for this dungeon item, which
        consists of its name."""
        return self.__name


class PillarOfOOP(DungeonItem):
    """A pillars dungeon item that represents some principle of object-oriented
    programming.  Picked up by an adventurer automatically upon entering the
    containing room, and is guaranteed to be accessible from the maze entrance
    (ignoring possible death due to pits). Must be picked up by the adventurer
    and carried to the exit in order to win the game.

    NOTE: This is an abstract class; subclasses must override init.
    NOTE: May be contained in a pit!
    """

    @abstractmethod
    def __init__(self, pillar_type):
        """Create an OOP pillar dungeon item with a nicely formatted name."""
        super().__init__(f"Pillar of {pillar_type}")


class AbstractionPillar(PillarOfOOP):
    """One of the four OOP pillars that represents the principle of
    abstraction. Picked up by an adventurer automatically upon entering the
    containing room, and is guaranteed to be accessible from the maze entrance
    (ignoring possible death due to pits). Must be picked up by the adventurer
    and carried to the exit in order to win the game.

    NOTE: May be contained in a pit!
    """

    def __init__(self):
        """Create an OOP abstraction pillar dungeon item with a nicely
        formatted name."""
        super().__init__("Abstraction")


class EncapsulationPillar(PillarOfOOP):
    """One of the four OOP pillars that represents the principle of
    encapsulation. Picked up by an adventurer automatically upon entering the
    containing room, and is guaranteed to be accessible from the maze entrance
    (ignoring possible death due to pits). Must be picked up by the adventurer
    and carried to the exit in order to win the game.

    NOTE: May be contained in a pit!
    """

    def __init__(self):
        """Create an OOP encapsulation pillar dungeon item with a nicely
        formatted name."""
        super().__init__("Encapsulation")


class InheritancePillar(PillarOfOOP):
    """One of the four OOP pillars that represents the principle of
    inheritance. Picked up by an adventurer automatically upon entering the
    containing room, and is guaranteed to be accessible from the maze entrance
    (ignoring possible death due to pits). Must be picked up by the adventurer
    and carried to the exit in order to win the game.

    NOTE: May be contained in a pit!
    """

    def __init__(self):
        """Create an OOP inheritance pillar dungeon item with a nicely
        formatted name."""
        super().__init__("Inheritance")


class PolymorphismPillar(PillarOfOOP):
    """One of the four OOP pillars that represents the principle of
    polymorphism. Picked up by an adventurer automatically upon entering the
    containing room, and is guaranteed to be accessible from the maze entrance
    (ignoring possible death due to pits). Must be picked up by the adventurer
    and carried to the exit in order to win the game.

    NOTE: May be contained in a pit!
    """

    def __init__(self):
        """Create an OOP polymorphism pillar dungeon item with a nicely
        formatted name."""
        super().__init__("Polymorphism")


class Potion(DungeonItem):
    """A concoction automatically picked up by an adventurer when they navigate
    to a containing room. The adventurer can consume them, which allows for
    various benefits.

    NOTE: This is an abstract class; subclasses must override init.
    """

    @abstractmethod
    def __init__(self, potion_type):
        """Create a potion dungeon item with a nicely formatted name."""
        super().__init__(f"Potion of {potion_type}")


class HealingPotion(Potion):
    """A potion that is automatically picked up by an adventurer when they
    navigate to a containing room. These potions possess a hit point healing
    value that is randomly generated in the specified range on initialization.
    When consumed, adds its healing value to the adventurer's hit point value
    (up to the maximum allowable hit points of an adventurer)."""

    def __init__(self, min_healing_value, max_healing_value):
        """Create a healing potion dungeon item with a nicely formatted
        name and a randomly chosen hit point healing value in the range
        [min_healing_value, _max_healing_value]."""
        super().__init__("Healing")
        self.healing_value = generate_random_int(
            min_healing_value, max_healing_value
        )

    def __lt__(self, other):
        """Define a healing potion to be less than another healing potion if
        its hit point value is lower than that of the other."""
        return self.healing_value < other.healing_value

    def __str__(self):
        """Return a human-readable string indicating this is a healing potion
        with a certain hit point value."""
        return f"HealingPotion({self.healing_value})"


class VisionPotion(Potion):
    """A potion that is automatically picked up by an adventurer when they
    navigate to a containing room. When consumed, prints all rooms adjacent to
    the current room (horizontally, vertically, and diagonally) to the console,
    up to 8 rooms if the adventurer is in an interior room of the dungeon."""

    def __init__(self):
        """Create a vision potion dungeon item with a nicely formatted name."""
        super().__init__("Vision")

    def __str__(self):
        """Return a human-readable string indicating this is a vision
        potion."""
        return "VisionPotion"


class Pit:
    """A damaging pit that can be placed in a dungeon room. When the adventurer
    navigates into a room with a pit, they endure its damage value, which is
    randomly generated within the specified range on initialization.

    NOTE: Assuming the adventurer does not die when stepping into a pit, they
    can navigate out of the containing room through any of its doors.

    NOTE: Pits can contain pillars, but not potions.
    """

    def __init__(self, min_damage, max_damage):
        """
        Create a pit object with a random hit point damage value in the
        range [min_damage, max_damage], where the latter two integer values are
        supplied as formal parameters.

        Parameters
        ----------
        min_damage : int
            Minimum amount of damage allowed when generating a random hit point
            damage value for the pit.
        max_damage : int
            Maximum amount of damage allowed when generating a random hit point
            damage value for the pit.
        """
        self.damage_value = generate_random_int(min_damage, max_damage)

    def __str__(self):
        """Return a human-readable string indicating this is a pit with a
        certain hit point damage value."""
        return f"Pit({self.damage_value})"
