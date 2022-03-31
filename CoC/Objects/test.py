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


class TestFurniture(EvenniaTest):

    def test_cocobject_obj_guid(self):
        room = create_object(CoC.CoC_Rooms.CoCRoom, key='A room with gravity')
        test_silla = create_object(Chair, key='Old chair', location=room)

        self.assertEqual("FNT-CHR-000001", test_silla.db.obj_guid, "Testing CoCObject obj_guid attribute.")

    pass  # END of CLASS

    def test_cocobject_obj_lvis(self):
        room = create_object(CoC.CoC_Rooms.CoCRoom, key='A room with gravity')
        test_silla = create_object(Chair, key='Old chair', location=room)

        self.assertEqual(True, test_silla.db.obj_lvis, "Testing CoCObject obj_lvis attribute")

    pass  # END of CLASS

    def test_chair_mass(self):
        room = create_object(CoC.CoC_Rooms.CoCRoom, key='A room with gravity')
        test_silla = create_object(Chair, key='Old chair', location=room)

        self.assertEqual(3028.800000, test_silla.db.obj_mass.mass, "Testing chair mass attribute.")
        self.assertEqual(1.000000, test_silla.db.obj_mass.gravity, "Testing chair gravity attribute.")
        self.assertEqual(3028.800000, test_silla.db.obj_mass.weight, "Testing chair weight attribute.")

        self.assertEqual(room, test_silla.location, "Testing Chair location")

        self.assertEqual(room.db.gravity, test_silla.db.obj_mass.gravity, "Testing Chair gravity.")

        self.assertEqual(3028800.000000, test_silla.db.obj_mass.weight_mg(), "Testing Chair weight attribute in milligrams.")
        self.assertEqual(3028.800000, test_silla.db.obj_mass.weight_gr(), "Testing Chair weight attribute in grams.")
        self.assertEqual(3.028800, test_silla.db.obj_mass.weight_kg(), "Testing Chair weight attribute in kilograms.")
        self.assertEqual(0.003029, test_silla.db.obj_mass.weight_tn(), "Testing Chair weight attribute in Tons.")

    pass  # END of CLASS

    def test_chair_seats(self):
        room = create_object(CoC.CoC_Rooms.CoCRoom, key='A room with gravity')
        test_silla = create_object(Chair, key='Old chair', location=room)

        self.assertEqual(1, test_silla.db.obj_seats.seats, "Testing Chair seats attribute.")
        self.assertEqual(1, test_silla.db.obj_seats.free_seats, "Testing Chair free seats attribute.")

    pass  # END of CLASS

    def test_chair_parts(self):
        room = create_object(CoC.CoC_Rooms.CoCRoom, key='A room with gravity')
        test_silla = create_object(Chair, key='Old chair', location=room)

        parts = test_silla.db.obj_parts
        self.assertEqual('Old chair body', parts.parts[0].part_name, "Testing Chair parts name attribute in milligrams.")
        #self.assertEqual(1, test_silla.db.obj_parts, "Testing Chair weight attribute in milligrams.")

    pass  # END of CLASS