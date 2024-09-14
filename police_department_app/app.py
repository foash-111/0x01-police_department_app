#!/usr/bin/python3
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
import bcrypt
import webview
import threading
from database import search_person, add_charge, add_person
from database import add_manager, check_login
import secrets
secret_key = secrets.token_hex(16)

app = Flask(__name__)
app.secret_key = secret_key



@app.route('/search_person', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        name = request.form.get('name')
        id_number = request.form.get('id_number')
        results = search_person(name, id_number)
        return jsonify(results)
    return render_template('search.html')

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
            distinctive_marks = request.form.get('distinctive_marks')
            entry_number = request.form.get('entry_number')

            charge_number = request.form.get('charge_number')
            charge_year = request.form.get('charge_year')
            police_station = request.form.get('police_station')
            crime_method = request.form.get('crime_method')

            # Add person and retrieve person_id
            person_id = add_person(
                name, alias, reputation, age, nationality, id_number,
                residence, profession, workplace, military_service,
                distinctive_marks, entry_number
            )

            # Add charge related to person
            add_charge(
                person_id, charge_number, charge_year, police_station, crime_method
            )

            return jsonify({"message": "تمت إضافة البيانات والتهمة بنجاح"})
        except Exception as e:
            return jsonify({"message": f"حدث خطأ: {str(e)}"})
    return render_template('add_person.html')

@app.route('/register_manager', methods=['GET', 'POST'])
def register_manager():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # إضافة المدير إلى قاعدة البيانات
        try:
            add_manager(username, password)
            # return 'تم إضافة المدير بنجاح.'
            return redirect(url_for('login_manager'))
        except Exception as e:
            # return 'فشل في إضافة المدير: '
            return redirect(url_for('register_manager'))

    return render_template('register_manager.html')

# @app.route('/')
# def home():
#     return render_template('login_manager.html')

@app.route('/')
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
            return redirect(url_for('login_manager'))

    return render_template('login_manager.html')

# لوحة التحكم للمديرين
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'manager' in session:
        return f"<h1>مرحبًا بك، {session['manager']}!</h1>"
    else:
        flash('يجب تسجيل الدخول للوصول إلى هذه الصفحة.')
        return redirect(url_for('login_manager'))

# مسار لتسجيل الخروج
@app.route('/logout')
def logout():
    session.pop('manager', None)
    flash('تم تسجيل الخروج بنجاح.')
    return redirect(url_for('login_manager'))




def start_flask():
    app.run()

if __name__ == '__main__':
    threading.Thread(target=start_flask).start()
    webview.create_window('برنامج البحث', 'http://localhost:5000/')
    webview.start()
