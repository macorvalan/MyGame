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
    * V Volumen: set the volume and shape of the object.
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
    Call of Cthulhu base Object class.

    """

    # --- Constructor ----------------------------------------------------------
    def at_object_creation(self):
        super(CoCObject, self).at_object_creation()

        self.db.obj_category = 'AAA-AAA-000000'
        self.db.obj_lvis = True

        self.db.obj_original = True
        self.db.obj_usable = True
        self.db.obj_sub_location = self.location

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

    Args:
        * set_obj: object to add locks.
        * set_locks: locks to add {'key': ['lock', 'message'], ...}

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
            add_locks: locks to add, in the format {'key': ['lock', 'message'], ...}

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
        Remove a lock from the object, if existed.

        Args:
            set_obj: object to remove lock
            rem_lock: key of the lock to remove (get, mov lift, etc)

        """
        if rem_lock in self._locks:
            set_obj.locks.remove(rem_lock)                                      # Remove the lock from the object
            del self._locks[rem_lock]                                           # Remove the lock from the Moveable object
        else:
            ex_msg = "The lock specified do not exist in the object"
            raise MovableException(ex_msg)

    pass  # END of CLASS


# --- VolumeException class ---
class VolumeException(Exception):
    """
    Base exception class raise by 'Volume' objects.

    Args:
        msg (str): informative error message.

    """

    # --- Constructor ----------------------------------------------------------
    def __init__(self, msg):
        self.msg = msg

    pass  # END of CLASS


# --- Volume class ---
class Volume(object):
    """
    Set the volume and the shape of the object.

    """

    # --- Constructor ----------------------------------------------------------
    def __init__(self, s_obj):
        self._vol_x = int(s_obj.split('x')[0])                                  # WIDTH
        self._vol_y = int(s_obj.split('x')[1])                                  # HEIGHT
        self._vol_z = int(s_obj.split('x')[2])                                  # DEEP

        self._volume = int(self._vol_x * self._vol_y * self._vol_z)
        self._shape = s_obj                                                     # X Y Z

    # --- Properties -----------------------------------------------------------
    # --- vol_x --- get/set
    @property
    def vol_x(self):
        return self._vol_x

    @vol_x.setter
    def vol_x(self, value):
        ex_msg = "The volume X can only be assigned at object creation."
        raise VolumeException(ex_msg)

    # --- vol_y --- get/set
    @property
    def vol_y(self):
        return self._vol_y

    @vol_y.setter
    def vol_y(self, value):
        ex_msg = "The volume Y can only be assigned at object creation."
        raise VolumeException(ex_msg)

    # --- vol_z --- get/set
    @property
    def vol_z(self):
        return self._vol_z

    @vol_z.setter
    def vol_z(self, value):
        ex_msg = "The volume Z can only be assigned at object creation."
        raise VolumeException(ex_msg)

    # --- volume --- get/set
    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        ex_msg = "The volume can only be assigned at object creation."
        raise VolumeException(ex_msg)

    # --- shape --- get/set
    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, value):
        ex_msg = "The shape can only be assigned at object creation."
        raise VolumeException(ex_msg)

    # --- Methods --------------------------------------------------------------

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

    For simplicity (for now) seats only check for capacity and not volume or size.

    """

    # --- Constructor ----------------------------------------------------------
    def __init__(self, seats):
        self._seats = {}

        for name, capacity in seats.items():
            self._seats[name] = Seat(name, capacity)

        self._total_mass = 0

    # --- Properties -----------------------------------------------------------
    # --- seats --- get/ser
    @property
    def seats(self):
        return self._seats

    @seats.setter
    def seats(self, value):
        ex_msg = "The seats can ONLY be modified at object creation"
        raise SeatsException(ex_msg)

    # --- total_mass --- get/ser
    @property
    def total_mass(self):
        return self._total_mass

    @total_mass.setter
    def total_mass(self, value):
        ex_msg = "The total mass of the seat can ONLY by calculated, not assigned."
        raise SeatsException(ex_msg)

    # --- Methods --------------------------------------------------------------

    def update_total_mass(self):
        """
        Update de mass of the seats.

        """

        temp_mass = 0
        for name, obj in self._seats:
            temp_mass += obj[name].seat_mass

        self._total_mass = temp_mass

    def at_enter_seat(self, s_name, s_obj):
        """
        Add the object to the seat selected seat, if there are space and the seat exist.

        Args:
            * s_name: seat name.
            * s_obj: object to put in the seat.

        """

        if s_name in self._seats:
            if self._seats[s_name].free_seats() > 0:
                self._seats[s_name].occupants = s_obj

                self.update_total_mass()
            else:
                ex_message = "Not enough free seats."
                raise SeatsException(ex_message)
        else:
            ex_message = "There is NOT seat with such name"
            raise SeatsException(ex_message)

    def at_leave_seat(self, s_name, s_obj):
        """
        Remove and object from the seat, if it is in the seats and the seat exist.

        Args:
            * s_name: seat name.
            * s_obj: object to remove from the seat

        """

        if s_name in self._seats:
            if  s_obj.name in self._seats[s_name]:
                self._seats[s_name].delete_occupant(s_obj.name)

                self.update_total_mass()
            else:
                ex_message = "There is NOT {} with such name in the {}.".format(s_obj.name, s_name)
                raise SeatsException(ex_message)
        else:
            ex_message = "There is NOT seat with such name"
            raise SeatsException(ex_message)

    def clear_seats(self, s_name):
        """
        Clear all the occupants and set the free seats to default value.

        Args:
            * s_name: seat name.
        """

        if s_name in self._seats:
            for key, value in self._seats.items():
                self._seats[key].clear_occupants()

            self.update_total_mass()
        else:
            ex_message = "There is NOT seat with such name"
            raise SeatsException(ex_message)

    def search_seats(self, s_name):
        """
        Search through all the seats of the object for a specified seat.

        Args:
            * s_name: seat name
        """

        if s_name in self._seats:
            return True
        else:
            return False

    def search_in_seats(self, s_name, o_name):
        """
        Search for a specified object in a specified seat.

        Args:
            * s_name: seat name.
            * o_name: object name to search.
        """

        if s_name in self._seats:
            if o_name in self._seats[s_name].occupants:
                return 'True:{} found {}'.format(o_name, s_name)
            else:
                return 'False:No such object.'
        else:
            return 'False:No such seat.'

    def access_seat(self, s_name):
        """
        Return the specified seat to access his data, using the access_seat_data
        method of the class Seats.

        Args:
                * s_name: seat name

        Return:
                * Seat (object)
                * None

        """

        if s_name in self._seats:
            return self._seats[s_name]
        else:
            return None

    def access_seat_data(self, s_name, s_data):
        """
        Access the specified seat data.

        Args:
                * s_name: seat name
                * s_data: seat data to retrieve (name, occupants, capacity, mass, free seats)

        Return:
                * Seat data (string/list/int)

        """

        s_seat = self.access_seat(s_name)
        if s_seat is not None:
            r_data = ''

            if s_data == 'name':
                r_data = s_seat.name
            elif s_data == 'occupants':
                r_data = s_seat.occupants
            elif s_data == 'capacity':
                r_data = s_seat.capacity
            elif s_data == 'mass':
                r_data = s_seat.seat_mass
            elif s_data == 'free seats':
                r_data = s_seat.free_seats()

            selected_property_value = r_data

            return selected_property_value
        else:
            ex_msg = "The seat specified do NOT exist."
            raise SeatsException(ex_msg)

    pass  # END of CLASS


# --- Seat class ---
class Seat(object):
    """
    Seat class to manage the seats' capacity, occupants, etc.

    """

    # --- Constructor ----------------------------------------------------------
    def __init__(self, name, capacity):
        self._name = name
        self._capacity = capacity
        self._occupants = {}

        self._seat_mass = 0

    # --- Properties -----------------------------------------------------------
    # --- name --- get/set
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        ex_msg = "The name of the Seat can ONLY be modified at object creation"
        raise SeatsException(ex_msg)

    # --- capacity --- get/set
    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        ex_msg = "The capacity of the Seat can ONLY be modified at object creation"
        raise SeatsException(ex_msg)

    # --- occupants --- get/set
    @property
    def occupants(self):
        return self._occupants

    @occupants.setter
    def occupants(self, value):
        self._occupants[value.name] = value

    # --- occupants --- get/set
    @property
    def seat_mass(self):
        return self._seat_mass

    @seat_mass.setter
    def seat_mass(self, value):
        ex_msg = "The total mass of the Seat can ONLY be modified with methods."
        raise SeatsException(ex_msg)

    # --- Methods --------------------------------------------------------------

    def free_seats(self):
        return self._capacity - len(self._occupants)

    def delete_occupant(self, occupant):
        del self._occupants[occupant]

        self.update_seat_mass()

    def clear_occupants(self):
        self._occupants.clear()

        self.update_seat_mass()

    def update_seat_mass(self):
        temp_mass = 0
        for key, value in self._occupants.items():
            temp_mass += value.db.obj_mass.mass

        self._seat_mass = temp_mass

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
        self._parts = {}
        self._total_mass = 0

        for key, value in parts.items():
            self._parts[key] = Part(key, value)

        self.update_total_mass()

    # --- Properties -----------------------------------------------------------
    # --- parts --- get/set
    @property
    def parts(self):
        return self._parts

    @parts.setter
    def parts(self, value):
        ex_msg = "Parts can only be assign at the object creation"
        raise PartsException(ex_msg)

    # --- total_mass --- get/set
    @property
    def total_mass(self):
        return self._total_mass

    @total_mass.setter
    def total_mass(self, value):
        ex_msg = "Total Mass can ONLY by calculated, not assigned."
        raise PartsException(ex_msg)

    # --- Methods --------------------------------------------------------------

    def parts_amount(self):
        """
        Return the amount of parts of the object.

        """

        return len(self._parts)

    def update_total_mass(self):
        """
        Update the total mass of the parts.

        """

        temp_mass = 0
        for p_name, p_obj in self._parts.items():
            temp_mass += p_obj.mass

        self._total_mass = temp_mass

    def search_part(self, p_name):
        """
        Search the specified part in the object.

        Args:
            * p_name: part name.

        Return:
                * True
                * False

        """

        if p_name in self._parts:
            return True
        else:
            return False

    def access_part(self, p_name):
        """
        Return the specified part to access his properties, using the access_part_property
        method of the class Parts.

        Args:
                * p_name: part name.
        Return:
                * Part (object) / None

        """

        if p_name in self._parts:
            return self._parts[p_name]
        else:
            return None

    def access_part_property(self, p_name, p_property):
        """
        Return the value of the part/property specified.

        Args:
                * p_name: part name.
                * p_property: part property to retrieve.

        Return:
                * property (int/float/string)

        """

        s_part = self.access_part(p_name)
        if s_part is not None:
            s_material = s_part.material
            s_property = s_material.get_property(p_property)

            selected_property_value = s_property

            return selected_property_value
        else:
            ex_msg = "The part specified do NOT exist."
            raise PartsException(ex_msg)

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
    def name(self):
        return self._part_name

    @name.setter
    def name(self, value):
        ex_msg = "Parts values can only be assigned during object creation. Can NOT be modified."
        raise PartsException(ex_msg)

    # --- part_material --- get/set
    @property
    def material(self):
        return self._part_material

    @material.setter
    def material(self, value):
        ex_msg = "Parts values can only be assigned during object creation. Can NOT be modified."
        raise PartsException(ex_msg)

    # --- part_amount --- get/set
    @property
    def amount(self):
        return self._part_amount

    @amount.setter
    def amount(self, value):
        ex_msg = "Parts values can only be assigned during object creation. Can NOT be modified."
        raise PartsException(ex_msg)

    # --- part_mass --- get/set
    @property
    def mass(self):
        return self._part_mass

    @mass.setter
    def mass(self, value):
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

        Args:
            * prop: property

        Return:
            * property value

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
        self._total_mass = 0

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

    # --- total_mass --- get/set
    @property
    def total_mass(self):
        return self._total_mass

    @total_mass.setter
    def total_mass(self, value):
        ex_msg = "The Total Mass of the stack is calculated when add/remove objects."
        raise StackableException(ex_msg)

    # --- Methods --------------------------------------------------------------

    def update_total_mass(self):
        """
        Update the total mass of the stack.

        """
        if self._actual_stack == 1:
            self._total_mass = 0
        else:
            temp_mass = 0
            for obj in range(self._actual_stack):
                temp_mass += self._obj_stack.db.obj_mass.mass

            self._total_mass = temp_mass

    def add_stack(self, obj):
        """
        Add the amount of stack of the selected object to the stack.

        Args:
            * obj: object to stack.

        Return: (string):
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
                    self.update_total_mass()

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

        Args:
            * stack: amount to remove from the stack.

        Return (string):
                        * 'True': Successfully remove the amount of the stack.
                        * 'False': Can't remove the amount of the stack, not enough objects in the stack.
        """

        a_stk = self._actual_stack
        r_stk = stack
        c_stk = self._obj_class

        if not ((a_stk - r_stk) < 1):
            self._actual_stack -= r_stk
            self.update_total_mass()

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

        self._actual_stack = 1
        self._total_mass = 0.0
        self._obj_stack = None

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
        self._slots = {}
        self._total_mass = 0

        for key, values in s_dict.items():
            self._slots[key] = Slot(key, values)

    # --- Properties -----------------------------------------------------------
    # --- obj_slots --- get/set
    @property
    def slots(self):
        return self._slots

    @slots.setter
    def slots(self, value):
        ex_msg = "The Slots can ONLY be set at object creation."
        raise SlotsException(ex_msg)

    # --- total_mass --- get/set
    @property
    def total_mass(self):
        return self._total_mass

    @total_mass.setter
    def total_mass(self, value):
        ex_msg = "The Total Mass can ONLY be calculated, not assigned."
        raise SlotsException(ex_msg)

    # --- Methods --------------------------------------------------------------

    def update_total_mass(self):
        """
        Update the total mass of the slots.

        """
        temp_mass = 0
        for name, slot in self._slots.items():
            temp_mass += slot.mass

        self._total_mass = temp_mass

    def has_slots(self):
        """
        Return if the object has slots for to use.

        """

        return bool(self._slots)

    def free_slots(self):
        """
        Return a list of strings of the slots with capacity >= 1.

        Return:
                slot_name:slot_actual_capacity:slot_actual_volume:slot_actual_mass (list)

        """
        temp_free = []

        for name, slot in self._slots.items():
            if slot.capacity >= 1:
                temp_free.append(slot.name + ':' + str(slot.capacity) + ':' + str(slot.volume) + ':' + str(slot.mass))
            else:
                pass

        return temp_free

    def used_slots(self):
        """
        Return a list of strings of the used slots of the object.

        Return:
                slot_name:slot_actual_capacity:slot_actual_volume:slot_actual_mass

        """
        temp_used = []

        for name, slot in self._slots.items():
            if slot.capacity == 0:
                temp_used.append(slot.name + ':' + str(slot.capacity) + ':' + str(slot.volume) + ':' + str(slot.mass))
            else:
                pass

        return temp_used

    def add_to_slot(self, s_name, obj):
        """
        Add an item to the selected Slot, checking if the slot exist and have capacity.

        Args:
                * s_name: slot name.
                * obj: object to add to the slot.

        Return:
                * True:Name of the slot used.
                * False:There is no slot by that name.
                * False:There is no enough capacity in the slot.
                * False:Not enough volume in the slot.
                * False:Object exceed the max volume of the slot.
                * False:Object exceed the max mass of the slot.
                * False:Object exceed the max capacity of the slot.

        """

        result = ''
        if s_name in self._slots:                                                               # check if the SLOT EXIST.
            s_mc = self._slots[s_name].max_volume
            s_mv = self._slots[s_name].max_capacity
            s_mm = self._slots[s_name].max_mass
            s_v = self._slots[s_name].volume
            s_c = self._slots[s_name].capacity
            s_m = self._slots[s_name].mass

            o_m = obj.db.obj_mass.mass
            o_v = obj.db.obj_volume.volume

            if s_c >= 1:                                                                            # check if the SLOT has CAPACITY for the item.
                if s_v >= obj.db.obj_volume.volume:                                                 # check if the SLOT has enough VOLUME to hold the item.
                    if not (o_v + s_v) > s_mv:                                                      # check if the object EXCEED slot VOLUME
                        if not (o_m + s_m) > s_mm:                                                  # check if the object EXCEED slot MASS
                            if not(s_c + 1) > s_mc:                                                 # check if the object EXCEED slot CAPACITY
                                self._slots[s_name].content = obj

                                self._slots[s_name].capacity -= 1
                                self._slots[s_name].volume += obj.db.obj_volume.volume
                                self._slots[s_name].mass += obj.db.obj_mass.mass

                                self.update_total_mass()

                                result = 'True:' + self._slots[s_name].name                         # ALL OK
                            else:
                                result = 'False:Object exceed the max capacity of the slot'
                        else:
                            result = 'False:Object exceed the max mass of the slot'
                    else:
                        result = 'False:Object exceed the max volume of the slot'
                else:
                    result = 'False:Not enough volume in the slot.'
            else:
                result = 'False:There is no enough capacity in the slot.'
        else:
            result = 'False:There is not slot by that name.'

        return result

    def remove_from_slot(self, s_name, s_obj, new_location):
        """
        Remove an item from the slot, checking if the slot/item exists.

        Args:
                * s_name: slot name.
                * s_obj: object to remove from the slot
                * new_location: new location of the object

        Return:
                * True
                * False:There is no slot by that name.
                * False:There is no object by that name in the slot.

        """

        result = ''
        if s_name in self._slots:                                                               # check if the SLOT EXIST.
            slot = self._slots[s_name].content
            for obj in slot:                                                                        # iterate through the OBJECTS in the slot.
                if obj.name == s_obj.name:                                                          # if FIND the object.
                    oi = slot.index(obj)

                    del slot[oi]

                    self.update_total_mass()

                    result = 'True:' + new_location                                                 # ALL OK
                else:
                    result = 'False:There is not object by that name in the slot.'
        else:
            result = 'False:There is not slot by that name.'

        return result

    def search_slots(self):
        """
        Return a list with all the name of the slots in the object and its max capacity

        Return:
                * slot_name:max_capacity

        """

        temp_slots = []
        for name, slot in self._slots.items():
            temp_slots.append(name + ':' + str(slot.max_capacity))

        return temp_slots

    def search_slot(self, s_name):
        """
        Return True or False if the slot exist.

        Args:
                * s_name: slot name.

        Return
                * True
                * False

        """

        if s_name in self._slots:
            return True
        else:
            return False

    def access_slot(self, s_name):
        """
        Return the specified slot.

        Args:
                * s_name: slot name.

        Return
                * Slot (object)
                * None

        """

        if s_name in self._slots:
            return self._slots[s_name]
        else:
            return None

    def access_slot_data(self, s_name, s_data):
        """
        Return the slot/data specified.

        Args:
                * s_name: name of the slot
                * s_data: data to return (max capacity, max mass, max volume, capacity, mass, volume, content)

        Returns:
                 * data

        """

        if self.access_slot(s_name):
            data = ''
            if s_data == 'max capacity':
                data = self.access_slot(s_name).max_capacity
            elif s_data == 'max mass':
                data = self.access_slot(s_name).max_mass
            elif s_data == 'max volume':
                data = self.access_slot(s_name).max_volume
            elif s_data == 'capacity':
                data = self.access_slot(s_name).capacity
            elif s_data == 'mass':
                data = self.access_slot(s_name).mass
            elif s_data == 'volume':
                data = self.access_slot(s_name).volume
            elif s_data == 'content':
                data = self.access_slot(s_name).content

            return data
        else:
            return 'None'

    pass  # END of CLASS


# --- Slot class ---
class Slot(object):
    """
    Class Slot containing the object attached.

    """

    # --- Constructor ----------------------------------------------------------
    def __init__(self, s_name, s_attr):
        self._slot_name = s_name
        self._slot_max_capacity = s_attr[0]
        self._slot_max_volume = s_attr[1]
        self._slot_max_mass = s_attr[2]

        self._slot_obj = []
        self._slot_capacity = s_attr[0]
        self._slot_volume = 0.0
        self._slot_mass = 0

    # --- Properties -----------------------------------------------------------
    # --- slot_name --- get/set
    @property
    def name(self):
        return self._slot_name

    @name.setter
    def name(self, value):
        ex_msg = "The Slot name can ONLY be set at object creation."
        raise SlotsException(ex_msg)

    # --- slot_max_capacity --- get/set
    @property
    def max_capacity(self):
        return self._slot_max_capacity

    @max_capacity.setter
    def max_capacity(self, value):
        ex_msg = "The Slot max capacity can ONLY be set at object creation."
        raise SlotsException(ex_msg)

    # --- slot_max_volume --- get/set
    @property
    def max_volume(self):
        return self._slot_max_volume

    @max_volume.setter
    def max_volume(self, value):
        ex_msg = "The Slot max volume can ONLY be set at object creation."
        raise SlotsException(ex_msg)

    # --- max_mass --- get/set
    @property
    def max_mass(self):
        return self._slot_max_mass

    @max_mass.setter
    def max_mass(self, value):
        ex_msg = "The Slot max mass can ONLY be set at object creation."
        raise SlotsException(ex_msg)

    # --- slot_obj --- get/set
    @property
    def content(self):
        return self._slot_obj

    @content.setter
    def content(self, value):
        self._slot_obj.append(value)

    # --- slot_capacity --- get/set
    @property
    def capacity(self):
        return self._slot_capacity

    @capacity.setter
    def capacity(self, value):
        self._slot_capacity = value

    # --- slot_volume --- get/set
    @property
    def volume(self):
        return self._slot_volume

    @volume.setter
    def volume(self, value):
        self._slot_volume = value

    # --- slot_mass --- get/set
    @property
    def mass(self):
        return self._slot_mass

    @mass.setter
    def mass(self, value):
        self._slot_mass = value

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
    Container class to set if the object con store other objects and to manage the size and volume
    of the container (capacity).

    """

    # --- Constructor ----------------------------------------------------------
    def __init__(self, container=False, max_capacity=0, max_volume=0, max_mass=0, is_open=False, lock_type='None'):
        self._is_container = container
        self._content = []

        self._lock = Lock(lock_type)

        self._max_capacity = max_capacity
        self._max_volume = max_volume
        self._max_mass = max_mass

        self._capacity = 0
        self._volume = 0
        self._total_mass = 0

        self._is_open = is_open

    # --- Properties -----------------------------------------------------------
    # --- obj_slots --- get/set
    @property
    def total_mass(self):
        return self._total_mass

    @total_mass.setter
    def total_mass(self, value):
        ex_msg = "The Total Mass can ONLY be calculated, not assigned."
        raise ContainerException(ex_msg)

    # --- Methods --------------------------------------------------------------

    def update_total_mass(self):
        """
        Update the total mass of the container.

        """

        temp_mass = 0
        for obj in self._content:
            temp_mass += obj.db.obj_mass.mass

        self._total_mass = temp_mass

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

        Args:
                * obj: object containing the information.

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
