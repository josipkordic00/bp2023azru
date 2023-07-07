from model import *
from model.relacije import *
from model.cache import region
from flask import Flask, request, render_template
from flask import jsonify
import json
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

def json_deserializer(data):
    return json.loads(data)
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

if __name__ == '__main__':
    app.run(debug=True)