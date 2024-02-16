from websockets.sync.client import connect
import os
import pygame
import json
import time
from loguru import logger
from dotenv import load_dotenv
load_dotenv()

# Initialize Pygame and the joystick
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Define the server URL
server_url = os.environ.get("HOST_URL")

# Define the time interval between updates in seconds
update_interval = float(os.environ.get("UPDATE_INTERVAL"))

# Continuously send joystick input to the server every 20 ms


def joystick_data_message_producer(websocket):
    while True:
        # time.sleep(update_interval)
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

        logger.info(joystick_stats["hats"])

        # Convert the input data to JSON format
        json_data = json.dumps(joystick_stats)
        # Send the input data as a POST request to the server
        websocket.send(json_data)
        message = websocket.recv()
        # Print the response from the server
        logger.info(f"Received: {message}")


def send_joystick_data():
    with connect("ws://localhost:8765") as websocket:
        joystick_data_message_producer(websocket)


send_joystick_data()
