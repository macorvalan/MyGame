"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia import DefaultRoom
from CoC.CoC_Rooms import CoCCharGenRoom
from CoC.CoC_Rooms import CoCRoom


class Room(CoCRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """

    def at_object_creation(self):
        super(Room, self).at_object_creation()

    pass


class CharGenRoom(CoCCharGenRoom):
    """
    Character Generation Room.

    Room used to generate the investigator for the first time
    or improve skills.
    """
    def at_object_creation(self):
        super(CharGenRoom, self).at_object_creation()

    pass
