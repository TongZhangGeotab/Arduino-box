

from flask import Flask, jsonify
from flask_socketio import SocketIO
import time
from pymata4 import pymata4


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

IGNITION_PIN = 2

message = {
    'ignition': 0,
    'pos_x': 0,
    'pos_y': 0,
    'z1': 0,
    'v': 0,
    'angle': 0,
    'bl': 0,
    'br': 0,
    'hb': 0,
    'hz': 0
}


def update_system():
    board = pymata4.Pymata4()
    board.set_pin_mode_digital_input(IGNITION_PIN)

    global message
    while True:
        ignition, _ = board.digital_read(IGNITION_PIN)
        if ignition != message['ignition']:
            message['ignition'] = ignition
            socketio.emit('state', message)
        socketio.sleep(0.1)  # Use socketio.sleep instead of time.sleep

@app.route('/state')
def get_state():
    return jsonify(message)

if __name__ == '__main__':
    # Start the system update as a background task
    socketio.start_background_task(update_system)
    # Run the Flask app with SocketIO integration
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)