from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import bcrypt
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from sqlalchemy import or_

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
    alias = Column(String, default='0')
    reputation = Column(String, default='0')
    age = Column(Integer, default=0)
    nationality = Column(String, default='0')
    id_number = Column(String, default='0')
    residence = Column(String, default='0')
    profession = Column(String, default='0')
    workplace = Column(String, default='0')
    military_service = Column(String, default='0')
    distinctive_marks = Column(String, default='0')
    entry_number = Column(String, default='0')
    place_number = Column(String, default='0')  # رقم مكانها
    risk_number = Column(String, default='0')   # رقم الخطورة
    activity = Column(String, default='0')      # النشاط
    category = Column(String, default='0')      # الفئة
    charges = relationship("Charge", back_populates="person")

class Charge(Base):
    __tablename__ = 'charges'
    charge_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('persons.id'), nullable=False)
    charge_number = Column(String, default='0')
    charge_year = Column(Integer, default=0)
    police_station = Column(String, default='0')
    crime_method = Column(String, default='0')
    person = relationship("Person", back_populates="charges")

class Manager(Base):
    __tablename__ = 'managers'
    manager_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

# Create the tables
# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


def add_charge(person_id, charge_number, charge_year, police_station, crime_method):
    new_charge = Charge(
        person_id=person_id, charge_number=charge_number, charge_year=charge_year,
        police_station=police_station, crime_method=crime_method
    )
    session.add(new_charge)
    session.commit()

def add_person(name, alias, reputation, age, nationality, id_number, residence, profession, workplace, military_service, distinctive_marks, entry_number, place_number, risk_number, activity, category):
    new_person = Person(
        name=name,
        alias=alias,
        reputation=reputation,
        age=age,
        nationality=nationality,
        id_number=id_number,
        residence=residence,
        profession=profession,
        workplace=workplace,
        military_service=military_service,
        distinctive_marks=distinctive_marks,
        entry_number=entry_number,
        place_number=place_number,  
        risk_number=risk_number,    
        activity=activity,          
        category=category
    )
    session.add(new_person)
    session.commit()
    return new_person.id  #  for future use


# Search person function with limit

def search_person(search_input):
    persons = []
    if search_input:
        # name
        persons = session.query(Person)\
        .join(Charge, Person.charges)\
        .filter(or_(Person.name.like(f'%{search_input}%'),
                    Charge.charge_number.like(f'%{search_input}%')))\
        .options(joinedload(Person.charges))\
        .limit(100)\
        .all()
        # person_id
    
    return [{"name": person.name, "id": person.id, "residence": person.residence} for person in persons]


def get_person_by_id(id=0):
    person = session.query(Person).filter_by(id=id).first()
    if person:
        return person
    return None


# Add manager with password hashing
def add_manager(username, password):
    try:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_manager = Manager(username=username, password=hashed_password)
        session.add(new_manager)
        session.commit()
        return True  # Success
    except IntegrityError:
        session.rollback()
        return False  # Username already exists
    except Exception as e:
        session.rollback()
        raise e  # Pass the exception upwards for the route to handle

# Check manager login with hashed password
def check_login(username, password):
    once = session.query(func.count(Manager.manager_id)).scalar()
    if once == 0:
        add_manager(username, password)
        return True

    manager = session.query(Manager).filter_by(username=username).first()
    
    if manager and bcrypt.checkpw(password.encode(), manager.password):
        return True
    return False


# Close connection
def close_connection():
    session.close()
