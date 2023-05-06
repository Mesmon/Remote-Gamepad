from flask import Flask, request
import threading
import pyvjoy

app = Flask(__name__)

# Define constants for converting joystick input to mouse movement
MOUSE_SPEED = 20
JOYSTICK_SPEED = 2
motion = [0, 0]

@app.route("/input", methods=["POST"])
def handle_input():
    # Initialize virtual joystick
    j = pyvjoy.VJoyDevice(1)

    data = request.get_json()
    events = data["events"]
    # Iterate over input events and process each one
    for event in events:
        if event["type"] == "joystick":
            x = event["x"]
            y = event["y"]

            # Update virtual joystick axes
            j.set_axis(pyvjoy.HID_USAGE_X, int((x + 1) * 32767))
            j.set_axis(pyvjoy.HID_USAGE_Y, int((y + 1) * 32767))

        elif event["type"] == "quit":
            j.reset()
            j.close()
            # Quit the application
            return "Application terminated."
    return "Input received."


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
