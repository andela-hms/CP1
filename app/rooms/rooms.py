class Room(object):
    """
    Class Room creates a Room object.
    Class Office and LivingSpace inherit from Room
    """
    def __init__(self, name):
        self.name = name
        self.occupants = []

    def is_full(self):
        """ Returns rooms that are fully occupied"""
        return len(self.occupants) >= self.max_capacity


class Office(Room):
    """ Creates an office """
    def __init__(self, name):
        super(Office, self).__init__(name)
        self.max_capacity = 6
        self.room_type = "office"

    def __repr__(self):
        return "{}" .format(self.name)


class LivingSpace(Room):
    """ Creates a livingspace """
    def __init__(self, name):
        super(LivingSpace, self).__init__(name)
        self.max_capacity = 4
        self.room_type = "livingspace"

    def __repr__(self):
        return "{}" .format(self.name)
