from flask import Flask, request
import threading
import pyvjoy
import logging

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

app = Flask(__name__)

# Define constants for converting joystick input to mouse movement
MOUSE_SPEED = 20
JOYSTICK_SPEED = 2
motion = [0, 0]


@app.route("/input", methods=["POST"])
def handle_input():
    # Initialize virtual joystick
    vj = pyvjoy.VJoyDevice(1)
    data = request.json

    x_left = data["axes"][0]
    y_left = data["axes"][1]
    x_right = data["axes"][2]
    y_right = data["axes"][3]

    print(int((x_left + 1) * 32767), int((y_left + 1) * 32767))
    # Update virtual joystick axes
    vj.set_axis(pyvjoy.HID_USAGE_X, int((x_left + 1) * 32767 / 2))
    vj.set_axis(pyvjoy.HID_USAGE_Y, int((y_left + 1) * 32767 / 2))

    vj.set_axis(pyvjoy.HID_USAGE_RX, int((x_right + 1) * 32767 / 2))
    vj.set_axis(pyvjoy.HID_USAGE_RY, int((y_right + 1) * 32767 / 2))

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

    # events = data["events"]
    # # Iterate over input events and process each one
    # for event in events:
    #     if event["type"] == "joystick":
    #         x = event["x"]
    #         y = event["y"]

    #         # Update virtual joystick axes
    #         j.set_axis(pyvjoy.HID_USAGE_X, int((x + 1) * 32767))
    #         j.set_axis(pyvjoy.HID_USAGE_Y, int((y + 1) * 32767))

    #     elif event["type"] == "quit":
    #         j.reset()
    #         j.close()
    #         # Quit the application
    #         return "Application terminated."
    return "Input received."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
