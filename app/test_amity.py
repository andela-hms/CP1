import unittest
import sys
sys.path.insert(0, '/Users/hms/Projects/cp1/app')
import os
from amity import Amity
from rooms.rooms import Office, LivingSpace

class TestAmity(unittest.TestCase):
    """ Test amity """
    def setUp(self):
        self.amity = Amity()
        self.offices = self.amity.offices
        self.living_spaces = self.amity.living_spaces
        self.fellows = self.amity.fellows
        self.staff = self.amity.staff
        self.new_offices = self.amity.create_room("O", "Occulus", "Narnia")
        self.new_living_space = self.amity.create_room("L", 'mombasa')
        self.new_fellow = self.amity.add_person("hum", "musonye", "fellow", "Y")
        self.new_staff = self.amity.add_person("hum", "musonye", "staff", "N")
        self.unallocated_fellows = self.amity.unallocated_fellow
        self.unallocated_staff = self.amity.unallocated_staff

    def test_create_living_space(self):
        """ Tests whether a livingspace(room) is created. """
        initial_room_count = len(self.living_spaces)
        self.amity.create_room("L", 'php')
        new_room_count = len(self.living_spaces)

        self.assertEqual(new_room_count, initial_room_count + 1)

    def test_create_office(self):
        """ Tests whether an office(room) is created. """
        initial_room_count = len(self.offices)
        self.amity.create_room("O", "Camelot")
        new_room_count = len(self.offices)

        self.assertEqual(new_room_count, initial_room_count + 1)

    def test_create_multiple_rooms(self):
        """ Tests whether multiple rooms can be created. """
        initial_room_count = len(self.living_spaces)
        self.amity.create_room("L", "Scalar", "Laravel")
        new_room_count = len(self.living_spaces)

        self.assertEqual(new_room_count, initial_room_count + 2)

    def test_room_already_exists(self):
        """ Test behaiviour of create room, when you create an already existing room """
        self.new_living_space
        msg = self.amity.create_room("L", "mombasa")

        self.assertEqual("Room Already Exists!", msg)

    def test_invalid_room_type(self):
        """ Tests whether message is return when invalid room type param is passed"""
        new_room = self.amity.create_room("S", "Laravel")
        self.assertEqual(new_room, "Inavlid Room Type!")

    def test_vacant_rooms_returned(self):
        """ Tests whether rooms that have remaining slots are returned. """
        new_room = Office('mombasa')
        self.amity.check_vacant_rooms()
        vacant_status = new_room.is_full()

        self.assertFalse(vacant_status)

    def test_is_full_returns_true(self):
        """ Tests whether the system knows when a room is fully occupied. """
        new_room = Office('mombasa')
        new_room.occupants.append(136648)
        new_room.occupants.append(136650)
        new_room.occupants.append(136651)
        new_room.occupants.append(136652)
        new_room.occupants.append(136653)
        new_room.occupants.append(136654)
        vacant_status = new_room.is_full()

        self.assertTrue(vacant_status)

    def test_is_full_returns_false(self):
        """ Tests whether the system knows when a room is not fully occupied. """
        new_room = Office('mombasa')
        new_room.occupants.append(136648)
        new_room.occupants.append(136650)
        new_room.occupants.append(136651)
        vacant_status = new_room.is_full()

        self.assertFalse(vacant_status)

    def test_add_fellow(self):
        """ Tests if a fellow is added successfully added. """
        new_fellow = self.new_fellow

        self.assertEqual("Person Created Successfully!", new_fellow)

    def test_add_staff(self):
        """ Tests if a staff is added successfully added """
        new_staff = self.new_staff

        self.assertEqual("Person Created Successfully!", new_staff)

    def test_new_fellow_in_unallocated(self):
        """ Tests whether a newly created fellow is saved to the unallocated list. """
        unallocated_status = True if len(self.unallocated_fellows) > 0 else False

        self.assertTrue(unallocated_status)

    def test_new_staff_in_unallocated(self):
        """ Tests whether a newly created staff is saved to the unallocated list. """
        unallocated_status = True if len(self.unallocated_staff) > 0 else False

        self.assertTrue(unallocated_status)

    def test_allocate_staff(self):
        """ Tests whether a new staff member is allocated an office. """
        staff = self.staff[-1]
        self.amity.allocate_person(str(staff.employee_id))
        unallocated_length = len(self.unallocated_staff)

        self.assertEqual(0, unallocated_length)

    def test_allocate_fellow(self):
        """ Tests whether a new fellow is allocated an office and livingspace. """
        fellow = self.fellows[-1]
        self.amity.allocate_person(str(fellow.employee_id))
        unallocated_length = len(self.unallocated_fellows)

        self.assertEqual(0, unallocated_length)

    def test_if_person_not_found(self):
        """ Tests whether a non-existent person can be allocated a room. """
        non_existent_person = 1000001
        allocated_status = self.amity.allocate_person(str(non_existent_person))

        self.assertEqual("Person not found!", allocated_status)

    def test_if_livingspaces_not_found(self):
        """ Test whether allocate_person works when no living_spaces are created. """
        fellow = self.fellows[-1]
        self.amity.living_spaces = []
        allocated_msg = self.amity.allocate_person(str(fellow.employee_id))

        self.assertIn("LivingSpace not available!", allocated_msg)

    def test_if_offices_not_found(self):
        """ Test whether allocate_person works when no offices are created. """
        fellow = self.fellows[-1]
        self.amity.offices = []
        allocated_msg = self.amity.allocate_person(str(fellow.employee_id))

        self.assertIn("Office not available!", allocated_msg)

    def test_when_staff_wants_lspace(self):
        """
        Tests whether the system returns an error message when
        Staff wants_accomodation = Y
        """
        self.amity.add_person("alexis", "sanchez", "staff", "Y")
        staff = self.staff[-1]
        allocated_msg = self.amity.allocate_person(str(staff.employee_id))

        self.assertIn("Cannot assign LivingSpace to staff!", allocated_msg)

    def test_reallocate_if_person_not_found(self):
        """ Tests whether a non-existent person can be reallocated to a room. """
        non_existent_person = 1000001
        allocated_status = self.amity.reallocate_person(str(non_existent_person), 'mombasa')

        self.assertEqual("Person not found", allocated_status)

    def test_if_new_room_name_exists(self):
        """ Test whether reallocate_person finds new_room_name. """
        fellow = self.fellows[-1]
        self.amity.allocate_person(str(fellow.employee_id))
        reallocated_status = self.amity.reallocate_person(str(fellow.employee_id), 'mogadishu')

        self.assertEqual("Room does not Exist!", reallocated_status)

    def test_reallocate_lspace(self):
        """ Test whether a person can be reallocated from one room to another. """
        fellow = self.fellows[-1]
        self.amity.allocate_person(str(fellow.employee_id))

        self.amity.create_room("L", 'kilifi')

        reallocated_status = self.amity.reallocate_person(str(fellow.employee_id), 'kilifi')

        self.assertIn("Successfully Reallocated", reallocated_status)

    def test_reallocate_office(self):
        """ Test whether a person can be reallocated from one room to another. """
        fellow = self.fellows[-1]
        self.amity.allocate_person(str(fellow.employee_id))

        self.amity.create_room("O", 'kilaguni')

        reallocated_status = self.amity.reallocate_person(str(fellow.employee_id), 'kilaguni')

        self.assertIn("Successfully Reallocated", reallocated_status)

    def test_staff_reallocated_lspace(self):
        """
        Test that error message is returned when staff is reallocated to \
        LivingSpace
        """
        staff = self.staff[-1]
        self.amity.allocate_person(str(staff.employee_id))

        reallocated_status = self.amity.reallocate_person(str(staff.employee_id), 'mombasa')

        self.assertIn("Cannot reallocate staff to livingspace!", reallocated_status)

    def test_load_people(self):
        """ Test whether load_people adds people to room from a text file. """
        self.amity.fellows = []
        self.amity.load_people("people")

        self.assertTrue(self.amity.fellows)

    def test_load_people_from_non_existent_file(self):
        """ Tests whether people can be loaded from a non-existent file. """
        load_people = self.amity.load_people("persons")

        self.assertEqual("File: persons, Not Found!", load_people)

    def test_allocations_outputs_file(self):
        """ Tests whether allocations can be printed on file: new_allocations. """
        staff = self.staff[-1]
        self.amity.allocate_person(str(staff.employee_id))
        self.amity.print_allocations("new_allocations")
        file_path = os.path.abspath("data/new_allocations.txt")
        file_status = os.path.isfile(file_path)

        self.assertTrue(file_status)

    def test_allocations_outputs_screen(self):
        """ Tests whether allocations can be printed on file: new_allocations. """
        staff = self.staff[-1]
        self.amity.allocate_person(str(staff.employee_id))
        data = self.amity.print_allocations()

        self.assertTrue(data)

    def test_output_when_no_room(self):
        """ Test print_allocations when no rooms in the system """
        self.amity.offices = []
        self.amity.living_spaces = []

        data = self.amity.print_allocations()

        self.assertIn("No Rooms Found.", data)

    def test_output_to_file(self):
        """ Tests whether the unallocated can be printed on file: new_unallocated. """
        staff = self.staff[-1]
        self.amity.allocate_person(str(staff.employee_id))
        self.amity.print_unallocated("new_unallocated")
        file_path = os.path.abspath("data/new_unallocated.txt")
        file_status = os.path.isfile(file_path)

        self.assertTrue(file_status)

    def test_unallocated_outputs_screen(self):
        """ Tests whether the unallocated can be printed on file: new_unallocated. """
        staff = self.staff[-1]
        self.amity.allocate_person(str(staff.employee_id))
        data = self.amity.print_unallocated()

        self.assertTrue(data)

    def test_print_non_existent_room(self):
        """ Test whether a non-existent room can be printed on screen. """
        print_room = self.amity.print_room("arkham")

        self.assertIn("Room not found!", print_room)

    def test_when_no_occupants_in_room(self):
        """ Test whether a room with no occupants can be printed on screen. """
        print_room = self.amity.print_room("mombasa")

        self.assertIn("No occupants in room", print_room)

    def test_print_correct_occupants(self):
        """ Test whether a room and its occupants can be printed on screen. """
        fellow = self.fellows[-1]
        self.amity.allocate_person(str(fellow.employee_id))
        print_room = self.amity.print_room("mombasa")

        self.assertIn("Hum Musonye", print_room)

    def test_save_state_creates_db(self):
        """ Test whether save_state creates a SQLite database. """
        self.amity.save_state("test")
        file_path = os.path.abspath("test.db")
        file_status = os.path.isfile(file_path)

        self.assertTrue(file_status)

    def test_non_existent_db(self):
        """ Tests how load_state behaves when passed a nn existent db name. """
        load_state = self.amity.load_state("amity_lagos")

        self.assertEqual("Database amity_lagos.db not found!", load_state)

    def test_load_test(self):
        """ Test whether load_state persists data from db to amity system. """
        self.amity.add_person("bat", "man", "fellow", "Y")
        self.amity.save_state("test_load")
        self.amity.load_state("test_load")

        is_loaded = True if len(self.amity.fellows) > 1 else False

        self.assertTrue(is_loaded)

if __name__ == '__main__':
    unittest.main()
