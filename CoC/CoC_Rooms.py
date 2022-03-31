"""

"""

from AU_Modules.AU_RPGSystem.AU_RPGCommunications import AURPGRPRoom


class CoCRoom(AURPGRPRoom):
    """

    """

    def at_object_creation(self):
        super(CoCRoom, self).at_object_creation()

        self.db.room_guid = 'AAA-AAAA-000000'
        self.db.gravity = 1.0

    pass  # END of CLASS


class CoCCharGenRoom(AURPGRPRoom):
    """

    """

    def at_object_creation(self):
        super(CoCCharGenRoom, self).at_object_creation()

        self.db.room_guid = 'AAA-AAAA-000000'
        self.db.gravity = 1.0

    pass  # END of CLASS

