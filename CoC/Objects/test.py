# -*- coding: utf-8 -*-
"""
Testing suit for CoC Objects

"""
from evennia.commands.default.tests import CommandTest
from evennia.utils.test_resources import EvenniaTest
from evennia import create_object
from evennia.objects.objects import DefaultRoom

import CoC.CoC_Rooms
from CoC.Objects.CoC_Furmitures import Chair
from CoC.Objects.CoC_Objects import CoCObject


class TestFurniture(EvenniaTest):

    def test_cocobject_obj_guid(self):
        """
        Test Class 01
        Test Inheritance from CoCObject class.
                * [obj.category]

        """

        room = create_object(CoC.CoC_Rooms.CoCRoom, key='A room with gravity')
        test_silla = create_object(Chair, key='Old chair', location=room)

        self.assertEqual("FNT-CHR-000001", test_silla.db.obj_category, "Testing CoCObject obj_category attribute.")

    def test_cocobject_obj_lvis(self):
        """
        Test Class 02
        Test Inheritance from CoCObject class.
                * [obj.lvis]

        """
        room = create_object(CoC.CoC_Rooms.CoCRoom, key='A room with gravity')
        test_silla = create_object(Chair, key='Old chair', location=room)

        self.assertEqual(True, test_silla.db.obj_lvis, "Testing CoCObject obj_lvis attribute")

    def test_cocobject_obj_sublocation(self):
        """
        Test Class 03
        Test Inheritance from CoCObject class.
                * [obj.sub_location]

        """
        room = create_object(CoC.CoC_Rooms.CoCRoom, key='A room with gravity')
        test_silla = create_object(Chair, key='Old chair', location=room)

        self.assertEqual(room, test_silla.db.obj_sub_location, "Testing CoCObject obj_sub_location attribute")

    def test_chair_mass(self):
        """
        Test Class 04
        Test the Mass class of the object
                * [mass]
                * [gravity]
                * [weight]
                * [chair base location]
                * [room gravity]
                * [weight mg]
                * [weight gr]
                * [weight kg]
                * [weight tn]

        """
        room = create_object(CoC.CoC_Rooms.CoCRoom, key='A room with gravity')
        test_caja = create_object(CoCObject, key='Caja Grande', location=room)
        test_silla = create_object(Chair, key='Old chair', location=test_caja)

        self.assertEqual(3028.800000, test_silla.db.obj_mass.mass, "Testing chair mass attribute.")
        self.assertEqual(1.000000, test_silla.db.obj_mass.gravity, "Testing chair gravity attribute.")
        self.assertEqual(3028.800000, test_silla.db.obj_mass.weight, "Testing chair weight attribute.")

        self.assertEqual(room, test_silla.get_room_location(), "Testing Chair location")

        self.assertEqual(room.db.gravity, test_silla.db.obj_mass.gravity, "Testing Chair gravity.")

        self.assertEqual(3028800.000000, test_silla.db.obj_mass.weight_mg(), "Testing Chair weight attribute in milligrams.")
        self.assertEqual(3028.800000, test_silla.db.obj_mass.weight_gr(), "Testing Chair weight attribute in grams.")
        self.assertEqual(3.028800, test_silla.db.obj_mass.weight_kg(), "Testing Chair weight attribute in kilograms.")
        self.assertEqual(0.003029, test_silla.db.obj_mass.weight_tn(), "Testing Chair weight attribute in Tons.")

    def test_chair_seats(self):
        """
        Test Class 05
        Test the Seats class of the object.
                * [Seats]
                * [free seats]

        """
        room = create_object(CoC.CoC_Rooms.CoCRoom, key='A room with gravity')
        test_silla = create_object(Chair, key='Old chair', location=room)

        self.assertEqual(1, test_silla.db.obj_seats, "Testing Chair seats attribute.")
        self.assertEqual(1, test_silla.db.obj_seats.free_seats(), "Testing Chair free seats attribute.")

    def test_chair_copy(self):
        """
        Test Class 06
        Test if the copy_object command copy all attributes.
                * [part name]

        """

        room = create_object(CoC.CoC_Rooms.CoCRoom, key='A room with gravity')
        test_silla = create_object(Chair, key='Old chair', location=room)
        test_silla2 = test_silla.copy()

        parts = test_silla2.db.obj_parts
        del test_silla

        self.assertEqual('Old chair body', parts.parts[0].part_name, "Testing Chair parts name attribute on copy.")

    def test_chair_stack(self):
        """
        Test Class 07
        Test  the Seats of the chair.
                * [can_stack]
                * [max_stack]
                * [actual_stack]
                * [mass_stack]

        """

        room = create_object(CoC.CoC_Rooms.CoCRoom, key='A room with gravity')
        test_silla1 = create_object(Chair, key='Old chair', location=room)
        test_silla2 = create_object(Chair, key='Old chair', location=room)

        self.assertEqual(True, test_silla1.db.obj_stack.can_stack, "Testing if the Chair can stack.")
        self.assertEqual(3, test_silla1.db.obj_stack.max_stack, "Testing if the Chair max stack.")
        self.assertEqual(1, test_silla1.db.obj_stack.actual_stack, "Testing if the Chair actual stack.")
        self.assertEqual(0.0, test_silla1.db.obj_stack.mass_stack, "Testing if the Chair mass stack.")

        stacked = test_silla1.db.obj_stack.add_stack(test_silla2)
        self.assertEqual('True', stacked, "Testing if the Chair stacked successfully.")

        self.assertEqual(True, test_silla1.db.obj_stack.can_stack, "Testing if the Chair can stack.")
        self.assertEqual(3, test_silla1.db.obj_stack.max_stack, "Testing if the Chair max stack.")
        self.assertEqual(2, test_silla1.db.obj_stack.actual_stack, "Testing if the Chair actual stack.")
        self.assertEqual(test_silla1.db.obj_mass.mass + test_silla2.db.obj_mass.mass, test_silla1.db.obj_stack.mass_stack,
                         "Testing if the Chair mass stack.")

        s_response, s_class = test_silla1.db.obj_stack.remove_stack(1)
        self.assertEqual(True, s_response, "Testing if the Chair response unstacked successfully.")
        self.assertEqual(Chair, s_class, "Testing if the Chair class unstacked successfully.")

        self.assertEqual(True, test_silla1.db.obj_stack.can_stack, "Testing if the Chair can stack.")
        self.assertEqual(3, test_silla1.db.obj_stack.max_stack, "Testing if the Chair max stack.")
        self.assertEqual(1, test_silla1.db.obj_stack.actual_stack, "Testing if the Chair actual stack.")
        self.assertEqual(0.0, test_silla1.db.obj_stack.mass_stack, "Testing if the Chair mass stack.")

    def test_chair_slots(self):
        """
        Test Class 08
        Test the Slots of the object

        """

        room = create_object(CoC.CoC_Rooms.CoCRoom, key='A room with gravity')
        test_silla1 = create_object(Chair, key='Old chair', location=room)

        self.assertEqual(True, test_silla1.db.obj_slots.has_slots(), "Testing the slots of the Chair.")

        s_free = test_silla1.db.obj_slots.free_slots()
        s_used = test_silla1.db.obj_slots.used_slots()
        self.assertEqual(True, bool(s_free), "Testing the free slots of the Chair.")
        self.assertEqual(False, bool(s_used), "Testing the used slots of the Chair.")



    pass  # END of CLASS
