"""
Call of Cthulhu base Object class/base exception/sub-classes

Base object class for every object in the game, it adds the following:

    * obj_category attribute: unique identificator.
    * obj_lvis attribute: makes tho object visible or not when use the look command in a room.


Sub-classes adding attributes to the objects.

    * L Movable: set the move properties of the object.                                             Ok
    * U Unbreakable: set if the object can be destroyed.
    * C Containers: set if the object is a container and the amount/capacity of its containers.
    * M Mass: set the weight of the object based on mass and gravity.                               Ok
    * S Seats: set the amount od seats the object has.                                              Ok
    * P Parts: set the parts of an object.                                                          Ok
    * T Materials: set the materials of the object (parts), dictionary(material_name, %).           Ok
    * A Assembly:
    * D Disassemble:
    * O Slots: set the amount of slots of the object.                                               Ok
    * E Mechanism:
    * K Stackable: set if the object can be stacked and the max amount.                             Ok
    * Information: show extra information about the object                                          In progress

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

    # --- Constructor ----------------------------------------------------------
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

        self.db.obj_category = 'AAA-AAA-000000'
        self.db.obj_lvis = True

        self.db.obj_original = True
        self.db.obj_usable = True

    # --- Hooks ----------------------------------------------------------------
    def return_appearance(self, looker):
        text = super().return_appearance(looker)

        return text

    # --- Methods --------------------------------------------------------------

    def get_room_location(self):
        """
        Get the room where the object is, iterate throw containers to get a room.

        """

        loc = self.location
        while loc.location is not None:
            loc = loc.location

        return loc

    pass  # END of CLASS


# --- Sub-Classes ------------------------------------------------------------------------------------------------------------------------------------

# --- Movable ------------------------------------------------------------------
# --- MovableException class ---
class MovableException(Exception):
    """
    Base exception class raise by 'Seats' objects.

    Args:
        msg (str): informative error message.
    """

    # --- Constructor ----------------------------------------------------------
    def __init__(self, msg):
        self.msg = msg

    pass  # END of CLASS


# --- Movable class ---
class Movable(object):
    """
    Set the move properties of the object.
    """

    # --- Constructor ----------------------------------------------------------
    def __init__(self, set_obj, set_locks):
        self._locks = dict(set_locks)

        for key, value in set_locks.items():
            temp_lock = key + ':' + value[0]
            set_obj.locks.add(temp_lock)

            if key == 'get':
                set_obj.db.get_err_msg = value[1]
            elif key == 'mov':  # TODO: Implement move command ---
                pass

    # --- Properties -----------------------------------------------------------
    # --- locks --- get/set
    @property
    def locks(self):
        return self._locks

    @locks.setter
    def locks(self, value):
        ex_msg = "Locks can be be assigned at object creation, or with the 'add' method."
        raise MovableException(ex_msg)

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
                temp_lock = key + ':' + value[0]  #
                set_obj.locks.add(temp_lock)  #
                #
                if key == 'get':  #
                    set_obj.db.get_err_msg = value[1]  #
                elif key == 'mov':  # Add the lock to the object
                    pass  #

                self._locks[key] = value  # Add the lock to the Moveable object
                pass
            else:
                ex_msg = "The lock specified is already present in the object, remove it first, than add the new lock"
                raise MovableException(ex_msg)

    def remove(self, set_obj, rem_lock):
        """
        Remove a lock from the object, if exist.

        Args:
            set_obj: object to remove lock
            rem_lock: key of the lock to remove (get, mov lift, etc)
        """
        if rem_lock in self._locks:
            set_obj.locks.remove(rem_lock)  # Remove the lock from the object
            del self._locks[rem_lock]  # Remove the lock from the Moveable object
        else:
            ex_msg = "The lock specified do not exist in the object"
            raise MovableException(ex_msg)

    pass  # END of CLASS


# --- Mass ---------------------------------------------------------------------
# --- MassException class ---
class MassException(Exception):
    """
    Base exception class raise by 'Mass' objects.

    Args:
        msg (str): informative error message.
    """

    # --- Constructor ----------------------------------------------------------
    def __init__(self, msg):
        self.msg = msg

    pass  # END of CLASS


# --- Mass class ---
class Mass(object):
    """
    Sub-class Mass to manage the weight of an object, it is based on mass and gravity.

    The mass is expressed in grams.
    """

    # --- Constructor ----------------------------------------------------------
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

    # --- Constructor ----------------------------------------------------------
    def __init__(self, msg):
        self.msg = msg

    pass  # END of CLASS


# --- Seats class ---
class Seats(object):
    """
    Add seats to the object, and the necessary methods to manage the seats.
    """

    # --- Constructor ----------------------------------------------------------
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


# --- Parts --------------------------------------------------------------------
# --- PartsException class ---
class PartsException(Exception):
    """
    Base exception class raise by 'Parts' objects.

    Args:
        msg (str): informative error message.
    """

    # --- Constructor ----------------------------------------------------------
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

    # --- Properties -----------------------------------------------------------
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


# --- Part class ---------------------------------------------------------------
class Part(object):
    """
    Set every part in the list of parts with material properties.

    Args:
        {'part name': ['material', amount, unitary weight]}
    """

    # --- Constructor ----------------------------------------------------------
    def __init__(self, key, value):
        self._part_name = key
        self._part_material = Materials(value[0])
        self._part_amount = value[1]
        self._part_mass = value[2]

    # --- Properties -----------------------------------------------------------
    # --- part_name --- get/set
    @property
    def part_name(self):
        return self._part_name

    @part_name.setter
    def part_name(self, value):
        ex_msg = "Parts values can only be assigned during object creation. Can NOT be modified."
        raise PartsException(ex_msg)

    # --- part_material --- get/set
    @property
    def part_material(self):
        return self._part_material

    @part_material.setter
    def part_material(self, value):
        ex_msg = "Parts values can only be assigned during object creation. Can NOT be modified."
        raise PartsException(ex_msg)

    # --- part_amount --- get/set
    @property
    def part_amount(self):
        return self._part_amount

    @part_amount.setter
    def part_amount(self, value):
        ex_msg = "Parts values can only be assigned during object creation. Can NOT be modified."
        raise PartsException(ex_msg)

    # --- part_mass --- get/set
    @property
    def part_mass(self):
        return self._part_mass

    @part_mass.setter
    def part_mass(self, value):
        ex_msg = "Parts values can only be assigned during object creation. Can NOT be modified."
        raise PartsException(ex_msg)

    pass  # END of CLASS


# --- Materials ----------------------------------------------------------------
# --- MaterialsException class ---
class MaterialsException(Exception):
    """
    Base exception class raise by 'Materials' objects.

    Args:
        msg (str): informative error message.
    """

    # --- Constructor ----------------------------------------------------------
    def __init__(self, msg):
        self.msg = msg

    pass  # END of CLASS


# --- Materials class ---
class Materials(object):
    """
    Set the materials witch the object is made.
    """

    # --- Constructor ----------------------------------------------------------
    def __init__(self, material):
        self._material = material
        self._properties = dict(PROPERTIES_DICT)

        for MPD_key, MPD_values in MATERIALS_PROPERTIES_DICT.items():           # Iter through materials DICT
            if self._material == MPD_key:                                       # If material is found
                for MPD_value in MPD_values:                                    # Iter through properties and update
                    d_key, d_value = MPD_value.split(':')

                    for p_key, p_values in self._properties.items():
                        if d_key == p_values[0]:
                            p_values[1] = d_value                               # Update property value

    # --- material --- get/set
    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, value):
        ex_msg = "Materials can ONLY be assigned during object creation."
        raise MaterialsException(ex_msg)

    # --- properties --- get/set
    @property
    def properties(self):
        return self._properties

    @properties.setter
    def properties(self, value):
        ex_msg = "Material's properties can ONLY be assigned during object creation."
        raise MaterialsException(ex_msg)

    # --- Methods --------------------------------------------------------------

    def get_property(self, prop):
        """
        Get the value of the property passed as argument.

        """
        return self._properties[prop][1]

    pass  # END of CLASS


# --- Stackable ----------------------------------------------------------------
# --- StackableException class ---
class StackableException(Exception):
    """
    Base exception class raise by 'Stackable' objects.

    Args:
        msg (str): informative error message.
    """

    # --- Constructor ----------------------------------------------------------
    def __init__(self, msg):
        self.msg = msg

    pass  # END of CLASS


# --- Stackable class ---
class Stackable(object):
    """
    Set if the object is stackable, and the max amount of the stack.

    For simplicity stacking, affect the weight but not affect the volume or size.
    * for now... *

    Stackable class DO NOT store created objects, it stores only ONE created object (for easy access),
    that's why the objects to stack must be of the same class, have the same attributes and name.

    In theory all the objects instantiates/created from the same class are equal, but the moment
    the player, upgrade/partially disassemble/modify the object, it becomes a different object
    of the same class.

    When stacked object, only one created-object is store and the stack counter in the class Stackable
    is increase, and the rest of the objects MUST be DELETED (outside this class).
    When un-stack items the items remove from the stack must be created with the tool Deserialize,
    and the class Stackable counter is decreased.

    For simplicity all the changes made to the object are store in one attribute:
        . obj_original (bool)

    """

    # --- Constructor ----------------------------------------------------------
    def __init__(self, obj_class, can_stack, max_stack):
        self._obj_class = obj_class
        self._obj_stack = None
        self._can_stack = can_stack
        self._max_stack = max_stack
        self._actual_stack = 1
        self._mass_stack = 0.0

    # --- Properties -----------------------------------------------------------
    # --- obj_class --- get/set
    @property
    def obj_class(self):
        return self._obj_class

    @obj_class.setter
    def obj_class(self, value):
        ex_msg = "The class of object CAN NOT be change EVER."
        raise StackableException(ex_msg)

    # --- obj_stack --- get/set
    @property
    def obj_stack(self):
        if self._obj_stack is None:
            return None
        else:
            return self._obj_stack

    @obj_stack.setter
    def obj_stack(self, value):
        ex_msg = "The object CAN NOT be change EVER."
        raise StackableException(ex_msg)

    # --- can_stack --- get/set
    @property
    def can_stack(self):
        return self._can_stack

    @can_stack.setter
    def can_stack(self, value):
        ex_msg = "Stack can ONLY be assigned during object creation."
        raise StackableException(ex_msg)

    # --- max_stack --- get/set
    @property
    def max_stack(self):
        return self._max_stack

    @max_stack.setter
    def max_stack(self, value):
        ex_msg = "Maximum amount of stack objects can ONLY be assigned during object creation."
        raise StackableException(ex_msg)

    # --- actual_stack --- get/set
    @property
    def actual_stack(self):
        return self._actual_stack

    @actual_stack.setter
    def actual_stack(self, value):
        ex_msg = "The actual stack space is calculated when add/remove objects."
        raise StackableException(ex_msg)

    # --- mass_stack --- get/set
    @property
    def mass_stack(self):
        return self._mass_stack

    @mass_stack.setter
    def mass_stack(self, value):
        ex_msg = "The total mass of the stack is calculated when add/remove objects."
        raise StackableException(ex_msg)

    # --- Methods --------------------------------------------------------------

    def update_stack(self):
        """
        Update the mass of the tack.

        """
        if self._actual_stack == 1:
            self._mass_stack = 0.0
        else:
            temp_mass = 0.0
            for obj in range(self._actual_stack):
                temp_mass += self._obj_stack.db.obj_mass.mass

            self._mass_stack = temp_mass

    def add_stack(self, obj):
        """
        Add the amount of stack of the selected object to the stack.

        Return (string):
                            * 'True': Stack added successfully.
                            * 'Max': Can't add the object to the stack, max reached.
                            * 'Mod': Can't add the object because are different.
                            * 'Dif': Can' stack, different objects.

        """

        if type(obj) == self._obj_class:
            if not obj.db.obj_modified:
                a_stk = self._actual_stack
                o_stk = obj.db.obj_stack.actual_stack

                if not ((a_stk + o_stk) > self._max_stack):
                    self._obj_stack = obj
                    self._actual_stack += obj.db.obj_stack.actual_stack
                    self.update_stack()

                    response = 'True'
                else:
                    response = 'Max'
            else:
                response = 'Mod'
        else:
            response = 'dif'

        return response

    def remove_stack(self, stack):
        """
        Remove the amount selected from the stack.

        Return (string):
                        * 'True': Successfully remove the amount of the stack.
                        * 'False': Can't remove the amount of the stack, not enough objects in the stack.
        """

        a_stk = self._actual_stack
        r_stk = stack
        c_stk = self._obj_class

        if not ((a_stk - r_stk) < 1):
            self._actual_stack -= r_stk
            self.update_stack()

            response = True

            return response, c_stk
        else:
            response = False

            return response, None

    def clear_stack(self):
        """
        Clear the stack, reset it to default values.

        all the objects are lost!

        """

        self._actual_stack = 0                                                  # super easy!

    pass  # END of CLASS


# --- Slots ------------------------------------------------------------------
# --- SlotsException class ---
class SlotsException(Exception):
    """
    Base exception class raise by 'Slots' objects.

    Args:
        msg (str): informative error message.
    """

    # --- Constructor ----------------------------------------------------------
    def __init__(self, msg):
        self.msg = msg

    pass  # END of CLASS


# --- Slots class ---
class Slots(object):
    """
    Set if the object has slots to attach other objects.
    
    The attached objects are inside the object with slots (.location), the use of slots its
    to expand the capacity of the object of carrying thing, and adding a realistic way
    to store the objects bases in the size, volume and anchor points.
    
    The class Slots keep a list of all the objects inside the slotted-object that are
    theoretically attached to the slots, so it can be access (only look), to manipulate
    the object must be taken it from the slot.

    Args:
        s_dict (dictionary) {'slot_name': [capacity(int, mass(float), volume(integer)]}

    """

    # --- Constructor ----------------------------------------------------------
    def __init__(self, s_dict):
        self._obj_slots = []

        for key, values in s_dict.items():
            self._obj_slots.append(Slot(key, values))

    # --- Properties -----------------------------------------------------------
    # --- obj_slots --- get/set
    @property
    def obj_slots(self):
        return self._obj_slots

    @obj_slots.setter
    def obj_slots(self, value):
        ex_msg = "The Slots can ONLY be set at object creation."
        raise SlotsException(ex_msg)

    # --- Methods --------------------------------------------------------------

    def has_slots(self):
        """
        Return if the object has slots for to use.

        """

        return bool(self._obj_slots)

    def free_slots(self):
        """
        Return a list with the name of the free slots of the object.

        """
        temp_free = []

        for slot in self._obj_slots:
            if slot.free:
                temp_free.append(slot.name)
            else:
                pass

        return temp_free

    def used_slots(self):
        """
        Return a list with the name of the used slots of the object.

        """
        temp_used = []

        for slot in self._obj_slots:
            if not slot.free:
                temp_used.append(slot.name)
            else:
                pass

        return temp_used

    def add_to_slot(self, s_name, obj):
        """
        Add an item to the selected Slot, checking if the slot exist and have capacity.

        """
        pass

    def remove_from_slot(self, s_name, obj):
        """
        Remove an item from the slot, checking if the slot/item exists.

        """
        pass

    pass  # END of CLASS


# --- Slot class ---
class Slot(object):
    """
    Class Slot containing the object attached.

    """

    # --- Constructor ----------------------------------------------------------
    def __init__(self, s_name, s_attr):
        self._slot_name = s_name
        self._slot_capacity = s_attr[0]
        self._slot_max_volume = s_attr[1]
        self._slot_mass = s_attr[2]

        self._slot_obj = []
        self._slot_fre = True
        self._slot_volume = 0.0

    # --- Properties -----------------------------------------------------------

    @property
    def name(self):
        """
        Return the name of the slot.

        """

        return self._slot_name

    @property
    def capacity(self):
        """
        Return the capacity of the slot.

        """

        return self._slot_capacity

    @property
    def max_volume(self):
        """
        Return the max volume of the slot.

        """

        return self._slot_max_volume

    @property
    def content(self):
        """
        Return a list with the objects attached to the slot.

        """

        return self._slot_obj

    @property
    def free(self):
        """
        Return if the slot is free or not.

        """
        return self._slot_fre

    @property
    def volume(self):
        """
        Return the actual volume of the slot.

        """

        return self._slot_volume

    # --- Methods --------------------------------------------------------------

    pass  # END of CLASS


# --- Container ------------------------------------------------------------------
# --- ContainerException class ---
class ContainerException(Exception):
    """
    Base exception class raise by 'Container' objects.

    Args:
        msg (str): informative error message.
    """

    # --- Constructor ----------------------------------------------------------
    def __init__(self, msg):
        self.msg = msg

    pass  # END of CLASS


# --- Container class ---
class Container(object):
    """
    Container class to set if the object coa store other objects and to manage the size and volume
    of the container (capacity).

    """

    # --- Constructor ----------------------------------------------------------
    def __init__(self, container=False, max_capacity=0, max_volume=0, lock_type='None'):
        self._is_container = container
        self._max_capacity = max_capacity
        self._max_volume = max_volume
        self._lock = Lock(lock_type)
        self._content_mass = 0.0

    pass  # END of CLASS


# --- Lock class ---
class Lock(object):

    # --- Constructor ----------------------------------------------------------
    def __init__(self, lock_type):
        pass

    pass  # END of CLASS


# --- Information --------------------------------------------------------------
# --- InformationException class ---
class InformationException(Exception):
    """
    Base exception class raise by 'Information' objects.

    Args:
        msg (str): informative error message.
    """

    # --- Constructor ----------------------------------------------------------
    def __init__(self, msg):
        self.msg = msg

    pass  # END of CLASS


# --- Information class ---
class Information(object):
    """
    Show information obout the object and its sub-classes.
    """

    # --- Constructor ----------------------------------------------------------
    def __init__(self):
        pass

    # --- Properties -----------------------------------------------------------

    # --- Methods --------------------------------------------------------------

    def update(self, obj):
        """
        Extra info about the object.

        """

        line_01 = '--- ' + obj.name + ' '
        for x in range(80 - len(line_01)):
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
        line_08 += ' ' + obj.db.obj_category + ' ---' + '\n'

        temp_info = line_01 + line_02 + line_03 + line_04 + line_05 + line_06 + line_07 + line_08

        return temp_info
