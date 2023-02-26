import pathlib
import random

import pytest

from adventurer import Adventurer
from maze import Maze
from maze_items import HealingPotion
from room import Room
from trivia_database import SQLiteTriviaDatabase

# Fix random seed so tests always run the same way
random.seed(99)

###############################################################################
# Fixture configuration (local to this module)
###############################################################################
# Min and max possible hit points an adventurer can have
HIT_POINTS_MIN = 0
HIT_POINTS_MAX = 100

# How many randomly initialized healing potion fixtures to generate
NUM_HEALING_POTIONS_TO_GENERATE = 10
NUM_HEALING_POTION_PAIRS_TO_GENERATE = 10

# Min and max number of rows and columns to use for randomly generated maze
# fixtures
MAZE_MIN_NUM_ROWS = 3
MAZE_MAX_NUM_ROWS = 10
MAZE_MIN_NUM_COLS = MAZE_MIN_NUM_ROWS
MAZE_MAX_NUM_COLS = MAZE_MAX_NUM_ROWS

# How many random maze fixtures to generate with the above parameters
NUM_MAZES_TO_GENERATE = 10


###############################################################################
# Helper methods
###############################################################################
def get_random_maze_shape(
    min_num_rows, max_num_rows, min_num_cols, max_num_cols, num_samples
):
    """
    Returns an iterable containing ``num_samples`` pairs of integers, each of
    which is a two-component list. The first component of each integer pair is
    in the range [min_num_rows, max_num_rows], while the second is in the range
    [min_num_cols, max_num_cols].

    Parameters
    ----------
    min_num_rows : int
        The minimum number of rows to return in the shape parameter integer
        pair.
    max_num_rows : int
        The maximum number of rows to return in the shape parameter integer
        pair.
    min_num_cols : int
        The minimum number of columns to return in the shape parameter integer
        pair.
    max_num_cols : int
        The maximum number of columns to return in the shape parameter integer
        pair.
    num_samples : int
        The number of integer pairs to generate.

    Returns
    -------
    zip
        A zip generator that yields ``num_samples`` pairs one-by-one.
    """
    return zip(
        random.choices(range(min_num_rows, max_num_rows + 1), k=num_samples),
        random.choices(range(min_num_cols, max_num_cols + 1), k=num_samples),
    )


def generate_healing_value_pairs(hit_points_min, hit_points_max, num_samples):
    """Returns an iterable containing ``num_samples`` pairs of integers. The
    first component of each integer pair in the range [hit_points_min,
    (hit_points_max-hit_points_min)//2] while the second is in the range
    ((hit_points_max-hit_points_min)//2, hit_points_max]. This guarantees that
    the first integer will always be less than the second.

    Parameters
    ----------
    hit_points_min : int
        Inclusive lower bound on the number of hit points a potion can restore.
    hit_points_max : int
        Inclusive upper bound on the number of hit points a potion can restore.
    num_samples : int
        How many healing value pairs to return.

    Returns
    -------
    zip
        An array of healing values in the specified range.
    """
    hit_points_mid = (hit_points_max - hit_points_min) // 2
    return zip(
        random.choices(
            range(hit_points_min, hit_points_mid + 1), k=num_samples
        ),
        random.choices(
            range(hit_points_mid + 1, hit_points_max + 1), k=num_samples
        ),
    )


def generate_healing_potion_pairs(
    hit_points_min, hit_points_max, num_healing_potion_pairs
):
    """Returns an iterable containing ``num_healing_potion_pairs`` pairs of
    HealingPotions. Each potion will have a healing value in the range
    [hit_points_min, hit_points_max].

    Parameters
    ----------
    hit_points_min : int
        Inclusive lower bound on the number of hit points a potion can restore.
    hit_points_max : int
        Inclusive upper bound on the number of hit points a potion can restore.
    num_healing_potion_pairs : int
        How many healing potion pairs to return.

    Returns
    -------
    zip
        An array of healing potion pairs.
    """
    potions1 = (
        HealingPotion(hp_min, hp_max)
        for hp_min, hp_max in generate_healing_value_pairs(
            hit_points_min, hit_points_max, num_healing_potion_pairs
        )
    )
    potions2 = (
        HealingPotion(hp_min, hp_max)
        for hp_min, hp_max in generate_healing_value_pairs(
            hit_points_min, hit_points_max, num_healing_potion_pairs
        )
    )
    return zip(potions1, potions2)


###############################################################################
# Fixtures
###############################################################################
@pytest.fixture
def adventurer():
    """An adventurer with randomly initialized hit points."""
    return Adventurer()


@pytest.fixture(
    params=generate_healing_value_pairs(
        HIT_POINTS_MIN, HIT_POINTS_MAX, NUM_HEALING_POTIONS_TO_GENERATE
    )
)
def healing_potion(request):
    min_healing_value, max_healing_value = request.param
    return HealingPotion(min_healing_value, max_healing_value)


@pytest.fixture(
    params=generate_healing_potion_pairs(
        HIT_POINTS_MIN, HIT_POINTS_MAX, NUM_HEALING_POTION_PAIRS_TO_GENERATE
    )
)
def healing_potion_pair(request):
    return request.param


@pytest.fixture
def trivia_database():
    DB_FILE_PATH = pathlib.Path("db") / "Lone_Rangers_QA_DB.csv"
    return SQLiteTriviaDatabase(DB_FILE_PATH)


@pytest.fixture(
    params=get_random_maze_shape(
        MAZE_MIN_NUM_ROWS,
        MAZE_MAX_NUM_ROWS,
        MAZE_MIN_NUM_COLS,
        MAZE_MAX_NUM_COLS,
        NUM_MAZES_TO_GENERATE,
    )
)
def maze(trivia_database, request):
    """A (randomly constructed) maze of the specified size"""
    num_rows, num_cols = request.param
    return Maze(num_rows, num_cols, trivia_database)


@pytest.fixture
def default_room():
    """A default room, which has all walls and no contents, located at
    coordinates (0, 0)."""
    return Room(0, 0)


def pytest_configure():
    """Used to add test config variables to pytest namespace so they can be
    accessed by tests."""
    pytest.HIT_POINTS_MIN = HIT_POINTS_MIN
    pytest.HIT_POINTS_MAX = HIT_POINTS_MAX
