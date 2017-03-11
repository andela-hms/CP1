import sys
sys.path.insert(0, '/Users/hms/Projects/cp1/app')
import os
import random
from rooms.rooms import Office, LivingSpace
from people.people import Staff, Fellow
from db.model_base import DbObject, PersonDetails, RoomDetails

class Amity(object):
    """
    The room management class that is instatiated to
    create rooms and persons and assign them to rooms
    """
    def __init__(self):
        self.fellows = []
        self.staff = []
        self.unallocated_fellow = []
        self.unallocated_staff = []
        self.offices = []
        self.living_spaces = []

    def create_room(self, room_type, *room_names):

        """
        Creates mutiple and single rooms in Amity.
        """
        if room_type.upper() not in ['L', 'O']:
            return "Inavlid Room Type!"

        all_rooms = [room.name for room in self.living_spaces + self.offices]

        for room in room_names:
            if room in all_rooms:
                return "Room Already Exists!"
            if room_type.upper() == 'L':
                new_room = LivingSpace(room.lower())
                self.living_spaces.append(new_room)
            elif room_type.upper() == 'O':
                new_room = Office(room.lower())
                self.offices.append(new_room)
        return "Room(s) Created Successfully"

    def check_vacant_rooms(self):
        """ Checks whether a room is full, if not it appends it to vacant_rooms """
        vacant_rooms = {
            'offices': [],
            'livingspaces':[]
        }

        for room in self.offices:
            if not room.is_full():
                vacant_rooms['offices'].append(room)

        for room in self.living_spaces:
            if not room.is_full():
                vacant_rooms['livingspaces'].append(room)

        return vacant_rooms

    def add_person(self, fname, lname, role, wants_accomodation='N'):

        """
        Adds a new Person(Fellow or Staff) to Amity System
        """

        full_name = "{} {}".format(fname, lname)
        role = role.upper()
        wants_accomodation = wants_accomodation.upper()
        if role == 'FELLOW':

            new_person = Fellow(full_name)
            self.fellows.append(new_person)
            self.unallocated_fellow.append(new_person)

        elif role == 'STAFF':

            new_person = Staff(full_name)
            self.staff.append(new_person)
            self.unallocated_staff.append(new_person)

        return "Person Created Successfully!"

    def allocate_person(self, person_id):
        """
        Assigns room to a newly added Person
        Also assigns a room to an unallocated Person
        """
        unallocated_persons = self.unallocated_fellow + self.unallocated_staff
        found = False
        msg = ""
        found_person = ""
        # find person with person_id
        for person in unallocated_persons:
            if person_id == str(person.employee_id):
                found = True
                found_person = person

        if found:

            if found_person.wants_accomodation == 'Y':

                if found_person.role == "FELLOW":

                    vacant_rooms = self.check_vacant_rooms()

                    if len(vacant_rooms['livingspaces']):
                        lspace_choice = random.choice(vacant_rooms['livingspaces'])
                        # Assign the living_space
                        lspace_choice.occupants.append(found_person.employee_id)
                        msg += "Person(s) assigned to LivingSpace : {}\n" .format(lspace_choice)
                        self.unallocated_fellow.remove(found_person)

                    else:
                        msg += "LivingSpace not available!\n"
            else:
                msg += "Cannot assign LivingSpace to staff!\n"

            vacant_offices = self.check_vacant_rooms()['offices']
            if len(vacant_offices):
                office_choice = random.choice(vacant_offices)

                office_choice.occupants.append(found_person.employee_id)
                msg += "Person(s) assigned to Office : {}\n" .format(office_choice)

                if found_person.role == "STAFF":
                    self.unallocated_staff.remove(found_person)
            else:
                msg += "Office not available!"

            return msg
        else:
            return "Person not found!"

    def reallocate_person(self, person_id, new_room_name):

        """
        Reallocates a Staff or Fellow to another Office \
        from an existing one
        Reallocates a Fellow from an existing room \
        to another one
        """
        found = False
        msg = ""
        person_role = ""
        room_occupied1 = ""
        room_occupied2 = ""
        found_new_room = ""
        occupied_rooms = []
        new_room_name = new_room_name.lower()
        all_persons = self.fellows + self.staff
        all_rooms = self.living_spaces + self.offices
        vacant_rooms = self.check_vacant_rooms()

        all_people = [str(person.employee_id) for person in all_persons]
        if person_id not in all_people:
            return "Person not found"
        else:
            found = True
            for person in all_persons:
                if str(person_id) == str(person.employee_id):
                    person_role = person.role.lower()

        if new_room_name not in [room.name for room in all_rooms]:
            return "Room does not Exist!"
        else:
            found = True
            for room in all_rooms:
                if str(new_room_name) == str(room.name):
                    found_new_room = room

        # Check whether person is allocated to a particular room
        # rooms_occupied has all rooms person_id is assigned to

        if found:
            try:
                for room in vacant_rooms['livingspaces']:
                    if int(person_id) in room.occupants:
                        msg += "{} Was in this room: {}\n" .format(person_id, room.name)
                        room_occupied1 = room
                        occupied_rooms.append(room.name)

                if found_new_room.room_type == "office":
                    for room in vacant_rooms['offices']:
                        if int(person_id) in room.occupants:
                            msg += "{} Was in this room: {}\n" .format(person_id, room.name)
                            room_occupied2 = room
                            occupied_rooms.append(room.name)

                    if new_room_name in occupied_rooms:
                        return "Cannot reallocate to currently occupied room!"

                    room_occupied2.occupants.remove(int(person_id))
                    msg += "Removed from: {}\n".format(room_occupied2.name)
                    found_new_room.occupants.append(int(person_id))
                    msg += "Successfully Reallocated to Room {}".format(found_new_room)

                elif found_new_room.room_type == "livingspace" and person_role == "fellow":
                    room_occupied1.occupants.remove(int(person_id))
                    msg += "Removed from: {}\n".format(room_occupied1.name)
                    found_new_room.occupants.append(int(person_id))
                    msg += "Successfully Reallocated to Room {}".format(found_new_room)

                else:
                    msg += "Cannot reallocate staff to livingspace!"
            except AttributeError:
                msg += "Cannot reallocate to different room type!"

        return msg


    def load_people(self, file_name):

        """
        Adds people to room from a text file
        """
        try:
            file_path = os.path.abspath("data/{}.txt").format(file_name)
            content = open(file_path, 'r')
            people = content.readlines()

            for person in people:
                person_info = person.split()

                self.add_person(*person_info)

            return "Successfully Loaded People"
        except(ValueError, IOError):
            return "File: {}, Not Found!".format(file_name)

    def print_allocations(self, file_name=None):
        """
        Prints a list of allocations onto the screen
        Or to a file if filename provided.
        """
        occupied_rooms = []
        found = False
        all_persons = self.staff + self.fellows

        rooms = self.living_spaces + self.offices
        for room in rooms:
            if len(room.occupants) > 0:
                occupied_rooms.append(room)
        data = ""
        data += ("{}\n".format("ALLOCATIONS"))
        data += ("{}\n\n".format("-" * 30))

        for room in occupied_rooms:
            found = True
            occupants = [occupant for occupant in room.occupants]
            names = [person.name for person in all_persons if person.employee_id in occupants]
            data += ("{} : {}\n".format(room.room_type.upper(), room.name))
            data += ("{}\n".format("-" * 30))
            data += ', '.join(str(name).title() for name in names)
            data += ("\n\n")

        if found is False:
            data += "No Rooms Found."

        if file_name:
            file_path = os.path.abspath("data/{}.txt").format(file_name)
            with open(file_path, 'w') as out:
                out.write('{}'.format(str(data)))
            return file_name + ".txt written successfully"

        else:
            return data

    def print_unallocated(self, file_name=None):

        """
        Prints a list of unallocated people to the screen.
        Or to a file if filename provided.
        """
        found = False
        unallocated_people = self.unallocated_fellow + self.unallocated_staff
        data = ""
        data += ("{}\n".format("UNALLOCATED PEOPLE"))
        data += ("{}\n\n".format("-" * 30))

        for person in unallocated_people:
            found = True
            data += ("{}\n".format("-"*35))
            data += ("{} {}:{}\n".format(person.role, person.name.title(), person.employee_id))
            data += ("{}\n".format("-"*35))
            data += ("\n")

        if found is False:
            data += "No Persons Found."

        if file_name:
            file_path = os.path.abspath("data/{}.txt").format(file_name)
            with open(file_path, 'w') as out:
                out.write('{}'.format(str(data)))
            response = file_name + ".txt written successfully"
            return response

        else:
            return data

    def print_room(self, room_name):

        """
        Prints the names of all the people in room_name on the
        """
        rooms = self.offices + self.living_spaces
        all_people = self.fellows + self.staff
        room_name = room_name.lower()
        # Check if room is available
        found = False
        members_available = False
        msg = ""
        msg += "Person(s) In: {}\n" .format(room_name)
        msg += ("{}\n\n".format("-" * 30))
        
        for room in rooms:
            if room_name.lower() == room.name:
                found = True
                room_type = room.room_type
                for person in all_people:
                    if person.employee_id in room.occupants:
                        members_available = True
                        msg += "{} {}: {}\n".format(person.role, person.name.title(), person.employee_id)

                if members_available is False:
                    msg += "No occupants in room"
        if found:
            return msg
        else:
            return "Room not found!"

    def save_state(self, dbname='amity'):

        """
        Persists all the data stored in the app to a SQLite database.
        """
        database_name = 'amity' if dbname is None else dbname
        msg = ""
        all_rooms = self.offices + self.living_spaces
        all_people = self.fellows + self.staff

        database = DbObject(database_name)
        session = database.start_session().session

        database.clear_db_data()

        for person in all_people:
            living_space = ""
            office = ""
            pid = person.employee_id
            name = person.name
            role = person.role
            for room in all_rooms:
                if pid in room.occupants:
                    if room.room_type == "livingspace":
                        living_space = room.name
                    elif room.room_type == "office":
                        office = room.name

            person = PersonDetails(person_id=pid, person_name=name, role=role, living_space_assigned=living_space, office_assigned=office)
            session.add(person)
            session.commit()

        for room in all_rooms:
            name = room.name
            roomtype = room.room_type
            occupants_num = len(room.occupants)

            room_info = RoomDetails(room_name=name, room_type=roomtype, number_of_occupants=occupants_num)
            session.add(room_info)
            session.commit()

        msg += "Successfully Persisted Data to db: {}".format(database_name)
        return msg


    def load_state(self, dbname='amity'):

        """
        Persists all the data stored in the SQLite database to the app.
        """
        database_name = 'amity' if dbname is None else dbname
        file_path = os.path.abspath(database_name + ".db")
        file_status = os.path.isfile(file_path)
        msg = ""

        self.living_spaces = []
        self.offices = []
        self.fellows = []
        self.staff = []
        self.unallocated_fellow = []
        self.unallocated_staff = []

        if file_status:

            database = DbObject(database_name)
            session = database.start_session().session

            # load people to their respective variables

            all_people_query = session.query(PersonDetails).all()
            for person in all_people_query:
                fellow = ""
                staff = ""
                if person.role.upper() == "FELLOW":
                    fellow = Fellow(person.person_name, person.person_id)
                    self.fellows.append(fellow)
                elif person.role.upper() == "STAFF":
                    staff = Staff(person.person_name, person.person_id)
                    self.staff.append(staff)

            # load rooms to their respective variables

            all_rooms_query = session.query(RoomDetails).all()
            for room in all_rooms_query:
                living_space = ""
                office = ""
                if room.room_type.upper() == "LIVINGSPACE":
                    living_space = LivingSpace(room.room_name)
                    self.living_spaces.append(living_space)

                elif room.room_type.upper() == "OFFICE":
                    office = Office(room.room_name)
                    self.offices.append(office)

            # add persons to occupants in all rooms
            all_loaded_rooms = self.living_spaces + self.offices

            for room in all_loaded_rooms:
                for person in all_people_query:
                    if person.living_space_assigned == room.name:
                        room.occupants.append(person.person_id)

                    elif person.office_assigned == room.name:
                        room.occupants.append(person.person_id)

            # get unallocated and add them to unallocated

            unallocated_fellow_ids = []
            unallocated_staff_ids = []

            for person in all_people_query:
                if person.role == "FELLOW":
                    if person.living_space_assigned == "":
                        unallocated_fellow_ids.append(person.person_id)
                else:
                    if person.office_assigned == "":
                        unallocated_staff_ids.append(person.person_id)

            # match ids with person objects then save them to unallocated
            for id_ in unallocated_fellow_ids:
                for person in self.fellows:
                    if id_ == person.employee_id:
                        self.unallocated_fellow.append(person)

            for id_ in unallocated_staff_ids:
                for person in self.staff:
                    if id_ == person.employee_id:
                        self.unallocated_staff.append(person)

            num_fellows = len(self.fellows)
            num_staff = len(self.staff)
            num_offices = len(self.offices)
            num_livingspaces = len(self.living_spaces)

            msg += "Successfully Loaded {} fellow(s)\n".format(num_fellows)
            msg += "Successfully Loaded {} staff\n".format(num_staff)
            msg += "Successfully Loaded {} living_space(s)\n".format(num_livingspaces)
            msg += "Successfully Loaded {} office(s)".format(num_offices)

        else:
            msg += "Database {}.db not found!".format(database_name)

        return msg
