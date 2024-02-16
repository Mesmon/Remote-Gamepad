import asyncio
from websockets.server import serve
import pyvjoy
import json

from loguru import logger

# Define constants for converting joystick input to mouse movement
MOUSE_SPEED = 20
JOYSTICK_SPEED = 2
JOYSTICK_RANGE = 32767
motion = [0, 0]

vj = pyvjoy.VJoyDevice(1)


def joystick_to_vjoy(joystick_stats):
    data = json.loads(joystick_stats)
    x_left = data["axes"][0]
    y_left = data["axes"][1]
    x_right = data["axes"][2]
    y_right = data["axes"][3]

    logger.info(int((x_left + 1) * JOYSTICK_RANGE),
                int((y_left + 1) * JOYSTICK_RANGE))

    # Update virtual joystick axes
    vj.set_axis(pyvjoy.HID_USAGE_X, int((x_left + 1) * JOYSTICK_RANGE / 2))
    vj.set_axis(pyvjoy.HID_USAGE_Y, int((y_left + 1) * JOYSTICK_RANGE / 2))

    vj.set_axis(pyvjoy.HID_USAGE_RX, int(
        (x_right + 1) * JOYSTICK_RANGE / 2))
    vj.set_axis(pyvjoy.HID_USAGE_RY, int(
        (y_right + 1) * JOYSTICK_RANGE / 2))

    buttons = data["buttons"]
    for button_index in range(len(buttons)):
        vj.set_button(button_index + 1, data["buttons"][button_index])

    hats = data["hats"]
    pov_hat_map = {
        (0, 0): -1,
        (0, 1): 0,
        (0, -1): 18000,
        (1, 0): 9000,
        (-1, 0): 27000,
        (1, 1): 4500,
        (1, -1): 13500,
        (-1, -1): 22500,
        (-1, 1): 31500,
    }
    vj.set_cont_pov(1, pov_hat_map[tuple(hats[0])])


async def handle_joystick(websocket):
    async for message in websocket:
        logger.info(f"Received: {message}")
        joystick_to_vjoy(message)
        await websocket.send("Received")
        logger.info("Sent: Received")


async def main():
    async with serve(handle_joystick, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())
