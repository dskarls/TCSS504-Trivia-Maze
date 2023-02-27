from enum import Enum, auto

from adventurer import Adventurer
from maze import Maze
from room import Room
from trivia_maze_model import TriviaMazeModel
from trivia_database import SQLiteTriviaDatabase


class TriviaMaze(TriviaMazeModel):
    """
    Driver for maze adventure game
    NOTE: There is a hidden command, currently set to the key 'z' that can be
    used to display the entire maze at any iteration of the game.

    Class Attributes
    ------------------
    __DEFAULT_NUM_ROWS : int
        Number of rows to use if user skips through rows prompt.
    __DEFAULT_NUM_COLS: int
        Number of columns to use if user skips through rows prompt.

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

    Methods
    -------
    __get_adjacent_rooms_in_maze
        Get a list of all rooms in the maze that are adjacent to the
        adventurer's current room.
    __apply_pit_damage_to_adventurer
        Apply the damage value of a pit to an adventurer when they step into it.
    move_adventurer
        Moves the adventurer.
    __can_adventurer_move
        Checks if move is legal.
    __get_adventurer_room
        Gets the room the adventurer is in.
    use_item
        Consumes an item from the adventurer's inventory.
    __unlock_trivia_door
        Unlocks a locked trivia door
    get_adventurer_hp
        Returns the adventurer's hit points
    get_adventurer_coords
        Returns a tuple of the room's coordinates the adventurer is in.
    """

    class __Items(Enum):
        HEALING_POTION = auto()
        VISION_POTION = auto()
        MAGIC_KEY = auto()

    __ITEMS = {
        __Items.HEALING_POTION: "healing potion",
        __Items.VISION_POTION: "vision potion",
        __Items.MAGIC_KEY: "magic key",
    }

    def __init__(self, num_rows, num_cols, db_file_path):
        super().__init__()
        self.__event_log_buffer = []
        self.__question_and_answer_buffer = []

        self.num_rows = num_rows
        self.num_cols = num_cols

        self.__db = SQLiteTriviaDatabase(db_file_path)

        self.__maze = Maze(num_rows, num_cols, self.__db)

        self.__adventurer = Adventurer()

        # Place adventurer in entrance room
        (
            self.__adventurer_current_row,
            self.__adventurer_current_col,
        ) = self.__maze.entrance

        # Set entrance room as visited
        self.__maze.rooms[self.__maze.entrance[0]][
            self.__maze.entrance[1]
        ].visited = True

        self.__direction_attempt = None

    def move_adventurer(self, direction):
        """
        Given a directional command will attempt to move the adventurer that
        direction if the move is legal (not a wall, not a locked/perm locked
        door).

        Parameters
        ----------
        direction : str
            direction the adventurer is trying to move.
        """
        self.__direction_attempt = direction

        door_or_wall = self.__get_adventurer_room().get_side(direction)

        if door_or_wall == Room.WALL:
            return

        elif door_or_wall.perm_locked:
            if len(self.__adventurer.get_magic_keys()) < 1:
                # FIXME: Tell controller to display the NeedMagicKey context
                return "Need magic key"

            # value to be returned to the controller
            return "Use magic key"

        elif door_or_wall.locked:
            # Door is not permanently locked, but is locked by a question and
            # answer. Put it in the question and buffer.
            self.__question_and_answer_buffer.append(
                door_or_wall.question_and_answer
            )

        else:
            # Passable door -- either wasn't locked to begin with or was
            # unlocked with a correct response to a question and answer
            if direction == Room.NORTH:
                self.__adventurer_current_row -= 1
            elif direction == Room.SOUTH:
                self.__adventurer_current_row += 1
            elif direction == Room.EAST:
                self.__adventurer_current_col += 1
            elif direction == Room.WEST:
                self.__adventurer_current_col -= 1

            # Mark the new room the adventurer has moved into as visited
            self.__maze.rooms[self.__adventurer_current_row][
                self.__adventurer_current_col
            ].visited = True

            # FIXME: Have adventurer pick up items and fall in pits

        self.__notify_observers()

    def __get_adventurer_room(self):
        """Returns the room the adventurer is currently in the maze."""
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
            A list of all the adjacent rooms that fall within the maze.
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
        PIT_STR = (
            f"You fell into a pit and sustained {pit.damage_value} damage! "
            f"{self.__adventurer.hit_points} health remaining!"
        )
        self.__event_log_buffer.append(PIT_STR)
        self.__notify_observers()

    def get_rooms(self):
        """Returns a 2d list of the rooms in the maze."""
        return self.__maze.rooms

    def use_item(self, item):
        """
        This method checks which item the adventurer used and will make the appropriate
        method calls.
        Parameters
        ----------
        item : str
            One of the consumable items the adventurer can use.
        """
        if item == self.__ITEMS[self.__Items.HEALING_POTION]:
            # Use healing potion
            hit_points_recovered = self.__adventurer.consume_healing_potion()
            if hit_points_recovered:
                HEALTH_USE_STR = (
                    "You consume a healing potion and gain "
                    f"{hit_points_recovered} hit points! "
                    f"{self.__adventurer.hit_points} health remaining."
                )
                self.__event_log_buffer.append(HEALTH_USE_STR)

        elif item == self.__ITEMS[self.__Items.VISION_POTION]:
            # Use vision potion
            vision_potion = self.__adventurer.consume_vision_potion()

            # Get set of adjacent rooms inside maze and set the rooms as
            # visited
            for room in self.__get_adjacent_rooms_in_maze(
                self.__get_adventurer_room()
            ):
                room.visited = True

            self.__event_log_buffer.append(f"You used a {str(vision_potion)}!")

        elif item == self.__ITEMS[self.__Items.MAGIC_KEY]:
            magic_key = self.__adventurer.consume_magic_key()

            self.__unlock_perm_locked_door()
            # TODO: Move adventurer into correct room after unlocking door
            self.__event_log_buffer.append(f"You used a {str(magic_key)}!")

        self.__notify_observers()

    def __unlock_perm_locked_door(self):
        """Unlocks a permanently locked trivia door in the room the adventurer
        is in along the direction they tried to move. This should be called if
        the player used a magic key.
        """
        current_room = self.__get_adventurer_room()
        current_room.get_side(self.__direction_attempt).perm_locked = False

    def __unlock_trivia_door(self):
        """Unlocks a locked trivia door in the room the adventurer is in along
        the direction they tried to move. This should be called if they answer
        a Q&A correctly.
        """
        current_room = self.__get_adventurer_room()
        current_room.get_side(self.__direction_attempt).locked = False

    def __perm_lock_trivia_door(self):
        """Permanently locks a trivia door in the room the adventurer is in
        along the direction they tried to move. This should be called if they
        answer a Q&A incorrectly.
        """
        current_room = self.__get_adventurer_room()
        current_room.get_side(self.__direction_attempt).perm_locked = True

    def inform_player_answer_correct_or_incorrect(self, answer_was_correct):
        """Informs the model whether the player's response to the latest
        question pulled from the Q&A buffer was correct or not. If it was,
        unlock the relevant door and move the adventurer into the room on the
        other side of the door. If not, permanently lock that door."""
        if answer_was_correct:
            # Unlock the relevant door
            self.__unlock_trivia_door()

            # Move adventurer
            self.move_adventurer(self.__direction_attempt)
        else:
            self.__perm_lock_trivia_door()

    def get_adventurer_hp(self):
        """Returns the adventurer's current hit points"""
        return self.__adventurer.hit_points

    def get_adventurer_coords(self):
        """Returns a tuple of the adventurer's current coordinates in the maze."""
        return self.__adventurer_current_row, self.__adventurer_current_col

    def __check_loss(self):
        """
        Checks to see if there is a traversable path from the adventurer's current
        location to the exit. Adventurer can still win if within their possible
        path there is a magic key.

        Returns
        -------
        bool
            Will return True if the adventurer still has the ability to win with
            the current state of the maze. Otherwise False if no possibilty to
            win.
        """
        DIRECTIONS = [Room.NORTH, Room.EAST, Room.SOUTH, Room.WEST]
        TOTAL_ROOMS = self.__maze.num_rows * self.__maze.num_cols

        visited_rooms = []
        invalid_rooms = []
        inaccessible_rooms = self.__get_inaccessible_rooms()
        current_room = self.__get_adventurer_room()
        pillars_found = list(self.__adventurer.get_pillars_found())
        exit_found = False

        while (
            len(visited_rooms) + len(invalid_rooms) + len(inaccessible_rooms)
            < TOTAL_ROOMS
        ):
            moved_to_new_room = False
            # check if we have moved into the exit room
            if current_room.is_exit():
                exit_found = True
            # check if the room has a key
            if current_room.contains_magic_key():
                return True
            # check if room has a pillar
            if current_room.contains_pillar():
                # add pillar to found list
                pillars_found.append(current_room.get_pillar())

            # check if adv has locked themselves in a room
            if self.__get_adventurer_room() in inaccessible_rooms:
                return False
            # loop through to find a valid direction to move into another room
            for direction in DIRECTIONS:
                # check direction won't put us into a visited room
                next_room = self.__move_to_new_room(current_room, direction)
                if next_room in visited_rooms or next_room in invalid_rooms:
                    # if so continue direction loop to find new direction
                    continue
                # if we havent been to that room...
                # check if a side isnt a wall or permanently locked and continue in that direction
                if not self.__wall_or_perm(current_room, direction):
                    # mark current room has having been visited
                    visited_rooms.append(current_room)
                    # move to the next room
                    current_room = next_room
                    moved_to_new_room = True
                    break
            # continue loop if successfully moved to a new room
            if moved_to_new_room:
                continue
            # went through all directions this room has no valid paths
            # need to backtrack and try new path
            if len(visited_rooms) > 0:
                invalid_rooms.append(current_room)
                current_room = visited_rooms.pop()
            else:
                # no other possible paths forward
                return False
        # check if the room is the exit and all pillars have been found
        if exit_found and len(pillars_found) == 4:
            return True
        # if all rooms have been considered no possible path to victory
        return False

    def __get_inaccessible_rooms(self):
        """
        Helper method that scans through the whole maze and checks if the room is
        blocked from being accessed through normal means. Locked trivia doors are
        not considered as blocking obstacles as the player may answer correctly.
        Does not consider magic key's ability to open perm locked doors as this is
        handled in the check_loss method.

        Returns
        -------
        inaccesible_rooms : list
            rooms that the adventurer will not have the ability to reach with out
            the use of a magic key
        """
        inaccessible_rooms = []
        DIRECTIONS = [Room.NORTH, Room.EAST, Room.SOUTH, Room.WEST]
        for row in range(self.__maze.num_rows):
            for col in range(self.__maze.num_cols):
                wall_count = 0
                perm_door_count = 0
                for direction in DIRECTIONS:
                    if (
                        self.__maze.rooms[row][col].get_side(direction)
                        == Room.WALL
                    ):
                        wall_count += 1
                    elif (
                        self.__maze.rooms[row][col]
                        .get_side(direction)
                        .perm_locked
                    ):
                        perm_door_count += 1
                if wall_count + perm_door_count == 4:
                    inaccessible_rooms.append(self.__maze.rooms[row][col])
        return inaccessible_rooms

    def __move_to_new_room(self, room, direction):
        """
        Will move a room pointer to an adjacent room based on the given direction
        and the ability to move to the next room.

        Parameters
        ----------
        room : Room
            A Room object used as a current room pointer
        direction : str
            Direction the room pointer will move in the maze

        Returns
        -------
        new_room : Room
            Will return a new room that is adjacent in the maze based off the
            given direction. Returns the same room if can't move in the given
            direction.
        """
        if self.__wall_or_perm(room, direction):
            return room

        if direction == Room.NORTH:
            new_room = self.__maze.rooms[room.coords[0] - 1][room.coords[1]]
        elif direction == Room.SOUTH:
            new_room = self.__maze.rooms[room.coords[0] + 1][room.coords[1]]
        elif direction == Room.EAST:
            new_room = self.__maze.rooms[room.coords[0]][room.coords[1] + 1]
        elif direction == Room.WEST:
            new_room = self.__maze.rooms[room.coords[0]][room.coords[1] - 1]
        return new_room

    def __wall_or_perm(self, room, direction):
        side = room.get_side(direction)
        if side == Room.WALL:
            return True
        elif side.perm_locked:
            return True
        return False

    def register_observer(self, observer):
        """Add a TriviaMazeModelObserver object to the registered list of
        observers tracked by the model."""
        self._maze_observers.append(observer)

    def __notify_observers(self):
        for observer in self._maze_observers:
            observer.update()

    def get_event_log_buffer_contents(self):
        """If there are any entries in the event log buffer, remove and return
        them."""
        log_contents = self.__event_log_buffer.copy()
        self.__event_log_buffer.clear()
        return log_contents

    def flush_question_and_answer_buffer(self):
        """If a question is in the Q&A buffer, remove and return it."""
        if self.__question_and_answer_buffer:
            return self.__question_and_answer_buffer.pop()

    def reset(self):
        """If the user returns to the main menu after starting a game and then
        starts a new game, the model should regenerate a new maze and a new
        adventurer, etc."""
        # FIXME: Implement this!
        pass
