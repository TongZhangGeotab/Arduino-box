import time

from pymata4 import pymata4

# Callback data indices
CB_PIN_MODE = 0
CB_PIN = 1
CB_VALUE = 2
CB_TIME = 3

# Pinout constants
IGNITION_PIN = 2

X1_PIN = 0
Y1_PIN = 1
Z1_PIN = 3

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

board = pymata4.Pymata4()

def pot_handler(data):
    print(data)
    if data < 256:
        message['bl'] = True
        board.digital_pin_write(LED_L_PIN, 1)
    else:
        message['bl'] = False
        board.digital_pin_write(LED_L_PIN, 0)
    if data > 768:
        message['br'] = True
        board.digital_pin_write(LED_L_PIN, 1)
    else:
        message['br'] = False
        board.digital_pin_write(LED_L_PIN, 0)

board.set_pin_mode_digital_input(IGNITION_PIN)

board.set_pin_mode_analog_input(X1_PIN)
board.set_pin_mode_analog_input(Y1_PIN)
board.set_pin_mode_digital_input(Z1_PIN)

board.set_pin_mode_analog_input(POT_PIN)

board.set_pin_mode_digital_output(LED_L_PIN)
board.set_pin_mode_digital_output(LED_R_PIN)

board.set_pin_mode_digital_input(BUTTON_HB_PIN)
board.set_pin_mode_digital_input(BUTTON_HZ_PIN)

board.set_pin_mode_digital_output(LED_HB_PIN)
board.set_pin_mode_digital_output(LED_HZ_PIN)

def system():
    hb_button_state = 0
    hz_button_state = 0
    while True:
        time.sleep(0.1)
        ignition, _ = board.digital_read(IGNITION_PIN)
        if ignition != message['ignition']:
            message['ignition'] = ignition
            print(f"ignition pin: {IGNITION_PIN}, val: {ignition}")

        hb, _ = board.digital_read(BUTTON_HB_PIN)
        if hb != hb_button_state:
            hb_button_state = hb
            if hb:
                message['hb'] = not message['hb']
                board.digital_write(LED_HB_PIN, message['hb'])
                print(f"high beam pin: {BUTTON_HB_PIN}, val: {message['hb']}")

        hz, _ = board.digital_read(BUTTON_HZ_PIN)
        if hz != hz_button_state:
            hz_button_state = hz
            if hz:
                message['hz'] = not message['hz']
                board.digital_write(LED_HZ_PIN, message['hz'])
                print(f"hazard pin: {BUTTON_HZ_PIN}, val: {message['hz']}")

        x1, _ = board.analog_read(X1_PIN)
        y1, _ = board.analog_read(Y1_PIN)
        z1, _ = board.digital_read(Z1_PIN)

        message['pos_x'] = x1
        message['pos_y'] = y1
        message['z1'] = z1

        pot, _ = board.analog_read(POT_PIN)

        if pot < 256 and not message['bl']:
            message['bl'] = True
            board.digital_pin_write(LED_L_PIN, 1)
        elif pot > 256 and message['bl']:
                message['bl'] = False
                board.digital_pin_write(LED_L_PIN, 0)
        if pot > 768 and not message['br']:
                message['br'] = True
                board.digital_pin_write(LED_R_PIN, 1)
        elif pot < 768 and message['br']:
                message['br'] = False
                board.digital_pin_write(LED_R_PIN, 0)
        print(x1, y1, z1, pot)

system()
