import pygame
import requests
import json
import time

# Initialize Pygame and the joystick
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(1)
joystick.init()

# Define the server URL
server_url = "http://localhost:5000/input"

# Define the time interval between updates in seconds
update_interval = 0.2

# Start the HTTP session
session = requests.Session()
# Set the headers to indicate that the payload is JSON
headers = {"Content-type": "application/json"}
session.headers.update(headers)

# Continuously send joystick input to the server every 20 ms
while True:
    time.sleep(update_interval)
    pygame.event.pump()
    joystick_stats = {}

    # Axes
    axes = []
    for i in range(joystick.get_numaxes()):
        axis = joystick.get_axis(i)
        axes.append(axis)
    joystick_stats["axes"] = axes

    # # Get the current joystick input values
    # x_axis = joystick.get_axis(0)
    # y_axis = joystick.get_axis(1)
    # buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]

    # # Define the input data as a dictionary
    # input_data = {
    #     "events": [{"type": "joystick", "x": x_axis, "y": y_axis, "buttons": buttons}]
    # }

    # Convert the input data to JSON format
    json_data = json.dumps(joystick_stats)
    print(json_data)
    # Send the input data as a POST request to the server
    # response = session.post(server_url, data=json_data)

    # Print the response from the server
    # print(response.text)
