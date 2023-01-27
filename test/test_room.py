from maze_items import AbstractionPillar, HealingPotion, VisionPotion, Pit
from room import Room


def test_room_place_and_get_pillar(default_room):
    """Check that we can place a pillar in a room and retrieve it"""
    assert default_room.get_pillar() is None

    pillar = AbstractionPillar()
    default_room.place_item(pillar)
    assert default_room.contains_pillar()
    assert default_room.get_pillar() is pillar


def test_room_is_dead_end(default_room):
    """Check that if we make a room a deade nd, it is detected as such. A dead
    end is a room with 3 walls and one door."""

    # A default room has all walls. Set the north side as a door and check that
    # it registers as a dead end
    default_room.set_side(Room.NORTH, Room.DOOR)
    assert default_room.is_dead_end()

    # Now set the west side to be a door and confirm that it's no longer a dead end
    default_room.set_side(Room.WEST, Room.DOOR)
    assert not default_room.is_dead_end()


def test_room_is_entrance(default_room):
    """Check that if we set a room as an entrance, it registers as one."""
    assert not default_room.is_entrance()
    default_room.set_entrance()
    assert default_room.is_entrance()


def test_room_is_exit(default_room):
    """Check that if we set a room as an exit, it registers as one."""
    assert not default_room.is_exit()
    default_room.set_exit()
    assert default_room.is_exit()


def test_room_is_pit(default_room):
    """Check that if we set a room as a pit, we can retrieve the pit."""
    pit = Pit(5, 13)
    default_room.set_pit(pit)
    assert default_room.get_pit() is pit


def test_remove_items(default_room):
    """Add a healing potion, a vision potion, and a pillar to the room and make
    sure they can all be reclaimed.

    NOTE: Item insertion and extraction order should not matter.
    """

    healing_potion = HealingPotion(5, 12)
    vision_potion = VisionPotion()
    pillar = AbstractionPillar()

    original_items = [healing_potion, vision_potion, pillar]
    for item in original_items:
        default_room.place_item(item)

    assert set(default_room.remove_items()) == set(original_items)


def test_reset_decorations(default_room):
    """Check that all items and a pit are removed from a room upon request."""
    healing_potion = HealingPotion(5, 12)
    vision_potion = VisionPotion()
    pillar = AbstractionPillar()

    original_items = [healing_potion, vision_potion, pillar]
    for item in original_items:
        default_room.place_item(item)

    pit = Pit(5, 13)
    default_room.set_pit(pit)

    # Remove everything from the room
    default_room.reset_decorations()

    assert default_room.remove_items() == []

    assert default_room.get_pit() is None


def test_set_side(default_room):
    """Guarantee that we can set and get each side of a room to a door or
    wall"""

    # Start off with all walls. Set and unset each side of the room to door and
    # back to wall
    for direction in (Room.EAST, Room.NORTH, Room.WEST, Room.SOUTH):
        assert default_room.get_side(direction) == Room.WALL
        default_room.set_side(direction, Room.DOOR)
        assert default_room.get_side(direction) == Room.DOOR
        default_room.set_side(direction, Room.WALL)
        assert default_room.get_side(direction) == Room.WALL
