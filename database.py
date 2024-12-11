from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import bcrypt
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from sqlalchemy import or_, and_
import re

# Setup SQLite database connection
engine = create_engine('sqlite:///police_department.db', echo=False)
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
    entry_number = Column(String, default='0')   # رقم الادراج
    risk_number = Column(String, default='0')   # رقم الخطورة
    activity = Column(String, default='0')      # النشاط
    category = Column(String, default='0')      # الفئة
    mother_name = Column(String, default='')  # اسم الأم
    spouse_name = Column(String, default='')  # اسم الزوج/الزوجة
    gender = Column(String, default='')  # النوع
    birth_date = Column(Date, nullable=True)  # تاريخ الميلاد
    marital_status = Column(String, default='')  # الحالة الاجتماعية
    charges = relationship("Charge", back_populates="person", cascade="all, delete-orphan")
    distinctive_marks = relationship("DistinctiveMark", back_populates="person", cascade="all, delete-orphan")


# جدول العلامات المميزة (DistinctiveMarks)
class DistinctiveMark(Base):
    __tablename__ = 'distinctive_marks'
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('persons.id'))
    distinctive_marks = Column(String, default='0')
    place_number = Column(String, default='0')  # رقم مكانها
    person = relationship("Person", back_populates="distinctive_marks")

class Charge(Base):
    __tablename__ = 'charges'
    charge_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('persons.id'), nullable=False)
    charge_number = Column(String, default='0')
    charge_year = Column(Integer, default='0')
    police_station = Column(String, default='0')
    case_type = Column(String, default='0')
    crime_method = Column(String, default='0')
    judgement = Column(String, default='0')
    person = relationship("Person", back_populates="charges")

class Manager(Base):
    __tablename__ = 'managers'
    manager_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

# Create the tables
# 
# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


def add_charge(person_id, charge_number, charge_year, police_station, crime_method, case_type, judgement):
    new_charge = Charge(
        person_id=person_id, charge_number=charge_number, charge_year=charge_year,
        police_station=police_station, crime_method=crime_method,
        case_type=case_type, judgement=judgement
    )
    session.add(new_charge)
    session.commit()


def add_distinctive_marks(person_id, distinctive_marks, place_number):
    new_distinctive_mark = DistinctiveMark(
        person_id=person_id,distinctive_marks=distinctive_marks, place_number=place_number)
    session.add(new_distinctive_mark)
    session.commit()

def add_person(name, alias, reputation, age, nationality, id_number, residence, profession, workplace, military_service, entry_number, risk_number, activity, category,
               mother_name,
                spouse_name,
                gender,
                birth_date,
                marital_status):
    normalized_name = normalize_name(name)
    new_person = Person(
        name=normalized_name,
        alias=alias,
        reputation=reputation,
        age=age,
        nationality=nationality,
        id_number=id_number,
        residence=residence,
        profession=profession,
        workplace=workplace,
        military_service=military_service,
        entry_number=entry_number,
        risk_number=risk_number,    
        activity=activity,          
        category=category,
        mother_name=mother_name,
        spouse_name=spouse_name,
        gender=gender,
        birth_date=birth_date,
        marital_status=marital_status
    )
    session.add(new_person)
    session.commit()
    return new_person.id  #  for future use


# Search person function with limit

def search_person(name, entry, search_charge_number, search_charge_year):
    persons = []
    if name:
        # name
        print("**expected name **", name)
        persons = session.query(Person)\
        .join(Charge, Person.charges)\
        .filter((Person.name.like(f'%{normalize_name(name)}%')))\
        .options(joinedload(Person.charges))\
        .limit(100)\
        .all()
    elif entry:
        persons = session.query(Person)\
        .join(Charge, Person.charges)\
        .filter(Person.entry_number.like(f'%{entry}%'))\
        .options(joinedload(Person.charges))\
        .limit(100)\
        .all()
    elif (search_charge_number and search_charge_year):
        persons = session.query(Person)\
        .join(Charge, Person.charges)\
        .filter(and_(Charge.charge_number.like(f'%{search_charge_number}%'),
                    Charge.charge_year.like(f'%{search_charge_year}%')))\
        .options(joinedload(Person.charges))\
        .limit(100)\
        .all()

        # person_id
    
    return [{"name": person.name, "id": person.id, "residence": person.residence, "entry_number": person.entry_number} for person in persons]




def normalize_name(name):
    # إزالة الهمزة من النص
    normalized_name = re.sub(r"[أإآ]", "ا", name)
    return normalized_name


def get_person_by_id(id=0):
    person = session.query(Person).filter_by(id=id).first()
    if person:
        return person
    return None

def get_distinctive_marks(id=0):
    person = session.query(Person).filter_by(id=id).first()
    if person:
        distinctive_marks = session.query(DistinctiveMark).filter_by(person_id=person.id).all()
        return distinctive_marks
    return None

# ************************************************************************
def get_charges(id=0):
    person = session.query(Person).filter_by(id=id).first()
    if person:
        charges = session.query(Charge).filter_by(person_id=person.id).all()
        return charges
    return None
# **************************************************************************

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
