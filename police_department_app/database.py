import sqlite3
import bcrypt
import re  # For validation

# Database connection
conn = sqlite3.connect('police_department.db', check_same_thread=False)
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS persons (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    alias TEXT,
                    reputation TEXT,
                    age INTEGER,
                    nationality TEXT,
                    id_number TEXT UNIQUE,
                    residence TEXT,
                    profession TEXT,
                    workplace TEXT,
                    military_service TEXT,
                    distinctive_marks TEXT,
                    entry_number TEXT UNIQUE)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS charges (
                    charge_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    person_id INTEGER,
                    charge_number TEXT,
                    charge_year INTEGER,
                    police_station TEXT,
                    crime_method TEXT,
                    FOREIGN KEY (person_id) REFERENCES persons (id) ON DELETE CASCADE)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS managers (
                    manager_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL)''')

# Add charge function
def add_charge(person_id, charge_number, charge_year, police_station, crime_method):
    cursor.execute("INSERT INTO charges (person_id, charge_number, charge_year, police_station, crime_method) VALUES (?, ?, ?, ?, ?)",
                   (person_id, charge_number, charge_year, police_station, crime_method))
    conn.commit()

# Add person with input validation
def add_person(name, alias, reputation, age, nationality, id_number, residence, profession, workplace, military_service, distinctive_marks, entry_number):
    if not re.match(r"^[a-zA-Z ]+$", name):  # Validate name to only contain letters and spaces
        raise ValueError("Invalid name format")
    cursor.execute(
        "INSERT INTO persons (name, alias, reputation, age, nationality, id_number, residence, profession, workplace, military_service, distinctive_marks, entry_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (name, alias, reputation, age, nationality, id_number, residence, profession, workplace, military_service, distinctive_marks, entry_number))
    conn.commit()

# Search person function with limit
def search_person(name=None, id_number=None):
    if id_number:
        cursor.execute("SELECT * FROM persons WHERE id_number = ? LIMIT 100", (id_number,))
    elif name:
        cursor.execute("SELECT * FROM persons WHERE name LIKE ? LIMIT 100", ('%' + name + '%',))
    
    results = cursor.fetchall()
    return [{"name": row[1], "id_number": row[6]} for row in results]

# Add manager with password hashing
def add_manager(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute('INSERT INTO managers (username, password) VALUES (?, ?)', (username, hashed_password))
    conn.commit()

# Check manager login with hashed password
def check_login(username, password):
    cursor.execute('SELECT password FROM managers WHERE username = ?', (username,))
    result = cursor.fetchone()
    
    if result:
        hashed_password = result[0]
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            return True
    return False

# Close connection
def close_connection():
    conn.close()
