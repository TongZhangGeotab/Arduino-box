import threading
import time

from pymata4 import pymata4
from flask import Flask, jsonify
from flask_cors import CORS

# Callback data indices
CB_PIN_MODE = 0
CB_PIN = 1
CB_VALUE = 2
CB_TIME = 3

# Pinout constants
IGNITION_PIN = 2

X_PIN = 0
Y_PIN = 1
Z_PIN = 3

POT_PIN = 2

BUTTON_HB_PIN = 4
BUTTON_HZ_PIN = 5

LED_L_PIN = 6
LED_R_PIN = 7

LED_HB_PIN = 8
LED_HZ_PIN = 9

# Constant values
CYCLE_TIME = 0.1

MAX_INT = 1024

LEFT_THRESH = MAX_INT // 3 - 1
RIGHT_THRESH = MAX_INT * 2 // 3 - 1

board = pymata4.Pymata4()

board.set_pin_mode_digital_input(IGNITION_PIN)

board.set_pin_mode_analog_input(X_PIN)
board.set_pin_mode_analog_input(Y_PIN)
board.set_pin_mode_digital_input(Z_PIN)

board.set_pin_mode_analog_input(POT_PIN)

board.set_pin_mode_digital_output(LED_L_PIN)
board.set_pin_mode_digital_output(LED_R_PIN)

board.set_pin_mode_digital_input(BUTTON_HB_PIN)
board.set_pin_mode_digital_input(BUTTON_HZ_PIN)

board.set_pin_mode_digital_output(LED_HB_PIN)
board.set_pin_mode_digital_output(LED_HZ_PIN)

state = {
    'ignition': 0,
    'x': 0,
    'y': 0,
    'z': 0,
    'speed': 0,
    'angle': 0,
    'bl': 0,
    'br': 0,
    'hb': 0,
    'hz': 0,
}

hb_button_state = 0
hz_button_state = 0

def system():
    global hb_button_state
    global hz_button_state

    ignition, _ = board.digital_read(IGNITION_PIN)
    if ignition != state['ignition']:
        state['ignition'] = ignition

    hb, _ = board.digital_read(BUTTON_HB_PIN)
    if hb != hb_button_state:
        hb_button_state = hb
        if hb:
            state['hb'] = not state['hb']
            board.digital_write(LED_HB_PIN, state['hb'])

    hz, _ = board.digital_read(BUTTON_HZ_PIN)
    if hz != hz_button_state:
        hz_button_state = hz
        if hz:
            state['hz'] = not state['hz']
            board.digital_write(LED_HZ_PIN, state['hz'])

    x, _ = board.analog_read(X_PIN)
    y, _ = board.analog_read(Y_PIN)
    z, _ = board.digital_read(Z_PIN)

    state['x'] = x
    state['y'] = y
    state['z'] = z

    pot, _ = board.analog_read(POT_PIN)

    if pot < 256 and not state['bl']:
        state['bl'] = 1
        board.digital_pin_write(LED_L_PIN, 1)
    elif pot > 256 and state['bl']:
            state['bl'] = 0
            board.digital_pin_write(LED_L_PIN, 0)
    if pot > 768 and not state['br']:
            state['br'] = 1
            board.digital_pin_write(LED_R_PIN, 1)
    elif pot < 768 and state['br']:
            state['br'] = 0
            board.digital_pin_write(LED_R_PIN, 0)

    print(state)


# App setup
app = Flask(__name__)
CORS(app)

@app.route('/api/state')
def get_data():
    system()
    state_data = jsonify(state)
    print(state_data)
    return state_data

if __name__ == "__main__":
    app.run(debug=True, port=5000)