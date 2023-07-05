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
@app.route("/")
def index():
    api = session.query(Ucenik).all()
    return render_template('evidention.html', api=api)
    
@app.route("/api/students")
def getStudents():
    students = session.query(Ucenik).all()
    serialized_students = [{"id": student.id, "ime": student.ime, "prezime": student.prezime, "email": student.email, "sifra": student.sifra, "broj_telefona": student.broj_telefona, "prisutnost": student.prisutnost} for student in students]
    return jsonify(serialized_students)


if __name__ == '__main__':
    app.run()