#!/usr/bin/python3
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
import bcrypt
import webview
import threading
from database import search_person, add_charge, add_person, add_distinctive_marks, Person, DistinctiveMark, Charge
from database import add_manager, check_login, get_person_by_id, get_distinctive_marks, get_charges
import secrets
secret_key = secrets.token_hex(16)
from sqlalchemy.exc import IntegrityError
from itertools import zip_longest
import logging
logging.basicConfig(level=logging.ERROR)

app = Flask(__name__)
app.secret_key = secret_key

@app.route('/search_person', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        search_input = request.form.get('searchInput')
        results = search_person(search_input)  # تمرير المدخل إلى دالة البحث
        return jsonify(results)  # إرجاع النتائج كـ JSON
    return render_template('search.html')

@app.route('/profile/<int:person_id>', methods=['Get', 'POST'])
def profile(person_id):
    person = get_person_by_id(person_id)  # دالة للحصول على بيانات الشخص من قاعدة البيانات
    for charge in person.charges:
        print(f"Charge Number: {charge.charge_number}, Year: {charge.charge_year}, Police Station: {charge.police_station}, Method: {charge.crime_method}")
    else:
        print("لا توجد تهم لهذا الشخص.")
    return render_template('profile.html', person=person)



@app.route('/add_person_and_charge', methods=['GET', 'POST'])
def add_person_and_charge():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            alias = request.form.get('alias')
            reputation = request.form.get('reputation')
            age = request.form.get('age')
            nationality = request.form.get('nationality')
            id_number = request.form.get('id_number')
            residence = request.form.get('residence')
            profession = request.form.get('profession')
            workplace = request.form.get('workplace')
            military_service = request.form.get('military_service')
            entry_number = request.form.get('entry_number')
            distinctive_marks = request.form.getlist('distinctive_marks[]')
            place_number = request.form.getlist('place_number[]')
            risk_number = request.form.get('risk_number')
            activity = request.form.get('activity')
            category = request.form.get('category')

            charge_number = request.form.getlist('charge_number[]')
            charge_year = request.form.getlist('charge_year[]')
            police_station = request.form.getlist('police_station[]')
            crime_method = request.form.getlist('crime_method[]')

             # Input validation
            if len(name) < 3 or len(name) > 60:
                return jsonify({"message": "الاسم يجب أن يكون بين 3 و 60 حرفًا."}), 400

            if id_number and len(id_number) != 14:
                return jsonify({"message": "الرقم القومي يجب أن يكون 14 رقمًا."}), 400

            if age and (not age.isdigit() or int(age) < 1 or int(age) > 120):
                return jsonify({"message": "يرجى إدخال سن صحيح بين 1 و 120."}), 400
            # إضافة الشخص للقاعدة مع البيانات الجديدة
            person_id = add_person(
                name, alias, reputation, age, nationality, id_number,
                residence, profession, workplace, military_service,
                entry_number,risk_number,
                activity, category
            )

            for mark, location in zip(distinctive_marks, place_number):
                add_distinctive_marks(
                    person_id=person_id, distinctive_marks=mark, place_number=location)

          
            for number, year, station, method in zip(charge_number, charge_year, police_station, crime_method):
                add_charge(
                            person_id=person_id, charge_number=number, charge_year=year, police_station=station, crime_method=method
                )

            return jsonify({"message": "تمت إضافة البيانات بنجاح"})
        except Exception as e:
            return jsonify({"message": f"حدث خطأ: {str(e)}"})
    return render_template('add_person.html')

# Edit profile route for updating person and charge details
@app.route('/edit_person_and_charge/<int:person_id>', methods=['GET', 'POST'])
def edit_person_and_charge(person_id):
    if request.method == 'POST':
        try:
            # Fetch form data for person's personal details
            name = request.form.get('name')
            alias = request.form.get('alias')
            reputation = request.form.get('reputation')
            age = request.form.get('age')
            nationality = request.form.get('nationality')
            id_number = request.form.get('id_number')
            residence = request.form.get('residence')
            profession = request.form.get('profession')
            workplace = request.form.get('workplace')
            military_service = request.form.get('military_service')
            entry_number = request.form.get('entry_number')
            distinctive_marks = request.form.getlist('distinctive_marks[]')
            place_number = request.form.getlist('place_number[]')
            risk_number = request.form.get('risk_number')
            activity = request.form.get('activity')
            category = request.form.get('category')

            # Fetch form data for charges
            charge_number = request.form.getlist('charge_number[]')
            charge_year = request.form.getlist('charge_year[]')
            police_station = request.form.getlist('police_station[]')
            crime_method = request.form.getlist('crime_method[]')

            # Validation checks with appropriate feedback
            if len(name) < 3 or len(name) > 60:
                return jsonify({"message": "الاسم يجب أن يكون بين 3 و 60 حرفًا."}), 400

            if id_number and len(id_number) != 14:
                return jsonify({"message": "الرقم القومي يجب أن يكون 14 رقمًا."}), 400

            if age and (not age.isdigit() or int(age) < 1 or int(age) > 120):
                return jsonify({"message": "يرجى إدخال سن صحيح بين 1 و 120."}), 400

            # Retrieve person by ID and check existence
            person = get_person_by_id(person_id)
            if not person:
                return jsonify({"message": "الشخص غير موجود"}), 404

            # Update person's details
            person.name = name
            person.alias = alias
            person.reputation = reputation
            person.age = age
            person.nationality = nationality
            person.id_number = id_number
            person.residence = residence
            person.profession = profession
            person.workplace = workplace
            person.military_service = military_service
            person.entry_number = entry_number
            person.risk_number = risk_number
            person.activity = activity
            person.category = category

            # Update distinctive marks by checking existing records
            existing_marks = get_distinctive_marks(id=person_id)
            for mark, location, record in zip_longest(distinctive_marks, place_number, existing_marks):
                if record:
                    # Update existing distinctive mark
                    record.place_number = location
                    record.distinctive_marks = mark
                else:
                    # Add new distinctive mark if none exists
                    add_distinctive_marks(person_id=person_id, distinctive_marks=mark, place_number=location)

            # Update charges by checking existing records
            existing_charges = get_charges(id=person_id)
            for number, year, station, method, charge in zip_longest(charge_number, charge_year, police_station, crime_method, existing_charges):
                if charge:
                    # Update existing charge details
                    charge.charge_number = number
                    charge.charge_year = year
                    charge.police_station = station
                    charge.crime_method = method
                else:
                    # Add a new charge if none exists
                    add_charge(person_id=person_id, charge_number=number, charge_year=year, police_station=station, crime_method=method)

            return jsonify({"message": "تم تعديل البيانات بنجاح"}), 200

        except Exception as e:
            # Handle errors and roll back session in case of failure
            logging.error(f"Error in updating person and charge: {str(e)}")
            return jsonify({"message": f"حدث خطأ: {str(e)}"}), 500


    # Fetch person data to pre-fill the form for editing
    person = get_person_by_id(person_id)
    distinctive_marks = get_distinctive_marks(person_id)
    charges = get_charges(person_id)

    return render_template('edit_person.html', person=person, distinctive_marks=distinctive_marks, charges=charges)




@app.route('/register_manager', methods=['GET', 'POST'])
def register_manager():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            if add_manager(username, password):
                flash('تمت إضافة المدير بنجاح', 'success')
               
            else:
                return jsonify({"message": "المدير موجود بالفعل"}), 409  # Conflict, since manager already exists
        except Exception as e:
            return jsonify({"message": "فشل في اضافة المدير", "error": str(e)}), 500 

    return render_template('register_manager.html')

# @app.route('/')
# def home():
#     return render_template('login_manager.html')

@app.route('/', methods=['GET', 'POST'])
@app.route('/login_manager', methods=['GET', 'POST'])
def login_manager():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # التحقق من بيانات تسجيل الدخول
        if check_login(username, password):
            session['manager'] = username
            # return 'تسجيل الدخول ناجح!'
            return render_template('dashboard.html', manager=session['manager'])
        else:
            # return 'اسم المستخدم أو كلمة المرور غير صحيحة.'
            error = "اسم المستخدم أو كلمة المرور غير صحيحة"  # Set error message
            return render_template('login_manager.html', error=error)

    return render_template('login_manager.html', error=False)

# لوحة التحكم للمديرين
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'manager' in session:
        return render_template('dashboard.html', manager=session['manager'])
    else:
        flash('يجب تسجيل الدخول للوصول إلى هذه الصفحة.')
        return redirect(url_for('login_manager'))

# مسار لتسجيل الخروج
@app.route('/logout')
def logout():
    # session.pop('manager', None)
    flash('تم تسجيل الخروج بنجاح.')
    return redirect(url_for('login_manager'))




def start_flask():
    app.run()


if __name__ == '__main__':
    threading.Thread(target=start_flask).start()
    webview.create_window(
            'مديرية امن الفيوم', 
            'http://127.0.0.1:5000', 
            resizable=True,  # Allows resizing
            min_size=(800, 600),  # Set minimum window size
            width=1024,   # Initial width
            height=768,   # Initial height
            hidden=False   # Initially show the window
        )
    webview.start()
