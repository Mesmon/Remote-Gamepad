import pygame
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()
import os

# Initialize Pygame and the joystick
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Define the server URL
server_url = os.environ.get("HOST_URL")

# Define the time interval between updates in seconds
update_interval = os.environ.get("UPDATE_INTERVAL")

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

    buttons = []
    for i in range(joystick.get_numbuttons()):
        button = joystick.get_button(i)
        buttons.append(button)
    joystick_stats["buttons"] = buttons

    hats = []
    for i in range(joystick.get_numhats()):
        hat = joystick.get_hat(i)
        hats.append(hat)
    joystick_stats["hats"] = hats

    print(joystick_stats["hats"])

    # Convert the input data to JSON format
    json_data = json.dumps(joystick_stats)
    print(json_data)
    # Send the input data as a POST request to the server
    response = session.post(server_url, data=json_data)

    # Print the response from the server
    print(response.text)
