from model import *
from model.relacije import *
from model.cache import region
from flask import Flask, request, render_template
from flask import jsonify
from flask_wtf.csrf import CSRFProtect
import json
from flask_socketio import SocketIO, emit
from sqlalchemy.exc import InvalidRequestError
from flask_cors import CORS
from datetime import datetime
from flask import redirect, url_for
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with your secret key
csrf = CSRFProtect(app)
def json_serializer(data):
    return json.dumps(data).encode('utf-8')

def json_deserializer(data):
    return json.loads(data)

#routes
@app.route("/evidentions")
def evidentions():
    evd = session.query(Ucenik).all()
    return render_template('evidentions.html', evd=evd)
@app.route("/classrooms")
def classrooms():
    classes = session.query(Ucenik).all()
    return render_template('classrooms.html', classes=classes)

@app.route("/")
def index():
    index = session.query(Ucionica).all()
    return render_template('index.html', index=index)
@app.route("/notifications")
def notifications():
    notif = session.query(Nastavnik).all()
    return render_template('notifications.html', notif=notif)
@app.route('/readNotification')
def read():
    notification_id = request.args.get('id')
    return render_template('readNotification.html', notification_id=notification_id)
@app.route('/reserve')
def reserve():
    classroom_id = request.args.get('id')
    return render_template('reserve.html', classroom_id=classroom_id)
@app.route('/admin')
def admin():
    teachers = session.query(Nastavnik).all()
    students = session.query(Ucenik).all()
    institutions = session.query(Ustanova).all()
    classrooms = session.query(Ucionica).all()
    data = {
        'teachers': teachers,
        'students': students,
        'institutions': institutions,
        'classrooms': classrooms
    }
    return render_template('admin.html', data=data)

@app.route('/insertStudent', methods=['GET', 'POST'])
def insertStudent():
    if request.method == 'POST':
        try:
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")
            email = request.form.get("email")
            password = request.form.get("password")
            phone = request.form.get("phone")
            student = Ucenik(
                ime=first_name,
                prezime=last_name,
                email=email,
                sifra=password,
                broj_telefona=phone
            )

            if not session.in_transaction():
                with session.begin():
                    session.add(student)
            else:
                session.add(student)

            return redirect(url_for('admin'))
        except Exception as e:
            return jsonify({'error': str(e)})

   
    students = session.query(Ucenik).all()
    data = {
        'students': students
    }
    return render_template('insertStudent.html', data=data)
@app.route('/insertTeacher', methods=['GET', 'POST'])
def insertTeacher():
    if request.method == 'POST':
        try:
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")
            email = request.form.get("email")
            password = request.form.get("password")
            phone = request.form.get("phone")
            teacher = Nastavnik(
                ime=first_name,
                prezime=last_name,
                email=email,
                sifra=password,
                broj_telefona=phone
            )

            if not session.in_transaction():
                with session.begin():
                    session.add(teacher)
            else:
                session.add(teacher)

            return redirect(url_for('admin'))
        except Exception as e:
            return jsonify({'error': str(e)})

   
    teachers = session.query(Ucenik).all()
    data = {
        'teachers': teachers
    }
    return render_template('insertTeacher.html', data=data)


@app.route('/admin/deleteStudent/<int:id>', methods=['DELETE'])
def deleteStudent(id):
     student = session.query(Ucenik).get(id)
     if student:
        session.delete(student)
        session.commit()
        return jsonify({'message': f'student sa ID {student} je izbrisan.'}), 200

@app.route('/admin/deleteTeacher/<int:id>', methods=['DELETE'])
def deleteTeacher(id):
     teacher = session.query(Nastavnik).get(id)
     if teacher:
        session.delete(teacher)
        session.commit()
        return jsonify({'message': f'teacher sa ID {teacher} je izbrisan.'}), 200











@app.route("/evd/evidention")
def get_evidention():
    evidentions = session.query(Evidencija).join(Evidencija.ustanova).join(Evidencija.ucionica).all()
    serialized_evidentions = [
        {
            "id": evidention.id,
            "institution_name": evidention.ustanova.naziv,
            "students": evidention.ucenici,
            "classroom_number": evidention.ucionica.broj_ucionice,
            "date": evidention.datum
        }
        for evidention in evidentions
    ] 
    return jsonify(serialized_evidentions)

@app.route("/index/classroom")
def get_classroom_info():
    classrooms = session.query(Ucionica).join(Ucionica.ustanova).join(Ucionica.nastavnik).all()
    serialized_classrooms = [
        {
            "id": classroom.id,
            "classroom_number": classroom.broj_ucionice,
            "institution": classroom.ustanova.naziv,
            "teacher_name": classroom.nastavnik.ime,
            "teacher_surname": classroom.nastavnik.prezime,
            "date": classroom.datum_rezervacije,
            "taken":classroom.zauzeto
        }
        for classroom in classrooms
    ] 
    return jsonify(serialized_classrooms)
@app.route("/notif/notifications")
def get_notifications():
    notifications = session.query(Obavijesti).join(Obavijesti.nastavnik).all()
    serialized_notifications = [
        {
            "id": notification.id,
            "teacher_name": notification.nastavnik.ime,
            "teacher_surname": notification.nastavnik.prezime,
            "text": notification.text
        }
        for notification in notifications
    ] 
    return jsonify(serialized_notifications)

@app.route("/classes/classrooms")
def get_classrooms():
    classrooms = session.query(Ucionica).join(Ucionica.ustanova).join(Ucionica.nastavnik).all()
    serialized_classrooms = [
        {
            "id": classroom.id,
            "classroom_number": classroom.broj_ucionice,
            "teacher_name": classroom.nastavnik_ime,
            "teacher_surname": classroom.nastavnik_prezime,
            "taken": classroom.zauzeto,
            "institution": classroom.ustanova_naziv
        }
        for classroom in classrooms
    ] 
    return jsonify(serialized_classrooms)
@app.route("/classroom/edit", methods=["PUT"])
def edit_date():
    id = request.args.get("id")
    date = request.json.get("date")  
    if id and date:
        # Fetch the classroom object based on the provided ID
        classroom = session.query(Ucionica).get(id)
        if classroom:
            # Convert the provided date string to a datetime object
            updated_date = datetime.strptime(date, "%Y-%m-%d %H:%M")
            classroom.datum_rezervacije = updated_date

            session.commit()
            return jsonify({'message': f'Razred sa ID {id} je ažuriran.'}), 200
        else:
            return jsonify({'message': f'Nema razreda s ID {id}.'}), 404
    else:
        return jsonify({'message': 'ID ili datum nisu pruženi.'}), 400
@app.route("/admin/all")
def get_all():
    classrooms = session.query(Ucionica).all()
    students = session.query(Ucenik).all()
    teachers = session.query(Nastavnik).all()
    institutions = session.query(Ustanova).all()
    serialized_classrooms = [
        {
            "id": classroom.id,
            "classroom_number": classroom.broj_ucionice,
            "institution": classroom.ustanova_id
        }
        for classroom in classrooms
    ]
    serialized_students = [
        {
            "id": student.id,
            "first_name": student.ime,
            "last_name": student.prezime,
            "email": student.email,
            "password": student.sifra
        }
        for student in students
    ]
    serialized_teachers = [
        {
            "id": teacher.id,
            "first_name": teacher.ime,
            "last_name": teacher.prezime,
            "email": teacher.email,
            "password": teacher.sifra
        }
        for teacher in teachers
    ]
    serialized_institutions = [
        {
            "id": institution.id,
            "name": institution.naziv,
            "address": institution.adresa
        }
        for institution in institutions
    ]
    return jsonify(serialized_classrooms, serialized_students, serialized_teachers, serialized_institutions)

if __name__ == '__main__':
    app.run(debug=True)