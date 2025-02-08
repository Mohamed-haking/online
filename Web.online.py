from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import random

app = Flask(__name__)
socketio = SocketIO(app)

rooms = {}  # تخزين الغرف العشوائية

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('find_partner')
def find_partner():
    room_id = None
    for room, users in rooms.items():
        if len(users) == 1:
            room_id = room
            break
    
    if room_id is None:
        room_id = str(random.randint(1000, 9999))
        rooms[room_id] = []
    
    join_room(room_id)
    rooms[room_id].append(request.sid)
    
    if len(rooms[room_id]) == 2:
        emit('partner_found', {'room': room_id}, room=room_id)

@socketio.on('send_message')
def send_message(data):
    emit('receive_message', data, room=data['room'])

@socketio.on('send_offer')
def send_offer(data):
    emit('receive_offer', data, room=data['room'])

@socketio.on('send_answer')
def send_answer(data):
    emit('receive_answer', data, room=data['room'])

@socketio.on('send_candidate')
def send_candidate(data):
    emit('receive_candidate', data, room=data['room'])

@socketio.on('disconnect')
def disconnect():
    for room, users in rooms.items():
        if request.sid in users:
            users.remove(request.sid)
            if not users:
                del rooms[room]
            break

if __name__ == '__main__':
    socketio.run(app, debug=True)
