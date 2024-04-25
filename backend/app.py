from datetime import datetime
import json

from pymata4 import pymata4
from flask import Flask, jsonify
from flask_cors import CORS

import dig_calls

# DIG constants
SEND_DIG = False
IGNITION_CODE = 10000
HIGH_BEAM_CODE = 2091
HAZARD_LIGHT_CODE = 2090
LEFT_SIGNAL_CODE = 41
RIGHT_SIGNAL_CODE = 42

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
POLL_COUNT = 25

MAX_INT = 1024

LEFT_THRESH = MAX_INT // 4
RIGHT_THRESH = MAX_INT * 3 // 4

with open('config.json', 'r') as file:
    data = json.load(file)
    SERIAL_NUMBER = data['serialNo']

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
    'bl': 0,
    'br': 0,
    'hb': 0,
    'hz': 0,
}

local_state = {
    "hb_button_state": 0,
    "hz_button_state": 0,
    "left_blinker_state": 0,
    "right_blinker_state": 0,
}

def send_dig_call(value, code):
    if SEND_DIG:
        try:
            res = dig_calls.send_GenericStatusRecord(
                token=token,
                serialNo=SERIAL_NUMBER,
                code=code,
                value=value,
                timestamp=datetime.now()
            )
            assert res
        except AssertionError:
            print('sending GeneritStatusRecord failed')

def system():
    ignition, _ = board.digital_read(IGNITION_PIN)
    if ignition != state['ignition']:
        state['ignition'] = ignition
        send_dig_call(state['ignition'], IGNITION_CODE)

    hb, _ = board.digital_read(BUTTON_HB_PIN)
    if hb != local_state["hb_button_state"]:
        local_state["hb_button_state"] = hb
        if hb:
            state['hb'] = not state['hb']
            board.digital_write(LED_HB_PIN, state['hb'])
            send_dig_call(state['hb'], HIGH_BEAM_CODE)

    hz, _ = board.digital_read(BUTTON_HZ_PIN)
    if hz != local_state["hz_button_state"]:
        local_state["hz_button_state"] = hz
        if hz:
            state['hz'] = not state['hz']
            board.digital_write(LED_HZ_PIN, state['hz'])
            send_dig_call(state['hz'], HAZARD_LIGHT_CODE)

    x, _ = board.analog_read(X_PIN)
    y, _ = board.analog_read(Y_PIN)
    z, _ = board.digital_read(Z_PIN)

    state['x'] = x
    state['y'] = y
    state['z'] = z

    pot, _ = board.analog_read(POT_PIN)

    if pot < LEFT_THRESH and not state['bl']:
        state['bl'] = 1
        board.digital_pin_write(LED_L_PIN, 1)
        if not local_state["left_blinker_state"]:
            send_dig_call(state['bl'], LEFT_SIGNAL_CODE)
            local_state["left_blinker_state"] = 1
    elif pot > LEFT_THRESH and state['bl']:
        state['bl'] = 0
        board.digital_pin_write(LED_L_PIN, 0)
        if local_state["left_blinker_state"]:
            send_dig_call(state['bl'], LEFT_SIGNAL_CODE)
            local_state["left_blinker_state"] = 0
    if pot > RIGHT_THRESH and not state['br']:
        state['br'] = 1
        board.digital_pin_write(LED_R_PIN, 1)
        if not local_state["right_blinker_state"]:
            send_dig_call(state['br'], RIGHT_SIGNAL_CODE)
            local_state["right_blinker_state"] = 1
    elif pot < RIGHT_THRESH and state['br']:
        state['br'] = 0
        board.digital_pin_write(LED_R_PIN, 0)
        if local_state["right_blinker_state"]:
            send_dig_call(state['br'], RIGHT_SIGNAL_CODE)
            local_state["right_blinker_state"] = 0
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
    # Authentication calls for MyAdmin and DIG
    if SEND_DIG:
        try:
            MyAdmin_authenticate_flag, userId, sessionId = dig_calls.authenticate_MyAdmin()
            assert MyAdmin_authenticate_flag

            DIG_authenticate_flag, token, tokenExpiration, refreshToken, refreshTokenExpiration = dig_calls.authenticate_DIG()
            assert DIG_authenticate_flag
        except AssertionError:
            print('Authentication Error')

    app.run(debug=True, port=5000)
