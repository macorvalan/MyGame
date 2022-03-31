"""
Call of Cthulhu base Object class/base exception/sub-classes

Base object class for every object in the game, it adds the following:

    * obj_guid attribute: unique identificator.
    * obj_lvis attribute: makes tho object visible or not when use the look command in a room.


Sub-classes adding attributes to the objects.

    * L Moveable: set the move properties of the object.
    * U Unbreakable: set if the object can be destroyed
    * C Container: set if the object is a container and the amount/capacity of its containers.
    * M Mass: set the weight of the object based on mass and gravity.
    * S Seats: set the amount od seats the object has.
    * P Parts: set the parts of an object
    * T Materials: set the materials of the object (parts), dictionary(material_name, %)
    * A Assemble:
    * D Disassemble:
    * O Slots:
    * E Mechanism:
    * Information: show extra information about the object

"""

from AU_Modules.AU_RPGSystem.AU_RPGCommunications import AURPGRPObject
from CoC.Objects.CoC_Materials import PROPERTIES_DICT, MATERIALS_PROPERTIES_DICT


# --- Base Object Exception --------------------------------------------------------------------------------------------------------------------------
class ObjectException(Exception):
    """
    Base exception class raise by 'Object' objects.

    Args:
        msg (str): informative error message.
    """

    def __init__(self, msg):
        self.msg = msg

    pass  # END of CLASS


# ---Base Object class -------------------------------------------------------------------------------------------------------------------------------
class CoCObject(AURPGRPObject):
    """
    Call of Cthulhu base Object class
    """

    # --- Constructor ----------------------------------------------------------
    def at_object_creation(self):
        super(CoCObject, self).at_object_creation()

        self.db.obj_guid = 'AAA-AAA-000000'
        self.db.obj_lvis = True

    # --- Hooks ----------------------------------------------------------------
    def return_appearance(self, looker):
        text = super().return_appearance(looker)

        return text

    # --- Methods --------------------------------------------------------------

    @staticmethod
    def get_room_location(obj):
        """
        Get the room where the object is, iterate throw containers to get a room.
        """
        loc = obj.location
        while loc.location is not None:
            loc = loc.location

        return loc

    pass  # END of CLASS


# --- Sub-Classes ------------------------------------------------------------------------------------------------------------------------------------
# --- MoveableException class ---
class MoveableException(Exception):
    """
    Base exception class raise by 'Seats' objects.

    Args:
        msg (str): informative error message.
    """

    def __init__(self, msg):
        self.msg = msg

    pass  # END of CLASS


# --- Moveable class ---
class Moveable(object):
    """
    Set the move properties of the object.
    """

    # --- Constructor ------------------------------------------------
    def __init__(self, set_obj, set_locks):
        self._locks = dict(set_locks)

        for key, value in set_locks.items():
            temp_lock = key + ':' + value[0]
            set_obj.locks.add(temp_lock)

            if key == 'get':
                set_obj.db.get_err_msg = value[1]
            elif key == 'mov':                                                  # TODO: Implement move command ---
                pass

    # --- Properties -----------------------------------------------------------
    # --- locks --- get/set
    @property
    def locks(self):
        return self._locks

    @locks.setter
    def locks(self, value):
        ex_msg = "Locks can be be assigned at object creation, or with the 'add' method."
        raise MoveableException(ex_msg)

    # --- Methods --------------------------------------------------------------
    def add(self, set_obj, add_locks):
        """
        Add a new lock to the object, checking for duplicates

        Args:
            set_obj: object to remove lock
            add_locks: locks to add, in the format {'key': ['condition', 'message'], ...}
        """
        for key, value in add_locks:
            if key not in self._locks:
                temp_lock = key + ':' + value[0]                                #
                set_obj.locks.add(temp_lock)                                    #
                #
                if key == 'get':                                                #
                    set_obj.db.get_err_msg = value[1]                           #
                elif key == 'mov':                                              # Add the lock to the object
                    pass                                                        #

                self._locks[key] = value                                        # Add the lock to the Moveable object
                pass
            else:
                ex_msg = "The lock specified is already present in the object, remove it first, than add the new lock"
                raise MoveableException(ex_msg)

    def remove(self, set_obj, rem_lock):
        """
        Remove a lock from the object, if exist.

        Args:
            set_obj: object to remove lock
            rem_lock: key of the lock to remove (get, mov lift, etc)
        """
        if rem_lock in self._locks:
            set_obj.locks.remove(rem_lock)                                      # Remove the lock from the object
            del self._locks[rem_lock]                                           # Remove the lock from the Moveable object
        else:
            ex_msg = "The lock specified do not exist in the object"
            raise MoveableException(ex_msg)

    pass  # END of CLASS


# --- Mass ---------------------------------------------------------------------
# --- MassException class ---
class MassException(Exception):
    """
    Base exception class raise by 'Mass' objects.

    Args:
        msg (str): informative error message.
    """

    def __init__(self, msg):
        self.msg = msg

    pass  # END of CLASS


# --- Mass class ---
class Mass(object):
    """
    Sub-class Mass to manage the weight of an object, it is based on mass and gravity.

    The mass is expressed in grams.
    """

    def __init__(self, mass, grav):
        self._mass = mass
        self._gravity = grav
        self._weight = self._mass * self._gravity

    # --- Properties -----------------------------------------------------------
    # --- mass --- get/set
    @property
    def mass(self):
        return round(self._mass, 6)

    @mass.setter
    def mass(self, value):
        self._mass = value
        # If mass is updated, the weight must be updated too.
        self._weight = self._mass * self._gravity

    # --- gravity --- get/set
    @property
    def gravity(self):
        return round(self._gravity, 6)

    @gravity.setter
    def gravity(self, value):
        self._gravity = value
        # If gravity is updated, the weight must be updated too.
        self._weight = self._mass * self._gravity

    # --- weight --- get/set
    @property
    def weight(self):
        return round(self._weight, 6)

    @weight.setter
    def weight(self, value):
        ex_msg = "Weight value MUST be calculated."
        raise MassException(ex_msg)

    # --- Methods --------------------------------------------------------------

    def weight_mg(self):
        """
        return the weight of the object in mili-grams.
        """
        return round(self._weight * 1000.0, 6)

    def weight_gr(self):
        """
        return the weight of the object in grams (default unit).
        """
        return round(self._weight, 6)

    def weight_kg(self):
        """
        return the weight of the object in kilograms.
        """
        return round(self._weight / 1000.0, 6)

    def weight_tn(self):
        """
        return the weight of the object in tonnes.
        """
        return round(self._weight / 1000000.0, 6)

    pass  # END of CLASS


# --- Seats --------------------------------------------------------------------
# --- SeatsException class ---
class SeatsException(Exception):
    """
    Base exception class raise by 'Seats' objects.

    Args:
        msg (str): informative error message.
    """

    def __init__(self, msg):
        self.msg = msg

    pass  # END of CLASS


# --- Seats class ---
class Seats(object):
    """
    Add seats to the object, and the necessary methods to manage the seats.
    """

    def __init__(self, seats):
        self._seats = seats
        self._occupants = {}
        self._free_seats = seats

    # --- Properties -----------------------------------------------------------
    # --- seats --- get/set
    @property
    def seats(self):
        return self._seats

    @seats.setter
    def seats(self, value):
        if not self._occupants:
            ex_msg = "To modified the amount of seats there be no occupants on the seats. Use clear_seats method"
            raise SeatsException(ex_msg)
        else:
            self._seats = value
            self._free_seats = value

    # --- occupants --- get/set
    @property
    def occupants(self):
        return self._occupants

    @occupants.setter
    def occupants(self, value):
        ex_msg = "Seats occupants can only be modified with the respective methods"
        raise SeatsException(ex_msg)

    # --- free_seats --- get/ser
    @property
    def free_seats(self):
        return self._free_seats

    @free_seats.setter
    def free_seats(self, value):
        ex_msg = "Free-seats can only be modified with the respective methods"
        raise SeatsException(ex_msg)

    # --- Methods --------------------------------------------------------------

    def at_enter_seat(self, obj):
        """
        Add an object to the seat, if there are free seats.
        """
        if self._free_seats > 0:
            self._free_seats -= 1
            self._occupants[obj.name] = obj
        else:
            ex_message = "Not enough free seats in the object."
            raise SeatsException(ex_message)

    def at_leave_seat(self, obj):
        """
        Remove and object from the seat, if it is in the seats.
        """
        if obj not in self._occupants:
            ex_message = "Object not found in seats {}.".format(obj)
            raise SeatsException(ex_message)
        else:
            del self._occupants[obj]
            self._free_seats += 1

    def clear_seats(self):
        """
        Clear all the occupants and set the free seats to default value.
        """

        self._occupants.clear()
        self._free_seats = self._seats

    pass  # END of CLASS


# --- Parts ----------------------------------------------------------
# --- PartsException class ---
class PartsException(Exception):
    """
    Base exception class raise by 'Parts' objects.

    Args:
        msg (str): informative error message.
    """

    def __init__(self, msg):
        self.msg = msg

    pass  # END of CLASS


# --- Parts class ---
class Parts(object):
    """
    Set the parts of the object.
    """

    def __init__(self, parts):
        self._parts = []

        for key, value in parts.items():
            temp_obj = Part(key, value)
            self._parts.append(temp_obj)
            del temp_obj

    # --- Properties -------------------------------------------------
    # --- parts --- get/set
    @property
    def parts(self):
        return self._parts

    @parts.setter
    def parts(self, value):
        ex_msg = "Parts can only be assign at the object creation"
        raise PartsException(ex_msg)

    # --- Methods --------------------------------------------------------------

    def parts_amount(self):
        return len(self._parts)

    pass  # END of CLASS


# --- Part class -----------------------------------------------------
class Part(object):
    """
    Set every part in the list of parts with material properties.

    Args:
        {'key': ['material', amount, unitary weight]}
    """

    def __init__(self, key, value):
        self._part_name = key
        self._part_material = Materials(value[0])
        self._part_amount = value[1]
        self._part_mass = value[2]

    # --- Properties -------------------------------------------------
    # --- obj_name --- get/set
    @property
    def part_name(self):
        return self._part_name

    @part_name.setter
    def part_name(self, value):
        ex_msg = "Parts values can only be assigned during object creation. Can NOT be modified."
        raise PartsException(ex_msg)

    # --- obj_material --- get/set
    @property
    def part_material(self):
        return self._part_material

    @part_material.setter
    def part_material(self, value):
        ex_msg = "Parts values can only be assigned during object creation. Can NOT be modified."
        raise PartsException(ex_msg)

    # --- obj_amount --- get/set
    @property
    def part_amount(self):
        return self._part_amount

    @part_amount.setter
    def part_amount(self, value):
        ex_msg = "Parts values can only be assigned during object creation. Can NOT be modified."
        raise PartsException(ex_msg)

    # --- obj_mass --- get/set
    @property
    def part_mass(self):
        return self._part_mass

    @part_mass.setter
    def part_mass(self, value):
        ex_msg = "Parts values can only be assigned during object creation. Can NOT be modified."
        raise PartsException(ex_msg)

    pass  # END of CLASS


# --- Materials ------------------------------------------------------
# --- MaterialsException class ---
class MaterialsException(Exception):
    """
    Base exception class raise by 'Materials' objects.

    Args:
        msg (str): informative error message.
    """

    def __init__(self, msg):
        self.msg = msg

    pass  # END of CLASS


# --- Materials class ---
class Materials(object):
    """
    Set the materials witch the object is made.
    """

    def __init__(self, material):
        self._material = material
        self._properties = dict(PROPERTIES_DICT)

        for MPD_key, MPD_values in MATERIALS_PROPERTIES_DICT.items():  # Iter through materials DICT
            if self._material == MPD_key:  # If material is found
                for MPD_value in MPD_values:  # Iter through properties and update
                    d_key, d_value = MPD_value.split(':')

                    for p_key, p_values in self._properties.items():
                        if d_key == p_values[0]:
                            p_values[1] = d_value  # Update property value

    # --- material --- get/set
    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, value):
        ex_msg = "Materials con ONLY be assigned during object creation."
        raise PartsException(ex_msg)

    pass  # END of CLASS


# --- Information ----------------------------------------------------
# --- Information class ---
class Information(object):
    """
    Show information obout the object and its sub-classes.
    """

    def __init__(self, obj):
        self.obj = obj

    # --- Methods --------------------------------------------------------

    @staticmethod
    def object_info(obj):
        """
        Extra info about the object.

        """
        obj_info = ""

        line_01 = '--- ' + obj.name + ' '
        for x in range(80-len(line_01)):
            line_01 += '-'

        line_02 = '* Visible on Room:  ' + obj.db.obj_lvis + '\n'
        line_03 = '* Mass:             ' + obj.db.obj_mass.mass + '\n'
        line_04 = '* Actual Gravity:   ' + obj.db.obj_mass.gravity + '\n'
        line_05 = '* Parts:            ' + obj.db.obj_parts.parts_amount() + '\n'
        for part in obj.db.obj_parts:
            line_05 += '                    ' + part.part_name + '\n'

        line_06 = '* Locks:            ' + str(bool(obj.db.obj_move)) + '\n'
        for key, value in obj.db.obj_move.items():
            line_06 += '                    ' + key + '\n'

        line_07 = '* Seats:            ' + obj.db.obj_seats.seats + '\n'

        line_08 = ''
        for x in range(80 - 19):
            line_08 += '-'
        line_08 += ' ' + obj.db.obj_guid + ' ---' + '\n'

        obj_info = line_01 + line_02 + line_03 + line_04 + line_05 + line_06 + line_07 + line_08

        return obj_info

    pass  # END of CLASS
