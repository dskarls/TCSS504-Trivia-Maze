import pytest

from adventurer import Adventurer


def test_adventurer_init_valid_name():
    """Ensure that an adventurer can be created with a valid name"""
    Adventurer("Indy")  # pylint: disable=expression-not-assigned


def test_adventurer_init_invalid_name():
    """Ensure we can't create an adventurer with an empty name"""
    try:
        Adventurer("")
    except:  # pylint: disable=bare-except
        # Some kind of exception was raised. Correct behavior.
        pass
    else:
        raise AssertionError(
            "Shouldn't be able to create an Adventurer with an empty name"
        )


def test_adventurer_set_hit_points(adventurer):
    """Make sure we can successfully add hit points"""
    initial_hit_points = adventurer.hit_points

    # Add enough hit points to hit max
    diff_to_max = pytest.HIT_POINTS_MAX - initial_hit_points
    adventurer.hit_points += diff_to_max
    assert adventurer.hit_points == pytest.HIT_POINTS_MAX

    # Adding should do nothing since hit points cap at
    # pytest.HIT_POINTS_MAX
    adventurer.hit_points += 15
    assert adventurer.hit_points == pytest.HIT_POINTS_MAX

    # Subtract pytest.HIT_POINTS_MAX and make sure HP is zero
    adventurer.hit_points -= pytest.HIT_POINTS_MAX
    assert adventurer.hit_points == pytest.HIT_POINTS_MIN

    # Subtract more hit points and ensure HP is still pytest.HIT_POINTS_MIN
    adventurer.hit_points -= 23
    assert adventurer.hit_points == pytest.HIT_POINTS_MIN

    # Add 15 hit points and check that the value is appropriate
    hp_to_add = 15
    adventurer.hit_points += hp_to_add
    assert adventurer.hit_points == hp_to_add

    # Subtract some quantity less than what we added and make sure the HP gets
    # set right
    hp_to_subtract = 7
    adventurer.hit_points -= hp_to_subtract
    assert adventurer.hit_points == hp_to_add - hp_to_subtract


def test_adventurer_consume_healing_potion(adventurer, healing_potion):
    """Check that an adventurer can pick up and consume a healing potion,
    receiving the correct amount of HP restoration (which, recall, cannot
    restore health above 100)."""
    adventurer.pick_up_item(healing_potion)

    init_hp = adventurer.hit_points
    adventurer.consume_healing_potion()
    assert adventurer.hit_points == min(
        100, init_hp + healing_potion.healing_value
    )


def test_adventurer_consume_multiple_healing_potions(
    adventurer, healing_potion_pair
):
    """Check that if we give an adventurer two healing potions, the one with
    the smaller healing value is consumed first."""

    healing_potion1, healing_potion2 = healing_potion_pair

    adventurer.pick_up_item(healing_potion1)
    adventurer.pick_up_item(healing_potion2)

    init_hp = adventurer.hit_points
    if healing_potion1 < healing_potion2:
        first_healing_potion = healing_potion1
        second_healing_potion = healing_potion2
    else:
        first_healing_potion = healing_potion2
        second_healing_potion = healing_potion1

    adventurer.consume_healing_potion()
    assert adventurer.hit_points == min(
        100, init_hp + first_healing_potion.healing_value
    )
    intermediate_hp = adventurer.hit_points
    adventurer.consume_healing_potion()
    assert adventurer.hit_points == min(
        100, intermediate_hp + second_healing_potion.healing_value
    )
