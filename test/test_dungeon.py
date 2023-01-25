from room import Room
from dungeon_items import (
    AbstractionPillar,
    EncapsulationPillar,
    InheritancePillar,
    PillarOfOOP,
    PolymorphismPillar,
)


class DungeonConstructionError(RuntimeError):
    """If there is any problem related to the construction of the dungeon"""


class MazeTooSmall(DungeonConstructionError):
    """If the the number of rows and/or columns passed into the maze is/are too small"""


class InvalidMinEntranceExitDistance(DungeonConstructionError):
    """If the minimum Manhattan distance between the (randomly generated)
    entrance and exit is impossibly large relative to the size of the dungeon
    maze."""


class MazeNotTraversible(DungeonConstructionError):
    """If an adventurer could not possibly reach the exit from the entrance."""


class MazeHasNoReachableDeadEnds(DungeonConstructionError):
    """If the maze generated does not contain a single dead end traversable
    from the entrance."""


class FailedToFindValidRoomDecoration(DungeonConstructionError):
    """If the decoration of the dungeon with potions, pits, and pillars is invalid."""


class MazeIsMissingReachablePillar(FailedToFindValidRoomDecoration):
    """If one of the pillars is not reachable from the entrance"""


class InvalidMazeSubsetCoords(DungeonConstructionError):
    """Raised if an invalid pair of rooms are passed to a method."""


def room_is_in_maze(maze, row, col):
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
    return row in range(0, maze.num_rows) and col in range(maze.num_cols)


def depth_first_search(
    maze, row, col, visited, goal
):  # pylint: disable=too-many-branches,too-many-return-statements
    """Do a depth-fetch search for the exit of the maze starting from the
    room with coordinates (row, col). This is meant to be called
    recursively, starting from the entrance.

    Parameters
    ----------
    row : int
        Zero-based row index of the starting room for the search.
    col : int
        Zero-based column index of the starting room for the search.
    visited : list of tuple
        Contains (row, col) coordinate tuples of rooms previously visited.
    goal : str or PillarOfOOP
        What to search for. This can be the string "exit", the string "dead
        end", or a subclass of PillarOfOOP.

    Returns
    -------
    bool
        True if the exit was reached; otherwise False.
    """
    if (not room_is_in_maze(maze, row, col)) or (row, col) in visited:
        return False

    this_room = maze.rooms[row][col]
    if goal == "exit":
        if this_room.is_exit():
            return True
    elif goal == "dead end":
        if (
            this_room.is_dead_end()
            and not this_room.is_entrance()
            and not this_room.is_exit()
        ):
            return True
    elif issubclass(goal, PillarOfOOP):
        if isinstance(this_room.get_pillar(), goal):
            return True

    # Mark this room as visited
    visited.append((row, col))

    # Try moving east
    if this_room.get_side(Room.EAST) == Room.DOOR:
        if depth_first_search(maze, row, col + 1, visited, goal):
            return True

    # Try moving north
    if this_room.get_side(Room.NORTH) == Room.DOOR:
        if depth_first_search(maze, row - 1, col, visited, goal):
            return True

    # Try moving west
    if this_room.get_side(Room.WEST) == Room.DOOR:
        if depth_first_search(maze, row, col - 1, visited, goal):
            return True

    # Try moving south
    if this_room.get_side(Room.SOUTH) == Room.DOOR:
        if depth_first_search(maze, row + 1, col, visited, goal):
            return True

    # Couldn't reach exit from any directions...backtrack
    visited.pop()

    return False


def test_ensure_maze_is_traversable(dungeon):
    """
    Ensure that it is possible to get from the entrance to the exit.

    Raises
    ------
    MazeNotTraversible
        If the exit cannot be reached from the entrance due to walls.
    """
    if not depth_first_search(dungeon, *dungeon.entrance, [], "exit"):
        raise MazeNotTraversible(
            "A valid maze must have an exit that is reachable from the "
            "entrance."
        )


def test_ensure_maze_has_at_least_one_dead_end(dungeon):
    """
    Ensure the maze contains at least one dead end that is reachable from
    the entrance. A dead end is defined as a room with 3 of its 4 sides
    consisting of walls.

    Raises
    ------
    MazeHasNoReachableDeadEnds
        If there was not a single dead end that could be reached from the
        entrance due to walls.
    """
    if not depth_first_search(dungeon, *dungeon.entrance, [], "dead end"):
        raise MazeHasNoReachableDeadEnds(
            "A valid maze must have at least one dead end reachable from "
            "the entrance."
        )


def test_ensure_all_pillars_reachable(dungeon):
    """
    Ensure that it is possible to reach each of the four pillars from the
    entrance, ignoring the fact that pits might kill the adventurer.

    Raises
    ------
    MazeIsMissingReachablePillar
        If the placement of pillars is such that at least one of the four
        could not be traversed to from the entrance due to walls.
    """
    for pillar_type in (
        AbstractionPillar,
        EncapsulationPillar,
        InheritancePillar,
        PolymorphismPillar,
    ):
        if not depth_first_search(dungeon, *dungeon.entrance, [], pillar_type):
            raise MazeIsMissingReachablePillar(
                f"The maze does not have a reachable {str(pillar_type())}"
            )
