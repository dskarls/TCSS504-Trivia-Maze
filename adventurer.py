"""
Contains the Adventurer class and Adventurer-specific exceptions
"""
from maze_items import HealingPotion, PillarOfOOP, VisionPotion, MagicKey
from util import generate_random_int


class InvalidHitPointsArgs(ValueError):
    """Raised if the hit point parameters passed into Adventurer initialization
    are inconsistent."""


class AttemptedToPlaceInvalidItemInInventory(RuntimeError):
    """An attempt was made to add an unsupported itemto the adventurer's
    inventory."""


class Adventurer:
    """
    A player character that can traverse a maze. An adventurer has an
    integer number of hit points, and can carry healing potions, vision
    potions, and pillars.

    Attributes
    ----------
    hit_points : int
        The health level of the adventurer; has a minimum value of 0 and a
        maximum value of 100.
    __healing_potions : list
        The list of health potions held by the adventurer.
    __vision_potions : list
        The list of vision potions held by the adventurer.
    __pillars_found : list
        The list of pillars of OOP held by the adventurer.
    __hit_points_max : int
        The maximum possible hit points an adventurer can have.
    __hit_points : int
        The current hit points the adventurer has.

    Methods
    -------
    consume_healing_potion
        Remove the next smallest health potion held in inventory and use it to
        store hit points.
    pick_up_item
        Pick up an item (potion or pillar) and place it in the inventory.
    consume_vision_potion
        Remove a vision potion from inventory and return it.
    get_pillars_found
        Return a list of all pillars held in adventurer inventory.
    __verify_hit_point_args
        Ensure that the values passed for the min and max used for initial hit
        point value selection are consistent with one another and with the
        hard-cap maximum for hit points.
    """

    def __init__(
        self,
        initial_hit_points_min=75,
        initial_hit_points_max=100,
        hit_points_max=100,
    ):
        """
        Create an adventurer with a random number of hit points in the
        specified range. The adventurer begins with no healing potions, vision
        potions, or pillars.

        Parameters
        ----------
        initial_hit_points_min : int
            The minimum number of hit points the adventurer can start out with.
        initial_hit_points_max : int
            The maximum number of hit points the adventurer can start out with.
        hit_points_max : int
            The maximum number of hit points the adventurer can ever possibly
            have.

        """
        self.__healing_potions = []
        self.__vision_potions = []
        self.__pillars_found = []
        self.__magic_keys = []

        # Verify hit point args
        self.__verify_hit_point_args(
            initial_hit_points_min, initial_hit_points_max, hit_points_max
        )

        # Set internal hit points instance attrs
        self.__hit_points_max = hit_points_max
        self.__hit_points = generate_random_int(
            initial_hit_points_min, initial_hit_points_max
        )

    def __verify_hit_point_args(
        self, initial_hit_points_min, initial_hit_points_max, hit_points_max
    ):
        """
        Ensure that the values passed for the min and max used for initial hit
        point value selection are consistent with one another and with the
        hard-cap maximum for hit points.

        Parameters
        ----------
        initial_hit_points_min : int
            Minimum value that the adventurer's initial hit point value should
            start at.
        initial_hit_points_max : int
            Maximum value that the adventurer's initial hit point value should
            start at.
        hit_points_max : int
            The absolute largest value that an adventurer's hit points can ever
            take.

        Raises
        -------
        InvalidHitPointsArgs
            If the values passed in for the initial min, initial max, and
            ceiling are inconsistent.
        """
        if initial_hit_points_min >= initial_hit_points_max:
            raise InvalidHitPointsArgs(
                "The initial hit points min value must be strictly less than "
                "the initial hit points max value."
            )
        if hit_points_max < initial_hit_points_max:
            raise InvalidHitPointsArgs(
                "The maximum possible hit points value must be greater than "
                "or equal to the initial hit points maximum."
            )

    @property
    def hit_points(self):
        """
        The current hit points level of the adventurer. The maximum possible
        value is given by _HIT_POINTS_MAX and the minimum value is 0, at which
        point the adventurer dies.

        Returns
        -------
        int
            The current hit points level.
        """
        return self.__hit_points

    @hit_points.setter
    def hit_points(self, new_hit_points):
        """
        Set the hit points counter of the adventurer to a desired value.  If
        the new hit points value is below 0, the hit points counter is set to
        zero. If the new hit points counter exceeds _HIT_POINTS_MAX, the hit
        points counter is set to _HIT_POINTS_MAX.

        Parameters
        ----------
        new_hit_points : int
            Positive, zero, or negative amount of hit points to change the
            adventurer's hit point counter to.
        """
        # Enforce a ceiling of _HIT_POINTS_MAX
        new_hit_points = max(0, new_hit_points)

        # Enforce a ceiling of _HIT_POINTS_MAX
        new_hit_points = min(self.__hit_points_max, new_hit_points)

        self.__hit_points = new_hit_points

    def consume_healing_potion(self):
        """
        Consume the next smallest healing potion. If adventurer has none left,
        simply return zero. Otherwise, increase hit points by the value of
        the potion, discard it, and return the total amount of health recovered.

        Returns
        -------
        hit_points_recovered : int
            The hit points value restored by the healing potion.
        """
        hit_points_recovered = 0
        if self.__healing_potions:
            # Pop off the last healing potion in inventory, which will have the
            # smallest hit points value
            healing_potion = self.__healing_potions.pop()

            # Generate healing potion restore value and apply it to hit points
            # counter
            initial_hp = self.hit_points
            self.hit_points = self.hit_points + healing_potion.healing_value
            hit_points_recovered = self.__hit_points - initial_hp

        return hit_points_recovered

    def pick_up_item(self, maze_item):
        """
        Add a single maze item (potion or pillar) to the inventory.

        Parameters
        ----------
        maze_item : Potion or PillarOfOOP
            A healing potion, vision potion, pillar, or magic key.

        Raises
        ------
        AttemptedToPlaceInvalidItemInInventory
            If an object other than a HealingPotion, VisionPotion, or
            PillarOfOOP subclass object is received as an argument.
        """
        if isinstance(maze_item, HealingPotion):
            self.__healing_potions.append(maze_item)

            # Sort healing potions (descending order)
            self.__healing_potions.sort(reverse=True)

        elif isinstance(maze_item, VisionPotion):
            self.__vision_potions.append(maze_item)

        elif isinstance(maze_item, PillarOfOOP):
            self.__pillars_found.append(maze_item)

        elif isinstance(maze_item, MagicKey):
            self.__magic_keys.append(maze_item)

        else:
            raise AttemptedToPlaceInvalidItemInInventory(
                f"Attempted to add invalid object {maze_item} to "
                "adventurer inventory. Only potions or pillars are allowed!"
            )

    def consume_vision_potion(self):
        """
        Consume a vision potion. If adventurer has none left, no action is
        taken.

        NOTE: The Adventurer class has no knowledge of the maze itself. The
        caller is responsible for taking the appropriate action associated with
        a vision potion, i.e. printing the 8 adjacent rooms.

        Returns
        -------
        VisionPotion
            A vision potion object. Note that these have no knowledge of the
            maze itself, so the object itself is only really useful in that
            it has a nice string representation.
        """
        if self.__vision_potions:
            return self.__vision_potions.pop()

    def get_pillars_found(self):
        """
        Return a list of pillars the adventurer has in their inventory.

        Returns
        -------
        list
            A list containing PillarOfOOP concrete subclass objects currently
            held by the adventurer.
        """
        return self.__pillars_found

    def consume_magic_key(self):
        """
        Consume a magic key. If adventurer has none left, no action is
        taken.

        Returns
        -------
        MagicKey
            A magic key object.
        """
        if self.__magic_keys:
            return self.__magic_keys.pop()

    def get_magic_keys(self):
        """
        Return a list of magic keys the adventurer has in their inventory.

        Returns
        -------
        list
            A list containing MagicKey objects.
        """
        return self.__magic_keys

    def get_vision_potions(self):
        """
        Return a list of vision potions the adventurer has in their inventory.

        Returns
        -------
        list
            A list containing VisionPotion objects.
        """
        return self.__vision_potions
    def get_items(self):
        """
        Return a tuple of references to all items held in inventory."""
        return tuple(
            self.__healing_potions
            + self.__vision_potions
            + self.__pillars_found
            + self.__magic_keys
        )
