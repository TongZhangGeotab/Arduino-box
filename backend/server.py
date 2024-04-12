import asyncio
import websockets
from pymata4 import pymata4

X_PIN = 0
Y_PIN = 1
Z_PIN = 12

board = pymata4.Pymata4()

board.set_pin_mode_analog_input(X_PIN)
board.set_pin_mode_analog_input(Y_PIN)
board.set_pin_mode_digital_input(Z_PIN)

async def send_keyboard_input(websocket, path):
    while True:
        await asyncio.sleep(0.1)
        x, time_stamp = board.analog_read(X_PIN)
        y, _ = board.analog_read(Y_PIN)
        z, _ = board.digital_read(Z_PIN)
        print(x, y, z, time_stamp)
        await websocket.send(f"{x}, {y}, {z}, {time_stamp}")

async def main():
    # Start the WebSocket server
    server = await websockets.serve(send_keyboard_input, "localhost", 6789)
    print("WebSocket server started.")
    await server.wait_closed()  # Run until the server is stopped


# Run the event loop
asyncio.run(main())