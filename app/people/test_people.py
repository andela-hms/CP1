import unittest
from people import Person, Staff, Fellow


class TestPerson(unittest.TestCase):
    """ Tests person (parent) class """
    def setUp(self):
        self.fellow = Fellow("mark")
        self.staff = Staff("caroline")

    def test_fellow_inherits_person(self):
        """ Test whether class fellow inherits from class Person. """

        fellow = self.fellow
        self.assertIsInstance(fellow, Person)

    def test_staff_inherits_person(self):
        """ Test whether class staff inherits from class Person. """

        staff = self.staff
        self.assertIsInstance(staff, Person)

    def test_staff_string_represantation(self):
        """ Tests whether string representation of the object is returned """
        staff = self.staff
        staff.employee_id = 4430611728

        self.assertEqual("S:caroline Id:4430611728", str(staff))

    def test_fellow_string_represantation(self):
        """ Tests whether string representation of the object is returned """
        fellow = self.fellow
        fellow.employee_id = 4430611728

        self.assertEqual("F:mark Id:4430611728", str(fellow))

if __name__ == "__main__":
    unittest.main()
