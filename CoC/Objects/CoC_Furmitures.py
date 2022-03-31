"""
Call of Cthulhu base Furniture class/base exception/common furniture's.

Base class for all furniture objects in the game.

Common furniture's inherit from the furniture class/sub-classes, (multiple inheritance)

    * Chair: common wood chair                                # FNT-STN-000001

"""

from CoC.Objects.CoC_Objects import CoCObject
from CoC.Objects.CoC_Objects import Mass, Seats, Parts, Moveable, Information


# ---Base Object -------------------------------------------------------------------------------------------------------------------------------------
# --- Exception class ---
class CoCFurnitureException(Exception):
    """
    Base exception class raise by 'CoCFurniture' objects.

    Args:
        msg (str): informative error message.
    """

    def __init__(self, msg):
        self.msg = msg

    pass  # END of CLASS


# --- CoCFurniture class -------------------------------------------------------
class CoCFurnitures(CoCObject):
    """
    Base class for all object that fall under the 'furniture' type.
        * Has Mass

    GUID = "FNT"
    """

    def at_object_creation(self):
        super(CoCFurnitures, self).at_object_creation()

        self.db.obj_mass = Mass(1.0, 1.0)

    # --- Hooks ----------------------------------------------------------------

    def return_appearance(self, looker):
        """

        """
        text = super().return_appearance(looker)

        return text

    # --- Methods --------------------------------------------------------------

    pass  # END of CLASS


# --- Common Furniture -------------------------------------------------------------------------------------------------------------------------------
# --- Chair class ---
class Chair(CoCFurnitures):
    """
    A common wood chair
        + Has Mass
        * Has Parts
        * Has Materials (Parts)
        * Has Movement
        * Has Seats

    GUID: "FNT-CHR-000001"
    """

    # --- Constructor ----------------------------------------------------------
    def at_object_creation(self):
        super(Chair, self).at_object_creation()
        self.db.sub_classes = ""

        # Important attributes to set for ALL objects
        self.db.obj_guid = "FNT-CHR-000001"                                                         # set GUID
        self.db.obj_lvis = True                                                                     # set Object look visibility

        parts = {self.name + " " + 'body': ['wood', 1, 2500.0],                                     # name: [material, amount, mass]
                 self.name + " " + 'upholstery': ['cloth', 1, 150.0],                               #
                 self.name + " " + 'filling': ['vegetable hair', 1, 350.0],                         #
                 self.name + " " + 'screw': ['iron', 16, 1.8],                                      #
                 }                                                                                  #
        self.db.obj_parts = Parts(parts)                                                            # set PARTS
        self.db.sub_classes += "P:"

        loc = self.get_room_location(self)                                                          #
        temp_gravity = loc.db.gravity                                                               #
                                                                                                    #
        temp_mass = 0                                                                               #
        for key, value in parts.items():                                                            #
            temp_mass += (value[1] * value[2])                                                      #
                                                                                                    #
        self.db.obj_mass = Mass(temp_mass, temp_gravity)                                            # set MASS and GRAVITY
        self.db.sub_classes += "M:"

        locks = {'get': ['false()', 'You can NOT put this object in your inventory.'],              #
                 }                                                                                  #
        self.db.obj_move = Moveable(self, locks)                                                    # set MOVE
        self.db.sub_classes += "L:"

        # Attributes only for chairs
        self.db.obj_seats = Seats(1)                                                                # set SEATS
        self.db.sub_classes += "S:"

        # Extra-Information about the object
        self.db.obj_info = Information(self)                                                        # set Information

    # --- Properties -----------------------------------------------------------

    # --- Methods --------------------------------------------------------------
    def show_info(self):
        """
        Extra info from the object (only for admin/ builders), show by executing a command.
        """

        obj_info = self.db.obj_info.info()

        return obj_info

    pass  # END of CLASS
