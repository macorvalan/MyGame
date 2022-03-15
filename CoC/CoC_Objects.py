"""

"""

from evennia import DefaultObject
from AU_RPGSystem.AU_RPGCommunications import AURPGRPObject


class CoCObject(AURPGRPObject):
    """


    """

    def at_object_creation(self):
        super(CoCObject, self).at_object_creation()
        self.db.prueba = 42

    def return_appearance(self, looker):
        text = super().return_appearance(looker)

        return text

    pass
