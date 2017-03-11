import unittest
from rooms import Room, Office, LivingSpace


class TestRoom(unittest.TestCase):
    """ Tests Room (parent) class """
    def test_office_inherits_room(self):
        """ Tests whether office inherits from Room class. """

        office = Office("Narnia")
        self.assertIsInstance(office, Room)

    def test_livingspace_inherits_room(self):
        """ Tests whether livingspace inherits from Room class. """

        livingspace = LivingSpace("Scalar")
        self.assertIsInstance(livingspace, Room)


if __name__ == "__main__":
    unittest.main()
