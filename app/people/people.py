class Person(object):
    """
    Class Person creates a Person object.
    Class Staff and Fellow inherit from Person
    """
    def __init__(self, name, employee_id, wants_accomodation):
        self.name = name
        self.wants_accomodation = wants_accomodation
        if employee_id:
            self.employee_id = employee_id
        else:
            self.employee_id = id(self)


class Fellow(Person):
    """ Creates a fellow """
    def __init__(self, name, employee_id=None, wants_accomodation='Y'):
        super(Fellow, self).__init__(name, employee_id, wants_accomodation)
        self.role = "FELLOW"

    def __repr__(self):
        return "F:{} Id:{}".format(self.name, self.employee_id)

class Staff(Person):
    """ Creates a staff """
    def __init__(self, name, employee_id=None, wants_accomodation='N'):
        super(Staff, self).__init__(name, employee_id, wants_accomodation)
        self.role = "STAFF"

    def __repr__(self):

        return "S:{} Id:{}".format(self.name, self.employee_id)
