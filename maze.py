"""
Contains the Maze class, which constructs and maze and decorates it with OOP
pillars, potions, and pits. Also contains custom exceptions relevant to these
operations.
"""
import random
from maze_items import (
    MazeItem,
    PillarOfOOP,
    AbstractionPillar,
    EncapsulationPillar,
    InheritancePillar,
    HealingPotion,
    Pit,
    PolymorphismPillar,
    SuggestionPotion,
    VisionPotion,
    MagicKey,
)
from question_and_answer import question_and_answer_factory
from room import Room
from util import generate_random_int, randomly_choose_between_two_outcomes
from difficulty_config import DifficultySettings, DIFFICULTY_SETTINGS


class MazeConstructionError(RuntimeError):
    """If there is any problem related to the construction of the maze"""


class MazeCannotAccommodatePillars(MazeConstructionError):
    """If there were too many pits in the generated maze to be able to fit all
    four pillars."""


class MazeTooSmall(MazeConstructionError):
    """If the the number of rows and/or columns passed into the maze is/are too small"""


class InvalidMinEntranceExitDistance(MazeConstructionError):
    """If the minimum Manhattan distance between the (randomly generated)
    entrance and exit is impossibly large relative to the size of the maze
    maze."""


class MazeNotTraversible(MazeConstructionError):
    """If an adventurer could not possibly reach the exit from the entrance."""


class MazeHasNoReachableDeadEnds(MazeConstructionError):
    """If the maze generated does not contain a single dead end traversable
    from the entrance."""


class FailedToFindValidRoomDecoration(MazeConstructionError):
    """If the decoration of the maze with potions, pits, and pillars is invalid."""


class MazeIsMissingReachablePillar(FailedToFindValidRoomDecoration):
    """If one of the pillars is not reachable from the entrance"""


class InvalidMazeSubsetCoords(MazeConstructionError):
    """Raised if an invalid pair of rooms are passed to a method."""


class AttemptedToMarkInvalidItemAsFound(ValueError):
    """Raised if a non-MazeItem object is attempted to be marked as picked
    up by the adventurer."""


class Maze:
    """
    A maze, which consists of a rectangular array of Room objects. Each
    room can be filled with (A) nothing, (B) a healing potion, (C) a vision
    potion, (D) one of the OOP pillars, and/or (E) a pit. There is exactly one
    entrance and one exit, and these rooms contain no other items (or pits). It
    is guaranteed that there exists a traversable path from the entrance to the
    exit. It is also guaranteed that there exists a traversable path to at
    least one dead end. Finally, it is guaranteed that there exists a
    traversable path to each of the OOP Pillars. However, note that it is *not*
    guaranteed that it is possible to get to either of these (most importantly
    the exit) without dying from pit damage, even if healing potions are
    consumed optimally. That is, although unlikely, it may literally be
    impossible to some games!

    Attributes
    ----------
    rooms : list of list of Room
       Two-dimensional array of Room objects that comprise the maze. They are
       located in the array according to their two-dimensional coords, e.g. the
       Room at indices [1][2] corresponds to row 1, column 2 (both zero-based
       indexing).
    num_rows : int
        The number of rows of the maze.
    num_cols : int
        The number of columns of the maze.
    entrance : tuple of int
        Two-dimensional tuple containing the integer coordinates of the
        maze entrance.
    exit : tuple of int
        Two-dimensional tuple containing the integer coordinates of the
        maze exit.
    __unfound_items_counter: dict
        Contains counter for each type of room decoration (pit, potions, and
        pillars).
    __MIN_ALLOWED_ROWS_OR_COLS: int
        The minimum number of rows or columns that can be used to build a maze.
    __PILLAR_PROBABILITY: float
        The probability of placing a pillar in a room during maze generation.
    __PIT_PROBABILITY: float
        The probability of placing a pit in a room during maze generation.
    __HEALING_POTION_PROBABILITY: float
        The probability of placing a healing potion in a room during maze
        generation.
    __VISION_POTION_PROBABILITY: float
        The probability of placing a vision potion in a room during maze
        generation.
    __MIN_HEALING_POTION_VALUE: int
        Minimum value a healing potion can have.
    __MAX_HEALING_POTION_VALUE: int
        Maximum value a healing potion can have.
    __MIN_PIT_DAMAGE: int
        Minimum damage a pit can deal to an adventurer.
    __MAX_PIT_DAMAGE: int
        Maximum damage a pit can deal to an adventurer.
    __MIN_ENTRANCE_EXIT_MANHATTAN_DISTANCE: int
        Minimum distance (in the Manhattan norm) between the entrance and exit
        when choosing where to place them in the maze.
    __MAX_ENTRANCE_EXIT_SAMPLE_ATTEMPTS: int
        Maximum number of attempts when randomly choosing where to place
        entrance and exit (subject to __MIN_ENTRANCE_EXIT_MANHATTAN_DISTANCE)
        before giving up and just placing the entrance at the top left room and
        the exit at the bottom right room.

    Methods
    -------
    build_maze
        Initializes the maze of the specified row and column count with rooms
        and fills them with pillars, potions, and pits.
    mark_maze_item_as_found
        Decrement the appropriate maze item type counter if an item is found
        by the adventurer.
    __set_entrance_and_exit
        Randomly select entrance and exit rooms. If the entrance and exit are
        not at least _MIN_ENTRANCE_EXIT_MANHATTAN_DISTANCE units apart (in the
        Manhattan norm), we resample.
    __decorate_rooms
        Places items (healing potions, vision potions, OOP pillars, and pits)
        into the maze via random selection according to the corresponding
        probabilities.
    __roll_to_place_item_or_pit_door
        Decide whether to place an item or not by doing a random sampling using
        its placement probability.
    __room_is_in_maze
        Return True if the coordinates (row, col) correspond to a room in the
        maze. Otherwise, return False.
    __set_room_doors_on_traversal_step
        When traversing from one room to adjacent room while building the maze,
        set the sides of each room passed through to be doors.
    __set_room_sides_to_doors_during_random_depth_first_traversal
        Perform a random depth-first traversal of the entire maze. This is done
        to decide where to place walls, by requiring that no rooms are
        revisited on the way "down" (i.e. increasing depth/distance from the
        starting room).
    """

    def __init__(self, row_count, col_count, trivia_db, difficulty=None):
        """
        Build a traversable maze of the specified dimensions and fill
        it with items and pits.

        Parameters
        ----------
        row_count : int
            The number of rows of the maze.
        col_count : int
            The number of columns of the maze.
        trivia_db : TriviaDatabase
            A database from which questions and answers can be obtained.

        Raises
        ------
        MazeTooSmall
            If the row or column counts are smaller than the smallest allowable
            size.
        """

        # Smallest dimensions of maze
        self.__MIN_ALLOWED_ROWS_OR_COLS = 3

        # values default to medium difficulty if no difficulty is chosen
        self.__PILLAR_PROBABILITY = 0.25
        self.__PIT_PROBABILITY = 0.15
        self.__HEALING_POTION_PROBABILITY = 0.15
        self.__VISION_POTION_PROBABILITY = 0.15
        self.__SUGGESTION_POTION_PROBABILITY = 0.15
        self.__MAGIC_KEY_PROBABILITY = 0.15
        self.__LOCKED_DOOR_PROBABILITY = 0.35

        # Min and max amount that a healing potion can restore to hit points
        self.__MIN_HEALING_POTION_VALUE = 1
        self.__MAX_HEALING_POTION_VALUE = 15

        # Min and max amount of damage that a pit can do
        self.__MIN_PIT_DAMAGE = 5
        self.__MAX_PIT_DAMAGE = 25

        # Minimum Manhattan distance enforced between entrance and exit when
        # choosing where they should be. Cannot be larger than
        #     (row_count - 1) + (col_count - 1)
        # where row_count and col_count are the number of rows and columns of the
        # entire maze.
        self.__MIN_ENTRANCE_EXIT_MANHATTAN_DISTANCE = 6
        self.__MAX_ENTRANCE_EXIT_SAMPLE_ATTEMPTS = 15
        self.rooms = []

        if (
                row_count < self.__MIN_ALLOWED_ROWS_OR_COLS
                or col_count < self.__MIN_ALLOWED_ROWS_OR_COLS
        ):
            raise MazeTooSmall(
                "The maze maze must be at least "
                f"{self.__MIN_ALLOWED_ROWS_OR_COLS} x "
                f"{self.__MIN_ALLOWED_ROWS_OR_COLS} rooms big."
            )

        self.num_rows = row_count
        self.num_cols = col_count

        # NOTE: entrance and exit are set by build_maze
        self.entrance, self.exit = None, None

        self.__unfound_items_counter = {
            Pit: 0,
            HealingPotion: 0,
            VisionPotion: 0,
            SuggestionPotion: 0,
            PillarOfOOP: 0,
            MagicKey: 0,
        }

        # Keep track of which questions we've attached to doors to avoid
        # repetition
        self.__used_question_and_answer_hashes = set({})

        # probabilities of items being placed in the maze
        if difficulty:
            self.__PIT_PROBABILITY = DIFFICULTY_SETTINGS[difficulty][
                DifficultySettings.PIT_PROBABILITY
            ]
            self.__HEALING_POTION_PROBABILITY = DIFFICULTY_SETTINGS[difficulty][
                DifficultySettings.HEALING_POTION_PROBABILITY
            ]
            self.__VISION_POTION_PROBABILITY = DIFFICULTY_SETTINGS[difficulty][
                DifficultySettings.VISION_POTION_PROBABILITY
            ]
            self.__SUGGESTION_POTION_PROBABILITY = DIFFICULTY_SETTINGS[difficulty][
                DifficultySettings.SUGGESTION_POTION_PROBABILITY
            ]
            self.__MAGIC_KEY_PROBABILITY = DIFFICULTY_SETTINGS[difficulty][
                DifficultySettings.MAGIC_KEY_PROBABILITY
            ]
            self.__LOCKED_DOOR_PROBABILITY = DIFFICULTY_SETTINGS[difficulty][
                DifficultySettings.LOCKED_DOOR_PROBABILITY
            ]

            # Min and max amount that a healing potion can restore to hit points
            self.__MIN_HEALING_POTION_VALUE = DIFFICULTY_SETTINGS[difficulty][
                DifficultySettings.MIN_HEALING_POTION_VALUE
            ]
            self.__MAX_HEALING_POTION_VALUE = DIFFICULTY_SETTINGS[difficulty][
                DifficultySettings.MAX_HEALING_POTION_VALUE
            ]

            # Min and max amount of damage that a pit can do
            self.__MIN_PIT_DAMAGE = DIFFICULTY_SETTINGS[difficulty][
                DifficultySettings.MIN_PIT_DAMAGE
            ]
            self.__MAX_PIT_DAMAGE = DIFFICULTY_SETTINGS[difficulty][
                DifficultySettings.MAX_PIT_DAMAGE
            ]


        self.build_maze(trivia_db)

    def __str__(self):
        """
        Prints a string representation of the entire maze, including the
        number of rows, number of columns, the coordinates of the entrance and
        exit, number of pits, number of unfound healing potions, number of
        unfound vision potions, number of unfound pillars.

        Returns
        -------
        maze_str
            The string representation of the entire maze.
        """
        maze_str = (
            f"Number of rooms: {self.num_rows * self.num_cols}",
            f"Number of rows: {self.num_rows}",
            f"Number of columns: {self.num_cols}",
            f"Entrance coords: {self.entrance}",
            f"Exit coords: {self.exit}",
            f"Number of pits: {self.__unfound_items_counter[Pit]}",
            f"Number of unfound healing potions: {self.__unfound_items_counter[HealingPotion]}",
            f"Number of unfound vision potions: {self.__unfound_items_counter[VisionPotion]}",
            f"Number of unfound pillars: {self.__unfound_items_counter[PillarOfOOP]}",
            f"Number of unfound magic keys: {self.__unfound_items_counter[MagicKey]}",
        )

        return (", ").join(maze_str)

    def mark_maze_item_as_found(self, maze_item):
        """
        Decrement the appropriate maze item type counter if an item is found
        by the adventurer.

        Parameters
        ----------
        maze_item : MazeItem
            A maze item picked up by the adventurer.
        """
        if not isinstance(maze_item, MazeItem):
            raise AttemptedToMarkInvalidItemAsFound(
                "Only a MazeItem object can be marked as picked up by the "
                "adventurer."
            )

        if issubclass(type(maze_item), PillarOfOOP):
            maze_item_type = PillarOfOOP
        else:
            maze_item_type = type(maze_item)

        self.__unfound_items_counter[maze_item_type] -= 1

    def __set_entrance_and_exit(self):
        """
        Randomly select entrance and exit rooms. If the entrance and exit are
        not at least _MIN_ENTRANCE_EXIT_MANHATTAN_DISTANCE units apart (in the
        Manhattan norm), we resample.

        NOTE: _MIN_ENTRANCE_EXIT_MANHATTAN_DISTANCE cannot be larger than the
        sum of the number of rows and columns of the entire maze.

        Returns
        -------
        entrance_coords : tuple of int
            Two-dimensional tuple containing the integer coordinates of the
            maze entrance.
        exit_coords : tuple of int
            Two-dimensional tuple containing the integer coordinates of the
            maze exit.
        """
        # Check that min. distance is valid
        if self.__MIN_ENTRANCE_EXIT_MANHATTAN_DISTANCE > (self.num_rows - 1) + (
                self.num_cols - 1
        ):
            raise InvalidMinEntranceExitDistance(
                "The minimum Manhattan distance enforced between the "
                "(randomly generated) entrance and exit cannot exceed "
                "(row_count - 1) + (col_count - 1), as that is already the "
                "largest distance possible (diagonal to diagonal)."
            )

        # Choose an entrance and exit at random and ensure minimum distance is
        # met. If not, resample. If we've tried sampling
        # _MAX_ENTRANCE_EXIT_SAMPLE_ATTEMPTS times t enough to get a valid
        # entrance and exit for some reason, simply set the top left room as
        # the entrance and the bottom left room as the exit.
        num_samplings = 0
        while True:
            entrance_coords = (
                generate_random_int(0, self.num_rows - 1),
                generate_random_int(0, self.num_cols - 1),
            )
            exit_coords = (
                generate_random_int(0, self.num_rows - 1),
                generate_random_int(0, self.num_cols - 1),
            )

            distance = abs(exit_coords[0] - entrance_coords[0]) + abs(
                exit_coords[1] - exit_coords[1]
            )

            if distance >= self.__MIN_ENTRANCE_EXIT_MANHATTAN_DISTANCE:
                break

            # See if we've wasted too much time sampling
            num_samplings += 1
            if num_samplings > self.__MAX_ENTRANCE_EXIT_SAMPLE_ATTEMPTS:
                entrance_coords = (0, 0)
                exit_coords = (self.num_rows - 1, self.num_cols - 1)
                break

        # Set rooms as entrance and exit
        self.rooms[entrance_coords[0]][entrance_coords[1]].set_entrance()
        self.rooms[exit_coords[0]][exit_coords[1]].set_exit()

        return entrance_coords, exit_coords

    def build_maze(self, trivia_db):
        """
        Create a rectangular maze with the specified number of rows and
        columns, one entrance, and one exit.

        Begin by created a 2D dynamic array in the form of a list of lists
        containing default-constructed Room objects. Then, loop over each room
        and set which of the four sides of the room are doors and which are
        walls. Finally, decorate the rooms with items (potions or pillars) and
        pits. It is guaranteed that there exists a traversable path from the
        entrance to the exit. It is also guaranteed that there exists a
        traversable path to at least one dead end. However, note that it is
        *not* guaranteed that it is possible to get to either of these (most
        importantly the exit) without dying from pit damage, even if healing
        potions are consumed optimally. That is, although unlikely, it may
        literally be impossible to some games!
        """
        for row in range(0, self.num_rows):
            self.rooms.append([Room(row, col) for col in range(0, self.num_cols)])

        # Set entrance and exit
        self.entrance, self.exit = self.__set_entrance_and_exit()

        # Perform a random depth-first traversal that visits every room and
        # sets necessary room sides to doors so as to allow the traversal
        self.__set_room_sides_to_doors_during_random_depth_first_traversal(
            *self.entrance,
            previous_room=None,
            cumulative_visited=[],
            trivia_db=trivia_db,
        )

        # Place potions, pits, pillars
        while True:
            try:
                self.__decorate_rooms()
            except MazeCannotAccommodatePillars:
                continue
            else:
                break

    def __decorate_rooms(self):
        """
        Places items (healing potions, vision potions, OOP pillars, and pits)
        into the maze via random selection according to the corresponding
        probabilities. Some constraints:

          - The entrance and exit must not contain any items or pits
          - No two pillars can be in the same room
          - No potions or pillars will be placed inside pits

        NOTE: Potions and pillars can be in the same room
        NOTE: There will never be more than one healing potion in a room.
        NOTE: There will never be more than one vision potion in a room.
        """
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self.rooms[row][col].reset_decorations()

        pillars_to_place = [
            AbstractionPillar(),
            EncapsulationPillar(),
            InheritancePillar(),
            PolymorphismPillar(),
        ]

        # First pass: potions, pits, and pillars
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                this_room = self.rooms[row][col]

                # If this room is an entrance or exit, don't place any items
                if this_room.is_entrance() or this_room.is_exit():
                    continue

                # Keep track of whether we placed a pillar, potion, or magic key.
                # If we do, then don't make this room a pit.
                placed_potion_pillar_or_key = False

                # Roll to see if we should place a pillar here
                if pillars_to_place:
                    if self.__roll_to_place_item_or_pit_or_door(
                            self.__PILLAR_PROBABILITY
                    ):
                        self.__unfound_items_counter[PillarOfOOP] += 1
                        this_room.place_item(pillars_to_place.pop())
                        placed_potion_pillar_or_key = True

                # Roll to see if we should place a healing potion
                if self.__roll_to_place_item_or_pit_or_door(
                        self.__HEALING_POTION_PROBABILITY
                ):
                    this_room.place_item(
                        HealingPotion(
                            self.__MIN_HEALING_POTION_VALUE,
                            self.__MAX_HEALING_POTION_VALUE,
                        )
                    )
                    self.__unfound_items_counter[HealingPotion] += 1
                    placed_potion_pillar_or_key = True

                # Roll to see if we should place a vision potion
                if self.__roll_to_place_item_or_pit_or_door(
                        self.__VISION_POTION_PROBABILITY
                ):
                    this_room.place_item(VisionPotion())
                    self.__unfound_items_counter[VisionPotion] += 1
                    placed_potion_pillar_or_key = True

                # Roll to see if we should place a vision potion
                if self.__roll_to_place_item_or_pit_or_door(
                        self.__SUGGESTION_POTION_PROBABILITY
                ):
                    this_room.place_item(SuggestionPotion())
                    self.__unfound_items_counter[SuggestionPotion] += 1
                    placed_potion_pillar_or_key = True

                # Roll to see if we should place a magic key
                if self.__roll_to_place_item_or_pit_or_door(
                        self.__MAGIC_KEY_PROBABILITY
                ):
                    this_room.place_item(MagicKey())
                    self.__unfound_items_counter[MagicKey] += 1
                    placed_potion_pillar_or_key = True

                # If we did not place a pillar or potion, roll to see if we
                # should place a pit.
                if not placed_potion_pillar_or_key:
                    if self.__roll_to_place_item_or_pit_or_door(self.__PIT_PROBABILITY):
                        this_room.set_pit(
                            Pit(self.__MIN_PIT_DAMAGE, self.__MAX_PIT_DAMAGE)
                        )
                        self.__unfound_items_counter[Pit] += 1

        # Second pass: ensure all pillars are placed (and note that no two can
        # be in the same room). Keep looping until we place them all

        MAX_PILLAR_PLACEMENT_ATTEMPTS = 10
        num_pillar_placement_attempts = 0
        while pillars_to_place:
            num_pillar_placement_attempts += 1

            if num_pillar_placement_attempts == MAX_PILLAR_PLACEMENT_ATTEMPTS:
                raise MazeCannotAccommodatePillars(
                    "Not enough rooms left for pillars after pits were placed."
                )

            for row in range(self.num_rows):
                for col in range(self.num_cols):
                    if not pillars_to_place:
                        # All done
                        return

                    this_room = self.rooms[row][col]

                    # If this room is an entrance or exit, or already contains
                    # a pillar, don't place any items
                    if (
                            this_room.is_entrance()
                            or this_room.is_exit()
                            or this_room.get_pit()
                            or this_room.contains_pillar()
                    ):
                        continue

                    # Roll to see if we should place a pillar here
                    if self.__roll_to_place_item_or_pit_or_door(
                            self.__PILLAR_PROBABILITY
                    ):
                        this_room.place_item(pillars_to_place.pop())
                        self.__unfound_items_counter[PillarOfOOP] += 1

    @staticmethod
    def __roll_to_place_item_or_pit_or_door(placement_probability):
        """Decide whether to place an item/pit/door or not by doing a random
        sampling using its placement probability. Return True if the item
        should be placed or False if it should not.

        Parameters
        ----------
        placement_probability : float
            The probability that an item should be placed.

        Returns
        -------
        bool
            True if the random sampling decided an item or pit should be
            placed; otherwise, false.
        """
        return randomly_choose_between_two_outcomes(
            (True, False), placement_probability
        )

    def __room_is_in_maze(self, row, col):
        """
        Return True if the coordinates (row, col) correspond to a room in the
        maze. Otherwise, return False.

        Parameters
        ----------
        row : int
            Zero-based row index of the room position of interest.
        col : int
            Zero-based column index of the room position of interest.

        Returns
        -------
        bool
            True if room is within the outer perimeter of the maze; otherwise False.
        """
        return row in range(0, self.num_rows) and col in range(self.num_cols)

    def __set_room_doors_on_traversal_step(self, previous_room, this_room, trivia_db):
        """
        When traversing from one room to adjacent room while building the maze,
        set the sides of each room passed through to be doors.

        Parameters
        ----------
        previous_room : Room
            The previous room (stepped out of).
        this_room : Room
            The current room (stepped out into from previous room).
        trivia_db : TriviaDatabase
            A database from which questions and answers can be obtained.
        """
        if previous_room is None:
            return

        previous_room_coords = previous_room.coords
        this_room_coords = this_room.coords

        if this_room_coords[0] > previous_room_coords[0]:
            # Step was in the south direction. Open south side of previous room
            # and north side of current room.
            previous_room_side = Room.SOUTH
            this_room_side = Room.NORTH

        elif this_room_coords[0] < previous_room_coords[0]:
            # Step was in the north direction. Open north side of previous room
            # and south side of current room.
            previous_room_side = Room.NORTH
            this_room_side = Room.SOUTH

        elif this_room_coords[1] > previous_room_coords[1]:
            # Step was in the east direction. Open east side of previous room
            # and west side of current room.
            previous_room_side = Room.EAST
            this_room_side = Room.WEST

        elif this_room_coords[1] < previous_room_coords[1]:
            # Step was in the west direction. Open west side of previous room
            # and east side of current room.
            previous_room_side = Room.WEST
            this_room_side = Room.EAST

        # Assume we will create an unlocked door
        question_and_answer = None

        if self.__roll_to_place_item_or_pit_or_door(self.__LOCKED_DOOR_PROBABILITY):
            # If we rolled to create a locked door, create a question and
            # answer. Creating a Door with it will make the door locked.
            question_and_answer = self.__get_new_question_and_answer_from_db(trivia_db)

        previous_room.set_side(previous_room_side, Room.DOOR, question_and_answer)
        this_room.set_side(this_room_side, Room.DOOR)

    def __get_new_question_and_answer_from_db(self, trivia_db):
        """Get a new random question from the database and make sure we haven't
        already used it."""
        # FIXME: This could, in principle, run forever if we have exhausted the
        # database. Should check to see if the number of doors we've generated
        # is still less than the number of questions in the database...or just
        # allow repetition at that point.
        question_and_answer_info = trivia_db.get_question()
        qa_obj = question_and_answer_factory(**question_and_answer_info)

        while hash(qa_obj) in self.__used_question_and_answer_hashes:
            question_and_answer_info = trivia_db.get_question()
            qa_obj = question_and_answer_factory(**question_and_answer_info)
        self.__used_question_and_answer_hashes.add(hash(qa_obj))

        return qa_obj

    def __set_room_sides_to_doors_during_random_depth_first_traversal(
            self, row, col, previous_room, cumulative_visited, trivia_db
    ):
        """
        Perform a random depth-first traversal of the entire maze. This is done
        to decide where to place walls, by requiring that no rooms are
        revisited on the way "down" (i.e. increasing depth/distance from the
        starting room).

        Parameters
        ----------
        row : int
            Zero-based row index of the starting room for the search.
        col : int
            Zero-based column index of the starting room for the search.
        previous_room : Room
            The previous room (stepped out of).
        previous_room_coords : tuple of int
            The coordinates of the previous room (stepped out of).
        cumulative_visited : list of tuple
            Contains (row, col) coordinate tuples of *ALL* rooms previously
            visited. This list only grows in size during traversal.
        trivia_db : TriviaDatabase
            A database from which questions and answers can be obtained.
        """
        if not self.__room_is_in_maze(row, col) or (row, col) in cumulative_visited:
            # Done tracing out new rooms as far as we can in this
            # path...backtrack by letting this frame get popped off the call
            # stack
            return

        # Set relevant side of current and previous rooms to doors
        this_room = self.rooms[row][col]
        self.__set_room_doors_on_traversal_step(previous_room, this_room, trivia_db)
        previous_room = this_room

        potential_neighbor_coords = [
            (row, col + 1),  # east
            (row - 1, col),  # north
            (row, col - 1),  # west
            (row + 1, col),  # south
        ]

        # Mark current room as visited
        cumulative_visited.append((row, col))

        # Shuffle list of potential neighbors
        random.shuffle(potential_neighbor_coords)

        # Attempt to descend further into maze down each neighbor
        for neigh_coords in potential_neighbor_coords:
            self.__set_room_sides_to_doors_during_random_depth_first_traversal(
                *neigh_coords, previous_room, cumulative_visited, trivia_db
            )
