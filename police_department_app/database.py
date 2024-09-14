from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import bcrypt
import re

# Setup SQLite database connection
engine = create_engine('sqlite:///police_department.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Models
class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    alias = Column(String)
    reputation = Column(String)
    age = Column(Integer)
    nationality = Column(String)
    id_number = Column(String, unique=True)
    residence = Column(String)
    profession = Column(String)
    workplace = Column(String)
    military_service = Column(String)
    distinctive_marks = Column(String)
    entry_number = Column(String, unique=True)
    charges = relationship("Charge", back_populates="person")

class Charge(Base):
    __tablename__ = 'charges'
    charge_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('persons.id'), nullable=False)
    charge_number = Column(String)
    charge_year = Column(Integer)
    police_station = Column(String)
    crime_method = Column(String)
    person = relationship("Person", back_populates="charges")

class Manager(Base):
    __tablename__ = 'managers'
    manager_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

# Create the tables
Base.metadata.create_all(engine)


def add_charge(person_id, charge_number, charge_year, police_station, crime_method):
    new_charge = Charge(
        person_id=person_id, charge_number=charge_number, charge_year=charge_year,
        police_station=police_station, crime_method=crime_method
    )
    session.add(new_charge)
    session.commit()


def add_person(name, alias, reputation, age, nationality, id_number, residence, profession, workplace, military_service, distinctive_marks, entry_number):
    
    new_person = Person(
        name=name, alias=alias, reputation=reputation, age=age,
        nationality=nationality, id_number=id_number,
        residence=residence, profession=profession, workplace=workplace,
        military_service=military_service, distinctive_marks=distinctive_marks,
        entry_number=entry_number
    )
    session.add(new_person)
    session.commit()
    return new_person.id  # Return the new person ID for future use


# Search person function with limit
def search_person(name=None, id_number=None):
    if id_number:
        persons = session.query(Person).filter_by(id_number=id_number).limit(100).all()
    elif name:
        persons = session.query(Person).filter(Person.name.like(f'%{name}%')).limit(100).all()
    
    return [{"name": person.name, "id_number": person.id_number} for person in persons]

# Add manager with password hashing
def add_manager(username, password):
    try:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_manager = Manager(username=username, password=hashed_password)
        session.add(new_manager)
        session.commit()
        return True
    except ValueError:
        return False

# Check manager login with hashed password
def check_login(username, password):
    manager = session.query(Manager).filter_by(username=username).first()
    
    if manager and bcrypt.checkpw(password.encode(), manager.password):
        return True
    return False


# Close connection
def close_connection():
    session.close()
