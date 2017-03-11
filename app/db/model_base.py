from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class DbObject(object):
    def __init__(self, dbname="amity"):
        self.db_name = dbname
        self.engine = create_engine('sqlite:///'+ self.db_name +'.db')
        Base.metadata.create_all(self.engine)

    def start_session(self):
        Session = sessionmaker(bind = self.engine)
        self.session = Session()

        return self

    def clear_db_data(self):
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

class PersonDetails(Base):
    __tablename__ = 'person'
    person_id = Column(Integer, primary_key=True)
    person_name = Column(String(40))
    role = Column(String(10))
    living_space_assigned = Column(String(50))
    office_assigned = Column(String(50))

class RoomDetails(Base):
    __tablename__ = 'room'
    room_name = Column(String(50), primary_key=True)
    room_type = Column(String(10))
    number_of_occupants = Column(Integer)