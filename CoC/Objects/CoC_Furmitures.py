"""
Call of Cthulhu base Furniture class/base exception/common furniture's.

Base class for all furniture objects in the game.

Common furniture's inherit from the furniture class/sub-classes, (multiple inheritance)

    * Chair: common wood chair                                # FNT-STN-000001

"""

from CoC.Objects.CoC_Objects import CoCObject
from CoC.Objects.CoC_Objects import Mass, Volume, Seats, Parts, Movable, Stackable, Slots, Container, Information


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
        * Has Volume
        * Has Parts
        * Has Materials (Parts)
        * Has Movement
        * Has Slots
        * Has Seats
        * Is Stack
        * Is Not Container


    GUID: "FNT-CHR-000001"
    """

    # --- Constructor ----------------------------------------------------------
    def at_object_creation(self):
        super(Chair, self).at_object_creation()
        self.db.sub_classes = ""

        # Important attributes to set for ALL objects
        self.db.obj_category = "FNT-CHR-000001"                                                     # set GUID
        self.db.obj_lvis = True                                                                     # set Object look visibility

        self.db.obj_usable = True                                                                   # set if the object is USABLE
        self.db.obj_original = True                                                                 # set if the object has been MODIFIED
        self.db.obj_sub_location = self.location                                                    # set if the object has a SUB_LOCATION

        parts = {self.name + " " + 'body': ['wood', 1, 2500.0],                                     # name: [material, amount, mass]
                 self.name + " " + 'upholstery': ['cloth', 1, 150.0],                               #
                 self.name + " " + 'filling': ['vegetable hair', 1, 350.0],                         #
                 self.name + " " + 'screw': ['iron', 16, 1.8],                                      #
                 }                                                                                  #
        self.db.obj_parts = Parts(parts)                                                            # set PARTS
        self.db.sub_classes += "P:"

        loc = self.get_room_location()                                                              #
        temp_gravity = loc.db.gravity                                                               #
                                                                                                    #
        temp_mass = 0                                                                               #
        for key, value in parts.items():                                                            #
            temp_mass += (value[1] * value[2])                                                      #
                                                                                                    #
        self.db.obj_mass = Mass(temp_mass, temp_gravity)                                            # set MASS and GRAVITY
        self.db.sub_classes += "M:"

        self.db.obj_volume = Volume('2x2x5')                                                        # set VOLUME and SHAPE
        self.db.sub_classes += "V:"

        locks = {'get': ['false()', 'You can NOT put this object in your inventory.'],              # lock: condition, message
                 }                                                                                  #
        self.db.obj_move = Movable(self, locks)                                                     # set MOVE
        self.db.sub_classes += "L:"

        self.db.obj_stack = Stackable(Chair, True, 3)                                               # set STACK
        self.db.sub_classes += "K:"                                                                 #

        slots_dic = {'back': [1, 3.0, 15000]}                                                       #
        self.db.obj_slots = Slots(slots_dic)                                                        # set SLOTS
        self.db.sub_classes += 'O:'

        self.db.obj_container = Container(container=False)                                          # set CONTAINER

        # Attributes only for chairs
        seats = {'seat': 1}
        self.db.obj_seats = Seats(seats)                                                                # set SEATS
        self.db.sub_classes += "S:"

        # Extra-Information about the object
        self.db.obj_info = Information()                                                            # set Information

    # --- Properties -----------------------------------------------------------

    # --- Methods --------------------------------------------------------------

    def update_total_mass(self):
        """
        Update the mass of the object, when necessary.

        """

        self.db.obj_slots.update_total_mass()
        self.db.obj_container.update_total_mass()
        self.db.obj_stack.update_total_mass()
        self.db.obj_parts.update_total_mass()
        self.db.obj_seats.update_total_mass()

        slots_mass = self.db.obj_slots.total_mass
        container_mass = self.db.obj_container.total_mass
        stacks_mas = self.db.obj_stack.total_mass
        parts_mass = self.db.obj_parts.total_mass
        seats_mass = self.db.obj_seats.total_mass

        self.db.obj_mass.mass = slots_mass + container_mass + stacks_mas + parts_mass + seats_mass

    def show_info(self):
        """
        Extra info from the object (only for admin/ builders), show by executing a command.

        """

        return self.db.obj_info.update(self)

    pass  # END of CLASS
